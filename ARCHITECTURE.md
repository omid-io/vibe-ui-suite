# 🏛️ Vibe UI Suite — System Architecture & Data Contract Specification

**Version:** 4.8.0 (Living Kinetic Standards & Kinetic Arrow Physics)  
**Status:** Feature Freeze (Production Certified)  
**Document Type:** Core Architectural Specification  
**Machine Contract Reference:** [`schemas/design-spec.v1.schema.json`](schemas/design-spec.v1.schema.json)  

---

## 1. Executive Overview & Architectural Philosophy

The **Vibe UI Skills Suite** is a contract-driven design engineering ecosystem designed for autonomous AI coding agents (such as Claude Code, Cursor, Antigravity, GitHub Copilot, and Windsurf). Standard frontier models default to generic visual archetypes—predictable `border-radius: 8px` cards, flat gray borders, cliché blue-to-purple gradients, missing AI execution states, and unstable RTL layout flips.

Vibe UI replaces ad-hoc prompt hacking with a **deterministic, contract-governed multi-skill architecture**. Commanded by the lead frontend architect agent **`mr-ui-designer`**, the system coordinates six modular sub-skills in a unidirectional pipeline that enforces strict visual diversity, mathematical physics, WCAG 2.2 AA accessibility, anti-dark-pattern copy, and structurally stable bidirectional rendering.

### Core Architectural Invariants
1. **Zero Hallucination of Data Shapes:** All UI generations are parameterized through the canonical JSON Schema (`design-spec.v1.schema.json`).
2. **Fixed-Structure Semantic RTL:** Macro layout grids remain physically stable; RTL directionality is scoped exclusively to text nodes, paired with `<bdi>` BiDi punctuation isolation and pure LTR telemetry.
3. **Strict Compositing Performance Budget:** A maximum cap of $\le 3$ active `backdrop-filter` blur surfaces is enforced across all viewports to protect GPU fill-rate.
4. **Frame-Rate-Independent Physics:** Motion decay and scroll physics rely on mathematical deltaTime integration ($\alpha = 1 - e^{-\lambda \cdot \Delta t}$, $\lambda = 14$) rather than frame-locked CSS keyframes.
5. **Zero Unicode Emojis in Production UI:** All iconography mandates inline SVG vectors with `currentColor` stroke binding.

---

## 2. The 6-Skill Orchestration Pipeline

The system operates as a unidirectional Directed Acyclic Graph (DAG) commanded by `mr-ui-designer`:

```
                                 ┌─────────────────────────────────┐
                                 │       Raw User Prompt           │
                                 │   "Build an analytics engine"   │
                                 └────────────────┬────────────────┘
                                                  │
                                                  ▼
                                 ┌─────────────────────────────────┐
                                 │        👑 mr-ui-designer        │
                                 │   (Master Frontend Architect)   │
                                 └────────────────┬────────────────┘
                                                  │
                ┌─────────────────────────────────┴─────────────────────────────────┐
                ▼                                                                   ▼
  ┌───────────────────────────┐                                       ┌───────────────────────────┐
  │ 🧠 autonomous-intent-     │                                       │ 🎨 visual-chemistry-      │
  │    expander               │                                       │    engine                 │
  │ - 3-Tier Ambiguity Budget │                                       │ - 5 Visual Chemistries    │
  │ - 8 Domain Archetypes     │                                       │ - Anti-Repetition Rules   │
  │ - P01-P30 Parameter Specs │                                       │ - OKLCH Color Engine      │
  └─────────────┬─────────────┘                                       └─────────────┬─────────────┘
                │                                                                   │
                └─────────────────────────────────┬─────────────────────────────────┘
                                                  ▼
  ┌───────────────────────────────────────────────────────────────────────────────────────────────┐
  │ Canonical Machine Contract: design-spec.json (Validated via Draft 2020-12 JSON Schema)        │
  └───────────────────────────────────────────────┬───────────────────────────────────────────────┘
                                                  │
                  ┌───────────────────────────────┼───────────────────────────────┐
                  ▼                               ▼                               ▼
    ┌───────────────────────────┐   ┌───────────────────────────┐   ┌───────────────────────────┐
    │ 🧩 ui-kit                 │   │ ⚡ vibe-physics-engine    │   │ ✍️ conversion-copy-engine │
    │ - 20 AI-Native Primitives │   │ - DeltaTime Physics Loop  │   │ - B2B JTBD / ROI Engine   │
    │ - 50+ Shadcn Components   │   │ - Lenis Momentum Smooth   │   │ - PAS Narrative Matrix    │
    │ - Asymmetric Bento Grids  │   │ - GPU Composite Only      │   │ - Objection Inversion     │
    │ - Zero-JS CSS Grid Acc.   │   │ - Strict Zero-Emoji SVG   │   │ - Anti-Dark-Pattern Rules │
    └─────────────┬─────────────┘   └─────────────┬─────────────┘   └─────────────┬─────────────┘
                  │                               │                               │
                  └───────────────────────────────┼───────────────────────────────┘
                                                  │
                                                  ▼
                                 ┌─────────────────────────────────┐
                                 │ 🔍 ui-verifier                  │
                                 │ 5-Pillar Autonomous Gate:       │
                                 │ 1. Visual Anti-Slop Check       │
                                 │ 2. Responsive (375/768/1440px)  │
                                 │ 3. WCAG 2.2 AA (>=4.5:1 / 3:1)  │
                                 │ 4. Blur Compositing (<=3 layers)│
                                 │ 5. Semantic RTL & BiDi Stability│
                                 └────────────────┬────────────────┘
                                                  │ [PASS]
                                                  ▼
                                 ┌─────────────────────────────────┐
                                 │ ✨ Production Output Code       │
                                 │ (Next.js 15 / React / HTML5)    │
                                 └─────────────────────────────────┘
```

### Flow Mechanics & Skill Responsibilities

1. **Stage 1: Intent Expansion (`autonomous-intent-expander`)**
   - Ingests raw user prompt and runs it through the **3-Tier Ambiguity Budget**.
   - Classifies domain intent into 1 of 8 Master Archetypes (`LUXURY_CLINICAL`, `HIGH_PERFORMANCE_SAAS`, `HIGH_TICKET_SERVICE`, `HEAVY_INDUSTRIAL_ECOMMERCE`, `CREATIVE_EDITORIAL`, `HOSPITALITY_EXPERIENCE`, `HYPER_LOCAL_TRADES`, `EDTECH_ACADEMY`).
   - Synthesizes Core Parameters (P01–P24) and activates relevant Conditional Parameters (P25–P30).
   - Generates and passes canonical `design-spec.json`.

2. **Stage 2: Chemistry Selection (`visual-chemistry-engine`)**
   - Evaluates the archetype against recent project state to enforce the **Anti-Repetition Protocol** across $\ge 3$ structural dimensions.
   - Establishes mathematical color ramps in OKLCH space (preserving lightness contrast under gamut mapping).
   - Generates the primary palette tokens, surface treatment (e.g. SVG noise fractal + mesh glow), and elevation layers.

3. **Stage 3: Primitive Composition (`ui-kit`)**
   - References 6 curated component catalogs (`ai_native_full_catalog.md`, `shadcn_full_catalog.md`, `bento_grids_and_cards.md`, `physics_transitions_catalog.md`, `data_and_flow.md`, `tokens_and_theme_engine.md`).
   - Injects AI-native primitives (collapsible reasoning drawer, tool execution chip, streaming token cursor, approval gate, diff inspector).
   - Implements asymmetric grid structures and CSS logical properties (`margin-inline-start`, `padding-inline-end`).

4. **Stage 4: Mathematical Physics Integration (`vibe-physics-engine`)**
   - Binds interactive transitions to the exponential decay easing function:
     $$\alpha = 1 - e^{-\lambda \cdot \Delta t} \quad (\lambda = 14)$$
   - Injects zero-dependency native smooth scroll fallback or progressive modern Lenis momentum.
   - Enforces GPU-accelerated compositing rules (`transform: translate3d(...)`, `will-change: transform`).
   - Replaces unicode emojis with scalable inline SVG vectors (`stroke="currentColor"`).

