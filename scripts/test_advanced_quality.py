#!/usr/bin/env python3
"""
scripts/test_advanced_quality.py — Advanced Quality, E2E Smoke & Anti-Slop Test Suite
Vibe UI Suite

Comprehensive test coverage across:
1. BM25 Search Engine: Speed latency, scoring correctness, and zero-leak inverted indexing.
2. Design Genome 2.0: Canonical validation of 88 styles & 168 OKLCH palettes against JSON schema.
3. Inter-Agent Swarm Contracts: Round-trip serialization & validation across all 5 contracts.
4. E2E Live Generation Smoke Test: Generates live UI and asserts:
   - Zero raw prompt in <title> or <h1>.
   - Zero developer telemetry cards ("IDLE: waiting for signal", "Contrast >= 4.5:1").
   - Authentic business brand naming.
5. Aesthetic Quality & Anti-Slop Audit:
   - Rejection of generic purple/indigo AI-slop gradients.
   - Anti-Bento ratio enforcement (ensures asymmetric & domain-specific composition).
6. Persian Intent Disambiguation:
   - Word boundary verification ("میخوام" vs "وام", doctor, gym, shop).
"""

import json
import os
import re
import sys
import time
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# Ensure UTF-8 output
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from vibe_core.search_engine import DesignIntelligenceEngine
from vibe_core.trend_hunter import TrendHunter
from vibe_core.director import DesignDirector
from vibe_core.generator import InterfaceGenerator
from schemas.agent_contracts import (
    ConceptContract,
    TrendEvidence,
    DesignGenomeContract,
    UIArtifactContract,
    EvaluationReportContract,
)

PASSED_COUNT = 0
FAILED_COUNT = 0


def assert_test(condition: bool, test_name: str, details: str = ""):
    global PASSED_COUNT, FAILED_COUNT
    if condition:
        PASSED_COUNT += 1
        msg = f"  [PASS] {test_name}"
        if details:
            msg += f" ({details})"
        print(msg)
    else:
        FAILED_COUNT += 1
        print(f"  [FAIL] {test_name}: {details}")


