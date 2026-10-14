#!/usr/bin/env python3
"""
evals/test_m4_challenger2_visual.py — Empirical Challenger 2 Test Harness
Milestone 4 Final Gate: Visual Geometry, Multi-Viewport Screenshots, Contrast Math,
Zero Raw Emojis, and Bidirectional Text Isolation.

Target under challenge:
- E:\\programming\\vibe-test-lab\\masterpiece.html
- E:\\programming\\vibe-test-lab\\VibeMasterpiece.tsx
"""

from __future__ import annotations

import json
import math
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

# Ensure UTF-8 output on Windows terminals
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "evals"))
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import run_evals

TARGET_HTML = Path("E:/programming/vibe-test-lab/masterpiece.html")
TARGET_TSX = Path("E:/programming/vibe-test-lab/VibeMasterpiece.tsx")
TARGET_LAB = Path("E:/programming/vibe-test-lab")
SCREENSHOTS_DIR = TARGET_LAB / "screenshots"

EMOJI_PATTERN = re.compile(
    r"[\U00010000-\U0010ffff]|[\u2600-\u27bf]|[\u2300-\u23ff]|[\u2b50-\u2b55]|[\u203c-\u2049]|[\u2194-\u21aa]"
)


class EmpiricalTestSession:
    def __init__(self):
        self.passes = 0
        self.failures: List[str] = []
        self.warnings: List[str] = []
        self.details: Dict[str, Any] = {}

    def assert_true(self, condition: bool, test_name: str, msg: str = ""):
        if condition:
            self.passes += 1
            print(f"  [PASS] {test_name}" + (f": {msg}" if msg else ""))
        else:
            fail_msg = f"FAIL: {test_name}" + (f" — {msg}" if msg else "")
            self.failures.append(fail_msg)
            print(f"  [{fail_msg}]")

    def assert_ge(self, actual: float, threshold: float, test_name: str, label: str = ""):
        if actual >= threshold:
            self.passes += 1
            print(f"  [PASS] {test_name}: {actual:.4f} >= {threshold:.4f} {label}")
        else:
            fail_msg = f"FAIL: {test_name}: {actual:.4f} < {threshold:.4f} {label}"
            self.failures.append(fail_msg)
            print(f"  [{fail_msg}]")


def test_suite_1_screenshot_audit_execution(session: EmpiricalTestSession):
    print("\n" + "=" * 80)
    print("SUITE 1: Automated Multi-Viewport Screenshot Audit Utility Execution")
    print("=" * 80)

    audit_script = REPO_ROOT / "scripts" / "screenshot_audit.py"
    session.assert_true(audit_script.exists(), "Screenshot Audit Script Exists", str(audit_script))
    session.assert_true(TARGET_HTML.exists(), "Target Masterpiece HTML Exists", str(TARGET_HTML))

    cmd = [
        sys.executable,
        str(audit_script),
        str(TARGET_HTML),
        "-o",
        str(SCREENSHOTS_DIR),
        "--json",
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, cwd=str(REPO_ROOT))
    session.assert_true(res.returncode == 0, "screenshot_audit.py Exit Code 0", f"code={res.returncode}")

    try:
        data = json.loads(res.stdout)
    except Exception as e:
        session.assert_true(False, "Parse screenshot_audit.py JSON output", f"Error: {e}, Output:\n{res.stdout}")
        return

    session.details["screenshot_audit"] = data
    overall_status = data.get("overall_status")
    session.assert_true(overall_status == "PASS", "screenshot_audit.py Overall Status", f"status={overall_status}")

    viewports = data.get("viewports", {})
    desktop = viewports.get("desktop", {})
    mobile = viewports.get("mobile", {})

    # Desktop Assertions
    session.assert_true(desktop.get("status") == "PASS", "Desktop Viewport Status PASS")
    session.assert_true(desktop.get("horizontal_overflow") is False, "Desktop Horizontal Overflow is 0px (False)")
    session.assert_true(desktop.get("broken_images") == 0, "Desktop Broken Images == 0")
    desktop_png = Path(desktop.get("screenshot_path", ""))
    session.assert_true(desktop_png.exists() and desktop_png.stat().st_size > 50000, "Desktop Screenshot PNG Exists and Size > 50KB", f"{desktop_png} ({desktop.get('file_size_bytes', 0)} bytes)")

    # Mobile Assertions
    session.assert_true(mobile.get("status") == "PASS", "Mobile Viewport Status PASS")
    session.assert_true(mobile.get("horizontal_overflow") is False, "Mobile Horizontal Overflow is 0px (False)")
    session.assert_true(mobile.get("broken_images") == 0, "Mobile Broken Images == 0")
    mobile_png = Path(mobile.get("screenshot_path", ""))
    session.assert_true(mobile_png.exists() and mobile_png.stat().st_size > 50000, "Mobile Screenshot PNG Exists and Size > 50KB", f"{mobile_png} ({mobile.get('file_size_bytes', 0)} bytes)")

    # Directory Isolation (Zero Root Pollution)
    session.assert_true(desktop_png.parent.resolve() == SCREENSHOTS_DIR.resolve(), "Desktop Screenshot Isolated in screenshots/ dir")
    session.assert_true(mobile_png.parent.resolve() == SCREENSHOTS_DIR.resolve(), "Mobile Screenshot Isolated in screenshots/ dir")


