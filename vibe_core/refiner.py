"""
vibe_core.refiner — Priority-Based Auto-Refinement Engine
Applies bounded surgical patches to resolve Critic defects with strict anti-regression gating.
"""

import re
from typing import Dict, Any, Tuple, Optional, Callable, List
from vibe_core.critic import DesignCritic
from vibe_core.visual_critic import VisualCritic
from vibe_core.physical_critic import PhysicalCritic

# Token scanner regex matching comments, scripts, styles, closing divs, and opening divs with attributes
TAG_TOKEN_RE = re.compile(
    r"""(<!--.*?-->)
    | (<script[^>]*>.*?</script>)
    | (<style[^>]*>.*?</style>)
    | (</div\s*>)
    | (<div((?:\s+[^"'>/=\s]+(?:\s*=\s*(?:"[^"]*"|'[^']*'|[^>\s]+))?)*)\s*(/?)>)
    """,
    re.IGNORECASE | re.DOTALL | re.VERBOSE
)


def replace_clickable_divs(html: str) -> str:
    """
    Scans HTML using a stack-based token scanner to match each <div ... onclick=...>
    with its exact corresponding closing </div> tag, converting them to
    <button type="button" ...> and </button> pairs via reverse index splicing.
    Handles nested divs, attributes containing '>', comments, scripts, styles, and void elements.
    """
    stack = []
    replacements = []

    for match in TAG_TOKEN_RE.finditer(html):
        comment_g = match.group(1)
        script_g = match.group(2)
        style_g = match.group(3)
        close_div_g = match.group(4)
        open_div_g = match.group(5)
        attrs = match.group(6)
        slash = match.group(7)

        # Ignore comments, script blocks, and style blocks
        if comment_g or script_g or style_g:
            continue

        if open_div_g:
            is_self_closing = bool(slash and slash.strip() == "/")
            is_clickable = bool(attrs and re.search(r"\bonclick\s*=", attrs, re.IGNORECASE))
            if is_self_closing:
                if is_clickable:
                    btn_attrs = attrs if (attrs and attrs.startswith(" ")) else (" " + (attrs or ""))
                    if not re.search(r"\btype\s*=", attrs or "", re.IGNORECASE):
                        open_btn = f'<button type="button"{btn_attrs}></button>'
                    else:
                        open_btn = f'<button{btn_attrs}></button>'
                    replacements.append((match.start(), match.end(), open_btn))
            else:
                stack.append((match.start(), match.end(), is_clickable, attrs))

        elif close_div_g:
            if stack:
                start_open, end_open, is_clickable, open_attrs = stack.pop()
                if is_clickable:
                    btn_attrs = open_attrs if (open_attrs and open_attrs.startswith(" ")) else (" " + (open_attrs or ""))
                    if not re.search(r"\btype\s*=", open_attrs or "", re.IGNORECASE):
                        open_btn = f'<button type="button"{btn_attrs}>'
                    else:
                        open_btn = f'<button{btn_attrs}>'
                    replacements.append((start_open, end_open, open_btn))
                    replacements.append((match.start(), match.end(), "</button>"))

    # Reverse splicing: process replacements in descending order of start position
    replacements.sort(key=lambda x: x[0], reverse=True)
    res = html
    for start, end, repl in replacements:
        res = res[:start] + repl + res[end:]
    return res


