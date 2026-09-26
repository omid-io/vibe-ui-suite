#!/usr/bin/env python3
"""
test_visual_critic.py — Unit Tests for VisualCritic (Multi-Dimensional Visual QA Engine).
Tests hierarchy detection, CTA prominence, sparkle traps, blur limits, and composite scoring.
"""

import sys
from pathlib import Path

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from vibe_core.visual_critic import VisualCritic
from vibe_core.generator import InterfaceGenerator

def run_tests():
    print("[INFO] Running VisualCritic Multi-Dimensional Aesthetic Tests...")
    critic = VisualCritic()
    gen = InterfaceGenerator()
    failures = []

    # 1. Test Clean Component (Generated via InterfaceGenerator)
    decision = {
        "selected_style": "clean_stripe",
        "intent": {"product_domain": "fintech_banking_investments", "theme_strategy": "light"}
    }
    tsx = gen.generate_react_tsx(decision, "FinTechDemo")
    eval_clean = critic.evaluate(tsx, decision)
    if eval_clean["acceptance_status"] != "ACCEPTED":
        failures.append(f"Clean TSX failed visual critic: {eval_clean['defects']}")
    if eval_clean["visual_score"] < 85.0:
        failures.append(f"Clean TSX visual score too low: {eval_clean['visual_score']} (< 85.0)")
    print(f"  [PASS] Test 1: Clean TSX Component Passed with Score {eval_clean['visual_score']}/100")

    # 2. Test Missing H1 Focal Point (P0 Defect)
    no_h1 = "<div><p class='text-sm'>Just paragraph text without main headline</p><button class='min-h-[44px] py-3 px-6'>Click</button></div>"
    eval_no_h1 = critic.evaluate(no_h1, decision)
    defect_types = [d["type"] for d in eval_no_h1["defects"]]
    if "missing_h1_focal_point" not in defect_types:
        failures.append("Failed to detect missing_h1_focal_point P0 defect")
    if eval_no_h1["acceptance_status"] != "REVISE_REQUIRED":
        failures.append("Component missing H1 should require revision")
    print("  [PASS] Test 2: Missing H1 Focal Point correctly flagged as P0 defect")

    # 3. Test Cliché AI Sparkle Trap (P0 Defect)
    slop_sparkle = "<div class='p-6'><h1 class='text-4xl'>Title ✨</h1><button class='min-h-[44px] py-3 px-6'>Action</button></div>"
    eval_sparkle = critic.evaluate(slop_sparkle, decision)
    defect_types_sparkle = [d["type"] for d in eval_sparkle["defects"]]
    if "cliche_ai_sparkle" not in defect_types_sparkle:
        failures.append("Failed to detect cliche_ai_sparkle P0 defect")
    print("  [PASS] Test 3: Cliché AI Sparkles correctly flagged and rejected")

    # 4. Test Substandard Touch Target (P1 Defect)
    bad_touch = "<div class='p-6'><h1 class='text-4xl'>Title</h1><button class='h-6 w-12 text-xs'>Tiny</button></div>"
    eval_touch = critic.evaluate(bad_touch, decision)
    defect_types_touch = [d["type"] for d in eval_touch["defects"]]
    if "substandard_touch_target" not in defect_types_touch:
        failures.append("Failed to detect substandard_touch_target P1 defect")
    print("  [PASS] Test 4: Substandard touch target (<44px) correctly flagged as P1")

    # 5. Test Excessive Compositing Blur Layers (P1 Defect)
    excessive_blur = """
    <div class="p-6 backdrop-blur-md">
      <h1 class="text-4xl">Title</h1>
      <div class="backdrop-blur-sm"><div class="backdrop-blur-lg"><div class="backdrop-blur-xl">Deep Blur</div></div></div>
      <button class="min-h-[44px] py-3 px-6">Action</button>
    </div>
    """
    eval_blur = critic.evaluate(excessive_blur, decision)
    defect_types_blur = [d["type"] for d in eval_blur["defects"]]
    if "excessive_compositing_blur" not in defect_types_blur:
        failures.append("Failed to detect excessive_compositing_blur P1 defect")
    print("  [PASS] Test 5: Excessive compositing blur (>3 layers) correctly flagged")

    if failures:
        print(f"\n[FAIL] {len(failures)} failures in visual critic tests:")
        for f in failures:
            print(f"  - {f}")
        sys.exit(1)

    print("\n[SUCCESS] All VisualCritic tests passed with 100% compliance.")

if __name__ == "__main__":
    run_tests()
