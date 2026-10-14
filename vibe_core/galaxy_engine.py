#!/usr/bin/env python3
"""
galaxy_engine.py — High-Performance Offline Search Engine for Uiverse Galaxy (3000+ UI components)
Provides sub-10ms search over local micro-interactions, buttons, loaders, cards, inputs, and toggles.
"""

import json
import re
import time
from pathlib import Path
from typing import Dict, List, Optional, Any

ROOT_DIR = Path(__file__).resolve().parent.parent
DEFAULT_GALAXY_DIR = ROOT_DIR / "data" / "uiverse-galaxy"
DEFAULT_INDEX_PATH = ROOT_DIR / "data" / "galaxy_index.json"

TAGS_PATTERN = re.compile(
    r"From\s+Uiverse\.io\s+by\s+([^\s\-]+)\s*-\s*Tags:\s*([^\*\/]+)",
    re.IGNORECASE
)
STYLE_PATTERN = re.compile(
    r"<style\b[^>]*>(.*?)</style>",
    re.IGNORECASE | re.DOTALL
)

CATEGORY_ALIASES = {
    "button": "Buttons",
    "buttons": "Buttons",
    "card": "Cards",
    "cards": "Cards",
    "checkbox": "Checkboxes",
    "checkboxes": "Checkboxes",
    "form": "Forms",
    "forms": "Forms",
    "input": "Inputs",
    "inputs": "Inputs",
    "loader": "loaders",
    "loaders": "loaders",
    "loading": "loaders",
    "notification": "Notifications",
    "notifications": "Notifications",
    "pattern": "Patterns",
    "patterns": "Patterns",
    "radio": "Radio-buttons",
    "radio-buttons": "Radio-buttons",
    "toggle": "Toggle-switches",
    "toggle-switches": "Toggle-switches",
    "switch": "Toggle-switches",
    "switches": "Toggle-switches",
    "tooltip": "Tooltips",
    "tooltips": "Tooltips"
}