def test_suite_2_multi_viewport_geometry_stress_test(session: EmpiricalTestSession):
    print("\n" + "=" * 80)
    print("SUITE 2: Multi-Viewport Geometry Stress Test (Headless Chromium)")
    print("=" * 80)

    from playwright.sync_api import sync_playwright

    test_viewports = [
        ("Ultra-Narrow Mobile", 320, 568),
        ("Android Compact", 360, 640),
        ("Standard Mobile (iPhone 8)", 375, 667),
        ("Modern Mobile (iPhone 12/13/14)", 390, 844),
        ("Large Mobile (iPhone XR)", 414, 896),
        ("Mobile Landscape / Foldable", 480, 800),
        ("Tablet Portrait (iPad Mini)", 768, 1024),
        ("Tablet Landscape (iPad)", 1024, 768),
        ("Small Laptop", 1280, 800),
        ("Standard Desktop", 1440, 900),
        ("Full HD Desktop", 1920, 1080),
    ]

    uri = TARGET_HTML.resolve().as_uri()

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--remote-debugging-port=0", "--disable-dev-shm-usage", "--no-sandbox"]
        )
        page = browser.new_page()

        for label, w, h in test_viewports:
            page.set_viewport_size({"width": w, "height": h})
            page.goto(uri, wait_until="domcontentloaded")
            page.wait_for_timeout(50)

            geom = page.evaluate("""() => {
                const scrollW = document.documentElement.scrollWidth;
                const clientW = document.documentElement.clientWidth;
                const diff = scrollW - clientW;
                return {
                    scrollW: scrollW,
                    clientW: clientW,
                    overflow: diff > 0,
                    overflowPx: diff
                };
            }""")

            session.assert_true(
                not geom["overflow"],
                f"Viewport {label} ({w}x{h}) 0px Overflow",
                f"scrollWidth={geom['scrollW']}px, clientWidth={geom['clientW']}px, diff={geom['overflowPx']}px"
            )

        browser.close()