5. **Stage 5: Narrative Architecture (`conversion-copy-engine`)**
   - Replaces placeholder filler with domain-tailored copy formulas:
     $$\mathbf{\text{Hero Headline}} = [\text{Dream Outcome}] + [\text{Without Main Fear/Friction}] + [\text{Unique Mechanism/Timeframe}]$$
   - Formulates Objection Inversion microcopy positioned directly beneath primary CTAs.
   - Enforces the Anti-Dark-Pattern standard: zero synthetic countdown timers, zero falsified testimonial quotes, and full pricing transparency.

6. **Stage 6: Autonomous Verification Gate (`ui-verifier`)**
   - Audits rendered code across 5 mandatory pillars before marking completion:
     - **Pillar 1 (Visual Anti-Slop):** Confirms adherence to the chosen chemistry and guarantees novelty across $\ge 2$ structural axes.
     - **Pillar 2 (Multi-Device Responsive):** Tests 375px mobile (0px horizontal overflow, $\ge 24\text{px}$ touch targets), 768px tablet, and 1440px desktop container bounds.
     - **Pillar 3 (WCAG 2.2 AA Accessibility):** Verifies keyboard reachability, visible focus indicators (`focus-visible:ring-2`), semantic clickables (`<button>`, `<a>`), and mathematical contrast ($\ge 4.5:1$ body, $\ge 3:1$ headers).
     - **Pillar 4 (Compositing Budget):** Enforces $\le 3$ active backdrop-blur surfaces and respects `@media (prefers-reduced-motion: reduce)`.
     - **Pillar 5 (Semantic RTL & BiDi):** Confirms macro coordinates remain physically frozen, `<bdi>` isolates mixed English phrases, and code/telemetry blocks maintain pure LTR.

---

## 3. Data Contracts & JSON Schema Architecture

All inter-skill communication relies on the machine-validated contract defined in [`schemas/design-spec.v1.schema.json`](schemas/design-spec.v1.schema.json).

### The 3-Tier Ambiguity Budget

To prevent agent paralysis while eliminating unapproved architectural drift, the expander operates under a calibrated three-tier decision model:

| Tier | Category | Autonomy Level | Protocol |
| :--- | :--- | :--- | :--- |
| **Tier 1** | Visual, Aesthetic & Token Selection | **100% Autonomous** | Zero user interrogation. The agent selects the optimal visual chemistry, color tokens, font stack, and grid density based on the detected archetype. |
| **Tier 2** | Architecture & Standard Workflows | **Autonomous with Stated Assumptions** | The agent infers standard user flows, data structures, and component hierarchies. It documents all assumptions under an explicit `⚠️ Assumptions Made:` block, allowing steering without pausing execution. |
| **Tier 3** | High-Risk Logic, Financials, Auth, Legal | **Zero Guesswork** | The agent must never guess regulatory compliance (HIPAA, GDPR), payment splits, transaction math, or authentication boundaries. It surfaces explicit decision forks. |

### Parameter Taxonomy (P01 – P30)

The specification maps user intent across 30 formal parameters divided into Universal Core and Contextual Domain sets:

#### A. Universal Core Parameters (P01 – P24)
- **P01–P05: Intent & Product Foundations**
  - `P01`: Master Domain Archetype (1 of 8 predefined enums).
  - `P02`: Primary Target Persona & Behavioral Modality.
  - `P03`: Core Job-To-Be-Done (JTBD).
  - `P04`: Primary Conversion Action (Primary CTA).
  - `P05`: Secondary Micro-Action (Low-friction entry).
- **P06–P08: Trust & Value Mechanics**
  - `P06`: Primary Objection Neutralization Strategy.
  - `P07`: Evidence Density & Social Proof Architecture.
  - `P08`: Transparent Risk Reversal Mechanism.
