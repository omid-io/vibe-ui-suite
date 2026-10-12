#!/usr/bin/env python3
"""
scripts/verify_m1_harmonization.py
Verification script for Milestone M1 (Skill Catalog Harmonization).
Checks:
  1. Zero oklch(0.14) in default palettes
  2. Zero "enabled": true in default semantic_rtl_contract
  3. Zero 30-parameter references in skills
  4. Zero \u200c ZWNJ characters in all modified files
"""

import os
import sys

# Windows console encoding safeguard
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

TARGET_FILES = [
    "skills/autonomous-intent-expander/SKILL.md",
    "skills/vibe-physics-engine/SKILL.md",
    "skills/ui-verifier/SKILL.md",
    "skills/visual-chemistry-engine/SKILL.md",
    "skills/conversion-copy-engine/SKILL.md",
    "skills/ui-kit/references/modern_vibe_components.md",
    "skills/ui-kit/references/tokens_and_theme_engine.md",
]


def main():
    failures = []

    print("=" * 60)
    print("AUDITING MILESTONE M1 SKILL HARMONIZATION")
    print("=" * 60)

    # 1. Zero oklch(0.14)
    print("\n[CHECK 1] Zero oklch(0.14) in default palettes...")
    for fpath in TARGET_FILES:
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()
        if "oklch(0.14" in content:
            msg = f"FAIL: oklch(0.14 found in {fpath}"
            print(f"  ❌ {msg}")
            failures.append(msg)
        else:
            print(f"  ✅ {fpath}")

    # 2. Zero "enabled": true in default semantic_rtl_contract
    print("\n[CHECK 2] Zero 'enabled': true in default semantic_rtl_contract...")
    for fpath in TARGET_FILES:
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()
        if '"enabled": true' in content or '"enabled":true' in content:
            msg = f"FAIL: 'enabled': true found in {fpath}"
            print(f"  ❌ {msg}")
            failures.append(msg)
        else:
            print(f"  ✅ {fpath}")

    # 3. Zero 30-parameter references in skills
    print("\n[CHECK 3] Zero 30-parameter references across all skills...")
    for root, _, files in os.walk("skills"):
        for fname in files:
            if fname.endswith(".md"):
                full_path = os.path.join(root, fname).replace("\\", "/")
                with open(full_path, "r", encoding="utf-8") as f:
                    content = f.read()
                if "30-parameter" in content.lower():
                    msg = f"FAIL: 30-parameter found in {full_path}"
                    print(f"  ❌ {msg}")
                    failures.append(msg)
    print("  ✅ All skills free of 30-parameter references.")

    # 4. Zero ZWNJ (\u200c) in modified files
    print("\n[CHECK 4] Zero ZWNJ (\\u200c) characters in modified files...")
    for fpath in TARGET_FILES:
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()
        if "\u200c" in content:
            msg = f"FAIL: ZWNJ found in {fpath}"
            print(f"  ❌ {msg}")
            failures.append(msg)
        else:
            print(f"  ✅ {fpath}")

    print("\n" + "=" * 60)
    if not failures:
        print("🎉 ALL M1 HARMONIZATION CHECKS PASSED WITH 100% ACCURACY!")
        print("=" * 60)
        return 0
    else:
        print(f"❌ {len(failures)} CHECKS FAILED:")
        for fail in failures:
            print(f"   - {fail}")
        print("=" * 60)
        return 1


if __name__ == "__main__":
    sys.exit(main())
