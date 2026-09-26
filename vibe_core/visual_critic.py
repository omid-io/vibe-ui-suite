"""
vibe_core.visual_critic — Multi-Dimensional Visual & Aesthetic Review Engine (v3.4.0)
Evaluates rendered UI interfaces beyond static DOM syntax to guarantee:
- Clear Visual Focal Point & Hero Prominence
- Primary CTA Elevation & Sizing (>= 44px)
- Typography Hierarchy & Dynamic Scale Ratio
- Spacing Rhythm & Content Density
- Asymmetric Composition & Anti-Template Monotony
- Distinctive Visual Chemistry Adherence
"""

import re
from typing import Dict, Any, List, Optional

class VisualCritic:
    """
    Evaluates visual and aesthetic quality of rendered interfaces across 7 dimensions.
    Returns composite visual score (0-100), dimensional ratings (0-10),
    ranked visual defects (P0/P1/P2), and actionable repair prescriptions.
    """

    def __init__(self):
        self.min_acceptable_score = 80.0

    def evaluate(self, content: str, decision: Dict[str, Any]) -> Dict[str, Any]:
        """
        Performs multi-dimensional visual critique on component markup / rendered DOM.
        """
        defects = []
        prescriptions = []

        # 1. Visual Hierarchy & Focal Point (0 - 10)
        hierarchy_score, h_defects, h_prescriptions = self._evaluate_hierarchy(content)
        defects.extend(h_defects)
        prescriptions.extend(h_prescriptions)

        # 2. CTA Prominence & Sizing (0 - 10)
        cta_score, c_defects, c_prescriptions = self._evaluate_cta_prominence(content)
        defects.extend(c_defects)
        prescriptions.extend(c_prescriptions)

        # 3. Typography Rhythm & Contrast (0 - 10)
        typo_score, t_defects, t_prescriptions = self._evaluate_typography(content)
        defects.extend(t_defects)
        prescriptions.extend(t_prescriptions)

        # 4. Spacing Rhythm & Content Density (0 - 10)
        spacing_score, s_defects, s_prescriptions = self._evaluate_spacing(content)
        defects.extend(s_defects)
        prescriptions.extend(s_prescriptions)

        # 5. Composition & Layout Diversity (0 - 10)
        comp_score, comp_defects, comp_prescriptions = self._evaluate_composition(content, decision)
        defects.extend(comp_defects)
        prescriptions.extend(comp_prescriptions)

        # 6. Distinctiveness & Anti-Template Monotony (0 - 10)
        dist_score, d_defects, d_prescriptions = self._evaluate_distinctiveness(content, decision)
        defects.extend(d_defects)
        prescriptions.extend(d_prescriptions)

        # 7. Aesthetic Polish & Surface Discipline (0 - 10)
        polish_score, p_defects, p_prescriptions = self._evaluate_polish(content)
        defects.extend(p_defects)
        prescriptions.extend(p_prescriptions)

        dimensions = {
            "hierarchy": round(hierarchy_score, 1),
            "cta_prominence": round(cta_score, 1),
            "typography_rhythm": round(typo_score, 1),
            "spacing_density": round(spacing_score, 1),
            "composition_layout": round(comp_score, 1),
            "distinctiveness": round(dist_score, 1),
            "aesthetic_polish": round(polish_score, 1)
        }

        # Weighted composite score
        weights = {
            "hierarchy": 0.20,
            "cta_prominence": 0.18,
            "typography_rhythm": 0.15,
            "spacing_density": 0.12,
            "composition_layout": 0.15,
            "distinctiveness": 0.10,
            "aesthetic_polish": 0.10
        }

        composite_score = sum(dimensions[k] * 10.0 * weights[k] for k in dimensions)
        composite_score = round(min(100.0, max(0.0, composite_score)), 1)

        has_p0 = any(d.get("severity") == "P0" for d in defects)
        is_accepted = composite_score >= self.min_acceptable_score and not has_p0

        return {
            "visual_score": composite_score,
            "acceptance_status": "ACCEPTED" if is_accepted else "REVISE_REQUIRED",
            "dimensions": dimensions,
            "defects": defects,
            "repair_prescriptions": prescriptions
        }

    def _evaluate_hierarchy(self, content: str) -> tuple[float, List[Dict[str, Any]], List[str]]:
        score = 7.0
        defects = []
        prescriptions = []

        has_h1 = bool(re.search(r"<h1\b", content, re.IGNORECASE))
        has_display_size = bool(re.search(r"text-(3xl|4xl|5xl|6xl|7xl|8xl)", content))
        has_tight_tracking = "tracking-tight" in content or "font-black" in content

        if not has_h1:
            score -= 3.5
            defects.append({
                "severity": "P0",
                "type": "missing_h1_focal_point",
                "message": "Hero section lacks prominent <h1> visual focal point"
            })
            prescriptions.append("Introduce strong semantic <h1> with bold visual scale in the above-the-fold hero section")
        else:
            score += 1.2

        if has_display_size:
            score += 1.2
        else:
            score -= 1.5
            defects.append({
                "severity": "P1",
                "type": "weak_hero_scale",
                "message": "Hero headline uses subdued scale without clear display size"
            })
            prescriptions.append("Elevate headline size to text-4xl or larger with tight letter-spacing")

        if has_tight_tracking:
            score += 0.6

        return max(1.0, min(10.0, score)), defects, prescriptions

    def _evaluate_cta_prominence(self, content: str) -> tuple[float, List[Dict[str, Any]], List[str]]:
        score = 7.0
        defects = []
        prescriptions = []

        # Check for min touch targets (min-h-[44px] or py-3/py-4 with px-5+)
        has_min_touch = bool(re.search(r"min-h-\[(4[4-9]|[5-9]\d)px\]", content)) or bool(re.search(r"py-(3|4)\b", content))
        has_generous_padding = bool(re.search(r"px-(5|6|7|8)\b", content))
        has_active_feedback = bool(re.search(r"active:(scale-\d+|translate-)", content)) or "cursor-pointer" in content

        if not has_min_touch:
            score -= 3.0
            defects.append({
                "severity": "P1",
                "type": "substandard_touch_target",
                "message": "Interactive action buttons lack verified >= 44px touch targets"
            })
            prescriptions.append("Enforce min-h-[44px] and comfortable padding (px-6 py-3) on all primary clickable elements")
        else:
            score += 1.3

        if has_generous_padding:
            score += 0.9

        if has_active_feedback:
            score += 0.8
        else:
            score -= 0.6
            defects.append({
                "severity": "P2",
                "type": "missing_active_spring",
                "message": "Primary buttons lack snappy active-press tactile feedback"
            })
            prescriptions.append("Add active:scale-95 or active:translate-y-[2px] for tactile spring response")

        return max(1.0, min(10.0, score)), defects, prescriptions

    def _evaluate_typography(self, content: str) -> tuple[float, List[Dict[str, Any]], List[str]]:
        score = 7.0
        defects = []
        prescriptions = []

        has_bdi = "<bdi>" in content
        has_font_character = bool(re.search(r"\b(font-mono|font-serif|uppercase|tracking-widest|tracking-tight)\b", content))
        has_numerical_clarity = bool(re.search(r"\b(tabular-nums|\d+(?:\.\d+)?(?:%|px|ms|s|\$|€))\b", content))

        if not has_bdi:
            score -= 2.0
            defects.append({
                "severity": "P1",
                "type": "missing_bdi_isolation",
                "message": "Numerical data and code tokens lack <bdi> bidirectional isolation"
            })
            prescriptions.append("Wrap all formatted numbers, currencies, and technical IDs in <bdi> tags")
        else:
            score += 1.4

        if has_font_character:
            score += 1.0

        if has_numerical_clarity:
            score += 0.6

        return max(1.0, min(10.0, score)), defects, prescriptions

    def _evaluate_spacing(self, content: str) -> tuple[float, List[Dict[str, Any]], List[str]]:
        score = 7.0
        defects = []
        prescriptions = []

        has_responsive_padding = bool(re.search(r"(?:p-[6-9]|py-[6-9]|py-1[0-6]|p-10|p-12)", content))
        has_multi_tier_gap = bool(re.search(r"(?:gap-4|gap-6|gap-8|space-y-[4-8])", content))

        if not has_responsive_padding:
            score -= 2.0
            defects.append({
                "severity": "P1",
                "type": "cramped_spacing_rhythm",
                "message": "Container lacks generous breathing room and section rhythm"
            })
            prescriptions.append("Apply generous padding (p-6 sm:p-10) to avoid cramped, card-heavy appearance")
        else:
            score += 1.6

        if has_multi_tier_gap:
            score += 1.4

        return max(1.0, min(10.0, score)), defects, prescriptions

    def _evaluate_composition(self, content: str, decision: Dict[str, Any]) -> tuple[float, List[Dict[str, Any]], List[str]]:
        score = 7.0
        defects = []
        prescriptions = []

        has_asymmetric_grid = bool(re.search(r"(?:grid-cols-12|col-span-7|col-span-5|col-span-8|col-span-4|grid-cols-1\s+(?:sm|md|lg):grid-cols-[23])", content))
        has_media_container = "aspect-" in content or "data-origin=\"synthetic_demo\"" in content

        if not has_asymmetric_grid:
            score -= 2.5
            defects.append({
                "severity": "P1",
                "type": "flat_monolithic_layout",
                "message": "Layout lacks structured multi-column or asymmetric grid rhythm"
            })
            prescriptions.append("Employ asymmetric bento grid or split-column rhythm (grid grid-cols-1 lg:grid-cols-12)")
        else:
            score += 1.6

        if has_media_container:
            score += 1.4

        return max(1.0, min(10.0, score)), defects, prescriptions

    def _evaluate_distinctiveness(self, content: str, decision: Dict[str, Any]) -> tuple[float, List[Dict[str, Any]], List[str]]:
        score = 7.8
        defects = []
        prescriptions = []

        has_raw_sparkle = "✨" in content or "icon-sparkle" in content
        has_cliche_purple = "from-purple-600" in content or "to-indigo-600" in content
        has_compiled_chemistry = bool(re.search(r"(?:shadow-\[\d+px_\d+px|backdrop-blur-xl|font-mono\s+uppercase|border-2\s+border-black)", content))

        if has_raw_sparkle:
            score -= 4.0
            defects.append({
                "severity": "P0",
                "type": "cliche_ai_sparkle",
                "message": "Interface uses clichéd sparkle emojis indicating generic AI aesthetic"
            })
            prescriptions.append("Remove raw sparkle emojis; use domain-specific SVG vector icons with currentColor")

        if has_cliche_purple:
            score -= 3.0
            defects.append({
                "severity": "P0",
                "type": "cliche_ai_gradient",
                "message": "Generic purple-to-indigo gradient detected"
            })
            prescriptions.append("Use authentic OKLCH palette matching the resolved visual chemistry")

        if has_compiled_chemistry:
            score += 1.8

        return max(1.0, min(10.0, score)), defects, prescriptions

    def _evaluate_polish(self, content: str) -> tuple[float, List[Dict[str, Any]], List[str]]:
        score = 7.5
        defects = []
        prescriptions = []

        blur_count = len(re.findall(r"backdrop-blur-(?:sm|md|lg|xl|2xl)", content))
        if blur_count > 3:
            score -= 2.5
            defects.append({
                "severity": "P1",
                "type": "excessive_compositing_blur",
                "message": f"Detected {blur_count} backdrop-blur layers, exceeding GPU budget of 3"
            })
            prescriptions.append("Reduce layered glassmorphism; cap backdrop blur to max 3 layers to prevent GPU fill-rate on mobile viewports")
        else:
            score += 1.0

        has_subtle_borders = bool(re.search(r"border-(?:zinc|stone|emerald|neutral)-\d+/\d+", content)) or "border-2 border-black" in content
        if has_subtle_borders:
            score += 1.5

        return max(1.0, min(10.0, score)), defects, prescriptions