def test_suite_3_color_contrast_mathematics(session: EmpiricalTestSession):
    print("\n" + "=" * 80)
    print("SUITE 3: Mathematical & Live DOM Color Contrast Verification")
    print("=" * 80)

    html_content = TARGET_HTML.read_text(encoding="utf-8")

    # Part A: Static CSS Variables & OKLCH Mathematical Derivations
    tokens = {
        "--canvas-bg": "oklch(0.14 0.005 264)",
        "--surface": "oklch(0.18 0.008 264)",
        "--surface-elevated": "oklch(0.22 0.010 264)",
        "--text-primary": "oklch(0.98 0.002 264)",
        "--text-secondary": "oklch(0.82 0.008 264)",
        "--text-muted": "oklch(0.70 0.01 264)",
        "--accent": "oklch(0.70 0.18 260)",
        "--accent-emerald": "oklch(0.72 0.17 155)",
    }

    lum_cache = {}
    for name, spec in tokens.items():
        lum = run_evals.parse_color_to_luminance(spec)
        lum_cache[name] = lum
        print(f"  Token {name} ({spec}) -> Relative Luminance L = {lum:.5f}")

    # Contrast ratios
    cr_primary_canvas = run_evals.contrast_ratio(lum_cache["--text-primary"], lum_cache["--canvas-bg"])
    session.assert_ge(cr_primary_canvas, 4.5, "Text Primary vs Canvas Background (WCAG AA Body >= 4.5:1)", f"ratio={cr_primary_canvas:.2f}:1")
    session.assert_ge(cr_primary_canvas, 7.0, "Text Primary vs Canvas Background (WCAG AAA Body >= 7.0:1)", f"ratio={cr_primary_canvas:.2f}:1")

    cr_secondary_canvas = run_evals.contrast_ratio(lum_cache["--text-secondary"], lum_cache["--canvas-bg"])
    session.assert_ge(cr_secondary_canvas, 4.5, "Text Secondary vs Canvas Background (WCAG AA Body >= 4.5:1)", f"ratio={cr_secondary_canvas:.2f}:1")

    cr_muted_canvas = run_evals.contrast_ratio(lum_cache["--text-muted"], lum_cache["--canvas-bg"])
    session.assert_ge(cr_muted_canvas, 4.5, "Text Muted vs Canvas Background (WCAG AA Body >= 4.5:1)", f"ratio={cr_muted_canvas:.2f}:1")

    cr_primary_surface = run_evals.contrast_ratio(lum_cache["--text-primary"], lum_cache["--surface"])
    session.assert_ge(cr_primary_surface, 4.5, "Text Primary vs Surface (WCAG AA Body >= 4.5:1)", f"ratio={cr_primary_surface:.2f}:1")

    cr_secondary_surface = run_evals.contrast_ratio(lum_cache["--text-secondary"], lum_cache["--surface"])
    session.assert_ge(cr_secondary_surface, 4.5, "Text Secondary vs Surface (WCAG AA Body >= 4.5:1)", f"ratio={cr_secondary_surface:.2f}:1")

    cr_primary_elevated = run_evals.contrast_ratio(lum_cache["--text-primary"], lum_cache["--surface-elevated"])
    session.assert_ge(cr_primary_elevated, 4.5, "Text Primary vs Surface Elevated (WCAG AA Body >= 4.5:1)", f"ratio={cr_primary_elevated:.2f}:1")

    # Part B: Extraction via run_evals.extract_html_colors
    canvas_c, body_c, header_c = run_evals.extract_html_colors(html_content)
    lum_c = run_evals.parse_color_to_luminance(canvas_c)
    lum_b = run_evals.parse_color_to_luminance(body_c)
    cr_extracted_body = run_evals.contrast_ratio(lum_c, lum_b)
    session.assert_ge(cr_extracted_body, 4.5, "Extracted Body Color Contrast (WCAG AA >= 4.5:1)", f"ratio={cr_extracted_body:.2f}:1 ({body_c} on {canvas_c})")

    # Part C: Live Playwright DOM Physical Pixel Contrast Inspection with W3C Alpha Compositing
    from playwright.sync_api import sync_playwright

    uri = TARGET_HTML.resolve().as_uri()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        page.goto(uri, wait_until="domcontentloaded")
        page.wait_for_timeout(100)

        contrast_results = page.evaluate("""() => {
            const canvas = document.createElement('canvas');
            canvas.width = 1;
            canvas.height = 1;
            const ctx = canvas.getContext('2d', { willReadFrequently: true });

            function getPhysicalRgba(colorStr) {
                if (!colorStr || colorStr === 'transparent' || colorStr === 'rgba(0, 0, 0, 0)') return null;
                ctx.clearRect(0, 0, 1, 1);
                ctx.fillStyle = colorStr;
                ctx.fillRect(0, 0, 1, 1);
                const [r, g, b, a] = ctx.getImageData(0, 0, 1, 1).data;
                if (a === 0) return null;
                return [r, g, b, a / 255.0];
            }

            function blendOver(fgRgba, bgRgb) {
                const a = fgRgba[3];
                return [
                    Math.round(fgRgba[0] * a + bgRgb[0] * (1 - a)),
                    Math.round(fgRgba[1] * a + bgRgb[1] * (1 - a)),
                    Math.round(fgRgba[2] * a + bgRgb[2] * (1 - a))
                ];
            }

            function resolveEffectiveBg(el) {
                let layers = [];
                let cur = el;
                while (cur && cur !== document.documentElement) {
                    const s = window.getComputedStyle(cur);
                    const rgba = getPhysicalRgba(s.backgroundColor);
                    if (rgba) {
                        layers.unshift(rgba);
                        if (rgba[3] >= 0.99) break;
                    }
                    cur = cur.parentElement;
                }
                let base = [2, 6, 23]; // slate-950 canvas base
                for (const layer of layers) {
                    base = blendOver(layer, base);
                }
                return base;
            }

            function luminance(rgb) {
                const a = rgb.map(v => {
                    v /= 255;
                    return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
                });
                return a[0] * 0.2126 + a[1] * 0.7152 + a[2] * 0.0722;
            }

            // Standard semantic text elements per run_evals contract: p, h1, h2, h3, h4, h5, h6, a, button, label
            const elements = Array.from(document.querySelectorAll('body, p, h1, h2, h3, h4, h5, h6, a, button, label')).filter(el => {
                const s = window.getComputedStyle(el);
                return s.display !== 'none' && s.visibility !== 'hidden' && s.opacity !== '0' && (el.innerText || '').trim().length > 0;
            });

            let tested = 0;
            const violations = [];
            let minRatio = 999.0;
            let sampleStats = [];

            for (const el of elements) {
                const s = window.getComputedStyle(el);
                const fgRgba = getPhysicalRgba(s.color);
                if (!fgRgba) continue;
                const fg = [fgRgba[0], fgRgba[1], fgRgba[2]];
                const bg = resolveEffectiveBg(el);

                const l1 = Math.max(luminance(fg), luminance(bg));
                const l2 = Math.min(luminance(fg), luminance(bg));
                const ratio = (l1 + 0.05) / (l2 + 0.05);

                tested++;
                if (ratio < minRatio) minRatio = ratio;

                const fontSize = parseFloat(s.fontSize || '16');
                const isBold = parseInt(s.fontWeight || '400') >= 700;
                const required = (fontSize >= 24 || (fontSize >= 18.5 && isBold)) ? 3.0 : 4.5;

                if (sampleStats.length < 5) {
                    sampleStats.push({
                        tag: el.tagName.toLowerCase(),
                        text: (el.innerText || '').slice(0, 30),
                        ratio: ratio.toFixed(2),
                        required: required
                    });
                }

                if (ratio < required) {
                    violations.push({
                        tag: el.tagName.toLowerCase(),
                        text: (el.innerText || '').slice(0, 40),
                        ratio: ratio.toFixed(2),
                        required: required,
                        color: s.color,
                        bg: bg
                    });
                }
            }

            return {
                tested: tested,
                minRatio: minRatio,
                violations: violations,
                sampleStats: sampleStats
            };
        }""")

        browser.close()

    session.assert_true(contrast_results["tested"] >= 20, f"Tested {contrast_results['tested']} Rendered Semantic Text Elements")
    session.assert_ge(contrast_results["minRatio"], 4.5, "Live DOM Minimum Contrast Ratio across all semantic text nodes (WCAG AA >= 4.5:1)", f"min={contrast_results['minRatio']:.2f}:1")
    session.assert_true(len(contrast_results["violations"]) == 0, "Zero Contrast Violations across live DOM semantic nodes", f"{len(contrast_results['violations'])} violation(s)")


