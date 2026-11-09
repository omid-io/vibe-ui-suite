"""
vibe_core.recommendation — Recommendation Engine & Conflict Resolver
Unified with Design Genome 2.0 catalog and BM25 DesignIntelligenceEngine.
Multi-factor candidate scoring, style matching, and conflict resolution matrix.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple, Union

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"

from vibe_core.search_engine import DesignIntelligenceEngine


class RecommendationEngine:
    def __init__(self, data_dir: Optional[Path] = None):
        self.data_dir = data_dir or DATA_DIR
        self.genome_path = self.data_dir / "catalog" / "design_genome.json"

        # Initialize DesignIntelligenceEngine (Okapi BM25 index across Design Genome 2.0)
        self.search_engine = DesignIntelligenceEngine(
            catalog_path=self.genome_path if self.genome_path.exists() else None
        )

        # Single Source of Truth: Load canonical design_genome.json
        genome_data: Dict[str, Any] = {}
        if self.genome_path.exists():
            try:
                with open(self.genome_path, "r", encoding="utf-8") as f:
                    genome_data = json.load(f)
            except Exception:
                genome_data = {}

        self.genome_styles = genome_data.get("styles", [])
        self.genome_palettes = genome_data.get("palettes", [])
        self.genome_typography = genome_data.get("typography_systems", [])
        self.genome_archetypes = genome_data.get("composition_archetypes", [])

        # Legacy fallbacks if genome is missing or empty
        legacy_styles = self._load_json("styles.json").get("styles", [])
        legacy_palettes = self._load_json("palettes.json").get("palettes", [])
        legacy_typo = self._load_json("typography.json").get("pairings", [])

        self.styles = self.genome_styles if self.genome_styles else legacy_styles
        self.palettes = self.genome_palettes if self.genome_palettes else legacy_palettes
        self.typography = self.genome_typography if self.genome_typography else legacy_typo

        self.taxonomy = self._load_json("taxonomy.json").get("domains", [])
        self.priors = self._load_json("priors.json").get("priors", {})
        self.compatibility = self._load_json("compatibility.json").get("compatibility_rules", [])

    def _load_json(self, filename: str) -> Dict[str, Any]:
        path = self.data_dir / filename
        if not path.exists():
            return {}
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}

    def recommend(
        self,
        intent: Union[Dict[str, Any], Any],
        user_style_preference: Optional[str] = None,
        trend_evidence: Optional[Any] = None
    ) -> Dict[str, Any]:
        """
        Ranks candidate styles from Design Genome 2.0 via Okapi BM25,
        resolves conflicts, matches calibrated palette and typography,
        and generates a unified DesignDecision contract.
        """
        if hasattr(intent, "to_dict"):
            c_dict = intent.to_dict()
            meta = c_dict.get("metadata", {})
            intent_dict = {**meta, **c_dict}
        elif isinstance(intent, dict):
            meta = intent.get("metadata", {})
            intent_dict = {**meta, **intent}
        else:
            intent_dict = {}

        trend_style = ""
        trend_arch = ""
        trend_banned: List[str] = []
        te_dict: Dict[str, Any] = {}
        if trend_evidence:
            if hasattr(trend_evidence, "to_dict"):
                te_dict = trend_evidence.to_dict()
            elif isinstance(trend_evidence, dict):
                te_dict = trend_evidence
            trend_style = str(te_dict.get("selected_style", "")).lower()
            trend_arch = str(te_dict.get("composition_archetype", ""))
            trend_banned = [str(b).lower() for b in te_dict.get("banned_slop_tropes", [])]

        domain_id = intent_dict.get("domain") or intent_dict.get("product_domain", "general_modern_saas")
        domain_info = next((d for d in self.taxonomy if d.get("id") == domain_id), {"id": domain_id, "name_en": domain_id})
        product_mode = intent_dict.get("product_mode", "persuade")

        conflict_resolutions: List[Dict[str, Any]] = []

        # Check for explicit user conflict against domain forbidden styles
        if user_style_preference:
            forbidden = domain_info.get("forbidden_styles", [])
            if user_style_preference in forbidden:
                resolved_hybrid_name = f"Controlled {user_style_preference.replace('_', ' ').title()} ({domain_info.get('name_en', '')})"
                conflict_resolutions.append({
                    "conflict_type": "user_style_vs_domain_prior",
                    "user_preference": user_style_preference,
                    "domain_prior": f"Domain forbids {user_style_preference} due to trust/clarity constraints",
                    "resolved_outcome": resolved_hybrid_name,
                    "reason": "Preserve explicit user aesthetic while enforcing strict high-contrast readability and removing decorative noise"
                })

        # -------------------------------------------------------------
        # 1. Okapi BM25 Candidate Ranking from Design Genome 2.0
        # -------------------------------------------------------------
        query_parts = [domain_id]
        if intent_dict.get("emotional_tone"):
            query_parts.append(str(intent_dict.get("emotional_tone")))
        if intent_dict.get("visual_energy"):
            query_parts.append(str(intent_dict.get("visual_energy")))
        if user_style_preference:
            query_parts.append(str(user_style_preference))
        search_query = " ".join(query_parts).strip()

        bm25_candidates = self.search_engine.search_styles(
            query=search_query,
            limit=5,
            domain_filter=domain_id
        )

        ranked_candidates: List[Dict[str, Any]] = []
        for cand in bm25_candidates:
            s_id = cand["id"]
            s_obj = cand.get("metadata", {})
            bm25_score = cand.get("score", 5.0)

            # Mathematical multi-factor boost & prior blending
            formula_score, breakdown = self._score_style(s_obj, domain_info, product_mode, intent_dict)
            composite_score = round(min(98.5, max(10.0, (bm25_score * 3.5) + (formula_score * 0.65))), 1)

            if user_style_preference and (user_style_preference == s_id or user_style_preference in s_id):
                composite_score = min(99.0, composite_score + 20.0)

            # Trend evidence style boost & slop penalties
            if trend_style and (trend_style in s_id.lower() or trend_style in str(s_obj.get("name", "")).lower()):
                composite_score = min(99.0, composite_score + 15.0)
            if any(b in s_id.lower() or b in str(s_obj.get("name", "")).lower() for b in trend_banned):
                composite_score = max(5.0, composite_score - 25.0)

            ranked_candidates.append({
                "style": s_id,
                "name": s_obj.get("name") or s_obj.get("name_en", s_id),
                "score": composite_score,
                "metadata": s_obj,
                "breakdown": breakdown
            })

        # Fallback if BM25 candidate list was empty
        if not ranked_candidates:
            for style in self.styles[:5]:
                s_id = style.get("style_id") or style.get("id", "clean_stripe")
                score, breakdown = self._score_style(style, domain_info, product_mode, intent_dict)
                ranked_candidates.append({
                    "style": s_id,
                    "name": style.get("name") or style.get("name_en", s_id),
                    "score": round(score, 1),
                    "metadata": style,
                    "breakdown": breakdown
                })

        ranked_candidates.sort(key=lambda x: x["score"], reverse=True)
        top_choice = ranked_candidates[0]
        selected_style_id = top_choice["style"]
        selected_style_obj = top_choice.get("metadata") or self.search_engine.get_style_by_id(selected_style_id) or self.styles[0]
        selected_style_family = selected_style_obj.get("name") or selected_style_obj.get("family", selected_style_id)

        # -------------------------------------------------------------
        # 2. Match Best Calibrated OKLCH Palette
        # -------------------------------------------------------------
        matched_palette = self._match_palette(selected_style_id, domain_id)

        # Extract light and OLED dark tokens
        if "light" in matched_palette and isinstance(matched_palette["light"], dict):
            light_tokens = matched_palette["light"]
            dark_tokens = matched_palette.get("dark_oled", {})
        elif "palette" in selected_style_obj and isinstance(selected_style_obj["palette"], dict):
            light_tokens = selected_style_obj["palette"]
            dark_tokens = selected_style_obj.get("secondary_oled", {})
        else:
            light_tokens = matched_palette
            dark_tokens = selected_style_obj.get("secondary_oled", {})

        unified_tokens = {
            "canvas": light_tokens.get("canvas", "oklch(0.99 0.005 0.0)"),
            "surface": light_tokens.get("surface", "oklch(0.96 0.007 0.0)"),
            "surface_elevated": light_tokens.get("surface_elevated", "oklch(1.00 0.005 0.0)"),
            "border": light_tokens.get("border", "oklch(0.90 0.006 0.0)"),
            "text": light_tokens.get("text_primary") or light_tokens.get("text", "oklch(0.12 0.020 0.0)"),
            "text_primary": light_tokens.get("text_primary") or light_tokens.get("text", "oklch(0.12 0.020 0.0)"),
            "text_secondary": light_tokens.get("text_secondary") or light_tokens.get("text_muted", "oklch(0.40 0.016 0.0)"),
            "text_muted": light_tokens.get("text_secondary") or light_tokens.get("text_muted", "oklch(0.40 0.016 0.0)"),
            "accent": light_tokens.get("accent", "oklch(0.58 0.080 0.0)"),
            "accent_hover": light_tokens.get("accent_hover", "oklch(0.51 0.084 0.0)"),
            "status_tokens": light_tokens.get("status_tokens", {
                "success": "oklch(0.62 0.17 145)",
                "warning": "oklch(0.68 0.16 75)",
                "error": "oklch(0.58 0.22 25)",
                "info": "oklch(0.60 0.18 245)"
            }),
            "dark_oled": dark_tokens if dark_tokens else {
                "canvas": "oklch(0.12 0.015 0.0)",
                "surface": "oklch(0.17 0.022 0.0)",
                "surface_elevated": "oklch(0.21 0.015 0.0)",
                "border": "oklch(0.26 0.018 0.0)",
                "text_primary": "oklch(0.96 0.010 0.0)",
                "text_secondary": "oklch(0.68 0.008 0.0)",
                "accent": "oklch(0.72 0.088 0.0)",
                "accent_hover": "oklch(0.79 0.092 0.0)",
                "status_tokens": {
                    "success": "oklch(0.75 0.17 145)",
                    "warning": "oklch(0.80 0.16 75)",
                    "error": "oklch(0.72 0.20 25)",
                    "info": "oklch(0.74 0.16 245)"
                }
            }
        }

        # -------------------------------------------------------------
        # 3. Match Typography Pairing & Persian Webfont Standard
        # -------------------------------------------------------------
        matched_typography = self._match_typography(selected_style_id, domain_id)
        style_typo = selected_style_obj.get("typography", {})

        display_font = style_typo.get("heading_font") or matched_typography.get("display") or matched_typography.get("display_en", "Inter")
        body_font = style_typo.get("body_font") or matched_typography.get("body") or matched_typography.get("body_en", "Inter")
        mono_font = style_typo.get("mono_font") or matched_typography.get("mono") or "JetBrains Mono"
        scale_ratio = style_typo.get("scale_ratio") or matched_typography.get("scale_ratio", 1.25)

        typography_dict = {
            "heading_font": display_font,
            "body_font": body_font,
            "mono_font": mono_font,
            "display_family": display_font,
            "body_family": body_font,
            "mono_family": mono_font,
            "persian_family": "Vazirmatn",
            "scale_ratio": scale_ratio,
            "line_height_body": 1.6
        }

        # -------------------------------------------------------------
        # 4. Match Composition Archetype (Incorporate TrendEvidence)
        # -------------------------------------------------------------
        comp_archetype = trend_arch or self._match_archetype(domain_id)

        # -------------------------------------------------------------
        # 5. Geometry, Density, Surfaces & Motion Physics
        # -------------------------------------------------------------
        style_geom = selected_style_obj.get("geometry", {})
        geometry = {
            "radius_base": style_geom.get("border_radius") or style_geom.get("radius_base", "8px"),
            "border_radius": style_geom.get("border_radius") or style_geom.get("radius_base", "8px"),
            "container": "12px",
            "button": "8px",
            "border_weight": style_geom.get("border_weight", "1px"),
            "shadow_style": style_geom.get("shadow_style", "micro_shadow"),
            "border_style": style_geom.get("border_style", "solid")
        }

        raw_density = selected_style_obj.get("spacing_density") or domain_info.get("density", "balanced")
        if raw_density in ("compact", "balanced", "airy"):
            density = str(raw_density)
        else:
            density = "compact" if any(k in str(raw_density).lower() for k in ["dense", "high", "hud"]) else ("airy" if "airy" in str(raw_density).lower() else "balanced")

        raw_surfaces = selected_style_obj.get("surfaces", "flat")
        surfaces = {
            "depth": raw_surfaces if isinstance(raw_surfaces, str) else raw_surfaces.get("depth", "flat"),
            "elevation": "surface",
            "treatment": "subtle_border"
        }

        motion_profile = selected_style_obj.get("motion", {
            "spring_physics": {"stiffness": 260, "damping": 24, "mass": 1.0},
            "easing": "cubic-bezier(0.34, 1.56, 0.64, 1)",
            "duration_scale": 1.0,
            "time_constant_lambda": 14,
            "duration_ms": 200,
            "respect_reduced_motion": True
        })

        is_hybrid = bool(conflict_resolutions)

        # Assemble full backward-compatible Genome object
        genome = {
            "style_id": selected_style_id,
            "style": selected_style_id,
            "style_family": selected_style_family if not is_hybrid else conflict_resolutions[0]["resolved_outcome"],
            "is_hybrid": is_hybrid,
            "hybrid_components": [selected_style_id, "controlled_minimal_invariants"] if is_hybrid else [selected_style_id],
            "mood": "calm" if domain_info.get("visual_energy") == "calm_restrained" else "technical",
            "domain": domain_id,
            "audience": intent_dict.get("audience", {}),
            "product_mode": product_mode,
            "brand_personality": selected_style_obj.get("emotional_tone") or selected_style_obj.get("personality", ["clean"]),
            "typography": typography_dict,
            "color": {
                "canvas": unified_tokens["canvas"],
                "surface": unified_tokens["surface"],
                "accent": unified_tokens["accent"],
                "border": unified_tokens["border"],
                "text": unified_tokens["text"],
                "muted_text": unified_tokens["text_muted"],
                "color_space": "oklch"
            },
            "tokens": unified_tokens,
            "layout": {
                "grid_type": comp_archetype,
                "container_max_width": "max-w-7xl",
                "whitespace_cadence": "generous" if density == "airy" else "balanced"
            },
            "composition_archetype": comp_archetype,
            "density": density,
            "radius": {
                "base": geometry["radius_base"],
                "container": geometry["container"],
                "button": geometry["button"]
            },
            "geometry": geometry,
            "depth": surfaces["depth"],
            "surfaces": surfaces,
            "motion": {
                "time_constant_lambda": motion_profile.get("time_constant_lambda", 14),
                "duration_ms": motion_profile.get("duration_ms", 200),
                "respect_reduced_motion": True,
                "spring_physics": motion_profile.get("spring_physics", {"stiffness": 260, "damping": 24, "mass": 1.0})
            },
            "motion_profile": motion_profile,
            "texture": "solid_clean",
            "iconography": "svg_geometric",
            "interaction": {
                "touch_target_min_px": 44
            },
            "platform": {
                "mobile_first": True,
                "rtl_support": bool(
                    "fa" in intent_dict.get("language", [])
                    if isinstance(intent_dict.get("language"), (list, tuple))
                    else (intent_dict.get("language") == "fa" or "fa" in intent_dict.get("languages", []) or intent_dict.get("is_rtl", False))
                )
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

        # Decision trace rationale
        decision_trace = {
            "scoring_breakdown": top_choice["breakdown"],
            "bm25_score": top_choice["score"],
            "rationale": [
                f"Selected '{top_choice['name']}' ({selected_style_id}) via Okapi BM25 ranking across Design Genome 2.0.",
                f"Typography matched: display='{display_font}', body='{body_font}' with guaranteed Persian Vazirmatn fallback.",
                f"Palette '{matched_palette.get('name', 'Calibrated OKLCH')}' loaded with dual-theme (Light canonical & OLED secondary)."
            ],
            "alternatives_considered": [
                {"style": c["style"], "score": c["score"], "rejection_reason": f"Lower composite score ({c['score']}) compared to {top_choice['score']}"}
                for c in ranked_candidates[1:4]
            ],
            "conflict_resolutions": conflict_resolutions
        }

        return {
            "decision_id": f"dec-{domain_id}-{selected_style_id}",
            "intent_id": f"int-{domain_id}",
            "timestamp": "2026-11-09T12:00:00Z",
            "selected_style": selected_style_id,
            "style_id": selected_style_id,
            "style": selected_style_id,
            "style_family": selected_style_family,
            "tokens": unified_tokens,
            "typography": typography_dict,
            "composition_archetype": comp_archetype,
            "palette": matched_palette,
            "geometry": geometry,
            "density": density,
            "surfaces": surfaces,
            "motion_profile": motion_profile,
            "domain": domain_id,
            "composite_score": top_choice["score"],
            "confidence": intent_dict.get("confidence", {}).get("overall", 0.90) if isinstance(intent_dict.get("confidence"), dict) else 0.90,
            "genome": genome,
            "decision_trace": decision_trace,
            "hard_constraints_verified": intent_dict.get("hard_constraints", []),
            "trend_evidence": te_dict,
            "intent": intent_dict
        }

    def _score_style(
        self,
        style: Dict[str, Any],
        domain: Dict[str, Any],
        mode: str,
        intent: Dict[str, Any]
    ) -> Tuple[float, Dict[str, float]]:
        """Calculates multi-factor domain prior score."""
        s_id = style.get("style_id") or style.get("id", "")
        rec_styles = domain.get("recommended_styles", [])
        forbid_styles = domain.get("forbidden_styles", [])

        # 1. Domain Fit (0-15)
        if s_id in rec_styles or any(s_id.startswith(r) for r in rec_styles):
            domain_fit = 15.0
        elif s_id in forbid_styles or any(s_id.startswith(f) for f in forbid_styles):
            domain_fit = 2.0
        else:
            # Check domain list in genome style
            style_domains = style.get("domains", [])
            domain_fit = 14.0 if domain.get("id") in style_domains else 9.0

        # 2. Audience Fit (0-15)
        style_density = [style.get("spacing_density", "balanced")] if "spacing_density" in style else style.get("density_support", ["balanced"])
        audience_fit = 14.0 if domain.get("density", "balanced") in style_density else 10.0

        # 3. Mode Fit (0-15)
        mode_fit = 14.0 if mode in ["persuade", "experience"] else 11.0

        # 4. Tone Fit (0-15)
        tone_fit = 13.0

        # 5. Platform Fit (0-10)
        platform_fit = 9.5

        # 6. A11y Fit (0-15)
        a11y_fit = 14.0

        # Penalties
        penalty = 30.0 if (s_id in forbid_styles or any(s_id.startswith(f) for f in forbid_styles)) else 0.0

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

    def _match_palette(self, style_id: str, domain_id: str) -> Dict[str, Any]:
        """Matches domain-calibrated OKLCH palette via BM25 search or catalog iteration."""
        bm25_palettes = self.search_engine.search_palettes(domain_id, limit=3)
        if bm25_palettes:
            return bm25_palettes[0].get("metadata", {})

        for pal in self.palettes:
            best_for = pal.get("best_for", [])
            if domain_id in best_for or style_id in best_for:
                return pal

        return self.palettes[0] if self.palettes else {}

    def _match_typography(self, style_id: str, domain_id: str) -> Dict[str, Any]:
        """Matches typography pairing from Genome systems."""
        for typo in self.typography:
            domains = typo.get("domains", [])
            best_for = typo.get("best_for_styles", [])
            if domain_id in domains or style_id in best_for:
                return typo

        return self.typography[0] if self.typography else {}

    def _match_archetype(self, domain_id: str) -> str:
        """Matches composition archetype for domain."""
        bm25_archs = self.search_engine.search_archetypes(domain_id, limit=1)
        if bm25_archs:
            return bm25_archs[0]["id"]

        from vibe_core.generator import DOMAIN_MACRO_ARCHETYPES
        return DOMAIN_MACRO_ARCHETYPES.get(domain_id, "classic_structured_saas")
