<div align="center">

<img src="assets/icon.png" alt="Vibe UI Suite Logo" width="96" height="96" style="border-radius: 18px; margin-bottom: 12px;">

# Vibe UI Suite

**Contract-driven frontend engineering, design-system constraints, and runtime verification for AI coding assistants.**

[![CI Pipeline](https://github.com/omid-io/vibe-ui-suite/actions/workflows/ci.yml/badge.svg)](https://github.com/omid-io/vibe-ui-suite/actions/workflows/ci.yml)
[![npm version](https://img.shields.io/npm/v/@omid-io/tokens.svg?color=cb3837&label=npm)](https://www.npmjs.com/package/@omid-io/tokens)
[![npm downloads](https://img.shields.io/npm/dm/%40omid-io%2Ftokens?color=red&label=npm%20downloads)](https://www.npmjs.com/package/@omid-io/tokens)
[![Open-VSX Downloads](https://img.shields.io/open-vsx/dt/omid-io/vibe-ui-vscode?color=green&logo=eclipseche&label=open-vsx%20downloads)](https://open-vsx.org/extension/omid-io/vibe-ui-vscode)
[![VS Code Marketplace Installs](https://img.shields.io/visual-studio-marketplace/i/omid-io.vibe-ui-vscode?color=blue&logo=visual-studio-code&label=marketplace%20installs)](https://marketplace.visualstudio.com/items?itemName=omid-io.vibe-ui-vscode)
[![GitHub Stars](https://img.shields.io/github/stars/omid-io/vibe-ui-suite?style=social)](https://github.com/omid-io/vibe-ui-suite)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![WCAG 2.2 AA](https://img.shields.io/badge/WCAG_2.2-AA_Mathematical-success.svg)](evals/)

<p align="center">
  <a href="README.fa.md"><strong>فارسی (Persian Documentation)</strong></a> •
  <a href="ARCHITECTURE.md"><strong>Architecture Specification</strong></a> •
  <a href="docs/ENTERPRISE_ADAPTATION.md"><strong>Enterprise Guide</strong></a> •
  <a href="https://omid-io.github.io/vibe-ui-suite/"><strong>Interactive Studio Playground</strong></a>
</p>

</div>

---

## ⚖️ Visual Impact: Vanilla AI Slop vs. Vibe UI V3

What happens when you ask an AI assistant to generate a frontend component?

```text
┌──────────────────────────────────────┐  vs  ┌──────────────────────────────────────┐
│ ❌ VANILLA AI SLOP                   │      │ ✨ VIBE UI V3 COMPILED               │
├──────────────────────────────────────┤      ├──────────────────────────────────────┤
│ • Generic purple gradient buttons    │      │ • Orthogonal Style DNA (26 families) │
│ • Low contrast text (3.2:1 FAILS AA) │      │ • Mathematical WCAG 2.2 AAA (17.8:1) │
│ • Broken mobile overflow (375px)     │      │ • Zero layout shift, mobile audited  │
│ • Hallucinated raw emojis            │      │ • Deterministic inline vector icons  │
│ • No loading / empty / error states  │      │ • Full 4-state lifecycle baked in    │
│ • Mixed direction text / numbers     │      │ • Strict LTR metrics & BiDi isolation│
└──────────────────────────────────────┘      └──────────────────────────────────────┘
```

👉 **[Launch the Interactive Design Compiler Studio Live](https://omid-io.github.io/vibe-ui-suite/)** — Zero server latency, instantaneous client-side domain inference & component preview.

---

Vibe UI Suite gives AI coding assistants (Cursor, Claude Code, Windsurf, Antigravity) a structured, machine-checkable framework to plan, implement, and verify frontend interfaces.

Instead of relying on fragile prompt engineering ("make this dashboard look clean and modern"), Vibe UI establishes an explicit compiler-style pipeline:

```text
User Intent
    ↓
Intent Expansion (30-parameter design contract)
    ↓
Machine-Readable Schema (design-spec.v1.schema.json)
    ↓
Visual System + Component Recipe Selection
    ↓
Code Implementation (Next.js 15 / React 19 / Tailwind OKLCH)
    ↓
Static Evaluation (Schema, luminance math, negative fixtures)
    ↓
Headless Browser Evaluation (Playwright 375px mobile overflow)
    ↓
Verified Output or Actionable Failure Diagnostics
```

> **Day-One Transparency**: Vibe UI Suite is at `v3.4.0` (The True Vision & Dynamic Architecture Engine). Featuring visual critic veto gating, 24 domain-specific causal reactive widgets, intelligent Media & Asset Direction, render-affecting style compilers (Neobrutalism, Swiss, Luxury, Terminal, Glass, Stripe), deep design system inheritance (shadcn/ui), 100% blind holdout benchmark accuracy, and dual-tier contrast governance (Target: WCAG AAA >= 7:1 | Hard Gate: WCAG AA >= 4.5:1). Constructive criticism, issues, and contributions from frontend engineers and AI researchers are warmly welcomed.

---

## 🤖 30-Second Quick Start for AI Assistants (Cursor, Claude Code, Windsurf)

Whether you are a beginner building your first app or a senior engineer designing enterprise software, you can equip your AI assistant with Vibe UI in one of two ways:

### Option A: The Prompt (Zero Install)
Copy and paste this single prompt directly into **Cursor, Claude Code, Windsurf, or Copilot**:
```text
Design and style this application using Vibe UI standards (https://github.com/omid-io/vibe-ui-suite):
- Use OKLCH color palettes & native Tailwind CSS v4 (@theme)
- Enforce dual-tier contrast standards: Target WCAG 2.2 AAA (>= 7:1), with invariant hard-gate at WCAG 2.2 AA (>= 4.5:1)
- Never use raw emojis in UI — use inline SVG vector icons with currentColor
- Use fixed-structure semantic RTL with <bdi> isolation and pure LTR metrics
```

### Option B: The 1-Command CLI Setup
In your project directory, run:
```bash
npx @omid-io/tokens init
```
This interactive command:
1. Configures your AI editor rules (`.cursorrules`, `CLAUDE.md`, `.windsurfrules`).
2. Selects your Visual Chemistry (`Minimalist SaaS`, `Luxury Glass`, `Neobrutalism`, `Swiss Editorial`, `Stripe Crisp Light`).
3. Injects OKLCH design variables into your project.

---

## 🎨 Native Tailwind CSS v4 (@theme) — Zero Config

In your `app/globals.css` or main stylesheet:
```css
@import "tailwindcss";
@import "@omid-io/tokens/v4.css";
```
Zero JavaScript configuration files needed. Instantly unlocks:
- **Semantic OKLCH colors**: `bg-vibe-canvas`, `bg-vibe-surface`, `text-vibe-primary`, `border-vibe-border`
- **Physics curves**: `transition-vibe-spring`, `transition-vibe-snap`, `transition-vibe-glide`
- **Material shadows**: `shadow-vibe-brutal`, `shadow-vibe-glass`

---

## 📦 Verified Component Recipes (`add`)

Add production-ready, accessible component templates directly into `components/vibe-ui/`:
```bash
# Collapsible AI reasoning drawer with CSS grid zero-JS transition & status radar
npx @omid-io/tokens add thinking-drawer

# LTR-isolated technical metric HUD for latency, tokens, and model status
npx @omid-io/tokens add telemetry-hud

# Live mathematical WCAG AA / AAA contrast compliance indicator badge
npx @omid-io/tokens add contrast-badge
```
List all available registry components:
```bash
npx @omid-io/tokens list
```

---

## 💻 Editor Extensions (VS Code & Cursor)

Vibe UI is available directly inside your IDE sidebar:

- **VS Code Marketplace**: [`omid-io.vibe-ui-vscode`](https://marketplace.visualstudio.com/items?itemName=omid-io.vibe-ui-vscode)
- **Open-VSX Registry**: [`omid-io.vibe-ui-vscode`](https://open-vsx.org/extension/omid-io/vibe-ui-vscode) (for Cursor, Windsurf, VSCodium)

### Features:
- **Interactive WCAG 2.2 Contrast Calculator**: Real-time color pickers with instant relative luminance calculation ($L_1 / L_2$) and dynamic Pass/Fail badges.
- **1-Click Component Inserter**: Insert component templates directly into your active text editor.
- **In-Editor Audit Command**: `Ctrl+Shift+P` ➔ `Vibe UI: Audit Active File Contrast`.

---

## 🏛️ Architecture: The 6-Skill Orchestration DAG

The system is coordinated by a lead architect agent (**`mr-ui-designer`**) that orchestrates 6 specialized sub-skills:

```text
               ┌──────────────────────────────┐
               │  User Prompt: "Build a UI"   │
               └──────────────┬───────────────┘
                              │
                              ▼
               ┌──────────────────────────────┐
               │       mr-ui-designer         │
               │  (Lead Frontend Architect)   │
               └──────────────┬───────────────┘
                              │
       ┌──────────────┬───────┴───────┬──────────────┐
       ▼              ▼               ▼              ▼
┌──────────────┐┌──────────────┐┌──────────────┐┌──────────────┐
│  autonomous- ││   visual-    ││   ui-kit     ││    vibe-     │
│    intent-   ││  chemistry-  ││  (70+ AI     ││   physics-   │
│   expander   ││    engine    ││   Recipes)   ││    engine    │
└──────┬───────┘└──────┬───────┘└──────┬───────┘└──────┬───────┘
       │               │               │               │
       └───────────────┼───────────────┴───────────────┘
                       │
                       ▼
       ┌──────────────────────────────┐
       │   conversion-copy-engine     │
       │   (PAS, JTBD, Anti-Deception)│
       └──────────────┬───────────────┘
                      │
                      ▼
       ┌──────────────────────────────┐
       │         ui-verifier          │
       │  (5-Pillar Quality Gate)     │
       └──────────────┬───────────────┘
                      │
                      ▼
       ┌──────────────────────────────┐
       │ Evaluated Frontend Code + Log│
       └──────────────────────────────┘
```

| Sub-Skill | Role & Boundary | Primary Constraint |
| :--- | :--- | :--- |
| **`autonomous-intent-expander`** | Intent synthesis via 30-parameter contract | Calibrated Ambiguity Budget; rejects unstated business assumptions |
| **`visual-chemistry-engine`** | Cohesive aesthetic system selection | 5 distinct chemistries; anti-repetition constraint across projects |
| **`ui-kit`** | Component primitives & interaction patterns | AI reasoning drawers, tool chips, telemetry HUDs, Bento recipes |
| **`vibe-physics-engine`** | Motion, color, and GPU budgets | OKLCH perceptual spaces, spring curves, strict $\le 3$ blur layer limit |
| **`conversion-copy-engine`** | Strategic narrative architecture | Domain-aware copy; strictly prohibits fake testimonials or false urgency |
| **`ui-verifier`** | Automated quality & accessibility gates | Static math + headless browser runtime DOM assertions |

---

## 🎨 Five Visual Chemistries

Vibe UI defines five visual systems for consistent design decisions:

1. **Minimalist SaaS**: Monochrome restraint, precision borders, high information density, functional typography (`oklch(0.12 0.01 260)`).
2. **Luxury Obsidian / Glass 2.0**: Dark substrates, specular Fresnel highlights, subtle gold accents, controlled GPU backdrop blur budget (`oklch(0.08 0.02 270)`).
3. **Neobrutalism**: High-contrast saturated cards, hard 3px black offset geometric drop-shadows, zero blur, explicit physical boundaries (`oklch(0.98 0.02 95)`).
4. **Swiss Editorial**: Asymmetric typographic grid, content-first layout inspired by the International Typographic Style (`oklch(0.97 0.005 80)`).
5. **Stripe Crisp Light**: Developer-first documentation aesthetic, micro-borders, clean typography, subtle shadows (`oklch(0.99 0.002 250)`).

---

## 🌐 Fixed-Structure Semantic RTL

Standard AI-generated interfaces frequently fail on Right-to-Left (RTL) languages by naively flipping the entire DOM tree with `dir="rtl"`, inverting navigation columns, telemetry charts, and numeric sequences.

Vibe UI enforces **Fixed-Structure Semantic RTL**:
- **Physical Macro Stability**: Application layout coordinates (sidebars, toolbars, chart axes) remain physically stable.
- **Content-Level RTL**: RTL is applied strictly to typography, paragraphs, and reading flows using CSS logical properties (`margin-inline-start`, `text-align: start`).
- **BiDi Resilience**: Technical identifiers, code blocks, URLs, and telemetry HUDs are explicitly isolated with `<bdi>` or `dir="ltr"`.

---

## 🧪 Evaluation Suite & Runtime Quality Gates

The repository includes an automated test runner:

```bash
# 1. Run deterministic static checks & negative fixtures
python evals/run_evals.py

# 2. Run machine-readable CI output
python evals/run_evals.py --json

# 3. Run headless browser DOM verification (Chromium via Playwright)
python evals/run_evals.py --browser
```

### Deterministic vs. Heuristic Checks:

| Verification Gate | Type | Method | Scope |
| :--- | :--- | :--- | :--- |
| **JSON Schema Validation** | Deterministic | Draft 2020-12 Schema Validator | Validates 30 parameters with `additionalProperties: false` |
| **Negative Fixture Rejection** | Deterministic | Exit code assertion | Verifies exit code 1 on out-of-range entropy, invalid archetypes, or touch targets $< 24\text{px}$ |
| **Relative Luminance & Contrast** | Deterministic | $L = 0.2126 R' + 0.7152 G' + 0.0722 B'$ | Enforces WCAG AA ($\ge 4.5:1$ body, $\ge 3.0:1$ headings) |
| **Mobile Viewport Overflow** | Runtime | Chromium DOM (`scrollWidth <= clientWidth`) | Verifies 0px horizontal overflow at exact 375px viewport |
| **Semantic Clickables** | Static / Lint | Regex DOM tree audit | Asserts 0 raw `<div onclick>` instances (buttons/anchors required) |
| **Focus Rings** | Static / Lint | CSS rule check | Verifies presence of `:focus-visible` styles |
| **GPU Compositing Budget** | Static / Heuristic | CSS rule check | Enforces $\le 3$ active `backdrop-filter` blur layers |

---

## 📦 Next.js 15 Production Starter

A reference production starter is available under [`examples/nextjs-starter/`](examples/nextjs-starter/):
- **Core**: Next.js 15 App Router, React 19, TypeScript 5, Tailwind CSS.
- **Typed OKLCH Tokens**: [`lib/tokens.ts`](examples/nextjs-starter/lib/tokens.ts) exporting all 5 chemistries.
- **AI Primitives**: [`AiThinkingDrawer.tsx`](examples/nextjs-starter/components/AiThinkingDrawer.tsx) with zero-JS CSS Grid height transitions and accessible ARIA live regions.
- **Verified Clean Build**: Compiles in production mode (`npm run build`) in CI with zero type errors.

---

## 🛡️ What Vibe UI Is — and What It Is Not

### What It Is:
- A contract-driven linter, design system, and verification layer for AI coding assistants.
- An orchestration DAG that separates intent, visual rules, component code, copy, and verification.
- A set of executable evaluation gates that reject measurable UI regressions with non-zero exit codes.

### What It Is Not:
- It is **not** a guarantee that an AI-generated interface is 100% bug-free or production-ready without human review.
- It is **not** a replacement for comprehensive manual accessibility testing (screen readers, voice control).
- It is **not** an enterprise design system replacement; it is designed to bind into your existing `@company/ui` library via [`docs/ENTERPRISE_ADAPTATION.md`](docs/ENTERPRISE_ADAPTATION.md).

---

## 🤝 Contributing & Community

Vibe UI Suite is open-source under the **MIT License**. We actively welcome community contributions:
- New evaluation fixtures & negative tests
- Framework adapters (Vue, Svelte, Angular)
- Component recipes for the registry
- Real-world bug reports with minimal reproductions

```bash
git clone https://github.com/omid-io/vibe-ui-suite.git
cd vibe-ui-suite
python evals/run_evals.py
```

Maintainer: [Omid Zaferi](https://github.com/omid-io) • Issues: [GitHub Issues](https://github.com/omid-io/vibe-ui-suite/issues)
