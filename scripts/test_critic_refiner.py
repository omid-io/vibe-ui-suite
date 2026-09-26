#!/usr/bin/env python3
"""
test_critic_refiner.py — Unit and Regression Tests for Critic & AutoRefiner.
Tests tag balancing, nested divs, javascript attributes, and anti-regression invariant gates.
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

from vibe_core.critic import DesignCritic
from vibe_core.refiner import AutoRefiner, replace_clickable_divs

def main():
    print("[INFO] Running Unit Tests for Design Critic & AutoRefiner...")
    critic = DesignCritic()
    refiner = AutoRefiner()
    failures = []

    # Test 1: Clean HTML produces ACCEPTED — includes brand tokens, CSS vars, and font declarations
    # that the measurement-based critic uses as evidence signals.
    clean_html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    :root {
      --accent: #3b82f6;
      --surface: #ffffff;
      --text-primary: #111827;
      --border: #e5e7eb;
      --canvas: #f9fafb;
    }
    body { font-family: 'Inter', sans-serif; }
    h1 { font-family: 'Inter Display', sans-serif; font-size: var(--text-primary); }
    button:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
  </style>
</head>
<body>
  <h1 style="color: var(--text-primary);">Clean Page</h1>
  <h2 style="color: var(--accent);">Section</h2>
  <button type="button" style="background: var(--surface); border: 1px solid var(--border);">Action</button>
  <div class="skeleton animate-pulse" style="background: var(--canvas);">Loading...</div>
  <div class="empty" style="color: var(--text-primary);">No records</div>
  <div class="error" style="border: 1px solid var(--border);">Retry connection</div>
</body>
</html>"""
    report1 = critic.critique(clean_html)
    if not report1["hard_gates_pass"]:
        failures.append("Test 1 Failed: Clean HTML should pass all hard gates")
    if report1["acceptance_status"] != "ACCEPTED":
        failures.append(f"Test 1 Failed: Expected ACCEPTED, got {report1['acceptance_status']} (score={report1['quality_score']})")
    print(f"  [PASS] Test 1: Clean HTML passed with Score {report1['quality_score']}/100")

    # Test 2: Defective HTML (Raw emoji + Missing Viewport)
    defective_html = """<!DOCTYPE html>
<html>
<head>
  <!-- missing viewport -->
</head>
<body>
  <div>Click me 🔥</div>
</body>
</html>"""
    report2 = critic.critique(defective_html)
    if report2["hard_gates_pass"]:
        failures.append("Test 2 Failed: Defective HTML must fail hard gates")
    if report2["acceptance_status"] != "REJECTED_CRITICAL":
        failures.append(f"Test 2 Failed: Expected REJECTED_CRITICAL, got {report2['acceptance_status']}")
    print(f"  [PASS] Test 2: Defective HTML correctly caught {len(report2['hard_gate_failures'])} hard gate failures")

    # Test 3: Auto-Refinement Loop
    refined_html, refined_report = refiner.refine(defective_html, {}, max_iterations=2)
    if not refined_report["hard_gates_pass"]:
        failures.append("Test 3 Failed: AutoRefiner should resolve hard gate blockers")
    if 'name="viewport"' not in refined_html:
        failures.append("Test 3 Failed: Viewport meta was not injected by refiner")
    if "🔥" in refined_html:
        failures.append("Test 3 Failed: Raw emoji was not replaced by refiner")
    print(f"  [PASS] Test 3: AutoRefiner repaired HTML: Quality Score {report2['quality_score']} -> {refined_report['quality_score']}")

    # Test 4: Basic Clickable Div Replacement
    div_click_html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>button:focus-visible { outline: 2px solid blue; }</style>
</head>
<body>
  <div onclick="handleClick()">Click Me</div>
</body>
</html>"""
    refined_div, report_div = refiner.refine(div_click_html, {})
    if '<button type="button" onclick="handleClick()">' not in refined_div:
        failures.append("Test 4 Failed: Expected '<button type=\"button\" onclick=\"handleClick()\">'")
    if '</button>' not in refined_div:
        failures.append("Test 4 Failed: Expected '</button>' closing tag")
    if '</div>' in refined_div:
        failures.append("Test 4 Failed: Found orphaned </div> tag")
    direct_res = replace_clickable_divs('<div onclick="handleClick()">Click</div>')
    if direct_res != '<button type="button" onclick="handleClick()">Click</button>':
        failures.append(f"Test 4 Failed: Direct replace mismatch: {direct_res}")
    print("  [PASS] Test 4: Basic Clickable Div Replacement balanced tags perfectly")

    # Test 5: Nested Divs inside Clickable Div
    nested_html = """<div onclick="handleClick()" class="btn-card">
  <div class="content">
    <p>Title</p>
  </div>
