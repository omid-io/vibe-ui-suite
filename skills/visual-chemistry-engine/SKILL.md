---
name: visual-chemistry-engine
description: The Visual Architecture & Design Chemistry Engine for mr-ui-designer (v2026). Transforms design specs into production-grade interfaces across 5 distinct visual chemistries (Minimalist SaaS, Luxury Glassmorphism 2.0, Neobrutalism, Swiss Editorial, and Stripe Crisp Light) while enforcing the Anti-Repetition Protocol and Semantic RTL.
triggers: ["mr-ui-designer", "mr_ui_designer", "visual chemistry engine", "visual_chemistry_engine", "visual-chemistry", "style engine", "build website", "landing page", "ui style", "design chemistry"]
---

# 🎨 Visual Chemistry Engine (mr-ui-designer Style Core)

The `visual-chemistry-engine` serves as the primary aesthetic and visual architecture core commanded by **`mr-ui-designer`**. It eliminates generic "AI slop" by strictly enforcing **bespoke, intentional visual chemistry**. Instead of forcing one rigid style, it provides **5 Production-Grade Design Archetypes**.

---

## 🎨 The 6 Master Visual Chemistries

The agent autonomously detects the domain or explicit user request and selects the matching chemistry:

```
                  ┌─► 1. Minimalist High-Performance SaaS (Linear / Vercel / Raycast)
                  ├─► 2. Luxury Obsidian & Glassmorphism 2.0 (AI Flagships / Web3 / Luxury)
PROMPT / DOMAIN ──┼─► 3. Neobrutalism & Playful High-Contrast (Creative / Gumroad / Notion)
                  ├─► 4. Swiss Editorial & Paper Craft (Portfolios / Journalism / Architecture)
                  ├─► 5. Modern Crisp Light (Stripe / Enterprise Fintech)
                  └─► 6. Apple Cupertino Fluid & Human Interface (WWDC Craft / Native Web)
```

---

### 1. ⚡ Minimalist High-Performance SaaS (Linear / Vercel Style)
*Best for: Developer tools, B2B SaaS, Analytics, Modern Dashboards.*
- **Canvas:** Pure Charcoal / Pitch Zinc (`#09090b` or `#000000`)
- **Borders:** Crisp, razor-sharp 1px borders (`border: 1px solid rgba(255, 255, 255, 0.08)`)
- **Lighting:** Ultra-subtle directional linear gradients (`linear-gradient(180deg, rgba(255,255,255,0.03) 0%, transparent 100%)`)
- **Typography:** Inter / Geist / JetBrains Mono for metrics.
- **Micro-Interactions:** Subtle hover outline glow (`hover:border-zinc-600`), keyboard shortcuts HUD (`⌘K`).

---

### 2. 💎 Luxury Obsidian & Glassmorphism 2.0
*Best for: AI Flagship products, Luxury brands, High-ticket services, Cutting-edge showcases.*
- **Canvas:** Deep Obsidian Velvet (`#0a0812` / `oklch(0.12 0.012 260)`)
- **Atmosphere:** SVG Fractal Noise overlay + Ambient Mesh Glow (`radial-gradient` multi-stop blur).
- **Glass Specular:** Multi-layer frosted cards with Fresnel specular highlights (`box-shadow: inset 0 1px 1px rgba(255,255,255,0.15)`).
- **Typography:** High-contrast Serif titles (Playfair / Newsreader) + Sans body (Inter).

---

### 3. 🎨 Neobrutalism & Playful High-Contrast (Gumroad / Figma Style)
*Best for: Creative agencies, Creator economy, Youth/EdTech, Bold Web Apps.*
- **Canvas:** Vibrant Pastels (Yellow `#fef08a`, Cyan `#a5f3fc`, Lavender `#e9d5ff`) or stark white with `#000` structure.
- **Borders & Strokes:** Thick, deliberate 2px-3px solid black outlines (`border: 2.5px solid #000000`).
- **Shadows:** Hard, unblurred offset drop shadows (`box-shadow: 4px 4px 0px #000000`).
- **Tactile Feedback:** Physical button-press active states (`transform: translate(2px, 2px); box-shadow: 2px 2px 0px #000000`).

