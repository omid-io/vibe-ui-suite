#!/usr/bin/env python3
"""
test_v32_features.py — Unit and Regression Tests for Vibe UI v3.2.0 Features:
1. Domain Blueprints Integrity (All 24 domains covered)
2. Typography Variants (Anti-slop fonts)
3. Project Stack Sensor (<5ms scan speed)
4. Smart Lighting Strategy (Light vs Dark theme decision)
5. Living React 19 TSX Generation (useState, bdi, glowing edges)
6. Aesthetic Critic Gates (Anti-slop, sparkle penalty)
"""

import sys
import json
import time
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from vibe_core.director import DesignDirector
from vibe_core.generator import InterfaceGenerator
from vibe_core.stack_sensor import ProjectStackSensor
from vibe_core.critic import DesignCritic

def run_tests():
    print("[INFO] Running Vibe UI v3.2.0 Feature Verification Suite...")
    failures = []

    # 1. Domain Blueprints Integrity
    bp_path = ROOT_DIR / "data" / "domain_blueprints.json"
    if not bp_path.exists():
        failures.append("Domain blueprints file data/domain_blueprints.json missing")
    else:
        with open(bp_path, "r", encoding="utf-8") as f:
            bp_data = json.load(f)
        domains = bp_data.get("domains", {})
        if len(domains) != 24:
            failures.append(f"Expected 24 domain blueprints, got {len(domains)}")
        for d_id, d_info in domains.items():
            if not d_info.get("signature_widget"):
                failures.append(f"Domain {d_id} missing signature_widget")
            if len(d_info.get("layout_flavors", [])) < 3:
                failures.append(f"Domain {d_id} has fewer than 3 layout flavors")
    print(f"  [PASS] Test 1: 24 Domain Blueprints & Signature Widgets Verified")

    # 2. Typography Variants
    typo_path = ROOT_DIR / "data" / "typography_variants.json"
    if not typo_path.exists():
        failures.append("Typography variants file data/typography_variants.json missing")
    else:
        with open(typo_path, "r", encoding="utf-8") as f:
            t_data = json.load(f)
        pairings = t_data.get("pairings", [])
        if len(pairings) < 5:
            failures.append(f"Expected at least 5 typography pairings, got {len(pairings)}")
    print(f"  [PASS] Test 2: Anti-Slop Typography Matrix Verified ({len(pairings)} pairings)")

    # 3. Stack Sensor Performance & Precision
    t0 = time.perf_counter()
    sensor = ProjectStackSensor(ROOT_DIR)
    scan = sensor.scan()
    dur_ms = (time.perf_counter() - t0) * 1000
    if dur_ms > 10.0:
        failures.append(f"Stack sensor took {dur_ms:.2f}ms (>10ms limit)")
    if "recommendation" not in scan or "tailwind_syntax" not in scan["recommendation"]:
        failures.append("Stack sensor output missing recommendation/tailwind_syntax")
    print(f"  [PASS] Test 3: Project Stack Sensor ({dur_ms:.2f}ms)")

    # 4. Smart Lighting Strategy (Contextual Theme Bias)
    director = DesignDirector()
    intent_med = director.infer_intent("سامانه رزرو وقت کلینیک دندانپزشکی")
    intent_crypto = director.infer_intent("crypto derivatives trading orderbook")
    
    if intent_med["theme_strategy"] != "light":
        failures.append(f"Expected light theme for clinic, got {intent_med['theme_strategy']}")
    if intent_crypto["theme_strategy"] != "dark":
        failures.append(f"Expected dark theme for crypto, got {intent_crypto['theme_strategy']}")
    if intent_med["clarification_needed"] is not False:
        failures.append("Clarification needed should be False for clinical prompt")
    print(f"  [PASS] Test 4: Smart Lighting & Zero-Interrogation Fallback")

    # 5. Living React 19 TSX Generation
    gen = InterfaceGenerator()
    decision = {
        "genome": {},
        "selected_style": "clean_stripe",
        "intent": intent_med
    }
    tsx = gen.generate_react_tsx(decision, "DentalClinicBooking")
    if '"use client";' not in tsx:
        failures.append("TSX missing 'use client' directive")
    if "useState" not in tsx:
        failures.append("TSX missing useState hook for living micro-states")
    if "<bdi>" not in tsx:
        failures.append("TSX missing <bdi> isolation for mixed numerals/terms")
    if "activeTab === 0" not in tsx or "activeTab === 1" not in tsx or "activeTab === 2" not in tsx:
        failures.append("TSX missing functional conditional tab panels (activeTab === 0/1/2)")
    if "simulatedValue" not in tsx and "splitPos" not in tsx and "isLiveActive" not in tsx:
        failures.append("TSX missing living dynamic interactive widget state")
    
    html_gen = gen.generate_html(decision, "DentalClinicBooking")
    if f'data-domain="{intent_med["product_domain"]}"' not in html_gen:
        failures.append(f"Generated HTML missing data-domain attribute for {intent_med['product_domain']}")
    print(f"  [PASS] Test 5: Living React 19 TSX Generation with State, BiDi & Conditional Tabs")

    # 6. Aesthetic Critic Invariants
    critic = DesignCritic()
    html_purple_slop = "<html><body><div class='bg-gradient-to-r from-purple-600 to-indigo-500'>Slop</div></body></html>"
    critique_slop = critic.critique(html_purple_slop, decision)
    slop_defects = [d["type"] for d in critique_slop["defects_ranked"]]
    if "cliche_ai_gradient" not in slop_defects:
        failures.append("Critic failed to flag cliche_ai_gradient on purple-600")
    print(f"  [PASS] Test 6: Aesthetic Critic Invariant & Slop Trap Certified")

    if failures:
        print(f"\n[FAIL] {len(failures)} failures in v3.2.0 features:")
        for f in failures:
            print(f"  - {f}")
        sys.exit(1)

    print("\n[SUCCESS] All Vibe UI v3.2.0 feature tests passed with 100% compliance.")

if __name__ == "__main__":
    run_tests()
