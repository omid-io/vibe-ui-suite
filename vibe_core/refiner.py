"""
vibe_core.refiner — Priority-Based Auto-Refinement Engine
Applies bounded surgical patches to resolve Critic defects with strict anti-regression gating.
"""

import re
from typing import Dict, Any, Tuple, Optional, Callable, List
from vibe_core.critic import DesignCritic
from vibe_core.visual_critic import VisualCritic

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
    def __init__(self):
        self.critic = DesignCritic()
        self.visual_critic = VisualCritic()

    replace_clickable_divs = staticmethod(replace_clickable_divs)

    @staticmethod
    def should_accept_patch(
        current_report: Dict[str, Any],
        re_critique: Dict[str, Any],
        patched_html: str,
        current_visual: Optional[Dict[str, Any]] = None,
        patched_visual: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Enforces 7-Rule Invariant Gate (DOM + Visual Critics):
        1. Gate Monotonicity (No introduced failures): len(new_failures - curr_failures) == 0
        2. Gate Monotonicity (Failure count non-increasing): len(new_failures) <= len(curr_failures)
        3. Tag Balance Invariant: Assert balanced <button>...</button> pairs
        4. Mobile Overflow Invariant: Reject fixed-width blowout classes (>= 400px)
        5. Score Progression: Only accept if quality_score is maintained or improved
        6. Visual Monotonicity: No new P0 visual defects introduced
        7. Visual Quality Non-Regression: Visual composite score maintained (within 2.0 tolerance)
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
        Strictly enforces atomic composite acceptance (DOM Critic + Visual Critic).
        """
        decision = decision or {}
        current_html = html_content
        current_report = self.critic.critique(current_html, decision, iteration=1)
        current_visual = self.visual_critic.evaluate(current_html, decision)
        current_report["visual_critic"] = current_visual

        dom_accepted = (current_report.get("acceptance_status") == "ACCEPTED")
        vis_accepted = (current_visual.get("acceptance_status") == "ACCEPTED")
        current_report["acceptance_status"] = "ACCEPTED" if (dom_accepted and vis_accepted) else "REVISE_REQUIRED"

        if dom_accepted and vis_accepted:
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
            defects = current_report.get("defects_ranked", []) + visual_defects
            if not defects:
                break

            # Sort defects: critical -> high -> medium -> low
            priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
            sorted_defects = sorted(defects, key=lambda d: priority_order.get(d.get("severity", "low"), 4))

            # Apply surgical patches
            if patch_fn is not None:
                patched_html = patch_fn(current_html, sorted_defects)
            else:
                patched_html = current_html
                for defect in sorted_defects:
                    d_type = defect.get("type")

                    # 1. Missing viewport patch
                    if d_type == "missing_viewport":
                        if "<head>" in patched_html:
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

                    # 4. Raw emoji replacement
                    elif d_type in ["raw_emoji_detected", "cliche_ai_sparkle"]:
                        # Replace common emojis and sparkles with SVG vector
                        svg_star = '<svg class="w-4 h-4 inline" viewBox="0 0 24 24" fill="currentColor"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>'
                        patched_html = re.sub(
                            r"[\U00010000-\U0010ffff]|[\u2600-\u27bf]|[\u2300-\u23ff]|[\u2b50-\u2b55]|[\u203c-\u2049]|✨",
                            svg_star,
                            patched_html
                        )

                    # 5. Missing bidi isolation
                    elif d_type == "missing_bidi_isolation":
                        if "</style>" in patched_html:
                            patched_html = patched_html.replace(
                                "</style>",
                                "  body { unicode-bidi: plaintext; }\n    bdi { direction: ltr !important; unicode-bidi: isolate; }\n  </style>"
                            )

                    # 6. Generic purple gradient replacement
                    elif d_type == "generic_ai_purple_gradient":
                        patched_html = patched_html.replace("from-purple-600 to-indigo-600", "bg-[var(--surface-bg)] border border-[var(--border-subtle)]")

                    # 7. Substandard touch target repair (ensure >= 44px)
                    elif d_type == "substandard_touch_target":
                        patched_html = re.sub(r'\b(h-6|h-7|h-8|py-1|py-2)\b', 'min-h-[44px] py-3', patched_html)

                    # 8. Excessive compositing blur
                    elif d_type == "excessive_compositing_blur":
                        patched_html = re.sub(r'backdrop-blur-(?:2xl|3xl)', 'backdrop-blur-md', patched_html)

            # Re-Evaluation
            re_critique = self.critic.critique(patched_html, decision, iteration=iteration + 1)
            re_visual = self.visual_critic.evaluate(patched_html, decision)

            # Strict 7-Rule Composite Invariant Gate Check
            accept_patch = self.should_accept_patch(
                current_report,
                re_critique,
                patched_html,
                current_visual=current_visual,
                patched_visual=re_visual
            )

            if accept_patch:
                current_html = patched_html
                current_report = re_critique
                current_visual = re_visual
                dom_ok = (current_report.get("acceptance_status") == "ACCEPTED")
                vis_ok = (current_visual.get("acceptance_status") == "ACCEPTED")
                current_report["acceptance_status"] = "ACCEPTED" if (dom_ok and vis_ok) else "REVISE_REQUIRED"
                current_report["visual_critic"] = current_visual
                if dom_ok and vis_ok:
                    break
            else:
                # Explicit rejection: discard patch, keep current_html
                pass

        current_report["visual_critic"] = current_visual
        dom_ok = (current_report.get("acceptance_status") == "ACCEPTED")
        vis_ok = (current_visual.get("acceptance_status") == "ACCEPTED")
        current_report["acceptance_status"] = "ACCEPTED" if (dom_ok and vis_ok) else "REVISE_REQUIRED"
        return current_html, current_report