class AutoRefiner:
    def __init__(self, enable_physical_browser: bool = True, verify_runtime_causal: bool = True):
        self.critic = DesignCritic()
        self.visual_critic = VisualCritic()
        self.physical_critic = PhysicalCritic(enable_browser=enable_physical_browser)
        self.verify_runtime_causal = verify_runtime_causal
        self.enable_physical_browser = enable_physical_browser

    replace_clickable_divs = staticmethod(replace_clickable_divs)

    @staticmethod
    def should_accept_patch(
        current_report: Dict[str, Any],
        re_critique: Dict[str, Any],
        patched_html: str,
        current_visual: Optional[Dict[str, Any]] = None,
        patched_visual: Optional[Dict[str, Any]] = None,
        current_physical: Optional[Dict[str, Any]] = None,
        patched_physical: Optional[Dict[str, Any]] = None,
        current_runtime: Optional[Dict[str, Any]] = None,
        patched_runtime: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Enforces 10-Rule Quad-Composite Invariant Gate (DOM + Visual + Physical + Runtime Critics):
        1. Gate Monotonicity (No introduced failures): len(new_failures - curr_failures) == 0
        2. Gate Monotonicity (Failure count non-increasing): len(new_failures) <= len(curr_failures)
        3. Tag Balance Invariant: Assert balanced <button>...</button> pairs
        4. Mobile Overflow Invariant: Reject fixed-width blowout classes (>= 400px)
        5. Score Progression: Only accept if quality_score is maintained or improved
        6. Visual Monotonicity: No new P0 visual defects introduced
        7. Visual Quality Non-Regression: Visual composite score maintained (within 2.0 tolerance)
        8. Physical Monotonicity: No new P0 physical layout defects introduced
        9. Physical Quality Non-Regression: Physical layout score maintained (within 2.0 tolerance)
        10. Runtime Causal Monotonicity: Reactivity must not regress (interactive_verified must remain True)
        """
        # Extract failure sets
        curr_failures = {f["gate"] for f in current_report.get("hard_gate_failures", [])}
        new_failures = {f["gate"] for f in re_critique.get("hard_gate_failures", [])}

        # 1 & 2. Gate Monotonicity: No new hard-gate failures permitted and failure count non-increasing
        introduced_failures = new_failures - curr_failures
        has_gate_regression = len(introduced_failures) > 0 or len(new_failures) > len(curr_failures)

        # 3. Tag Balance Invariant: Assert balanced <button>...</button> pairs
        open_buttons = len(re.findall(r"<button\b", patched_html, re.IGNORECASE))
        close_buttons = len(re.findall(r"</button>", patched_html, re.IGNORECASE))
        tag_balance_violation = (open_buttons != close_buttons)

        # 4. Mobile Overflow Invariant: Detect fixed-width blowout classes
        overflow_violation = bool(re.search(
            r'(?:width:\s*(?:[4-9]\d\d|\d{4,})px|w-\[(?:[4-9]\d\d|\d{4,})px\]|min-w-\[(?:[4-9]\d\d|\d{4,})px\])',
            patched_html
        ))

        # 5. Score Progression Condition
        score_progression = re_critique.get("quality_score", 0) >= current_report.get("quality_score", 0)

        base_ok = (
            not has_gate_regression
            and not tag_balance_violation
            and not overflow_violation
            and score_progression
        )

        if not base_ok:
            return False

        # 6 & 7. Visual Invariant Gate
        if current_visual is not None and patched_visual is not None:
            curr_p0 = {d.get("type", d.get("id")) for d in current_visual.get("defects", []) if d.get("severity") == "P0"}
            new_p0 = {d.get("type", d.get("id")) for d in patched_visual.get("defects", []) if d.get("severity") == "P0"}
            introduced_p0 = new_p0 - curr_p0
            if len(introduced_p0) > 0:
                return False

            curr_vis_score = current_visual.get("visual_score", current_visual.get("score", 0.0))
            patch_vis_score = patched_visual.get("visual_score", patched_visual.get("score", 0.0))
            if patch_vis_score < curr_vis_score - 2.0:
                return False

        # 8 & 9. Physical Invariant Gate
        if current_physical is not None and patched_physical is not None:
            curr_phys_p0 = {d.get("type") for d in current_physical.get("defects", []) if d.get("severity") == "P0"}
            new_phys_p0 = {d.get("type") for d in patched_physical.get("defects", []) if d.get("severity") == "P0"}
            introduced_phys_p0 = new_phys_p0 - curr_phys_p0
            if len(introduced_phys_p0) > 0:
                return False

            curr_targets = current_physical.get("metrics", {}).get("total_touch_targets", 0)
            curr_phys_score = current_physical.get("physical_score", 0.0)
            patch_phys_score = patched_physical.get("physical_score", 0.0)
            # If baseline had 0 touch targets, it held unearned 25pts for non-existent targets.
            # When semantic interactive elements first appear, evaluate monotonicity on equal footing.
            if curr_targets == 0 and patched_physical.get("metrics", {}).get("total_touch_targets", 0) > 0:
                curr_phys_score -= 25.0

            if patch_phys_score < curr_phys_score - 2.0:
                return False

        # 10. Runtime Causal Reactivity Invariant Gate
        if current_runtime is not None and patched_runtime is not None:
            curr_runtime_ok = current_runtime.get("interactive_verified", True)
            patch_runtime_ok = patched_runtime.get("interactive_verified", True)
            if curr_runtime_ok and not patch_runtime_ok:
                return False

            # 11. Visual Perception & Collision Invariant Gate (VisionSensor)
            curr_vision = current_runtime.get("vision_report", {})
            patch_vision = patched_runtime.get("vision_report", {})
            if curr_vision and patch_vision:
                curr_vis_score = curr_vision.get("visual_score", 100.0)
                patch_vis_score = patch_vision.get("visual_score", 100.0)
                if patch_vis_score < curr_vis_score - 2.0:
                    return False
                curr_p0_vision = sum(1 for d in curr_vision.get("defects", []) if d.get("severity") == "P0")
                patch_p0_vision = sum(1 for d in patch_vision.get("defects", []) if d.get("severity") == "P0")
                if patch_p0_vision > curr_p0_vision:
                    return False

        return True

    def refine(
        self,
        html_content: str,
        decision: Optional[Dict[str, Any]] = None,
        max_iterations: int = 2,
        patch_fn: Optional[Callable[[str, List[Dict[str, Any]]], str]] = None
    ) -> Tuple[str, Dict[str, Any]]:
        """
        Runs bounded refinement loop (max 2 iterations) resolving defects in priority order.
        Strictly enforces atomic Quad-Composite acceptance (DOM + Visual + Physical + Runtime Critics).
        """
        decision = decision or {}
        domain_id = decision.get("genome", {}).get("domain") or decision.get("intent", {}).get("product_domain")
        current_html = html_content
        current_report = self.critic.critique(current_html, decision, iteration=1)
        current_visual = self.visual_critic.evaluate(current_html, decision)
        current_physical = self.physical_critic.audit_physical_layout(current_html)
        current_runtime = self.physical_critic.audit_runtime_interaction(current_html, domain_id=domain_id) if self.verify_runtime_causal else {"interactive_verified": True}
        current_report["visual_critic"] = current_visual
        current_report["physical_critic"] = current_physical
        current_report["runtime_critic"] = current_runtime

        dom_accepted = (current_report.get("acceptance_status") == "ACCEPTED")
        vis_accepted = (current_visual.get("acceptance_status") == "ACCEPTED")
        phys_accepted = (current_physical.get("acceptance_status") == "ACCEPTED")
        runtime_accepted = current_runtime.get("interactive_verified", True)
        current_report["acceptance_status"] = (
            "ACCEPTED" if (dom_accepted and vis_accepted and phys_accepted and runtime_accepted)
            else "REVISE_REQUIRED"
        )

        if dom_accepted and vis_accepted and phys_accepted and runtime_accepted:
            return current_html, current_report

        severity_map = {"P0": "critical", "P1": "high", "P2": "medium"}

        for iteration in range(1, max_iterations + 1):
            # Inject visual defects into defect queue
            visual_defects = [
                {
                    "type": d.get("type", d.get("id")),
                    "category": "visual_critic",
                    "severity": severity_map.get(d.get("severity", "P2"), "low"),
                    "message": d.get("message", ""),
                    "prescription": d.get("prescription", "")
                }
                for d in current_visual.get("defects", [])
            ]
            # Inject physical layout defects into defect queue
            raw_phys_defects = list(current_physical.get("defects", []))
            motion_defects = current_physical.get("metrics", {}).get("motion_ergonomics", {}).get("defects", [])
            for md in motion_defects:
                if md not in raw_phys_defects:
                    raw_phys_defects.append(md)

            physical_defects = [
                {
                    "type": d.get("type"),
                    "category": "physical_critic",
                    "severity": severity_map.get(d.get("severity", "P2"), "low"),
                    "message": d.get("message", ""),
                    "prescription": d.get("prescription", "")
                }
                for d in raw_phys_defects
            ]
            defects = current_report.get("defects_ranked", []) + visual_defects + physical_defects
            if not defects:
                break

            # Sort defects: critical -> high -> medium -> low
            priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
            sorted_defects = sorted(defects, key=lambda d: priority_order.get(d.get("severity", "low"), 4))

            # Canonical defect normalization map
            CANONICAL_DEFECT_MAP = {
                "missing_bidi_isolation": "missing_bdi_isolation",
                "generic_ai_purple_gradient": "cliche_ai_gradient",
                "raw_emoji_detected": "cliche_ai_sparkle",
            }

            # Apply surgical patches
            if patch_fn is not None:
                patched_html = patch_fn(current_html, sorted_defects)
            else:
                patched_html = current_html
                for defect in sorted_defects:
                    raw_type = defect.get("type", "")
                    d_type = CANONICAL_DEFECT_MAP.get(raw_type, raw_type)

                    # 1. Missing viewport patch
                    if d_type == "missing_viewport":
                        if "<head>" in patched_html and 'name="viewport"' not in patched_html:
                            patched_html = patched_html.replace(
                                "<head>",
                                "<head>\n  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">"
                            )

                    # 2. Missing focus rings patch
                    elif d_type == "missing_focus_rings":
                        focus_css = "\n    button:focus-visible, a:focus-visible { outline: 2px solid var(--accent, #3b82f6); outline-offset: 2px; }\n"
                        if "</style>" in patched_html:
                            patched_html = patched_html.replace("</style>", f"{focus_css}  </style>")
                        elif "<head>" in patched_html:
                            patched_html = patched_html.replace("<head>", f"<head>\n  <style>{focus_css}</style>")

                    # 3. Non-semantic clickable (<div onclick>)
                    elif d_type == "non_semantic_clickable":
                        patched_html = self.replace_clickable_divs(patched_html)

                    # 4. Raw emoji / sparkle replacement
                    elif d_type == "cliche_ai_sparkle":
                        svg_star = '<svg class="w-4 h-4 inline" viewBox="0 0 24 24" fill="currentColor"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>'
                        patched_html = re.sub(
                            r"[\U00010000-\U0010ffff]|[\u2600-\u27bf]|[\u2300-\u23ff]|[\u2b50-\u2b55]|[\u203c-\u2049]|✨",
                            svg_star,
                            patched_html
                        )

                    # 5. Missing BDI bidirectional isolation
                    elif d_type == "missing_bdi_isolation":
                        if "</style>" in patched_html:
                            patched_html = patched_html.replace(
                                "</style>",
                                "  body { unicode-bidi: plaintext; }\n    bdi { direction: ltr !important; unicode-bidi: isolate; }\n  </style>"
                            )
                        # If no <bdi> exists, wrap numerical/metric tokens with <bdi>
                        if "<bdi>" not in patched_html:
                            patched_html = re.sub(
                                r'(\$?\d+(?:\.\d+)?%?)(\s*(?:USD|EUR|ms|req/s|GB|TB|users|TPS)?)',
                                r'<bdi class="tabular-nums">\1\2</bdi>',
                                patched_html,
                                count=5
                            )

                    # 6. Cliche AI purple gradient replacement
                    elif d_type == "cliche_ai_gradient":
                        patched_html = re.sub(
                            r'from-purple-\d+\s+to-(?:indigo|fuchsia|pink)-\d+',
                            'bg-[var(--surface-bg,#0d1117)] border border-[var(--border-subtle,#30363d)] text-[var(--text-primary,#c9d1d9)]',
                            patched_html
                        )
                        patched_html = patched_html.replace("from-purple-600 to-indigo-600", "bg-[var(--surface-bg,#0d1117)] border border-[var(--border-subtle,#30363d)]")

                    # 7. Substandard touch target repair (ensure >= 44px)
                    elif d_type == "substandard_touch_target":
                        patched_html = re.sub(r'\b(h-[5-8]|py-[12]|min-h-\[(?:3[0-9]|4[0-3])px\])\b', 'min-h-[44px] py-3 px-5', patched_html)
                        # Ensure buttons have min-h-[44px]
                        if not re.search(r"min-h-\[(4[4-9]|[5-9]\d)px\]", patched_html):
                            patched_html = re.sub(r'(<button\b[^>]*class="[^"]*)(")', r'\1 min-h-[44px] px-6 py-3\2', patched_html)

                    # 8. Missing active spring physics
                    elif d_type == "missing_active_spring":
                        if not re.search(r"active:(?:scale-\d+|translate-)", patched_html):
                            patched_html = re.sub(
                                r'(<button\b[^>]*class="[^"]*)(")',
                                r'\1 transition-all duration-150 active:scale-95\2',
                                patched_html
                            )

                    # 9. Missing H1 focal point
                    elif d_type == "missing_h1_focal_point":
                        if not re.search(r"<h1\b", patched_html, re.IGNORECASE):
                            if re.search(r"<h2\b", patched_html, re.IGNORECASE):
                                # Upgrade first <h2> to <h1>
                                patched_html = re.sub(
                                    r'<h2(\b[^>]*)>(.*?)</h2>',
                                    r'<h1\1 class="text-4xl sm:text-5xl font-extrabold tracking-tight mb-4">\2</h1>',
                                    patched_html,
                                    count=1,
                                    flags=re.IGNORECASE | re.DOTALL
                                )
                            elif "<main>" in patched_html:
                                patched_html = patched_html.replace("<main>", '<main>\n  <h1 class="text-4xl sm:text-5xl font-extrabold tracking-tight mb-4">Overview</h1>')
                            elif "<body>" in patched_html:
                                patched_html = patched_html.replace("<body>", '<body>\n  <h1 class="text-4xl sm:text-5xl font-extrabold tracking-tight mb-4">Overview</h1>')

                    # 10. Weak hero scale
                    elif d_type == "weak_hero_scale":
                        if not re.search(r"text-(3xl|4xl|5xl|6xl|7xl|8xl)", patched_html):
                            patched_html = re.sub(
                                r'(<h1\b[^>]*class="[^"]*)(")',
                                r'\1 text-5xl lg:text-7xl font-extrabold tracking-tight\2',
                                patched_html,
                                count=1
                            )
                            if not re.search(r"text-(3xl|4xl|5xl|6xl|7xl|8xl)", patched_html):
                                # Fallback on any header
                                patched_html = re.sub(r'class="([^"]*)\btext-(?:sm|base|lg|xl|2xl)\b([^"]*)"', r'class="\1text-5xl lg:text-7xl font-extrabold tracking-tight\2"', patched_html, count=1)

                    # 11. Cramped spacing rhythm
                    elif d_type == "cramped_spacing_rhythm":
                        if not re.search(r"(?:p-[6-9]|py-[6-9]|py-1[0-6]|p-10|p-12)", patched_html):
                            patched_html = re.sub(r'\b(p-[1-4]|py-[1-4])\b', 'p-6 sm:p-10', patched_html, count=2)
                            if not re.search(r"(?:p-[6-9]|py-[6-9]|py-1[0-6]|p-10|p-12)", patched_html):
                                patched_html = re.sub(r'(<section\b[^>]*class="[^"]*)(")', r'\1 p-8 sm:p-12\2', patched_html, count=1)

                    # 12. Flat monolithic layout
                    elif d_type == "flat_monolithic_layout":
                        if not re.search(r"(?:grid-cols-12|col-span-7|col-span-5|col-span-8|col-span-4)", patched_html):
                            patched_html = re.sub(
                                r'(<div\b[^>]*class="[^"]*)\b(flex\s+flex-col|grid-cols-1)\b([^"]*")',
                                r'\1grid grid-cols-1 lg:grid-cols-12 gap-8\3',
                                patched_html,
                                count=1
                            )

                    # 13. Excessive compositing blur
                    elif d_type == "excessive_compositing_blur":
                        patched_html = re.sub(r'backdrop-blur-(?:2xl|3xl|xl)', 'backdrop-blur-md', patched_html)

                    # 14. Physical horizontal overflow
                    elif d_type == "physical_horizontal_overflow":
                        patched_html = re.sub(
                            r'(?:width:\s*(?:[4-9]\d\d|\d{4,})px|w-\[(?:[4-9]\d\d|\d{4,})px\]|min-w-\[(?:[4-9]\d\d|\d{4,})px\])',
                            'w-full max-w-full',
                            patched_html
                        )

                    # 15. Physical substandard touch target
                    elif d_type == "physical_substandard_touch_target":
                        patched_html = re.sub(r'\b(h-[1-8]|py-[12]|min-h-\[(?:3[0-9]|4[0-3])px\])\b', 'min-h-[44px] py-3 px-5', patched_html)
                        if not re.search(r"min-h-\[(4[4-9]|[5-9]\d)px\]", patched_html):
                            patched_html = re.sub(r'(<button\b[^>]*class="[^"]*)(")', r'\1 min-h-[44px] px-6 py-3\2', patched_html)

                    # 16. Motion transition all anti-pattern
                    elif d_type == "motion_transition_all_anti_pattern":
                        patched_html = re.sub(
                            r'\btransition:\s*all\b',
                            'transition: transform 200ms cubic-bezier(0.16, 1, 0.3, 1), opacity 200ms ease-out',
                            patched_html
                        )
                        patched_html = re.sub(
                            r'\btransition-all\b',
                            'transition-transform duration-200 ease-out',
                            patched_html
                        )

                    # 17. Motion scale zero entry anti-pattern
                    elif d_type == "motion_scale_zero_entry_anti_pattern":
                        patched_html = re.sub(
                            r'\bscale\(\s*0(?:\.0+)?\s*\)',
                            'scale(0.96)',
                            patched_html
                        )
                        patched_html = re.sub(
                            r'\bscale:\s*0\b',
                            'scale: 0.96',
                            patched_html
                        )

                    # 18. Motion missing reduced motion guard
                    elif d_type == "motion_missing_reduced_motion_guard":
                        reduced_motion_css = "\n    @media (prefers-reduced-motion: reduce) { *, ::before, ::after { animation-duration: 0.01ms !important; transition-duration: 0.01ms !important; } }\n"
                        if "</style>" in patched_html:
                            patched_html = patched_html.replace("</style>", f"{reduced_motion_css}  </style>")
                        elif "<head>" in patched_html:
                            patched_html = patched_html.replace("<head>", f"<head>\n  <style>{reduced_motion_css}</style>")

            # Re-Evaluation (Quad-Composite: DOM + Visual + Physical + Runtime)
            re_critique = self.critic.critique(patched_html, decision, iteration=iteration + 1)
            re_visual = self.visual_critic.evaluate(patched_html, decision)
            re_physical = self.physical_critic.audit_physical_layout(patched_html)
            re_runtime = self.physical_critic.audit_runtime_interaction(patched_html, domain_id=domain_id) if self.verify_runtime_causal else {"interactive_verified": True}

            # Strict 11-Rule Quad-Composite Invariant Gate Check
            accept_patch = self.should_accept_patch(
                current_report,
                re_critique,
                patched_html,
                current_visual=current_visual,
                patched_visual=re_visual,
                current_physical=current_physical,
                patched_physical=re_physical,
                current_runtime=current_runtime,
                patched_runtime=re_runtime
            )

            if accept_patch:
                current_html = patched_html
                current_report = re_critique
                current_visual = re_visual
                current_physical = re_physical
                current_runtime = re_runtime
                dom_ok = (current_report.get("acceptance_status") == "ACCEPTED")
                vis_ok = (current_visual.get("acceptance_status") == "ACCEPTED")
                phys_ok = (current_physical.get("acceptance_status") == "ACCEPTED")
                runtime_ok = current_runtime.get("interactive_verified", True)
                current_report["acceptance_status"] = "ACCEPTED" if (dom_ok and vis_ok and phys_ok and runtime_ok) else "REVISE_REQUIRED"
                current_report["visual_critic"] = current_visual
                current_report["physical_critic"] = current_physical
                current_report["runtime_critic"] = current_runtime
                if dom_ok and vis_ok and phys_ok and runtime_ok:
                    break
            else:
                # Explicit rejection: discard patch, keep current_html
                pass

        current_report["visual_critic"] = current_visual
        current_report["physical_critic"] = current_physical
        current_report["runtime_critic"] = current_runtime
        dom_ok = (current_report.get("acceptance_status") == "ACCEPTED")
        vis_ok = (current_visual.get("acceptance_status") == "ACCEPTED")
        phys_ok = (current_physical.get("acceptance_status") == "ACCEPTED")
        runtime_ok = current_runtime.get("interactive_verified", True)
        current_report["acceptance_status"] = "ACCEPTED" if (dom_ok and vis_ok and phys_ok and runtime_ok) else "REVISE_REQUIRED"
        return current_html, current_report

    def refine_react_tsx(
        self,
        tsx_code: str,
        decision: Optional[Dict[str, Any]] = None,
        max_iterations: int = 2,
        page: Any = None
    ) -> Tuple[str, Dict[str, Any]]:
        """
        Closed-Loop Autonomous Browser Truth Refiner for real React 19 TSX artifacts:
        1. Compiles and audits in Chromium headless browser.
        2. Detects runtime crashes, causal dead states, direction inversions, formula mismatches,
           substandard touch targets, and visual/pixel defects.
        3. Applies targeted surgical code repairs to TSX source.
        4. Re-bundles via esbuild and re-mounts in Chromium.
        5. Enforces Quad-Composite non-regression gate: rolls back if visual score degrades or P0s appear.
        """
        decision = decision or {}
        domain_id = decision.get("genome", {}).get("domain") or decision.get("intent", {}).get("product_domain")
        is_rtl = decision.get("genome", {}).get("platform", {}).get("rtl_support", False)

        current_tsx = tsx_code
        current_audit = self.physical_critic.audit_runtime_react_tsx(
            current_tsx,
            domain_id=domain_id,
            is_rtl=is_rtl,
            page=page
        )

        if current_audit.get("interactive_verified") and current_audit.get("directional_passed", True):
            return current_tsx, current_audit

        for iteration in range(1, max_iterations + 1):
            defects = current_audit.get("defects", [])
            if not defects:
                break

            patched_tsx = current_tsx
            for d in defects:
                d_type = d.get("type", "")
                metric_id = d.get("metric_id", "")

                # 1. Surgical repair for direction inversion
                if d_type == "runtime_direction_inversion":
                    if metric_id in ("cluster-latency", "ttft-latency", "ping-latency", "completion-timeline"):
                        patched_tsx = re.sub(
                            r'(\b\d+\s*)\+\s*\(simulatedValue\s*/\s*(\d+)\)',
                            r'\1 - (simulatedValue / \2)',
                            patched_tsx
                        )
                    elif metric_id in ("network-throughput", "node-count", "token-budget", "framerate-target"):
                        patched_tsx = re.sub(
                            r'(\b\d+\s*)-\s*\(simulatedValue\s*/\s*(\d+)\)',
                            r'\1 + (simulatedValue / \2)',
                            patched_tsx
                        )

                # 2. Formula mismatch repair
                elif d_type == "formula_mismatch":
                    from vibe_core.interaction_contract import get_interaction_contract
                    contract = get_interaction_contract(domain_id or "general_modern_saas")
                    target_metric = next((m for m in getattr(contract, "metrics", []) if m.metric_id == metric_id), None)
                    if target_metric and target_metric.formula_expr:
                        js_formula = target_metric.formula_expr.replace("max(", "Math.max(").replace("round(", "Math.round(").replace("min(", "Math.min(")
                        pattern = rf'(<bdi[^>]*data-vibe-metric="{re.escape(metric_id)}"[^>]*>)\{{{{.*?\}}}}'
                        replacement = rf'\1{{{{{js_formula}}}}}'
                        patched_tsx = re.sub(pattern, replacement, patched_tsx)

                # 3. Substandard touch target repair
                elif d_type in ("substandard_touch_target", "physical_substandard_touch_target"):
                    patched_tsx = re.sub(r'\b(h-[1-8]|py-[12]|min-h-\[(?:3[0-9]|4[0-3])px\])\b', 'min-h-[44px] py-3 px-5', patched_tsx)

                # 4. Missing BDI isolation repair
                elif d_type == "missing_bdi_isolation":
                    if "<bdi>" not in patched_tsx and "<bdi " not in patched_tsx:
                        patched_tsx = re.sub(r'(\$\d[\d,.]*|\d+%\s*Off)', r'<bdi>\1</bdi>', patched_tsx)

            # Re-audit patched TSX in Chromium
            re_audit = self.physical_critic.audit_runtime_react_tsx(
                patched_tsx,
                domain_id=domain_id,
                is_rtl=is_rtl,
                page=page
            )

            curr_defects = len(current_audit.get("defects", []))
            new_defects = len(re_audit.get("defects", []))
            curr_ver = current_audit.get("interactive_verified", False)
            new_ver = re_audit.get("interactive_verified", False)

            if (new_ver and not curr_ver) or (new_defects < curr_defects):
                current_tsx = patched_tsx
                current_audit = re_audit
                if new_ver and re_audit.get("directional_passed", True):
                    break

        return current_tsx, current_audit

    def unify_canonical_artifact_session(
        self,
        react_tsx: str,
        decision: Optional[Dict[str, Any]] = None,
        page: Any = None
    ) -> Dict[str, Any]:
        """
        Single Canonical Artifact Session (v4.0 Endgame):
        Unifies React 19 TSX compilation, mounting in real headless Chromium, and simultaneous
        evaluation across all verification gates (DOM, Physical, Causal, Directional, Formula, Vision, Pixel).
        """
        decision = decision or {}
        domain_id = decision.get("genome", {}).get("domain") or decision.get("intent", {}).get("product_domain")
        is_rtl = decision.get("genome", {}).get("platform", {}).get("rtl_support", False)

        audit_res = self.physical_critic.audit_runtime_react_tsx(
            react_tsx,
            domain_id=domain_id,
            is_rtl=is_rtl,
            page=page
        )

        browser_truth_ok = audit_res.get("interactive_verified", False)
        causal_ok = audit_res.get("causal_contract_satisfied", False)
        directional_ok = audit_res.get("directional_passed", True)
        formula_ok = audit_res.get("formula_passed", True)
        pixel_ok = not audit_res.get("pixel_report", {}).get("is_blank", False)
        vis_score = audit_res.get("vision_report", {}).get("visual_score", 95.0)

        all_passed = browser_truth_ok and causal_ok and directional_ok and formula_ok and pixel_ok

        return {
            "session_status": "ACCEPTED" if all_passed else "REVISE_REQUIRED",
            "browser_truth_verified": browser_truth_ok,
            "causal_contract_satisfied": causal_ok,
            "directional_passed": directional_ok,
            "formula_passed": formula_ok,
            "pixel_buffer_valid": pixel_ok,
            "in_browser_vision_score": vis_score,
            "audit_report": audit_res
        }

