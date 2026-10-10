# 🧪 Benchmark: Swiss Editorial Typographic Article (`evals/swiss_editorial_eval.md`)

## 🎯 Test Objective
Verifies that `vibe-ui-agent` commands `visual-chemistry-engine` to produce a refined Swiss Editorial layout on warm paper ivory, with high-contrast serif typography, asymmetric grid cadence, generous whitespace, and zero artificial glow or blur.

---

## 📥 Benchmark Prompt
```text
vibe-ui-agent create a Swiss Editorial essay layout about design craftsmanship.
Must feature warm paper ivory canvas, high-contrast Instrument Serif headers,
an oversized drop cap, two-column asymmetric metadata sidebar, and zero blur layers.
```

---

## 🔍 Verification Specification & Pass Criteria

### 1. Expected Properties
- [ ] **Canvas & Background:** Warm paper ivory base (`#faf8f5` / `oklch(0.98 0.005 80)`).
- [ ] **Typography:** High-contrast luxury Serif headers (Instrument Serif, Bodoni) paired with clean Sans body.
- [ ] **Asymmetric Grid:** Two-column grid cadence (4-column metadata sidebar + 8-column prose body).
- [ ] **High Contrast:** Meets WCAG AAA minimum (sampled text nodes exceed 12.0:1 contrast ratio).
- [ ] **Restraint:** 0 backdrop blur layers, 0 ambient mesh orbs, and clean hairline rules (`#e7e5e4`).
- [ ] **Iconography:** Clean inline SVG vectors; 0 raw unicode emojis.

### 2. Forbidden Anti-Patterns
- [ ] ❌ Dark obsidian canvas or purple gradients.
- [ ] ❌ Frosted glass or floating glowing orbs.
- [ ] ❌ Raw emojis used as icons.
- [ ] ❌ Centered generic card stacks.

---

## 🏆 Reference Implementation
See [`examples/swiss_editorial_article.html`](../examples/swiss_editorial_article.html).
