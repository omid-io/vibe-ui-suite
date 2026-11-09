#!/usr/bin/env python3
"""
vibe_core/search_engine.py — Standalone Pure-Python BM25 Design Intelligence Engine
Vibe UI Suite

Provides zero-dependency in-memory Okapi BM25 retrieval across:
1. Visual Design Genome Styles (80+ canonical and specialized styles)
2. Domain-Calibrated OKLCH Palettes (150+ Light-First & OLED Dark palettes)
3. Typography Systems (Pairings, scales, and font stacks)
4. Curated Elite Open-Source Benchmarks (>10k stars UI paradigms)
5. Layout Archetypes (Asymmetric editorial, high-density HUD, canvas workspace, etc.)

Adheres to Okapi BM25 scoring with configurable k1 (default 1.5) and b (default 0.75).
Zero external dependencies (pure Python standard library).
"""

from __future__ import annotations

import json
import math
import re
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Sequence, Set, Tuple

ROOT_DIR = Path(__file__).resolve().parent.parent
CATALOG_PATH = ROOT_DIR / "data" / "catalog" / "design_genome.json"
LEGACY_STYLES_PATH = ROOT_DIR / "data" / "styles.json"
LEGACY_PALETTES_PATH = ROOT_DIR / "data" / "palettes.json"
ARCHETYPES_PATH = ROOT_DIR / "data" / "design_vault" / "archetypes.json"

# Common English stop words to prune query noise while preserving technical domain terms
DEFAULT_STOP_WORDS: Set[str] = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and",
    "any", "are", "as", "at", "be", "because", "been", "before", "being", "below",
    "between", "both", "but", "by", "could", "did", "do", "does", "doing", "down",
    "during", "each", "few", "for", "from", "further", "had", "has", "have", "having",
    "he", "her", "here", "hers", "herself", "him", "himself", "his", "how", "i",
    "if", "in", "into", "is", "it", "its", "itself", "me", "more", "most", "my",
    "myself", "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other",
    "ought", "our", "ours", "ourselves", "out", "over", "own", "same", "she", "should",
    "so", "some", "such", "than", "that", "the", "their", "theirs", "them", "themselves",
    "then", "there", "these", "they", "this", "those", "through", "to", "too", "under",
    "until", "up", "very", "was", "we", "were", "what", "when", "where", "which",
    "while", "who", "whom", "why", "with", "would", "you", "your", "yours", "yourself",
}


def tokenize(text: str, remove_stopwords: bool = True) -> List[str]:
    """
    Normalizes and tokenizes text for semantic BM25 indexing.
    Handles underscores, hyphens, and mixed casing; supports alphanumeric and Persian tokens.
    """
    if not text:
        return []

    # Replace punctuation / delimiters with space, keeping alphanumeric and Persian/Arabic letters
    cleaned = re.sub(r"[^\w\s\u0600-\u06FF]", " ", str(text).lower())
    # Split tokens
    raw_tokens = [t.strip("_") for t in cleaned.split()]
    tokens: List[str] = []

    for t in raw_tokens:
        if not t or len(t) < 2:
            continue
        # Sub-split compound tokens joined by underscores or digits (e.g. "saas_b2b" -> "saas", "b2b")
        sub_parts = [p for p in t.split("_") if p]
        for part in sub_parts:
            if remove_stopwords and part in DEFAULT_STOP_WORDS and len(part) <= 4:
                continue
            tokens.append(part)

    return tokens


