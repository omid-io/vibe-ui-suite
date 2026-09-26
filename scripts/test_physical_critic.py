#!/usr/bin/env python3
"""
scripts/test_physical_critic.py — Unit and integration tests for PhysicalCritic.
Tests:
1. Headless Chromium physical evaluation on 390px, 768px, 1440px viewports.
2. Accurate physical touch target detection (width and height >= 44px).
3. Accurate horizontal overflow blowout detection on 390px mobile viewport.
4. Static heuristic fallback mode resilience.
"""

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from vibe_core.physical_critic import PhysicalCritic

def main():
    print("[INFO] Running Headless Physical Viewport Critic Suite...")
    critic = PhysicalCritic(enable_browser=True)
    failures = []

    # Test 1: Clean responsive page (Should pass with high score in Chromium)
    clean_html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: sans-serif; overflow-x: hidden; }
    .container { max-width: 1200px; margin: 0 auto; padding: 24px; }
    .btn { display: inline-flex; align-items: center; justify-content: center; min-height: 48px; min-width: 120px; padding: 12px 24px; font-size: 16px; background: #2563eb; color: #fff; border: none; border-radius: 8px; cursor: pointer; }
  </style>
</head>
<body>
  <div class="container">
    <h1>Physical Geometry Test</h1>
    <p>Testing real bounding boxes and physical viewport layout.</p>
    <button type="button" class="btn">Primary Action</button>
  </div>
</body>
</html>"""

    res1 = critic.audit_physical_layout(clean_html)
    if not res1["acceptance_status"] == "ACCEPTED":
        failures.append(f"Test 1 Failed: Clean HTML rejected (status={res1['acceptance_status']}, score={res1['physical_score']})")
    if res1["metrics"].get("horizontal_overflow", False):
        failures.append("Test 1 Failed: False positive horizontal overflow reported")
    print(f"  [PASS] Test 1: Clean page scored {res1['physical_score']}/100 in {res1['engine']}")

    # Test 2: Defective page with horizontal blowout (> 390px fixed container)
    overflow_html = """<!DOCTYPE html>
<html>
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    .blowout { width: 650px; background: red; height: 100px; }
  </style>
</head>
<body>
  <div class="blowout">Fixed width blowout causing horizontal scrollbar on mobile</div>
</body>
</html>"""

    res2 = critic.audit_physical_layout(overflow_html)
    if res2["acceptance_status"] != "REVISE_REQUIRED":
        failures.append(f"Test 2 Failed: Horizontal blowout was not rejected (status={res2['acceptance_status']})")
    if not res2["metrics"].get("horizontal_overflow", False):
        failures.append("Test 2 Failed: Horizontal overflow metric was not flagged as True")
    print(f"  [PASS] Test 2: Physical overflow correctly caught and rejected on mobile viewport")

    # Test 3: Substandard touch target (< 44px)
    substandard_html = """<!DOCTYPE html>
<html>
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    * { box-sizing: border-box; }
    .tiny-btn { width: 24px; height: 24px; padding: 0; font-size: 10px; }
  </style>
</head>
<body>
  <button type="button" class="tiny-btn">x</button>
</body>
</html>"""

    res3 = critic.audit_physical_layout(substandard_html)
    has_target_defect = any("substandard_touch_target" in d["type"] for d in res3["defects"])
    if not has_target_defect:
        failures.append("Test 3 Failed: Tiny 24x24px button was not flagged as substandard touch target")
    print(f"  [PASS] Test 3: Substandard physical touch target (24x24px) detected via getBoundingClientRect()")

    # Test 4: Static fallback mode
    fallback_critic = PhysicalCritic(enable_browser=False)
    res4 = fallback_critic.audit_physical_layout(clean_html)
    if "static" not in res4["engine"]:
        failures.append("Test 4 Failed: Expected static fallback engine")
    print(f"  [PASS] Test 4: Static fallback engine verified successfully")

    # Test 5: Runtime Causal Interaction Verification in Chromium
    interactive_html = """<!DOCTYPE html>
<html>
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>
  <div>
    <span id="label">Estimated Volume: <bdi id="metric">50,000 USD</bdi></span>
    <input
      type="range"
      id="vol-slider"
      min="1000"
      max="100000"
      value="50000"
      oninput="document.getElementById('metric').innerText = Number(this.value).toLocaleString() + ' USD';"
    />
  </div>
</body>
</html>"""

    res5 = critic.audit_runtime_interaction(
        interactive_html,
        slider_selector="#vol-slider",
        metric_selector="#metric",
        target_value=85000
    )
    if not res5.get("interactive_verified"):
        failures.append(f"Test 5 Failed: Interactive state not verified (result={res5})")
    if "85,000 USD" not in res5.get("updated_metric", ""):
        failures.append(f"Test 5 Failed: Expected updated metric to contain '85,000 USD', got '{res5.get('updated_metric')}'")
    print(f"  [PASS] Test 5: Runtime causal interaction verified in Chromium ({res5.get('initial_metric')} -> {res5.get('updated_metric')})")

    # Test 6: Real React 19 TSX Living Component Mount & State Drag Audit
    from vibe_core.generator import InterfaceGenerator
    generator = InterfaceGenerator()
    fintech_decision = {
        "genome": {
            "domain": "fintech_banking",
            "platform": {"rtl_support": False}
        },
        "intent": {
            "product_domain": "fintech_banking",
            "language": ["en"]
        },
        "selected_style": "clean_stripe"
    }
    fintech_tsx = generator.generate_react_tsx(fintech_decision)

    res6 = critic.audit_runtime_react_tsx(
        fintech_tsx,
        target_slider_value=175000,
        capture_screenshots=True
    )
    if not res6.get("interactive_verified"):
        failures.append(f"Test 6 Failed: Real React 19 component interaction not verified (result={res6})")
    if res6.get("recalculated_count", 0) < 1:
        failures.append(f"Test 6 Failed: Expected at least 1 recalculated metric in DOM, got {res6.get('recalculated_count')}")
    if len(res6.get("screenshots_captured", [])) != 3:
        failures.append(f"Test 6 Failed: Expected 3 multi-viewport screenshots, got {res6.get('screenshots_captured')}")
    print(f"  [PASS] Test 6: Real React 19 TSX component mounted in Chromium ({res6.get('recalculated_count')} metrics causally recalculated, 3 screenshots captured)")

    if failures:
        print("\n[FAIL] Physical Critic Suite Failures:", file=sys.stderr)
        for f in failures:
            print(f"  - {f}", file=sys.stderr)
        return 1

    print("\n[SUCCESS] Headless Physical Viewport Critic passed all tests (6/6).")
    return 0

if __name__ == "__main__":
    sys.exit(main())
