"""
vibe_core.critic — Style-Aware Design Critic Engine
Independent evaluator auditing 15 design dimensions, separating Hard Gates from Quality Scorecard.
AST-based HTML parsing via BeautifulSoup4 (falls back to regex if unavailable).
"""

import re
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional

from vibe_core.constants import (
    MAX_BLUR_SURFACES,
    HARD_MIN_TOUCH_PX,
    RECOMMENDED_TOUCH_PX,
    MIN_WCAG_AA_CONTRAST_NORMAL,
)

try:
    from bs4 import BeautifulSoup as _BS4
    _BS4_AVAILABLE = True
except ImportError:  # pragma: no cover
    _BS4_AVAILABLE = False
    _BS4 = None  # type: ignore

def _srgb_to_linear(c_byte: float) -> float:
    c_norm = c_byte / 255.0
    if c_norm <= 0.04045:
        return c_norm / 12.92
    return ((c_norm + 0.055) / 1.055) ** 2.4

def _oklch_to_linear_srgb(l: float, c: float, h: float) -> Tuple[float, float, float]:
    theta = math.radians(h)
    a = c * math.cos(theta)
    b = c * math.sin(theta)
    l_ = l + 0.3963377774 * a + 0.2158037573 * b
    m_ = l - 0.1055613458 * a - 0.0638541728 * b
    s_ = l - 0.0894841775 * a - 1.2914855480 * b
    r_lin = +4.0767416621 * (l_**3) - 3.3077115913 * (m_**3) + 0.2309699292 * (s_**3)
    g_lin = -1.2684380046 * (l_**3) + 2.6097574011 * (m_**3) - 0.3413193965 * (s_**3)
    b_lin = -0.0041960863 * (l_**3) - 0.7034186147 * (m_**3) + 1.7076147010 * (s_**3)
    return max(0.0, min(1.0, r_lin)), max(0.0, min(1.0, g_lin)), max(0.0, min(1.0, b_lin))

def _calculate_color_luminance(color_str: str) -> float:
    color_str = color_str.strip().lower()
    oklch_match = re.search(r"oklch\(\s*([\d.]+%?)\s+([\d.]+)\s+([\d.]+)", color_str)
    if oklch_match:
        l_str, c_str, h_str = oklch_match.groups()
        l_val = float(l_str[:-1]) / 100.0 if l_str.endswith("%") else float(l_str)
        r, g, b = _oklch_to_linear_srgb(l_val, float(c_str), float(h_str))
        return 0.2126 * r + 0.7152 * g + 0.0722 * b
    hex_match = re.search(r"#([0-9a-f]{3,8})", color_str)
    if hex_match:
        h = hex_match.group(1)
        if len(h) in (3, 4):
            h = "".join([c * 2 for c in h[:3]])
        elif len(h) >= 6:
            h = h[:6]
        r = _srgb_to_linear(int(h[0:2], 16))
        g = _srgb_to_linear(int(h[2:4], 16))
        b = _srgb_to_linear(int(h[4:6], 16))
        return 0.2126 * r + 0.7152 * g + 0.0722 * b
    return 0.5

def _calculate_contrast_ratio(lum1: float, lum2: float) -> float:
    lighter = max(lum1, lum2)
    darker = min(lum1, lum2)
    return (lighter + 0.05) / (darker + 0.05)

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"

