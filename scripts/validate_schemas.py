#!/usr/bin/env python3
"""
validate_schemas.py — Validates all JSON Schemas in schemas/ for syntax and self-consistency,
and actively validates data/catalog/design_genome.json against schemas/design_genome.schema.json.
"""

import sys
import json
from pathlib import Path

# Ensure UTF-8 output on Windows consoles
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent.parent
SCHEMAS_DIR = ROOT_DIR / "schemas"
CATALOG_FILE = ROOT_DIR / "data" / "catalog" / "design_genome.json"
GENOME_SCHEMA_FILE = SCHEMAS_DIR / "design_genome.schema.json"

try:
    import jsonschema
    HAS_JSONSCHEMA = True
except ImportError:
    HAS_JSONSCHEMA = False


def validate_schema_file(schema_path: Path):
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)

    if not isinstance(schema, dict):
        raise ValueError("Schema root must be a JSON object")

    if "$schema" not in schema:
        raise ValueError("Missing $schema declaration")

    if "type" not in schema and "properties" not in schema and "oneOf" not in schema and "$ref" not in schema:
        raise ValueError("Schema lacks type, properties, oneOf, or $ref")

    if HAS_JSONSCHEMA:
        # Check that the schema is a structurally valid JSON schema
        validator_cls = jsonschema.validators.validator_for(schema)
        validator_cls.check_schema(schema)

    return True


def strict_fallback_validation(genome_data: dict) -> list:
    """Strict validation check enforcing catalog schema rules."""
    errors = []

    # Required top-level fields: styles, palettes, typography, archetypes
    for field in ("styles", "palettes"):
        if field not in genome_data:
            errors.append(f"Missing required catalog field: '{field}'")

    has_typo = "typography" in genome_data or "typography_systems" in genome_data
    if not has_typo:
        errors.append("Missing required catalog field: 'typography' / 'typography_systems'")

    has_archetypes = "archetypes" in genome_data or "composition_archetypes" in genome_data
    if not has_archetypes:
        errors.append("Missing required catalog field: 'archetypes' / 'composition_archetypes'")

    styles = genome_data.get("styles", [])
    if not isinstance(styles, list) or len(styles) < 80:
        errors.append(f"Styles must be a list with >= 80 items (found {len(styles) if isinstance(styles, list) else 0})")
    else:
        for idx, s in enumerate(styles):
            if not isinstance(s, dict):
                errors.append(f"Style #{idx} is not an object")
                continue
            if not (s.get("id") or s.get("style_id")):
                errors.append(f"Style #{idx} missing id/style_id")
            if not s.get("name"):
                errors.append(f"Style #{idx} missing name")
            if not (s.get("family") or s.get("domains")):
                errors.append(f"Style #{idx} missing family/domains")
            if not (s.get("tokens") or s.get("palette")):
                errors.append(f"Style #{idx} missing tokens/palette")

    palettes = genome_data.get("palettes", [])
    if not isinstance(palettes, list) or len(palettes) < 150:
        errors.append(f"Palettes must be a list with >= 150 items (found {len(palettes) if isinstance(palettes, list) else 0})")
    else:
        for idx, p in enumerate(palettes):
            if not isinstance(p, dict):
                errors.append(f"Palette #{idx} is not an object")
                continue
            if not p.get("id"):
                errors.append(f"Palette #{idx} missing id")
            if not p.get("light"):
                errors.append(f"Palette #{idx} missing light tokens")
            if not (p.get("dark") or p.get("dark_oled")):
                errors.append(f"Palette #{idx} missing dark/dark_oled tokens")

            cmetrics = p.get("contrast_metrics", {})
            if not isinstance(cmetrics, dict):
                errors.append(f"Palette #{idx} ({p.get('id')}) missing contrast_metrics object")
            else:
                lc = cmetrics.get("light_contrast", 0)
                dc = cmetrics.get("dark_contrast", 0)
                if lc < 4.5:
                    errors.append(f"Palette #{idx} ({p.get('id')}) light_contrast {lc} < 4.5")
                if dc < 4.5:
                    errors.append(f"Palette #{idx} ({p.get('id')}) dark_contrast {dc} < 4.5")

    return errors


def validate_catalog():
    if not CATALOG_FILE.exists():
        raise FileNotFoundError(f"Catalog file not found: {CATALOG_FILE}")
    if not GENOME_SCHEMA_FILE.exists():
        raise FileNotFoundError(f"Schema file not found: {GENOME_SCHEMA_FILE}")

    with open(CATALOG_FILE, "r", encoding="utf-8") as f:
        genome_data = json.load(f)

    with open(GENOME_SCHEMA_FILE, "r", encoding="utf-8") as f:
        schema = json.load(f)

    # 1. Active validation against schemas/design_genome.schema.json
    if HAS_JSONSCHEMA:
        jsonschema.validate(instance=genome_data, schema=schema)
        print("  [OK] Validated data/catalog/design_genome.json against schemas/design_genome.schema.json (jsonschema engine)")
    else:
        print("  [INFO] jsonschema library not installed; executing strict fallback validation")

    # 2. Strict invariant validation (always run to guarantee field & contrast requirements)
    fallback_errors = strict_fallback_validation(genome_data)
    if fallback_errors:
        raise ValueError("Catalog strict schema validation failed:\n" + "\n".join(f"    - {e}" for e in fallback_errors[:10]))

    print(f"  [OK] Strict catalog integrity verified: {len(genome_data['styles'])} styles, {len(genome_data['palettes'])} palettes (all contrast >= 4.5)")
    return True


def main():
    print("[INFO] Auditing JSON Schemas in schemas/...")
    schema_files = list(SCHEMAS_DIR.glob("*.json"))
    if not schema_files:
        print("[FAIL] No schema files found in schemas/", file=sys.stderr)
        return 1

    errors = []
    for sf in schema_files:
        try:
            validate_schema_file(sf)
            print(f"  [OK] {sf.name} is valid JSON schema")
        except Exception as e:
            errors.append(f"{sf.name}: {e}")

    if errors:
        print("\n[FAIL] Schema validation errors:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    print(f"\n[INFO] Actively validating design genome catalog against schema...")
    try:
        validate_catalog()
    except Exception as e:
        print(f"[FAIL] Catalog validation error: {e}", file=sys.stderr)
        return 1

    print(f"\n[SUCCESS] All {len(schema_files)} schemas and design genome catalog validated successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
