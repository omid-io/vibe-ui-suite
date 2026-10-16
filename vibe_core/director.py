"""
vibe_core.director — Design Director Module
Autonomous intent extraction, domain blueprint alignment, project stack sensing,
confidence estimation, and autonomous best-in-class fallback without interrogation halts.
"""

import json
import re
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

from vibe_core.stack_sensor import ProjectStackSensor

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"

import unicodedata

def normalize_text(text: str) -> str:
    """Normalizes prompt text for robust semantic matching."""
    if not text:
        return ""
    # Unicode NFKC normalization
    text = unicodedata.normalize("NFKC", text)
    text = text.strip().lower()
    text = re.sub(r"[^\w\s]", " ", text)
    return " ".join(text.split())

DIVERSE_FALLBACK_ARCHETYPES = [
    {
        "id": "creative_portfolio_agency",
        "style": "claymorphism",
        "reason": "entropy_diversity:creative_agency"
    },
    {
        "id": "ai_developer_platform",
        "style": "apple-glass",
        "reason": "entropy_diversity:ai_platform"
    },
    {
        "id": "crypto_trading_web3",
        "style": "bento-grid",
        "reason": "entropy_diversity:crypto_web3"
    },
    {
        "id": "media_editorial_magazine",
        "style": "minimalism",
        "reason": "entropy_diversity:editorial_magazine"
    },
    {
        "id": "devops_cloud_terminal",
        "style": "cyberpunk",
        "reason": "entropy_diversity:devops_terminal"
    },
    {
        "id": "general_modern_saas",
        "style": "clean-stripe",
        "reason": "entropy_diversity:modern_saas"
    },
    {
        "id": "bold_consumer_app",
        "style": "neubrutalism",
        "reason": "entropy_diversity:bold_consumer"
    },
    {
        "id": "tactile_hardware_studio",
        "style": "neumorphism",
        "reason": "entropy_diversity:hardware_studio"
    }
]

