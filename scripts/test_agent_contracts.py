"""
scripts/test_agent_contracts.py — Unit Tests for Swarm Agent Contracts
Validates serialization, deserialization, type safety, and validation logic
for ConceptContract, TrendEvidence, DesignGenomeContract, UIArtifactContract, and EvaluationReportContract.
"""

import sys
import os
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from schemas.agent_contracts import (
    ConceptContract,
    TrendEvidence,
    DesignGenomeContract,
    UIArtifactContract,
    EvaluationReportContract,
)


def test_concept_contract():
    c = ConceptContract(
        domain="food_restaurant_cafe",
        product_name="L'Artisan Bistro",
        target_audience="Fine dining patrons",
        emotional_tone="warm, intimate, refined",
        primary_job_to_be_done="Reserve a dining table and browse seasonal menu",
        spatial_flow=["hero", "signature_menu", "booking_drawer", "footer"],
        language="en",
        is_rtl=False
    )
    valid, errs = c.validate()
    assert valid, f"ConceptContract validation failed: {errs}"
    
    # Test JSON round-trip
    json_str = c.to_json()
    c2 = ConceptContract.from_json(json_str)
    assert c2.domain == c.domain
    assert c2.product_name == c.product_name
    assert c2.spatial_flow == c.spatial_flow
    # Test emotional_tone as List[str]
    c_list = ConceptContract(
        domain="food_restaurant_cafe",
        product_name="L'Artisan Bistro",
        target_audience="Fine dining patrons",
        emotional_tone=["warm", "intimate", "refined"],
        primary_job_to_be_done="Reserve a dining table",
        spatial_flow=["hero", "menu"]
    )
    valid_list, errs_list = c_list.validate()
    assert valid_list, f"ConceptContract with list emotional_tone failed: {errs_list}"
    assert c_list.emotional_tones == ["warm", "intimate", "refined"]
    print("[PASS] ConceptContract validation & serialization")


def test_trend_evidence():
    t = TrendEvidence(
        selected_style="organic_nordic",
        style_reasoning="Understated warmth, earthy OKLCH neutrals, and tactile terracotta cards",
        composition_archetype="conversion_stepper_funnel",
        typography_pair={"display": "Playfair Display", "body": "Plus Jakarta Sans"},
        novelty_risk_assessment="Low risk; optimal trust score",
        banned_slop_tropes=["generic_purple_gradient", "raw_unicode_emojis", "flat_black_void"],
        trend_sources=["godly", "dribbble_trending_2026", "uiverse"],
        confidence=0.96
    )
    valid, errs = t.validate()
    assert valid, f"TrendEvidence validation failed: {errs}"
    
    d = t.to_dict()
    t2 = TrendEvidence.from_dict(d)
    assert t2.selected_style == "organic_nordic"
    assert len(t2.banned_slop_tropes) == 3

    # Test tuple typography_pair auto-conversion
    t_tuple = TrendEvidence(
        selected_style="minimalist_saas",
        style_reasoning="Sharp clarity",
        composition_archetype="asymmetric_split_editorial",
        typography_pair=("Inter", "JetBrains Mono"),
        novelty_risk_assessment="Minimal",
        banned_slop_tropes=[]
    )
    assert t_tuple.typography_pair == {"display": "Inter", "body": "JetBrains Mono"}
    valid_t, errs_t = t_tuple.validate()
    assert valid_t, f"TrendEvidence with tuple typography failed: {errs_t}"

    t_tuple_dict = TrendEvidence.from_dict({
        "selected_style": "minimalist_saas",
        "style_reasoning": "Sharp clarity",
        "composition_archetype": "asymmetric_split_editorial",
        "typography_pair": ("Space Grotesk", "Space Mono"),
        "novelty_risk_assessment": "Minimal",
        "banned_slop_tropes": []
    })
    assert t_tuple_dict.typography_pair == {"display": "Space Grotesk", "body": "Space Mono"}
    print("[PASS] TrendEvidence validation & serialization")


