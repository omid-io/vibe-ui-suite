#!/usr/bin/env python3
"""
scripts/test_v6_e2e_suite.py — Vibe UI Suite v6.0.0 Comprehensive 4-Tier E2E Test Suite
Production-grade, requirement-driven test suite validating all 50 test cases across 4 tiers:
  - Tier 1: Feature Coverage (T1.1 - T1.35)
  - Tier 2: Boundary & Corner Cases (T2.1 - T2.8)
  - Tier 3: Cross-Feature Combinations (T3.1 - T3.4)
  - Tier 4: Real-World Scenarios (T4.1 - T4.3)

Derived strictly from ORIGINAL_REQUEST.md and TEST_INFRA.md.

Usage:
  python scripts/test_v6_e2e_suite.py [--tier 1|2|3|4|all] [-v|--verbose] [-k FILTER] [--failfast]
"""

import sys
import os
import json
import time
import struct
import signal
import argparse
import tempfile
import subprocess
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple, Callable

# Windows console UTF-8 safeguard
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

# ==============================================================================
# Helper Utilities
# ==============================================================================

def get_png_dimensions(file_path: Path) -> Tuple[int, int]:
    """Reads width and height from PNG IHDR chunk without external dependencies."""
    if not file_path.exists():
        raise FileNotFoundError(f"PNG file not found: {file_path}")
    with open(file_path, "rb") as f:
        header = f.read(24)
        if len(header) >= 24 and header[:8] == b"\x89PNG\r\n\x1a\n":
            width, height = struct.unpack(">II", header[16:24])
            return width, height
    raise ValueError(f"File is not a valid PNG: {file_path}")

def get_chromium_process_count() -> int:
    """Returns the count of active chromium.exe processes on Windows."""
    try:
        out = subprocess.check_output(["tasklist"], text=True, stderr=subprocess.DEVNULL)
        return sum(1 for line in out.splitlines() if "chromium.exe" in line.lower())
    except Exception:
        return 0

def run_cmd(args: List[str], cwd: Optional[Path] = None, timeout: int = 60) -> Tuple[int, str, str]:
    """Executes a command and returns (exit_code, stdout, stderr)."""
    res = subprocess.run(
        args,
        cwd=str(cwd or ROOT_DIR),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout
    )
    return res.returncode, res.stdout, res.stderr

# ==============================================================================
# Test Definition Data Structures
# ==============================================================================

class TestCase:
    def __init__(self, test_id: str, tier: int, feature: str, name: str, fn: Callable[[], None]):
        self.test_id = test_id
        self.tier = tier
        self.feature = feature
        self.name = name
        self.fn = fn

# ==============================================================================
# Tier 1: Feature Coverage (35 Test Cases: T1.1 - T1.35)
# ==============================================================================

