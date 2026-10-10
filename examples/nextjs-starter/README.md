# ⚡ Vibe UI — Next.js 15 & React 19 Production Starter

> **Modern, contract-driven production starter for Next.js 15 App Router showcasing the Vibe UI design architecture: typed OKLCH tokens, 5 visual chemistries, AI-native interactive primitives, zero-emoji SVG iconography, and fixed-structure semantic RTL.**

---

## 🌟 Overview

The **Vibe UI Next.js 15 Starter** provides a reference implementation of the Vibe UI ecosystem (`vibe-ui-agent`). It demonstrates how to replace generic "AI slop" interfaces with intentional visual chemistries, mathematical color scales, and accessible AI interaction primitives.

### Core Architecture Highlights

- **Framework**: [Next.js 15](https://nextjs.org/) (App Router, Server Components & Client Primitives)
- **Runtime**: [React 19](https://react.dev/)
- **Styling**: [Tailwind CSS](https://tailwindcss.com/) with pure CSS variable mappings
- **Perceptual Color**: OKLCH color spaces preserving mathematical contrast across themes
- **Interactive AI Primitives**:
  - `AiThinkingDrawer.tsx`: Pure CSS grid collapsible drawer (`0fr` to `1fr`), radar pulse status, micro-latency tool chips, and full ARIA accessibility.
  - `HeroSection.tsx`: Responsive high-contrast hero layout with telemetry HUD, action CTAs, and semantic bidirectional support.
- **Fixed-Structure Semantic RTL**: Physical macro layout coordinates stay locked; text direction mirrors smoothly; mixed Latin terms are isolated via `<bdi>`; telemetry & code blocks remain strictly LTR (`.ltr-code`).
- **Iconography**: 100% crisp inline SVG vectors (`currentColor`). Zero Unicode emojis in production UI.
- **Accessibility**: Strict WCAG 2.2 AA contrast compliance ($\ge 4.5:1$ body copy, $\ge 3:1$ headers) and `prefers-reduced-motion` fallbacks.

---

## 🎨 The 5 Master Visual Chemistries

The starter includes typed tokens and live CSS runtime switching across all 5 Vibe UI archetypes:

| Chemistry ID | Style Name | Target Domains | Base Palette & Vibe |
| :--- | :--- | :--- | :--- |
| `MINIMALIST_SAAS` | **Minimalist High-Performance SaaS** | Developer tools, B2B platforms, Analytics | Pitch zinc `#09090b`, 1px razor borders, electric indigo accent |
| `LUXURY_GLASS_2` | **Luxury Obsidian & Glassmorphism 2.0** | AI flagships, Luxury brands, High-ticket | Obsidian velvet `#0a0812`, champagne gold `#d4af37`, frosted specular glass |
| `NEOBRUTALISM` | **Neobrutalism & Playful High-Contrast** | Creator economy, Creative tools, Bold apps | Vibrant yellow `#fef08a`, solid black 2.5px borders, hard offset shadows |
| `SWISS_EDITORIAL` | **Swiss Editorial & Paper Craft** | Thought leadership, Publications, Architecture | Warm paper ivory `#faf8f5`, hairline rules, editorial vermilion `#d9381e` |
| `STRIPE_CRISP_LIGHT` | **Modern Crisp Light** | Fintech, Enterprise SaaS, Trust platforms | Porcelain snow `#ffffff`, electric sapphire blue `#2563eb`, diffuse elevation |

---

## 🚀 Quick Start

### 1. Prerequisites
- Node.js $\ge 18.18.0$ (Node 20 or 22+ recommended)
- npm, pnpm, or yarn

### 2. Install Dependencies
```bash
npm install
```

### 3. Run Development Server
```bash
npm run dev
```
Open [http://localhost:3000](http://localhost:3000) in your browser to explore the live interactive showcase.

### 4. Build for Production
```bash
npm run build
npm run start
```

---

## 📁 Project Structure

```
examples/nextjs-starter/
├── app/
│   ├── globals.css              # OKLCH CSS variables for all 5 chemistries & LTR utilities
│   ├── layout.tsx               # Next.js 15 root layout & viewport configuration
│   └── page.tsx                 # Interactive showcase with chemistry & language toggles
├── components/
│   ├── AiThinkingDrawer.tsx     # Collapsible CSS grid reasoning drawer with SVG icons
│   └── HeroSection.tsx          # High-contrast hero section with embedded thinking drawer
├── lib/
│   ├── tokens.ts                # Typed OKLCH token model & VISUAL_CHEMISTRIES dictionary
│   └── utils.ts                 # Class merger utility (clsx + tailwind-merge)
├── next.config.ts               # Next.js configuration
├── tailwind.config.ts           # Tailwind CSS variable mapping
├── tsconfig.json                # TypeScript compiler configuration with "@/*" path alias
└── package.json                 # Dependency manifest
```

---

## 📐 Semantic RTL Protocol

When switching to Persian or Arabic:
1. **Macro Stability**: The asymmetric grid columns, navigation bars, and telemetry rails do not swap sides.
2. **Text-Only RTL**: Headings and descriptions adopt `direction: rtl` and natural text alignment.
3. **BiDi Resilience**: Technical brands and versions (e.g. `Next.js 15`, `Tailwind CSS`) are enclosed in `<bdi>` tags to prevent punctuation scrambling.
4. **Monospace Telemetry**: Metrics (`1.2ms`, `99.99%`) use the `.ltr-code` utility class to lock left-to-right number ordering.

---

## 📄 License

MIT © [Omid Zaferi](https://github.com/omid-io)
Part of the **[Vibe UI Suite](https://github.com/omid-io/vibe-ui-suite)**.
