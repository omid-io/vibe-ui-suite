---
name: autonomous-intent-expander
description: Streamlined intent expansion engine that synthesizes architectural specifications from sparse prompts anchored in the Two Golden Pillars (Trend Inspiration & Living Visual Feedback).
triggers: ["expand intent", "auto-spec", "read my mind", "full architecture", "scale this", "deepen constraints", "lazy prompt", "complete website design", "requirements spec"]
---

# 🧠 Autonomous Intent Expander (v6.1.1 Architecture Core)

## 🎯 Purpose & Philosophy
The `autonomous-intent-expander` skill eliminates friction and interrogation fatigue while preventing blind hallucinations. When a user provides a minimal or ambiguous prompt (e.g., *"Build gym website"*, *"Design aesthetic dental clinic website"*), this engine applies **opinionated default inference** governed by **The Four Architectural Mandates (v6.1.1)**:
1. **Mandate 1: Strict Light-First Canvas & Anti-Dark-Bias Invariant** (Defaulting canvas to crisp, luminous Light Mode unless the prompt explicitly requests dark or the archetype is inherently dark, alongside an accessible Dark Mode toggle).
2. **Mandate 2: Unrushed, Deliberate Craft & Multi-Pass Inspection** (Unbounded creative refinement loop; allocating cognitive budget to polish visuals and typography).
3. **Mandate 3: Living Ambient Hero Video & Fluid Canvas Loops** (Proactively planning lightweight, cinematic ambient video loops or fluid interactive canvas backgrounds for hero focal points).
4. **Mandate 4: Trend-First Pipeline** (Harvesting aesthetic trends from Dribbble, Figma Community, Mobbin, and Awwwards first, then mapping tools and assets to execute).


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

3. **The 6-Dimensional Streamlined Architecture:**
   Instead of overwhelming the agent's attention window with legacy parameter bloat, the expander synthesizes 6 essential dimensions:
   1. **D1: Domain Archetype & Target Persona** (Operational stakes, trust level, and primary conversion goal).
   2. **D2: Living Visual Direction & Vibrant Light Mode Default** (Crisp white canvas `#ffffff` / `oklch(0.99 0.002 260)`, surface `oklch(0.97 0.005 260)`, dark slate text `#0f172a`, and vibrant primary accent `oklch(0.55 0.22 260)`).
   3. **D3: Curated Real Imagery Specification** (High-res Unsplash CDN URLs from `data/unsplash_assets.json` and `skills/ui-kit/references/curated_unsplash_vault.md`).
   4. **D4: Typography & 8pt Spatial Rhythm** (Bold display headers, readable body font, and generous padding).
   5. **D5: Living Micro-States & Components** (Modular cards, active navigation, interactive sliders/tabs from `skills/ui-kit`).
   6. **D6: On-Demand RTL & Language Protocol** (Disabled by default; activated strictly on-demand for Persian/Arabic queries with `<bdi>` isolation).

---

## 📄 4. Canonical Machine-Readable Output (`design-spec.json`)

When requested or when compiling specs for downstream build pipelines, `autonomous-intent-expander` outputs this clean JSON Design Contract:

```json
{
  "$schema": "../../schemas/design-spec.v1.schema.json",
  "spec_version": "6.0.0",
  "domain_archetype": "HIGH_PERFORMANCE_SAAS",
  "visual_chemistry": "STRIPE_CRISP_LIGHT",
  "core_parameters": {
    "primary_palette": {
      "canvas_oklch": "oklch(0.99 0.002 260)",
      "surface_oklch": "oklch(0.97 0.005 260)",
      "primary_accent_oklch": "oklch(0.55 0.22 260)",
      "border_oklch": "oklch(0.92 0.008 260)"
    },
    "typography_pair": {
      "display_font": "Plus Jakarta Sans, Inter, system-ui, sans-serif",
      "body_font": "Inter, system-ui, sans-serif",
      "mono_font": "JetBrains Mono, monospace"
    },
    "surface_treatment": "crisp_light_with_subtle_elevation",
    "grid_density": "bento_asymmetric",
    "hero_composition": "split_visual_showcase"
  },
  "asset_strategy": {
    "provider": "curated_unsplash_vault",
    "domain_key": "saas_b2b_enterprise",
    "dimensions": {
      "hero": "&auto=format&fit=crop&w=1200&q=80",
      "card": "&auto=format&fit=crop&w=600&h=400&q=80"
    }
  },
  "accessibility_contract": {
    "wcag_level": "AA",
    "min_touch_target_px": 24,
    "target_recommendation_px": 44,
    "focus_visible_required": true,
    "reduced_motion_strategy": "functional_only"
  },
  "semantic_rtl_contract": {
    "enabled": false,
    "physical_macro_stability": true,
    "bidi_isolation": false,
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
