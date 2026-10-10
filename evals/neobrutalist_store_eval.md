# 🧪 Benchmark: Neobrutalist High-Contrast Store (`evals/neobrutalist_store_eval.md`)

## 🎯 Test Objective
Verifies that `vibe-ui-agent` commands `visual-chemistry-engine` to produce a high-contrast Neobrutalist interface with hard offset box shadows, physical click states, zero blur layers, and 100% accessible contrast without falling back to generic purple gradients.

---

## 📥 Benchmark Prompt
```text
vibe-ui-agent build a bold neobrutalist creative design store for digital assets.
Must feature high-contrast pastels with pitch black borders, hard offset shadows,
interactive physical buttons, and zero generic gradients or blurry glassmorphism.
```

---

## 🔍 Verification Specification & Pass Criteria

### 1. Expected Properties
- [ ] **Canvas & Borders:** Clean chalk/pastel canvas with deliberate 2.5px-3px solid `#000000` outlines.
- [ ] **Hard Offset Shadows:** Flat non-blurred drop shadows (`box-shadow: 4px 4px 0px #000000` or `5px 5px 0px #000000`).
- [ ] **Tactile Button Press:** Physical click active states (`transform: translate(2px, 2px); box-shadow: 1px 1px 0px #000000`).
- [ ] **Accessibility:** Exceeds WCAG AA contrast (borders & text meet 7.0:1+ contrast against background).
- [ ] **Zero Blur:** Exactly 0 `backdrop-filter: blur(...)` layers used.
- [ ] **Iconography:** 100% inline SVG vector paths; 0 raw unicode emojis.

### 2. Forbidden Anti-Patterns
- [ ] ❌ Frosted glassmorphism blur layers.
- [ ] ❌ Cliché purple-to-blue linear gradients.
- [ ] ❌ Raw emojis used as icons.
- [ ] ❌ Soft ambient diffuse box shadows.

---

## 🏆 Reference Implementation
See [`examples/neobrutalist_creative_store.html`](../examples/neobrutalist_creative_store.html).
