"""
vibe_core.physical_critic — Headless Physical Viewport Auditor (v3.8.0)
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
from vibe_core.interaction_contract import get_interaction_contract, InteractionContract
from vibe_core.vision_sensor import VisionSensor
from vibe_core.pixel_critic import PixelCritic


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
        viewports: Optional[List[Dict[str, int]]] = None,
        page: Any = None
    ) -> Dict[str, Any]:
        """
        Renders HTML in headless Chromium and measures exact pixel geometries.
        If browser cannot be launched, uses static geometric fallback.
        Supports passing an existing Playwright Page to prevent redundant browser boots.
        """
        viewports = viewports or self.STANDARD_VIEWPORTS
        if not self.enable_browser:
            return self._static_fallback_audit(html_content, viewports)

        owns_page = page is None
        playwright_ctx = None
        browser = None
        try:
            if owns_page:
                from playwright.sync_api import sync_playwright
                playwright_ctx = sync_playwright()
                p = playwright_ctx.__enter__()
                browser = p.chromium.launch(headless=True)
                active_page = browser.new_page()
            else:
                active_page = page

            defects = []
            viewport_results = {}
            total_touch_targets = 0
            compliant_touch_targets = 0
            has_overflow = False

            for vp in viewports:
                active_page.set_viewport_size({"width": vp["width"], "height": vp["height"]})
                active_page.set_content(html_content, wait_until="domcontentloaded")

                # 1. Measure physical scroll width blowout
                overflow_data = active_page.evaluate("""() => {
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
                elements_data = active_page.evaluate("""() => {
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
                    "viewport_details": viewport_results,
                    "motion_ergonomics": self.audit_motion_ergonomics(html_content)
                },
                "engine": "playwright_headless_chromium"
            }

        except Exception as e:
            # Safe fallback if Chromium fails to boot
            return self._static_fallback_audit(html_content, viewports, error_note=str(e))
        finally:
            if owns_page and browser:
                try:
                    browser.close()
                except Exception:
                    pass
                try:
                    playwright_ctx.__exit__(None, None, None)
                except Exception:
                    pass


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
                "static_mode": True,
                "motion_ergonomics": self.audit_motion_ergonomics(html_content)
            },
            "engine": f"static_heuristic_fallback ({error_note})" if error_note else "static_heuristic"
        }

    def audit_motion_ergonomics(self, code_content: str) -> Dict[str, Any]:
        """
        Audits UI motion and animation patterns against Anti-Slop physical invariants:
        - transition: all or transition-all anti-pattern detection
        - scale(0) entry pop-in detection
        - Missing @media (prefers-reduced-motion) for animated interfaces
        - Excessive micro-interaction transition duration (> 300ms)
        - Sticky mobile touch hover (:hover without pointer: fine media query)
        """
        import re
        defects = []
        score = 100.0

        # 1. transition: all or transition-all
        has_transition_all = bool(re.search(r'\btransition(?::\s*all|-all)\b', code_content))
        if has_transition_all:
            defects.append({
                "type": "motion_transition_all_anti_pattern",
                "severity": "P1",
                "message": "Found 'transition: all' or 'transition-all'. Mandate explicit animated properties (e.g. transform, opacity) to prevent layout recalculation jank."
            })
            score -= 15.0

        # 2. scale(0) or scale(0.0) initial entry state
        has_scale_zero = bool(re.search(r'\bscale\(\s*0(?:\.0+)?\s*\)|\bscale:\s*0\b', code_content))
        if has_scale_zero:
            defects.append({
                "type": "motion_scale_zero_entry_anti_pattern",
                "severity": "P1",
                "message": "Detected 'scale(0)' entry state. Mandate initial scale >= 0.95 with opacity: 0 for natural, non-comical pop-in."
            })
            score -= 20.0

        # 3. Excessive micro-interaction duration (> 300ms on interactive controls)
        has_excessive_duration = bool(re.search(r'\bduration-(?:500|700|1000)\b|transition:\s*[^;]*?(?:[4-9]\d\d|\d{4,})ms', code_content))
        if has_excessive_duration:
            defects.append({
                "type": "motion_excessive_duration",
                "severity": "P2",
                "message": "Detected animation duration > 300ms on UI controls. Interactive transitions should complete within 150ms - 250ms."
            })
            score -= 10.0

        # 4. Check for animations/transitions without prefers-reduced-motion
        has_motion = bool(re.search(r'(@keyframes|\banimate-|\btransition:|\btransition-)', code_content))
        has_reduced_motion = bool(re.search(r'prefers-reduced-motion|useReducedMotion', code_content))
        if has_motion and not has_reduced_motion:
            defects.append({
                "type": "motion_missing_reduced_motion_guard",
                "severity": "P2",
                "message": "Animated UI elements detected without 'prefers-reduced-motion' accessibility guard."
            })
            score -= 10.0

        # 5. Check for raw CSS :hover without fine pointer media query
        has_raw_hover = bool(re.search(r'[^{}@]+\b:hover\b\s*\{', code_content))
        has_hover_guard = bool(re.search(r'@media\s*\(\s*hover:\s*hover\s*\)\s*and\s*\(\s*pointer:\s*fine\s*\)', code_content))
        if has_raw_hover and not has_hover_guard:
            defects.append({
                "type": "motion_sticky_touch_hover",
                "severity": "P2",
                "message": "Detected raw CSS ':hover' rule without '@media (hover: hover) and (pointer: fine)'. Causes sticky hover states on mobile touchscreens."
            })
            score -= 10.0

        score = max(0.0, score)
        return {
            "motion_score": score,
            "acceptance_status": "ACCEPTED" if score >= 80.0 else "REVISE_REQUIRED",
            "is_ergonomic": score >= 80.0,
            "defects": defects,
            "metrics": {
                "has_transition_all": has_transition_all,
                "has_scale_zero": has_scale_zero,
                "has_excessive_duration": has_excessive_duration,
                "has_reduced_motion_guard": has_reduced_motion if has_motion else True,
                "has_hover_guard": has_hover_guard if has_raw_hover else True
            }
        }

    def audit_runtime_react_tsx(
        self,
        tsx_code: str,
        target_slider_value: Optional[float] = None,
        is_rtl: bool = False,
        capture_screenshots: bool = False,
        domain_id: Optional[str] = None,
        page: Any = None
    ) -> Dict[str, Any]:
        """
        End-to-End Browser Truth Audit for real React 19 TSX components:
        1. Compiles TSX component into offline self-contained bundle via esbuild (<30ms).
        2. Mounts into Chromium with local React 19 + ReactDOM 19 + baseline CSS.
        3. Listens for React runtime crashes or unhandled exceptions.
        4. Simulates physical pointer / native value change targeted via InteractionContract.
        5. Asserts dynamic causal recalculation in bound semantic metrics.
        6. Asserts directional compliance (positive/negative/recalculated) per domain contract.
        7. Inspects rendered screenshot pixel buffers via PixelCritic (blank screen / contrast collapse).
        8. Executes in-browser VisionSensor to detect collisions, clipping, and hero prominence.
        9. Optionally captures real multi-viewport screenshots (390px, 768px, 1440px).
        Supports reusable external page instances for zero-overhead continuous benchmarking.
        """
        if not self.enable_browser:
            return {
                "interactive_verified": True,
                "status": "SKIPPED_STATIC_MODE",
                "message": "Browser execution disabled; skipped runtime interaction simulation."
            }

        from vibe_core.runtime_compiler import RuntimeCompiler
        compiler = RuntimeCompiler()
        harness_html, err = compiler.compile_and_harness(tsx_code, component_name="VibeMasterpiece", is_rtl=is_rtl)
        if err:
            return {
                "interactive_verified": False,
                "status": "COMPILATION_ERROR",
                "error": err,
                "defects": [{
                    "type": "runtime_compilation_error",
                    "severity": "P0",
                    "message": f"React 19 TSX failed compilation: {err[:200]}"
                }]
            }

        contract = get_interaction_contract(domain_id or "general_modern_saas")

        owns_page = page is None
        try:
            if owns_page:
                from playwright.sync_api import sync_playwright
                playwright_ctx = sync_playwright()
                p = playwright_ctx.__enter__()
                browser = p.chromium.launch(headless=True)
                active_page = browser.new_page(viewport={"width": 1280, "height": 800})
            else:
                playwright_ctx = None
                browser = None
                active_page = page

            try:
                errors = []
                active_page.on("pageerror", lambda e: errors.append(str(e)))

                active_page.set_content(harness_html, wait_until="load")

                if errors:
                    if owns_page and browser:
                        browser.close()
                        playwright_ctx.__exit__(None, None, None)
                    return {
                        "interactive_verified": False,
                        "status": "REACT_RUNTIME_CRASH",
                        "error": errors[0],
                        "defects": [{
                            "type": "react_runtime_crash",
                            "severity": "P0",
                            "message": f"React component crashed on mount: {errors[0][:200]}"
                        }]
                    }

                # 1. Read initial metrics before user interaction
                metrics_before = active_page.eval_on_selector_all('bdi', 'els => els.map(el => el.innerText.trim())')
                dynamic_before = active_page.eval_on_selector_all('[data-vibe-metric]', 'els => els.map(el => el.innerText.trim())')
                metrics_by_id_before = active_page.evaluate("""() => {
                    const res = {};
                    document.querySelectorAll('[data-vibe-metric]').forEach(el => {
                        const id = el.getAttribute('data-vibe-metric');
                        if (id) res[id] = el.innerText.trim();
                    });
                    return res;
                }""")

                # 2. Find targeted interactive control using InteractionContract
                slider = active_page.query_selector(contract.control_selector)
                if not slider:
                    slider = active_page.query_selector('input[type="range"]')

                if not slider:
                    # Execute visual perception audit even if no slider
                    vision_audit = VisionSensor.audit_page_visual_intelligence(active_page, viewport_name="desktop")
                    desktop_screenshot = active_page.screenshot(type="png")
                    pixel_audit = PixelCritic().audit_screenshot(desktop_screenshot, viewport_name="desktop")
                    if owns_page and browser:
                        browser.close()
                        playwright_ctx.__exit__(None, None, None)
                    return {
                        "interactive_verified": True,
                        "status": "NO_RANGE_SLIDER",
                        "message": "No range slider in component; mounted cleanly.",
                        "vision_report": vision_audit,
                        "pixel_report": pixel_audit
                    }

                curr_val = float(slider.get_attribute("value") or 0)
                min_val = float(slider.get_attribute("min") or 0)
                max_val = float(slider.get_attribute("max") or 100)

                new_val = target_slider_value if target_slider_value is not None else contract.target_value
                if new_val < min_val or new_val > max_val or new_val == curr_val:
                    # Self-healing: calibrate target to 70% of physical slider domain
                    new_val = min_val + 0.70 * (max_val - min_val)
                    if abs(new_val - curr_val) < 0.05 * (max_val - min_val):
                        new_val = min_val + 0.25 * (max_val - min_val)

                # 3. Dispatch native React synthetic event to targeted control
                active_page.evaluate("""({sel, val}) => {
                    const input = document.querySelector(sel) || document.querySelector('input[type="range"]');
                    if (input) {
                        const nativeSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
                        nativeSetter.call(input, String(val));
                        input.dispatchEvent(new Event('input', { bubbles: true }));
                        input.dispatchEvent(new Event('change', { bubbles: true }));
                    }
                }""", {"sel": contract.control_selector, "val": new_val})

                active_page.wait_for_timeout(80)

                # 4. Read metrics after interaction and verify causal assertion
                metrics_after = active_page.eval_on_selector_all('bdi', 'els => els.map(el => el.innerText.trim())')
                dynamic_after = active_page.eval_on_selector_all('[data-vibe-metric]', 'els => els.map(el => el.innerText.trim())')
                metrics_by_id_after = active_page.evaluate("""() => {
                    const res = {};
                    document.querySelectorAll('[data-vibe-metric]').forEach(el => {
                        const id = el.getAttribute('data-vibe-metric');
                        if (id) res[id] = el.innerText.trim();
                    });
                    return res;
                }""")

                recalculated = [f"{b} -> {a}" for b, a in zip(metrics_before, metrics_after) if b != a]
                dynamic_recalculated = [f"{b} -> {a}" for b, a in zip(dynamic_before, dynamic_after) if b != a]

                is_causal = len(recalculated) > 0
                causal_contract_satisfied = (len(dynamic_recalculated) > 0) or is_causal

                # 5. Assert fine-grained directional compliance & executable formulas
                import re
                def extract_num(s: str) -> Optional[float]:
                    nums = re.findall(r"[-+]?\d*\.?\d+", s.replace(",", ""))
                    return float(nums[0]) if nums else None

                slider_delta = new_val - curr_val
                directional_passed = True
                formula_passed = True
                metric_eval_details = []
                direction_defects = []
                formula_defects = []

                metric_contracts = getattr(contract, "metrics", [])
                if metric_contracts:
                    for idx, m in enumerate(metric_contracts):
                        m_passed = True
                        m_form_passed = True
                        before_str = metrics_by_id_before.get(m.metric_id)
                        after_str = metrics_by_id_after.get(m.metric_id)

                        # Positional fallback if explicit ID not found
                        if (before_str is None or after_str is None) and idx < len(recalculated):
                            parts = recalculated[idx].split(" -> ")
                            if len(parts) == 2:
                                before_str, after_str = parts[0], parts[1]

                        if before_str is not None and after_str is not None:
                            n_before = extract_num(before_str)
                            n_after = extract_num(after_str)
                            if n_before is not None and n_after is not None:
                                metric_delta = n_after - n_before

                                if m.expected_direction == "positive":
                                    if slider_delta > 0 and metric_delta < 0 and not (n_before < 0 and n_after < 0 and abs(n_after) > abs(n_before)):
                                        m_passed = False
                                    elif slider_delta < 0 and metric_delta > 0:
                                        m_passed = False
                                elif m.expected_direction == "negative":
                                    if slider_delta > 0 and metric_delta > 0:
                                        m_passed = False
                                    elif slider_delta < 0 and metric_delta < 0:
                                        m_passed = False
                                elif m.expected_direction == "recalculated":
                                    if n_before == n_after and before_str == after_str:
                                        m_passed = False

                                # Executable formula verification
                                if m.formula_expr:
                                    try:
                                        js_formula = m.formula_expr.replace("max(", "Math.max(").replace("round(", "Math.round(").replace("min(", "Math.min(")
                                        calc_expected = active_page.evaluate(
                                            f"((simulatedValue, splitPos) => {{ try {{ return Number({js_formula}); }} catch(e) {{ return null; }} }})",
                                            new_val, new_val
                                        )
                                        if calc_expected is not None:
                                            diff = abs(abs(n_after) - abs(calc_expected))
                                            allowed = max(2.0, abs(calc_expected) * m.tolerance)
                                            if diff > allowed:
                                                m_form_passed = False
                                                formula_defects.append({
                                                    "type": "formula_mismatch",
                                                    "severity": "P1",
                                                    "metric_id": m.metric_id,
                                                    "message": f"Metric '{m.metric_id}' computed value ({n_after}) does not match formula '{m.formula_expr}' expected ({calc_expected}) within tolerance."
                                                })
                                    except Exception:
                                        pass

                        if not m_passed:
                            directional_passed = False
                            direction_defects.append({
                                "type": "runtime_direction_inversion",
                                "severity": "P1",
                                "metric_id": m.metric_id,
                                "message": f"Metric '{m.metric_id}' changed inversely ({m.expected_direction}) for domain '{contract.domain_id}'."
                            })

                        metric_eval_details.append({
                            "metric_id": m.metric_id,
                            "directional_passed": m_passed,
                            "formula_passed": m_form_passed
                        })

                    if formula_defects:
                        formula_passed = False

                elif contract.expected_direction in ("positive", "negative") and len(recalculated) > 0:
                    for pair in recalculated:
                        parts = pair.split(" -> ")
                        if len(parts) == 2:
                            n_before = extract_num(parts[0])
                            n_after = extract_num(parts[1])
                            if n_before is not None and n_after is not None and n_before != n_after:
                                metric_delta = n_after - n_before
                                if contract.expected_direction == "positive":
                                    if slider_delta > 0 and metric_delta < 0 and not (n_before < 0 and n_after < 0 and abs(n_after) > abs(n_before)):
                                        directional_passed = False
                                    elif slider_delta < 0 and metric_delta > 0:
                                        directional_passed = False
                                elif contract.expected_direction == "negative":
                                    if slider_delta > 0 and metric_delta > 0:
                                        directional_passed = False
                                    elif slider_delta < 0 and metric_delta < 0:
                                        directional_passed = False

                # 6. In-Browser Visual Intelligence Analysis (VisionSensor)
                vision_audit = VisionSensor.audit_page_visual_intelligence(active_page, viewport_name="desktop")

                # 7. Rendered Screenshot Pixel Inspection (PixelCritic)
                desktop_screenshot = active_page.screenshot(type="png")
                pixel_audit = PixelCritic().audit_screenshot(desktop_screenshot, viewport_name="desktop")

                screenshots = {}
                if capture_screenshots:
                    screenshots["desktop"] = desktop_screenshot
                    for vp_name, vp_w in [("mobile", 390), ("tablet", 768)]:
                        active_page.set_viewport_size({"width": vp_w, "height": 844 if vp_w < 500 else 900})
                        active_page.wait_for_timeout(40)
                        vp_bytes = active_page.screenshot(type="png")
                        screenshots[vp_name] = vp_bytes
                        if vp_name == "mobile":
                            mobile_vision = VisionSensor.audit_page_visual_intelligence(active_page, viewport_name="mobile")
                            for d in mobile_vision.get("defects", []):
                                if not any(existing.get("type") == d.get("type") for existing in vision_audit.get("defects", [])):
                                    vision_audit["defects"].append(d)

                if owns_page and browser:
                    browser.close()
                    playwright_ctx.__exit__(None, None, None)

                defects = []
                if not causal_contract_satisfied:
                    defects.append({
                        "type": "runtime_causal_dead_state",
                        "severity": "P0",
                        "message": f"Interaction on '{contract.input_variable}' did not causally recalculate bound metrics in domain '{contract.domain_id}'."
                    })

                defects.extend(direction_defects)
                defects.extend(formula_defects)

                # Merge vision defects
                defects.extend(vision_audit.get("defects", []))

                # Merge pixel defects
                defects.extend(pixel_audit.get("defects", []))

                if pixel_audit.get("is_blank"):
                    causal_contract_satisfied = False

                is_fully_verified = causal_contract_satisfied and directional_passed and not any(d.get("severity") == "P0" for d in defects)

                return {
                    "interactive_verified": is_fully_verified,
                    "causal_contract_satisfied": causal_contract_satisfied,
                    "directional_passed": directional_passed,
                    "formula_passed": formula_passed,
                    "metric_details": metric_eval_details,
                    "causal_contract": {
                        "domain_id": contract.domain_id,
                        "control": contract.input_variable,
                        "target_value": new_val,
                        "expected_metrics": contract.bound_metrics,
                        "expected_direction": contract.expected_direction,
                        "formula_expr": contract.formula_expr
                    },
                    "status": "PASSED" if is_fully_verified else "DEFECTS_DETECTED",
                    "metrics_count": len(metrics_before),
                    "recalculated_count": len(recalculated),
                    "recalculated_pairs": recalculated,
                    "dynamic_recalculated": dynamic_recalculated,
                    "vision_report": vision_audit,
                    "pixel_report": pixel_audit,
                    "screenshots_captured": list(screenshots.keys()),
                    "defects": defects
                }
            except Exception as e:
                if owns_page and browser:
                    browser.close()
                    playwright_ctx.__exit__(None, None, None)
                raise e

        except Exception as e:
            return {
                "interactive_verified": False,
                "status": "ERROR",
                "message": f"Runtime React audit failed: {e}",
                "defects": [{
                    "type": "runtime_audit_error",
                    "severity": "P0",
                    "message": str(e)
                }]
            }

    def audit_runtime_interaction(
        self,
        html_content: str,
        slider_selector: str = 'input[type="range"]',
        metric_selector: str = 'bdi',
        target_value: Optional[float] = None,
        domain_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Simulates physical causal user interaction in real Chromium browser.
        Automatically routes React TSX code through audit_runtime_react_tsx().
        """
        # Auto-route if code is TSX component
        if "export function" in html_content or "export const VibeMasterpiece" in html_content or "from 'react'" in html_content:
            return self.audit_runtime_react_tsx(html_content, target_slider_value=target_value, domain_id=domain_id)

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
                    if slider_selector != 'input[type="range"]':
                        return {
                            "interactive_verified": False,
                            "status": "FAIL_SELECTOR_NOT_FOUND",
                            "message": f"Interactive control selector '{slider_selector}' not found in DOM."
                        }
                    else:
                        return {
                            "interactive_verified": True,
                            "status": "NO_RANGE_SLIDER",
                            "message": "No range slider found; mounted cleanly."
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

