# 🧪 Vibe UI Evaluation Suite (`evals/`)

This directory contains formal evaluation benchmarks for measuring AI coding agent outputs when guided by **`vibe-ui-agent`** and the Vibe UI Skills Suite.

---

## 🎯 Purpose of the Eval Suite

Prompt libraries often fail silently because LLMs drift into generic templates ("AI slop") or violate accessibility/RTL invariants. This suite provides **verifiable test specifications** that test:
1. **Visual Anti-Slop & Novelty:** Absence of predictable cliché gradients or flat gray borders.
2. **Accessibility & WCAG AA:** Proper semantic tags (`<button>`, `<bdi>`), keyboard reachability, and visible focus rings.
3. **Semantic RTL Resilience:** Preservation of physical macro coordinates while correctly mirroring directional cues and isolating English terms.
4. **Performance Budgets:** Strict caps on backdrop-filter layers and mandatory reduced-motion wrapping.

---

## 📂 Test Cases & Examples in this Suite

| Test Case File | Domain Archetype | Production Example | Key Verification Focus |
| :--- | :--- | :--- | :--- |
| [`saas_dashboard_eval.md`](saas_dashboard_eval.md) | `HIGH_PERFORMANCE_SAAS` | [`examples/saas_ai_hero.html`](../examples/saas_ai_hero.html) | Minimalist SaaS chemistry, JetBrains Mono metrics, tool call chips, max 3 blur layers. |
| [`persian_rtl_landing_eval.md`](persian_rtl_landing_eval.md) | `HIGH_TICKET_SERVICE` | [`examples/persian_rtl_bento.html`](../examples/persian_rtl_bento.html) | Vazirmatn font stack, fixed macro coordinates, `<bdi>` punctuation isolation, no flipped grids. |
| [`ai_chat_interface_eval.md`](ai_chat_interface_eval.md) | `AI_NATIVE_ASSISTANT` | [`examples/saas_ai_hero.html`](../examples/saas_ai_hero.html) | Accessible thinking state button, streaming response bubbles, human approval card. |
| [`neobrutalist_store_eval.md`](neobrutalist_store_eval.md) | `CREATIVE_EDITORIAL` | [`examples/neobrutalist_creative_store.html`](../examples/neobrutalist_creative_store.html) | 2.5px solid strokes, hard 4px offset drop shadows, tactile button press, 0 blur layers. |
| [`swiss_editorial_eval.md`](swiss_editorial_eval.md) | `EDITORIAL_READING` | [`examples/swiss_editorial_article.html`](../examples/swiss_editorial_article.html) | Warm paper canvas, Instrument Serif typography, 14.2:1 contrast ratio, zero ambient mesh glow. |

---

## ⚡ How to Run Evaluations

### Option A: Automated Runner (1-Command Verification)
Execute the Python test harness to audit all example files in the repository:
```bash
python evals/run_evals.py
```

### Option B: Interactive AI Agent Evaluation
1. Send the `Prompt` defined in any eval file to your AI agent (Claude Code, Cursor, Antigravity, Copilot).
2. Feed the agent's output through the **`ui-verifier`** skill.
3. Verify that the generated code satisfies all **Expected Properties** and triggers zero **Forbidden Patterns**.
4. Confirm an overall **PASS** status on the UI-Verifier Scorecard.
