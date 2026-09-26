"""
vibe_core.interaction_contract — Deterministic Interaction Contracts for 24 Canonical Domains (v3.9.0)
Defines semantic control targeting, input variable bounds, test sweep parameters,
and exact causal assertion invariants for real browser runtime interaction in headless Chromium.
"""

from dataclasses import dataclass
from typing import Dict, Any, List, Optional


@dataclass
class InteractionContract:
    domain_id: str
    control_selector: str
    input_variable: str
    target_value: float
    bound_metrics: List[str]
    expected_direction: str  # "positive", "negative", "recalculated"
    description: str
    formula_expr: str = ""


# Canonical interaction specifications for all 24 domains with calibrated targets and explicit formulas
DOMAIN_INTERACTION_CONTRACTS: Dict[str, InteractionContract] = {
    "beauty_clinical_wellness": InteractionContract(
        domain_id="beauty_clinical_wellness",
        control_selector='[data-vibe-control="split-slider"], input[type="range"]',
        input_variable="splitPos",
        target_value=65.0,
        bound_metrics=["melanin-uniformity", "collagen-index"],
        expected_direction="positive",
        description="Clinical split-view slider adjusting before/after dermal reconstruction metrics",
        formula_expr="1.2 + (splitPos / 100) * 0.7"
    ),
    "fintech_banking": InteractionContract(
        domain_id="fintech_banking",
        control_selector='[data-vibe-control="simulated-range"], input[type="range"]',
        input_variable="simulatedValue",
        target_value=164250.0,
        bound_metrics=["annual-apy", "compounded-growth"],
        expected_direction="positive",
        description="Active capital allocation adjusting annual APY and 3-year compounded returns",
        formula_expr="round(simulatedValue * 1.056)"
    ),
    "crypto_trading_web3": InteractionContract(
        domain_id="crypto_trading_web3",
        control_selector='[data-vibe-control="simulated-range"], input[type="range"]',
        input_variable="simulatedValue",
        target_value=65350.0,
        bound_metrics=["order-volume", "slippage-rate"],
        expected_direction="positive",
        description="Execution order volume adjusting order size and estimated pool slippage",
        formula_expr="0.02 + (simulatedValue / 100000) * 0.18"
    ),
    "devops_cloud_terminal": InteractionContract(
        domain_id="devops_cloud_terminal",
        control_selector='[data-vibe-control="simulated-range"], input[type="range"]',
        input_variable="simulatedValue",
        target_value=66750.0,
        bound_metrics=["pod-count", "network-throughput"],
        expected_direction="positive",
        description="Cluster replica scaler adjusting pod allocations and network throughput",
        formula_expr="round(simulatedValue / 4000)"
    ),
    "saas_b2b_enterprise": InteractionContract(
        domain_id="saas_b2b_enterprise",
        control_selector='[data-vibe-control="simulated-range"], input[type="range"]',
        input_variable="simulatedValue",
        target_value=66750.0,
        bound_metrics=["seat-savings", "sla-uptime"],
        expected_direction="positive",
        description="Enterprise seat count adjusting annual labor savings and SLA guarantees",
        formula_expr="round((simulatedValue / 500) * 4200)"
    ),
    "ai_developer_platform": InteractionContract(
        domain_id="ai_developer_platform",
        control_selector='[data-vibe-control="simulated-range"], input[type="range"]',
        input_variable="simulatedValue",
        target_value=32850.0,
        bound_metrics=["token-budget", "vram-allocation"],
        expected_direction="positive",
        description="Monthly processed token budget adjusting VRAM and inference cluster slots",
        formula_expr="simulatedValue * 10000"
    ),
    "food_restaurant_cafe": InteractionContract(
        domain_id="food_restaurant_cafe",
        control_selector='[data-vibe-control="simulated-range"], input[type="range"]',
        input_variable="simulatedValue",
        target_value=68500.0,
        bound_metrics=["tasting-subtotal", "pairing-allocation"],
        expected_direction="positive",
        description="Degustation guest seating slider adjusting multi-course subtotal and pairings",
        formula_expr="max(4, round(simulatedValue / 10000))"
    ),
    "real_estate_architecture": InteractionContract(
        domain_id="real_estate_architecture",
        control_selector='[data-vibe-control="simulated-range"], input[type="range"]',
        input_variable="simulatedValue",
        target_value=68500.0,
        bound_metrics=["interior-volume", "cap-rate"],
        expected_direction="positive",
        description="Architectural area slider adjusting structural volume and cap rate",
        formula_expr="round(simulatedValue / 80)"
    ),
    "healthcare_hospital_medical": InteractionContract(
        domain_id="healthcare_hospital_medical",
        control_selector='[data-vibe-control="simulated-range"], input[type="range"]',
        input_variable="simulatedValue",
        target_value=40750.0,
        bound_metrics=["triage-wait", "icu-capacity"],
        expected_direction="positive",
        description="Emergency room intake volume adjusting triage wait and ICU occupancy",
        formula_expr="max(4, round(simulatedValue / 1800))"
    ),
    "education_edtech_lms": InteractionContract(
        domain_id="education_edtech_lms",
        control_selector='[data-vibe-control="simulated-range"], input[type="range"]',
        input_variable="simulatedValue",
        target_value=66750.0,
        bound_metrics=["curriculum-completion", "weekly-pacing"],
        expected_direction="positive",
        description="Weekly study commitment slider adjusting projected syllabus completion",
        formula_expr="max(4, round(simulatedValue / 5000))"
    ),
    "creative_portfolio_agency": InteractionContract(
        domain_id="creative_portfolio_agency",
        control_selector='[data-vibe-control="simulated-range"], input[type="range"]',
        input_variable="simulatedValue",
        target_value=68500.0,
        bound_metrics=["prototype-delivery", "conversion-lift"],
        expected_direction="positive",
        description="Sprint scope slider adjusting prototype delivery horizon and conversion lift",
        formula_expr="max(2, round(simulatedValue / 15000))"
    ),
    "ecommerce_luxury_fashion": InteractionContract(
        domain_id="ecommerce_luxury_fashion",
        control_selector='[data-vibe-control="simulated-range"], input[type="range"]',
        input_variable="simulatedValue",
        target_value=68500.0,
        bound_metrics=["cashmere-weight", "atelier-price"],
        expected_direction="positive",
        description="Artisanal fabric weight adjusting bespoke atelier unit price",
        formula_expr="round(300 + (simulatedValue / 400))"
    ),
    "ecommerce_mass_market": InteractionContract(
        domain_id="ecommerce_mass_market",
        control_selector='[data-vibe-control="simulated-range"], input[type="range"]',
        input_variable="simulatedValue",
        target_value=33375.0,
        bound_metrics=["cart-subtotal", "bulk-discount"],
        expected_direction="positive",
        description="Cart volume slider adjusting tiered checkout subtotal and volume discount",
        formula_expr="simulatedValue / 100"
    ),
    "media_editorial_magazine": InteractionContract(
        domain_id="media_editorial_magazine",
        control_selector='[data-vibe-control="simulated-range"], input[type="range"]',
        input_variable="simulatedValue",
        target_value=66750.0,
        bound_metrics=["readership-reach", "read-through-retention"],
        expected_direction="positive",
        description="Investigative report depth adjusting monthly words and immersion time",
        formula_expr="simulatedValue * 1.5"
    ),
    "travel_hospitality_tourism": InteractionContract(
        domain_id="travel_hospitality_tourism",
        control_selector='[data-vibe-control="simulated-range"], input[type="range"]',
        input_variable="simulatedValue",
        target_value=80800.0,
        bound_metrics=["nights-stay", "all-inclusive-total"],
        expected_direction="positive",
        description="Resort duration slider adjusting nights stay and total all-inclusive cost",
        formula_expr="max(3, round(simulatedValue / 8000))"
    ),
    "legal_compliance_law": InteractionContract(
        domain_id="legal_compliance_law",
        control_selector='[data-vibe-control="simulated-range"], input[type="range"]',
        input_variable="simulatedValue",
        target_value=66750.0,
        bound_metrics=["audited-contracts", "retainer-hours"],
        expected_direction="positive",
        description="Contract portfolio volume slider adjusting forensic audit hours and liability",
        formula_expr="round(simulatedValue / 40)"
    ),
    "gaming_entertainment_streaming": InteractionContract(
        domain_id="gaming_entertainment_streaming",
        control_selector='[data-vibe-control="simulated-range"], input[type="range"]',
        input_variable="simulatedValue",
        target_value=40750.0,
        bound_metrics=["bitrate-allocation", "framerate-stability"],
        expected_direction="positive",
        description="Live 4K stream bitrate slider adjusting transmission bandwidth and FPS",
        formula_expr="round(2500 + (simulatedValue / 10))"
    ),
    "automotive_ev_mobility": InteractionContract(
        domain_id="automotive_ev_mobility",
        control_selector='[data-vibe-control="simulated-range"], input[type="range"]',
        input_variable="simulatedValue",
        target_value=66750.0,
        bound_metrics=["ev-range", "charging-eta"],
        expected_direction="positive",
        description="Battery pack capacity slider adjusting estimated driving range and charging speed",
        formula_expr="round((simulatedValue / 1000) * 4.8)"
    ),
    "logistics_supply_chain": InteractionContract(
        domain_id="logistics_supply_chain",
        control_selector='[data-vibe-control="simulated-range"], input[type="range"]',
        input_variable="simulatedValue",
        target_value=66750.0,
        bound_metrics=["active-fleet", "dispatch-latency"],
        expected_direction="positive",
        description="Active transit fleet slider adjusting aggregate vehicle units and dispatch latency",
        formula_expr="round(simulatedValue / 1200)"
    ),
    "energy_greentech_sustainability": InteractionContract(
        domain_id="energy_greentech_sustainability",
        control_selector='[data-vibe-control="simulated-range"], input[type="range"]',
        input_variable="simulatedValue",
        target_value=66750.0,
        bound_metrics=["co2-offset", "annual-grid-export"],
        expected_direction="positive",
        description="Solar array capacity slider adjusting annual CO2 offset and grid revenue",
        formula_expr="simulatedValue * 0.042"
    ),
    "nonprofit_charity_social": InteractionContract(
        domain_id="nonprofit_charity_social",
        control_selector='[data-vibe-control="simulated-range"], input[type="range"]',
        input_variable="simulatedValue",
        target_value=32850.0,
        bound_metrics=["clean-water", "community-reach"],
        expected_direction="positive",
        description="Donation budget slider adjusting clean water filtration volume and meals served",
        formula_expr="simulatedValue * 240"
    ),
    "personal_branding_creator": InteractionContract(
        domain_id="personal_branding_creator",
        control_selector='[data-vibe-control="simulated-range"], input[type="range"]',
        input_variable="simulatedValue",
        target_value=66750.0,
        bound_metrics=["audience-reach", "sponsorship-revenue"],
        expected_direction="positive",
        description="Newsletter subscriber scale adjusting projected monthly reach and brand value",
        formula_expr="round(simulatedValue * 1.8)"
    ),
    "cybersecurity_identity_auth": InteractionContract(
        domain_id="cybersecurity_identity_auth",
        control_selector='[data-vibe-control="simulated-range"], input[type="range"]',
        input_variable="simulatedValue",
        target_value=66750.0,
        bound_metrics=["anomalies-intercepted", "zero-trust-mttr"],
        expected_direction="positive",
        description="Endpoint ingress monitor adjusting intercepted attack telemetry and MTTR",
        formula_expr="round(simulatedValue * 14.5)"
    ),
    "general_modern_saas": InteractionContract(
        domain_id="general_modern_saas",
        control_selector='[data-vibe-control="simulated-range"], input[type="range"]',
        input_variable="simulatedValue",
        target_value=65350.0,
        bound_metrics=["throughput-rate", "system-efficiency"],
        expected_direction="positive",
        description="Core workflow event load adjusting throughput rate and system efficiency",
        formula_expr="simulatedValue * 25"
    ),
}


def get_interaction_contract(domain_id: str) -> InteractionContract:
    """Returns canonical InteractionContract for a given domain, defaulting to general_modern_saas."""
    return DOMAIN_INTERACTION_CONTRACTS.get(domain_id, DOMAIN_INTERACTION_CONTRACTS["general_modern_saas"])
