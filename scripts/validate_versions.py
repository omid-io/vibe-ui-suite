#!/usr/bin/env python3
"""
validate_versions.py — Vibe UI Version Consistency Validator
Ensures all package.json files, manifests, and documentation match the canonical version.
"""

import sys
import json
import re
from pathlib import Path

# Ensure UTF-8 output on Windows consoles
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent.parent
MANIFEST_PATH = ROOT_DIR / "version.manifest.json"
VERSION_JSON_PATH = ROOT_DIR / "version.json"

PACKAGE_FILES = [
    ROOT_DIR / "packages" / "vibe-ui-suite" / "package.json",
    ROOT_DIR / "packages" / "tokens" / "package.json",
    ROOT_DIR / "packages" / "vibe-ui-vscode" / "package.json",
    ROOT_DIR / "examples" / "nextjs-starter" / "package.json",
]

def main():
    if not MANIFEST_PATH.exists():
        print(f"[FAIL] Manifest not found at {MANIFEST_PATH}", file=sys.stderr)
        return 1

    try:
        with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
            manifest = json.load(f)
    except Exception as e:
        print(f"[FAIL] Malformed manifest: {e}", file=sys.stderr)
        return 1

    canonical_version = manifest.get("version")
    package_targets = manifest.get("packages", {})

    print(f"[INFO] Validating version synchronization (Canonical: {canonical_version})...")

    errors = []

    # 1. Validate version.json
    if VERSION_JSON_PATH.exists():
        try:
            with open(VERSION_JSON_PATH, "r", encoding="utf-8") as f:
                vjson = json.load(f)
            if vjson.get("version") != canonical_version:
                errors.append(f"version.json version '{vjson.get('version')}' does not match canonical '{canonical_version}'")
            else:
                print(f"  [OK] version.json: {canonical_version} matches manifest")
        except Exception as e:
            errors.append(f"Invalid JSON in version.json: {e}")

    # 2. Validate packages
    for pkg_path in PACKAGE_FILES:
        if not pkg_path.exists():
            errors.append(f"Missing package file: {pkg_path.relative_to(ROOT_DIR)}")
            continue

        try:
            with open(pkg_path, "r", encoding="utf-8") as f:
                pkg_data = json.load(f)
        except Exception as e:
            errors.append(f"Invalid JSON in {pkg_path.relative_to(ROOT_DIR)}: {e}")
            continue

        name = pkg_data.get("name")
        version = pkg_data.get("version")
        expected_version = package_targets.get(name, canonical_version)

        if version != expected_version:
            errors.append(
                f"Version drift in {pkg_path.relative_to(ROOT_DIR)}: "
                f"found '{version}', expected '{expected_version}'"
            )
        else:
            print(f"  [OK] {name}: {version} matches manifest")

    # 3. Validate evals/run_evals.py SUITE_VERSION
    evals_path = ROOT_DIR / "evals" / "run_evals.py"
    if evals_path.exists():
        content = evals_path.read_text(encoding="utf-8")
        match = re.search(r'SUITE_VERSION\s*=\s*"([^"]+)"', content)
        if match:
            v = match.group(1)
            if v != canonical_version:
                errors.append(f"evals/run_evals.py SUITE_VERSION '{v}' does not match canonical '{canonical_version}'")
            else:
                print(f"  [OK] evals/run_evals.py: SUITE_VERSION {v} matches manifest")
        else:
            errors.append("Could not find SUITE_VERSION in evals/run_evals.py")

    # 4. Validate ARCHITECTURE.md Version
    arch_path = ROOT_DIR / "ARCHITECTURE.md"
    if arch_path.exists():
        content = arch_path.read_text(encoding="utf-8")
        match = re.search(r'\*\*Version:\*\*\s*([^\s\n]+)', content)
        if match:
            v = match.group(1).strip()
            if v != canonical_version:
                errors.append(f"ARCHITECTURE.md version '{v}' does not match canonical '{canonical_version}'")
            else:
                print(f"  [OK] ARCHITECTURE.md: Version {v} matches manifest")
        else:
            errors.append("Could not find **Version:** in ARCHITECTURE.md")

    if errors:
        print("\n[FAIL] Version Drift Detected:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    print("\n[SUCCESS] All package versions synchronized successfully.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
