"""
vibe_core.genome — 19-Parameter Composable Design Genome Engine
Generates and validates typed genome configurations, CSS variables, and Tailwind theme mappings.
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional

ROOT_DIR = Path(__file__).resolve().parent.parent
SCHEMAS_DIR = ROOT_DIR / "schemas"

class DesignGenomeEngine:
    def __init__(self, schemas_dir: Optional[Path] = None):
        self.schemas_dir = schemas_dir or SCHEMAS_DIR

    def to_css_variables(self, genome: Dict[str, Any]) -> str:
        """Converts Design Genome color, radius, and motion tokens into standard CSS variables."""
        tokens = genome.get("tokens", {}) or {}
        color = genome.get("color", {})
        radius = genome.get("radius", {})
        geometry = genome.get("geometry", {})
        motion = genome.get("motion", {})
        typography = genome.get("typography", {})

        accent_color = tokens.get('accent') or color.get('accent', 'oklch(0.65 0.09 75)')
        on_primary = "oklch(0.99 0 0)"
        import re
        oklch_match = re.search(r"oklch\(\s*([\d.]+%?)\s+([\d.]+)\s+([\d.]+)", str(accent_color).lower())
        if oklch_match:
            l_str = oklch_match.group(1)
            l_val = float(l_str[:-1]) / 100.0 if l_str.endswith("%") else float(l_str)
            if l_val > 0.62:
                on_primary = "oklch(0.12 0.02 85)"

        disp_font = typography.get('display_family') or typography.get('heading_font') or typography.get('heading', 'Inter')
        body_font = typography.get('body_family') or typography.get('body_font') or typography.get('body', 'Inter')
        mono_font = typography.get('mono_family') or typography.get('mono_font') or typography.get('mono', 'JetBrains Mono')
        fa_font = typography.get('persian_family', 'Vazirmatn')

        base_radius = geometry.get('border_radius') or geometry.get('radius_base') or radius.get('base', '8px')
        container_radius = geometry.get('container') or radius.get('container', '12px')
        button_radius = geometry.get('button') or radius.get('button', '8px')

        css_lines = [
            ":root {",
            f"  --canvas-bg: {tokens.get('canvas') or color.get('canvas', 'oklch(0.98 0.005 85)')};",
            f"  --surface-bg: {tokens.get('surface') or color.get('surface', 'oklch(0.95 0.01 85)')};",
            f"  --surface-elevated: {tokens.get('surface_elevated', 'oklch(1.00 0.005 85)')};",
            f"  --accent: {accent_color};",
            f"  --accent-hover: {tokens.get('accent_hover', 'oklch(0.51 0.084 75)')};",
            f"  --vibe-on-primary: {on_primary};",
            f"  --border-subtle: {tokens.get('border') or color.get('border', 'oklch(0.88 0.01 85)')};",
            f"  --text-primary: {tokens.get('text_primary') or tokens.get('text') or color.get('text', 'oklch(0.20 0.015 60)')};",
            f"  --text-muted: {tokens.get('text_secondary') or tokens.get('text_muted') or color.get('muted_text', 'oklch(0.48 0.015 60)')};",
            f"  --radius-base: {base_radius};",
            f"  --radius-container: {container_radius};",
            f"  --radius-button: {button_radius};",
            f"  --font-display: '{disp_font}', '{fa_font}', sans-serif;",
            f"  --font-body: '{body_font}', '{fa_font}', sans-serif;",
            f"  --font-mono: '{mono_font}', monospace;",
            f"  --motion-lambda: {motion.get('time_constant_lambda', 14)};",
            f"  --transition-duration: {motion.get('duration_ms', 200)}ms;",
            "}"
        ]

        dark_tokens = tokens.get("dark_oled") or genome.get("secondary_oled") or {}
        if dark_tokens:
            dark_canvas = dark_tokens.get("canvas", "oklch(0.12 0.015 0.0)")
            dark_surface = dark_tokens.get("surface", "oklch(0.17 0.022 0.0)")
            dark_elevated = dark_tokens.get("surface_elevated", "oklch(0.21 0.015 0.0)")
            dark_border = dark_tokens.get("border", "oklch(0.26 0.018 0.0)")
            dark_text = dark_tokens.get("text_primary", "oklch(0.96 0.010 0.0)")
            dark_text_muted = dark_tokens.get("text_secondary", "oklch(0.68 0.008 0.0)")
            dark_accent = dark_tokens.get("accent", "oklch(0.72 0.088 0.0)")
            dark_accent_hover = dark_tokens.get("accent_hover", "oklch(0.79 0.092 0.0)")

            css_lines.extend([
                "",
                ".dark, [data-theme=\"dark\"] {",
                f"  --canvas-bg: {dark_canvas};",
                f"  --surface-bg: {dark_surface};",
                f"  --surface-elevated: {dark_elevated};",
                f"  --border-subtle: {dark_border};",
                f"  --text-primary: {dark_text};",
                f"  --text-muted: {dark_text_muted};",
                f"  --accent: {dark_accent};",
                f"  --accent-hover: {dark_accent_hover};",
                f"  --vibe-on-primary: oklch(0.12 0.02 85);",
                "}"
            ])

        return "\n".join(css_lines)

    def to_tailwind_theme(self, genome: Dict[str, Any]) -> Dict[str, Any]:
        """Generates Tailwind theme extension object from genome."""
        color = genome.get("color", {})
        radius = genome.get("radius", {})
        return {
            "colors": {
                "vibe-canvas": color.get("canvas"),
                "vibe-surface": color.get("surface"),
                "vibe-accent": color.get("accent"),
                "vibe-border": color.get("border"),
                "vibe-text": color.get("text"),
                "vibe-muted": color.get("muted_text")
            },
            "borderRadius": {
                "vibe-base": radius.get("base"),
                "vibe-container": radius.get("container"),
                "vibe-button": radius.get("button")
            }
        }
