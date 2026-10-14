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

### Pillar 1: Living Visual & Screenshot Inspection (Playwright Multi-Viewport)
- **Measurement Method:** Execute automated headless Chromium rendering via `python scripts/screenshot_audit.py <file>` or `vibe_cli.py screenshot <file>`. Capture both **Desktop (1440px)** and **Mobile (390px)** viewports into `.test-artifacts/screenshots/`.
- **Vision Review:** Inspect captured PNGs directly (`view_file`) to audit whitespace cadence, optical balance, alignment, typographic contrast, and card boundaries.
- **Novelty & Anti-Slop Audit:** Audit visual chemistry against the 5 archetypes and verify the **Novelty Budget** (at least 2 of 6 structural dimensions—hero composition, card geometry, background treatment, typography pairing, CTA style, lighting—differ from previous outputs to prevent template collapse). Verify real CDN photography from `skills/ui-kit/references/curated_unsplash_vault.md` rather than empty gray placeholder boxes.

### Pillar 2: Responsive Multi-Device Integrity
- **Measurement Method:** Verify CSS rules across 3 critical viewport widths.
- **Evidence Required:**
  - **Mobile (375px/390px):** Zero horizontal scroll blowouts (`overflow-x: hidden` / flex wrapping confirmed). Touch targets conform to **WCAG 2.2 AA (min $24 \times 24\text{px}$)**, with **$44 \times 44\text{px}$ design best practice** recommended for primary mobile CTAs.
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
  - **Backdrop Blur Layers:** Detected active `backdrop-filter: blur(...)` elements (Threshold: $\le 5$ active layers simultaneously, reduced to $\le 2$ on mobile).
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
│ 1. Living Visual & Screenshot Inspection (Playwright Multi-VP)  │
│    [PASS] Multi-Viewport PNG : 1440px & 390px screenshots viewed│
│    [PASS] Visual Hierarchy   : Whitespace & typography balanced │
│    [PASS] Novelty Budget     : 3/6 structural dimensions unique │
│    [PASS] Curated CDN Assets : Real photography, 0 gray boxes   │
│                                                                 │
│ 2. Responsive Breakpoints                                       │
│    [PASS] Mobile 390px/375px : 0 horizontal overflow violations │
│    [PASS] Touch Targets      : Meets WCAG AA (>= 24px, CTA 44px)│
│    [PASS] Desktop 1440px     : max-w-7xl container bounded      │
│                                                                 │
│ 3. Accessibility & WCAG 2.2 AA                                  │
│    [PASS] Keyboard Traversal : 12/12 elements keyboard reachable│
│    [PASS] Focus Rings        : 12/12 have focus-visible states  │
│    [PASS] Color Contrast     : Min 5.4:1 (exceeds 4.5:1 minimum)│
│    [PASS] Functional Motion  : prefers-reduced-motion enforced  │
│                                                                 │
│ 4. Performance & Compositing Budget                             │
│    [PASS] Backdrop Blur Layers: 2 active layers (budget max: 5) │
│    [PASS] Vector Iconography : 0 raw emojis, inline SVGs used   │
│    [PASS] Motion Driver      : rAF-based sub-pixel interpolation│
│                                                                 │
│ 5. Semantic RTL & BiDi Stability                                │
│    [PASS / N/A (LTR Default)] Macro Layout : Coordinate grid locked │
│    [PASS / N/A (LTR Default)] BiDi Wrapper : <bdi> on brand tokens  │
│    [PASS / N/A (LTR Default)] Monospace LTR: Code/metrics locked LTR│
└─────────────────────────────────────────────────────────────────┘
```

- **PASS:** All critical checks pass. Code is production-ready.
- **WARN:** Non-breaking advisory (e.g., 4 blur layers detected; advisory to reduce to max 2 on mobile).
- **FAIL:** Blocking defect detected (e.g., `<div onclick>`, missing focus ring, 375px layout blowout, unisolated BiDi punctuation). Execution must pause and fix before completion.

---

## 📋 Standard Audit Report Template

When conducting an audit, output findings using this concise scorecard:

```markdown
### 🔍 UI Quality Verification Scorecard

| Pillar | Status | Key Observations & Verified Items |
| :--- | :---: | :--- |
| **1. Living Visual Inspection** | ✅ PASS | Playwright 1440px/390px screenshots captured & inspected; 0 template slop. |
| **2. Responsive Design** | ✅ PASS | Fluid across 390px, 768px, and 1440px with no horizontal overflow. |
| **3. Accessibility (WCAG)** | ✅ PASS | Semantic `<button>` elements, visible focus, reduced-motion handled. |
| **4. Motion & Performance** | ✅ PASS | GPU-friendly compositing (<=5 blur layers), inline SVGs, rAF interpolation. |
| **5. Semantic RTL & BiDi** | [PASS / N/A (LTR Default)] | Evaluated strictly for RTL/Persian interfaces; passes as N/A on pure English LTR. |
```