- **P09–P13: Visual Chemistry & Tokens**
  - `P09`: Canvas Base Token (`oklch(...)`).
  - `P10`: Surface Elevation Token (`oklch(...)`).
  - `P11`: Primary Accent Token (`oklch(...)`).
  - `P12`: Border & Stroke Specification (`1px solid oklch(...)`).
  - `P13`: Base Corner Radius (`rounded-md`, `rounded-xl`, etc.).
- **P14–P17: Typography & Spatial Rhythm**
  - `P14`: Display Title Font Family.
  - `P15`: Body Copy Font Family.
  - `P16`: Tabular Metric & Code Font Family (`JetBrains Mono`).
  - `P17`: Spatial Rhythm & Baseline Cadence (8pt baseline).
- **P18–P21: Motion & Interaction Model**
  - `P18`: Scroll Physics & Momentum Strategy (`lenis` or native).
  - `P19`: Interactive Hero Module Composition.
  - `P20`: Iconography Protocol (Strict SVG Vector Standard).
  - `P21`: Transition Curve & DeltaTime Physics ($\lambda = 14$).
- **P22–P24: Narrative & Copy Architecture**
  - `P22`: Bottom-Line-Up-Front (BLUF) Value Hook.
  - `P23`: Problem-Agitation-Solution (PAS) Matrix.
  - `P24`: Brand Voice Register (Technical, Luxurious, Bold).

#### B. Conditional Domain Parameters (P25 – P30)
- `P25`: Local Geo-Coordinates & Schema (Local trades and brick-and-mortar hospitality).
- `P26`: Clinical & Board Certification Proof (Healthcare, medical, high-end aesthetics).
- `P27`: Public Schema.org & Wikidata Entity Linking (Public discoverable landing pages).
- `P28`: Financial Math & Transaction Guardrails (Fintech, trading, checkout flows).
- `P29`: Core Web Vitals Budget ($\text{LCP} \le 1.8\text{s}$, $\text{CLS} \le 0.05$).
- `P30`: Sandbox & Boundary Isolation (Multi-tenant widgets, third-party iframe containment).

### Canonical JSON Contract Example

```json
{
  "$schema": "schemas/design-spec.v1.schema.json",
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

---

## 4. The 5 Master Visual Chemistries Specification Matrix

The Vibe UI design space is divided into 5 distinct, mathematically calibrated visual chemistries:

| Parameter / Dimension | 1. Minimalist High-Performance SaaS | 2. Luxury Obsidian & Glass 2.0 | 3. Neobrutalism & Playful High-Contrast | 4. Swiss Editorial & Paper Craft | 5. Modern Crisp Light (Stripe / Apple) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Primary Use Cases** | Developer Tools, B2B SaaS, Observability, Telemetry | AI Flagships, Web3, High-End Clinics, Luxury Services | Creative Agencies, Youth Apps, Creator Economy, Bold SaaS | Long-Form Journals, Architecture, Deep Research Portfolios | Fintech, Payments, Enterprise SaaS, Healthcare |
| **Canvas Token** | `oklch(0.14 0.005 260)` (`#09090b`) | `oklch(0.12 0.012 260)` (`#0a0812`) | Pastel Chalk (`#fef08a` / `#a5f3fc` / `#ffffff`) | `oklch(0.98 0.005 80)` (`#faf8f5`) Warm Paper | `oklch(0.985 0.002 90)` (`#ffffff`) Snow |
| **Surface Treatment** | Flat matte card `oklch(0.18 0.008 260)` | Multi-layer frosted card with SVG fractal noise & mesh glow | Solid high-contrast opaque white card (`#ffffff`) | Flat warm parchment card (`#f4f0eb`) | Pure white card with soft diffuse gradient wash |
| **Borders & Strokes** | 1px razor border `rgba(255,255,255,0.08)` | Fresnel Specular Inset `inset 0 1px 1px 0 rgba(255,255,255,0.16)` | 2.5px solid jet black outline (`#000000`) | 1px hairline typographic rule (`#e5e0d8`) | Refined micro-border `1px solid #e2e8f0` |
| **Elevation & Shadows** | Linear top-edge light wash `rgba(255,255,255,0.03)` | Deep atmospheric ambient diffuse blur `rgba(0,0,0,0.5)` | Hard unblurred 4px offset drop shadow `4px 4px 0px #000` | Zero elevation; 100% flat typographic rhythm | Multi-stage ambient shadow `0 1px 3px rgba(0,0,0,0.05), 0 10px 25px rgba(0,0,0,0.03)` |
| **Primary Accent** | Electric Indigo `oklch(0.65 0.22 265)` or Pure White | Champagne Gold `oklch(0.72 0.145 85)` | High-Saturation Jet Black (`#000000`) or Hyper-Pink | Editorial Charcoal Black (`#1c1917`) | Electric Sapphire Blue `oklch(0.55 0.22 260)` (`#2563eb`) |
| **Typography Stack** | Inter / Geist Sans + JetBrains Mono metrics | Playfair / Newsreader Serif titles + Inter body | Space Grotesk / Lexend + Bold Display Sans | Instrument Serif / Bodoni + Generous Tracking Sans | Inter / SF Pro + Clean Tabular Numerals |
| **Interaction / Hover** | Subtle border outline brightening (`border-zinc-500`) | Glass sheen transition + specular highlight shift | Physical button-press translation (`translate(2px, 2px); box-shadow: 2px 2px 0px #000`) | High-contrast underline or inverse text pill | Gentle elevation increase (`translateY(-1px)`) |
| **Compositing Budget** | Max 1 blur layer | Max 3 blur layers | 0 blur layers (100% opaque vector) | 0 blur layers (100% paper craft) | 0–1 blur layer (header only) |

