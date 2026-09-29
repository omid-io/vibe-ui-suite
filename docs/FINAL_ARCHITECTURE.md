# 🏛️ Vibe UI V3 — Final System Architecture

## 1. Executive System Overview

Vibe UI V3 is a deterministic, anti-slop Design Compiler and Evaluation Engine engineered specifically for autonomous AI coding agents (Claude, Cursor, Copilot, Antigravity, Hermes). It transforms sparse, ambiguous user prompts into production-grade, accessible, and aesthetically distinctive user interfaces through a closed-loop synthesis and verification pipeline.

```text
User Prompt ("Decentralized Crypto Swap in Tehran")
   │
   ▼
[Intent & Domain Inference] (<5ms zero-token keyword analysis)
   │
   ├── Resolved Domain: fintech_crypto (Ambiguity Budget: 0.15)
   └── Direction: RTL (Persian) + LTR isolate metrics
   │
   ▼
[Style Resolver & Genome Engine] (vibe_core/director.py & genome.py)
   │
   ├── Anchor Style: linear_dark (Obsidian matte, 1px border)
   ├── Spatial DNA: keyboard_navigable_lanes (density: dense)
   ├── Material DNA: specular_border_glow (shadow: diffused_dark)
   ├── Motion DNA: spring_stiffness: 280, damping: 0.9 (lambda: 14)
   └── Typography: sans display + mono tabular metrics
   │
   ▼
[Canonical Design Spec (v1)] (schemas/design-spec.v1.schema.json)
   │
   ▼
[Token & Theme Pipeline] (packages/tokens & data/palettes.json)
   │
   └── OKLCH Tokens: --canvas-bg, --surface-bg, --accent, --text-primary
   │
   ▼
[UI Code Generation] (Tailwind CSS + Pure Semantic HTML / Next.js)
   │
   ├── 4-State Component Lifecycle: default, skeleton, empty, error
   └── BiDi Resilience: strict <bdi> isolation for English tickers/numbers
   │
   ▼
[3-Layer Tripartite Verification Engine] (evals/run_evals.py)
   │
   ├── Layer 1 (Static): JSON Schema, semantic tags, anti-slop regex
   ├── Layer 2 (Runtime Chromium): Real DOM contrast, focus rings, mobile viewports
   └── Layer 3 (Visual / Geometry): Zero-overflow bounds, backdrop blur limits
   │
   ▼
[Evidence Report & Auto-Repair Loop] (vibe_core/refiner.py)
   │
   ▼
[Production Artifact] (Deployable HTML / TSX + Tailwind Config)
```

---

## 2. Component Boundaries & Package Isolation

To eliminate supply-chain vulnerabilities and build coupling, Vibe UI strictly isolates all subsystems:

| Component | Path | Language / Runtime | Isolation Contract |
| :--- | :--- | :--- | :--- |
| **Data & Taxonomy** | `data/` | Canonical JSON (13 datasets) | Single source of truth. Zero code dependencies. |
| **JSON Schemas** | `schemas/` | Draft-07 JSON Schema (8 schemas) | Fail-closed validation contract with combinators. |
| **Vibe Core** | `vibe_core/` | Python 3.10+ stdlib | Zero external dependencies for core inference. |
| **Design Tokens & Suite** | `packages/vibe-ui-suite` | TypeScript 5 / Node 20+ | Flagship NPM package `vibe-ui-suite`. |
| **VS Code Extension** | `packages/vibe-ui-vscode` | TypeScript 5 / VS Code API | Independent extension packaging without examples coupling. |
| **Evaluation Engine** | `evals/` | Python + Playwright | Independent test runner with headless Chromium runtime. |
| **Showcase & Studio** | `showcase/` & `index.html` | Client-side Vanilla JS | 100% zero-server interactive studio on GitHub Pages. |

---

## 3. The 26-Style Orthogonal Genome Matrix

Rather than creating hundreds of superficial styles, Vibe UI defines **26 orthogonal style families** where visual parameters vary independently across 5 fundamental dimensions:

1. **Spatial Density:** `airy` (whitespace factor >= 1.5), `balanced` (1.1 - 1.4), `dense` (<= 0.9).
2. **Materiality:** `flat`, `matte_paper`, `porcelain_soft`, `specular_glass_2`, `galvanized_steel`, `earthen_moss`.
3. **Motion Physics:** Spring stiffness (150 - 450), damping ratio (0.65 - 1.3), lambda time constants (9 - 22ms).
4. **Typography Pairings:** Sans, Serif, Mono, Display, combined with Vazirmatn Persian script.
5. **Anti-Pattern Avoid Lists:** Hard constraints preventing AI slop (e.g. purple gradients, noisy shadows, arbitrary borders).

---

## 4. Verification Contract & Quality Gates

Every generated UI artifact must pass the **Master Quality Gate** before delivery:
- **WCAG 2.2 Level AA Contrast:** >= 4.5:1 for body copy and >= 3.0:1 for large headers and interactive states, verified on live physical pixels via Canvas 2D.
- **Keyboard Focus Visibility:** Guaranteed `:focus` and `:focus-visible` ring indicators on all focusable targets.
- **Multi-Viewport Mobile Stability:** Zero horizontal scroll overflow at 375x667 and 320x568 boundaries.
- **GPU Composite Budget:** Maximum 3 simultaneous `backdrop-filter` layers to avoid mobile framerate drops.
- **Semantic RTL / BiDi Resilience:** Structural layout invariants preserved; zero horizontal flipping of controls; LTR isolation for numbers and code.
