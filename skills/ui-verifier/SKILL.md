---
name: ui-verifier
description: Complete 5-Pillar UI & Frontend Quality Verification Engine (WCAG AA Accessibility, Responsive Breakpoints, Anti-Slop Visual Architecture, Sub-Pixel rAF Motion Performance, and Semantic RTL/BiDi Resilience).
triggers: ["verify ui", "ui-verifier", "audit ui", "a11y check", "check design", "responsive audit", "ui inspection", "frontend audit", "design review"]
---

# 🔍 UI-Verifier: 5-Pillar Frontend Quality & Verification Engine

## 🎯 Purpose
The `ui-verifier` skill provides automated, rigorous quality gates for generated interfaces. It acts as an autonomous design auditor, ensuring that code synthesized by `vibe-ui-agent` (utilizing `visual-chemistry-engine` and `ui-kit`) meets international engineering, accessibility, and aesthetic standards.

---

## 🏛️ The 5 Verification Pillars

Whenever asked to audit, verify, or review any web page, component, or frontend generation, execute this 5-stage inspection:

```
┌─────────────────────────────────────────────────────────────┐
│                   🔍 UI-VERIFIER PIPELINE                   │
└─────────────────────────────────────────────────────────────┘
  │
  ├─► [1] Living Visual & Screenshot Inspection (Eyes on Render)
  ├─► [2] Responsive Multi-Device Integrity (375px / 768px / 1440px)
  ├─► [3] Accessibility & WCAG AA (Keyboard, ARIA, Reduced Motion)
  ├─► [4] Performance & Compositing Budget (Clean CSS, Vectors)
  └─► [5] On-Demand RTL & BiDi Stability (Only when RTL requested)
```

---

### Pillar 1: Anti-Slop Visual & Novelty Audit
- **Measurement Method:** Audit visual chemistry against the 5 archetypes and verify the **Novelty Budget**.
- **Evidence Required:**
  - Specified visual chemistry (e.g., *Minimalist SaaS*, *Neobrutalism*, *Swiss Editorial*).
  - Novelty check: At least 2 of 6 structural dimensions (hero composition, card geometry, background treatment, typography pairing, CTA style, lighting) differ from previous outputs to prevent template collapse.

### Pillar 2: Responsive Multi-Device Integrity
- **Measurement Method:** Verify CSS rules across 3 critical viewport widths.
- **Evidence Required:**
  - **Mobile (375px):** Zero horizontal scroll blowouts (`overflow-x: hidden` / flex wrapping confirmed). Touch targets conform to **WCAG 2.2 AA (min $24 \times 24\text{px}$)**, with **$44 \times 44\text{px}$ design best practice** recommended for primary mobile CTAs.
  - **Tablet (768px):** Asymmetric Bento grids collapse gracefully into balanced 1-column or 2-column stacks.
  - **Desktop (1440px+):** Max-width containers (`max-w-7xl` or equivalent) prevent awkward stretching.

### Pillar 3: Accessibility & WCAG 2.2 AA Compliance
- **Measurement Method:** Count interactive elements, check contrast, verify ARIA states.
- **Evidence Required:**
  - **Semantic Controls:** $X/X$ clickables use `<button type="button">` or `<a href="...">` (zero `<div onclick>`).
  - **Visible Focus Rings:** $X/X$ interactive elements feature `focus-visible:ring-2` with sufficient contrast.
  - **State Semantics:** Dynamic disclosures, accordions, and sheets provide `aria-expanded` and `aria-controls`.
  - **Color Contrast:** Sampled text nodes meet minimum $4.5:1$ contrast ratio against background tokens.
  - **Functional Reduced Motion:** Non-essential decorative loops, parallax, and ambient meshes disabled via `@media (prefers-reduced-motion: reduce)`; functional state feedback transitions preserved with snappy durations ($\le 150\text{ms}$).

### Pillar 4: Performance & Rendering Compositing Budget
- **Measurement Method:** Count stacked blur layers, inspect SVG icons, verify animation drivers.
- **Evidence Required:**
  - **Backdrop Blur Layers:** Detected active `backdrop-filter: blur(...)` elements (Threshold: $\le 8$ active layers simultaneously, calibrated for rich floating docks and multi-tier glassmorphism).
  - **Zero Emojis:** Zero raw unicode emojis used as interface icons; verified inline SVG vector paths.
  - **Frame Driver:** Continuous interactive elements (sliders, spring tilts) driven via `requestAnimationFrame`.