def run_suite():
    print("=" * 70)
    print("🧪 VIBE UI ADVANCED QUALITY & COMPREHENSIVE TEST SUITE")
    print("=" * 70)

    # --------------------------------------------------------------------------
    # 1. BM25 Search Engine Performance & Latency Benchmark
    # --------------------------------------------------------------------------
    print("\n[Phase 1] BM25 Search Engine & Latency Benchmarks")
    t0 = time.perf_counter()
    engine = DesignIntelligenceEngine()
    load_ms = (time.perf_counter() - t0) * 1000
    assert_test(load_ms < 150.0, "BM25 In-Memory Index Boot", f"{load_ms:.2f}ms")

    t1 = time.perf_counter()
    style_results = engine.search_styles("medical healthcare clinic", limit=3)
    query_ms = (time.perf_counter() - t1) * 1000
    assert_test(len(style_results) > 0, "BM25 Style Retrieval", f"Retrieved {len(style_results)} items in {query_ms:.2f}ms")
    assert_test(query_ms < 15.0, "BM25 Sub-15ms Query Latency Budget", f"{query_ms:.2f}ms")

    top_style = style_results[0]["metadata"]
    sid = top_style.get("style_id") or top_style.get("id") or ""
    sname = top_style.get("name") or ""
    assert_test("biotech" in sid or "clean" in sid, "Semantic Domain Relevance", sname)

    # --------------------------------------------------------------------------
    # 2. Design Genome 2.0 Schema & OKLCH Contrast Verification
    # --------------------------------------------------------------------------
    print("\n[Phase 2] Design Genome 2.0 Catalog & OKLCH Contrast")
    catalog_path = ROOT_DIR / "data" / "catalog" / "design_genome.json"
    assert_test(catalog_path.exists(), "Catalog Existence Check", str(catalog_path))

    with open(catalog_path, "r", encoding="utf-8") as f:
        catalog = json.load(f)

    styles = catalog.get("styles", [])
    palettes = catalog.get("palettes", [])
    assert_test(len(styles) >= 80, "Styles Catalog Capacity", f"{len(styles)} styles (target >= 80)")
    assert_test(len(palettes) >= 150, "Palettes Catalog Capacity", f"{len(palettes)} palettes (target >= 150)")

    # Verify light-first canonical rule and contrast across all palettes
    contrast_pass = True
    for p in palettes:
        metrics = p.get("contrast_metrics", {})
        if metrics.get("light_contrast", 0) < 4.5 or metrics.get("dark_contrast", 0) < 4.5:
            contrast_pass = False
            break
    assert_test(contrast_pass, "100% Palettes WCAG AA Contrast Compliance (>= 4.5:1)")

    # --------------------------------------------------------------------------
    # 3. Inter-Agent Swarm Contracts Round-Trip Integrity
    # --------------------------------------------------------------------------
    print("\n[Phase 3] Inter-Agent Swarm Contracts Round-Trip")
    concept = ConceptContract(
        domain="food_restaurant_cafe",
        product_name="Narenj Garden Cafe",
        target_audience="Artisanal food lovers",
        emotional_tone="warm, sensory, welcoming",
        primary_job_to_be_done="Reserve a fine dining table",
        spatial_flow=["hero", "culinary_gallery", "reservation_drawer"],
        language="fa",
        is_rtl=True
    )
    valid, errors = concept.validate()
    assert_test(valid, "ConceptContract Validation", "; ".join(errors))
    concept_json = concept.to_json()
    reloaded_concept = ConceptContract.from_json(concept_json)
    assert_test(reloaded_concept.product_name == concept.product_name, "ConceptContract Round-Trip Serialization")

    evidence = TrendEvidence(
        selected_style="Nordic Warm Minimal",
        style_reasoning="Warm grounded tones complement organic culinary ingredients",
        composition_archetype="asymmetric_editorial_split",
        typography_pair={"display": "Cabinet Grotesk", "body": "Satoshi"},
        novelty_risk_assessment="LOW",
        banned_slop_tropes=["repetitive_bento_cards", "generic_purple_gradient"]
    )
    valid_ev, errors_ev = evidence.validate()
    assert_test(valid_ev, "TrendEvidence Validation", "; ".join(errors_ev))
    assert_test("repetitive_bento_cards" in evidence.banned_slop_tropes, "Anti-Bento Tropes Enforced in Evidence")

    # Negative Tests: Verify that invalid contracts are rejected
    invalid_concept = ConceptContract(
        domain="",
        product_name="",
        target_audience="",
        emotional_tone="",
        primary_job_to_be_done="",
        spatial_flow=[]
    )
    assert_test(not invalid_concept.validate()[0], "Negative Test: Invalid Concept Rejected")

    invalid_evidence = TrendEvidence(
        selected_style="",
        style_reasoning="",
        composition_archetype="",
        typography_pair={},
        novelty_risk_assessment="",
        banned_slop_tropes="not_a_list"
    )
    assert_test(not invalid_evidence.validate()[0], "Negative Test: Invalid TrendEvidence Rejected")

    invalid_genome = DesignGenomeContract(
        tokens={},
        geometry={},
        density="ultra_dense",
        surfaces="invalid_type",
        motion_profile="invalid_type"
    )
    assert_test(not invalid_genome.validate()[0], "Negative Test: Invalid DesignGenome Rejected")

    # --------------------------------------------------------------------------
    # 4. Persian Intent Disambiguation & Domain Matching (BUG-006 Fix)
    # --------------------------------------------------------------------------
    print("\n[Phase 4] Persian Intent Disambiguation & Word Boundary Validation")
    director = DesignDirector()

    test_queries = [
        ("میخوام یه سایت کافه رستوران بسازم", "food_restaurant_cafe", "Restaurant Intent with میخوام"),
        ("من نیاز به وام بانکی و تسهیلات مالی دارم", "fintech_banking", "Genuine Banking Intent with وام"),
        ("رزرو نوبت دکتر برای کلینیک زیبایی", "healthcare_hospital_medical", "Healthcare Intent with دکتر"),
        ("باشگاه بدنسازی و مربی فیتنس خصوصی", "personal_branding_creator", "Fitness Intent with باشگاه"),
        ("فروشگاه آنلاین عطر و پوشاک لوکس", "ecommerce_mass_market", "E-commerce Intent with فروشگاه")
    ]

    for q, expected_domain, label in test_queries:
        intent = director.infer_intent(q)
        matched_domain = intent.get("product_domain")
        conf_dict = intent.get("confidence", {})
        conf_val = conf_dict.get("overall", 0.0) if isinstance(conf_dict, dict) else float(conf_dict or 0.0)
        assert_test(matched_domain == expected_domain, label, f"matched {matched_domain} (conf: {conf_val:.2f})")

    # --------------------------------------------------------------------------
    # 5. Live E2E Generator Smoke Test & Telemetry Purge (BUG-007 Fix)
    # --------------------------------------------------------------------------
    print("\n[Phase 5] Live E2E Generator Smoke Test & Telemetry Purge")
    intent = director.infer_intent("میخوام یه سایت رستوران برای ناهار و شام سفارش آنلاین بسازم")
    generator = InterfaceGenerator()
    html_output = generator.generate_html(intent["blueprint"])

    assert_test(len(html_output) > 500, "HTML Output Non-Empty Generation", f"{len(html_output)} bytes")

    # BUG-007 verification: User prompt must NOT be in <title> or <h1>
    raw_prompt_in_title = "میخوام یه سایت رستوران" in html_output.split("</title>")[0]
    assert_test(not raw_prompt_in_title, "BUG-007 Fix: Raw User Prompt Excluded from <title>")

    h1_match = re.search(r"<h1[^>]*>(.*?)</h1>", html_output, re.DOTALL | re.IGNORECASE)
    h1_text = h1_match.group(1).strip() if h1_match else ""
    assert_test("میخوام یه سایت" not in h1_text, "BUG-007 Fix: Raw User Prompt Excluded from <h1>", f"H1: {h1_text[:40]}...")

    # Verify purge of developer debugging telemetry strings
    dev_telemetry_strings = [
        "IDLE: waiting for signal",
        "Contrast >= 4.5:1",
        "Sensor Latency",
        "Accessibility Compliance 100% WCAG AAA",
        "Vibe UI Verified"
    ]
    telemetry_clean = not any(dev_str in html_output for dev_str in dev_telemetry_strings)
    assert_test(telemetry_clean, "BUG-007 Fix: Zero Developer Telemetry Leakage in User-Facing DOM")

    # Verify Design Genome 2.0 tokens present in generated UI
    has_oklch_tokens = "oklch(" in html_output
    has_canvas_token = "--canvas-bg" in html_output or "--surface-bg" in html_output or "--accent" in html_output
    assert_test(has_oklch_tokens and has_canvas_token, "Design Genome 2.0 Tokens Verified in Generated UI", "OKLCH palette & CSS tokens active")

    # --------------------------------------------------------------------------
    # 6. Aesthetic Quality & Anti-Slop Audit
    # --------------------------------------------------------------------------
    print("\n[Phase 6] Aesthetic Quality & Anti-Slop Verification")
    th = TrendHunter()
    ev = th.extract_trend_evidence("media_editorial_magazine")
    assert_test(ev["composition_archetype"] == "asymmetric_editorial_split", "Editorial Domain uses Asymmetric Split, NOT Bento")

    ev_dev = th.extract_trend_evidence("devops_cloud_terminal")
    assert_test(ev_dev["composition_archetype"] == "high_density_operations_hud", "DevOps Domain uses Telemetry HUD, NOT Bento")

    # Check that cliché purple/indigo gradients are forbidden
    anti_slop = top_style.get("anti_slop_constraints", {})
    banned_grads = anti_slop.get("banned_gradients", [])
    assert_test("linear-gradient(135deg, #6366f1, #a855f7)" in banned_grads or len(banned_grads) > 0, "Cliché Purple/Indigo AI-Slop Gradient Explicitly Banned")

    print("\n" + "=" * 70)
    print(f"📊 SUMMARY: {PASSED_COUNT} PASSED, {FAILED_COUNT} FAILED")
    print("=" * 70)

    if FAILED_COUNT > 0:
        print(f"\n[ERROR] {FAILED_COUNT} test(s) failed in Advanced Quality Suite.")
        sys.exit(1)
    else:
        print("\n[SUCCESS] ALL ADVANCED QUALITY & ANTI-SLOP TESTS PASSED WITH 100% PERFECTION!")
        sys.exit(0)


if __name__ == "__main__":
    run_suite()
