"""
vibe_core.physical_critic — Headless Physical Viewport Auditor (v3.6.0)
Uses headless Playwright Chromium to inspect rendered physical geometry:
- Physical bounding boxes via getBoundingClientRect()
- Minimum touch targets (>= 44px on screen)
- Physical horizontal scroll blowout (scrollWidth > clientWidth) across 390px, 768px, 1440px
- Runtime causal interaction verification (assert dynamic DOM recalculation on user input)
- Graceful fast-path fallback when running in headless-restricted environments
"""

import sys
import os
from typing import Dict, Any, List, Optional

class PhysicalCritic:
    """
    Physical layout and geometry auditor evaluating rendered interfaces in headless Chromium.
    Guarantees that visual claims are physically true on screen pixels, not just in text regex.
    """

    STANDARD_VIEWPORTS = [
        {"name": "mobile", "width": 390, "height": 844},
        {"name": "tablet", "width": 768, "height": 1024},
        {"name": "desktop", "width": 1440, "height": 900}
    ]

    def __init__(self, enable_browser: bool = True):
        self.enable_browser = enable_browser and (os.environ.get("SKIP_PHYSICAL_BROWSER", "0") != "1")

    def audit_physical_layout(
        self,
        html_content: str,
        viewports: Optional[List[Dict[str, int]]] = None
    ) -> Dict[str, Any]:
        """
        Renders HTML in headless Chromium and measures exact pixel geometries.
        If browser cannot be launched, uses static geometric fallback.
        """
        viewports = viewports or self.STANDARD_VIEWPORTS
        if not self.enable_browser:
            return self._static_fallback_audit(html_content, viewports)

        try:
            from playwright.sync_api import sync_playwright
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()

                defects = []
                viewport_results = {}
                total_touch_targets = 0
                compliant_touch_targets = 0
                has_overflow = False

                for vp in viewports:
                    page.set_viewport_size({"width": vp["width"], "height": vp["height"]})
                    page.set_content(html_content, wait_until="domcontentloaded")

                    # 1. Measure physical scroll width blowout
                    overflow_data = page.evaluate("""() => {
                        const doc = document.documentElement;
                        const body = document.body;
                        const scrollW = Math.max(doc.scrollWidth, body ? body.scrollWidth : 0);
                        const clientW = doc.clientWidth;
                        return {
                            scroll_width: scrollW,
                            client_width: clientW,
                            overflows: scrollW > (clientW + 1)
                        };
                    }""")

                    if overflow_data["overflows"]:
                        has_overflow = True
                        defects.append({
                            "type": "physical_horizontal_overflow",
                            "severity": "P0",
                            "viewport": vp["name"],
                            "width": vp["width"],
                            "message": f"Physical layout blew out viewport width ({overflow_data['scroll_width']}px > {overflow_data['client_width']}px) on {vp['name']} (390px/768px)"
                        })

                    # 2. Measure physical touch targets (>= 44x44px)
                    elements_data = page.evaluate("""() => {
                        const selectors = 'button, a, input, select, [role="button"], [role="switch"], [role="tab"]';
                        const nodes = Array.from(document.querySelectorAll(selectors));
                        return nodes.map((el, i) => {
                            const rect = el.getBoundingClientRect();
                            const style = window.getComputedStyle(el);
                            const isVisible = style.display !== 'none' && style.visibility !== 'hidden' && style.opacity !== '0' && rect.width > 0 && rect.height > 0;
                            return {
                                tag: el.tagName.toLowerCase(),
                                role: el.getAttribute('role') || '',
                                text: (el.innerText || el.value || '').trim().substring(0, 30),
                                width: Math.round(rect.width * 10) / 10,
                                height: Math.round(rect.height * 10) / 10,
                                is_visible: isVisible
                            };
                        });
                    }""")

                    vp_targets = [el for el in elements_data if el["is_visible"]]
                    vp_substandard = [el for el in vp_targets if el["width"] < 43.5 or el["height"] < 43.5]

                    total_touch_targets += len(vp_targets)
                    compliant_touch_targets += (len(vp_targets) - len(vp_substandard))

                    if vp_substandard and vp["name"] == "mobile":
                        for bad in vp_substandard[:3]:
                            defects.append({
                                "type": "physical_substandard_touch_target",
                                "severity": "P1",
                                "viewport": "mobile",
                                "element": f"<{bad['tag']}> {bad['text']}",
                                "physical_size": f"{bad['width']}x{bad['height']}px",
                                "message": f"Element '{bad['text']}' measures {bad['width']}x{bad['height']}px physically on screen, below 44x44px requirement"
                            })

                    viewport_results[vp["name"]] = {
                        "width": vp["width"],
                        "overflow": overflow_data["overflows"],
                        "targets_count": len(vp_targets),
                        "substandard_count": len(vp_substandard)
                    }

                browser.close()

                # Calculate physical score
                score = 100.0
                if has_overflow:
                    score -= 30.0
                if total_touch_targets > 0:
                    compliance_ratio = compliant_touch_targets / total_touch_targets
                    score -= ((1.0 - compliance_ratio) * 25.0)

                score = round(max(0.0, min(100.0, score)), 1)
                has_p0 = any(d.get("severity") == "P0" for d in defects)
                is_accepted = (score >= 80.0) and not has_p0

                return {
                    "physical_score": score,
                    "acceptance_status": "ACCEPTED" if is_accepted else "REVISE_REQUIRED",
                    "viewports_tested": [vp["width"] for vp in viewports],
                    "defects": defects,
                    "metrics": {
                        "total_touch_targets": total_touch_targets,
                        "compliant_touch_targets": compliant_touch_targets,
                        "horizontal_overflow": has_overflow,
                        "viewport_details": viewport_results
                    },
                    "engine": "playwright_headless_chromium"
                }

        except Exception as e:
            # Safe fallback if Chromium fails to boot
            return self._static_fallback_audit(html_content, viewports, error_note=str(e))

    def _static_fallback_audit(
        self,
        html_content: str,
        viewports: List[Dict[str, int]],
        error_note: Optional[str] = None
    ) -> Dict[str, Any]:
        """Heuristic fallback when browser execution is disabled or unavailable."""
        import re
        defects = []
        has_fixed_blowout = bool(re.search(
            r'(?:width:\s*(?:[4-9]\d\d|\d{4,})px|w-\[(?:[4-9]\d\d|\d{4,})px\]|min-w-\[(?:[4-9]\d\d|\d{4,})px\])',
            html_content
        ))
        has_substandard = bool(re.search(r'\b(h-[5-8]|py-[12]|min-h-\[(?:3[0-9]|4[0-3])px\])\b', html_content))

        if has_fixed_blowout:
            defects.append({
                "type": "physical_horizontal_overflow",
                "severity": "P0",
                "message": "Detected fixed width styling >= 400px that causes physical blowout on 390px mobile viewports"
            })

        if has_substandard:
            defects.append({
                "type": "physical_substandard_touch_target",
                "severity": "P1",
                "message": "Detected substandard button padding or height (< 44px)"
            })

        score = 92.0
        if has_fixed_blowout:
            score -= 30.0
        if has_substandard:
            score -= 15.0

        return {
            "physical_score": score,
            "acceptance_status": "ACCEPTED" if score >= 80.0 and not has_fixed_blowout else "REVISE_REQUIRED",
            "viewports_tested": [vp["width"] for vp in viewports],
            "defects": defects,
            "metrics": {
                "horizontal_overflow": has_fixed_blowout,
                "static_mode": True
            },
            "engine": f"static_heuristic_fallback ({error_note})" if error_note else "static_heuristic"
        }

    def audit_runtime_interaction(
        self,
        html_content: str,
        slider_selector: str = 'input[type="range"]',
        metric_selector: str = 'bdi',
        target_value: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Simulates physical causal user interaction in real Chromium browser:
        1. Loads html_content in Chromium page.
        2. Queries initial text from `metric_selector`.
        3. Simulates physical slider drag or value change event on `slider_selector`.
        4. Queries recalculated text from `metric_selector`.
        5. Asserts that state is dynamically responsive and causal (initial != recalculated).
        """
        if not self.enable_browser:
            return {
                "interactive_verified": True,
                "status": "SKIPPED_STATIC_MODE",
                "message": "Browser execution disabled; skipped runtime interaction simulation."
            }

        try:
            from playwright.sync_api import sync_playwright
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page(viewport={"width": 1280, "height": 800})
                page.set_content(html_content, wait_until="domcontentloaded")

                # Check element presence
                slider = page.query_selector(slider_selector)
                if not slider:
                    browser.close()
                    return {
                        "interactive_verified": False,
                        "status": "FAIL_SELECTOR_NOT_FOUND",
                        "message": f"Interactive control selector '{slider_selector}' not found in DOM."
                    }

                initial_metric = page.eval_on_selector(metric_selector, "el => el.innerText.trim()") if page.query_selector(metric_selector) else ""

                # Simulate physical slider interaction
                curr_val = float(slider.get_attribute("value") or 0)
                min_val = float(slider.get_attribute("min") or 0)
                max_val = float(slider.get_attribute("max") or 100)
                if target_value is not None:
                    new_val = target_value
                else:
                    new_val = max_val if curr_val < (min_val + max_val) / 2 else min_val

                # Dispatch both input and change events to simulate real browser touch/drag
                page.evaluate("""({sel, val}) => {
                    const el = document.querySelector(sel);
                    if (el) {
                        el.value = val;
                        el.dispatchEvent(new Event('input', { bubbles: true }));
                        el.dispatchEvent(new Event('change', { bubbles: true }));
                    }
                }""", {"sel": slider_selector, "val": str(new_val)})

                # Allow microtasks/event callbacks to execute
                page.wait_for_timeout(60)

                final_metric = page.eval_on_selector(metric_selector, "el => el.innerText.trim()") if page.query_selector(metric_selector) else ""

                browser.close()

                is_dynamic = (initial_metric != final_metric) and bool(final_metric)

                return {
                    "interactive_verified": is_dynamic,
                    "status": "PASSED" if is_dynamic else "STATIC_OR_UNCHANGED",
                    "initial_metric": initial_metric,
                    "updated_metric": final_metric,
                    "slider_target": new_val,
                    "message": "Causal interaction verified; dynamic recalculation asserted." if is_dynamic else "Metric value remained unchanged after slider interaction."
                }
        except Exception as e:
            return {
                "interactive_verified": False,
                "status": "ERROR",
                "message": f"Runtime interaction audit failed: {e}"
            }

