# vibe-ui-suite

<p align="center">
  <strong>Deterministic design contracts, component recipes, and WCAG evaluation gates for AI coding agents.</strong>
</p>

<p align="center">
  <a href="https://www.npmjs.com/package/vibe-ui-suite"><img src="https://img.shields.io/npm/v/vibe-ui-suite?color=blue&style=flat-square" alt="NPM Version" /></a>
  <a href="https://marketplace.visualstudio.com/items?itemName=omid-io.vibe-ui-vscode"><img src="https://img.shields.io/visual-studio-marketplace/v/omid-io.vibe-ui-vscode?color=blue&style=flat-square&logo=visual-studio-code" alt="VS Code Marketplace" /></a>
  <a href="https://open-vsx.org/extension/omid-io/vibe-ui-vscode"><img src="https://img.shields.io/open-vsx/v/omid-io/vibe-ui-vscode?color=blue&style=flat-square" alt="Open-VSX Version" /></a>
  <a href="https://github.com/omid-io/vibe-ui-suite/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" alt="License" /></a>
</p>

---

## ⚡ What is Vibe UI Suite?

Modern AI coding agents (Cursor, Claude Code, Windsurf, v0) are fast, but they often produce **"AI Slop"**:
- Clichéd, low-contrast purple/indigo gradients that fail basic accessibility (WCAG AA).
- Uncalibrated spacing, broken mobile layouts, and excessive blur overlays.
- Broken bidirectional text (RTL/BiDi) and inverted business formulas.

**`vibe-ui-suite`** acts as a **machine-verifiable design linter and contrast gatekeeper**. It equips your project with typed OKLCH color spaces, physics animation curves, accessible component recipes, and automated editor rule contracts (`.cursorrules`, `CLAUDE.md`, `.windsurfrules`).

---

## 🚀 Quick Start (3 Seconds)

### 1. Initialize Workspace Contracts (`init`)

Scaffold AI editor contracts and OKLCH CSS variables in your project with zero manual configuration:

```bash
npx vibe-ui-suite init
```

This interactive command sets up:
- `.cursorrules` / `CLAUDE.md` / `.windsurfrules` with strict anti-slop invariants.
- 5 distinct visual chemistry themes (Minimalist SaaS, Swiss Editorial, Neobrutalism, Luxury Glass 2.0, Stripe Crisp Light).
- Native Tailwind CSS v4 variables or Tailwind v3 configuration.

---

### 2. Add Accessible Component Primitives (`add`)

Add verified, zero-emoji, accessible React 19 component templates directly into your codebase (`components/vibe-ui/`):

```bash
# Add an expandable reasoning / thinking trace drawer
npx vibe-ui-suite add thinking-drawer

# Add a dense telemetry HUD with live metric formatting
npx vibe-ui-suite add telemetry-hud

# Add a real-time WCAG AAA contrast indicator badge
npx vibe-ui-suite add contrast-badge
```

### 3. List Registry Components (`list`)

```bash
npx vibe-ui-suite list
```

---

## 🎨 Programmatic Usage

### 1. Native Tailwind CSS v4 (`@theme`) — Recommended

In your global stylesheet (e.g. `app/globals.css` or `src/index.css`):

```css
@import "tailwindcss";
@import "vibe-ui-suite/v4.css";
```

Zero JavaScript configuration files required. Instantly unlocks:
- **Semantic Color Utilities:** `bg-vibe-canvas`, `bg-vibe-surface`, `text-vibe-primary`, `border-vibe-border`
- **Physics Springs:** `transition-vibe-spring`, `transition-vibe-snap`, `transition-vibe-glide`
- **Surface Elevation:** `shadow-vibe-brutal`, `shadow-vibe-glass`

---

### 2. Direct Token Imports (TypeScript / JavaScript)

Access typed OKLCH color spaces and mathematical contrast verification utilities:

```typescript
import { VISUAL_CHEMISTRIES, MOTION_CURVES, getContrastRatio } from 'vibe-ui-suite';

// Access typed OKLCH color tokens
const saasColors = VISUAL_CHEMISTRIES.MINIMALIST_SAAS.colors;
console.log(saasColors.primaryAccent); // 'oklch(0.65 0.22 260)'

// Verify real-time WCAG contrast mathematics
const contrast = getContrastRatio('#0F172A', '#F8FAFC');
console.log(`Contrast ratio: ${contrast.toFixed(2)}:1`); // e.g. 15.8:1 (AAA Certified)
```

---

### 3. Tailwind CSS v3 Legacy Plugin (Backward Compatible)

In your `tailwind.config.js` or `tailwind.config.ts`:

```javascript
import vibeUiPlugin from 'vibe-ui-suite/tailwind';

export default {
  content: ['./app/**/*.{js,ts,jsx,tsx}', './components/**/*.{js,ts,jsx,tsx}'],
  plugins: [vibeUiPlugin],
};
```

---

## 🛠️ CLI Command Reference

| Command | Description |
| :--- | :--- |
| `npx vibe-ui-suite init` | Interactively scaffold AI editor contracts & OKLCH variables |
| `npx vibe-ui-suite init --dry-run` | Preview file operations without modifying disk |
| `npx vibe-ui-suite add <name>` | Copy an accessible component primitive into `components/vibe-ui/` |
| `npx vibe-ui-suite add <name> -f` | Overwrite existing component with automated `.bak` backup |
| `npx vibe-ui-suite list` | List all available component primitives in the registry |
| `npx vibe-ui-suite -v` | Display installed version |
| `npx vibe-ui-suite -h` | Display full help menu |

---

## 🧩 Companion IDE Extensions

Install the companion extension for real-time contrast auditing, instant color inspection, and 1-click component templates right inside your editor:

- **VS Code Marketplace:** [`omid-io.vibe-ui-vscode`](https://marketplace.visualstudio.com/items?itemName=omid-io.vibe-ui-vscode)
- **Open-VSX Registry:** [`omid-io.vibe-ui-vscode`](https://open-vsx.org/extension/omid-io/vibe-ui-vscode) (for Cursor, Windsurf, VSCodium)

---

## 🌐 Community & Ecosystem

- **Documentation & Live Showcase:** [https://omid-io.github.io/vibe-ui-suite/](https://omid-io.github.io/vibe-ui-suite/)
- **GitHub Repository:** [https://github.com/omid-io/vibe-ui-suite](https://github.com/omid-io/vibe-ui-suite)
- **Issue Tracker:** [https://github.com/omid-io/vibe-ui-suite/issues](https://github.com/omid-io/vibe-ui-suite/issues)

---

## 📄 License

MIT © [Omid Zaferi](https://github.com/omid-io)