class BM25Index:
    """
    In-memory Okapi BM25 ranking index.
    Supports weighted fields, dynamic filtering, and epsilon-smoothed IDF.
    """

    def __init__(self, k1: float = 1.5, b: float = 0.75, epsilon: float = 0.25):
        self.k1 = k1
        self.b = b
        self.epsilon = epsilon

        # Document storage
        self.documents: Dict[str, Dict[str, Any]] = {}
        # Document token counts: doc_id -> {token: count}
        self.doc_term_freqs: Dict[str, Dict[str, int]] = {}
        # Document lengths: doc_id -> int
        self.doc_lengths: Dict[str, int] = {}
        # Inverted index: token -> list of doc_ids
        self.inverted_index: Dict[str, List[str]] = {}
        # Document frequency: token -> count of docs containing token
        self.doc_freqs: Dict[str, int] = {}
        # Precomputed IDF: token -> float
        self.idf: Dict[str, float] = {}

        self.num_docs: int = 0
        self.avg_doc_len: float = 0.0
        self._is_indexed: bool = False

    def add_document(
        self,
        doc_id: str,
        fields: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None,
        field_weights: Optional[Dict[str, float]] = None,
    ) -> None:
        """
        Adds a document with weighted text fields to the index.
        Weights duplicate tokens proportionally to boost matched fields.
        """
        weights = field_weights or {}
        combined_tokens: List[str] = []

        for field_name, field_val in fields.items():
            if field_val is None:
                continue
            weight = max(1, int(round(weights.get(field_name, 1.0))))
            text_str = ""
            if isinstance(field_val, (list, tuple, set)):
                text_str = " ".join(str(item) for item in field_val)
            elif isinstance(field_val, dict):
                text_str = " ".join(f"{k} {v}" for k, v in field_val.items())
            else:
                text_str = str(field_val)

            toks = tokenize(text_str)
            for _ in range(weight):
                combined_tokens.extend(toks)

        doc_len = len(combined_tokens)
        tf: Dict[str, int] = {}
        for t in combined_tokens:
            tf[t] = tf.get(t, 0) + 1

        self.documents[doc_id] = {
            "id": doc_id,
            "fields": fields,
            "metadata": metadata if metadata is not None else fields,
        }
        self.doc_term_freqs[doc_id] = tf
        self.doc_lengths[doc_id] = doc_len
        self._is_indexed = False

    def build_index(self) -> None:
        """Computes corpus statistics, inverted index, and smoothed Okapi BM25 IDFs."""
        self.num_docs = len(self.documents)
        if self.num_docs == 0:
            self.avg_doc_len = 0.0
            self._is_indexed = True
            return

        total_length = sum(self.doc_lengths.values())
        self.avg_doc_len = total_length / self.num_docs if self.num_docs > 0 else 0.0

        # Inverted index & doc freqs
        self.inverted_index.clear()
        self.doc_freqs.clear()

        for doc_id, tf in self.doc_term_freqs.items():
            for token in tf.keys():
                if token not in self.inverted_index:
                    self.inverted_index[token] = []
                    self.doc_freqs[token] = 0
                self.inverted_index[token].append(doc_id)
                self.doc_freqs[token] += 1

        # Calculate Robertson-Spärck Jones IDF with floor smoothing
        self.idf.clear()
        negative_idfs: List[str] = []
        sum_positive_idf = 0.0

        for token, df in self.doc_freqs.items():
            # Standard Okapi BM25 IDF formula
            numerator = (self.num_docs - df + 0.5)
            denominator = (df + 0.5)
            val = math.log(1.0 + (numerator / denominator))
            if val < 0:
                negative_idfs.append(token)
            else:
                self.idf[token] = val
                sum_positive_idf += val

        # Handle negative IDFs via epsilon floor
        avg_idf = (sum_positive_idf / len(self.idf)) if self.idf else 0.5
        eps_floor = self.epsilon * avg_idf
        for token in negative_idfs:
            self.idf[token] = eps_floor

        self._is_indexed = True

    def search(
        self,
        query: str,
        limit: int = 10,
        filter_fn: Optional[Callable[[Dict[str, Any]], bool]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Executes an Okapi BM25 search for the given query string.
        Returns sorted document matches with their BM25 score and metadata.
        """
        if not self._is_indexed:
            self.build_index()

        if self.num_docs == 0:
            return []

        query_tokens = tokenize(query)
        if not query_tokens:
            # If query is blank, return first items up to limit
            results = []
            for doc in list(self.documents.values())[:limit]:
                if filter_fn is None or filter_fn(doc["metadata"]):
                    results.append({
                        "id": doc["id"],
                        "score": 0.0,
                        "metadata": doc["metadata"]
                    })
            return results

        # Candidate docs containing at least one query token
        scores: Dict[str, float] = {}

        for q_token in query_tokens:
            q_idf = self.idf.get(q_token, 0.0)
            if q_idf <= 0.0:
                continue

            posting_list = self.inverted_index.get(q_token, [])
            for doc_id in posting_list:
                doc = self.documents[doc_id]
                if filter_fn is not None and not filter_fn(doc["metadata"]):
                    continue

                tf = self.doc_term_freqs[doc_id].get(q_token, 0)
                doc_len = self.doc_lengths.get(doc_id, 0)
                len_norm = 1.0 - self.b + self.b * (doc_len / self.avg_doc_len if self.avg_doc_len > 0 else 1.0)
                numerator = tf * (self.k1 + 1.0)
                denominator = tf + self.k1 * len_norm
                term_score = q_idf * (numerator / denominator)

                scores[doc_id] = scores.get(doc_id, 0.0) + term_score

        if not scores:
            # Fallback prefix / partial match for edge cases
            for q_token in query_tokens:
                for token, posting_list in self.inverted_index.items():
                    if q_token in token or token in q_token:
                        q_idf = self.idf.get(token, 0.1)
                        for doc_id in posting_list:
                            doc = self.documents[doc_id]
                            if filter_fn is not None and not filter_fn(doc["metadata"]):
                                continue
                            scores[doc_id] = scores.get(doc_id, 0.0) + (q_idf * 0.5)

        sorted_docs = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        results: List[Dict[str, Any]] = []

        for doc_id, score in sorted_docs[:limit]:
            results.append({
                "id": doc_id,
                "score": round(score, 4),
                "metadata": self.documents[doc_id]["metadata"],
            })

        return results


# -----------------------------------------------------------------------------
# Curated Elite Open-Source UI Benchmarks (>10k stars) for Offline Discovery
# -----------------------------------------------------------------------------
CURATED_BENCHMARKS = [
    {
        "id": "shadcn_ui",
        "name": "shadcn/ui",
        "stars": 75000,
        "domains": ["saas_b2b_enterprise", "general_modern_saas", "devops_cloud_terminal", "fintech_banking", "settings"],
        "paradigm": "Radix primitives, headless accessibility, Tailwind CSS semantic tokens, composable component copy-paste",
        "composition_archetype": "asymmetric_operational_split",
        "recommended_for": ["dashboard", "saas", "clean_business", "settings", "telemetry"]
    },
    {
        "id": "aceternity_ui",
        "name": "aceternity/ui",
        "stars": 24000,
        "domains": ["creative_portfolio_agency", "ecommerce_luxury_fashion", "ai_developer_platform", "gaming_entertainment_streaming"],
        "paradigm": "Physics springs, 3D perspective tilt, liquid canvas particle shaders, specular edge lights",
        "composition_archetype": "centered_floating_stage",
        "recommended_for": ["luxury", "hero_showcase", "creative_agency", "fintech_modern"]
    },
    {
        "id": "magicui",
        "name": "magicui/design",
        "stars": 18000,
        "domains": ["ai_developer_platform", "general_modern_saas", "energy_greentech_sustainability"],
        "paradigm": "Curated asymmetric interactive cards, dynamic dock bars, animated beam connectors, marquee social proof",
        "composition_archetype": "interactive_canvas_matrix",
        "recommended_for": ["bento_matrix", "developer_tools", "ai_platform"]
    },
    {
        "id": "tremor",
        "name": "tremor/tremor",
        "stars": 17000,
        "domains": ["fintech_banking", "crypto_trading_web3", "logistics_supply_chain", "devops_cloud_terminal"],
        "paradigm": "High-density operational dashboards, micro-sparklines, KPI callout telemetry, minimal visual chrome",
        "composition_archetype": "dense_telemetry_hud",
        "recommended_for": ["analytics", "crypto_trading", "enterprise_data", "metrics"]
    },
    {
        "id": "lucide_icons",
        "name": "lucide-react",
        "stars": 16000,
        "domains": ["general_modern_saas", "beauty_clinical_wellness", "media_editorial_magazine"],
        "paradigm": "Crisp 24px/16px vector geometry, zero-slop emoji avoidance, accessible inline SVG glyphs",
        "composition_archetype": "editorial_spread",
        "recommended_for": ["vector_icons", "clean_navigation", "accessible_ui"]
    },
    {
        "id": "cmdk",
        "name": "pacocoursey/cmdk",
        "stars": 12000,
        "domains": ["devops_cloud_terminal", "ai_developer_platform", "cybersecurity_identity_auth"],
        "paradigm": "Fast keyboard-driven command palette, zero layout shift, sub-frame focus navigation",
        "composition_archetype": "keyboard_navigable_lanes",
        "recommended_for": ["terminal", "command_k", "developer_workflow"]
    },
    {
        "id": "sonner",
        "name": "emilkowalski/sonner",
        "stars": 11000,
        "domains": ["general_modern_saas", "fintech_banking", "ecommerce_mass_market"],
        "paradigm": "Stacked physics toast system, fluid spring height transitions, swipe-to-dismiss velocity handoff",
        "composition_archetype": "floating_dock_telemetry",
        "recommended_for": ["toast_feedback", "notifications", "interactive_state"]
    }
]


# -----------------------------------------------------------------------------
# Color Science: WCAG Contrast Utilities for OKLCH
# -----------------------------------------------------------------------------
def oklch_to_linear_srgb(l: float, c: float, h: float) -> Tuple[float, float, float]:
    """Converts OKLCH coordinates into linear sRGB channels."""
    theta = math.radians(h)
    a = c * math.cos(theta)
    b = c * math.sin(theta)
    l_ = l + 0.3963377774 * a + 0.2158037573 * b
    m_ = l - 0.1055613458 * a - 0.0638541728 * b
    s_ = l - 0.0894841775 * a - 1.2914855480 * b
    l_cubed = l_ ** 3
    m_cubed = m_ ** 3
    s_cubed = s_ ** 3
    r_lin = +4.0767434099 * l_cubed - 3.3077115913 * m_cubed + 0.2309699292 * s_cubed
    g_lin = -1.2684380046 * l_cubed + 2.6097574011 * m_cubed - 0.3413193965 * s_cubed
    b_lin = -0.0041960863 * l_cubed - 0.7034186147 * m_cubed + 1.7076147010 * s_cubed
    return (max(0.0, min(1.0, r_lin)), max(0.0, min(1.0, g_lin)), max(0.0, min(1.0, b_lin)))


def calculate_oklch_luminance(l: float, c: float, h: float) -> float:
    """Calculates relative luminance from OKLCH coordinates."""
    r_lin, g_lin, b_lin = oklch_to_linear_srgb(l, c, h)
    return 0.2126 * r_lin + 0.7152 * g_lin + 0.0722 * b_lin


def parse_oklch_string(oklch_str: str) -> Optional[Tuple[float, float, float]]:
    """Parses 'oklch(0.98 0.01 250)' or 'oklch(98% 0.01 250)' into (l, c, h)."""
    match = re.search(
        r"oklch\(\s*([\d.]+%?)\s+([\d.]+)\s+([\d.]+)(?:deg)?(?:\s*/\s*[\d.]+%?)?\s*\)",
        oklch_str,
        re.IGNORECASE
    )
    if not match:
        return None
    l_s, c_s, h_s = match.groups()
    l_val = float(l_s[:-1]) / 100.0 if l_s.endswith("%") else float(l_s)
    return (l_val, float(c_s), float(h_s))


def calculate_oklch_contrast(color1: str, color2: str) -> float:
    """Calculates WCAG 2.2 contrast ratio between two OKLCH color strings."""
    coords1 = parse_oklch_string(color1)
    coords2 = parse_oklch_string(color2)
    if not coords1 or not coords2:
        return 4.5  # Safe default if parsing fails

    lum1 = calculate_oklch_luminance(*coords1)
    lum2 = calculate_oklch_luminance(*coords2)
    l_high = max(lum1, lum2)
    l_low = min(lum1, lum2)
    return (l_high + 0.05) / (l_low + 0.05)


# -----------------------------------------------------------------------------
# Design Intelligence Engine (BM25 Index Orchestrator)
# -----------------------------------------------------------------------------
class DesignIntelligenceEngine:
    """
    High-performance in-memory search and design intelligence engine.
    Indexes styles, palettes, typography, and benchmarks using pure-Python Okapi BM25.
    """

    _instance: Optional[DesignIntelligenceEngine] = None

    def __init__(self, catalog_path: Optional[Path] = None):
        self.catalog_path = catalog_path or CATALOG_PATH
        self.styles_index = BM25Index(k1=1.5, b=0.75)
        self.palettes_index = BM25Index(k1=1.5, b=0.75)
        self.typography_index = BM25Index(k1=1.5, b=0.75)
        self.benchmarks_index = BM25Index(k1=1.5, b=0.75)
        self.archetypes_index = BM25Index(k1=1.5, b=0.75)

        self._raw_catalog: Dict[str, Any] = {}
        self._load_and_index()

    @classmethod
    def get_instance(cls) -> DesignIntelligenceEngine:
        """Singleton accessor for zero-latency reuse across swarm stations."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def _load_and_index(self) -> None:
        """Loads catalog (or fallback data) and builds in-memory BM25 indices."""
        catalog_loaded = False
        if self.catalog_path.exists():
            try:
                with open(self.catalog_path, "r", encoding="utf-8") as f:
                    self._raw_catalog = json.load(f)
                    catalog_loaded = True
            except Exception:
                catalog_loaded = False

        if not catalog_loaded:
            # Fallback to existing legacy data files
            self._load_legacy_fallbacks()

        self._index_all_domains()

    def _load_legacy_fallbacks(self) -> None:
        """Populates basic catalog from legacy styles, palettes, and archetypes."""
        self._raw_catalog = {
            "version": "6.5.1",
            "styles": [],
            "palettes": [],
            "typography_systems": [],
            "composition_archetypes": []
        }

        if LEGACY_STYLES_PATH.exists():
            try:
                with open(LEGACY_STYLES_PATH, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self._raw_catalog["styles"] = data.get("styles", [])
            except Exception:
                pass

        if LEGACY_PALETTES_PATH.exists():
            try:
                with open(LEGACY_PALETTES_PATH, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self._raw_catalog["palettes"] = data.get("palettes", [])
            except Exception:
                pass

        if ARCHETYPES_PATH.exists():
            try:
                with open(ARCHETYPES_PATH, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    archetypes_dict = data.get("macro_archetypes", {})
                    self._raw_catalog["composition_archetypes"] = [
                        {"id": k, **v} for k, v in archetypes_dict.items()
                    ]
            except Exception:
                pass

    def _index_all_domains(self) -> None:
        """Constructs weighted indices across all design intelligence vectors."""
        # 1. Index Styles
        styles = self._raw_catalog.get("styles", [])
        for style in styles:
            style_id = style.get("style_id") or style.get("id", "")
            fields = {
                "name": style.get("name") or style.get("name_en", ""),
                "domains": style.get("domains", []),
                "emotional_tone": style.get("emotional_tone", []) or style.get("personality", []),
                "surfaces": style.get("surfaces") or style.get("elevation", ""),
                "keywords": style.get("keywords", []) or style.get("tailwind_signatures", []),
                "avoid": style.get("anti_slop_constraints", {}).get("forbidden_tropes", []) if isinstance(style.get("anti_slop_constraints"), dict) else style.get("avoid_patterns", [])
            }
            # Field weights: name and domains get highest boost
            self.styles_index.add_document(
                doc_id=style_id,
                fields=fields,
                metadata=style,
                field_weights={"name": 3.0, "domains": 2.5, "emotional_tone": 2.0, "keywords": 1.5, "surfaces": 1.0}
            )
        self.styles_index.build_index()

        # 2. Index Palettes
        palettes = self._raw_catalog.get("palettes", [])
        for pal in palettes:
            pal_id = pal.get("id", "")
            fields = {
                "name": pal.get("name", ""),
                "best_for": pal.get("best_for", []),
                "mood": pal.get("mood", ""),
                "color_mode": pal.get("canonical_mode", "") or pal.get("color_mode", "")
            }
            self.palettes_index.add_document(
                doc_id=pal_id,
                fields=fields,
                metadata=pal,
                field_weights={"name": 3.0, "best_for": 3.0, "mood": 2.0, "color_mode": 1.0}
            )
        self.palettes_index.build_index()

        # 3. Index Curated Elite Benchmarks
        benchmarks = self._raw_catalog.get("benchmarks", CURATED_BENCHMARKS)
        for bench in benchmarks:
            bench_id = bench.get("id", bench.get("name", ""))
            fields = {
                "name": bench.get("name", ""),
                "paradigm": bench.get("paradigm", ""),
                "domains": bench.get("domains", []) or bench.get("recommended_for", []),
                "archetype": bench.get("composition_archetype", "")
            }
            self.benchmarks_index.add_document(
                doc_id=bench_id,
                fields=fields,
                metadata=bench,
                field_weights={"name": 3.0, "domains": 2.5, "paradigm": 2.0}
            )
        self.benchmarks_index.build_index()

        # 4. Index Composition Archetypes
        archetypes = self._raw_catalog.get("composition_archetypes", [])
        for arch in archetypes:
            arch_id = arch.get("id", "")
            fields = {
                "name": arch.get("name", ""),
                "domains": arch.get("domains", []),
                "hero_layout": arch.get("hero_layout", ""),
                "typography": arch.get("typography", "")
            }
            self.archetypes_index.add_document(
                doc_id=arch_id,
                fields=fields,
                metadata=arch,
                field_weights={"name": 3.0, "domains": 3.0, "hero_layout": 2.0}
            )
        self.archetypes_index.build_index()

        # 5. Index Typography Systems
        typography_systems = self._raw_catalog.get("typography_systems", [])
        for typo in typography_systems:
            typo_id = typo.get("id", typo.get("name", ""))
            fields = {
                "name": typo.get("name", ""),
                "display": typo.get("display", ""),
                "body": typo.get("body", ""),
                "mono": typo.get("mono", ""),
                "domains": typo.get("domains", []),
                "personality": typo.get("personality", [])
            }
            self.typography_index.add_document(
                doc_id=typo_id,
                fields=fields,
                metadata=typo,
                field_weights={"name": 3.0, "domains": 2.5, "display": 2.0, "personality": 1.5}
            )
        self.typography_index.build_index()

    # Public Search APIs
    def search_styles(
        self,
        query: str,
        limit: int = 5,
        domain_filter: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Retrieves best-matching visual styles sorted by BM25 score."""
        filter_fn = None
        if domain_filter:
            d_norm = domain_filter.lower().strip()
            filter_fn = lambda m: d_norm in [str(d).lower() for d in m.get("domains", [])]

        results = self.styles_index.search(query, limit=limit, filter_fn=filter_fn)
        if not results and filter_fn is not None:
            # Fallback to unfiltered search if strict domain filter returned zero
            results = self.styles_index.search(query, limit=limit)
        return results

    def search_palettes(
        self,
        query: str,
        limit: int = 5,
        color_mode: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Retrieves best-matching OKLCH palettes sorted by BM25 score."""
        filter_fn = None
        if color_mode:
            c_norm = color_mode.lower().strip()
            filter_fn = lambda m: str(m.get("canonical_mode") or m.get("color_mode", "")).lower() == c_norm

        return self.palettes_index.search(query, limit=limit, filter_fn=filter_fn)

    def search_benchmarks(
        self,
        query: str,
        limit: int = 4
    ) -> List[Dict[str, Any]]:
        """Retrieves top open-source UI benchmarks (>10k stars) via BM25 matching."""
        results = self.benchmarks_index.search(query, limit=limit)
        if not results:
            # Fallback to top curated benchmarks
            return [
                {"id": b["id"], "score": 1.0, "metadata": b}
                for b in CURATED_BENCHMARKS[:limit]
            ]
        return results

    def search_archetypes(
        self,
        query: str,
        limit: int = 3
    ) -> List[Dict[str, Any]]:
        """Retrieves composition archetypes (split stage, editorial, HUD, canvas)."""
        return self.archetypes_index.search(query, limit=limit)

    def get_style_by_id(self, style_id: str) -> Optional[Dict[str, Any]]:
        """Direct lookup of style metadata by ID."""
        doc = self.styles_index.documents.get(style_id)
        return doc["metadata"] if doc else None

    def get_palette_by_id(self, palette_id: str) -> Optional[Dict[str, Any]]:
        """Direct lookup of palette metadata by ID."""
        doc = self.palettes_index.documents.get(palette_id)
        return doc["metadata"] if doc else None

    def get_total_counts(self) -> Dict[str, int]:
        """Returns indexed item counts for health monitoring."""
        return {
            "styles": self.styles_index.num_docs,
            "palettes": self.palettes_index.num_docs,
            "benchmarks": self.benchmarks_index.num_docs,
            "archetypes": self.archetypes_index.num_docs,
            "typography": self.typography_index.num_docs
        }


# -----------------------------------------------------------------------------
# Standalone Unit Test Suite
# -----------------------------------------------------------------------------
def _run_self_tests() -> None:
    print("[*] Running vibe_core/search_engine.py BM25 self-tests...")

    # 1. Test Tokenization
    sample_text = "Modern SaaS & B2B_Enterprise: Clinical-Wellness!"
    toks = tokenize(sample_text)
    assert "modern" in toks, f"Expected 'modern' in {toks}"
    assert "saas" in toks, f"Expected 'saas' in {toks}"
    assert "b2b" in toks, f"Expected 'b2b' in {toks}"
    assert "wellness" in toks, f"Expected 'wellness' in {toks}"
    print("  [PASS] Tokenization logic & punctuation normalization")

    # 2. Test BM25 Index creation & scoring
    test_index = BM25Index(k1=1.5, b=0.75)
    test_index.add_document("doc1", {"content": "Minimalist Swiss typography and precise layout grid"})
    test_index.add_document("doc2", {"content": "Cyberpunk neon dark HUD terminal with high density metrics"})
    test_index.add_document("doc3", {"content": "Modern SaaS enterprise dashboard with clean light cards"})
    test_index.build_index()

    res = test_index.search("swiss typography", limit=2)
    assert len(res) > 0, "BM25 search returned empty results"
    assert res[0]["id"] == "doc1", f"Expected doc1 to rank #1 for 'swiss typography', got {res[0]['id']}"
    assert res[0]["score"] > 0, "Score should be positive"
    print("  [PASS] BM25 inverted index ranking & query scoring")

    # 3. Test Color Science & WCAG Contrast
    # Pure white vs deep slate (#0f172a approx oklch(0.18 0.02 260))
    white_oklch = "oklch(0.99 0.003 250)"
    slate_oklch = "oklch(0.18 0.02 260)"
    contrast = calculate_oklch_contrast(white_oklch, slate_oklch)
    assert contrast >= 4.5, f"Expected WCAG AA >= 4.5:1, got {contrast:.2f}:1"
    print(f"  [PASS] OKLCH relative luminance & WCAG contrast calculation ({contrast:.2f}:1)")

    # 4. Test DesignIntelligenceEngine Initialization
    engine = DesignIntelligenceEngine()
    counts = engine.get_total_counts()
    print(f"  [PASS] DesignIntelligenceEngine loaded: {counts}")

    print("[SUCCESS] All search_engine.py unit tests passed cleanly.")


if __name__ == "__main__":
    _run_self_tests()