---

### 4. 📰 Swiss Editorial & Paper Craft
*Best for: Thought leadership, Publications, High-end Portfolios, Minimalist Commerce.*
- **Canvas:** Warm Paper Ivory (`#faf8f5` / `oklch(0.98 0.005 80)`)
- **Grid Architecture:** Strict asymmetrical typographic grids, oversized drop caps, structured hairline rules (`#e5e0d8`).
- **Typography:** Refined editorial Serif headers (Instrument Serif, Bodoni) with generous tracking and strict leading.
- **Restraint:** Zero blur or floating glowing orbs; 100% typographic hierarchy and spatial rhythm.

---

### 5. ☀️ Modern Crisp Light (Stripe Style)
*Best for: Fintech, Enterprise SaaS, Trust-heavy platforms, Global consumer products.*
- **Canvas:** Crisp Porcelain Snow (`#ffffff` / `#f8fafc`)
- **Surfaces:** Pure white floating cards with multi-stage ambient diffuse shadows (`box-shadow: 0 1px 3px rgba(0,0,0,0.05), 0 10px 25px rgba(0,0,0,0.03)`).
- **Accents:** Electric Sapphire Blue (`#2563eb`), Emerald Mint, or Violet with strict 4.5:1 text contrast compliance.
- **Crispness:** High-contrast data tables, subtle badge chips, and refined micro-borders (`#e2e8f0`).

---

### 6. 🍏 Apple Cupertino Fluid & Human Interface (WWDC Craft Style)
*Best for: Consumer utilities, Creative production tools, Productivity suites, Apple ecosystem web apps.*
- **Canvas:** Natural Tinted Canvas (`light: oklch(0.975 0.005 250)`, `dark: oklch(0.12 0.008 250)`)
- **Translucent Chrome:** Multi-layer frosted navigation bars and floating toolbars with content scrolling underneath (`backdrop-filter: blur(20px) saturate(180%)`).
- **Surface Resilience:** Explicit `@media (prefers-reduced-transparency: reduce)` fallback with opaque high-contrast background.
- **Continuous Curvature (Squircle):** Smooth Apple-style corner squircle radii (`border-radius: 20px` to `28px` with proportional inner child nested radii: $R_{inner} = R_{outer} - padding$).
- **Optical Typography:** Dynamic tracking & leading hierarchy:
  - Display / Hero Headings: `letter-spacing: -0.025em; line-height: 1.05;`
  - Body Text: `letter-spacing: -0.005em; line-height: 1.5;`
  - System font priority: `-apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text", system-ui, sans-serif`.
- **System Accents:** High-fidelity Apple System Blue (`oklch(0.58 0.22 255)`), System Indigo, or Natural Graphite with rigorous WCAG 2.2 AAA contrast verification.

---

## 🛡️ Anti-Repetition Protocol (Preventing "Vibe UI Slop")

To prevent every generated interface from collapsing into a predictable "dark obsidian glassmorphism" clone, the AI Agent must actively diversify across projects by varying at least **3 structural dimensions**:

1. **Archetype Selection:** Do NOT default blindly to Luxury Obsidian. Match the exact domain (e.g. Developer Tools ➔ Minimalist SaaS, Creative ➔ Neobrutalism, Editorial/Reading ➔ Swiss Craft, Consumer/Fintech ➔ Stripe Crisp Light).
2. **Hero Composition:** Alternate between Split-Screen, Centered Minimal, Asymmetric Editorial, and HUD/Dashboard-Driven heroes.
3. **Card & Grid Density:** Alternate between high-density compact telemetry HUDs, expansive generous Swiss whitespace, and modular Bento tiles.
4. **Lighting & Surface:** Rotate between pure matte flat surfaces with crisp 1px borders, tactile Neobrutalist hard shadows, and frosted Glassmorphism 2.0.

