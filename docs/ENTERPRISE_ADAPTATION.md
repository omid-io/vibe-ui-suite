# 🏢 Enterprise Adaptation & Design System Integration Guide

This guide establishes the architectural protocol for engineering organizations looking to integrate Vibe UI's deterministic agent skills into existing proprietary design systems, Figma token pipelines, and component libraries.

---

## 1. Architectural Model & Boundary

Vibe UI enforces a unidirectional 6-skill orchestration DAG commanded by `vibe-ui-agent`. When deploying in an enterprise codebase with an existing design system (e.g. `@company/design-system`, Storybook, or Radix UI):

```
┌───────────────────────────────────────┐
│     Enterprise Brand Tokens           │
│   (Figma Tokens / Style Dictionary)   │
└──────────────────┬────────────────────┘
                   │ Map to OKLCH
                   ▼
┌───────────────────────────────────────┐
│   Vibe UI Token Contract Layer        │
│   (lib/tokens.ts / @vibe-ui/tokens)   │
└──────────────────┬────────────────────┘
                   │ Enforce
                   ▼
┌───────────────────────────────────────┐
│   Agent Generation & UI-Kit Binding   │
│ (Imports @company/ui instead of divs) │
└──────────────────┬────────────────────┘
                   │ Audit
                   ▼
┌───────────────────────────────────────┐
│        ui-verifier Invariants         │
│   (WCAG AA 4.5:1, rAF dt, Logic RTL)  │
└───────────────────────────────────────┘
```

---

## 2. Mapping Enterprise Brand Tokens to OKLCH

Vibe UI standardizes on perceptual OKLCH color spaces to guarantee contrast stability across gamut switches.

### Step-by-Step Translation Formula:
If your company defines brand colors in sRGB hex:

```typescript
// enterprise-tokens.ts
import { oklchFromHex, type OklchColor } from '@vibe-ui/tokens';

export const CompanyBrandTokens = {
  primary: oklchFromHex('#0F172A'),       // Maps to: oklch(0.208 0.042 265.755)
  accent: oklchFromHex('#0D9488'),        // Maps to: oklch(0.601 0.125 186.5)
  surface: oklchFromHex('#FFFFFF'),       // Maps to: oklch(1 0 0)
  surfaceSubtle: oklchFromHex('#F8FAFC'), // Maps to: oklch(0.985 0.002 247.8)
};
```

---

## 3. Registering a Custom Brand Chemistry

Instead of forking Vibe UI to support your company's aesthetic, configure an enterprise archetype in your workspace rules (`.cursorrules` or `CLAUDE.md`):

```markdown
### Enterprise Brand Chemistry: CompanyDesignSystem
- **Base Style:** Minimalist Enterprise SaaS
- **Primary Chroma:** oklch(0.208 0.042 265.755) (Deep Slate)
- **Accent Chroma:** oklch(0.601 0.125 186.5) (Teal Precision)
- **Corner Radii:** 6px (Strict Corporate Geometry)
- **Elevation:** 1px border `oklch(0.92 0.005 264)` with 0px blur drop-shadow
- **Typography:** Inter Variable for interface, JetBrains Mono for telemetry
```

---

## 4. Component Binding Protocol (Internal Libraries)

To prevent AI agents from generating raw HTML or generic Tailwind primitives when your company has existing UI components:

Add the following binding declaration to your workspace adapter (`CLAUDE.md` or `.cursorrules`):

```markdown
### Enterprise Component Binding Matrix
Whenever generating UI components, DO NOT output raw markup. Always import and bind to `@company/ui-core`:
- Button -> `import { Button } from '@company/ui-core/button'`
- Modal / Dialog -> `import { Dialog } from '@company/ui-core/dialog'`
- Dropdown -> `import { DropdownMenu } from '@company/ui-core/dropdown'`
- Input -> `import { Input } from '@company/ui-core/input'`
```

---

## 5. Parameterizing `ui-verifier` for Enterprise Baselines

If your internal compliance standard mandates stricter contrast or specific brand invariants:

```json
{
  "$schema": "./schemas/design-spec.v1.schema.json",
  "spec_version": "2.2.1",
  "archetype": "enterprise_custom",
  "verification_profile": {
    "min_body_contrast": 7.0,
    "min_heading_contrast": 4.5,
    "max_backdrop_filters": 2,
    "disallow_raw_emojis": true,
    "enforce_semantic_rtl": true
  }
}
```

This guarantees that `evals/run_evals.py` validates code against your specific corporate design requirements without regressions.
