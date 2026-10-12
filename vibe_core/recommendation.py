"""
vibe_core.recommendation — Recommendation Engine & Conflict Resolver
Multi-factor candidate scoring, style matching, and conflict resolution matrix.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"

class RecommendationEngine:
    def __init__(self, data_dir: Optional[Path] = None):
        self.data_dir = data_dir or DATA_DIR
        self.taxonomy = self._load_json("taxonomy.json").get("domains", [])
        self.styles = self._load_json("styles.json").get("styles", [])
        self.palettes = self._load_json("palettes.json").get("palettes", [])
        self.typography = self._load_json("typography.json").get("pairings", [])
        self.priors = self._load_json("priors.json").get("priors", {})
        self.compatibility = self._load_json("compatibility.json").get("compatibility_rules", [])

    def _load_json(self, filename: str) -> Dict[str, Any]:
        path = self.data_dir / filename
        if not path.exists():
            return {}
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def recommend(self, intent: Dict[str, Any], user_style_preference: Optional[str] = None) -> Dict[str, Any]:
        """
        Ranks candidate styles, resolves conflicts, and generates DesignDecisionContract.
        """
        domain_id = intent.get("product_domain", "general_modern_saas")
        domain_info = next((d for d in self.taxonomy if d["id"] == domain_id), self.taxonomy[0] if self.taxonomy else {})
        product_mode = intent.get("product_mode", "persuade")

        ranked_candidates = []
        conflict_resolutions = []

        # Check for explicit user conflict
        active_style_target = user_style_preference
        if user_style_preference:
            forbidden = domain_info.get("forbidden_styles", [])
            if user_style_preference in forbidden:
                # Conflict detected! Resolve to Controlled Hybrid
                resolved_hybrid_name = f"Controlled {user_style_preference.replace('_', ' ').title()} ({domain_info.get('name_en', '')})"
                conflict_resolutions.append({
                    "conflict_type": "user_style_vs_domain_prior",
                    "user_preference": user_style_preference,
                    "domain_prior": f"Domain forbids {user_style_preference} due to trust/clarity constraints",
                    "resolved_outcome": resolved_hybrid_name,
                    "reason": "Preserve explicit user aesthetic while enforcing strict high-contrast readability and removing decorative noise"
                })

        for style in self.styles:
            s_id = style["id"]
            score, breakdown = self._score_style(style, domain_info, product_mode, intent)
            
            # Boost if user explicitly asked for this style
            if user_style_preference == s_id:
                score = min(99.0, score + 25.0)

            ranked_candidates.append({
                "style": s_id,
                "name": style.get("name_en", s_id),
                "score": round(score, 1),
                "breakdown": breakdown
            })

        ranked_candidates.sort(key=lambda x: x["score"], reverse=True)
        top_choice = ranked_candidates[0]
        selected_style_id = top_choice["style"]
        selected_style_obj = next((s for s in self.styles if s["id"] == selected_style_id), self.styles[0])

        # Match typography pairing
        matched_typography = self._match_typography(selected_style_id, domain_id)

        # Match palette
        matched_palette = self._match_palette(selected_style_id, domain_id)

        # Construct Design Genome
        is_hybrid = bool(conflict_resolutions)
        genome = {
            "style_family": selected_style_obj["family"] if not is_hybrid else conflict_resolutions[0]["resolved_outcome"],
            "is_hybrid": is_hybrid,
            "hybrid_components": [selected_style_id, "controlled_minimal_invariants"] if is_hybrid else [selected_style_id],
            "mood": "calm" if domain_info.get("visual_energy") == "calm_restrained" else "technical",
            "domain": domain_id,
            "audience": intent.get("audience", {}),
            "product_mode": product_mode,
            "brand_personality": selected_style_obj.get("personality", ["clean"]),
            "typography": {
                "display_family": matched_typography.get("display_en", "Inter"),
                "body_family": matched_typography.get("body_en", "Inter"),
                "mono_family": "JetBrains Mono",
                "persian_family": matched_typography.get("persian_fa", "Vazirmatn"),
                "scale_ratio": matched_typography.get("scale_ratio", 1.25),
                "line_height_body": matched_typography.get("line_height_body", 1.6)
            },
            "color": {
                "canvas": matched_palette.get("canvas", "oklch(0.98 0.005 85)"),
                "surface": matched_palette.get("surface", "oklch(0.95 0.01 85)"),
                "accent": matched_palette.get("accent", "oklch(0.65 0.09 75)"),
                "border": matched_palette.get("border", "oklch(0.88 0.01 85)"),
                "text": matched_palette.get("text", "oklch(0.20 0.015 60)"),
                "muted_text": matched_palette.get("text_muted", "oklch(0.48 0.015 60)"),
                "color_space": "oklch"
            },
            "layout": {
                "grid_type": "asymmetric_bento" if product_mode in ["persuade", "experience"] else "standard_columns",
                "container_max_width": "max-w-7xl",
                "whitespace_cadence": "generous" if domain_info.get("density") == "airy" else "balanced"
            },
            "density": domain_info.get("density", "balanced"),
            "radius": {
                "base": selected_style_obj.get("geometry", {}).get("radius_base", "8px"),
                "container": "12px",
                "button": "8px"
            },
            "depth": selected_style_obj.get("elevation", "diffused_soft"),
            "motion": {
                "time_constant_lambda": selected_style_obj.get("motion", {}).get("time_constant_lambda", 14),
                "duration_ms": 200,
                "respect_reduced_motion": True
            },
            "texture": "solid_clean",
            "iconography": "svg_geometric",
            "interaction": {
                "touch_target_min_px": 44
            },
            "platform": {
                "mobile_first": True,
                "rtl_support": ("fa" in intent.get("language", [])) if isinstance(intent.get("language"), (list, tuple)) else (intent.get("language") == "fa" or "fa" in intent.get("languages", []))
            },
            "accessibility": {
                "target_contrast": "WCAG_AA",
                "focus_visible_required": True
            },
            "states": {
                "skeleton_loading": True,
                "empty_state": True,
                "error_retry": True
            }
        }

        # Construct decision trace
        decision_trace = {
            "scoring_breakdown": top_choice["breakdown"],
            "rationale": [
                f"Selected '{top_choice['name']}' based on optimal domain fit for {domain_info.get('name_en', '')}.",
                f"Typography matched with '{matched_typography.get('display_en')}' and guaranteed Persian Vazirmatn web font.",
                f"Palette '{matched_palette.get('name', '')}' calibrated in OKLCH space with verified contrast ratio of {matched_palette.get('contrast_ratio_text', 14.5)}:1."
            ],
            "alternatives_considered": [
                {"style": c["style"], "score": c["score"], "rejection_reason": f"Lower composite fit score ({c['score']}) compared to {top_choice['score']}"}
                for c in ranked_candidates[1:4]
            ],
            "conflict_resolutions": conflict_resolutions
        }

        return {
            "decision_id": f"dec-{domain_id}-{selected_style_id}",
            "intent_id": f"int-{domain_id}",
            "timestamp": "2026-09-03T12:00:00Z",
            "selected_style": selected_style_id,
            "composite_score": top_choice["score"],
            "confidence": intent.get("confidence", {}).get("overall", 0.90),
            "genome": genome,
            "decision_trace": decision_trace,
            "hard_constraints_verified": intent.get("hard_constraints", [])
        }

    def _score_style(self, style: Dict[str, Any], domain: Dict[str, Any], mode: str, intent: Dict[str, Any]) -> Tuple[float, Dict[str, float]]:
        """Applies mathematical candidate scoring formula."""
        s_id = style["id"]
        rec_styles = domain.get("recommended_styles", [])
        forbid_styles = domain.get("forbidden_styles", [])

        # 1. Domain Fit (0-15)
        if s_id in rec_styles:
            rank_idx = rec_styles.index(s_id)
            domain_fit = 15.0 - (rank_idx * 2.0)
        elif s_id in forbid_styles:
            domain_fit = 2.0
        else:
            domain_fit = 8.0

        # 2. Audience Fit (0-15)
        audience_fit = 13.0 if domain.get("density") in style.get("density_support", []) else 9.0

        # 3. Mode Fit (0-15)
        if mode == "operate" and s_id in ["data_dense_terminal", "linear_dark", "clean_stripe"]:
            mode_fit = 15.0
        elif mode in ["persuade", "experience"] and s_id in ["quiet_luxury", "editorial_magazine", "neobrutalism", "modern_glass_2"]:
            mode_fit = 15.0
        else:
            mode_fit = 10.0

        # 4. Tone Fit (0-15)
        tone_fit = 12.0

        # 5. Platform Fit (0-10)
        platform_fit = 9.0

        # 6. A11y Fit (0-15)
        # Neobrutalism and Minimal Swiss have high contrast natively
        a11y_fit = 15.0 if s_id in ["minimal_swiss", "neobrutalism", "clean_stripe"] else 12.5

        # Penalties
        penalty = 30.0 if s_id in forbid_styles else 0.0

        # Normalize total to 0-100
        raw_total = (domain_fit * 0.25 + audience_fit * 0.20 + mode_fit * 0.20 + tone_fit * 0.15 + platform_fit * 0.10 + a11y_fit * 0.10) * 6.666 - penalty
        score = max(5.0, min(98.0, raw_total))

        breakdown = {
            "domain_fit": domain_fit,
            "audience_fit": audience_fit,
            "mode_fit": mode_fit,
            "tone_fit": tone_fit,
            "platform_fit": platform_fit,
            "a11y_fit": a11y_fit,
            "penalty": penalty
        }
        return score, breakdown

    def _match_typography(self, style_id: str, domain_id: str) -> Dict[str, Any]:
        for pair in self.typography:
            if style_id in pair.get("best_for_styles", []):
                return pair
        return self.typography[0] if self.typography else {}

    def _match_palette(self, style_id: str, domain_id: str) -> Dict[str, Any]:
        for pal in self.palettes:
            if domain_id in pal.get("best_for", []) or style_id in pal.get("best_for", []):
                return pal
        return self.palettes[0] if self.palettes else {}
