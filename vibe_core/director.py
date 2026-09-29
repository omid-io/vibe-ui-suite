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

def normalize_text(text: str) -> str:
    """Normalizes Persian and English text for robust semantic matching."""
    if not text:
        return ""
    text = text.strip().lower()
    # Normalize Arabic/Persian characters
    text = text.replace("ي", "ی").replace("ك", "ک").replace("ة", "ه").replace(" ", " ")
    # Remove punctuation
    text = re.sub(r"[^\w\s\u0600-\u06FF]", " ", text)
    return " ".join(text.split())

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

        # Language detection
        has_persian = bool(re.search(r"[\u0600-\u06FF]", prompt))
        language = ["fa", "en"] if has_persian else ["en"]

        # Smart Lighting / Theme Strategy (Breaking the Dark Mode Bias)
        theme_bias = user_overrides.get("theme_bias") or blueprint.get("theme_bias", "light")

        # Hard constraints extraction
        hard_constraints = [
            "WCAG AA contrast >= 4.5:1 (Target AAA >= 7:1 for text)",
            "Zero horizontal overflow on 320px/375px/390px",
            "Touch targets >= 44px (Minimum accessible tap area)",
            "Zero raw unicode emojis in UI (Inline SVGs with stroke='currentColor' only)",
            "Interactive buttons and switches must have real functional React state"
        ]
        if has_persian:
            hard_constraints.append("RTL punctuation and numerical isolation via <bdi>")
            hard_constraints.append("Vazirmatn / Shabnam Persian web font integration")

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

        # Explicit style override detection
        style_override = None
        lower_prompt = prompt.lower()
        if any(w in lower_prompt for w in ["apple", "cupertino", "ios", "macos", "اپل"]):
            style_override = "apple_cupertino"
        elif any(w in lower_prompt for w in ["neobrutalism", "brutalist", "نئوبروتالیسم"]):
            style_override = "neobrutalism"
        elif any(w in lower_prompt for w in ["swiss", "editorial", "سوئیس"]):
            style_override = "minimal_swiss"
        elif any(w in lower_prompt for w in ["luxury", "obsidian", "لاکچری"]):
            style_override = "quiet_luxury"
        elif any(w in lower_prompt for w in ["glass", "glassmorphism", "شیشه"]):
            style_override = "specular_glass"

        chosen_style = user_overrides.get("selected_style") or style_override or matched_domain.get("recommended_styles", ["clean_stripe"])[0]

        # Construct Comprehensive DesignIntentContract
        intent = {
            "product_domain": user_overrides.get("product_domain") or domain_id,
            "selected_style": chosen_style,
            "audience": {
                "type": matched_domain.get("name_en", "General Audience"),
                "technical_level": "expert" if "terminal" in domain_id or "devops" in domain_id else "general",
                "primary_device": "mobile" if matched_domain.get("density") == "airy" else "cross_platform"
            },
            "product_mode": user_overrides.get("product_mode") or detected_mode,
            "business_goal": f"Deliver high-conversion, masterpiece experience for {matched_domain['name_en']}",
            "visual_energy": matched_domain.get("visual_energy", "calm_restrained"),
            "density": user_overrides.get("density") or matched_domain.get("density", "balanced"),
            "theme_strategy": theme_bias,
            "platform": ["mobile", "tablet", "desktop"],
            "language": language,
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
                "mock_data": blueprint.get("mock_data", {}).get("fa" if has_persian else "en", {})
            },
            "wireframe_skeleton": [s["name"] for s in section_flow],
            "research_hook": research_hook,
            "stack_profile": stack_profile,
            "soft_preferences": [
                f"Prioritize {theme_bias} mode based on domain psychology",
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
            for suffix in ['های', 'ها', 'ان', 'ات', 'ی', 'ین', 'ترین', 'تر', 's', 'es', 'ing', 'ed']:
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
                if norm_sig in text:
                    domain_score += 0.85
                    matched_aliases.append(sig)
                    break
                sig_tokens = norm_sig.split()
                if len(sig_tokens) > 1 and all(w in stems for w in sig_tokens):
                    domain_score += 0.70
                    matched_aliases.append(sig)
                    break

            # 2. Aliases and secondary signals
            for alias in domain.get("aliases", []):
                norm_alias = normalize_text(alias)
                if norm_alias in text:
                    domain_score += 0.35
                    matched_aliases.append(alias)
                elif norm_alias in stems:
                    domain_score += 0.25
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
            fallback = next((d for d in self.taxonomy if d["id"] == "general_modern_saas"), self.taxonomy[0] if self.taxonomy else {})
            actual_score = round(best_score, 2) if best_domain else 0.0
            return fallback, actual_score, ["fallback_general_modern_saas", "no_matching_taxonomy"]

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