def test_design_genome_contract():
    g = DesignGenomeContract(
        tokens={
            "canvas": "oklch(0.98 0.005 85)",
            "surface": "oklch(1.0 0 0)",
            "accent": "oklch(0.65 0.18 45)",
            "text": "oklch(0.20 0.015 60)",
            "border": "oklch(0.90 0.008 85)"
        },
        geometry={
            "radius_container": "24px",
            "radius_button": "12px",
            "border_width": "1px"
        },
        density="airy",
        surfaces={
            "depth": "diffused_soft",
            "elevation": "subtle_lift"
        },
        motion_profile={
            "spring_response": 0.35,
            "damping_ratio": 1.0,
            "motion_type": "critically_damped"
        },
        domain="food_restaurant_cafe",
        style="organic_nordic"
    )
    valid, errs = g.validate()
    assert valid, f"DesignGenomeContract validation failed: {errs}"
    
    json_str = g.to_json()
    g2 = DesignGenomeContract.from_json(json_str)
    assert g2.density == "airy"
    assert g2.tokens["canvas"] == "oklch(0.98 0.005 85)"
    print("[PASS] DesignGenomeContract validation & serialization")


def test_ui_artifact_contract():
    a = UIArtifactContract(
        code_html_or_tsx="<!DOCTYPE html><html dir='ltr'><body><main>Artisan</main></body></html>",
        title="Artisanal Wood-Fired Dining",
        signature_widgets=[{"widget": "menu_booking_card", "stateful": True}],
        micro_interactions=[{"element": "dish_card", "trigger": "hover", "effect": "subtle_scale"}],
        viewport_configs=[{"width": 390}, {"width": 768}, {"width": 1440}],
        format="html",
        brand_name="L'Artisan Bistro"
    )
    valid, errs = a.validate()
    assert valid, f"UIArtifactContract validation failed: {errs}"
    
    a2 = UIArtifactContract.from_dict(a.to_dict())
    assert a2.format == "html"
    assert len(a2.viewport_configs) == 3
    print("[PASS] UIArtifactContract validation & serialization")


def test_evaluation_report_contract():
    r = EvaluationReportContract(
        hard_quality_pass=True,
        wcag_contrast_score=17.12,
        overflow_0px_pass=True,
        aesthetic_quality_score=95.0,
        slop_penalty_deductions=0.0,
        correction_advice=[],
        iteration=1,
        acceptance_status="ACCEPTED"
    )
    valid, errs = r.validate()
    assert valid, f"EvaluationReportContract validation failed: {errs}"
    
    r2 = EvaluationReportContract.from_dict(r.to_dict())
    assert r2.hard_quality_pass is True
    assert r2.wcag_contrast_score == 17.12

    # Test strict boolean parsing and fail-closed defaults
    r_fail = EvaluationReportContract.from_dict({
        "hard_quality_pass": "false",
        "overflow_0px_pass": "false",
        "wcag_contrast_score": 3.2
    })
    assert r_fail.hard_quality_pass is False, "bool('false') must not become True"
    assert r_fail.overflow_0px_pass is False, "bool('false') must not become True"
    assert r_fail.acceptance_status == "PENDING", "fail-closed default must be PENDING"

    # Test empty dict fail-closed
    r_empty = EvaluationReportContract.from_dict({})
    assert r_empty.hard_quality_pass is False
    assert r_empty.acceptance_status == "PENDING"
    print("[PASS] EvaluationReportContract validation & serialization")


if __name__ == "__main__":
    print("[+] Running Agent Contracts Test Suite...")
    test_concept_contract()
    test_trend_evidence()
    test_design_genome_contract()
    test_ui_artifact_contract()
    test_evaluation_report_contract()
    print("[SUCCESS] All 5 Swarm Agent Contracts verified and operational!\n")