### The Anti-Repetition Protocol

To guarantee that AI-generated interfaces do not converge into repetitive clichés across successive generations, `visual-chemistry-engine` mandates rotation across **at least 3 of 4 structural axes**:
1. **Hero Composition:** Alternate between `split_terminal`, `centered_badge`, `asymmetric_editorial`, and `bento_hero`.
2. **Card/Grid Density:** Alternate between `airy` (generous 32px padding), `standard` (24px padding), and `bento_asymmetric` (variable column spans).
3. **Lighting/Surface Treatment:** Alternate between flat matte, SVG fractal noise glassmorphism, and opaque high-contrast planes.
4. **Accent Palette Hue:** Rotate accent color vectors outside a 60-degree OKLCH hue angle from prior generation.

---

## 5. Fixed-Structure Semantic RTL Architecture

A critical architectural flaw in generic AI-generated interfaces is layout destruction upon enabling right-to-left (RTL) mode. Naive RTL implementations horizontally mirror entire grids, reverse navigation menus, and swap column hierarchies, causing severe disorientation.

Vibe UI enforces a **Fixed-Structure Semantic RTL Architecture**:

```
 ┌─────────────────────────────────────────────────────────────────────────────┐
 │                         GLOBAL MACRO CONTAINER (STABLE)                     │
 │  ┌─────────────────────────────────┐  ┌──────────────────────────────────┐  │
 │  │      Column 1 (Span 2)          │  │       Column 2 (Span 1)          │  │
 │  │  PHYSICALLY LOCKED ON LEFT      │  │   PHYSICALLY LOCKED ON RIGHT     │  │
 │  │                                 │  │                                  │  │
 │  │  [Text in RTL: Right-Aligned]   │  │   [Metric: LTR Monospace]        │  │
 │  │  "عملکرد پروژه با موفقیت ثبت شد"│  │   "latency: 18ms"                │  │
 │  │  [Mixed English in <bdi>]       │  │                                  │  │
 │  │  "ماژول <bdi>Next.js 15</bdi>"  │  │   [Semantic Chevron: Mirrored]   │  │
 │  └─────────────────────────────────┘  └──────────────────────────────────┘  │
 └─────────────────────────────────────────────────────────────────────────────┘
```

### Inviolable Invariants

