# 🧪 Eval 03: AI Assistant Thinking State & Human-in-the-Loop Approval

**Test ID:** `EVAL-AI-CHAT-03`  
**Domain:** `AI_NATIVE_ASSISTANT`  
**Archetype:** Glassmorphism 2.0 / Dark Canvas  

---

## 📝 Input Prompt
```text
vibe-ui-agent create an AI chat response component featuring a collapsible thinking state, tool execution pill, and an approval card for database execution.
```

---

## ✅ Expected Properties (Pass Criteria)
1. **AI Native Primitives:**
   - Includes **Thinking State** primitive with animated pulsing skeleton and elapsed execution timer.
   - Includes **Tool Execution Chip** showing status: `Executing bash command...` with spinner.
   - Includes **Approval Card** with destructive action styling, parameter diff preview, and distinct `Approve` / `Reject` buttons.
2. **Accessibility & WCAG AA:**
   - Collapsible thinking accordion uses a semantic `<button>` with `aria-expanded="false"` and `aria-controls="thinking-content"`.
   - Focus rings visible on all interactive buttons.
   - Destructive action button has distinct styling and accessible text.
3. **Motion:**
   - Accordion expansion uses pure CSS Grid height interpolation (`grid-template-rows: 0fr` $\to$ `1fr`) without rigid JavaScript heights.
   - All keyframe pulses wrapped with `@media (prefers-reduced-motion: reduce)`.

---

## ❌ Forbidden Patterns (Fail Triggers)
- ❌ Clickable `<div>` without keyboard support.
- ❌ Hardcoded JavaScript pixel height animations (`height = 240px`).
- ❌ Missing ARIA attributes on collapsible sections.
