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
        color = genome.get("color", {})
        radius = genome.get("radius", {})
        motion = genome.get("motion", {})
        typography = genome.get("typography", {})

        accent_color = color.get('accent', 'oklch(0.65 0.09 75)')
        on_primary = "oklch(0.99 0 0)"
        import re
        oklch_match = re.search(r"oklch\(\s*([\d.]+%?)\s+([\d.]+)\s+([\d.]+)", str(accent_color).lower())
        if oklch_match:
            l_str = oklch_match.group(1)
            l_val = float(l_str[:-1]) / 100.0 if l_str.endswith("%") else float(l_str)
            if l_val > 0.62:
                on_primary = "oklch(0.12 0.02 85)"

        css_lines = [
            ":root {",
            f"  --canvas-bg: {color.get('canvas', 'oklch(0.98 0.005 85)')};",
            f"  --surface-bg: {color.get('surface', 'oklch(0.95 0.01 85)')};",
            f"  --accent: {accent_color};",
            f"  --vibe-on-primary: {on_primary};",
            f"  --border-subtle: {color.get('border', 'oklch(0.88 0.01 85)')};",
            f"  --text-primary: {color.get('text', 'oklch(0.20 0.015 60)')};",
            f"  --text-muted: {color.get('muted_text', 'oklch(0.48 0.015 60)')};",
            f"  --radius-base: {radius.get('base', '8px')};",
            f"  --radius-container: {radius.get('container', '12px')};",
            f"  --radius-button: {radius.get('button', '8px')};",
            f"  --font-display: '{typography.get('display_family', 'Inter')}', '{typography.get('persian_family', 'Vazirmatn')}', sans-serif;",
            f"  --font-body: '{typography.get('body_family', 'Inter')}', '{typography.get('persian_family', 'Vazirmatn')}', sans-serif;",
            f"  --motion-lambda: {motion.get('time_constant_lambda', 14)};",
            f"  --transition-duration: {motion.get('duration_ms', 200)}ms;",
            "}"
        ]
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
