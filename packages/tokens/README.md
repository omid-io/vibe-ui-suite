# @omid-io/tokens

> [!WARNING]
> **Package Migrated to [`vibe-ui-suite`](https://www.npmjs.com/package/vibe-ui-suite)**  
> This package has been superseded by the unified flagship package **`vibe-ui-suite`**. Please migrate your dependencies and CLI usage to:
> ```bash
> npx vibe-ui-suite init
> ```

> Typed OKLCH design tokens, physics curves, and zero-config Tailwind CSS preset for Vibe UI.

## Installation

```bash
npm install @omid-io/tokens
```

## Quick Start with CLI

### 1. Initialize Workspace Contracts (`init`)

Scaffold AI editor contracts (`.cursorrules`, `CLAUDE.md`, `.windsurfrules`) and OKLCH CSS variables in 3 seconds:

```bash
npx @omid-io/tokens init
```

### 2. Add AI-Native Components (`add`)

Add accessible, zero-emoji, verified React 19 component templates directly into your project (`components/vibe-ui/`):

```bash
npx @omid-io/tokens add thinking-drawer
npx @omid-io/tokens add telemetry-hud
npx @omid-io/tokens add contrast-badge
```

### 3. List Registry Components (`list`)

```bash
npx @omid-io/tokens list
```

## Programmatic Usage

### 1. Direct Token Imports

```typescript
import { VISUAL_CHEMISTRIES, MOTION_CURVES, getContrastRatio } from '@omid-io/tokens';

// Access typed OKLCH color spaces
const saasColors = VISUAL_CHEMISTRIES.MINIMALIST_SAAS.colors;
console.log(saasColors.primaryAccent); // 'oklch(0.65 0.22 260)'
```

### 2. Native Tailwind CSS v4 (@theme) — Recommended

In your global stylesheet (e.g. `app/globals.css`):

```css
@import "tailwindcss";
@import "@omid-io/tokens/v4.css";
```

Zero JavaScript configuration files needed. Instantly unlocks:
- Semantic color utilities: `bg-vibe-canvas`, `bg-vibe-surface`, `text-vibe-primary`, `border-vibe-border`
- Physics curves: `ease-vibe-spring`, `ease-vibe-snap`, `ease-vibe-glide` (or utility `.vibe-spring`)
- Shadows: `shadow-vibe-brutal`, `shadow-vibe-glass`

### 3. Tailwind CSS v3 Legacy Plugin (Backward Compatible)

In your `tailwind.config.js` or `tailwind.config.ts`:

```javascript
import vibeUiPlugin from '@omid-io/tokens/tailwind';

export default {
  content: ['./app/**/*.{js,ts,jsx,tsx}', './components/**/*.{js,ts,jsx,tsx}'],
  plugins: [vibeUiPlugin],
};
```

## License

MIT © [Omid Zaferi](https://github.com/omid-io)