#### 1. Physical Macro Coordinate Stability
- Grids, column orders, navigation bars, and comparison sliders remain **physically locked in place**.
- An asymmetric 3-column Bento grid with column spans `[col-span-2, col-span-1]` retains identical physical positions from left to right. Grid columns are **never** inverted into `[col-span-1, col-span-2]`.

#### 2. Text-Only RTL Scoping
- The `dir="rtl"` attribute and `text-align: right` are scoped exclusively to readable content nodes: headings (`<h1>`–`<h6>`), paragraphs (`<p>`), lists (`<ul>`, `<ol>`), and descriptions.

#### 3. Semantic Directional Affordance Mirroring
- Only UI controls that convey reading progress or chronological flow mirror horizontally:
  - Navigation back/forward arrows (`<svg>` left/right chevrons).
  - Multi-step timeline progress rails.
  - Breadcrumb navigation trails.
- Symmetrical controls (close `×` buttons, search icons, play/pause controls, sliders) **never** mirror.

#### 4. BiDi Punctuation Isolation via `<bdi>`
- When Persian or Arabic sentences incorporate Latin technical terms, brands, or version numbers (e.g. `Next.js 15`, `Tailwind CSS`, `Claude Code`), punctuation marks frequently scramble to the incorrect side of the string.
- Isolation is guaranteed using semantic HTML tags:
  ```html
  <p class="text-right" dir="rtl">
    سیستم با موفقیت به پشته <bdi class="font-mono text-primary">Next.js 15 App Router</bdi> ارتقا یافت.
  </p>
  ```
  or via CSS utility:
  ```css
  .bidi-isolated {
    unicode-bidi: plaintext;
  }
  ```

#### 5. Strict LTR Monospace Enforcement for Telemetry & Code
- Terminal blocks, shell commands, JSON contracts, URLs, response times (`18ms`), percentage deltas (`+14.2%`), and SemVer tags (`v2.2.0`) are strictly locked to LTR:
  ```css
  .ltr-code, .telemetry-pill, code, pre, .font-mono {
    direction: ltr !important;
    text-align: left !important;
    unicode-bidi: isolate !important;
  }
  ```

#### 6. Universal CSS Logical Properties
- Physical left/right styling properties are banned in favor of bidirectional logical equivalents:
  - `margin-inline-start` (`ms-*`) instead of `margin-left` (`ml-*`)
  - `margin-inline-end` (`me-*`) instead of `margin-right` (`mr-*`)
  - `padding-inline-start` (`ps-*`) instead of `padding-left` (`pl-*`)
  - `padding-inline-end` (`pe-*`) instead of `padding-right` (`pr-*`)
  - `inset-inline-start` (`start-*`) instead of `left` (`left-*`)
  - `inset-inline-end` (`end-*`) instead of `right` (`right-*`)

---

## 6. Platform Adapter Integration Topology

Vibe UI provides universal IDE configuration adapters to ensure consistent agent behavior across diverse developer toolchains:

```
vibe-ui-skills/
├── adapters/
│   ├── cursor/
│   │   └── .cursorrules               --> Root `.cursorrules` for Cursor IDE
│   ├── claude/
│   │   └── CLAUDE.md                  --> Root `CLAUDE.md` for Claude Code CLI
│   ├── copilot/
│   │   └── copilot-instructions.md    --> `.github/copilot-instructions.md` for GitHub Copilot
│   └── windsurf/
│       └── .windsurfrules             --> Root `.windsurfrules` for Windsurf / Cascade
```

### Adapter Deployment Rules

1. **Rule File Precedence:**
   - Cursor: `.cursorrules` placed in project root governs multi-model prompt injection.
   - Claude Code: `CLAUDE.md` placed in project root injects system-level commands and design standards.
   - Copilot: `.github/copilot-instructions.md` guides Copilot Chat and inline completions.
   - Windsurf: `.windsurfrules` placed in project root configures Cascade orchestration.
2. **Standard Skill Path Resolution:**
   The adapters route skill invocations to `skills/` using either relative repository paths or user-level global configuration (`~/.gemini/config/skills/` or `~/.cursor/skills/`).

---

