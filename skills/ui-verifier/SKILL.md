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

### Pillar 1: Living Visual & Screenshot Inspection (Harness-Native)
- **Light-First & Anti-Suffocating Gate (Constitution Standard):**
  - Verify that the interface is designed, structured, and visually verified in LIGHT THEME first (#ffffff/#f8fafc surfaces, #e2e8f0 borders, #0f172a text).
  - Enforce the Anti-Suffocating Rule: Zero flat pitch-black (#000000, #0a0a0a) or muddy grey voids. Dark mode must exhibit OLED cockpit depth (#0b0f19, #0f172a) with specular highlights.
- **Measurement Method:** Use only the browser exposed by the active AI harness. The suite never installs, launches or controls a browser. Capture Mobile (390px), Tablet (768px) and Desktop (1440px) screenshots, including the complete page.
- **Vision Review:** A vision-capable reviewer must inspect every screenshot for whitespace cadence, optical balance, alignment, typography, clipping, image quality and domain fit.
- **Evidence Contract:** Submit vibe.browser-evidence/v1 bound to the final artifact SHA-256. Validate it with `vibe-ui-suite browser-evidence validate <report.json> --artifact <file>`. Missing, stale or invalid evidence is NOT_EVALUATED, never PASS.
- **Novelty & Anti-Slop Audit:**- **Novelty & Anti-Slop Audit:** Audit visual chemistry against the 5 archetypes and verify the **Novelty Budget** (at least 2 of 6 structural dimensions—hero composition, card geometry, background treatment, typography pairing, CTA style, lighting—differ from previous outputs to prevent template collapse). Verify real CDN photography from `skills/ui-kit/references/curated_unsplash_vault.md` rather than empty gray placeholder boxes.

### Pillar 2: Responsive Multi-Device Integrity
- **Measurement Method:** Verify CSS rules across 3 critical viewport widths.
- **Evidence Required:**
  - **Mobile (375px/390px):** Zero horizontal scroll blowouts (`overflow-x: hidden` / flex wrapping confirmed). Touch targets conform to **WCAG 2.2 AA (min $24 \times 24\text{px}$)**, with **$44 \times 44\text{px}$ design best practice** recommended for primary mobile CTAs.
  - **Tablet (768px):** Asymmetric Bento grids collapse gracefully into balanced 1-column or 2-column stacks.
  - **Desktop (1440px+):** Max-width containers (`max-w-7xl` or equivalent) prevent awkward stretching.

### Pillar 3: Accessibility & WCAG 2.2 AA Compliance (Affordance & Functional Integrity)
- **Measurement Method:** Count interactive elements, check contrast, verify ARIA states, test keyboard traversal and escape-to-close behavior.
- **Evidence Required:**
  - **Semantic Controls (R-39):** $X/X$ clickables use `<button type="button">` or `<a href="...">` (zero `<div onclick>`). Enabled controls declare `cursor: pointer` in CSS; disabled controls declare `cursor: not-allowed`.
  - **Functional Completeness (R-26):** Every clickable button/link triggers a real behavior (modal disclosure, accordion toggle, smooth scroll to existent section ID, or form validation). Zero dead buttons. Modals/drawers must support `Escape` key dismissal.
  - **Navbar Link Integrity (R-24):** 100% of navbar links point to sections that physically exist in the DOM (zero ghost navigation).
  - **Visible Focus Rings (R-32):** $X/X$ interactive elements feature `focus-visible:ring-2` with sufficient contrast.
  - **State Semantics:** Dynamic disclosures, accordions, and sheets provide `aria-expanded` and `aria-controls`.
  - **Color Contrast (R-25):** Sampled text nodes meet minimum $4.5:1$ contrast ratio against background tokens across full gradient bounds.
  - **Functional Reduced Motion:** Non-essential decorative loops, parallax, and ambient meshes disabled via `@media (prefers-reduced-motion: reduce)`; functional state feedback transitions preserved with snappy durations ($\le 150\text{ms}$).

### Pillar 4: Performance & Web Vitals Budget (Core Web Vitals & Compositing)
- **Measurement Method:** Inspect media tags for dimensions/aspect-ratio, hero loading attributes, stacked blur layers, vector icons, and script tags.
- **Evidence Required:**
  - **Explicit Media Sizing (R-40 CLS Prevention):** 100% of `<img>`, `<video>`, and `<iframe>` elements declare explicit `width` and `height` attributes or CSS `aspect-ratio` to reserve layout bounds and eliminate Cumulative Layout Shift.
  - **Hero Image Contract (R-40 LCP Budget):** Above-the-fold hero image is a native `<img>` tag in the HTML, never `loading="lazy"`, with `fetchpriority="high"` declared.
  - **Zero Render-Blocking Scripts (R-40):** Zero render-blocking third-party scripts in `<head>`. Non-critical scripts use `defer`/`async` or load on interaction.
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
│ 1. Living Visual & Screenshot Inspection (Harness Multi-VP)  │
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
│ 3. Accessibility & WCAG 2.2 AA (Functional Integrity)           │
│    [PASS] Semantic Clickables: 12/12 buttons/anchors (0 div onclick)│
│    [PASS] Functional Actions : 12/12 elements active (0 dead controls)│
│    [PASS] Navbar Link Targets: 5/5 nav items point to real DOM IDs│
│    [PASS] Focus Rings & A11y : 12/12 focus-visible & contrast ok│
│                                                                 │
│ 4. Performance & Web Vitals Budget                              │
│    [PASS] Media Layout Sizing: 100% img/video have explicit dims│
│    [PASS] Hero LCP Contract  : fetchpriority="high", no lazy img│
│    [PASS] Backdrop Blur      : 2 active layers (budget max: 5)  │
│    [PASS] Vector Iconography : 0 raw emojis, inline SVGs used   │
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
| **1. Living Visual Inspection** | ✅ PASS | Harness-provided 390px/768px/1440px screenshots inspected and evidence SHA verified; 0 template slop. |
| **2. Responsive Design** | ✅ PASS | Fluid across 390px, 768px, and 1440px with no horizontal overflow. |
| **3. Accessibility (WCAG)** | ✅ PASS | Semantic `<button>` elements, visible focus, reduced-motion handled. |
| **4. Motion & Performance** | ✅ PASS | GPU-friendly compositing (<=5 blur layers), inline SVGs, rAF interpolation. |
| **5. Semantic RTL & BiDi** | [PASS / N/A (LTR Default)] | Evaluated strictly for RTL/Persian interfaces; passes as N/A on pure English LTR. |
```
