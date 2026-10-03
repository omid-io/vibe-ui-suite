"""
vibe_core.constants — Centralized Design & Verification Policies (Single Source of Truth)

All operational thresholds, compliance limits, and architectural budgets must be defined here
to prevent policy drift across critic, verifier, refiner, benchmark, and CLI modules.
"""

# Visual & GPU Composite Performance Budgets
MAX_BLUR_SURFACES: int = 8
"""Maximum allowable backdrop-filter / blur surfaces before flagging GPU composite blowout (calibrated for modern hardware, floating docks, and luxury glassmorphism)."""

# WCAG & Accessibility Compliance Thresholds
HARD_MIN_TOUCH_PX: int = 24
"""Minimum touch target dimension in pixels required by WCAG 2.2 Success Criterion 2.5.8 (AA)."""

RECOMMENDED_TOUCH_PX: int = 44
"""Recommended touch target dimension in pixels per Apple iOS & Google Material mobile HIG."""

MIN_WCAG_AA_CONTRAST_NORMAL: float = 4.5
"""Minimum luminance contrast ratio for standard text under WCAG 2.2 AA."""

MIN_WCAG_AA_CONTRAST_LARGE: float = 3.0
"""Minimum luminance contrast ratio for large text (>= 18pt or 14pt bold) and graphical UI controls."""

# Refinement & Self-Healing Loop Limits
MAX_REFINEMENT_ITERATIONS: int = 2
"""Bounded maximum iteration count for AutoRefiner and SelfHealingLoop to prevent infinite loops."""

MAX_DEFECTS_IN_CORRECTION_PROMPT: int = 5
"""Maximum defects included in a generated LLM correction prompt to avoid token bloat."""

# Aesthetic & Anti-Slop Thresholds (v3.2.0)
MAX_SPARKLE_ICONS: int = 1
"""Maximum allowable AI sparkle icons before flagging generic AI-slop trope."""

SLOP_GENERIC_GRADIENT_PENALTY: int = 6
"""Score deduction when clichéd purple/indigo gradients are detected."""
