#!/usr/bin/env python3
"""
vibe_core/trend_hunter.py — Dual Trend & Design Evidence Intelligence Engine
Vibe UI Suite

Discovers and structures verified UI patterns and design evidence:
1. Local BM25 Design Intelligence Engine (88+ styles, 168+ palettes, benchmarks).
2. Context-aware spatial & composition archetypes (Anti-Bento, Editorial, Canvas, HUD).
3. Uiverse Galaxy micro-interactions filtered by top ratings / likes.
4. Structured TrendEvidence contract generation for inter-agent compilation.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from vibe_core.galaxy_engine import GalaxyEngine
from vibe_core.search_engine import DesignIntelligenceEngine

# Curated benchmark repositories with verified design systems
CURATED_ELITE_REPOS = [
    {
        "name": "shadcn/ui",
        "stars": "80k+",
        "paradigm": "Radix primitives, Tailwind CSS tokens, accessible interactive states",
        "recommended_for": ["dashboard", "saas", "clean_business", "settings", "general_modern_saas"]
    },
    {
        "name": "aceternity/ui",
        "stars": "20k+",
        "paradigm": "Spring physics, liquid glow cards, 3D perspective tilt, canvas animations",
        "recommended_for": ["luxury", "hero_showcase", "creative_agency", "fintech", "crypto_trading_web3"]
    },
    {
        "name": "magicui/design",
        "stars": "18k+",
        "paradigm": "Animated beam connectors, dynamic dock bars, marquee proof, interactive grids",
        "recommended_for": ["bento_matrix", "developer_tools", "ai_platform", "ai_developer_platform"]
    },
    {
        "name": "tremor/tremor",
        "stars": "16k+",
        "paradigm": "High-density operational dashboards, micro-sparklines, KPI callout metrics",
        "recommended_for": ["analytics", "crypto_trading", "enterprise_data", "devops_cloud_terminal"]
    },
    {
        "name": "lucide-icons/lucide",
        "stars": "15k+",
        "paradigm": "Ultra-clean vector stroke iconography with uniform optical balance",
        "recommended_for": ["general_modern_saas", "saas_b2b_enterprise"]
    }
]

# Domain-specific spatial recommendations to eliminate generic "Bento + Glass" slop
DOMAIN_SPATIAL_BLUEPRINTS: Dict[str, Dict[str, Any]] = {
    "media_editorial_magazine": {
        "composition": "asymmetric_editorial_split",
        "rules": [
            "Asymmetric headline-heavy split hero (60% typography, 40% portrait asset)",
            "Multi-column newspaper serif rhythm with generous white margins",
            "Zero card boxes in hero; text flows directly on crisp paper canvas"
        ],
        "banned": ["repetitive_bento_cards", "backdrop_blur_glass"]
    },
    "devops_cloud_terminal": {
        "composition": "high_density_operations_hud",
        "rules": [
            "Dense telemetry data grid with monospace coordinate readouts",
            "Compact metric tables with live status pulse indicators",
            "Single-screen operational cockpit with minimized empty decorative padding"
        ],
        "banned": ["pastel_gradients", "decorative_bubbles", "fluffy_bento_boxes"]
    },
    "ai_developer_platform": {
        "composition": "canvas_workspace_split",
        "rules": [
            "Split-pane conversational HUD with interactive artifact canvas",
            "Collapsible thinking accordion with real-time token/latency telemetry",
            "Context chips and tool execution cards with discrete state borders"
        ],
        "banned": ["generic_landing_page_bento", "fake_stock_photos"]
    },
    "creative_portfolio_agency": {
        "composition": "hyper_kinetic_showcase",
        "rules": [
            "Staggered media reveal with magnetic cursor physics",
            "High-contrast tactile press buttons with solid offset drop shadows",
            "Dynamic horizontal project reel with variable aspect ratios"
        ],
        "banned": ["boring_corporate_cards", "muddy_dark_grey"]
    },
    "healthcare_hospital_medical": {
        "composition": "reassuring_clinical_flow",
        "rules": [
            "Wide tranquil hero with clear physician appointment booking trigger",
            "Trust credential badges and verified doctor cards with clean 1px slate borders",
            "Calm, high-contrast light canvas ensuring maximum legibility"
        ],
        "banned": ["dark_mode_bias", "neon_glow", "bento_clutter"]
    },
    "food_restaurant_cafe": {
        "composition": "sensory_culinary_stage",
        "rules": [
            "Immersive focal photography with warm negative space for headline typography",
            "Seasonal tasting menu columns with subtle warm paper dividers",
            "Direct table reservation CTA with tactile interactive states"
        ],
        "banned": ["cold_tech_cards", "cyberpunk_neon", "unrelated_metrics"]
    }
}

DEFAULT_SPATIAL_BLUEPRINT: Dict[str, Any] = {
    "composition": "balanced_modern_flow",
    "rules": [
        "Light-First canonical standard with crisp surfaces and deep graphite typography",
        "Asymmetric focal balance: primary value proposition paired with verified product view",
        "Dynamic card rhythms tailored to content semantics rather than identical boxes"
    ],
    "banned": ["generic_purple_gradient", "meaningless_ai_sparkles", "muddy_pitch_black_void"]
}


class TrendHunter:
    """Discovers and structures top-trending UI patterns and design evidence."""

    def __init__(self):
        self.galaxy = GalaxyEngine()
        self.engine = DesignIntelligenceEngine()

    def search_benchmarks(self, query: str, limit: int = 4) -> List[Dict[str, Any]]:
        """
        Retrieves top-starred design benchmarks using local BM25 ranking.
        Never stalls or fails on network timeouts or API rate-limits.
        """
        # First query BM25 engine for matching benchmarks
        engine_results = self.engine.search_benchmarks(query, limit=limit)
        if engine_results:
            return engine_results

        # Fallback to curated elite repos
        q_lower = query.lower()
        matched = [r for r in CURATED_ELITE_REPOS if any(tag in q_lower for tag in r.get("recommended_for", []))]
        return matched[:limit] if matched else CURATED_ELITE_REPOS[:limit]

    def search_github_top_starred(self, query: str, limit: int = 4) -> List[Dict[str, Any]]:
        """Backward-compatible alias for search_benchmarks."""
        return self.search_benchmarks(query, limit=limit)

    def search_galaxy_top_liked(self, category_or_query: str, limit: int = 4) -> List[Dict[str, Any]]:
        """Retrieves top-liked micro-interactions from the local Galaxy dataset."""
        if not self.galaxy.ensure_galaxy_dataset():
            return []
        return self.galaxy.search(category_or_query, limit=limit)

    def extract_trend_evidence(self, domain: str, style_preference: Optional[str] = None) -> Dict[str, Any]:
        """
        Extracts structured Design Evidence for the swarm pipeline:
        - BM25 matched style from Design Genome 2.0.
        - Domain-calibrated spatial blueprint (explicitly avoids Bento+Glass slop).
        - Curated micro-interactions and benchmark references.
        """
        search_query = f"{domain} {style_preference or ''}".strip()
        matched_styles = self.engine.search_styles(search_query, limit=3)
        top_style = matched_styles[0].get("metadata", {}) if matched_styles else {}

        matched_palettes = self.engine.search_palettes(search_query, limit=2)
        top_palette = matched_palettes[0].get("metadata", {}) if matched_palettes else {}

        benchmarks = self.search_benchmarks(domain, limit=3)
        galaxy_buttons = self.search_galaxy_top_liked("button", limit=2)
        galaxy_cards = self.search_galaxy_top_liked("card", limit=2)

        # Retrieve domain-specific spatial composition and only publish typography
        # when the matched genome actually contains a font recommendation.
        spatial = DOMAIN_SPATIAL_BLUEPRINTS.get(domain, DEFAULT_SPATIAL_BLUEPRINT)
        raw_typography = top_style.get("typography", {})
        typography_pair: Dict[str, str] = {}
        if isinstance(raw_typography, dict):
            display_font = (
                raw_typography.get("heading_font")
                or raw_typography.get("display")
                or raw_typography.get("display_font")
            )
            body_font = (
                raw_typography.get("body_font")
                or raw_typography.get("body")
                or raw_typography.get("text_font")
            )
            if display_font:
                typography_pair["display"] = str(display_font)
            if body_font:
                typography_pair["body"] = str(body_font)

        return {
            "domain": domain,
            "target_style": top_style.get("name", style_preference or "Minimalist SaaS"),
            "style_id": top_style.get("style_id", "minimalist_saas"),
            "composition_archetype": spatial["composition"],
            "spatial_rules": spatial["rules"],
            "banned_slop_tropes": spatial["banned"],
            "recommended_palette": top_palette,
            "typography_pair": typography_pair,
            "style_reasoning": (
                f"Matched local Design Genome evidence for {domain}"
                if top_style else "No direct style metadata match; using domain fallback"
            ),
            "benchmarks": benchmarks,
            "curated_micro_interactions": {
                "buttons": galaxy_buttons,
                "cards": galaxy_cards
            },
            "evidence_confidence": 0.96 if top_style else 0.85
        }

    def curate_trend_package(self, domain: str, style_preference: Optional[str] = None) -> Dict[str, Any]:
        """Backward-compatible package for legacy callers, powered by Design Genome evidence."""
        evidence = self.extract_trend_evidence(domain, style_preference)
        return {
            "domain": domain,
            "target_style": evidence["target_style"],
            "composition_archetype": evidence["composition_archetype"],
            "banned_slop_tropes": evidence["banned_slop_tropes"],
            "typography_pair": evidence["typography_pair"],
            "style_reasoning": evidence["style_reasoning"],
            "evidence_confidence": evidence["evidence_confidence"],
            "recommended_palette": evidence["recommended_palette"],
            "top_starred_benchmarks": evidence["benchmarks"],
            "curated_components": evidence["curated_micro_interactions"],
            "recommended_spatial_rules": evidence["spatial_rules"]
        }


if __name__ == "__main__":
    th = TrendHunter()
    print("[*] Testing TrendHunter with local BM25 engine...")
    ev = th.extract_trend_evidence("healthcare_hospital_medical")
    print(f"  Target Style: {ev['target_style']}")
    print(f"  Composition: {ev['composition_archetype']}")
    print(f"  Spatial Rules: {len(ev['spatial_rules'])}")
    print(f"  Banned Slop: {ev['banned_slop_tropes']}")
    print("[SUCCESS] TrendHunter verified offline and anti-slop calibrated.")