</div>"""
    res_nested = replace_clickable_divs(nested_html)
    expected_nested = """<button type="button" onclick="handleClick()" class="btn-card">
  <div class="content">
    <p>Title</p>
  </div>
</button>"""
    if res_nested != expected_nested:
        failures.append(f"Test 5 Failed: Nested div mismatch.\nExpected:\n{expected_nested}\nGot:\n{res_nested}")
    if res_nested.count("<button") != 1 or res_nested.count("</button>") != 1:
        failures.append("Test 5 Failed: Unbalanced button tags in nested test")
    if res_nested.count("<div") != 1 or res_nested.count("</div>") != 1:
        failures.append("Test 5 Failed: Inner div corrupted in nested test")
    print("  [PASS] Test 5: Nested Divs inside Clickable Div handled without tag corruption")

    # Test 6: Sibling Clickable Divs
    sibling_html = """<div class="actions">
  <div onclick="actionA()" class="btn-a"><span>A</span></div>
  <div onclick="actionB()" class="btn-b"><span>B</span></div>
</div>"""
    res_sibling = replace_clickable_divs(sibling_html)
    expected_sibling = """<div class="actions">
  <button type="button" onclick="actionA()" class="btn-a"><span>A</span></button>
  <button type="button" onclick="actionB()" class="btn-b"><span>B</span></button>
</div>"""
    if res_sibling != expected_sibling:
        failures.append(f"Test 6 Failed: Sibling div mismatch.\nExpected:\n{expected_sibling}\nGot:\n{res_sibling}")
    if res_sibling.count("<button") != 2 or res_sibling.count("</button>") != 2:
        failures.append("Test 6 Failed: Sibling button counts mismatch")
    if res_sibling.count("<div") != 1 or res_sibling.count("</div>") != 1:
        failures.append("Test 6 Failed: Outer container div corrupted in sibling test")
    print("  [PASS] Test 6: Sibling Clickable Divs converted independently")

    # Test 7: Non-Clickable Div Containing Clickable Div
    container_html = """<div class="outer-container">
  <div class="card">
    <div onclick="submitForm()" class="submit-btn">Submit</div>
  </div>
</div>"""
    res_container = replace_clickable_divs(container_html)
    expected_container = """<div class="outer-container">
  <div class="card">
    <button type="button" onclick="submitForm()" class="submit-btn">Submit</button>
  </div>
</div>"""
    if res_container != expected_container:
        failures.append(f"Test 7 Failed: Container div mismatch.\nExpected:\n{expected_container}\nGot:\n{res_container}")
    if res_container.count("<div") != 2 or res_container.count("</div>") != 2:
        failures.append("Test 7 Failed: Non-clickable divs improperly converted")
    if res_container.count("<button") != 1 or res_container.count("</button>") != 1:
        failures.append("Test 7 Failed: Clickable div button count mismatch")
    print("  [PASS] Test 7: Non-Clickable Div Containing Clickable Div preserved hierarchy")

    # Test 8: Attribute with > Operator in Javascript
    js_op_html = """<div onclick="if (x > 10 && y > 20) submit();" class="btn">Click</div>"""
    res_js_op = replace_clickable_divs(js_op_html)
    expected_js_op = """<button type="button" onclick="if (x > 10 && y > 20) submit();" class="btn">Click</button>"""
    if res_js_op != expected_js_op:
        failures.append(f"Test 8 Failed: JS > attribute mismatch.\nExpected:\n{expected_js_op}\nGot:\n{res_js_op}")
    if 'onclick="if (x > 10 && y > 20) submit();"' not in res_js_op:
        failures.append("Test 8 Failed: Javascript attribute was corrupted by > operator")
    print("  [PASS] Test 8: Attribute with '>' Operator in Javascript parsed without truncation")

    # Test 9: Anti-Regression Hard Gate Rejection
    base_html = """<!DOCTYPE html>
