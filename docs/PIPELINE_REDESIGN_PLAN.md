# 🏛️ Vibe UI Pipeline Architecture & Execution Specification (v2.0)

## 🎯 The Core Philosophy: Two Golden Pillars

Rather than overwhelming the LLM with 60+ obscure micro-rules that dilute attention, the redesigned `vibe-ui-agent` is anchored on **Two Invariant Pillars**:

```
┌─────────────────────────────────────────────────────────────┐
│ PILLAR 1: Deep Trend Research & Award-Winning Inspiration    │
│ (Dribbble, Mobbin, Figma Community, Awwwards, Godly)        │
│ Study top-rated designs, generate/curate visual concepts,   │
│ and plan an intentional aesthetic before touching code.     │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ PHASE 2 & 3: High-Res Real Imagery & Modern Clean Skeleton  │
│ (Unsplash CDN / AI Gen, Vibrant Light Default, Clean Grid)  │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ PILLAR 2: Living Visual Feedback Loop ("Eyes of the Agent")  │
│ (Playwright Render -> Real Screenshot -> Vision Inspection)  │
│ Inspect spacing, contrast, typography, and fix flaws.       │
└─────────────────────────────────────────────────────────────┘
```

---

## 🏛️ The Two Golden Pillars Explained

### 🌟 Pillar 1: Trend Research & Award-Winning Inspiration (الگوبرداری از بهترین‌ها)
Before generating layout code, the agent MUST anchor itself in real-world, high-converting, modern design trends:
1. **Design Archetype Sourcing:** Synthesizes patterns from premier platforms:
   - **Mobbin & Land-book:** Clean UX flows, navigation paradigms, onboarding patterns.
   - **Dribbble & Figma Community:** Card treatments, spatial cadence, modern micro-interactions.
   - **Awwwards & Godly:** Typographic confidence, editorial layouts, subtle luxury.
2. **Concept Ideation & Visual Spec:**
   - Define a vibrant, modern **Light Theme** as the default baseline (clean whites, subtle off-white `#fafafa`, crisp charcoal text, distinct brand accent).
   - If image generation tools are available, generate a conceptual mockup.
   - If text-only, formulate a clear visual direction (color palette, typography hierarchy, section flow).

### 👁️ Pillar 2: Living Visual Feedback Loop (دیدن خروجی با چشم ایجنت)
No UI task is complete without eyes on the rendered output:
1. **Headless Browser Execution:** Renders the generated code using Playwright / browser tools.
2. **Multi-Viewport Screenshot:** Captures a high-resolution screenshot (Desktop 1440px and Mobile 390px).
3. **Multimodal Self-Critique:** The agent inspects the rendered image:
   - *Whitespace & Breathing Room:* Are elements crowded or margins uneven?
   - *Typographic Balance:* Is the headline-to-body scale harmonious?
   - *Visual Richness:* Does the page feel alive with high-quality imagery or dull/empty?
4. **Auto-Refinement:** Fixes any visual awkwardness before delivering the final code to the user.

---

## 🧹 Rule Pruning & Baseline Hygiene Matrix

| Former Obstacle | Status in v2.0 | New Placement & Behavior |
| :--- | :--- | :--- |
| **Strict Emoji Prohibition** | **Demoted** | 1-line styling hygiene: "Use clean vector SVGs (`lucide`) instead of raw emojis for professional UI." |
| **BiDi `<bdi>` & Technical Tags** | **Scoped strictly to RTL** | **Zero impact on English/LTR projects.** Only activated when the output language is Persian/Arabic. |
| **Non-Mirrored Fixed Structure** | **Scoped strictly to RTL** | Moved entirely into `RTL.md`. LTR layouts behave naturally. |
| **OKLCH Math & 7:1 AAA formulas** | **Replaced** | Replaced with human-intuitive contrast: "Ensure crisp, readable contrast between text and background." |
| **Mandatory Dual-Theme (Every Project)**| **Restructured** | **Vibrant Light Mode is the primary default.** Dark mode is optional (toggle) or domain-specific (crypto/gaming/terminal). |
| **Mandatory `--color-vibe-on-primary`** | **Removed** | Use standard Tailwind classes (`text-primary-foreground` or direct high-contrast text color). |
| **7 Rigid Style Jails** | **Unlocked** | Changed from a rigid constraint to an open library of creative inspiration. |
| **24 Mandatory Domain Widgets** | **Repurposed** | Transformed into an optional "Component Idea Bank", not a forced template. |
| **Spring Bezier & CSS Grid Accordions** | **Simplified** | Use smooth, standard Tailwind transitions (`duration-300 ease-out`). Advanced physics is opt-in. |
| **Custom Cursor Tracking Dot** | **Removed from Agent** | Preserved only in the showcase gallery; strictly forbidden in standard business UI. |
| **Max Blur Surface = 3 Budget** | **Removed** | Simplified to: "Use backdrop blur tastefully without cluttering the view." |
| **Abstract Quad-Composite Gate** | **Replaced** | Replaced by the actionable **Pillar 2 Living Screenshot Loop**. |
| **Rigid 44px Touch Target Penalties**| **Softened** | Standard mobile UX guideline: ensure interactive buttons are comfortably tap-able on touch devices. |

---

## 📸 Asset & Imagery Strategy
- **Never produce empty gray placeholder boxes.**
- If AI image generation is accessible: generate tailored hero imagery.
- If web-assisted: embed curated, high-resolution Unsplash URLs with specific dimensions (`&auto=format&fit=crop&w=1200&q=80`).
- Use crisp vector icons (`lucide-react` or clean SVGs).
