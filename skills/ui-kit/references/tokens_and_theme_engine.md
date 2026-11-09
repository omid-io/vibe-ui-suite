# 🎨 Universal Design Tokens & Theme Engine

Universal CSS custom properties, color scales, typography tokens, and Tailwind configuration presets compatible with all UI-Kit components.

> **Living Default Mandate:** `:root` defines **Vibrant Light Mode** as the primary living default (`--color-vibe-canvas: oklch(0.985 0.002 264)`). The `.dark` class serves strictly as an optional OLED cockpit layer. All component layouts run standard LTR by default with zero bidirectional overhead, while logical properties ensure on-demand Persian/Arabic RTL works seamlessly without code duplication.

---

## 1. Native Tailwind CSS v4 `@theme` Architecture (2026 Canonical Standard)

Tailwind CSS v4 replaces JavaScript configuration with declarative CSS `@theme` blocks:

```css
@import "tailwindcss";

@theme {
  /* OKLCH Perceptual Colors — Semantic Palette */
  --color-vibe-canvas: var(--vibe-canvas);
  --color-vibe-surface: var(--vibe-surface);
  --color-vibe-border: var(--vibe-border);
  --color-vibe-primary: var(--vibe-primary-accent);
  --color-vibe-primary-accent: var(--vibe-primary-accent);
  --color-vibe-on-primary: var(--vibe-on-primary);
  --color-vibe-text-primary: var(--vibe-text-primary);
  --color-vibe-text-muted: var(--vibe-text-muted);
  --color-vibe-ring: var(--vibe-ring);

  /* Typography Stacks with Vazirmatn Persian Web Font */
  --font-vibe-sans: Vazirmatn, Inter, system-ui, -apple-system, sans-serif;
  --font-vibe-display: Vazirmatn, Inter, system-ui, sans-serif;
  --font-vibe-mono: JetBrains Mono, Menlo, monospace;

  /* Spring & Snap Physics Curves */
  --ease-vibe-spring: cubic-bezier(0.34, 1.56, 0.64, 1);
  --ease-vibe-snap: cubic-bezier(0.16, 1, 0.3, 1);
  --ease-vibe-glide: cubic-bezier(0.25, 1, 0.5, 1);

  /* Elevation & Specular Shadows */
  --shadow-vibe-glass: inset 0 1px 1px rgba(255, 255, 255, 0.15);
  --shadow-vibe-brutal: 4px 4px 0px #000000;
  --shadow-vibe-brutal-lg: 6px 6px 0px #000000;
}

:root {
  /* Vibe UI Canonical Light Theme */
  --vibe-canvas: oklch(0.985 0.002 264);
  --vibe-surface: oklch(1 0 0);
  --vibe-border: oklch(0.90 0.008 264);
  --vibe-primary-accent: oklch(0.55 0.22 260);
  --vibe-on-primary: oklch(0.99 0 0);
  --vibe-text-primary: oklch(0.14 0.005 264);
  --vibe-text-muted: oklch(0.48 0.015 264);
  --vibe-ring: oklch(0.55 0.22 260);
}

.dark, [data-theme="dark"] {
  /* OLED Cockpit Dark Theme */
  --vibe-canvas: oklch(0.14 0.005 264);
  --vibe-surface: oklch(0.18 0.008 264);
  --vibe-border: oklch(0.28 0.01 264);
  --vibe-primary-accent: oklch(0.65 0.22 260);
  --vibe-on-primary: oklch(0.99 0 0);
  --vibe-text-primary: oklch(0.98 0 0);
  --vibe-text-muted: oklch(0.65 0.015 264);
  --vibe-ring: oklch(0.65 0.22 260);
}
```

---

## 2. Legacy Tailwind v3 Theme Variables (`@layer base`)

For backward compatibility with Tailwind CSS v3 projects:

```css
@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    --card: 0 0% 100%;
    --card-foreground: 222.2 84% 4.9%;
    --popover: 0 0% 100%;
    --popover-foreground: 222.2 84% 4.9%;
    --primary: 221.2 83.2% 53.3%;
    --primary-foreground: 210 40% 98%;
    --secondary: 210 40% 96.1%;
    --secondary-foreground: 222.2 47.4% 11.2%;
    --muted: 210 40% 96.1%;
    --muted-foreground: 215.4 16.3% 46.9%;
    --accent: 210 40% 96.1%;
    --accent-foreground: 222.2 47.4% 11.2%;
    --destructive: 0 84.2% 60.2%;
    --destructive-foreground: 210 40% 98%;
    --border: 214.3 31.8% 91.4%;
    --input: 214.3 31.8% 91.4%;
    --ring: 221.2 83.2% 53.3%;
    --radius: 0.75rem;
  }

  .dark {
    --background: 222.2 84% 4.9%;
    --foreground: 210 40% 98%;
    --card: 222.2 84% 4.9%;
    --card-foreground: 210 40% 98%;
    --popover: 222.2 84% 4.9%;
    --popover-foreground: 210 40% 98%;
    --primary: 217.2 91.2% 59.8%;
    --primary-foreground: 222.2 47.4% 11.2%;
    --secondary: 217.2 32.6% 17.5%;
    --secondary-foreground: 210 40% 98%;
    --muted: 217.2 32.6% 17.5%;
    --muted-foreground: 215 20.2% 65.1%;
    --accent: 217.2 32.6% 17.5%;
    --accent-foreground: 210 40% 98%;
    --destructive: 0 62.8% 30.6%;
    --destructive-foreground: 210 40% 98%;
    --border: 217.2 32.6% 17.5%;
    --input: 217.2 32.6% 17.5%;
    --ring: 224.3 76.3% 48%;
  }
}
```

---

## 3. Directional Agnostic Logical Properties (RTL / LTR)

All components in UI-Kit use CSS Logical Properties for seamless bi-directional support:
- `margin-inline-start` / `ms-*` instead of `ml-*`
- `margin-inline-end` / `me-*` instead of `mr-*`
- `inset-inline-start` / `start-*` instead of `left-*`
- `inset-inline-end` / `end-*` instead of `right-*`
- `text-start` / `text-end` instead of `text-left` / `text-right`