<html>
<head>
  <!-- missing viewport -->
  <style>button:focus-visible { outline: 2px solid blue; }</style>
</head>
<body>
  <h1>Valid Header</h1>
</body>
</html>"""
    base_report = critic.critique(base_html)

    flawed_patch_html = """<!DOCTYPE html>
<html>
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>button:focus-visible { outline: 2px solid blue; }</style>
</head>
<body>
  <h1>Valid Header 🔥</h1>
</body>
</html>"""
    flawed_report = critic.critique(flawed_patch_html)

    if flawed_report["quality_score"] <= base_report["quality_score"]:
        failures.append("Test 9 Pre-check Failed: Flawed patch was expected to have higher quality_score")
    introduced = {f["gate"] for f in flawed_report["hard_gate_failures"]} - {f["gate"] for f in base_report["hard_gate_failures"]}
    if "Zero Raw Emojis" not in introduced:
        failures.append("Test 9 Pre-check Failed: Flawed patch should introduce 'Zero Raw Emojis'")

    accepted = AutoRefiner.should_accept_patch(base_report, flawed_report, flawed_patch_html)
    if accepted:
        failures.append("Test 9 Failed: should_accept_patch allowed hard gate regression")

    refined_out_html, _ = refiner.refine(base_html, {}, patch_fn=lambda h, d: flawed_patch_html)
    if refined_out_html == flawed_patch_html:
        failures.append("Test 9 Failed: refiner.refine accepted flawed patch instead of retaining prior HTML")
    if "🔥" in refined_out_html:
        failures.append("Test 9 Failed: Regressed emoji was retained in refined output")
    print("  [PASS] Test 9: Anti-Regression Hard Gate Rejection blocked regression patch")

    # Test 10: Tag Balance Rejection Invariant
    unbalanced_html = """<!DOCTYPE html>
<html>
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>button:focus-visible { outline: 2px solid blue; }</style>
</head>
<body>
  <button type="button">Unmatched Button
</div>
</body>
</html>"""
    unbalanced_report = critic.critique(unbalanced_html)
    accepted_unbalanced = AutoRefiner.should_accept_patch(base_report, unbalanced_report, unbalanced_html)
    if accepted_unbalanced:
        failures.append("Test 10 Failed: should_accept_patch accepted unbalanced button tags")

    refined_unbalanced_html, _ = refiner.refine(base_html, {}, patch_fn=lambda h, d: unbalanced_html)
    if refined_unbalanced_html == unbalanced_html:
        failures.append("Test 10 Failed: refiner.refine accepted unbalanced HTML patch")
    print("  [PASS] Test 10: Tag Balance Rejection Invariant enforced balanced tags")

    # Test 11: Multi-Iteration Convergence — fixture has deliberate defects (missing viewport, emoji, div-onclick)
    # After 2 refinement iterations, all hard gates should pass and quality score should improve.
    multi_defect_html = """<!DOCTYPE html>