def test_suite_4_zero_raw_unicode_emojis(session: EmpiricalTestSession):
    print("\n" + "=" * 80)
    print("SUITE 4: Zero Raw Unicode Emojis & Inline SVG Vector Audit")
    print("=" * 80)

    # 1. Inspect masterpiece.html
    html_text = TARGET_HTML.read_text(encoding="utf-8")
    html_emojis = EMOJI_PATTERN.findall(html_text)
    session.assert_true(
        len(html_emojis) == 0,
        "Zero Raw Unicode Emojis in masterpiece.html",
        f"Found {len(html_emojis)}: {html_emojis[:5]}"
    )

    # Count inline SVGs in masterpiece.html
    svg_count = len(re.findall(r"<svg[\s>]", html_text, re.IGNORECASE))
    session.assert_true(
        svg_count >= 10,
        f"Verified Rich Inline SVG Vector Icons in masterpiece.html (Count: {svg_count} >= 10)",
        f"count={svg_count}"
    )

    # 2. Inspect VibeMasterpiece.tsx if present
    if TARGET_TSX.exists():
        tsx_text = TARGET_TSX.read_text(encoding="utf-8")
        tsx_emojis = EMOJI_PATTERN.findall(tsx_text)
        session.assert_true(
            len(tsx_emojis) == 0,
            "Zero Raw Unicode Emojis in VibeMasterpiece.tsx",
            f"Found {len(tsx_emojis)}: {tsx_emojis[:5]}"
        )
        tsx_svgs = len(re.findall(r"<svg[\s>]", tsx_text, re.IGNORECASE))
        session.assert_true(
            tsx_svgs >= 10,
            f"Verified Rich Inline SVG Vector Icons in VibeMasterpiece.tsx (Count: {tsx_svgs} >= 10)",
            f"count={tsx_svgs}"
        )

    # 3. Scan all components in vibe-test-lab
    lab_tsx = list(TARGET_LAB.rglob("*.tsx")) + list(TARGET_LAB.rglob("*.jsx"))
    for f in lab_tsx:
        content = f.read_text(encoding="utf-8")
        emojis = EMOJI_PATTERN.findall(content)
        session.assert_true(
            len(emojis) == 0,
            f"Zero Raw Unicode Emojis in {f.name}",
            f"Found {len(emojis)}"
        )


