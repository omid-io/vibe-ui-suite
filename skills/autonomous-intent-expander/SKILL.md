---
name: autonomous-intent-expander
description: Opinionated 30-parameter intent expansion engine that synthesizes complete technical, aesthetic, and architectural specifications from sparse prompts using a calibrated Ambiguity Budget.
triggers: ["expand intent", "auto-spec", "read my mind", "full architecture", "scale this", "deepen constraints", "lazy prompt", "complete website design", "requirements spec"]
---

# 🧠 Autonomous Intent Expander (30-Parameter Specification Engine)

## 🎯 Purpose & Philosophy
The `autonomous-intent-expander` skill eliminates friction and interrogation fatigue while preventing blind hallucinations. When a user provides a minimal or ambiguous prompt (e.g., *"Build gym website"*, *"Design aesthetic dental clinic website"*), this engine applies **opinionated default inference** governed by a strict **Ambiguity Budget**.

---

## ⚙️ Operating Rules & Ambiguity Budget

1. **The 3-Tier Ambiguity Budget:**
   - **Tier 1: Visual, Aesthetic & Component Selection (100% Autonomous):**
     Do NOT interrogate the user for layout, color palettes, visual chemistries, or component choices. Select the most cohesive, modern default and implement it directly.
   - **Tier 2: Product Architecture & Standard Workflows (Autonomous with Stated Assumptions):**
     Infer standard industry user flows and data shapes. Always report these under a clear `⚠️ Assumptions Made:` section so the user can steer if needed, without halting execution.
   - **Tier 3: High-Risk Logic, Financials, Auth & Legal/Compliance (Zero Guesswork):**
     Never blindly guess transaction logic, payment split math, HIPAA/GDPR constraints, or authentication models. If critical information is missing that changes liability or data integrity, surface the exact decision fork.

2. **Domain Archetype & 24 Taxonomy Classification:**
   The expander queries `scripts/search.py` (<10ms zero-token retrieval) and aligns with the 24 canonical domains in `data/taxonomy.json`, 24 architectural blueprints in `data/domain_blueprints.json`, and 26 orthogonal style families in `data/styles.json`:
   - `beauty_clinical_wellness` (Quiet Luxury / Soft Humanist / Warm Light)
   - `fintech_banking` (Clean Stripe / Minimal Swiss / High-Trust Light)
   - `crypto_trading_web3` (Linear Dark / Terminal HUD / Live Telemetry)
   - `devops_cloud_terminal` (Data-Dense Terminal / Linear Dark)
   - `saas_b2b_enterprise` (Clean Stripe / Minimal Swiss / Executive ROI)
   - `ai_developer_platform` (Linear Dark / Modern Glass 2.0 / Reasoning HUD)
   - `creative_portfolio_agency` (Neo-Brutalism / Editorial / Magnetic Bento)
   - Plus 17 additional specialized domains with bilingual Persian/English blueprints.
   - **Stack-Sensor Integration:** Automatically detects React 18/19, Tailwind v3/v4, and existing CSS tokens via `vibe_core.stack_sensor`.

2.1. **Fast Zero-Token Retrieval Command:**
   ```bash
   python scripts/search.py "<user prompt>" --pretty
   ```

3. **Structured Specification Pipeline (Core vs. Conditional Parameters):**
   Synthesizes an explicit architectural contract without inflating irrelevant metadata:
   
   **A. Core Parameters (Universal for all interfaces):**
   - **P01-P05: Intent & Product Foundations** (Archetype, Target Persona, Core Job-To-Be-Done, Primary CTA, Secondary Micro-Action).
   - **P06-P08: Trust & Value Mechanics** (Objection Neutralization, Evidence Density, Transparent Risk Reversal).
   - **P09-P13: Visual Chemistry & Tokens** (Canvas Base, Surface Layers, Accent Palette, Functional Colors, Border Radius).
   - **P14-P17: Typography & Spatial Rhythm** (Display Font, Body Font, Tabular Metric Font, 8pt Spacing Cadence).
   - **P18-P21: Motion & Interaction Model** (Scroll Mechanics, Interactive Hero Module, SVG Vector Iconography, Transition Curves).
   - **P22-P24: Narrative & Copy Architecture** (BLUF Value Hook, Problem/Solution Matrix, Brand Voice Register).
   
   **B. Conditional Domain Parameters (Synthesized only when contextually relevant):**
   - **P25: Local Geo-Coordinates & Address** *(Conditional: Local Trades, Hospitality, Brick-and-Mortar only; skipped for SaaS).*
   - **P26: Clinical / Board Certification Proof** *(Conditional: Healthcare, Medical, Legal only).*
   - **P27: Public Web Schema & Wikidata Entity Graph** *(Conditional: Public discoverable SEO sites only; skipped for internal dashboards).*
   - **P28: Financial Math & Transaction Guardrails** *(Conditional: FinTech, Trading, Payment flows only).*
   - **P29-P30: Performance & Isolation Budgets** (Core Web Vitals Budget, Boundary Isolation).

---

## 📄 4. Canonical Machine-Readable Output (`design-spec.json`)

When requested or when compiling specs for downstream build pipelines, `autonomous-intent-expander` outputs this formal JSON Design Contract:

```json
{
  "$schema": "../../schemas/design-spec.v1.schema.json",
  "spec_version": "2.2.0",
  "domain_archetype": "HIGH_PERFORMANCE_SAAS",
  "visual_chemistry": "MINIMALIST_SAAS",
  "core_parameters": {
    "primary_palette": {
      "canvas_oklch": "oklch(0.14 0.005 260)",
      "surface_oklch": "oklch(0.18 0.008 260)",
      "primary_accent_oklch": "oklch(0.65 0.22 265)",
      "border_oklch": "oklch(0.28 0.01 260)"
    },
    "typography_pair": {
      "display_font": "Inter, system-ui, sans-serif",
      "body_font": "Inter, system-ui, sans-serif",
      "mono_font": "JetBrains Mono, monospace"
    },
    "surface_treatment": "subtle_mesh_glow_with_svg_noise",
    "grid_density": "bento_asymmetric",
    "hero_composition": "split_terminal"
  },
  "accessibility_contract": {
    "wcag_level": "AA",
    "min_touch_target_px": 24,
    "target_recommendation_px": 44,
    "focus_visible_required": true,
    "reduced_motion_strategy": "functional_only"
  },
  "semantic_rtl_contract": {
    "enabled": true,
    "physical_macro_stability": true,
    "bidi_isolation": true,
    "code_ltr_enforced": true
  },
  "novelty_budget": {
    "dimensions_varied": [
      "hero_composition",
      "grid_density",
      "accent_palette"
    ],
    "entropy_heuristic": 0.85
  }
}
```