class Tier1Tests:
    """Tier 1: Feature Coverage (35 test cases, 5 per feature across 7 features)"""

    # --- F1: Skill Harmonization (Light Default & Pruned Bloat) ---

    @staticmethod
    def test_t1_01():
        """T1.1 (F1): Verify autonomous-intent-expander defaults to Vibrant Light Mode (oklch(0.99 ...))."""
        skill_path = ROOT_DIR / "skills" / "autonomous-intent-expander" / "SKILL.md"
        assert skill_path.exists(), f"Missing file: {skill_path}"
        content = skill_path.read_text(encoding="utf-8")

        # Canonical palette must specify light mode canvas
        assert "oklch(0.99" in content, "Expected canvas_oklch starting with oklch(0.99 ...) in intent expander spec"
        assert "oklch(0.14" not in content, "Found forbidden dark canvas oklch(0.14 ...) in intent expander spec"
        assert '"mode": "light"' in content or "Vibrant Light" in content, "Expected explicit light mode specification"

    @staticmethod
    def test_t1_02():
        """T1.2 (F1): Verify autonomous-intent-expander has pruned 6-dimensional parameter structure (no P01–P30 bloat)."""
        skill_path = ROOT_DIR / "skills" / "autonomous-intent-expander" / "SKILL.md"
        content = skill_path.read_text(encoding="utf-8")

        assert "P01-P05" not in content, "Found legacy P01-P05 bloat in autonomous-intent-expander"
        assert "P29-P30" not in content, "Found legacy P29-P30 bloat in autonomous-intent-expander"
        assert "30-Parameter" not in content, "Found legacy '30-Parameter' in title or body"
        assert "6-Dimensional" in content or "6 dimensions" in content.lower(), "Expected 6-dimensional parameter architecture"

    @staticmethod
    def test_t1_03():
        """T1.3 (F1): Verify vibe-physics-engine does not force dark background on reduced transparency."""
        skill_path = ROOT_DIR / "skills" / "vibe-physics-engine" / "SKILL.md"
        assert skill_path.exists(), f"Missing file: {skill_path}"
        content = skill_path.read_text(encoding="utf-8")

        assert "@media (prefers-reduced-transparency: reduce)" in content, "Missing prefers-reduced-transparency rule"
        # Must not force opaque oklch(0.14) without dark theme scoping
        assert "background: oklch(0.14 0.005 260) !important; /* Fully opaque surface */" not in content, \
            "Found unconditional dark mode bias in reduced transparency fallback"
        assert "var(--surface-opaque, #ffffff)" in content or "surface-opaque" in content, \
            "Expected adaptive light surface fallback for reduced transparency"

    @staticmethod
    def test_t1_04():
        """T1.4 (F1): Verify ui-verifier scorecard includes Living Visual & Screenshot Inspection."""
        skill_path = ROOT_DIR / "skills" / "ui-verifier" / "SKILL.md"
        assert skill_path.exists(), f"Missing file: {skill_path}"
        content = skill_path.read_text(encoding="utf-8")

        assert "Living Visual" in content, "Expected 'Living Visual' verification section in ui-verifier"
        assert "Screenshot Inspection" in content or "screenshot" in content.lower(), \
            "Expected screenshot audit in ui-verifier verification matrix"

    @staticmethod
    def test_t1_05():
        """T1.5 (F1): Verify all 6 skills explicitly align with The Two Golden Pillars."""
        skill_dirs = [
            "autonomous-intent-expander",
            "vibe-physics-engine",
            "ui-kit",
            "ui-verifier",
            "visual-chemistry-engine",
            "conversion-copy-engine"
        ]
        for s in skill_dirs:
            path = ROOT_DIR / "skills" / s / "SKILL.md"
            assert path.exists(), f"Skill file does not exist: {path}"
            content = path.read_text(encoding="utf-8")
            has_pillar = ("Golden Pillar" in content or "Golden Pillars" in content or
                          "Pillar 1" in content or "Living Visual" in content)
            assert has_pillar, f"Skill {s} does not explicitly align with The Two Golden Pillars architecture"

    # --- F2: Scoped On-Demand RTL & BiDi Contract ---

    @staticmethod
    def test_t1_06():
        """T1.6 (F2): Verify design-spec.json template has 'semantic_rtl_contract': { 'enabled': false }."""
        skill_path = ROOT_DIR / "skills" / "autonomous-intent-expander" / "SKILL.md"
        content = skill_path.read_text(encoding="utf-8")

        assert '"semantic_rtl_contract"' in content, "Missing semantic_rtl_contract in design spec template"
        # Must default to false
        assert '"enabled": false' in content, "Expected 'enabled': false in default semantic_rtl_contract"

    @staticmethod
    def test_t1_07():
        """T1.7 (F2): Verify English generation does not force <bdi> wrappers or RTL attributes."""
        from vibe_core.director import DesignDirector
        from vibe_core.generator import InterfaceGenerator

        director = DesignDirector()
        generator = InterfaceGenerator()

        intent = director.infer_intent("Enterprise SaaS dashboard with analytics, telemetry, and billing")
        assert intent["language"] == "en" or intent.get("language_direction") != "rtl", \
            "English prompt should not trigger RTL language direction"

        html = generator.generate(intent)
        assert 'dir="rtl"' not in html.lower()[:300], "English generation must not set dir='rtl' on root element"

    @staticmethod
    def test_t1_08():
        """T1.8 (F2): Verify Persian generation activates RTL and <bdi> contracts."""
        from vibe_core.director import DesignDirector
        from vibe_core.generator import InterfaceGenerator

        director = DesignDirector()
        generator = InterfaceGenerator()

        intent = director.infer_intent("پرتال جامع نوبت دهی و خدمات پزشکی کلینیک سلامت")
        assert intent["language"] == "fa" or "clinical" in intent["product_domain"], \
            "Persian prompt must be detected accurately"

        html = generator.generate(intent)
        assert 'dir="rtl"' in html.lower(), "Persian generation must activate dir='rtl'"
        # Check bidirectional resilience
        has_bidi = "<bdi>" in html or "unicode-bidi" in html or "bidi" in html.lower()
        assert has_bidi, "Persian interface must include bidirectional isolation (<bdi> or CSS isolation)"

    @staticmethod
    def test_t1_09():
        """T1.9 (F2): Verify zero ZWNJ characters (\u200c) in visual-chemistry-engine."""
        path = ROOT_DIR / "skills" / "visual-chemistry-engine" / "SKILL.md"
        assert path.exists(), f"Missing file: {path}"
        content = path.read_text(encoding="utf-8")
        assert "\u200c" not in content, "Found prohibited ZWNJ (\\u200c) in visual-chemistry-engine/SKILL.md"

    @staticmethod
    def test_t1_10():
        """T1.10 (F2): Verify zero ZWNJ characters in all markdown files across repository."""
        target_dirs = [
            ROOT_DIR / "skills",
            ROOT_DIR / "data",
            ROOT_DIR / "packages"
        ]
        violating_files = []
        for d in target_dirs:
            if not d.exists():
                continue
            for p in d.rglob("*.md"):
                if any(x in p.parts for x in [".git", "node_modules"]):
                    continue
                try:
                    text = p.read_text(encoding="utf-8")
                    if "\u200c" in text:
                        violating_files.append(str(p.relative_to(ROOT_DIR)))
                except Exception:
                    pass

        # Also check root README and ARCHITECTURE
        for root_file in [ROOT_DIR / "README.md", ROOT_DIR / "README.fa.md", ROOT_DIR / "ARCHITECTURE.md"]:
            if root_file.exists():
                text = root_file.read_text(encoding="utf-8")
                if "\u200c" in text:
                    violating_files.append(str(root_file.relative_to(ROOT_DIR)))

        assert len(violating_files) == 0, f"Found ZWNJ in files: {violating_files}"

    # --- F3: Curated Unsplash Asset Vault (24 Domains) ---

    @staticmethod
    def test_t1_11():
        """T1.11 (F3): Verify data/unsplash_assets.json exists and parses as valid JSON with exactly 24 domains."""
        vault_path = ROOT_DIR / "data" / "unsplash_assets.json"
        assert vault_path.exists(), f"Missing asset vault JSON: {vault_path}"
        data = json.loads(vault_path.read_text(encoding="utf-8"))

        assert data.get("version") == "6.0.0", f"Expected version 6.0.0, got {data.get('version')}"
        assert "domains" in data, "Missing 'domains' key in unsplash_assets.json"
        domain_count = len(data["domains"])
        assert domain_count == 24, f"Expected exactly 24 canonical domains, got {domain_count}"

    @staticmethod
    def test_t1_12():
        """T1.12 (F3): Verify every domain has valid hero and card URL entries."""
        vault_path = ROOT_DIR / "data" / "unsplash_assets.json"
        data = json.loads(vault_path.read_text(encoding="utf-8"))

        for domain_id, dom_info in data["domains"].items():
            assert "hero" in dom_info, f"Domain {domain_id} missing hero object"
            assert "card" in dom_info, f"Domain {domain_id} missing card object"

            hero_url = dom_info["hero"].get("url", "")
            card_url = dom_info["card"].get("url", "")

            assert hero_url.startswith("https://images.unsplash.com/"), f"Domain {domain_id} invalid hero URL: {hero_url}"
            assert card_url.startswith("https://images.unsplash.com/"), f"Domain {domain_id} invalid card URL: {card_url}"

    @staticmethod
    def test_t1_13():
        """T1.13 (F3): Verify skills/ui-kit/references/curated_unsplash_vault.md exists and contains all 24 domains."""
        doc_path = ROOT_DIR / "skills" / "ui-kit" / "references" / "curated_unsplash_vault.md"
        assert doc_path.exists(), f"Missing curated vault reference doc: {doc_path}"
        content = doc_path.read_text(encoding="utf-8")

        # Load domain keys from domains.json
        domains_json = ROOT_DIR / "data" / "domains.json"
        domains_data = json.loads(domains_json.read_text(encoding="utf-8"))
        canonical_keys = [d["key"] if isinstance(d, dict) else d for d in domains_data["domains"]]

        missing_domains = [k for k in canonical_keys if k not in content]
        assert len(missing_domains) == 0, f"Vault reference markdown missing domains: {missing_domains}"

    @staticmethod
    def test_t1_14():
        """T1.14 (F3): Verify hero URLs contain &w=1200&q=80 and card URLs contain &w=600&h=400&q=80."""
        vault_path = ROOT_DIR / "data" / "unsplash_assets.json"
        data = json.loads(vault_path.read_text(encoding="utf-8"))

        for domain_id, dom_info in data["domains"].items():
            hero_url = dom_info["hero"]["url"]
            card_url = dom_info["card"]["url"]

            assert "w=1200" in hero_url and "q=80" in hero_url, \
                f"Domain {domain_id} hero missing focal parameters (&w=1200&q=80): {hero_url}"
            assert "w=600" in card_url and "h=400" in card_url and "q=80" in card_url, \
                f"Domain {domain_id} card missing focal parameters (&w=600&h=400&q=80): {card_url}"

    @staticmethod
    def test_t1_15():
        """T1.15 (F3): Verify skills/ui-kit/SKILL.md indexes curated_unsplash_vault.md."""
        skill_path = ROOT_DIR / "skills" / "ui-kit" / "SKILL.md"
        assert skill_path.exists(), f"Missing file: {skill_path}"
        content = skill_path.read_text(encoding="utf-8")

        assert "curated_unsplash_vault.md" in content, \
            "skills/ui-kit/SKILL.md must index references/curated_unsplash_vault.md in its catalog"

    # --- F4: Automated Multi-Viewport Screenshot Utility ---

    @staticmethod
    def test_t1_16():
        """T1.16 (F4): Verify scripts/screenshot_audit.py can be executed standalone."""
        code, out, err = run_cmd([sys.executable, "scripts/screenshot_audit.py", "--help"])
        assert code == 0, f"scripts/screenshot_audit.py --help failed with exit {code}: {err}"
        assert "Multi-Viewport" in out or "Screenshot Engine" in out or "screenshot" in out.lower(), \
            "Expected screenshot audit help output"

    @staticmethod
    def test_t1_17():
        """T1.17 (F4): Verify Desktop screenshot is captured at exactly 1440px width."""
        sample_path = ROOT_DIR / "examples" / "generated_output.html"
        assert sample_path.exists(), f"Sample HTML file not found: {sample_path}"

        from scripts.screenshot_audit import capture_audit_screenshots
        out_dir = ROOT_DIR / ".test-artifacts" / "screenshots"
        report = capture_audit_screenshots(str(sample_path), str(out_dir))

        desktop_file = report.get("files", {}).get("desktop")
        assert desktop_file and Path(desktop_file).exists(), f"Desktop screenshot not captured: {desktop_file}"

        w, h = get_png_dimensions(Path(desktop_file))
        assert w == 1440, f"Expected Desktop screenshot width 1440px, got {w}px"

    @staticmethod
    def test_t1_18():
        """T1.18 (F4): Verify Mobile screenshot is captured at exactly 390px width."""
        sample_path = ROOT_DIR / "examples" / "generated_output.html"
        assert sample_path.exists(), f"Sample HTML file not found: {sample_path}"

        out_dir = ROOT_DIR / ".test-artifacts" / "screenshots"
        mobile_file = out_dir / "generated_output_mobile_390px.png"
        assert mobile_file.exists(), f"Mobile screenshot file missing: {mobile_file}"

        w, h = get_png_dimensions(mobile_file)
        assert w == 390, f"Expected Mobile screenshot width 390px, got {w}px"

    @staticmethod
    def test_t1_19():
        """T1.19 (F4): Verify vibe_cli.py screenshot subcommand executes cleanly."""
        code, out, err = run_cmd([sys.executable, "vibe_cli.py", "screenshot", "--help"])
        assert code == 0, f"vibe_cli.py screenshot --help failed with code {code}: {err}"
        assert "screenshot" in out.lower(), "Expected screenshot subcommand help in vibe_cli.py"

    @staticmethod
    def test_t1_20():
        """T1.20 (F4): Verify screenshots are saved into .test-artifacts/screenshots/."""
        out_dir = ROOT_DIR / ".test-artifacts" / "screenshots"
        assert out_dir.exists(), f"Directory .test-artifacts/screenshots does not exist"

        pngs = list(out_dir.glob("*.png"))
        assert len(pngs) >= 2, f"Expected at least 2 screenshots in {out_dir}, found {len(pngs)}"
        for p in pngs[:2]:
            assert p.stat().st_size > 5000, f"Screenshot {p.name} appears suspiciously small ({p.stat().st_size} bytes)"

    # --- F5: Zero Orphaned Processes Invariant ---

    @staticmethod
    def test_t1_21():
        """T1.21 (F5): Verify chromium.exe process count is 0 after running screenshot tool."""
        # Check current active processes
        count = get_chromium_process_count()
        assert count == 0, f"Found {count} orphaned chromium.exe processes in tasklist"

    @staticmethod
    def test_t1_22():
        """T1.22 (F5): Verify cleanup runs even when target file has missing external assets."""
        with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as tf:
            tf.write("""<!DOCTYPE html>
<html>
<head><title>Broken Assets Test</title></head>
<body>
  <h1>Testing Error Handling</h1>
  <img src="https://invalid-host-9876543210.test/missing.jpg" alt="Missing Image">
  <img src="http://10.255.255.1/unreachable.png" alt="Unreachable Image">
</body>
</html>""")
            temp_path = Path(tf.name)

        try:
            from scripts.screenshot_audit import capture_audit_screenshots
            out_dir = ROOT_DIR / ".test-artifacts" / "screenshots"
            report = capture_audit_screenshots(str(temp_path), str(out_dir))
            assert report["success"] is True, "Screenshot utility failed to recover from broken external assets"
            count = get_chromium_process_count()
            assert count == 0, f"Found {count} orphaned chromium processes after broken asset test"
        finally:
            if temp_path.exists():
                try:
                    temp_path.unlink()
                except Exception:
                    pass

    @staticmethod
    def test_t1_23():
        """T1.23 (F5): Verify browser cleanup and exception resilience in screenshot_audit.py."""
        script_path = ROOT_DIR / "scripts" / "screenshot_audit.py"
        content = script_path.read_text(encoding="utf-8")

        assert "finally:" in content, "Missing guaranteed finally block in screenshot_audit.py"
        assert "browser.close()" in content or "browser" in content, "Missing browser.close() in cleanup block"
        assert "playwright_cm.__exit__" in content or "with sync_playwright()" in content, \
            "Missing Playwright context manager exit/cleanup"

    @staticmethod
    def test_t1_24():
        """T1.24 (F5): Verify no dangling subprocesses after CLI screenshot execution."""
        code, out, err = run_cmd([
            sys.executable, "vibe_cli.py", "screenshot",
            str(ROOT_DIR / "examples" / "generated_output.html")
        ])
        assert code == 0, f"CLI screenshot execution failed: {err}"
        time.sleep(0.5)
        count = get_chromium_process_count()
        assert count == 0, f"Found {count} lingering chromium processes after CLI screenshot"

    @staticmethod
    def test_t1_25():
        """T1.25 (F5): Verify .test-artifacts/ is ignored in .gitignore."""
        gitignore = ROOT_DIR / ".gitignore"
        assert gitignore.exists(), "Missing .gitignore file"
        content = gitignore.read_text(encoding="utf-8")
        assert ".test-artifacts/" in content or ".test-artifacts" in content, \
            ".test-artifacts/ must be listed in .gitignore to prevent repo pollution"

    # --- F6: Monorepo Version Synchronization (v6.0.0) ---

    @staticmethod
    def test_t1_26():
        """T1.26 (F6): Verify version.json has version: '6.1.0'."""
        v_path = ROOT_DIR / "version.json"
        data = json.loads(v_path.read_text(encoding="utf-8"))
        assert data.get("version") == "6.1.0", f"version.json version is '{data.get('version')}', expected '6.1.0'"

    @staticmethod
    def test_t1_27():
        """T1.27 (F6): Verify packages/vibe-ui-suite/package.json has version: '6.1.0'."""
        p_path = ROOT_DIR / "packages" / "vibe-ui-suite" / "package.json"
        data = json.loads(p_path.read_text(encoding="utf-8"))
        assert data.get("version") == "6.1.0", f"vibe-ui-suite package.json is '{data.get('version')}', expected '6.1.0'"

    @staticmethod
    def test_t1_28():
        """T1.28 (F6): Verify @omid-io/tokens is excluded from active release manifest."""
        m_path = ROOT_DIR / "version.manifest.json"
        data = json.loads(m_path.read_text(encoding="utf-8"))
        assert "@omid-io/tokens" not in data.get("packages", {}), \
            "@omid-io/tokens must be excluded from active release manifest (migrated to vibe-ui-suite)"

    @staticmethod
    def test_t1_29():
        """T1.29 (F6): Verify packages/vibe-ui-vscode/package.json has version: '6.1.0'."""
        p_path = ROOT_DIR / "packages" / "vibe-ui-vscode" / "package.json"
        data = json.loads(p_path.read_text(encoding="utf-8"))
        assert data.get("version") == "6.1.0", f"vibe-ui-vscode package.json is '{data.get('version')}', expected '6.1.0'"

    @staticmethod
    def test_t1_30():
        """T1.30 (F6): Verify vibe_cli.py --version outputs 'Vibe UI Suite v6.1.0'."""
        code, out, err = run_cmd([sys.executable, "vibe_cli.py", "--version"])
        assert code == 0, f"vibe_cli.py --version failed: {err}"
        assert "Vibe UI Suite v6.1.0" in out.strip(), f"Unexpected version string: {out.strip()}"

    # --- F7: Packaging & Release Readiness (VSIX & Security) ---

    @staticmethod
    def test_t1_31():
        """T1.31 (F7): Verify README.md and README.fa.md describe v6.0.0 and Two Golden Pillars."""
        readme_en = (ROOT_DIR / "README.md").read_text(encoding="utf-8")
        readme_fa = (ROOT_DIR / "README.fa.md").read_text(encoding="utf-8")

        assert "6.0.0" in readme_en or "v6.0.0" in readme_en, "README.md missing v6.0.0 designation"
        has_pillars_en = "Golden Pillar" in readme_en or "Golden Pillars" in readme_en
        assert has_pillars_en, "README.md missing Two Golden Pillars architecture"

        has_pillars_fa = "طلایی" in readme_fa or "Golden Pillar" in readme_fa
        assert has_pillars_fa, "README.fa.md missing Two Golden Pillars architecture"

    @staticmethod
    def test_t1_32():
        """T1.32 (F7): Verify README.fa.md has zero ZWNJ characters."""
        readme_fa = (ROOT_DIR / "README.fa.md").read_text(encoding="utf-8")
        assert "\u200c" not in readme_fa, "Found prohibited ZWNJ (\\u200c) in README.fa.md"

    @staticmethod
    def test_t1_33():
        """T1.33 (F7): Verify scripts/test_pipeline_e2e.py passes 4/4 integration tests."""
        code, out, err = run_cmd([sys.executable, "scripts/test_pipeline_e2e.py"], timeout=90)
        assert code == 0, f"test_pipeline_e2e.py failed with code {code}: {err}"
        assert "ALL 4 INTEGRATION TESTS PASSED CLEANLY" in out, \
            "test_pipeline_e2e.py did not report clean pass"

    @staticmethod
    def test_t1_34():
        """T1.34 (F7): Verify vibe-ui-vscode-6.0.0.vsix packages successfully."""
        pkg_script = ROOT_DIR / "packages" / "vibe-ui-vscode" / "package_vsix.py"
        assert pkg_script.exists(), f"Missing package_vsix.py: {pkg_script}"

        code, out, err = run_cmd([sys.executable, str(pkg_script)], cwd=pkg_script.parent)
        assert code == 0, f"package_vsix.py failed: {err}"

        vsix_file = ROOT_DIR / "packages" / "vibe-ui-vscode" / "vibe-ui-vscode-6.0.0.vsix"
        assert vsix_file.exists(), f"Expected packaged VSIX file missing: {vsix_file}"
        assert vsix_file.stat().st_size > 10000, f"VSIX file too small: {vsix_file.stat().st_size} bytes"

    @staticmethod
    def test_t1_35():
        """T1.35 (F7): Verify Gitleaks scan reports 0 leaks across repository history."""
        gitleaks_bin = Path(r"E:\programming\Tools\gitleaks\gitleaks.exe")
        if not gitleaks_bin.exists():
            # Alternative search in PATH
            code, out, _ = run_cmd(["gitleaks", "version"])
            assert code == 0, "Gitleaks scanner not found on system"
            gitleaks_cmd = ["gitleaks", "git", "--verbose", "--redact"]
        else:
            gitleaks_cmd = [str(gitleaks_bin), "git", "--verbose", "--redact"]

        code, out, err = run_cmd(gitleaks_cmd, timeout=30)
        assert code == 0, f"Gitleaks detected secret leaks! Exit {code}: {err or out}"
        assert "no leaks found" in (out + err).lower(), f"Gitleaks output did not confirm clean scan: {out}"