class GalaxyEngine:
    """Offline indexing and ultra-fast retrieval engine for Uiverse Galaxy components."""

    def __init__(
        self,
        galaxy_dir: Optional[Path] = None,
        index_path: Optional[Path] = None,
        auto_index: bool = True
    ):
        self.galaxy_dir = Path(galaxy_dir or DEFAULT_GALAXY_DIR)
        self.index_path = Path(index_path or DEFAULT_INDEX_PATH)
        self._index: List[Dict[str, Any]] = []
        self._by_name: Dict[str, Dict[str, Any]] = {}
        self._by_path: Dict[str, Dict[str, Any]] = {}

        if auto_index:
            self.load_or_build()

    def is_galaxy_available(self) -> bool:
        return self.galaxy_dir.exists() and self.galaxy_dir.is_dir()

    def ensure_galaxy_dataset(self) -> bool:
        """Auto-provisions the 5MB offline galaxy dataset via shallow clone if missing."""
        if self.is_galaxy_available():
            return True
        try:
            import subprocess
            import sys
            print("🌌 [Galaxy] Offline dataset not found. Auto-cloning library (~5MB)...", file=sys.stderr)
            self.galaxy_dir.parent.mkdir(parents=True, exist_ok=True)
            res = subprocess.run(
                ["git", "clone", "--depth", "1", "https://github.com/uiverse-io/galaxy.git", str(self.galaxy_dir)],
                capture_output=True,
                text=True,
                check=False
            )
            if res.returncode == 0:
                print("🌌 [Galaxy] Dataset successfully provisioned and cached!", file=sys.stderr)
                self.build_index()
                return True
            return False
        except Exception:
            return False

    def load_or_build(self, force: bool = False) -> None:
        """Loads cached index if available; builds and saves it if missing or stale."""
        if not force and self.index_path.exists():
            try:
                with open(self.index_path, "r", encoding="utf-8") as f:
                    self._index = json.load(f)
                self._rebuild_lookup_tables()
                return
            except Exception:
                # Fall back to rebuilding if index is corrupted
                pass

        if self.is_galaxy_available():
            self.build_index()

    def _rebuild_lookup_tables(self) -> None:
        self._by_name = {item["name"].lower(): item for item in self._index}
        self._by_path = {item["relative_path"].replace("\\", "/").lower(): item for item in self._index}

    def build_index(self) -> int:
        """Scans galaxy repository, parses metadata and writes cache file."""
        if not self.is_galaxy_available():
            self._index = []
            return 0

        items: List[Dict[str, Any]] = []

        # Scan each directory inside galaxy_dir
        for cat_dir in sorted(self.galaxy_dir.iterdir()):
            if not cat_dir.is_dir() or cat_dir.name.startswith("."):
                continue

            category = cat_dir.name

            for html_file in cat_dir.glob("*.html"):
                filename = html_file.name
                stem = html_file.stem

                # Parse author and slug: Author_slug
                if "_" in stem:
                    author, slug = stem.split("_", 1)
                else:
                    author = "uiverse"
                    slug = stem

                rel_path = f"{category}/{filename}"

                # Extract tags from HTML comment
                tags: List[str] = []
                try:
                    with open(html_file, "r", encoding="utf-8", errors="ignore") as f:
                        header = f.read(2048)
                    m = TAGS_PATTERN.search(header)
                    if m:
                        author_in_tag = m.group(1).strip()
                        if author_in_tag:
                            author = author_in_tag
                        raw_tags = m.group(2).strip()
                        tags = [t.strip().lower() for t in raw_tags.split(",") if t.strip()]
                except Exception:
                    tags = []

                if not tags:
                    # Tokenize slug as fallback tags
                    tags = [t.lower() for t in re.split(r"[-_]+", slug) if len(t) > 2]

                search_string = f"{slug} {category} {' '.join(tags)} {author}".lower()

                items.append({
                    "name": slug,
                    "author": author,
                    "category": category,
                    "tags": tags,
                    "relative_path": rel_path,
                    "title": f"{author}/{slug}",
                    "search_string": search_string
                })

        self._index = items
        self._rebuild_lookup_tables()

        # Save to disk cache
        try:
            self.index_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.index_path, "w", encoding="utf-8") as f:
                json.dump(self._index, f, indent=2, ensure_ascii=False)
        except Exception:
            pass

        return len(self._index)

    def search(
        self,
        query: str,
        category: Optional[str] = None,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Sub-10ms keyword and tag search over galaxy components.
        """
        start_time = time.perf_counter()
        if not self._index:
            self.load_or_build()

        if not self._index:
            return []

        # Normalize category filter
        target_category = None
        if category:
            cat_clean = category.strip().lower()
            target_category = CATEGORY_ALIASES.get(cat_clean, category)

        # Tokenize query
        tokens = [t.lower() for t in re.split(r"[\s\-_,]+", query) if len(t) > 1]
        exact_query = query.strip().lower()

        scored_results = []

        for item in self._index:
            # Category match check
            if target_category and item["category"].lower() != target_category.lower():
                continue

            score = 0
            name_lower = item["name"].lower()
            item_tags = item["tags"]
            search_str = item["search_string"]

            # Exact query matches
            if exact_query == name_lower:
                score += 50
            elif exact_query in item_tags:
                score += 40
            elif exact_query in search_str:
                score += 25

            # Token level matches
            for token in tokens:
                if token in item_tags:
                    score += 15
                if token in name_lower:
                    score += 12
                if token == item["category"].lower():
                    score += 8
                if token in search_str:
                    score += 4

            if score > 0:
                scored_results.append((score, item))

        scored_results.sort(key=lambda x: x[0], reverse=True)
        results = []
        for score, item in scored_results[:limit]:
            res = dict(item)
            res["score"] = score
            results.append(res)

        elapsed_ms = (time.perf_counter() - start_time) * 1000
        # Attach elapsed search latency for telemetry
        for r in results:
            r["search_time_ms"] = round(elapsed_ms, 2)

        return results

    def get_component(self, path_or_name: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves raw content, clean HTML, and CSS for a specific component.
        """
        clean_key = path_or_name.strip().replace("\\", "/").lower()

        # Find in lookup table
        item = self._by_path.get(clean_key)
        if not item:
            item = self._by_name.get(clean_key)

        if not item:
            # Try matching filename end
            for p, it in self._by_path.items():
                if p.endswith(clean_key) or it["name"].lower() == clean_key:
                    item = it
                    break

        if not item:
            return None

        file_path = self.galaxy_dir / item["relative_path"]
        if not file_path.exists():
            return None

        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            raw_content = f.read()

        # Split CSS and HTML
        css_match = STYLE_PATTERN.search(raw_content)
        css_content = css_match.group(1).strip() if css_match else ""
        html_content = STYLE_PATTERN.sub("", raw_content).strip()

        return {
            "name": item["name"],
            "author": item["author"],
            "category": item["category"],
            "tags": item["tags"],
            "relative_path": item["relative_path"],
            "title": item["title"],
            "html": html_content,
            "css": css_content,
            "raw": raw_content
        }


if __name__ == "__main__":
    engine = GalaxyEngine()
    print(f"Galaxy Engine ready. Indexed: {len(engine._index)} items.")
    sample = engine.search("neon button", limit=3)
    print("Search 'neon button':")
    print(json.dumps(sample, indent=2, ensure_ascii=False))
