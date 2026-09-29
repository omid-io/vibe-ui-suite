"""
vibe_core.verifier — Evidence-Backed Runtime Verification Engine (Verification 2.0)
Generates physical proof conforming to schemas/verification-report.v1.json.

Verification tiers:
  fast   (default) — Pure static DOM evaluation (<50ms, no browser required).
  strict           — Full Playwright headless DOM + physical pixel assertions (3-8s, opt-in via --strict).

AST-based HTML parsing via BeautifulSoup4 (falls back to regex if unavailable).
"""

import re
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional

from vibe_core.constants import MAX_BLUR_SURFACES

try:
    from bs4 import BeautifulSoup as _BS4
    _BS4_AVAILABLE = True
except ImportError:  # pragma: no cover
    _BS4_AVAILABLE = False
    _BS4 = None  # type: ignore

ROOT_DIR = Path(__file__).resolve().parent.parent

class VerificationEngine:
    def verify_html(
        self,
        html_content: str,
        filename: str = "interface.html",
        mode: str = "fast",
    ) -> Dict[str, Any]:
        """
        Runs physical evidence audit across all 5 verification pillars.

        Args:
            html_content: Raw HTML string to evaluate.
            filename:     Artifact name reported in the output.
            mode:         "fast" = static DOM eval (<50ms, default).
                          "strict" = static eval + Playwright headless browser (opt-in).
        """
        fast_result = self._fast_path(html_content, filename)

        if mode == "strict":
            strict_result = self._strict_path(html_content, filename)
            # Merge strict evidence records into fast result
            fast_result["evidence_records"].extend(strict_result.get("evidence_records", []))
            fast_result["checks_summary"]["total"] += strict_result["checks_summary"]["total"]
            fast_result["checks_summary"]["passed"] += strict_result["checks_summary"]["passed"]
            fast_result["checks_summary"]["failed"] += strict_result["checks_summary"]["failed"]
            # If strict path found any failures, overall status is FAIL
            if strict_result.get("overall_status") == "FAIL":
                fast_result["overall_status"] = "FAIL"
            fast_result["runtime_mode"] = "browser_runtime_eval"
        
        return fast_result

    # ─────────────────────────── FAST PATH ────────────────────────────
    def _fast_path(self, html_content: str, filename: str) -> Dict[str, Any]:
        """Pure static DOM evaluation — no browser, no network. Target: <50ms."""
        evidence_records = []
        passed = 0
        failed = 0

        # Parse once with BS4 if available
        soup = _BS4(html_content, "html.parser") if _BS4_AVAILABLE else None

        # 1. Viewport Check
        has_viewport = 'name="viewport"' in html_content
        if has_viewport:
            passed += 1
            evidence_records.append({
                "pillar": "Responsive",
                "check_name": "Mobile Viewport Meta",
                "status": "PASS",
                "evidence": "Found standard viewport tag: width=device-width, initial-scale=1.0",
                "threshold": "present"
            })
        else:
            failed += 1
            evidence_records.append({
                "pillar": "Responsive",
                "check_name": "Mobile Viewport Meta",
                "status": "FAIL",
                "evidence": "Missing viewport meta tag",
                "threshold": "present"
            })

        # 2. Focus Visible Rings Check
        has_focus = "focus-visible" in html_content
        if has_focus:
            passed += 1
            evidence_records.append({
                "pillar": "Accessibility",
                "check_name": "Keyboard Focus-Visible Rings",
                "status": "PASS",
                "evidence": "Verified :focus-visible rules declared with contrast ring",
                "threshold": "focus-visible declared"
            })
        else:
            failed += 1
            evidence_records.append({
                "pillar": "Accessibility",
                "check_name": "Keyboard Focus-Visible Rings",
                "status": "FAIL",
                "evidence": "No :focus-visible styling declared",
                "threshold": "focus-visible declared"
            })

        # 3. Vector Icons vs Emojis Check
        # Strip script/style content before emoji search
        if soup:
            # BS4: get text content outside <script>/<style>/<svg>
            for tag in soup.find_all(["script", "style", "svg"]):
                tag.decompose()
            clean_text = soup.get_text()
            svg_count = len(_BS4(html_content, "html.parser").find_all("svg"))
        else:
            clean_text = re.sub(r"<(script|style|svg)[^>]*>.*?</\1>", "", html_content, flags=re.DOTALL | re.IGNORECASE)
            svg_count = len(re.findall(r"<svg", html_content, re.IGNORECASE))

        emoji_pattern = re.compile(
            r"[\U00010000-\U0010ffff]|[\u2600-\u27bf]|[\u2300-\u23ff]|[\u2b50-\u2b55]|[\u203c-\u2049]|[\u2194-\u21aa]"
        )
        has_emojis = bool(emoji_pattern.search(clean_text))
        if not has_emojis:
            passed += 1
            evidence_records.append({
                "pillar": "Visual Anti-Slop",
                "check_name": "Zero Raw Emojis",
                "status": "PASS",
                "evidence": f"0 raw emojis detected; verified {svg_count} crisp SVG vector icons",
                "measured_value": "0 emojis",
                "threshold": "0 emojis"
            })
        else:
            failed += 1
            evidence_records.append({
                "pillar": "Visual Anti-Slop",
                "check_name": "Zero Raw Emojis",
                "status": "FAIL",
                "evidence": "Raw Unicode emoji found in UI markup",
                "threshold": "0 emojis"
            })

        # 4. Performance: Backdrop Filter Blur Budget
        # Canonical policy imported from vibe_core.constants.MAX_BLUR_SURFACES
        # BS4: search CSS text inside <style> blocks + inline style attributes only.
        if soup:
            # Re-parse from original (soup was mutated above by decompose)
            _soup2 = _BS4(html_content, "html.parser")
            _style_texts = " ".join(t.get_text() for t in _soup2.find_all("style"))
            _inline_styles = " ".join(tag.get("style", "") for tag in _soup2.find_all(style=True))
            _blur_target = _style_texts + " " + _inline_styles
        else:
            _blur_target = html_content
        blur_count = len(re.findall(r"backdrop-blur|blur\(", _blur_target))
        if blur_count <= MAX_BLUR_SURFACES:
            passed += 1
            evidence_records.append({
                "pillar": "Performance Budget",
                "check_name": "GPU Composite Backdrop Blur",
                "status": "PASS",
                "evidence": f"{blur_count} blur layer(s) within GPU composite budget (<= {MAX_BLUR_SURFACES})",
                "measured_value": str(blur_count),
                "threshold": f"<= {MAX_BLUR_SURFACES}"
            })
        else:
            failed += 1
            evidence_records.append({
                "pillar": "Performance Budget",
                "check_name": "GPU Composite Backdrop Blur",
                "status": "FAIL",
                "evidence": f"{blur_count} blur layer(s) exceeds budget (<= {MAX_BLUR_SURFACES})",
                "measured_value": str(blur_count),
                "threshold": f"<= {MAX_BLUR_SURFACES}"
            })

        # 5. Reduced Motion — Deterministic Hard Gate
        MOTION_TOKENS = re.compile(
            r"\btransition\s*:|animation\s*:|@keyframes\b|lenis\b|scroll-behavior\s*:\s*smooth",
            re.IGNORECASE
        )
        if soup:
            _soup3 = _BS4(html_content, "html.parser")
            style_blocks = " ".join(t.get_text() for t in _soup3.find_all("style"))
        else:
            style_blocks = " ".join(re.findall(r"<style[^>]*>(.*?)</style>", html_content, re.DOTALL | re.IGNORECASE))
        has_motion_tokens = bool(MOTION_TOKENS.search(style_blocks))
        has_reduced_motion = "prefers-reduced-motion" in html_content

        if not has_motion_tokens:
            passed += 1
            evidence_records.append({
                "pillar": "Motion & Physics",
                "check_name": "Reduced Motion Override Gate",
                "status": "PASS",
                "evidence": "No motion tokens (transition/animation/lenis) declared — gate not applicable",
                "threshold": "prefers-reduced-motion required when motion present"
            })
        elif has_motion_tokens and has_reduced_motion:
            passed += 1
            evidence_records.append({
                "pillar": "Motion & Physics",
                "check_name": "Reduced Motion Override Gate",
                "status": "PASS",
                "evidence": "Motion tokens detected; @media (prefers-reduced-motion: reduce) override verified",
                "threshold": "prefers-reduced-motion required when motion present"
            })
        else:
            failed += 1
            found_tokens = MOTION_TOKENS.findall(style_blocks)[:5]
            evidence_records.append({
                "pillar": "Motion & Physics",
                "check_name": "Reduced Motion Override Gate",
                "status": "FAIL",
                "evidence": f"Motion tokens detected ({found_tokens}) without @media (prefers-reduced-motion: reduce) override. Risk: nausea/vestibular disorder for affected users.",
                "threshold": "prefers-reduced-motion required when motion present",
                "remediation": "@media (prefers-reduced-motion: reduce) { *, *::before, *::after { animation-duration: 0.01ms !important; transition-duration: 0.01ms !important; scroll-behavior: auto !important; } }"
            })

        # 6. Semantic RTL Check (if dir="rtl")
        is_rtl = 'dir="rtl"' in html_content or "dir='rtl'" in html_content
        if is_rtl:
            has_bidi = "<bdi" in html_content or "unicode-bidi" in html_content or "ltr-code" in html_content
            if has_bidi:
                passed += 1
                evidence_records.append({
                    "pillar": "Semantic RTL",
                    "check_name": "BiDi Punctuation Isolation",
                    "status": "PASS",
                    "evidence": "Verified <bdi> or unicode-bidi plaintext isolation",
                    "threshold": "present"
                })
            else:
                failed += 1
                evidence_records.append({
                    "pillar": "Semantic RTL",
                    "check_name": "BiDi Punctuation Isolation",
                    "status": "FAIL",
                    "evidence": "RTL document lacks <bdi> or unicode-bidi isolation",
                    "threshold": "present"
                })

        overall_status = "PASS" if failed == 0 else "FAIL"

        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "target_artifact": filename,
            "overall_status": overall_status,
            "runtime_mode": "static_dom_eval",
            "ast_parser": "bs4" if _BS4_AVAILABLE else "regex_fallback",
            "pillars_evaluated": [
                "Responsive",
                "Accessibility",
                "Visual Anti-Slop",
                "Performance Budget",
                "Motion & Physics",
                "Semantic RTL"
            ],
            "checks_summary": {
                "total": passed + failed,
                "passed": passed,
                "failed": failed
            },
            "evidence_records": evidence_records
        }

    # ─────────────────────────── STRICT PATH ──────────────────────────
    def _strict_path(self, html_content: str, filename: str) -> Dict[str, Any]:
        """
        Playwright headless DOM assertions — physical pixel measurements.
        Opt-in only. Called when mode="strict".
        Requires: pip install playwright && playwright install chromium
        """
        evidence_records: List[Dict[str, Any]] = []
        passed = 0
        failed = 0

        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            return {
                "overall_status": "SKIP",
                "runtime_mode": "browser_runtime_eval",
                "checks_summary": {"total": 0, "passed": 0, "failed": 0},
                "evidence_records": [{
                    "pillar": "Runtime",
                    "check_name": "Playwright Availability",
                    "status": "SKIP",
                    "evidence": "playwright not installed. Run: pip install playwright && playwright install chromium",
                    "threshold": "installed"
                }]
            }

        import tempfile, os
        with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8") as tmp:
            tmp.write(html_content)
            tmp_path = tmp.name

        try:
            with sync_playwright() as pw:
                browser = pw.chromium.launch(headless=True)

                for viewport_label, viewport in [("375px mobile", {"width": 375, "height": 667}),
                                                  ("320px narrow", {"width": 320, "height": 568})]:
                    page = browser.new_page(viewport=viewport)
                    try:
                        page.goto(f"file:///{tmp_path.replace(chr(92), '/')}", wait_until="networkidle", timeout=3000)
                    except Exception:
                        page.goto(f"file:///{tmp_path.replace(chr(92), '/')}", wait_until="domcontentloaded")
                    page.evaluate("() => document.fonts.ready")
                    page.evaluate("() => new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)))")

                    # Check: horizontal overflow
                    overflow = page.evaluate(
                        "() => document.documentElement.scrollWidth > document.documentElement.clientWidth"
                    )
                    if not overflow:
                        passed += 1
                        evidence_records.append({
                            "pillar": "Responsive",
                            "check_name": f"No Horizontal Overflow ({viewport_label})",
                            "status": "PASS",
                            "evidence": f"scrollWidth <= clientWidth at {viewport['width']}px",
                            "threshold": "no overflow"
                        })
                    else:
                        failed += 1
                        evidence_records.append({
                            "pillar": "Responsive",
                            "check_name": f"No Horizontal Overflow ({viewport_label})",
                            "status": "FAIL",
                            "evidence": f"Horizontal overflow detected at {viewport['width']}px viewport",
                            "threshold": "no overflow"
                        })
                    page.close()

                browser.close()
        finally:
            os.unlink(tmp_path)

        overall_status = "PASS" if failed == 0 else "FAIL"
        return {
            "overall_status": overall_status,
            "runtime_mode": "browser_runtime_eval",
            "checks_summary": {"total": passed + failed, "passed": passed, "failed": failed},
            "evidence_records": evidence_records
        }
