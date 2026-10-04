#!/usr/bin/env python3
"""
scripts/test_pipeline_e2e.py — End-to-End Pipeline Integration Test Suite
Validates seamless execution across the entire Vibe UI pipeline:
  Query -> Director -> Recommendation -> Generator -> Critic -> Healer -> Verifier

Fixes Qwen Coder P1 critique: "عدم وجود Integration Tests واقعی".
"""

import sys
import json
from pathlib import Path

# Windows console encoding safeguard
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from vibe_core.director import DesignDirector
from vibe_core.recommendation import RecommendationEngine
from vibe_core.generator import InterfaceGenerator
from vibe_core.critic import DesignCritic
from vibe_core.refiner import AutoRefiner
from vibe_core.healer import SelfHealingLoop
from vibe_core.verifier import VerificationEngine
from vibe_core.constants import (
    MAX_BLUR_SURFACES,
    HARD_MIN_TOUCH_PX,
    RECOMMENDED_TOUCH_PX,
)


def test_full_pipeline_persian_rtl():
    """Test 1: Full pipeline execution on Persian RTL prompt."""
    prompt = "کلینیک تخصصی پوست و مو و لیزر گلوریا"
    director = DesignDirector()
    engine = RecommendationEngine()
    generator = InterfaceGenerator()
    healer = SelfHealingLoop()
    verifier = VerificationEngine()

    # 1. Intent extraction
    intent = director.infer_intent(prompt)
    assert intent["product_domain"] == "beauty_clinical_wellness", f"Unexpected domain: {intent['product_domain']}"
    assert "fa" in intent["language"], f"Persian language not detected in {intent['language']}"

    # 2. Recommendation
    decision = engine.recommend(intent)
    assert decision["selected_style"] is not None
    assert "genome" in decision

    # 3. HTML Generation
    html = generator.generate_html(decision, prompt_title=prompt)
    assert 'dir="rtl"' in html, "Generated Persian artifact missing dir='rtl'"
    assert "<bdi" in html or "unicode-bidi" in html, "Missing semantic RTL isolation"

    # 4. Self-Healing (Critic + Refiner + Prompt Generation if needed)
    healed_html, report, prompt_corr = healer.heal(html, decision, original_prompt=prompt)
    assert report["quality_score"] >= 80.0, f"Quality score {report['quality_score']} below 80"
    assert report["hard_gates_pass"] is True, f"Hard gate failures: {report.get('hard_gate_failures')}"

    # 5. Fast-Path Verification
    ver_report = verifier.verify_html(healed_html, "persian_test.html", mode="fast")
    assert ver_report["overall_status"] == "PASS", f"Fast verification failed: {ver_report}"
    assert ver_report["checks_summary"]["failed"] == 0


def test_full_pipeline_english_saas():
    """Test 2: Full pipeline execution on English SaaS fintech prompt."""
    prompt = "Enterprise Cloud Billing and Cost Analytics Dashboard"
    director = DesignDirector()
    engine = RecommendationEngine()
    generator = InterfaceGenerator()
    healer = SelfHealingLoop()
    verifier = VerificationEngine()

    intent = director.infer_intent(prompt)
    assert "fa" not in intent["language"]

    decision = engine.recommend(intent)
    assert decision["composite_score"] > 0.5

    html = generator.generate_html(decision, prompt_title=prompt)
    assert 'name="viewport"' in html
    assert "<html" in html and "</html>" in html

    healed_html, report, _ = healer.heal(html, decision, original_prompt=prompt)
    assert report["hard_gates_pass"] is True

    ver_report = verifier.verify_html(healed_html, "saas_test.html", mode="fast")
    assert ver_report["overall_status"] == "PASS"


def test_self_healing_defect_recovery():
    """Test 3: Injected defect recovery via SelfHealingLoop and AutoRefiner."""
    healer = SelfHealingLoop()
    critic = DesignCritic()

    # Raw HTML with multiple deliberate defects: div onclick and raw emoji
    flawed_html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Flawed Test</title>
  <style>
    body { font-family: sans-serif; }
  </style>
</head>
<body>
  <div class="card" onclick="alert('clicked')">
    <h2>Test Card 🔥</h2>
    <p>Click me</p>
  </div>
</body>
</html>"""

    # Initial critique must detect defects
    initial_critique = critic.critique(flawed_html)
    assert initial_critique["hard_gates_pass"] is False, "Critic failed to catch injected defects"

    # Self-healing loop must heal the clickable div
    healed_html, healed_report, correction_prompt = healer.heal(flawed_html, max_rounds=2)
    assert "<button" in healed_html, "AutoRefiner failed to convert <div onclick> to <button>"
    assert "<div class=\"card\" onclick=" not in healed_html, "Old <div onclick> still present"


def test_constants_and_timestamp_integrity():
    """Test 4: Verifies centralized constants and non-hardcoded timestamps."""
    assert MAX_BLUR_SURFACES == 8
    assert HARD_MIN_TOUCH_PX == 24
    assert RECOMMENDED_TOUCH_PX == 44

    critic = DesignCritic()
    report = critic.critique("<html><body><h1>Hello</h1></body></html>")
    timestamp = report.get("timestamp", "")
    assert timestamp != "2026-09-03T12:00:00Z", f"Hardcoded timestamp still present in critic: {timestamp}"
    assert "T" in timestamp, "Timestamp must be ISO 8601 formatted"

    verifier = VerificationEngine()
    v_report = verifier.verify_html("<html><body><h1>Hello</h1></body></html>")
    v_timestamp = v_report.get("timestamp", "")
    assert v_timestamp != "2026-09-03T12:00:00Z", f"Hardcoded timestamp still present in verifier: {v_timestamp}"


def main():
    print("=" * 70)
    print("🧪 VIBE UI V3 FULL PIPELINE INTEGRATION TESTS (E2E)")
    print("=" * 70)

    tests = [
        ("Persian RTL Full Pipeline", test_full_pipeline_persian_rtl),
        ("English SaaS Full Pipeline", test_full_pipeline_english_saas),
        ("Defect Recovery via Self-Healing Loop", test_self_healing_defect_recovery),
        ("Constants & Dynamic Timestamp Integrity", test_constants_and_timestamp_integrity),
    ]

    passed = 0
    failed = 0

    for name, test_fn in tests:
        try:
            print(f"[RUNNING] {name}...")
            test_fn()
            print(f"  [PASS] {name}")
            passed += 1
        except Exception as e:
            print(f"  [FAIL] {name}: {e}", file=sys.stderr)
            import traceback
            traceback.print_exc()
            failed += 1

    print("\n" + "=" * 70)
    if failed == 0:
        print(f"✅ ALL {passed} INTEGRATION TESTS PASSED CLEANLY.")
        return 0
    else:
        print(f"❌ {failed} OF {passed + failed} INTEGRATION TESTS FAILED.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
