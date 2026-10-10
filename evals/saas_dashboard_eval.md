# 🧪 Eval 01: B2B SaaS Dashboard & AI Agent Metric HUD

**Test ID:** `EVAL-SAAS-01`  
**Domain:** `HIGH_PERFORMANCE_SAAS`  
**Archetype:** Minimalist SaaS (Linear / Vercel style)  

---

## 📝 Input Prompt
```text
vibe-ui-agent build a dark developer analytics dashboard hero with live agent execution metrics and active tool status chips.
```

---

## ✅ Expected Properties (Pass Criteria)
1. **Visual System:**
   - Deep charcoal/pitch canvas (`#09090b` or `oklch(0.14 ...)`).
   - Subtle 1px crisp borders (`border-white/10` or `oklch(0.28 ...)`).
   - Monospace font (`JetBrains Mono` or equivalent) on all numbers, latency meters, and timestamps.
2. **Component Integration:**
   - Includes at least 1 **Tool Execution Chip** from `ui-kit` with running/success pulse states.
   - Includes metric cards with secondary delta indicators (`+14.2% from last sprint`).
3. **Accessibility & WCAG AA:**
   - All interactive action chips use `<button type="button">`.
   - Visible focus states: `focus-visible:ring-2 focus-visible:ring-offset-2`.
   - Text contrast ratio $\ge 4.5:1$ on all data labels.
4. **Performance & Motion:**
   - Backdrop filter layers capped at $\le 2$.
   - Animation pulses wrapped with `@media (prefers-reduced-motion: reduce)`.

---

## ❌ Forbidden Patterns (Fail Triggers)
- ❌ Cliché purple-to-blue linear gradients on buttons.
- ❌ Using raw unicode emojis (e.g. 🚀, ⚡, 🤖) instead of inline SVG icons.
- ❌ Using `<div onclick="...">` for interactive chips or metric toggles.
- ❌ Generic white cards with blurry black shadows.
