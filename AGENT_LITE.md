# Vibe UI Suite — Core Engineering Directives (Lite)

> High-density, actionable frontend rules. Preserves technical constraints while eliminating token overhead.

---

## 1. Five-Station Pipeline
Execute UI generation and refactoring across five deterministic phases:
1. **Concept**: Map domain, layout archetype (asymmetric flow, operational grid, timeline, or bento), and spatial density.
2. **Assets**: Mine curated photography (Unsplash vault with Asset Intelligence), SVG icons, and verified micro-interactions.
3. **Art Direction**: Bind OKLCH color tokens, typography scales (Vazirmatn + sans), and physics easing curves.
4. **Engineering Build**: Produce clean, single-author HTML/React markup with Tailwind v4 `@theme` tokens, spring physics, and zero seams.
5. **Adversarial Gate**: Validate multi-viewport layout (1440px desktop, 390px mobile), WCAG AA contrast ($\ge 4.5:1$), and 0px horizontal overflow with closed-loop healing ($\le 3$ loops).

---

## 2. Visual & Spatial Standards
- **Light-First Canonical Standard**: Light mode is ALWAYS the primary, default design. Surfaces: `#ffffff` / `#f8fafc`; borders: `#e2e8f0`; typography: `#0f172a` / `#334155`.
- **OLED Cockpit Dark Mode (Secondary)**: Dark mode is an optional secondary layer. Foundations: `#0b0f19` / `#0f172a` (never flat pitch-black or muddy grey); specular highlights: `inset 0 1px 0 rgba(255, 255, 255, 0.08)`; crisp AA contrast.
- **Anti-Cosmetic Patch**: Modifying only colors or emojis while leaving flawed DOM layouts intact is forbidden. Must overhaul structural spatial rhythm, padding scales, and responsive hierarchies.
- **Form Follows Function**: Avoid repetitive bento grid boxes when inappropriate. Tailor layout to the specific domain.

---

## 3. Motion & Tailwind v4 Tokens
- **Tailwind v4 `@theme`**: All tokens reside in CSS `@theme` blocks (`--color-vibe-*`, `--ease-vibe-*`, `--font-vibe-*`).
- **Spring Physics Standard**: Use `ease-vibe-spring transition-all` or `.vibe-spring`. The utility `transition-vibe-spring` is invalid and forbidden.
- **Reduced Motion Invariant**: Every motion token or animation MUST include an `@media (prefers-reduced-motion: reduce)` override setting duration to $\le 150\text{ms}$ or `none`.

---

## 4. Typography & Internationalization (RTL)
- **Root Direction**: Root document remains `dir="ltr"`.
- **Font Stack**: `Vazirmatn, Inter, system-ui, -apple-system, sans-serif`.
- **Bidirectional Isolation**: Wrap all numeric metrics, timestamps, and code identifiers in `<bdi>` tags.
- **Logical Properties**: Use CSS logical properties (`margin-inline-start`, `inset-inline-start`, `text-start`) instead of physical directional properties (`left`, `right`).

---

## 5. Verification & Operational Mandates
- **Pre-Delivery Verification**: Validate syntax before presenting deliverables (`node -c <file.js>`, `tsc --noEmit`, `python -m py_compile`). Zero broken syntax permitted.
- **Zero Orphan Tasks**: Kill hanging background tasks explicitly (`taskkill /F /T`). Clean up residual processes at turn conclusion.
- **Zero Unsolicited Versions**: Never quote or announce version numbers in greetings, chat introductions, or banners unless explicitly requested by the user. Keep docs and prompts evergreen.
- **Asset Intelligence**: When selecting photography, respect `focal_point`, `negative_space` (for text overlay contrast), and `mobile_crop_safe` metadata.