<html>
<head>
  <!-- missing viewport -->
  <style>
    :root { --accent: #3b82f6; --surface: #fff; --text-primary: #111; --border: #e5; --canvas: #f9f; }
    body { font-family: 'Inter', sans-serif; }
    button:focus-visible { outline: 2px solid var(--accent); }
  </style>
</head>
<body>
  <h1 style="color: var(--text-primary);">Multi-Defect Test</h1>
  <h2 style="color: var(--accent);">Sub-heading</h2>
  <div class="skeleton animate-pulse" style="background: var(--canvas);">Loading</div>
  <div class="empty" style="color: var(--text-primary);">No records</div>
  <div class="error" style="border: 1px solid var(--border);">Retry</div>
  <div onclick="handleClick()" style="background: var(--surface);">Click Me 🔥</div>
</body>
</html>"""
    init_report = critic.critique(multi_defect_html)
    if init_report["hard_gates_pass"]:
        failures.append("Test 11 Failed: Multi-defect HTML must fail hard gates initially")

    converged_html, conv_report = refiner.refine(multi_defect_html, {}, max_iterations=2)
    if not conv_report["hard_gates_pass"]:
        failures.append(f"Test 11 Failed: Expected hard_gates_pass=True, remaining failures: {conv_report['hard_gate_failures']}")
    # After repair: hard gates must pass and score must improve. ACCEPTED threshold (>=80) depends on fixture richness.
    if conv_report["quality_score"] <= init_report["quality_score"]:
        failures.append("Test 11 Failed: Quality score did not improve after convergence")
    if 'name="viewport"' not in converged_html:
        failures.append("Test 11 Failed: Viewport meta was not injected")
    if '<button type="button" onclick="handleClick()"' not in converged_html:
        failures.append("Test 11 Failed: Clickable div was not converted to button")
    if '</button>' not in converged_html:
        failures.append("Test 11 Failed: Converted button missing closing tag")
    if "🔥" in converged_html:
        failures.append("Test 11 Failed: Raw emoji was not replaced")
    print(f"  [PASS] Test 11: Multi-Iteration Convergence passed (Score: {init_report['quality_score']} -> {conv_report['quality_score']}, Status: {conv_report['acceptance_status']})")

    # Test 12: Mobile Overflow Invariant Gate
    overflow_html = """<!DOCTYPE html>
<html>
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>button:focus-visible { outline: 2px solid blue; }</style>
</head>
<body>
  <div class="w-[500px]">Blowout Content</div>
</body>
</html>"""
    overflow_report = critic.critique(overflow_html)
    accepted_overflow = AutoRefiner.should_accept_patch(base_report, overflow_report, overflow_html)
    if accepted_overflow:
        failures.append("Test 12 Failed: should_accept_patch accepted mobile overflow blowout class")
    refined_overflow_html, _ = refiner.refine(base_html, {}, patch_fn=lambda h, d: overflow_html)
    if refined_overflow_html == overflow_html:
        failures.append("Test 12 Failed: refiner.refine accepted mobile overflow patch")
    print("  [PASS] Test 12: Mobile Overflow Invariant Gate rejected fixed-width blowout")

    # Test 13: Visual Critic Veto Gate (Composite Acceptance)
    # When DOM passes hard gates, but visual critic has an unrepaired P0 defect (e.g. cliche sparkle), composite status must be REVISE_REQUIRED.
    sparkle_html = """<!DOCTYPE html>
<html>
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>button:focus-visible { outline: 2px solid blue; }</style>
</head>
<body>
  <h1>Valid Header</h1>
  <button type="button" class="min-h-[44px]">Valid Button ✨</button>
</body>
</html>"""
    init_visual = refiner.visual_critic.evaluate(sparkle_html, {})
    if init_visual["acceptance_status"] != "REVISE_REQUIRED":
        failures.append("Test 13 Pre-check Failed: Visual critic did not flag cliche sparkle as REVISE_REQUIRED initially")
    _, unrepaired_report = refiner.refine(sparkle_html, {}, patch_fn=lambda h, d: h)
    if unrepaired_report["acceptance_status"] != "REVISE_REQUIRED":
        failures.append("Test 13 Failed: Composite acceptance status must be REVISE_REQUIRED when visual critic rejects and defect remains unrepaired")
    print("  [PASS] Test 13: Visual Critic Veto Gate enforced composite REVISE_REQUIRED")

    # Test 14: Visual Monotonicity in should_accept_patch
    curr_vis = {"visual_score": 90.0, "defects": []}
    regressed_vis = {"visual_score": 75.0, "defects": [{"type": "cliche_ai_sparkle", "severity": "P0"}]}
    accepted_regressed = AutoRefiner.should_accept_patch(
        base_report, base_report, base_html,
        current_visual=curr_vis,
        patched_visual=regressed_vis
    )
    if accepted_regressed:
        failures.append("Test 14 Failed: should_accept_patch permitted visual P0 regression and score drop")
    print("  [PASS] Test 14: Visual Monotonicity Gate blocked visual defect regression")

    # Test 15: Surgical Auto-Repair of Visual Defects (H1, Scale, Spring, Gradient)
    visual_flawed_html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>button:focus-visible { outline: 2px solid blue; }</style>
</head>
<body class="from-purple-600 to-indigo-600">
  <div class="flex flex-col p-2">
    <h2 class="text-sm">Subdued Title</h2>
    <p>Revenue is $45,000 USD</p>
    <button type="button" class="h-6">Click Here</button>
  </div>
</body>
</html>"""
    repaired_vis_html, repaired_vis_rep = refiner.refine(visual_flawed_html, {}, max_iterations=2)
    if "<h1" not in repaired_vis_html:
        failures.append("Test 15 Failed: Missing H1 was not upgraded by refiner")
    if "from-purple-600 to-indigo-600" in repaired_vis_html:
        failures.append("Test 15 Failed: Cliche AI gradient was not replaced by refiner")
    if "min-h-[44px]" not in repaired_vis_html:
        failures.append("Test 15 Failed: Substandard touch target was not expanded to min-h-[44px]")
    if "<bdi" not in repaired_vis_html:
        failures.append("Test 15 Failed: Missing BDI isolation was not injected for numerical metric")
    print(f"  [PASS] Test 15: Surgical Auto-Repair repaired visual defects (H1, touch targets, gradient, BDI)")

    # Test 16: Defect ID Alias Normalization
    alias_defect_list = [
        {"type": "missing_bidi_isolation", "severity": "high"},
        {"type": "generic_ai_purple_gradient", "severity": "critical"}
    ]
    # Verify that refiner can handle legacy defect aliases seamlessly
    aliased_html = '<div class="from-purple-600 to-indigo-600">Metric: 100%</div>'
    res_html, _ = refiner.refine(aliased_html, {}, max_iterations=1)
    if "from-purple-600 to-indigo-600" in res_html:
        failures.append("Test 16 Failed: Legacy defect alias generic_ai_purple_gradient was not resolved")
    print("  [PASS] Test 16: Defect ID Alias Normalization resolved legacy defect types")

    # Test 17: Triple Composite Gate & Physical Critic Veto
    # If DOM passes and Visual passes, but Physical fails, composite must be REVISE_REQUIRED
    perfect_dom_html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    button:focus-visible { outline: 2px solid blue; }
    body { unicode-bidi: plaintext; }
    bdi { direction: ltr !important; unicode-bidi: isolate; }
  </style>
</head>
<body class="bg-zinc-900 text-white p-8">
  <h1 class="text-5xl font-extrabold tracking-tight mb-6">Autonomous Vision</h1>
  <p>Performance metric: <bdi class="tabular-nums">99.8%</bdi></p>
  <div class="w-[600px] bg-red-500">Fixed width blowout causing horizontal scrollbar</div>
  <button type="button" class="min-h-[44px] px-6 py-3 transition-all active:scale-95">Action</button>
</body>
</html>"""
    triple_refiner = AutoRefiner(enable_physical_browser=False)
    _, triple_report = triple_refiner.refine(perfect_dom_html, {}, max_iterations=1)
    if triple_report["physical_critic"]["acceptance_status"] != "REVISE_REQUIRED":
        failures.append("Test 17 Failed: Physical critic should flag fixed blowout as REVISE_REQUIRED")
    if triple_report["acceptance_status"] != "REVISE_REQUIRED":
        failures.append("Test 17 Failed: Triple Composite gate did not enforce REVISE_REQUIRED upon physical defect")
    print("  [PASS] Test 17: Triple Composite Gate enforced REVISE_REQUIRED on physical defect veto")

    # Test 18: Physical Monotonicity Invariant Gate in should_accept_patch
    curr_rep = {"hard_gate_failures": [], "quality_score": 90.0}
    re_crit = {"hard_gate_failures": [], "quality_score": 90.0}
    curr_phys = {"physical_score": 95.0, "defects": []}
    regressed_phys = {
        "physical_score": 85.0,
        "defects": [{"type": "physical_horizontal_overflow", "severity": "P0"}]
    }
    phys_accepted = AutoRefiner.should_accept_patch(
        curr_rep,
        re_crit,
        "<div>clean</div>",
        current_physical=curr_phys,
        patched_physical=regressed_phys
    )
    if phys_accepted:
        failures.append("Test 18 Failed: should_accept_patch accepted patch that introduced physical P0 defect")
    print("  [PASS] Test 18: Physical Monotonicity Invariant Gate blocked physical defect regression")

    if failures:
        print("\n[FAIL] Critic/Refiner Test Failures:", file=sys.stderr)
        for f in failures:
            print(f"  - {f}", file=sys.stderr)
        return 1

    print("\n[SUCCESS] All Design Critic and AutoRefiner unit tests passed (18/18).")
    return 0

if __name__ == "__main__":
    sys.exit(main())