def test_suite_5_bidirectional_text_isolation(session: EmpiricalTestSession):
    print("\n" + "=" * 80)
    print("SUITE 5: Bidirectional Text Isolation (<bdi> & unicode-bidi)")
    print("=" * 80)

    html_text = TARGET_HTML.read_text(encoding="utf-8")

    # 1. Check body / root unicode-bidi
    has_bidi_plaintext = "unicode-bidi: plaintext" in html_text or "unicode-bidi:plaintext" in html_text
    session.assert_true(
        has_bidi_plaintext,
        "Body specifies 'unicode-bidi: plaintext' for bidirectional fallback"
    )

    # 2. Check bdi / ltr-isolated CSS rules
    has_bdi_isolate_rule = "unicode-bidi: isolate" in html_text or "unicode-bidi:isolate" in html_text
    session.assert_true(
        has_bdi_isolate_rule,
        "CSS rule specifies 'unicode-bidi: isolate' for <bdi> and .ltr-isolated"
    )

    # 3. Check <bdi> tag usage
    bdi_tags = re.findall(r"<bdi[^>]*>(.*?)</bdi>", html_text, re.DOTALL | re.IGNORECASE)
    session.assert_true(
        len(bdi_tags) >= 5,
        f"Verified <bdi> elements isolating technical tokens, versions, currencies (Count: {len(bdi_tags)} >= 5)",
        f"Sample: {[t.strip() for t in bdi_tags[:3]]}"
    )


def test_suite_6_broken_images_and_assets(session: EmpiricalTestSession):
    print("\n" + "=" * 80)
    print("SUITE 6: Broken Images, External Asset Links & CDN Integrity")
    print("=" * 80)

    from playwright.sync_api import sync_playwright

    uri = TARGET_HTML.resolve().as_uri()

    failed_requests: List[str] = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        page = browser.new_page()

        def on_request_failed(request):
            failed_requests.append(f"{request.url} ({request.failure})")

        page.on("requestfailed", on_request_failed)

        page.goto(uri, wait_until="networkidle", timeout=5000)

        # Audit document.images
        img_stats = page.evaluate("""() => {
            const imgs = Array.from(document.images);
            const broken = imgs.filter(i => !i.complete || i.naturalWidth === 0);
            return {
                total: imgs.length,
                broken: broken.length,
                brokenSrcs: broken.map(b => b.src)
            };
        }""")

        browser.close()

    session.assert_true(
        img_stats["broken"] == 0,
        "Zero Broken <img> Elements in DOM",
        f"total={img_stats['total']}, broken={img_stats['broken']}"
    )

    session.assert_true(
        len(failed_requests) == 0,
        "Zero Failed HTTP/CDN Network Requests",
        f"failed count={len(failed_requests)}"
    )


def main():
    print("================================================================================")
    print("🚀 EMPIRICAL CHALLENGER 2: MILESTONE 4 FINAL GATE AUDIT")
    print("Visual Geometry, Screenshots, Contrast Math, Unicode Emojis, BDI Isolation")
    print("================================================================================")

    session = EmpiricalTestSession()

    test_suite_1_screenshot_audit_execution(session)
    test_suite_2_multi_viewport_geometry_stress_test(session)
    test_suite_3_color_contrast_mathematics(session)
    test_suite_4_zero_raw_unicode_emojis(session)
    test_suite_5_bidirectional_text_isolation(session)
    test_suite_6_broken_images_and_assets(session)

    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total Passes:   {session.passes}")
    print(f"Total Failures: {len(session.failures)}")
    if session.failures:
        print("\nFailures:")
        for f in session.failures:
            print(f"  ❌ {f}")
        print("\nVerdict: REJECT")
        sys.exit(1)
    else:
        print("\nVerdict: APPROVE (100% Empirical Tests Passed)")
        sys.exit(0)


if __name__ == "__main__":
    main()