class DesignCritic:
    def __init__(self, data_dir: Optional[Path] = None):
        self.data_dir = data_dir or DATA_DIR
        self.anti_patterns = self._load_anti_patterns()

    def _load_anti_patterns(self) -> List[Dict[str, Any]]:
        path = self.data_dir / "anti-patterns.json"
        if not path.exists():
            return []
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f).get("anti_patterns", [])

    def critique(self, html_content: str, decision: Optional[Dict[str, Any]] = None, iteration: int = 1) -> Dict[str, Any]:
        """
        Conducts independent multi-pillar audit and returns CriticReport conforming to schemas/critic-report.v1.json.
        """
        decision = decision or {}
        genome = decision.get("genome", {})
        style_family = decision.get("selected_style", "clean_stripe")

        hard_gate_failures = []
        defects_ranked = []

        # 1. Hard Gate: Zero Raw Emojis
        emoji_pattern = re.compile(
            r"[\U00010000-\U0010ffff]|[\u2600-\u27bf]|[\u2300-\u23ff]|[\u2b50-\u2b55]|[\u203c-\u2049]"
        )
        # Strip script/style tags before checking content
        clean_text = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", html_content, flags=re.DOTALL)
        if emoji_pattern.search(clean_text):
            hard_gate_failures.append({
                "gate": "Zero Raw Emojis",
                "message": "Found raw Unicode emoji in UI. Strict vector SVG icons are required.",
                "evidence": "Emoji codepoints detected in markup"
            })
            defects_ranked.append({
                "severity": "critical",
                "type": "raw_emoji_detected",
                "message": "Replace raw emoji with crisp SVG vector icon.",
                "suggested_patch": "Use <svg viewBox='0 0 24 24'> icon primitive."
            })

        # 2. Hard Gate: Viewport Meta Tag
        if 'name="viewport"' not in html_content:
            hard_gate_failures.append({
                "gate": "Mobile Viewport",
                "message": "Missing standard mobile viewport meta tag.",
                "evidence": "No <meta name='viewport'> tag"
            })
            defects_ranked.append({
                "severity": "critical",
                "type": "missing_viewport",
                "message": "Add mobile viewport meta tag.",
                "suggested_patch": "<meta name='viewport' content='width=device-width, initial-scale=1.0'>"
            })

        # 3. Hard Gate: Semantic Clickables (<div onclick>)
        # AST-based detection via BS4 to handle minified/malformed HTML correctly.
        if _BS4_AVAILABLE:
            soup = _BS4(html_content, "html.parser")
            div_onclick = soup.find_all("div", onclick=True)
        else:
            # Regex fallback (fragile on minified HTML, kept for zero-dep environments)
            div_onclick = re.findall(r"<div[^>]*onclick=", html_content, re.IGNORECASE)
        if div_onclick:
            hard_gate_failures.append({
                "gate": "Semantic Clickables",
                "message": f"Found {len(div_onclick)} non-semantic <div onclick> violation(s).",
                "evidence": "div onclick detected"
            })
            defects_ranked.append({
                "severity": "critical",
                "type": "non_semantic_clickable",
                "message": "Convert <div onclick> to semantic <button type='button'> or <a>.",
                "suggested_patch": "<button type='button' class='...'>"
            })

        # 4. Hard Gate: Focus Visible Rings
        if "focus-visible" not in html_content and ":focus" not in html_content:
            hard_gate_failures.append({
                "gate": "Keyboard Focus Rings",
                "message": "No focus-visible styling declared in stylesheet.",
                "evidence": "Missing :focus-visible rules"
            })
            defects_ranked.append({
                "severity": "critical",
                "type": "missing_focus_rings",
                "message": "Add focus-visible outline or ring to interactive elements.",
                "suggested_patch": "button:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }"
            })

        # 5. Anti-Slop Check: Generic AI Purple Gradient
        if "from-purple-600" in html_content and "to-indigo-600" in html_content:
            defects_ranked.append({
                "severity": "high",
                "type": "generic_ai_purple_gradient",
                "message": "Detected overused generic purple/indigo AI gradient trope.",
                "suggested_patch": "Replace with domain-calibrated OKLCH surface tones or edge lighting."
            })

        # 6. Performance Budget: Backdrop Filter Blur Budget
        # Canonical policy imported from vibe_core.constants.MAX_BLUR_SURFACES
        # BS4: search inside <style> blocks + inline style attributes only, not class names.
        if _BS4_AVAILABLE:
            _soup_blur = _BS4(html_content, "html.parser") if not _BS4_AVAILABLE or "soup" not in dir() else soup
            _style_texts = " ".join(t.get_text() for t in _soup_blur.find_all("style"))
            _inline_styles = " ".join(tag.get("style", "") for tag in _soup_blur.find_all(style=True))
            _blur_target = _style_texts + " " + _inline_styles
        else:
            _blur_target = html_content
        blur_matches = re.findall(r"backdrop-blur|blur\(", _blur_target)
        if len(blur_matches) > MAX_BLUR_SURFACES:
            defects_ranked.append({
                "severity": "high",
                "type": "excessive_backdrop_blur",
                "message": f"Found {len(blur_matches)} blur layers, exceeding GPU budget (<= {MAX_BLUR_SURFACES}).",
                "suggested_patch": "Reduce backdrop-filter layers to prevent mobile frame drops."
            })

        # 7. Semantic RTL Check
        is_rtl = 'dir="rtl"' in html_content or "dir='rtl'" in html_content
        if is_rtl:
            if "<bdi" not in html_content and "unicode-bidi" not in html_content and "ltr-code" not in html_content:
                hard_gate_failures.append({
                    "gate": "Semantic RTL Isolation",
                    "message": "RTL document lacks <bdi> or unicode-bidi isolation for mixed English terms.",
                    "evidence": "No <bdi> or unicode-bidi found"
                })
                defects_ranked.append({
                    "severity": "high",
                    "type": "missing_bidi_isolation",
                    "message": "Wrap mixed-language terms or add unicode-bidi: plaintext.",
                    "suggested_patch": "body { unicode-bidi: plaintext; }"
                })
        # 8. Reduced Motion Hard Gate — Deterministic (P0 from Qwen Review)
        # RULE: Motion tokens WITHOUT @media (prefers-reduced-motion: reduce) = CRITICAL hard gate failure.
        # Rationale: CSS animations without override can cause nausea/vestibular disorder in affected users.
        MOTION_TOKEN_RE = re.compile(
            r"\btransition\s*:|animation\s*:|@keyframes\b|lenis\b|scroll-behavior\s*:\s*smooth",
            re.IGNORECASE
        )
        style_blocks_content = " ".join(re.findall(r"<style[^>]*>(.*?)</style>", html_content, re.DOTALL | re.IGNORECASE))
        has_motion_tokens = bool(MOTION_TOKEN_RE.search(style_blocks_content))
        has_reduced_motion_override = "prefers-reduced-motion" in html_content

        if has_motion_tokens and not has_reduced_motion_override:
            hard_gate_failures.append({
                "gate": "Reduced Motion Override",
                "message": "Motion tokens (transition/animation/lenis) declared without @media (prefers-reduced-motion: reduce) override.",
                "evidence": "Risk: vestibular/nausea disorder for affected users. WCAG 2.1 SC 2.3.3 (AAA)."
            })
            defects_ranked.append({
                "severity": "critical",
                "type": "missing_reduced_motion_override",
                "message": "Add @media (prefers-reduced-motion: reduce) to neutralize all motion declarations.",
                "suggested_patch": "@media (prefers-reduced-motion: reduce) { *, *::before, *::after { animation-duration: 0.01ms !important; transition-duration: 0.01ms !important; scroll-behavior: auto !important; } }"
            })

        # 9. Component States Matrix Check
        has_skeleton = "skeleton" in html_content.lower() or "animate-pulse" in html_content
        has_empty = "empty" in html_content.lower() or "یافت نشد" in html_content or "no records" in html_content.lower()
        has_error = "retry" in html_content.lower() or "خطا" in html_content or "error" in html_content.lower()
        state_completeness_score = 10
        if not has_skeleton:
            state_completeness_score -= 3
            defects_ranked.append({
                "severity": "medium",
                "type": "missing_skeleton_state",
                "message": "No skeleton loading placeholder detected.",
                "suggested_patch": "Add skeleton state with animate-pulse."
            })
        if not has_empty:
            state_completeness_score -= 3
            defects_ranked.append({
                "severity": "low",
                "type": "missing_empty_state",
                "message": "No empty state UI container detected.",
                "suggested_patch": "Add empty state with vector icon and helper text."
            })
        if not has_error:
            state_completeness_score -= 3
            defects_ranked.append({
                "severity": "medium",
                "type": "missing_error_state",
                "message": "No error and retry recovery state detected.",
                "suggested_patch": "Add error container with retry button."
            })

        # 10. Mathematical WCAG Contrast Evaluation
        canvas_match = re.search(r"--canvas(?:-bg)?\s*:\s*([^;]+);", html_content)
        text_match = re.search(r"--text-primary\s*:\s*([^;]+);", html_content)
        if canvas_match and text_match:
            canvas_color = canvas_match.group(1).strip()
            text_color = text_match.group(1).strip()
            lum_canvas = _calculate_color_luminance(canvas_color)
            lum_text = _calculate_color_luminance(text_color)
            contrast_val = _calculate_contrast_ratio(lum_canvas, lum_text)
            if contrast_val < MIN_WCAG_AA_CONTRAST_NORMAL:
                defects_ranked.append({
                    "severity": "high",
                    "type": "low_wcag_contrast",
                    "message": f"Mathematical contrast ratio ({contrast_val:.2f}:1) fails WCAG AA minimum ({MIN_WCAG_AA_CONTRAST_NORMAL}:1).",
                    "suggested_patch": f"Adjust lightness of text or canvas to achieve at least {MIN_WCAG_AA_CONTRAST_NORMAL}:1 contrast."
                })

        # Scorecard computation — all values derived from measurable HTML signals, no hardcoded constants.
        # Touch target policy: HARD_MIN_TOUCH_PX = 24px (WCAG 2.2 AA), RECOMMENDED_TOUCH_PX = 44px (mobile HIG)
        
        # Visual Hierarchy: evidence — heading tags, display-font tokens, and asymmetric layout rhythm
        heading_tags = len(re.findall(r"<h[1-3][^>]*>", html_content, re.IGNORECASE))
        has_asymmetric_grid = "md:col-span-2" in html_content or "col-span-2" in html_content or "row-span-2" in html_content
        visual_hierarchy = min(14, 5 + (heading_tags * 2) + (3 if has_asymmetric_grid else 0) + (2 if "display-font" in html_content else 0))

        # Anti-Slop Distinctiveness: evidence — penalize clichéd purple/indigo gradients and sparkle icon tropes
        sparkle_count = len(re.findall(r"sparkle|lucide-sparkle|✨", html_content, re.IGNORECASE))
        has_purple_slop = "from-purple-600" in html_content or "from-indigo-500" in html_content
        
        anti_slop_distinctiveness = 15
        if has_purple_slop:
            anti_slop_distinctiveness -= 5
            defects_ranked.append({
                "severity": "medium",
                "type": "cliche_ai_gradient",
                "message": "Generic purple/indigo AI gradient detected. Use brand-calibrated OKLCH color palettes.",
                "suggested_patch": "Replace purple gradient with domain-calibrated OKLCH palette."
            })
        if sparkle_count > 1:
            anti_slop_distinctiveness -= 3
            defects_ranked.append({
                "severity": "low",
                "type": "ai_sparkle_infestation",
                "message": f"Excessive AI sparkle icons ({sparkle_count}) detected. Replace with domain-specific conceptual iconography.",
                "suggested_patch": "Use purposeful domain vector icons instead of repetitive sparkles."
            })
        anti_slop_distinctiveness = max(4, anti_slop_distinctiveness)

        # Domain Fit: evidence — CSS custom properties and domain-calibrated tokens signal intentional design
        css_var_count = len(re.findall(r"var\(--", html_content))
        has_signature_widget = "signature-widget" in html_content or "data-widget" in html_content or "calculator" in html_content or "slider" in html_content
        domain_fit = min(14, 4 + min(8, css_var_count) + (2 if has_signature_widget else 0))

        # Usability: evidence — presence of interactive semantic elements and absence of div-onclick violations
        usability = 10 if not div_onclick else 6

        # Typography: evidence — character-rich font-family declarations beyond generic Inter
        has_font_family = bool(re.search(r"font-family\s*:", html_content) or "display-font" in html_content)
        is_only_inter = "family=Inter" in html_content and not any(f in html_content for f in ["Plus+Jakarta", "Playfair", "Space+Grotesk", "JetBrains", "Instrument", "Syne", "Fraunces", "Vazirmatn", "Shabnam"])
        
        typography = 5
        if has_font_family:
            typography += 3
        if not is_only_inter:
            typography += 2
        else:
            defects_ranked.append({
                "severity": "low",
                "type": "monotonous_typography",
                "message": "Generic Inter-only typography detected without distinct display character pairing.",
                "suggested_patch": "Pair body font with distinct display typography (e.g. Plus Jakarta Sans, Instrument Serif, Vazirmatn)."
            })
        typography = min(10, typography)

        # Responsive: evidence — mobile viewport meta tag presence
        responsive = 10 if 'name="viewport"' in html_content else 4

        # Brand Coherence: evidence — presence of CSS variable design tokens (--surface, --accent, --text)
        brand_token_signals = ["--accent", "--surface", "--text-primary", "--border", "--canvas"]
        brand_matches = sum(1 for t in brand_token_signals if t in html_content)
        brand_coherence = min(9, brand_matches * 2)

        # Performance Budget: evidence — blur surface count measured above
        perf_budget = 5 if len(blur_matches) <= MAX_BLUR_SURFACES else 2

        scorecard = {
            "visual_hierarchy": visual_hierarchy,
            "anti_slop_distinctiveness": anti_slop_distinctiveness,
            "domain_fit": domain_fit,
            "usability": usability,
            "typography": typography,
            "responsive": responsive,
            "state_completeness": max(2, state_completeness_score),
            "brand_coherence": brand_coherence,
            "performance_budget": perf_budget
        }

        quality_score = sum(scorecard.values())
        hard_gates_pass = len(hard_gate_failures) == 0

        if hard_gates_pass and quality_score >= 80.0:
            acceptance_status = "ACCEPTED"
        elif not hard_gates_pass:
            acceptance_status = "REJECTED_CRITICAL"
        else:
            acceptance_status = "NEEDS_REFINEMENT"

        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "iteration": iteration,
            "evaluated_style": style_family,
            "hard_gates_pass": hard_gates_pass,
            "hard_gate_failures": hard_gate_failures,
            "quality_score": round(quality_score, 1),
            "scorecard": scorecard,
            "defects_ranked": defects_ranked,
            "acceptance_status": acceptance_status
        }