class DesignDirector:
    def __init__(self, data_dir: Optional[Path] = None):
        self.data_dir = data_dir or DATA_DIR
        self.taxonomy = self._load_taxonomy()
        self.blueprints = self._load_blueprints()

    def _load_taxonomy(self) -> List[Dict[str, Any]]:
        tax_path = self.data_dir / "taxonomy.json"
        if not tax_path.exists():
            return []
        try:
            with open(tax_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("domains", [])
        except Exception:
            return []

    def _load_blueprints(self) -> Dict[str, Any]:
        bp_path = self.data_dir / "domain_blueprints.json"
        if not bp_path.exists():
            return {}
        try:
            with open(bp_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("domains", {})
        except Exception:
            return {}

    def infer_intent(self, prompt: str, user_overrides: Optional[Dict[str, Any]] = None, project_dir: Optional[Path] = None) -> Dict[str, Any]:
        """
        Infers DesignIntentContract from natural language user prompt,
        auto-sensing project stack, domain blueprints, and autonomous best-in-class defaults.
        """
        norm_prompt = normalize_text(prompt)
        user_overrides = user_overrides or {}

        matched_domain, confidence_score, match_reasons = self._match_domain(norm_prompt)
        detected_mode = self._detect_product_mode(norm_prompt, matched_domain)

        # Autonomously scan project stack context
        stack_sensor = ProjectStackSensor(project_dir)
        stack_profile = stack_sensor.scan()

        # Retrieve domain blueprint
        domain_id = matched_domain["id"]
        blueprint = self.blueprints.get(domain_id, {})

        # Autonomous Ambiguity Handling (Zero-Interrogation Protocol)
        if confidence_score >= 0.80:
            ambiguity_status = "low_ambiguity"
            clarification_needed = False
            candidate_directions = []
        elif confidence_score >= 0.50:
            ambiguity_status = "medium_ambiguity"
            clarification_needed = False
            candidate_directions = self._generate_candidate_directions(matched_domain)
        else:
            # Autonomous Best-in-Class Fallback — NEVER halt vibe coding with clarification questions
            ambiguity_status = "autonomous_best_in_class_fallback"
            clarification_needed = False
            candidate_directions = self._generate_candidate_directions(matched_domain)

        # Script and direction detection (RTL support for Arabic, Hebrew, Persian, Urdu)
        has_rtl_script = bool(re.search(r"[\u0590-\u08FF]", prompt))
        language = "fa" if any(c in prompt for c in ["پ", "چ", "گ", "ژ"]) else ("ar" if bool(re.search(r"[\u0600-\u06FF]", prompt)) else ("he" if bool(re.search(r"[\u0590-\u05FF]", prompt)) else "en"))
        languages = [language, "en"] if has_rtl_script else ["en"]

        lower_prompt = prompt.lower()

        # Explicit style override detection across 11 paradigms
        style_override = None
        if any(w in lower_prompt for w in ["claymorphism", "clay"]):
            style_override = "claymorphism"
        elif any(w in lower_prompt for w in ["apple", "cupertino", "ios", "macos", "glass", "glassmorphism"]):
            style_override = "apple-glass"
        elif any(w in lower_prompt for w in ["neumorphism", "neumorphic", "soft emboss"]):
            style_override = "neumorphism"
        elif any(w in lower_prompt for w in ["neubrutalism", "brutalist"]):
            style_override = "neubrutalism"
        elif any(w in lower_prompt for w in ["bento", "bentogrid"]):
            style_override = "bento-grid"
        elif any(w in lower_prompt for w in ["cyberpunk", "matrix", "neon"]):
            style_override = "cyberpunk"
        elif any(w in lower_prompt for w in ["bauhaus"]):
            style_override = "bauhaus"
        elif any(w in lower_prompt for w in ["retrowave", "synthwave"]):
            style_override = "retrowave"
        elif any(w in lower_prompt for w in ["swiss", "editorial", "minimal", "minimalism"]):
            style_override = "minimalism"
        elif any(w in lower_prompt for w in ["y2k", "retro"]):
            style_override = "y2k-retro"
        elif any(w in lower_prompt for w in ["stripe", "clean_stripe"]):
            style_override = "clean-stripe"
        elif any(w in lower_prompt for w in ["terminal", "hud"]):
            style_override = "cyberpunk"

        # Entropy Diversity: if confidence is low or ambiguity is high and no explicit style is given
        entropy_active = any("entropy_diversity" in str(r) for r in match_reasons)
        if entropy_active and not style_override and "selected_style" not in user_overrides:
            entropy_seed = sum(ord(c) for c in norm_prompt) if norm_prompt else 0
            pick = DIVERSE_FALLBACK_ARCHETYPES[entropy_seed % len(DIVERSE_FALLBACK_ARCHETYPES)]
            chosen_style = pick["style"]
        else:
            chosen_style = user_overrides.get("selected_style") or style_override or matched_domain.get("recommended_styles", ["claymorphism"])[0]

        # Strict Light-First Mandate & Anti-Dark-Bias Invariant:
        # Default canvas is ALWAYS Vibrant Light unless:
        # 1. The prompt explicitly requests dark mode ("dark", "black", "night", "darkmode").
        # 2. The chosen style is inherently dark (e.g. linear_dark, cyberpunk, apple-glass, retrowave, bento-grid, data_dense_terminal).
        # In all other cases, theme_strategy must be "light" (with dual_theme dark toggle support).
        prompt_requests_dark = any(w in lower_prompt for w in ["dark", "black", "night", "darkmode", "dark-mode"])
        style_is_inherently_dark = chosen_style in ["linear_dark", "cyberpunk", "apple-glass", "retrowave", "bento-grid", "data_dense_terminal", "cyber_terminal", "midnight_executive", "linear_hud"]
        
        if user_overrides.get("theme_bias"):
            theme_strategy = user_overrides["theme_bias"]
        elif prompt_requests_dark or style_is_inherently_dark:
            theme_strategy = "dark"
        else:
            theme_strategy = "light"

        # Hard constraints extraction
        hard_constraints = [
            "WCAG AA contrast >= 4.5:1 (Target AAA >= 7:1 for text)",
            "Zero horizontal overflow on 320px/375px/390px",
            "Touch targets >= 44px (Minimum accessible tap area)",
            "Zero raw unicode emojis in UI (Inline SVGs with stroke='currentColor' only)",
            "Interactive buttons and switches must have real functional React state",
            "Dual-theme support: Light mode as default with elegant dark mode toggle"
        ]
        if has_rtl_script:
            hard_constraints.append("RTL punctuation and numerical isolation via <bdi>")

        # Wireframe-First Thinking: Pre-compute 3-step spatial skeleton
        section_flow = blueprint.get("section_flow", [
            {"id": "hero", "name": "Hero Section", "type": "split_hero"},
            {"id": "features", "name": "Core Features", "type": "bento_grid"},
            {"id": "footer", "name": "Footer Hub", "type": "standard_footer"}
        ])

        # Research Hook: autonomous lookup guidance if confidence is modest
        research_hook = {
            "should_research": confidence_score < 0.60,
            "suggested_query": f"{matched_domain.get('name_en', 'Modern Web')} UI UX trends 2026 Dribbble Mobbin"
        }

        # Construct Comprehensive DesignIntentContract
        intent = {
            "product_domain": user_overrides.get("product_domain") or domain_id,
            "selected_style": chosen_style,
            "entropy_diversity": {
                "active": entropy_active,
                "chosen_style": chosen_style,
                "entropy_score": round(((sum(ord(c) for c in norm_prompt) if norm_prompt else 0) % 100) / 100, 2)
            },
            "audience": {
                "type": matched_domain.get("name_en", "General Audience"),
                "technical_level": "expert" if "terminal" in domain_id or "devops" in domain_id else "general",
                "primary_device": "mobile" if matched_domain.get("density") == "airy" else "cross_platform"
            },
            "product_mode": user_overrides.get("product_mode") or detected_mode,
            "business_goal": f"Deliver high-conversion, masterpiece experience for {matched_domain['name_en']}",
            "visual_energy": matched_domain.get("visual_energy", "calm_restrained"),
            "density": user_overrides.get("density") or matched_domain.get("density", "balanced"),
            "theme_strategy": theme_strategy,
            "theme_mandate": {
                "primary_theme": theme_strategy,
                "is_light_first": theme_strategy == "light",
                "dual_theme_toggle_required": True,
                "reason": "explicit_request" if prompt_requests_dark else ("inherently_dark_archetype" if style_is_inherently_dark else "strict_vibrant_light_default")
            },
            "unrushed_generation_budget": {
                "mode": "deliberate_deep_craft",
                "max_refinement_passes": 5,
                "asset_curation_priority": "bespoke_or_generated",
                "rush_to_deliver": False
            },
            "creative_assets": {
                "hero_ambient_video_eligible": any(w in lower_prompt for w in ["creative", "showcase", "hero", "video", "modern"]),
                "video_loop_params": "autoplay muted loop playsinline opacity-20 pointer-events-none"
            },
            "trend_first_pipeline": {
                "step_1": "harvest_trends_and_patterns_from_dribbble_figma_galaxy",
                "step_2": "map_available_tools_and_micro_interactions_to_match_trend",
                "step_3": "implement_light_canvas_with_dual_theme_and_living_physics",
                "step_4": "multimodal_and_dom_audit_before_delivery"
            },
            "platform": ["mobile", "tablet", "desktop"],
            "language": language,
            "languages": languages,
            "language_direction": "rtl" if has_rtl_script else "ltr",
            "confidence": {
                "overall": confidence_score,
                "domain": confidence_score,
                "audience": 0.85,
                "product_mode": 0.90
            },
            "ambiguity_status": ambiguity_status,
            "clarification_needed": clarification_needed,
            "candidate_directions": candidate_directions,
            "hard_constraints": hard_constraints,
            "blueprint": {
                "signature_widget": blueprint.get("signature_widget", {}),
                "layout_flavors": blueprint.get("layout_flavors", []),
                "ambient_motion": blueprint.get("ambient_motion", {}),
                "mock_data": blueprint.get("mock_data", {}).get(language, blueprint.get("mock_data", {}).get("en", {}))
            },
            "wireframe_skeleton": [s["name"] for s in section_flow],
            "research_hook": research_hook,
            "stack_profile": stack_profile,
            "soft_preferences": [
                f"Prioritize {theme_strategy} mode based on Light-First Mandate and domain psychology",
                f"Recommended style family: {chosen_style}",
                f"Format output as {stack_profile['recommendation']['file_extension']} ({stack_profile['recommendation']['tailwind_syntax']})"
            ],
            "provenance": {
                "product_domain": "user_explicit" if "product_domain" in user_overrides else "inferred",
                "product_mode": "user_explicit" if "product_mode" in user_overrides else "inferred",
                "confidence": "system_policy_v3_2"
            }
        }
        return intent

    def _match_domain(self, text: str) -> Tuple[Dict[str, Any], float, List[str]]:
        """Matches normalized prompt text against taxonomy strong signals, aliases, and negative disambiguation."""
        best_domain = None
        best_score = 0.05
        reasons = []

        tokens = set(text.split())
        stems = set(tokens)
        for t in tokens:
            for suffix in ['s', 'es', 'ing', 'ed']:
                if len(t) > len(suffix) + 2 and t.endswith(suffix):
                    stems.add(t[:-len(suffix)])

        for domain in self.taxonomy:
            domain_score = 0.0
            matched_aliases = []

            # Check negative disambiguation signals first
            is_negated = False
            for neg in domain.get("negative_signals", []):
                norm_neg = normalize_text(neg)
                if norm_neg and norm_neg in text:
                    is_negated = True
                    break
            if is_negated:
                continue

            # Exact ID / Name match
            if domain["id"].replace("_", " ") in text:
                domain_score += 0.95
                matched_aliases.append(domain["id"])

            # 1. Strong multi-word or distinct signals
            for sig in domain.get("strong_signals", []):
                norm_sig = normalize_text(sig)
                sig_words = norm_sig.split()
                if len(sig_words) == 1:
                    if norm_sig in tokens or norm_sig in stems:
                        domain_score += 0.85
                        matched_aliases.append(sig)
                        break
                else:
                    if norm_sig in text:
                        domain_score += 0.85
                        matched_aliases.append(sig)
                        break
                    if all(w in stems for w in sig_words):
                        domain_score += 0.70
                        matched_aliases.append(sig)
                        break

            # 2. Aliases and secondary signals
            for alias in domain.get("aliases", []):
                norm_alias = normalize_text(alias)
                alias_words = norm_alias.split()
                if len(alias_words) == 1:
                    if norm_alias in tokens or norm_alias in stems:
                        domain_score += 0.35
                        matched_aliases.append(alias)
                else:
                    if norm_alias in text:
                        domain_score += 0.35
                        matched_aliases.append(alias)

            # Downweight generic SaaS fallback unless explicitly matched
            if domain["id"] == "general_modern_saas":
                domain_score *= 0.70

            # Cap score to 0.98 max for non-exact overrides
            domain_score = min(0.98, domain_score)

            if domain_score > best_score:
                best_score = domain_score
                best_domain = domain
                reasons = matched_aliases

        if not best_domain or best_score < 0.20:
            # Entropy Diversity: avoid falling back to generic SaaS when confidence is low or input is ambiguous
            entropy_seed = sum(ord(c) for c in text) if text else 0
            pick = DIVERSE_FALLBACK_ARCHETYPES[entropy_seed % len(DIVERSE_FALLBACK_ARCHETYPES)]
            fallback = next((d for d in self.taxonomy if d["id"] == pick["id"]), None)
            if not fallback:
                fallback = next((d for d in self.taxonomy if d["id"] == "general_modern_saas"), self.taxonomy[0] if self.taxonomy else {})
            actual_score = round(best_score, 2) if best_domain else 0.0
            return fallback, actual_score, [pick["reason"], "entropy_diversity_applied"]

        return best_domain, best_score, reasons

    def _detect_product_mode(self, text: str, domain: Dict[str, Any]) -> str:
        """Determines product mode from keywords or domain primary mode."""
        operate_keywords = ["dashboard", "داشبورد", "پنل", "panel", "admin", "ادمین", "ترید", "trading", "console", "مدیریت", "orderbook"]
        read_keywords = ["doc", "docs", "مستندات", "مقاله", "blog", "وبلاگ", "آموزش", "learning", "article"]
        experience_keywords = ["portfolio", "نمونه کار", "showcase", "game", "بازی", "event", "creative"]

        for kw in operate_keywords:
            if kw in text:
                return "operate"
        for kw in read_keywords:
            if kw in text:
                return "read"
        for kw in experience_keywords:
            if kw in text:
                return "experience"

        return domain.get("primary_mode", "persuade")

    def _generate_candidate_directions(self, domain: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generates 3 human-readable directions under medium/high ambiguity."""
        styles = domain.get("recommended_styles", ["clean_stripe", "minimal_swiss", "quiet_luxury"])
        candidates = []
        labels = [
            ("A (Recommended)", "Editorial Prestige & Calm Restraint", "Focuses on high trust and understated elegance"),
            ("B", "Crisp Corporate & Structured SaaS", "Focuses on clarity, metrics, and conversion speed"),
            ("C", "Approachable Humanist & Friendly Warmth", "Focuses on warmth, empathy, and accessibility")
        ]
        for i, style in enumerate(styles[:3]):
            lbl, title, desc = labels[i]
            candidates.append({
                "id": style,
                "label": f"{lbl}: {title}",
                "description": desc,
                "tradeoff": f"Applies {style} visual geometry with optimized domain priors."
            })
        return candidates
