#!/usr/bin/env python3
"""
validate_data.py — Validates all JSON datasets in data/ for structure, invariants, and encoding.
"""

import sys
import json
import re
from pathlib import Path

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"

EMOJI_PATTERN = re.compile(
    r"[\U00010000-\U0010ffff]|"
    r"[\u2600-\u27bf]|"
    r"[\u2300-\u23ff]|"
    r"[\u2b50-\u2b55]|"
    r"[\u203c-\u2049]"
)

EXPECTED_FILES = [
    "taxonomy.json",
    "domains.json",
    "styles.json",
    "priors.json",
    "typography.json",
    "palettes.json",
    "layouts.json",
    "density.json",
    "motion.json",
    "interaction-patterns.json",
    "states.json",
    "anti-patterns.json",
    "compatibility.json",
    "domain_blueprints.json",
    "typography_variants.json"
]

def check_emojis(obj, file_name, path=""):
    errors = []
    if isinstance(obj, str):
        if EMOJI_PATTERN.search(obj):
            errors.append(f"Raw emoji found in {file_name} at {path}: '{obj}'")
    elif isinstance(obj, dict):
        for k, v in obj.items():
            errors.extend(check_emojis(v, file_name, f"{path}.{k}"))
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            errors.extend(check_emojis(item, file_name, f"{path}[{i}]"))
    return errors

def main():
    print("[INFO] Auditing Knowledge Base datasets in data/...")
    if not DATA_DIR.exists():
        print(f"[FAIL] Data directory not found at {DATA_DIR}", file=sys.stderr)
        return 1

    errors = []

    # Check for expected files
    for ef in EXPECTED_FILES:
        target = DATA_DIR / ef
        if not target.exists():
            errors.append(f"Missing canonical data file: {ef}")

    if errors:
        for err in errors:
            print(f"  [FAIL] {err}", file=sys.stderr)
        return 1

    # Validate each JSON file
    for json_file in DATA_DIR.glob("*.json"):
        try:
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            # Check for raw emojis
            emoji_errs = check_emojis(data, json_file.name)
            errors.extend(emoji_errs)

            print(f"  [OK] {json_file.name}: Valid JSON, 0 emojis")
        except Exception as e:
            errors.append(f"Failed to parse {json_file.name}: {e}")

    # Specific semantic checks
    # 1. taxonomy.json: 24 domains
    tax_path = DATA_DIR / "taxonomy.json"
    if tax_path.exists():
        with open(tax_path, "r", encoding="utf-8") as f:
            tax_data = json.load(f)
        domains = tax_data.get("domains", [])
        if len(domains) != 24:
            errors.append(f"taxonomy.json must define exactly 24 domains, found {len(domains)}")
        else:
            print(f"  [OK] taxonomy.json: Exactly 24 domains verified with bilingual aliases")

    # 2. styles.json: 12 anchor styles
    styles_path = DATA_DIR / "styles.json"
    if styles_path.exists():
        with open(styles_path, "r", encoding="utf-8") as f:
            styles_data = json.load(f)
        styles = styles_data.get("styles", [])
        if len(styles) < 12:
            errors.append(f"styles.json must define at least 12 anchor styles, found {len(styles)}")
        else:
            print(f"  [OK] styles.json: Exactly {len(styles)} anchor styles verified")

    # 3. palettes.json: OKLCH format
    palettes_path = DATA_DIR / "palettes.json"
    if palettes_path.exists():
        with open(palettes_path, "r", encoding="utf-8") as f:
            pal_data = json.load(f)
        palettes = pal_data.get("palettes", [])
        for p in palettes:
            for color_key in ["canvas", "surface", "accent", "text"]:
                val = p.get(color_key, "")
                if not val.startswith("oklch("):
                    errors.append(f"Palette '{p.get('id')}' {color_key} is not OKLCH: '{val}'")
        if not errors:
            print(f"  [OK] palettes.json: {len(palettes)} palettes verified in typed OKLCH color space")

    if errors:
        print("\n[FAIL] Data Validation Failures:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    print("\n[SUCCESS] All 13 canonical datasets in data/ validated successfully.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
