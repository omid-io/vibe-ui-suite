"""
vibe_core — Vibe UI Suite v6.0.0 Architecture Engine
Autonomous Design Decision Engine, Director, Recommendation & Genome
"""

from vibe_core.constants import (
    MAX_BLUR_SURFACES,
    HARD_MIN_TOUCH_PX,
    RECOMMENDED_TOUCH_PX,
    MIN_WCAG_AA_CONTRAST_NORMAL,
    MIN_WCAG_AA_CONTRAST_LARGE,
    MAX_REFINEMENT_ITERATIONS,
    MAX_DEFECTS_IN_CORRECTION_PROMPT,
)

__version__ = "6.0.0"

__all__ = [
    "MAX_BLUR_SURFACES",
    "HARD_MIN_TOUCH_PX",
    "RECOMMENDED_TOUCH_PX",
    "MIN_WCAG_AA_CONTRAST_NORMAL",
    "MIN_WCAG_AA_CONTRAST_LARGE",
    "MAX_REFINEMENT_ITERATIONS",
    "MAX_DEFECTS_IN_CORRECTION_PROMPT",
    "__version__",
]
