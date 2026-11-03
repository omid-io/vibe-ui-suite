#!/usr/bin/env python3
"""
vibe_core/trend_hunter.py — Dual Trend & High-Star UI Pattern Explorer
Vibe UI Suite v6.4.2

Discovers and filters world-class UI patterns based on verified popularity:
1. GitHub Trending UI repositories (>10k stars) via public API.
2. Uiverse Galaxy micro-interactions filtered by top ratings / likes.
3. Godly / Awwwards curated design paradigms.
"""

from __future__ import annotations

import json
import urllib.request
import urllib.error
from pathlib import Path
from typing import Any, Dict, List, Optional

from vibe_core.galaxy_engine import GalaxyEngine

ROOT_DIR = Path(__file__).resolve().parent.parent

# Benchmark elite repositories with proven world-class design systems
CURATED_ELITE_REPOS = [
    {
        "name": "shadcn/ui",
        "stars": "75k+",
        "paradigm": "Radix primitives, Tailwind CSS tokens, accessible interactive states",
        "recommended_for": ["dashboard", "saas", "clean_business", "settings"]
    },
    {
        "name": "aceternity/ui",
        "stars": "20k+",
        "paradigm": "Spring physics, liquid glow cards, 3D perspective tilt, canvas animations",
        "recommended_for": ["luxury", "hero_showcase", "creative_agency", "fintech"]
    },
    {
        "name": "magicui/design",
        "stars": "15k+",
        "paradigm": "Bento grids, animated beam connectors, dynamic dock bars, marquee proof",
        "recommended_for": ["bento_matrix", "developer_tools", "ai_platform"]
    },
    {
        "name": "tremor/tremor",
        "stars": "16k+",
        "paradigm": "High-density operational dashboards, micro-sparklines, KPI callout metrics",
        "recommended_for": ["analytics", "crypto_trading", "enterprise_data"]
    }
]

class TrendHunter:
    """Discovers and structures top-trending UI patterns from internal and external sources."""

    def __init__(self):
        self.galaxy = GalaxyEngine()

    def search_github_top_starred(self, query: str, limit: int = 4) -> List[Dict[str, Any]]:
        """
        Queries public GitHub API for repositories related to query sorted by star count.
        Falls back to CURATED_ELITE_REPOS if offline or rate-limited.
        """
        api_url = f"https://api.github.com/search/repositories?q={urllib.parse.quote(query)}+topic:ui+stars:>5000&sort=stars&order=desc&per_page={limit}"
        headers = {
            "User-Agent": "Vibe-UI-TrendHunter/6.5.0",
            "Accept": "application/vnd.github.v3+json"
        }
        req = urllib.request.Request(api_url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                items = data.get("items", [])
                results = []
                for item in items[:limit]:
                    results.append({
                        "name": item.get("full_name"),
                        "stars": item.get("stargazers_count"),
                        "description": item.get("description", ""),
                        "url": item.get("html_url"),
                        "topics": item.get("topics", [])
                    })
                if results:
                    return results
        except Exception:
            pass

        # Return relevant curated elite models matching query domain
        q_lower = query.lower()
        matched = [r for r in CURATED_ELITE_REPOS if any(tag in q_lower for tag in r["recommended_for"])]
        return matched if matched else CURATED_ELITE_REPOS[:limit]

    def search_galaxy_top_liked(self, category_or_query: str, limit: int = 4) -> List[Dict[str, Any]]:
        """
        Retrieves top-liked micro-interactions from the local Galaxy dataset.
        """
        if not self.galaxy.ensure_galaxy_dataset():
            return []

        results = self.galaxy.search(category_or_query, limit=limit)
        return results

    def curate_trend_package(self, domain: str, style_preference: Optional[str] = None) -> Dict[str, Any]:
        """
        Builds a comprehensive Trend Package containing:
        - High-star architectural paradigms.
        - Verified micro-interactions (buttons, cards, forms) with clean HTML/CSS.
        - Visual layout guidance.
        """
        gh_trends = self.search_github_top_starred(domain)
        galaxy_buttons = self.search_galaxy_top_liked("button", limit=2)
        galaxy_cards = self.search_galaxy_top_liked("card", limit=2)

        return {
            "domain": domain,
            "target_style": style_preference or "Modern High-End",
            "top_starred_benchmarks": gh_trends,
            "curated_components": {
                "buttons": galaxy_buttons,
                "cards": galaxy_cards
            },
            "recommended_spatial_rules": [
                "Strict 8px spacing rhythm (p-4, p-6, p-8)",
                "Bento grid with 2:1 and 1:1 asymmetric aspect ratios",
                "Subtle borders (border-white/10 or border-black/10) with 1px backdrop-blur glass"
            ]
        }