## 7. Testing & Evaluation Architecture

To prevent silent regressions and qualitative drift, the repository includes an automated evaluation harness in [`evals/`](evals/):

### Evaluation Harness (`evals/run_evals.py`)

The evaluation harness performs static AST and regex-driven inspections against HTML and JSON fixtures. Key verification layers include:

1. **Mathematical WCAG Relative Luminance Engine:**
   Computes exact relative luminance ($L$) across body and header elements:
   $$L = 0.2126 R' + 0.7152 G' + 0.0722 B'$$
   where for each color channel $C \in \{R, G, B\}$:
   $$C' = \begin{cases} \frac{C}{12.92} & \text{if } C \le 0.04045 \\ \left(\frac{C + 0.055}{1.055}\right)^{2.4} & \text{otherwise} \end{cases}$$
   The contrast ratio between light luminance $L_1$ and dark luminance $L_2$ is verified:
   $$\text{Ratio} = \frac{L_1 + 0.05}{L_2 + 0.05}$$
   - **Body Copy:** Contrast ratio $\ge 4.5:1$ (WCAG AA).
   - **Headings & Large Elements:** Contrast ratio $\ge 3.0:1$ (WCAG AA).

2. **Negative Schema Test Fixtures (`evals/fixtures/`):**
   Verifies that invalid design specifications are rejected with exit code 1:
   - `invalid_archetype.json`: Asserts rejection of unlisted domain archetypes.
   - `out_of_range_entropy.json`: Asserts rejection of entropy scores outside `[0.0, 1.0]`.
   - `touch_target_below_24px.json`: Asserts rejection of interactive targets $< 24\text{px}$.

3. **Machine-Readable `--json` Mode:**
   The runner supports a `--json` CLI flag that suppresses terminal styling and outputs a machine-readable summary object for continuous integration (CI) pipelines:
   ```bash
   python evals/run_evals.py --json
   ```

---

## 8. Modern Production Starter Architecture (`examples/nextjs-starter/`)

The repository includes a modern Next.js 15 production starter demonstrating full architectural integration:

- **Framework Core:** Next.js 15 App Router (`next: ^15.1.7`), React 19 (`react: ^19.0.0`), TypeScript 5.
- **Typed OKLCH Tokens (`lib/tokens.ts`):** Full TypeScript typing across all 5 visual chemistries, exporting `VISUAL_CHEMISTRIES` with canvas, surface, accent, and border definitions.
- **AI-Native Component Primitives:**
  - `AiThinkingDrawer.tsx`: Collapsible reasoning drawer featuring zero-JS CSS Grid height transition (`grid-template-rows: 0fr` to `1fr`), ARIA live regions (`role="region"`), pulsing radar status indicator, and micro-latency execution chips.
  - `HeroSection.tsx`: Responsive landing hero combining conversion copy, chemistry badge indicator, embedded reasoning drawer, and a live telemetry HUD (`.ltr-code`).
- **Semantic RTL Implementation:** Native bidirectional layout support using CSS logical properties, `<bdi>` term isolation, and physical macro stability.

---

## 9. Conclusion & Reference Links

The Vibe UI Skills Suite bridges the gap between frontier AI generative capabilities and enterprise frontend standards. By enforcing strict schemas, mathematical physics, accessibility guardrails, and fixed-structure RTL stability, it establishes the industry benchmark for AI-driven user interface development.

- **Master Agent Specification:** [`mr-ui-designer/AGENT.md`](mr-ui-designer/AGENT.md)
- **JSON Schema:** [`schemas/design-spec.v1.schema.json`](schemas/design-spec.v1.schema.json)
- **Evaluation Suite:** [`evals/README.md`](evals/README.md)
- **Component Catalogs:** [`skills/ui-kit/references/`](skills/ui-kit/references/)
- **Golden Prompts:** [`PROMPTS.md`](PROMPTS.md) • [`PROMPTS.fa.md`](PROMPTS.fa.md)
- **Changelog & Version History:** [`CHANGELOG.md`](CHANGELOG.md)
