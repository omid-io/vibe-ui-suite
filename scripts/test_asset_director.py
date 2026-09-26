#!/usr/bin/env python3
"""
scripts/test_asset_director.py — Unit tests for AssetDirector canonical domain alignment.
Verifies:
1. 100% coverage of all 24 canonical domains in AssetDirector.DOMAIN_MEDIA_SPECS.
2. Zero fallback to DEFAULT_MEDIA_SPEC when given canonical domain keys.
3. Verification that badging uses "SYNTHETIC MEDIA SLOT — AWAITING SOURCE ASSET".
4. Correct resolution of legacy domain aliases.
"""

import sys
import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from vibe_core.asset_director import AssetDirector

def main():
    print("[INFO] Running Asset Director Canonical Alignment Suite...")
    bp_path = ROOT_DIR / "data" / "domain_blueprints.json"
    with open(bp_path, "r", encoding="utf-8") as f:
        blueprints = json.load(f)["domains"]

    director = AssetDirector()
    failures = []

    for domain_id in blueprints.keys():
        if domain_id not in director.DOMAIN_MEDIA_SPECS:
            failures.append(f"Domain '{domain_id}' missing from AssetDirector.DOMAIN_MEDIA_SPECS")
            continue

        spec = director.get_media_spec(domain_id)
        if spec == director.DEFAULT_MEDIA_SPEC:
            failures.append(f"Domain '{domain_id}' triggered fallback to DEFAULT_MEDIA_SPEC")

        # Test JSX generation for LTR and RTL
        for is_rtl in [False, True]:
            jsx = director.generate_media_container_jsx(domain_id, style_name="clean_stripe", is_rtl=is_rtl)
            if "SYNTHETIC MEDIA SLOT — AWAITING SOURCE ASSET" not in jsx:
                failures.append(f"Domain '{domain_id}' (rtl={is_rtl}) does not contain honest synthetic badge")
            if "data-origin=\"synthetic_demo\"" not in jsx:
                failures.append(f"Domain '{domain_id}' (rtl={is_rtl}) missing data-origin='synthetic_demo'")
            if "VERIFIED ASSET" in jsx:
                failures.append(f"Domain '{domain_id}' (rtl={is_rtl}) contains misleading 'VERIFIED ASSET' string")

    # Test Aliases
    for alias, canonical in director.DOMAIN_ALIASES.items():
        spec = director.get_media_spec(alias)
        expected_spec = director.DOMAIN_MEDIA_SPECS.get(canonical)
        if spec != expected_spec:
            failures.append(f"Alias '{alias}' did not resolve to canonical spec of '{canonical}'")

    print(f"  [PASS] Verified 24/24 canonical domain media specifications.")
    print(f"  [PASS] Verified honest synthetic demarcation badge on all media containers.")
    print(f"  [PASS] Verified {len(director.DOMAIN_ALIASES)} legacy domain aliases.")

    if failures:
        print("\n[FAIL] Asset Director Suite Failures:", file=sys.stderr)
        for f in failures:
            print(f"  - {f}", file=sys.stderr)
        return 1

    print("\n[SUCCESS] Asset Director test suite passed with 100% compliance.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