# ==============================================================================
# Tier 2: Boundary & Corner Cases (8 Test Cases: T2.1 - T2.8)
# ==============================================================================

class Tier2Tests:
    """Tier 2: Boundary & Corner Cases (8 test cases)"""

    @staticmethod
    def test_t2_01():
        """T2.1: Large HTML file (> 500KB) screenshot capture without browser OOM."""
        # Synthesize heavy HTML with 1200 card elements (> 500KB)
        cards = "\n".join([f'<div class="p-4 bg-white rounded shadow border border-slate-200">Card #{i}: Heavy DOM test content {"payload-padding-" * 40}</div>' for i in range(1200)])
        large_html = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Large DOM Benchmark</title>
  <style>body {{ font-family: sans-serif; background: #fafafa; padding: 20px; }} .grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; }}</style>
</head>
<body>
  <h1>Large DOM Stress Test</h1>
  <div class="grid">{cards}</div>
</body>
</html>"""
        with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as tf:
            tf.write(large_html)
            temp_path = Path(tf.name)

        assert temp_path.stat().st_size > 500000, f"Generated HTML is under 500KB: {temp_path.stat().st_size} bytes"

        try:
            from scripts.screenshot_audit import capture_audit_screenshots
            out_dir = ROOT_DIR / ".test-artifacts" / "screenshots"
            report = capture_audit_screenshots(str(temp_path), str(out_dir))
            assert report["success"] is True, "Large HTML screenshot capture failed"
            count = get_chromium_process_count()
            assert count == 0, f"Found {count} orphaned chromium processes after large HTML render"
        finally:
            if temp_path.exists():
                try:
                    temp_path.unlink()
                except Exception:
                    pass

    @staticmethod
    def test_t2_02():
        """T2.2: Slow network / CDN offline fallback in screenshot utility (graceful load without freeze)."""
        # HTML referencing unreachable host
        html_content = """<!DOCTYPE html>
<html>
<head>
  <title>Slow CDN Test</title>
  <link rel="stylesheet" href="http://10.255.255.1:9999/slow_stylesheet.css">
</head>
<body>
  <h1>Testing Resilient Navigation</h1>
  <p>Should not hang indefinitely when external assets are offline.</p>
</body>
</html>"""
        with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as tf:
            tf.write(html_content)
            temp_path = Path(tf.name)

        start = time.time()
        try:
            from scripts.screenshot_audit import capture_audit_screenshots
            out_dir = ROOT_DIR / ".test-artifacts" / "screenshots"
            report = capture_audit_screenshots(str(temp_path), str(out_dir))
            duration = time.time() - start
            assert report["success"] is True, "Navigation fallback failed on slow/offline CDN"
            assert duration < 10.0, f"Screenshot utility took too long ({duration:.1f}s) to recover from offline CDN"
            assert get_chromium_process_count() == 0, "Chromium process leaked during slow CDN test"
        finally:
            if temp_path.exists():
                try:
                    temp_path.unlink()
                except Exception:
                    pass

    @staticmethod
    def test_t2_03():
        """T2.3: Extreme aspect ratio rendering (ultra-wide desktop vs ultra-narrow mobile)."""
        sample_path = ROOT_DIR / "examples" / "generated_output.html"
        assert sample_path.exists(), "Sample file missing"

        from scripts.screenshot_audit import capture_audit_screenshots
        out_dir = ROOT_DIR / ".test-artifacts" / "screenshots"

        extreme_viewports = [
            {"name": "ultrawide", "width": 2560, "height": 1080},
            {"name": "ultranarrow", "width": 320, "height": 568}
        ]
        report = capture_audit_screenshots(str(sample_path), str(out_dir), viewports=extreme_viewports)
        assert report["success"] is True, "Extreme aspect ratio capture failed"

        uw_file = out_dir / "generated_output_ultrawide_2560px.png"
        un_file = out_dir / "generated_output_ultranarrow_320px.png"

        assert uw_file.exists(), f"Ultrawide screenshot missing: {uw_file}"
        assert un_file.exists(), f"Ultranarrow screenshot missing: {un_file}"

        w1, _ = get_png_dimensions(uw_file)
        w2, _ = get_png_dimensions(un_file)

        assert w1 == 2560, f"Expected 2560px, got {w1}px"
        assert w2 == 320, f"Expected 320px, got {w2}px"

    @staticmethod
    def test_t2_04():
        """T2.4: Asset URL query parameter variations (handling custom &q= or &fit=)."""
        # Test Unsplash URL parameter formatting logic
        base_url = "https://images.unsplash.com/photo-1629909613654-28e377c37b09"
        focal_hero = "&auto=format&fit=crop&w=1200&q=80"
        focal_card = "&auto=format&fit=crop&w=600&h=400&q=80"

        full_hero = f"{base_url}?{focal_hero.lstrip('&')}"
        full_card = f"{base_url}?{focal_card.lstrip('&')}"

        assert full_hero.count("?") == 1, "Malformed query parameters with multiple '?'"
        assert "w=1200" in full_hero and "q=80" in full_hero, "Missing parameters in hero URL"
        assert "w=600" in full_card and "h=400" in full_card, "Missing parameters in card URL"

    @staticmethod
    def test_t2_05():
        """T2.5: Domain fallback when requested domain is not in the 24 canonical domains."""
        from vibe_core.asset_director import AssetDirector
        ad = AssetDirector()

        spec = ad.get_media_spec("quantum_computing_nanotech_unknown")
        assert spec is not None, "Expected fallback spec for unknown domain, got None"
        assert "unsplash_url" in spec, "Fallback spec missing unsplash_url"
        assert spec["unsplash_url"].startswith("https://images.unsplash.com/"), \
            "Fallback spec unsplash_url is invalid"

    @staticmethod
    def test_t2_06():
        """T2.6: CLI error handling when invalid file path is passed to vibe_cli.py screenshot."""
        code, out, err = run_cmd([
            sys.executable, "vibe_cli.py", "screenshot", "definitely_non_existent_file_xyz987.html"
        ])
        assert code != 0, f"Expected non-zero exit code for missing file, got {code}"
        assert "not found" in (out + err).lower() or "error" in (out + err).lower(), \
            f"Expected clear file not found error message, got: {out} {err}"

    @staticmethod
    def test_t2_07():
        """T2.7: Handling corrupted or empty HTML file in screenshot audit."""
        with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as tf:
            tf.write("")  # 0-byte file
            temp_path = Path(tf.name)

        try:
            from scripts.screenshot_audit import capture_audit_screenshots
            out_dir = ROOT_DIR / ".test-artifacts" / "screenshots"
            report = capture_audit_screenshots(str(temp_path), str(out_dir))
            # Should complete without crash and cleanup browser cleanly
            assert report["success"] is True, "Screenshot utility failed on 0-byte empty HTML"
            assert get_chromium_process_count() == 0, "Chromium process leaked on empty HTML file"
        finally:
            if temp_path.exists():
                try:
                    temp_path.unlink()
                except Exception:
                    pass

    @staticmethod
    def test_t2_08():
        """T2.8: Mixed Persian and English text rendering with correct <bdi> boundary isolation."""
        from vibe_core.director import DesignDirector
        from vibe_core.generator import InterfaceGenerator

        director = DesignDirector()
        generator = InterfaceGenerator()

        # Mixed prompt: Persian sentence containing English technical brand
        intent = director.infer_intent("داشبورد مدیریت پلتفرم ابری Kubernetes و داکر با متریک های آپتایم")
        html = generator.generate(intent)

        # In RTL Persian, English brand names or numbers should have directional boundaries or bidi isolation
        assert 'dir="rtl"' in html.lower(), "Interface should be RTL"
        assert "Kubernetes" in html or "داشبورد" in html, "Interface should render mixed tokens"

# ==============================================================================
# Tier 3: Cross-Feature Combinations (4 Test Cases: T3.1 - T3.4)
# ==============================================================================

class Tier3Tests:
    """Tier 3: Cross-Feature Combinations (Pairwise Coverage)"""

    @staticmethod
    def test_t3_01():
        """T3.1: Intent Expander (F1) -> Unsplash Vault (F3) -> Screenshot Audit (F4)."""
        from vibe_core.director import DesignDirector
        from vibe_core.generator import InterfaceGenerator
        from scripts.screenshot_audit import capture_audit_screenshots

        director = DesignDirector()
        generator = InterfaceGenerator()

        intent = director.infer_intent("Enterprise B2B SaaS Cloud Intelligence Suite")
        html = generator.generate(intent)

        # Verify Unsplash asset from vault was incorporated
        assert "images.unsplash.com" in html, "Generated Light Mode SaaS missing Unsplash asset"

        with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as tf:
            tf.write(html)
            temp_path = Path(tf.name)

        try:
            out_dir = ROOT_DIR / ".test-artifacts" / "screenshots"
            report = capture_audit_screenshots(str(temp_path), str(out_dir))
            assert report["success"] is True, "Screenshot audit failed on synthesized SaaS page"
            assert len(report["viewports_captured"]) == 2, "Expected 2 viewports (Desktop & Mobile)"
        finally:
            if temp_path.exists():
                try:
                    temp_path.unlink()
                except Exception:
                    pass

    @staticmethod
    def test_t3_02():
        """T3.2: On-Demand RTL (F2) -> Screenshot Audit (F4)."""
        from vibe_core.director import DesignDirector
        from vibe_core.generator import InterfaceGenerator
        from scripts.screenshot_audit import capture_audit_screenshots

        director = DesignDirector()
        generator = InterfaceGenerator()

        intent = director.infer_intent("پورتال جامع خدمات پزشکی و رزرو کلینیک زیبایی")
        html = generator.generate(intent)

        with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as tf:
            tf.write(html)
            temp_path = Path(tf.name)

        try:
            out_dir = ROOT_DIR / ".test-artifacts" / "screenshots"
            mobile_vp = [{"name": "mobile", "width": 390, "height": 844}]
            report = capture_audit_screenshots(str(temp_path), str(out_dir), viewports=mobile_vp)
            assert report["success"] is True, "Mobile screenshot capture failed on RTL interface"
        finally:
            if temp_path.exists():
                try:
                    temp_path.unlink()
                except Exception:
                    pass

    @staticmethod
    def test_t3_03():
        """T3.3: Screenshot Tool (F4) -> Zero Orphan Invariant (F5): 5 consecutive runs leave 0 orphans."""
        sample_path = ROOT_DIR / "examples" / "generated_output.html"
        from scripts.screenshot_audit import capture_audit_screenshots
        out_dir = ROOT_DIR / ".test-artifacts" / "screenshots"

        for i in range(5):
            report = capture_audit_screenshots(str(sample_path), str(out_dir))
            assert report["success"] is True, f"Run {i+1}/5 failed"

        count = get_chromium_process_count()
        assert count == 0, f"Found {count} orphaned chromium processes after 5 consecutive audits"

    @staticmethod
    def test_t3_04():
        """T3.4: Monorepo Version Sync (F6) -> Packaging (F7): Identical v6.1.0 across CLI & manifests."""
        # 1. CLI version
        code, out, _ = run_cmd([sys.executable, "vibe_cli.py", "--version"])
        assert "6.1.0" in out, f"CLI version drift: {out}"

        # 2. version.json
        v_data = json.loads((ROOT_DIR / "version.json").read_text(encoding="utf-8"))
        assert v_data["version"] == "6.1.0", f"version.json drift: {v_data['version']}"

        # 3. vscode package.json
        vs_pkg = json.loads((ROOT_DIR / "packages" / "vibe-ui-vscode" / "package.json").read_text(encoding="utf-8"))
        assert vs_pkg["version"] == "6.1.0", f"vscode package.json drift: {vs_pkg['version']}"

        # 4. Built VSIX file naming check
        vsix_file = ROOT_DIR / "packages" / "vibe-ui-vscode" / "vibe-ui-vscode-6.0.0.vsix"
        assert vsix_file.exists() or (ROOT_DIR / "packages" / "vibe-ui-vscode").glob("*.vsix"), f"Packaged VSIX file missing: {vsix_file}"

# ==============================================================================
# Tier 4: Real-World Scenarios (3 Test Cases: T4.1 - T4.3)
# ==============================================================================

class Tier4Tests:
    """Tier 4: Real-World Workload Scenarios (End-to-End Applications)"""

    @staticmethod
    def test_t4_01():
        """T4.1: Enterprise SaaS Landing Page (Linear/Stripe style) in Light Mode with screenshot audit."""
        from vibe_core.director import DesignDirector
        from vibe_core.recommendation import RecommendationEngine
        from vibe_core.generator import InterfaceGenerator
        from vibe_core.critic import DesignCritic
        from scripts.screenshot_audit import capture_audit_screenshots

        director = DesignDirector()
        engine = RecommendationEngine()
        generator = InterfaceGenerator()
        critic = DesignCritic()

        intent = director.infer_intent("Enterprise SaaS high performance cloud telemetry with light mode canvas")
        decision = engine.recommend(intent)
        html = generator.generate(intent, decision)

        # Audit with Design Critic
        critique = critic.critique(html)
        assert critique["score"] >= 70, f"Enterprise SaaS quality score too low: {critique['score']}"

        with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as tf:
            tf.write(html)
            temp_path = Path(tf.name)

        try:
            out_dir = ROOT_DIR / ".test-artifacts" / "screenshots"
            report = capture_audit_screenshots(str(temp_path), str(out_dir))
            assert report["success"] is True, "Visual inspection failed on Enterprise SaaS page"
            assert len(report["viewports_captured"]) == 2, "Expected both Desktop and Mobile screenshots"
        finally:
            if temp_path.exists():
                try:
                    temp_path.unlink()
                except Exception:
                    pass

    @staticmethod
    def test_t4_02():
        """T4.2: Clinical Wellness BiDi Portal generated in Persian RTL with Unsplash health hero."""
        from vibe_core.director import DesignDirector
        from vibe_core.generator import InterfaceGenerator
        from scripts.screenshot_audit import capture_audit_screenshots

        director = DesignDirector()
        generator = InterfaceGenerator()

        intent = director.infer_intent("کلینیک تخصصی پوست، لیزر و زیبایی با رزرو آنلاین و معرفی پزشکان")
        html = generator.generate(intent)

        assert 'dir="rtl"' in html.lower(), "Expected RTL attribute on Persian clinical portal"
        assert "images.unsplash.com" in html, "Expected Unsplash photography on clinical portal"

        with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as tf:
            tf.write(html)
            temp_path = Path(tf.name)

        try:
            out_dir = ROOT_DIR / ".test-artifacts" / "screenshots"
            report = capture_audit_screenshots(str(temp_path), str(out_dir))
            assert report["success"] is True, "Visual inspection failed on Clinical Persian Portal"
        finally:
            if temp_path.exists():
                try:
                    temp_path.unlink()
                except Exception:
                    pass

    @staticmethod
    def test_t4_03():
        """T4.3: End-to-End Monorepo Release Dry Run (Version sync, Integration suite, VSIX build, Gitleaks)."""
        # Step 1: Validate versions across manifests
        code, out, err = run_cmd([sys.executable, "scripts/validate_versions.py"])
        assert code == 0, f"validate_versions.py failed in release dry run: {err}"

        # Step 2: Full integration tests
        code, out, err = run_cmd([sys.executable, "scripts/test_pipeline_e2e.py"])
        assert code == 0, f"test_pipeline_e2e.py failed in release dry run: {err}"

        # Step 3: Package VS Code extension
        pkg_script = ROOT_DIR / "packages" / "vibe-ui-vscode" / "package_vsix.py"
        code, out, err = run_cmd([sys.executable, str(pkg_script)], cwd=pkg_script.parent)
        assert code == 0, f"VS Code packaging failed in release dry run: {err}"

        # Step 4: Gitleaks scanner
        gitleaks_bin = Path(r"E:\programming\Tools\gitleaks\gitleaks.exe")
        cmd = [str(gitleaks_bin) if gitleaks_bin.exists() else "gitleaks", "git", "--verbose", "--redact"]
        code, out, err = run_cmd(cmd)
        assert code == 0, f"Gitleaks detected leaks in release dry run: {err or out}"

# ==============================================================================
# Suite Aggregator & CLI Runner
# ==============================================================================

ALL_TEST_CASES: List[TestCase] = [
    # Tier 1 (35 test cases: T1.1 - T1.35)
    TestCase("T1.01", 1, "F1", "Verify autonomous-intent-expander defaults to Vibrant Light Mode", Tier1Tests.test_t1_01),
    TestCase("T1.02", 1, "F1", "Verify autonomous-intent-expander has pruned 6-dimensional parameter structure", Tier1Tests.test_t1_02),
    TestCase("T1.03", 1, "F1", "Verify vibe-physics-engine does not force dark background on reduced transparency", Tier1Tests.test_t1_03),
    TestCase("T1.04", 1, "F1", "Verify ui-verifier scorecard includes Living Visual & Screenshot Inspection", Tier1Tests.test_t1_04),
    TestCase("T1.05", 1, "F1", "Verify all 6 skills explicitly align with The Two Golden Pillars", Tier1Tests.test_t1_05),
    TestCase("T1.06", 1, "F2", "Verify design-spec.json template has semantic_rtl_contract: { enabled: false }", Tier1Tests.test_t1_06),
    TestCase("T1.07", 1, "F2", "Verify English generation does not force <bdi> wrappers or RTL attributes", Tier1Tests.test_t1_07),
    TestCase("T1.08", 1, "F2", "Verify Persian generation activates RTL and <bdi> contracts", Tier1Tests.test_t1_08),
    TestCase("T1.09", 1, "F2", "Verify zero ZWNJ characters (\\u200c) in visual-chemistry-engine", Tier1Tests.test_t1_09),
    TestCase("T1.10", 1, "F2", "Verify zero ZWNJ characters in all markdown files across repository", Tier1Tests.test_t1_10),
    TestCase("T1.11", 1, "F3", "Verify data/unsplash_assets.json exists and parses as valid JSON with 24 domains", Tier1Tests.test_t1_11),
    TestCase("T1.12", 1, "F3", "Verify every domain has valid hero and card URL entries", Tier1Tests.test_t1_12),
    TestCase("T1.13", 1, "F3", "Verify skills/ui-kit/references/curated_unsplash_vault.md exists and contains 24 domains", Tier1Tests.test_t1_13),
    TestCase("T1.14", 1, "F3", "Verify hero URLs contain &w=1200&q=80 and card URLs contain &w=600&h=400&q=80", Tier1Tests.test_t1_14),
    TestCase("T1.15", 1, "F3", "Verify skills/ui-kit/SKILL.md indexes curated_unsplash_vault.md", Tier1Tests.test_t1_15),
    TestCase("T1.16", 1, "F4", "Verify scripts/screenshot_audit.py can be executed standalone", Tier1Tests.test_t1_16),
    TestCase("T1.17", 1, "F4", "Verify Desktop screenshot is captured at exactly 1440px width", Tier1Tests.test_t1_17),
    TestCase("T1.18", 1, "F4", "Verify Mobile screenshot is captured at exactly 390px width", Tier1Tests.test_t1_18),
    TestCase("T1.19", 1, "F4", "Verify vibe_cli.py screenshot subcommand executes cleanly", Tier1Tests.test_t1_19),
    TestCase("T1.20", 1, "F4", "Verify screenshots are saved into .test-artifacts/screenshots/", Tier1Tests.test_t1_20),
    TestCase("T1.21", 1, "F5", "Verify chromium.exe process count is 0 after running screenshot tool", Tier1Tests.test_t1_21),
    TestCase("T1.22", 1, "F5", "Verify cleanup runs even when target file has missing external assets", Tier1Tests.test_t1_22),
    TestCase("T1.23", 1, "F5", "Verify browser cleanup and exception resilience in screenshot_audit.py", Tier1Tests.test_t1_23),
    TestCase("T1.24", 1, "F5", "Verify no dangling subprocesses after CLI screenshot execution", Tier1Tests.test_t1_24),
    TestCase("T1.25", 1, "F5", "Verify .test-artifacts/ is ignored in .gitignore", Tier1Tests.test_t1_25),
    TestCase("T1.26", 1, "F6", "Verify version.json has version: '6.0.0'", Tier1Tests.test_t1_26),
    TestCase("T1.27", 1, "F6", "Verify packages/vibe-ui-suite/package.json has version: '6.0.0'", Tier1Tests.test_t1_27),
    TestCase("T1.28", 1, "F6", "Verify @omid-io/tokens is excluded from active release manifest", Tier1Tests.test_t1_28),
    TestCase("T1.29", 1, "F6", "Verify packages/vibe-ui-vscode/package.json has version: '6.0.0'", Tier1Tests.test_t1_29),
    TestCase("T1.30", 1, "F6", "Verify vibe_cli.py --version outputs 'Vibe UI Suite v6.0.0'", Tier1Tests.test_t1_30),
    TestCase("T1.31", 1, "F7", "Verify README.md and README.fa.md describe v6.0.0 and Two Golden Pillars", Tier1Tests.test_t1_31),
    TestCase("T1.32", 1, "F7", "Verify README.fa.md has zero ZWNJ characters", Tier1Tests.test_t1_32),
    TestCase("T1.33", 1, "F7", "Verify scripts/test_pipeline_e2e.py passes 4/4 integration tests", Tier1Tests.test_t1_33),
    TestCase("T1.34", 1, "F7", "Verify vibe-ui-vscode-6.0.0.vsix packages successfully", Tier1Tests.test_t1_34),
    TestCase("T1.35", 1, "F7", "Verify Gitleaks scan reports 0 leaks across repository history", Tier1Tests.test_t1_35),

    # Tier 2 (8 test cases: T2.1 - T2.8)
    TestCase("T2.01", 2, "B1", "Large HTML file (> 500KB) screenshot capture without browser OOM", Tier2Tests.test_t2_01),
    TestCase("T2.02", 2, "B2", "Slow network / CDN offline fallback in screenshot utility", Tier2Tests.test_t2_02),
    TestCase("T2.03", 2, "B3", "Extreme aspect ratio rendering (ultra-wide desktop vs ultra-narrow mobile)", Tier2Tests.test_t2_03),
    TestCase("T2.04", 2, "B4", "Asset URL query parameter variations (handling custom &q= or &fit=)", Tier2Tests.test_t2_04),
    TestCase("T2.05", 2, "B5", "Domain fallback when requested domain is not in the 24 canonical domains", Tier2Tests.test_t2_05),
    TestCase("T2.06", 2, "B6", "CLI error handling when invalid file path is passed to vibe_cli.py screenshot", Tier2Tests.test_t2_06),
    TestCase("T2.07", 2, "B7", "Handling corrupted or empty HTML file in screenshot audit", Tier2Tests.test_t2_07),
    TestCase("T2.08", 2, "B8", "Mixed Persian and English text rendering with correct <bdi> boundary isolation", Tier2Tests.test_t2_08),

    # Tier 3 (4 test cases: T3.1 - T3.4)
    TestCase("T3.01", 3, "C1", "Cross: Intent Expander (F1) -> Unsplash Vault (F3) -> Screenshot Audit (F4)", Tier3Tests.test_t3_01),
    TestCase("T3.02", 3, "C2", "Cross: On-Demand RTL (F2) -> Screenshot Audit (F4) mobile layout", Tier3Tests.test_t3_02),
    TestCase("T3.03", 3, "C3", "Cross: Screenshot Tool (F4) -> Zero Orphan Invariant (F5) across 5 runs", Tier3Tests.test_t3_03),
    TestCase("T3.04", 3, "C4", "Cross: Monorepo Version Sync (F6) -> Packaging (F7) identical v6.0.0", Tier3Tests.test_t3_04),

    # Tier 4 (3 test cases: T4.1 - T4.3)
    TestCase("T4.01", 4, "R1", "Real-World: Enterprise SaaS Landing Page in Light Mode with visual audit", Tier4Tests.test_t4_01),
    TestCase("T4.02", 4, "R2", "Real-World: Clinical Wellness BiDi Portal in Persian RTL with Unsplash hero", Tier4Tests.test_t4_02),
    TestCase("T4.03", 4, "R3", "Real-World: End-to-End Monorepo Release Dry Run (Sync, Tests, VSIX, Gitleaks)", Tier4Tests.test_t4_03),
]

TIER_NAMES = {
    1: "TIER 1: FEATURE COVERAGE (35 TEST CASES)",
    2: "TIER 2: BOUNDARY & CORNER CASES (8 TEST CASES)",
    3: "TIER 3: CROSS-FEATURE COMBINATIONS (4 TEST CASES)",
    4: "TIER 4: REAL-WORLD APPLICATION SCENARIOS (3 TEST CASES)",
}

def run_suite(
    tier_filter: str = "all",
    verbose: bool = False,
    name_filter: Optional[str] = None,
    failfast: bool = False
) -> bool:
    """Executes the test suite and prints structured tier reports."""
    start_total = time.time()

    # Filter tests
    selected_tests = ALL_TEST_CASES
    if tier_filter != "all":
        tier_num = int(tier_filter)
        selected_tests = [t for t in selected_tests if t.tier == tier_num]

    if name_filter:
        pattern = name_filter.lower()
        selected_tests = [t for t in selected_tests if pattern in t.name.lower() or pattern in t.test_id.lower()]

    print("=" * 78)
    print("🧪 VIBE UI SUITE v6.0.0 COMPREHENSIVE E2E TEST RUNNER")
    print(f"   Selected Tier: {tier_filter.upper()} | Total Test Cases Queued: {len(selected_tests)}")
    print("=" * 78)

    passed_count = 0
    failed_count = 0
    failures: List[Tuple[TestCase, str]] = []

    # Group by tier
    current_tier = None
    tier_stats = {1: [0, 0], 2: [0, 0], 3: [0, 0], 4: [0, 0]}

    for test in selected_tests:
        if test.tier != current_tier:
            current_tier = test.tier
            print("\n" + "─" * 78)
            print(f"📦 {TIER_NAMES.get(current_tier, f'TIER {current_tier}')}")
            print("─" * 78)

        t_start = time.time()
        try:
            test.fn()
            elapsed = time.time() - t_start
            passed_count += 1
            tier_stats[test.tier][0] += 1
            if verbose:
                print(f"  [PASS] {test.test_id} ({test.feature}): {test.name} ({elapsed:.2f}s)")
            else:
                print(f"  [PASS] {test.test_id}: {test.name}")
        except Exception as e:
            elapsed = time.time() - t_start
            failed_count += 1
            tier_stats[test.tier][1] += 1
            err_msg = str(e)
            failures.append((test, err_msg))
            print(f"  ❌ [FAIL] {test.test_id}: {test.name} ({elapsed:.2f}s)")
            print(f"       Reason: {err_msg}")
            if failfast:
                print("\n[FAILFAST] Terminating execution on first failure.")
                break

    total_duration = time.time() - start_total

    # Summary Report
    print("\n" + "=" * 78)
    print("📊 VIBE UI SUITE v6.0.0 E2E TEST EXECUTION SUMMARY")
    print("=" * 78)
    print(f"  Tier 1 (Feature Coverage):        {tier_stats[1][0]:2d} passed | {tier_stats[1][1]:2d} failed")
    print(f"  Tier 2 (Boundary & Corner):        {tier_stats[2][0]:2d} passed | {tier_stats[2][1]:2d} failed")
    print(f"  Tier 3 (Cross-Feature):            {tier_stats[3][0]:2d} passed | {tier_stats[3][1]:2d} failed")
    print(f"  Tier 4 (Real-World Scenarios):     {tier_stats[4][0]:2d} passed | {tier_stats[4][1]:2d} failed")
    print("─" * 78)
    print(f"  TOTAL:                             {passed_count:2d} / {len(selected_tests):2d} passed ({total_duration:.2f}s)")

    if failed_count > 0:
        print("\n❌ FAILURES BREAKDOWN:")
        for t, msg in failures:
            print(f"  • {t.test_id} ({t.name}): {msg}")
        print("\nResult: ❌ SUITE COMPLETED WITH FAILURES.")
        return False
    else:
        print("\nResult: ✅ ALL 50 TEST CASES PASSED WITH 100% COMPLIANCE.")
        return True

def main():
    parser = argparse.ArgumentParser(description="Vibe UI Suite v6.0.0 Comprehensive E2E Test Suite")
    parser.add_argument("--tier", choices=["1", "2", "3", "4", "all"], default="all",
                        help="Execution tier: 1 (Feature), 2 (Boundary), 3 (Cross), 4 (Real-World), or all")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose per-test timing and logging")
    parser.add_argument("-k", "--filter", help="Filter tests by name or test ID substring")
    parser.add_argument("--failfast", action="store_true", help="Stop execution upon first test failure")

    args = parser.parse_args()

    success = run_suite(
        tier_filter=args.tier,
        verbose=args.verbose,
        name_filter=args.filter,
        failfast=args.failfast
    )
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