### Pillar 5: On-Demand RTL & BiDi Resilience (Applies to RTL/Bilingual Targets)
- **Activation Scope:** Evaluated exclusively on Persian/RTL interfaces or bilingual UIs with RTL support (`RTL.md`). For pure English interfaces, this pillar evaluates as N/A or passes without imposing RTL overhead.
- **Measurement Method:** Inspect bidirectional CSS logical properties, non-mirrored layout, and font independence.
- **Evidence Required:**
  - **Zero Layout Mirroring:** Macro grid coordinates, traffic lights, and component columns physically locked in LTR coordinates.
  - **Font Independence:** English copy retains default English fonts (Inter, Geist, sans-serif); Vazirmatn is scoped strictly to Persian characters.
  - **BiDi Punctuation Isolation:** Mixed sentences with English terms (`Claude Code`, `Tailwind`, `API`) wrapped in `<bdi>` or styled with `unicode-bidi: isolate`.
  - **Pure Monospace LTR:** Code blocks, CLI commands, telemetry digits, and URLs explicitly styled with `direction: ltr !important; text-align: left !important`.

---

## 📋 Mandatory Output Scorecard Schema

When evaluating or generating any frontend code, `ui-verifier` outputs a structured evidence scorecard:

```text
┌─────────────────────────────────────────────────────────────────┐
│                 📊 UI-VERIFIER AUDIT SCORECARD                  │
├─────────────────────────────────────────────────────────────────┤
│ Overall Status: [ PASS | WARN | FAIL ]                          │
├─────────────────────────────────────────────────────────────────┤
│ 1. Accessibility (WCAG 2.2 AA)                                  │
│    [PASS] Keyboard Traversal : 12/12 elements keyboard reachable│
│    [PASS] Focus Rings        : 12/12 have focus-visible states  │
│    [PASS] Color Contrast     : Min 5.4:1 (exceeds 4.5:1 minimum)│
│    [PASS] Functional Motion  : prefers-reduced-motion enforced  │
│                                                                 │
│ 2. Responsive Breakpoints                                       │
│    [PASS] Mobile 375px       : 0 horizontal overflow violations │
│    [PASS] Touch Targets      : Meets WCAG AA (>= 24px, CTA 44px)│
│    [PASS] Desktop 1440px     : max-w-7xl container bounded      │
│                                                                 │
│ 3. Performance & Compositing Budget                             │
│    [PASS] Backdrop Blur Layers: 2 active layers (budget max: 3) │
│    [PASS] Vector Iconography : 0 raw emojis, 6 SVG paths used   │
│    [PASS] Motion Driver      : rAF-based sub-pixel interpolation│
│                                                                 │
│ 4. Semantic RTL & BiDi Stability                                │
│    [PASS] Macro Layout       : Coordinate grid physically locked│
│    [PASS] BiDi Punctuation   : <bdi> wrappers on brand terms    │
│    [PASS] Monospace LTR      : Code/metrics locked in LTR font  │
│                                                                 │
│ 5. Visual Novelty & Anti-Slop                                   │
│    [PASS] Visual Chemistry   : Minimalist SaaS Archetype applied│
│    [PASS] Novelty Budget     : 3/6 structural dimensions unique │
└─────────────────────────────────────────────────────────────────┘
```

- **PASS:** All critical checks pass. Code is production-ready.
- **WARN:** Non-breaking advisory (e.g., 4 blur layers detected; advisory to reduce to 3 on mobile).
- **FAIL:** Blocking defect detected (e.g., `<div onclick>`, missing focus ring, 375px layout blowout, unisolated BiDi punctuation). Execution must pause and fix before completion.

---

## 📋 Standard Audit Report Template

When conducting an audit, output findings using this concise scorecard:

```markdown
### 🔍 UI Quality Verification Scorecard

| Pillar | Status | Key Observations & Verified Items |
| :--- | :---: | :--- |
| **1. Visual Architecture** | ✅ PASS | Distinct visual chemistry, clear visual hierarchy. |
| **2. Responsive Design** | ✅ PASS | Fluid across 375px, 768px, and 1440px with no horizontal overflow. |
| **3. Accessibility (WCAG)** | ✅ PASS | Semantic `<button>` elements, visible focus, reduced-motion handled. |
| **4. Motion & Performance** | ✅ PASS | GPU-friendly compositing, SVG vectors, rAF interpolation. |
| **5. Semantic RTL & BiDi** | ✅ PASS | Macro layout stable, mixed English/Persian punctuation intact, telemetry in LTR. |
```
