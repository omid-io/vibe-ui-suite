"""
vibe_core.interaction_contract — Deterministic Interaction Contracts for 24 Canonical Domains (v4.0.0)
Defines semantic control targeting, input variable bounds, test sweep parameters,
and fine-grained per-metric causal & directional assertion invariants for Chromium Browser Truth.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional


@dataclass
class MetricContract:
    metric_id: str
    label: str
    expected_direction: str  # "positive", "negative", "recalculated"
    formula_expr: str = ""
    tolerance: float = 0.05


@dataclass
class InteractionContract:
    domain_id: str
    control_selector: str
    input_variable: str
    target_value: float
    description: str
    metrics: List[MetricContract] = field(default_factory=list)
    # Backward compatibility properties
    bound_metrics: List[str] = field(default_factory=list)
    expected_direction: str = "positive"
    formula_expr: str = ""

    def __post_init__(self):
        if self.metrics and not self.bound_metrics:
            self.bound_metrics = [m.metric_id for m in self.metrics]
        if self.metrics and not self.formula_expr:
            self.formula_expr = self.metrics[0].formula_expr


# Canonical 24-Domain Interaction Specifications with Metric-Level Causal Contracts
DOMAIN_INTERACTION_CONTRACTS: Dict[str, InteractionContract] = {
    "beauty_clinical_wellness": InteractionContract(
        domain_id="beauty_clinical_wellness",
        control_selector='[data-vibe-control="split-slider"], input[type="range"]',
        input_variable="splitPos",
        target_value=65.0,
        description="Clinical split-view slider adjusting dermal reconstruction metrics",
        metrics=[
            MetricContract(
                metric_id="melanin-uniformity",
                label="Melanin Uniformity",
                expected_direction="positive",
                formula_expr="splitPos * 0.42"
            ),
            MetricContract(
                metric_id="collagen-index",
                label="Dermal Collagen Index",
                expected_direction="positive",
                formula_expr="62 + splitPos * 0.36"
            ),
        ]
    ),
    "fintech_banking": InteractionContract(
        domain_id="fintech_banking",
        control_selector='[data-vibe-control="simulated-range"], input[type="range"]',
        input_variable="simulatedValue",
        target_value=164250.0,
        description="Active capital allocation adjusting annual APY and daily liquidity",
        metrics=[
            MetricContract(
                metric_id="capital-deposit",
                label="Active Capital Allocation",
                expected_direction="positive",
                formula_expr="simulatedValue"
            ),
            MetricContract(
                metric_id="annual-yield",
                label="Est. Annual APY",
                expected_direction="positive",
                formula_expr="simulatedValue * 0.068"
            ),
            MetricContract(
                metric_id="daily-liquidity",
                label="T+0 Daily Liquidity",
                expected_direction="positive",
                formula_expr="(simulatedValue * 0.068) / 365"
            ),
        ]
    ),
    "crypto_trading_web3": InteractionContract(
        domain_id="crypto_trading_web3",
        control_selector='[data-vibe-control="simulated-range"], input[type="range"]',
        input_variable="simulatedValue",
        target_value=65350.0,
        description="Execution order volume adjusting order size and estimated pool slippage",
        metrics=[
            MetricContract(
                metric_id="order-volume",
                label="Execution Order Volume",
                expected_direction="positive",
                formula_expr="simulatedValue / 2850"
            ),
            MetricContract(
                metric_id="slippage-rate",
                label="Estimated Slippage",
                expected_direction="positive",
                formula_expr="0.02 + (simulatedValue / 100000) * 0.12"
            ),
        ]
    ),
    "devops_cloud_terminal": InteractionContract(
        domain_id="devops_cloud_terminal",
        control_selector='[data-vibe-control="simulated-range"], input[type="range"]',
        input_variable="simulatedValue",
        target_value=66750.0,
        description="Cluster replica scaler adjusting pod allocations, latency and throughput",
        metrics=[
            MetricContract(
                metric_id="node-count",
                label="Dynamic Node Cluster Capacity",
                expected_direction="positive",
                formula_expr="4 + (simulatedValue / 5000)"
            ),
            MetricContract(
                metric_id="cluster-latency",
                label="P99 Edge Latency",
                expected_direction="negative",  # Inversely proportional: more nodes -> lower latency
                formula_expr="max(12, 48 - (simulatedValue / 2500))"
            ),
            MetricContract(
                metric_id="network-throughput",
                label="Peak Throughput",
                expected_direction="positive",
                formula_expr="simulatedValue * 1.8"
            ),
        ]
    ),
    "saas_b2b_enterprise": InteractionContract(
        domain_id="saas_b2b_enterprise",
        control_selector='[data-vibe-control="simulated-range"], input[type="range"]',
        input_variable="simulatedValue",
        target_value=66750.0,
        description="Enterprise seat count adjusting annual labor savings and SLA guarantees",
        metrics=[
            MetricContract(
                metric_id="seat-allocation",
                label="Enterprise Active Seats",
                expected_direction="positive",
                formula_expr="simulatedValue / 500"
            ),
            MetricContract(
                metric_id="enterprise-savings",
                label="Annual Ops Savings",
                expected_direction="positive",
                formula_expr="(simulatedValue / 500) * 4200"
            ),
        ]
    ),
    "ai_developer_platform": InteractionContract(
        domain_id="ai_developer_platform",
        control_selector='[data-vibe-control="simulated-range"], input[type="range"]',
        input_variable="simulatedValue",
        target_value=32850.0,
        description="Monthly processed token budget adjusting VRAM, slots, and TTFT latency",
        metrics=[
            MetricContract(
                metric_id="token-budget",
                label="Monthly Processed Token Budget",
                expected_direction="positive",
                formula_expr="simulatedValue * 10000"
            ),
            MetricContract(
                metric_id="ttft-latency",
                label="Time-To-First-Token",
                expected_direction="negative",  # Inversely proportional: higher compute slots -> lower TTFT
                formula_expr="max(18, 95 - (simulatedValue / 800))"
            ),
            MetricContract(
                metric_id="gpu-slices",
                label="Active H100 GPU Slices",
                expected_direction="positive",
                formula_expr="max(2, simulatedValue / 6000)"
            ),
        ]
    ),
    "food_restaurant_cafe": InteractionContract(
        domain_id="food_restaurant_cafe",
        control_selector='[data-vibe-control="simulated-range"], input[type="range"]',
        input_variable="simulatedValue",
        target_value=68500.0,
        description="Degustation guest seating slider adjusting multi-course subtotal and pairings",
        metrics=[
            MetricContract(
                metric_id="guest-count",
                label="Private Dining & Tasting Guests",
                expected_direction="positive",
                formula_expr="max(2, simulatedValue / 10000)"
            ),
            MetricContract(
                metric_id="tasting-subtotal",
                label="Tasting Subtotal",
                expected_direction="positive",
                formula_expr="max(2, simulatedValue / 10000) * 185"
            ),
        ]
    ),
    "real_estate_architecture": InteractionContract(
        domain_id="real_estate_architecture",
        control_selector='[data-vibe-control="simulated-range"], input[type="range"]',
        input_variable="simulatedValue",
        target_value=68500.0,
        description="Architectural development slider adjusting spatial value and rent",
        metrics=[
            MetricContract(
                metric_id="capital-value",
                label="Portfolio Value",
                expected_direction="positive",
                formula_expr="simulatedValue * 50"
            ),
            MetricContract(
                metric_id="projected-rent",
                label="Projected Monthly Rent",
                expected_direction="positive",
                formula_expr="(simulatedValue * 50) * 0.0051"
            ),
        ]
    ),
    "healthcare_hospital_medical": InteractionContract(
        domain_id="healthcare_hospital_medical",
        control_selector='[data-vibe-control="simulated-range"], input[type="range"]',
        input_variable="simulatedValue",
        target_value=40750.0,
        description="Emergency room intake volume adjusting queue and triage wait",
        metrics=[
            MetricContract(
                metric_id="triage-queue",
                label="In Queue",
                expected_direction="positive",
                formula_expr="simulatedValue / 1500"
            ),
            MetricContract(
                metric_id="triage-wait",
                label="Triage Wait",
                expected_direction="positive",
                formula_expr="max(4, (simulatedValue / 1500) * 1.8)"
            ),
            MetricContract(
                metric_id="physicians-assigned",
                label="MDs Assigned",
                expected_direction="positive",
                formula_expr="12 + (simulatedValue / 5000)"
            ),
        ]
    ),
    "education_edtech_lms": InteractionContract(
        domain_id="education_edtech_lms",
        control_selector='[data-vibe-control="simulated-range"], input[type="range"]',
        input_variable="simulatedValue",
        target_value=66750.0,
        description="Weekly study commitment slider adjusting projected syllabus completion",
        metrics=[
            MetricContract(
                metric_id="weekly-study",
                label="Weekly Interactive Study Hours",
                expected_direction="positive",
                formula_expr="max(2, simulatedValue / 5000)"
            ),
            MetricContract(
                metric_id="completion-timeline",
                label="Weeks to Certification",
                expected_direction="negative",  # Inversely proportional: more hours -> fewer weeks to certify
                formula_expr="max(4, 160 / max(2, (simulatedValue / 5000)))"
            ),
        ]
    ),
    "creative_portfolio_agency": InteractionContract(
        domain_id="creative_portfolio_agency",
        control_selector='[data-vibe-control="simulated-range"], input[type="range"]',
        input_variable="simulatedValue",
        target_value=68500.0,
        description="Sprint scope slider adjusting prototype delivery horizon and conversion lift",
        metrics=[
            MetricContract(
                metric_id="sprint-scope",
                label="Design Sprints",
                expected_direction="positive",
                formula_expr="simulatedValue / 10000"
            ),
            MetricContract(
                metric_id="delivery-weeks",
                label="Delivery Horizon",
                expected_direction="positive",
                formula_expr="max(2, simulatedValue / 15000)"
            ),
            MetricContract(
                metric_id="conversion-lift",
                label="Conversion Lift",
                expected_direction="positive",
                formula_expr="24 + (simulatedValue / 10000) * 3.2"
            ),
        ]
    ),
    "ecommerce_luxury_fashion": InteractionContract(
        domain_id="ecommerce_luxury_fashion",
        control_selector='[data-vibe-control="simulated-range"], input[type="range"]',
        input_variable="simulatedValue",
        target_value=68500.0,
        description="Artisanal fabric weight adjusting bespoke atelier unit price",
        metrics=[
            MetricContract(
                metric_id="fabric-weight",
                label="Fabric Weight",
                expected_direction="positive",
                formula_expr="300 + (simulatedValue / 400)"
            ),
            MetricContract(
                metric_id="atelier-price",
                label="Atelier Unit Price",
                expected_direction="positive",
                formula_expr="1850 + (simulatedValue / 20)"
            ),
        ]
    ),
    "ecommerce_mass_market": InteractionContract(
        domain_id="ecommerce_mass_market",
        control_selector='[data-vibe-control="simulated-range"], input[type="range"]',
        input_variable="simulatedValue",
        target_value=33375.0,
        description="Cart volume slider adjusting tiered checkout subtotal and volume discount",
        metrics=[
            MetricContract(
                metric_id="cart-subtotal",
                label="Total Shopping Cart Value",
                expected_direction="positive",
                formula_expr="simulatedValue / 100"
            ),
            MetricContract(
                metric_id="volume-discount",
                label="Tiered Volume Discount",
                expected_direction="recalculated",  # Discount magnitude increases, signed as negative in UI
                formula_expr="simulatedValue > 25000 ? 25 : 15"
            ),
        ]
    ),
    "media_editorial_magazine": InteractionContract(
        domain_id="media_editorial_magazine",
        control_selector='[data-vibe-control="simulated-range"], input[type="range"]',
        input_variable="simulatedValue",
        target_value=66750.0,
        description="Investigative report depth adjusting monthly words and immersion time",
        metrics=[
            MetricContract(
                metric_id="wordcount-depth",
                label="Monthly Investigative Report Depth",
                expected_direction="positive",
                formula_expr="simulatedValue * 1.5"
            ),
            MetricContract(
                metric_id="reading-time",
                label="Read-Through Time",
                expected_direction="positive",
                formula_expr="(simulatedValue * 1.5) / 220"
            ),
        ]
    ),
    "travel_hospitality_tourism": InteractionContract(
        domain_id="travel_hospitality_tourism",
        control_selector='[data-vibe-control="simulated-range"], input[type="range"]',
        input_variable="simulatedValue",
        target_value=80800.0,
        description="Resort duration slider adjusting nights stay and total all-inclusive cost",
        metrics=[
            MetricContract(
                metric_id="nights-stay",
                label="Nights Stay",
                expected_direction="positive",
                formula_expr="max(3, simulatedValue / 8000)"
            ),
            MetricContract(
                metric_id="all-inclusive-price",
                label="All-Inclusive Total",
                expected_direction="positive",
                formula_expr="max(3, simulatedValue / 8000) * 480"
            ),
        ]
    ),
    "legal_compliance_law": InteractionContract(
        domain_id="legal_compliance_law",
        control_selector='[data-vibe-control="simulated-range"], input[type="range"]',
        input_variable="simulatedValue",
        target_value=66750.0,
        description="Contract portfolio volume slider adjusting forensic audit hours and liability",
        metrics=[
            MetricContract(
                metric_id="audited-contracts",
                label="Active Audited Contracts",
                expected_direction="positive",
                formula_expr="simulatedValue / 1000"
            ),
            MetricContract(
                metric_id="litigation-exposure",
                label="Litigation Exposure Reduction",
                expected_direction="recalculated",  # Risk reduction increases magnitude, formatted with minus sign
                formula_expr="72 + (simulatedValue / 10000) * 1.5"
            ),
        ]
    ),
    "gaming_entertainment_streaming": InteractionContract(
        domain_id="gaming_entertainment_streaming",
        control_selector='[data-vibe-control="simulated-range"], input[type="range"]',
        input_variable="simulatedValue",
        target_value=40750.0,
        description="Live 4K stream bitrate slider adjusting transmission bandwidth, FPS, and ping",
        metrics=[
            MetricContract(
                metric_id="framerate-target",
                label="Engine Render Frame Rate Target",
                expected_direction="positive",
                formula_expr="120 + (simulatedValue / 500)"
            ),
            MetricContract(
                metric_id="ping-latency",
                label="Tickrate / Ping Latency",
                expected_direction="negative",  # Inversely proportional: more bandwidth -> lower ping
                formula_expr="max(3, 18 - (simulatedValue / 5000))"
            ),
        ]
    ),
    "automotive_ev_mobility": InteractionContract(
        domain_id="automotive_ev_mobility",
        control_selector='[data-vibe-control="simulated-range"], input[type="range"]',
        input_variable="simulatedValue",
        target_value=66750.0,
        description="Battery pack capacity slider adjusting estimated driving range and capacity",
        metrics=[
            MetricContract(
                metric_id="battery-capacity",
                label="Active Battery Pack Capacity",
                expected_direction="positive",
                formula_expr="60 + (simulatedValue / 1250)"
            ),
            MetricContract(
                metric_id="ev-range",
                label="Real-World Range (WLTP)",
                expected_direction="positive",
                formula_expr="(60 + (simulatedValue / 1250)) * 6.4"
            ),
        ]
    ),
    "logistics_supply_chain": InteractionContract(
        domain_id="logistics_supply_chain",
        control_selector='[data-vibe-control="simulated-range"], input[type="range"]',
        input_variable="simulatedValue",
        target_value=66750.0,
        description="Active transit fleet slider adjusting aggregate vehicle units and fuel economy",
        metrics=[
            MetricContract(
                metric_id="fleet-units",
                label="Active Dispatched Fleet Units",
                expected_direction="positive",
                formula_expr="15 + (simulatedValue / 2000)"
            ),
            MetricContract(
                metric_id="fuel-economy",
                label="Fuel Economy Optimization",
                expected_direction="recalculated",  # Savings percentage magnitude increases, formatted with minus
                formula_expr="18.5 + (simulatedValue / 10000) * 1.2"
            ),
        ]
    ),
    "energy_greentech_sustainability": InteractionContract(
        domain_id="energy_greentech_sustainability",
        control_selector='[data-vibe-control="simulated-range"], input[type="range"]',
        input_variable="simulatedValue",
        target_value=66750.0,
        description="Solar array capacity slider adjusting annual CO2 offset and capacity",
        metrics=[
            MetricContract(
                metric_id="solar-capacity",
                label="Solar Microgrid Capacity",
                expected_direction="positive",
                formula_expr="50 + (simulatedValue / 1000)"
            ),
            MetricContract(
                metric_id="carbon-offset",
                label="Annual Carbon Offset",
                expected_direction="positive",
                formula_expr="(50 + (simulatedValue / 1000)) * 1.45"
            ),
        ]
    ),
    "nonprofit_charity_social": InteractionContract(
        domain_id="nonprofit_charity_social",
        control_selector='[data-vibe-control="simulated-range"], input[type="range"]',
        input_variable="simulatedValue",
        target_value=32850.0,
        description="Donation budget slider adjusting clean water filtration volume and community reach",
        metrics=[
            MetricContract(
                metric_id="donation-budget",
                label="Contribution Allocation",
                expected_direction="positive",
                formula_expr="simulatedValue / 20"
            ),
            MetricContract(
                metric_id="impact-beneficiaries",
                label="Community Beneficiaries",
                expected_direction="positive",
                formula_expr="(simulatedValue / 20) * 4"
            ),
        ]
    ),
    "personal_branding_creator": InteractionContract(
        domain_id="personal_branding_creator",
        control_selector='[data-vibe-control="simulated-range"], input[type="range"]',
        input_variable="simulatedValue",
        target_value=66750.0,
        description="Newsletter subscriber scale adjusting projected monthly reach and brand value",
        metrics=[
            MetricContract(
                metric_id="creator-subscribers",
                label="Total Active Subscribers",
                expected_direction="positive",
                formula_expr="simulatedValue * 2"
            ),
            MetricContract(
                metric_id="creator-revenue",
                label="Est. Monthly Sponsorships",
                expected_direction="positive",
                formula_expr="(simulatedValue * 2) * 0.045"
            ),
        ]
    ),
    "cybersecurity_identity_auth": InteractionContract(
        domain_id="cybersecurity_identity_auth",
        control_selector='[data-vibe-control="simulated-range"], input[type="range"]',
        input_variable="simulatedValue",
        target_value=66750.0,
        description="Endpoint ingress monitor adjusting intercepted attack telemetry and entities",
        metrics=[
            MetricContract(
                metric_id="active-entities",
                label="Monitored Entities",
                expected_direction="positive",
                formula_expr="simulatedValue / 10"
            ),
        ]
    ),
    "general_modern_saas": InteractionContract(
        domain_id="general_modern_saas",
        control_selector='[data-vibe-control="simulated-range"], input[type="range"]',
        input_variable="simulatedValue",
        target_value=65350.0,
        description="Core workflow event load adjusting throughput rate and system efficiency",
        metrics=[
            MetricContract(
                metric_id="workflow-volume",
                label="Total Executions",
                expected_direction="positive",
                formula_expr="simulatedValue"
            ),
            MetricContract(
                metric_id="time-savings",
                label="Saved Labor Hours",
                expected_direction="positive",
                formula_expr="simulatedValue * 0.041"
            ),
        ]
    ),
}


def get_interaction_contract(domain_id: str) -> InteractionContract:
    """Returns canonical InteractionContract for a given domain, defaulting to general_modern_saas."""
    return DOMAIN_INTERACTION_CONTRACTS.get(domain_id, DOMAIN_INTERACTION_CONTRACTS["general_modern_saas"])
