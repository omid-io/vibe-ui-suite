---
name: ui-kit
description: Exhaustive, domain-agnostic UI/UX Component Engine & Design Intelligence. Curated from Beautiful UI (beautifului.dev - 20 AI primitives), Shadcn UI (ui.shadcn.com - 50+ components), BeUI (beui.dev), Rare UI (rareui.com), and Transitions.dev. Provides copy-paste primitives for AI Thinking states, Streaming text, Tool chips, Approval cards, Task rows, Flowcharts, Insight sparklines, Bento grids, Physics transitions, and accessible UI controls for any tech stack (React, Next.js, Vue, Tailwind, HTML/Vanilla, Flutter) in any visual style or language (LTR/RTL).
triggers: ["ui-kit", "uikit", "beautifului", "beui", "rareui", "transitions.dev", "shadcn", "component library", "ui components", "ai ui", "components", "ui design", "frontend design"]
---

# 🎨 UI-Kit: Exhaustive AI-Native & Modern Component Recipes

`ui-kit` is a 100% domain-agnostic component encyclopedia and design intelligence engine. It contains 70+ accessible component recipes and reference implementations across premier modern design ecosystems.

---

## 🌐 The 7 Pillar Resource Catalogs

| Catalog Reference | Source / Provenance | Component Scope |
| :--- | :--- | :--- |
| [`references/ai_native_full_catalog.md`](references/ai_native_full_catalog.md) | **[Beautiful UI](https://beautifului.dev)** (Adapted) | **20 AI Primitives:** Loading State, Thinking State, Streaming Text, Approval Card, Tool Chips, Task Rows, Chat, Prompt Bar, Recommendation Card, Context Cards, Diff Table, Records Table, Filter Table, Sidebar Nav, Search HUD, Insight Cards / Sparklines, Code Block with Copy, Fine-tune Card, Selection Actions. |
| [`references/shadcn_full_catalog.md`](references/shadcn_full_catalog.md) | **[Shadcn UI](https://ui.shadcn.com)** (MIT) | **50+ UI Primitives:** Forms & Inputs (Input, Textarea, Select, Checkbox, Switch, InputOTP, Slider), Overlays & Modals (Dialog, Sheet/Drawer, Popover, Tooltip, Dropdown), Navigation (Command Palette `Cmd+K`, Tabs, Breadcrumb), Feedback (Sonner Toast, Skeleton Shimmer, Progress), Data Display (Accordion, Avatar, Table). |
| [`references/bento_grids_and_cards.md`](references/bento_grids_and_cards.md) | **[BeUI](https://beui.dev) & [Rare UI](https://rareui.com)** (MIT) | **Bento & Interactive Cards:** 3-Col & 4-Col Asymmetric Bento Grids, Glassmorphism 2.0 Inset Specular Cards, Animated Gradient Shimmer Buttons, Metric HUD Tiles. |
| [`references/modern_vibe_components.md`](references/modern_vibe_components.md) | **[Aceternity](https://ui.aceternity.com) & [Magic UI](https://magicui.design)** (Adapted) | **Modern Vibe Recipes:** Aurora Glow Background, Spotlight Hero, Neon Border-Beam Cards, 3D Tilt Cards, Infinite Smooth Marquee, Shimmer Glow Buttons, Floating Dock Island. |
| [`references/data_and_flow.md`](references/data_and_flow.md) | **Flow & Metric Visualization** | **Workflow & Canvas Nodes:** Modular Trigger Nodes, If/Else Conditional Splitters, Action Execution Cards, Micro Sparkline Meters, Dotted Grid Canvas. |
| [`references/physics_transitions_catalog.md`](references/physics_transitions_catalog.md) | **[Transitions.dev](https://transitions.dev)** (Zero-Dep) | **Zero-Dependency Motion:** Pure CSS Grid Dynamic Height Accordions (`0fr` -> `1fr`), Spring Easing Bezier Curves, Staggered List Reveals, JS Number Flip Counters, 3D Tilt Cards. |
| [`references/tokens_and_theme_engine.md`](references/tokens_and_theme_engine.md) | **Universal Design System** | **Tokens & Layouts:** Theme Variables (Light, Dark, Custom), Directional Logical CSS (`ms-*`, `me-*`, `start-*`, `end-*`) for universal LTR & RTL support. |

---

## ♿ Mandatory Accessibility & Quality Contract (WCAG AA)

When generating or adapting any component from this kit, the AI Agent must strictly uphold:
1. **Semantic HTML Elements:** Use `<button>` for clickables (never `<div onclick>`), `<nav>`, `<aside>`, `<dialog>`, etc.
2. **Keyboard Operability & Visible Focus:** All interactive controls must respond to `Enter`/`Space` and feature high-contrast `focus-visible:ring-2` states.
3. **Screen Reader Semantics:** Provide `aria-expanded`, `aria-controls`, `aria-label`, and `role="region"` for collapsing or stateful elements.
4. **Functional Motion Sensitivity:** Disable non-essential decorative loops, parallax, and continuous spring animations under `@media (prefers-reduced-motion: reduce)`; preserve essential functional state transitions (e.g. accordion disclosure, button states) with short, non-disorienting durations ($\le 150\text{ms}$).

---

## ⚡ Universal Usage Workflow

Whenever asked to build, design, or refactor any frontend component or view:
1. **Identify the Component Domain:** AI Reasoning, Forms, Navigation, Data Visualization, or Layout.
2. **Read the Target Reference:** Pull exact markup, Tailwind utility classes, and zero-JS transitions from `references/`.
3. **Adapt Seamlessly:** Match the target framework (React, Vue, HTML/JS, Tailwind), color theme, and language direction (LTR / RTL).

---

## 📐 Semantic & Fixed-Structure RTL Architecture

When implementing components in Persian, Arabic, or Bilingual LTR/RTL views:
1. **Preserve Macro Layout & Coordinates:**
   - Global grid columns, module cards, slider tracks, and navigation bars remain physically stable. Do not indiscriminately flip entire layout grids.
2. **Target Textual & Paragraph Direction:**
   - Apply `direction: rtl` and text alignments to text nodes, headings, and descriptions.
3. **Mirror Semantic Directional Affordances:**
   - Navigation arrows (previous/next), sequential timelines, step wizards, and back-buttons must mirror semantically to follow reading flow.
4. **BiDi Resilience & Strict Monospace LTR:**
   - Mixed English brand names or tech terms inside Persian sentences must not scramble punctuation (`unicode-bidi: plaintext` or `<bdi>`).
   - Code blocks, numbers, metric counters (`99.98%`), and URLs always stay strictly `direction: ltr !important; text-align: left !important`.

---

## 📱 Mobile-Native Resilience & Touch Polish

To ensure web interfaces feel as polished and responsive as native iOS and Android apps, enforce the following ergonomic invariants:

1. **Dynamic Viewport Height (`100dvh`):**
   - Never use static `height: 100vh` for full-screen modals, sheets, or mobile heroes. Mobile browser address bars collapse/expand on scroll, causing jarring layout jumps.
   - Use `min-height: 100dvh;` with graceful fallback:
     ```css
     min-height: 100vh;
     min-height: 100dvh;
     ```

2. **iOS Safari Input Auto-Zoom Guard:**
   - In iOS Safari, any `<input>`, `<select>`, or `<textarea>` with `font-size < 16px` triggers an involuntary, disruptive zoom on touch focus.
   - Always ensure base font size for form controls on mobile is at least `16px` (`text-base` in Tailwind):
     ```css
     @media (max-width: 640px) {
       input, select, textarea {
         font-size: 16px !important;
       }
     }
     ```

3. **Tap Highlight Suppression:**
   - Remove default WebKit gray rectangular tap flash on clickable elements:
     ```css
     button, a, [role="button"] {
       -webkit-tap-highlight-color: transparent;
       touch-action: manipulation; /* Eliminates 300ms tap delay */
     }
     ```

4. **Sticky Hover State Elimination:**
   - Touch devices emulate mouse hover upon touch tap, leaving buttons permanently stuck in their hover visual state after the finger lifts.
   - Strictly encapsulate all hover pseudo-classes in fine pointer media queries:
     ```css
     @media (hover: hover) and (pointer: fine) {
       .interactive-element:hover {
         /* Hover transformation/glow here */
       }
     }
     ```

5. **Physical Touch Target Dimensions (WCAG 2.5.8):**
   - All interactive touch targets (buttons, icon triggers, pills) must provide an active bounding box of at least **44px × 44px** on touch viewports, even if the visible icon is smaller (use transparent hit padding or pseudo-elements).

---

## 📜 Provenance, Adaptation & Legal Licensing

- **Clean-Room Implementation:** All 70+ components in this encyclopedia are clean-room adaptations, re-written from scratch as portable semantic Tailwind CSS / HTML / React recipes.
- **No Proprietary Runtime Bundles:** This library does not import or re-distribute proprietary binaries or runtime npm packages.
- **MIT & Open Source Attribution:**
  - **Shadcn UI:** Re-implemented following the open-source patterns under the MIT License.
  - **Transitions.dev:** Pure CSS motion patterns adapted from open CSS specifications.
  - **Beautiful UI, BeUI & Rare UI:** Conceptual layout patterns synthesized into production-ready accessible code recipes.

