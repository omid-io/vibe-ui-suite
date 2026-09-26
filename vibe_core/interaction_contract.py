"""
vibe_core.interaction_contract — Deterministic Interaction Contracts for 24 Canonical Domains (v3.8.0)
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
    expected_direction: str  # "recalculated", "positive", "negative"
    description: str


# Canonical interaction specifications for all 24 domains
DOMAIN_INTERACTION_CONTRACTS: Dict[str, InteractionContract] = {
    "beauty_clinical_wellness": InteractionContract(
        domain_id="beauty_clinical_wellness",
        control_selector='[data-vibe-control="split-slider"], input[type="range"]',
        input_variable="splitPos",
        target_value=85.0,
        bound_metrics=["melanin-uniformity", "collagen-index"],
        expected_direction="positive",
        description="Clinical split-view slider adjusting before/after dermal reconstruction metrics"
    ),
    "fintech_banking": InteractionContract(
        domain_id="fintech_banking",
        control_selector='[data-vibe-control="simulated-range"], input[type="range"]',
        input_variable="simulatedValue",
        target_value=125000.0,
        bound_metrics=["annual-apy", "compounded-growth"],
        expected_direction="positive",
        description="Active capital allocation adjusting annual APY and 3-year compounded returns"
    ),
    "crypto_trading_web3": InteractionContract(
        domain_id="crypto_trading_web3",
        control_selector='[data-vibe-control="simulated-range"], input[type="range"]',
        input_variable="simulatedValue",
        target_value=75000.0,
        bound_metrics=["order-volume", "slippage-rate"],
        expected_direction="positive",
        description="Execution order volume adjusting order size and estimated pool slippage"
    ),
    "devops_cloud_terminal": InteractionContract(
        domain_id="devops_cloud_terminal",
        control_selector='[data-vibe-control="simulated-range"], input[type="range"]',
        input_variable="simulatedValue",
        target_value=64.0,
        bound_metrics=["pod-count", "network-throughput"],
        expected_direction="positive",
        description="Cluster replica scaler adjusting pod allocations and network throughput"
    ),
    "healthcare_hospital_medical": InteractionContract(
        domain_id="healthcare_hospital_medical",
        control_selector='[data-vibe-control="simulated-range"], input[type="range"]',
        input_variable="simulatedValue",
        target_value=140.0,
        bound_metrics=["triage-wait", "icu-capacity"],
        expected_direction="recalculated",
        description="Emergency room intake volume adjusting triage wait and ICU occupancy"
    ),
    "automotive_ev_mobility": InteractionContract(
        domain_id="automotive_ev_mobility",
        control_selector='[data-vibe-control="simulated-range"], input[type="range"]',
        input_variable="simulatedValue",
        target_value=85.0,
        bound_metrics=["ev-range", "charging-eta"],
        expected_direction="recalculated",
        description="Battery State-of-Charge slider adjusting estimated driving range and charging ETA"
    ),
    "ecommerce_luxury_fashion": InteractionContract(
        domain_id="ecommerce_luxury_fashion",
        control_selector='[data-vibe-control="simulated-range"], input[type="range"]',
        input_variable="simulatedValue",
        target_value=8.0,
        bound_metrics=["atelier-total", "bespoke-hours"],
        expected_direction="positive",
        description="Atelier edition quantity adjusting order total and bespoke fabrication hours"
    ),
    "real_estate_architecture": InteractionContract(
        domain_id="real_estate_architecture",
        control_selector='[data-vibe-control="simulated-range"], input[type="range"]',
        input_variable="simulatedValue",
        target_value=2400000.0,
        bound_metrics=["monthly-mortgage", "cap-rate"],
        expected_direction="recalculated",
        description="Asset valuation slider adjusting monthly mortgage amortization and cap rate"
    ),
    "education_edtech_lms": InteractionContract(
        domain_id="education_edtech_lms",
        control_selector='[data-vibe-control="simulated-range"], input[type="range"]',
        input_variable="simulatedValue",
        target_value=16.0,
        bound_metrics=["curriculum-completion", "weekly-pacing"],
        expected_direction="positive",
        description="Weekly study commitment slider adjusting projected syllabus completion"
    ),
    "logistics_supply_chain": InteractionContract(
        domain_id="logistics_supply_chain",
        control_selector='[data-vibe-control="simulated-range"], input[type="range"]',
        input_variable="simulatedValue",
        target_value=180.0,
        bound_metrics=["fuel-burn", "fleet-latency"],
        expected_direction="recalculated",
        description="Active transit fleet slider adjusting aggregate fuel burn and dispatch latency"
    ),
    "energy_greentech_sustainability": InteractionContract(
        domain_id="energy_greentech_sustainability",
        control_selector='[data-vibe-control="simulated-range"], input[type="range"]',
        input_variable="simulatedValue",
        target_value=18.5,
        bound_metrics=["co2-offset", "annual-grid-export"],
        expected_direction="positive",
        description="Solar array capacity slider adjusting annual CO2 offset and grid revenue"
    ),
    "cybersecurity_identity_auth": InteractionContract(
        domain_id="cybersecurity_identity_auth",
        control_selector='[data-vibe-control="simulated-range"], input[type="range"]',
        input_variable="simulatedValue",
        target_value=7500.0,
        bound_metrics=["anomalies-intercepted", "zero-trust-mttr"],
        expected_direction="recalculated",
        description="Endpoint ingress monitor adjusting intercepted attack telemetry and MTTR"
    ),
    "food_restaurant_cafe": InteractionContract(
        domain_id="food_restaurant_cafe",
        control_selector='[data-vibe-control="simulated-range"], input[type="range"]',
        input_variable="simulatedValue",
        target_value=8.0,
        bound_metrics=["tasting-subtotal", "pairing-allocation"],
        expected_direction="positive",
        description="Degustation guest seating slider adjusting multi-course subtotal and pairings"
    ),
    "travel_hospitality_tourism": InteractionContract(
        domain_id="travel_hospitality_tourism",
        control_selector='[data-vibe-control="simulated-range"], input[type="range"]',
        input_variable="simulatedValue",
        target_value=9.0,
        bound_metrics=["expedition-total", "concierge-credits"],
        expected_direction="positive",
        description="Expedition duration slider adjusting bespoke itinerary cost and credits"
    ),
    "legal_compliance_law": InteractionContract(
        domain_id="legal_compliance_law",
        control_selector='[data-vibe-control="simulated-range"], input[type="range"]',
        input_variable="simulatedValue",
        target_value=1400.0,
        bound_metrics=["clause-audit-time", "retained-exposure"],
        expected_direction="recalculated",
        description="Contract portfolio volume slider adjusting forensic audit hours and liability"
    ),
    "media_editorial_magazine": InteractionContract(
        domain_id="media_editorial_magazine",
        control_selector='[data-vibe-control="simulated-range"], input[type="range"]',
        input_variable="simulatedValue",
        target_value=250000.0,
        bound_metrics=["readership-reach", "read-through-retention"],
        expected_direction="recalculated",
        description="Syndication reach slider adjusting readership volume and read-through depth"
    ),
    "gaming_entertainment_streaming": InteractionContract(
        domain_id="gaming_entertainment_streaming",
        control_selector='[data-vibe-control="simulated-range"], input[type="range"]',
        input_variable="simulatedValue",
        target_value=120.0,
        bound_metrics=["render-fps", "frame-frametime"],
        expected_direction="recalculated",
        description="Target framerate slider adjusting hardware render pipeline and frametime"
    ),
    "ai_developer_platform": InteractionContract(
        domain_id="ai_developer_platform",
        control_selector='[data-vibe-control="simulated-range"], input[type="range"]',
        input_variable="simulatedValue",
        target_value=8500000.0,
        bound_metrics=["token-cost", "ttft-latency"],
        expected_direction="recalculated",
        description="Model inference token slider adjusting billing cost and time-to-first-token"
    ),
    "creative_portfolio_agency": InteractionContract(
        domain_id="creative_portfolio_agency",
        control_selector='[data-vibe-control="simulated-range"], input[type="range"]',
        input_variable="simulatedValue",
        target_value=6.0,
        bound_metrics=["design-sprints", "agency-investment"],
        expected_direction="positive",
        description="Design sprint scope slider adjusting agency delivery timeline and budget"
    ),
    "saas_b2b_enterprise": InteractionContract(
        domain_id="saas_b2b_enterprise",
        control_selector='[data-vibe-control="simulated-range"], input[type="range"]',
        input_variable="simulatedValue",
        target_value=450.0,
        bound_metrics=["seat-license-mrr", "enterprise-sla"],
        expected_direction="positive",
        description="Enterprise seat allocation slider adjusting monthly subscription MRR and SLA"
    ),
    "nonprofit_charity_social": InteractionContract(
        domain_id="nonprofit_charity_social",
        control_selector='[data-vibe-control="simulated-range"], input[type="range"]',
        input_variable="simulatedValue",
        target_value=750.0,
        bound_metrics=["lives-supported", "impact-efficiency"],
        expected_direction="positive",
        description="Monthly patron contribution slider adjusting direct human lives supported"
    ),
    "personal_branding_creator": InteractionContract(
        domain_id="personal_branding_creator",
        control_selector='[data-vibe-control="simulated-range"], input[type="range"]',
        input_variable="simulatedValue",
        target_value=120000.0,
        bound_metrics=["creator-sponsorship", "audience-engagement"],
        expected_direction="positive",
        description="Subscriber community reach slider adjusting projected sponsorship pipeline"
    ),
    "ecommerce_mass_market": InteractionContract(
        domain_id="ecommerce_mass_market",
        control_selector='[data-vibe-control="simulated-range"], input[type="range"]',
        input_variable="simulatedValue",
        target_value=6.0,
        bound_metrics=["cart-subtotal", "bulk-discount"],
        expected_direction="positive",
        description="Bundle quantity slider adjusting checkout subtotal and volume tier discount"
    ),
    "general_modern_saas": InteractionContract(
        domain_id="general_modern_saas",
        control_selector='[data-vibe-control="simulated-range"], input[type="range"]',
        input_variable="simulatedValue",
        target_value=85.0,
        bound_metrics=["seat-allocation", "active-savings"],
        expected_direction="positive",
        description="Team size slider adjusting annual software license volume and cost savings"
    )
}


def get_interaction_contract(domain_id: str) -> InteractionContract:
    """Retrieves canonical InteractionContract for any domain with safe default fallback."""
    if domain_id in DOMAIN_INTERACTION_CONTRACTS:
        return DOMAIN_INTERACTION_CONTRACTS[domain_id]
    return DOMAIN_INTERACTION_CONTRACTS["general_modern_saas"]
