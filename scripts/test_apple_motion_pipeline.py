#!/usr/bin/env python3
"""
scripts/test_apple_motion_pipeline.py — End-to-end verification of Apple Cupertino styling,
Director style override detection, and AutoRefiner motion defect healing.
"""

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from vibe_core.director import DesignDirector
from vibe_core.generator import InterfaceGenerator
from vibe_core.refiner import AutoRefiner
from vibe_core.physical_critic import PhysicalCritic

def main():
    print("[INFO] Running Apple Cupertino & Motion Pipeline Verification Suite...")
    failures = []

    # 1. Verify Director automatic style selection on Apple prompts
    director = DesignDirector()
    prompt_en = "Build an audio workstation tool with Apple Cupertino design language"
    intent_en = director.infer_intent(prompt_en)
    if intent_en.get("selected_style") != "apple_cupertino":
        failures.append(f"Step 1 Failed: Expected 'apple_cupertino' style, got '{intent_en.get('selected_style')}' for prompt '{prompt_en}'")
    else:
        print("  [PASS] Step 1a: Director correctly mapped 'Apple Cupertino' prompt to 'apple_cupertino' style")

    prompt_fa = "یک داشبورد مدیریت مالی با طرح اپل بساز"
    intent_fa = director.infer_intent(prompt_fa)
    if intent_fa.get("selected_style") != "apple_cupertino":
        failures.append(f"Step 1 Failed: Expected 'apple_cupertino' style, got '{intent_fa.get('selected_style')}' for Persian prompt '{prompt_fa}'")
    else:
        print("  [PASS] Step 1b: Director correctly mapped Persian 'طرح اپل' to 'apple_cupertino' style")

    # 2. Verify Generator produces Apple Cupertino layout geometry
    generator = InterfaceGenerator()
    apple_decision = {
        "genome": {
            "domain": "audio_production",
            "platform": {"rtl_support": False}
        },
        "intent": {
            "product_domain": "audio_production",
            "selected_style": "apple_cupertino",
            "language": ["en"]
        },
        "selected_style": "apple_cupertino"
    }
    apple_tsx = generator.generate_react_tsx(apple_decision)
    if "rounded-[28px]" not in apple_tsx or "#0071e3" not in apple_tsx:
        failures.append("Step 2 Failed: Generated React TSX missing Apple Cupertino styling cues (rounded-[28px] or #0071e3)")
    else:
        print("  [PASS] Step 2: Generator rendered authentic Apple Cupertino squircle geometry and System Blue CTA")

    # 3. Verify AutoRefiner surgical repair of motion defects
    refiner = AutoRefiner(enable_physical_browser=False)
    defective_html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    .card {
      transition: all;
      transform: scale(0);
    }
  </style>
</head>
<body>
  <h1>Test Title</h1>
  <div class="card">Defective Motion</div>
</body>
</html>"""

    refined_html, final_report = refiner.refine(defective_html, apple_decision)
    if "transition: all" in refined_html:
        failures.append("Step 3 Failed: 'transition: all' was not repaired by AutoRefiner")
    if "scale(0)" in refined_html:
        failures.append("Step 3 Failed: 'scale(0)' was not repaired by AutoRefiner")
    if "@media (prefers-reduced-motion" not in refined_html:
        failures.append("Step 3 Failed: prefers-reduced-motion was not injected by AutoRefiner")

    if not failures:
        print("  [PASS] Step 3: AutoRefiner successfully healed transition: all, scale(0), and missing reduced-motion guard")

    if failures:
        print("\n[FAIL] Pipeline Verification Failures:", file=sys.stderr)
        for f in failures:
            print(f"  - {f}", file=sys.stderr)
        return 1

    print("\n[SUCCESS] Apple Cupertino & Motion Ergonomics Pipeline 100% Verified (3/3).")
    return 0

if __name__ == "__main__":
    sys.exit(main())