---

---

## 💎 The Impeccable Craft & Calming Standard (Bakaus Benchmark)

To achieve world-class editorial calm and eliminate visual noise:
1. **The Distill Law:** Before finalizing any generation, strip out unnecessary container borders, redundant badges, and box-in-a-box nesting. Let monumental typography and content breathe with confident negative space.
2. **The Quieter Filter:** Replace aggressive, neon-glowing drop-shadows with subtle, multi-stop inset specular highlights (`box-shadow: inset 0 1.5px 1px 0 rgba(255, 255, 255, 0.22), inset 0 -1px 1px 0 rgba(0, 0, 0, 0.08)`).
3. **Tactile Material Atmosphere:** Introduce procedural SVG film grain (`feTurbulence`) and dot-matrix ambient canvases with fade masks to replace sterile plastic digital surfaces.
4. **Tactile Floating Control Island:** Use fixed-bottom floating islands with glass blur and drag handles for secondary toolbars, theme switchers, or preview controls.
---

## 🕹️ Universal Interactive Modules & Micro-Physics
1. **Interactive 3D Perspective Tilt:** Mouse-following tilt with subtle angles (`perspective(1000px) rotateX/rotateY`) and dynamic specular reflection highlights (`--mouse-x` / `--mouse-y`).
2. **Time-Based Damped Lerp Physics:** Frame-rate independent velocity decays ($\alpha = 1 - e^{-\lambda \cdot \Delta t}$).
3. **Magnetic Spring CTAs:** Responsive cursor-snapping buttons with critically damped release.
4. **Asymmetric Editorial Bento:** Diverse aspect ratios (`2.4:1`, `1.4:1`, `1:1`) to prevent uniform card grids.

---

## 📐 Semantic & Fixed-Structure RTL Architecture
When building Persian, Arabic, or Bilingual LTR/RTL interfaces:
1. **Preserve Macro Layout & Coordinates:** Navbars, grid column structures, and window controls stay physically locked in LTR coordinates.
2. **Apply RTL Exclusively to Textual Content:** Text prose, headings, and descriptions adapt without page mirroring.
3. **BiDi Resilience & Mixed English Brand Names:** Wrap all mixed Latin tokens and acronyms inside `<bdi>` tags.
4. **Code & Technical Metrics Remain Strictly LTR:** Telemetry, digits, URLs, and code snippets stay strictly `direction: ltr !important`.

---

## 🌟 The Lightswind Kinetic Living Benchmark (Living Web Experience)
To guarantee generated interfaces feel tactile, magnetic, and alive rather than static templates:
1. **Curated Editorial Photography via AssetDirector:** Eliminate empty grey boxes with camera icons. Always embed domain-curated high-resolution Unsplash photography with `loading="lazy"`, `decoding="async"`, and dark gradient scrim overlays ensuring WCAG AAA text contrast.
2. **Fluid Trailing Cursor & Magnetic Snapping:** Precision center dot + smooth trailing ring/follower with Kowalski damped lerp physics (`@media (pointer: fine)` only), expanding on interactive elements (`mix-blend-difference` or magnetic scale).
3. **Infinite Kinetic Marquee Rails:** Continuous horizontal scrolling rails (`.animate-marquee`) for tech stacks, badges, and partners with gradient edge fade masks (`mask-image: linear-gradient(...)`) and hover pause.
4. **Interactive Radial Spotlight Dot Matrix:** Ambient dot matrix canvases that respond to cursor movement with dynamic radial illumination masks (`radial-gradient(circle 500px at var(--mouse-x) var(--mouse-y), ...)`).
5. **Scroll-Driven Journey Milestone Timeline:** Progressive vertical glowing timeline rail that fills dynamically during scroll, activating milestones and lighting nodes as they enter view.
6. **Staggered Viewport Entrances:** Progressive scroll reveals using IntersectionObserver with staggered delays and smooth cubic-bezier transitions (`cubic-bezier(0.16, 1, 0.3, 1)`).


