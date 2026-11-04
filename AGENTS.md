# 🎨 Vibe UI Suite — Workspace Directives & Architecture

> **Single Source of Truth for Frontend, UI/UX, and Web Design across the ecosystem.**

---

## 1. Core Architecture: Sovereign Multi-Agent Swarm
All UI design in this repository executes via the 5-phase autonomous swarm commanded by `vibe-ui-agent` (Sovereign Swarm Orchestrator):
- **Zero Direct Code Writing Invariant:** `vibe-ui-agent` never authors HTML/CSS code directly; it orchestrates execution state and dispatches specialized subagents:
  1. **Phase 1 (Concept & Intent):** `vibe-concept-architect` expands raw prompts into a Macro Concept Manifest.
  2. **Phase 2 (Trend & Asset Mining):** `vibe-trend-hunter` curates GitHub >10k stars, Uiverse micro-interactions, and the Unsplash Vault.
  3. **Phase 3 (Art Direction):** `vibe-art-director` synthesizes OKLCH color tokens, typography scales, and the Design Style Blueprint.
  4. **Phase 4 (Master Engineering Build):** `vibe-master-builder` writes pristine, single-author HTML/React code with spring physics and zero seams.
  5. **Phase 5 (Adversarial Inspection Gate):** `vibe-visual-auditor` and `vibe-tech-auditor` run headless screenshot audits (Desktop 1440px / Mobile 390px), WCAG AA contrast (>=4.5:1), and 0px overflow checks with closed-loop healing (<=3 loops).

---

## 2. Spatial & Aesthetic Standards
- **Anti-Cosmetic-Patch Invariant:** Shallow skin patches (tweaking colors or emojis while leaving dead layouts untouched) are strictly forbidden. UI work mandates structural spatial overhaul, dual-theme support, and living browser screenshot verification.
- **Anti-Bento-Dogma Invariant:** Never dogmatically default to repetitive "Bento Grid" card boxes. Form follows function: employ asymmetric flows, single hero focal points, continuous timelines, or high-density operational tables.
- **Creative Synthesis Standard:** Never clone benchmark templates (Mobbin, Dribbble, Awwwards) verbatim. Synthesize core mechanics into bespoke interfaces authentic to the specific project domain.
- **Universal Dual-Theme Mandate (Light + Dark):** Every interface must natively support semantic light/dark themes with zero gravitational dark bias (calibrate daylight ivory, golden hour, twilight based on domain context).
- **On-Demand RTL Protocol:** Root stays `dir="ltr"`. Persian text is scoped with Vazirmatn fallback, `<bdi>` token isolation, and non-mirrored coordinates per `RTL.md`.

---

## 3. Mandatory Multi-Registry Release Law ("Publish")
Whenever publishing or releasing this suite:
1. **Version Bump & Skill Sync:** Synchronize canonical semantic version across all manifests (`version.manifest.json`, `package.json` in root, packages, starter) and sync all skills from `skills/` to `.agents/skills/` and `packages/vibe-ui-suite/skills/`.
2. **Changelog & Readme Update:** Record changes in root `CHANGELOG.md` and `packages/vibe-ui-vscode/CHANGELOG.md`. Update `README.md` if features, tokens, or options changed.
3. **Mandatory Pre-Release Inspector Agent Audit (Regression & Compatibility Gate):** Before proceeding to deployment, always dispatch an independent Inspector/Auditor Agent (or run adversarial multi-file diff inspection) to audit all code changes. The inspector must verify that newly added features or modifications do not introduce regressions, break backwards compatibility, or create conflicts/inconsistencies with existing components, templates, CLI commands, tokens, or prior architectural standards.
4. **Build & Automated Quality Gates:** Run `python scripts/validate_versions.py`, `python evals/run_evals.py --json`, and Gitleaks scan (`E:\programming\Tools\gitleaks\gitleaks.exe`).
5. **NPM & Open-VSX Publishing:** Build `packages/vibe-ui-suite` and package `vibe-ui-vscode-*.vsix`. Commit, tag (`vX.Y.Z`), and push to GitHub to trigger automated publishing to **NPM** and **Open-VSX** via `.github/workflows/publish.yml`.
6. **Microsoft Visual Studio Marketplace Upload:** Run `python scripts/publish_marketplace_browser.py`, connect to the active Chrome publisher session on `https://marketplace.visualstudio.com/manage/publishers/omid-io` via Playwright MCP, open the `Update` dialog, inject the VSIX via `browser_run_code_unsafe(filename='run_upload.js')`, and verify version status reaches "Verifying" or "Published".

---

## 4. Mandatory Pre-Publish Compatibility & Regression Inspector Gate
- **Zero-Conflict & Zero-Regression Law:** Under no circumstances may any release, package bump, or git tag be pushed without prior adversarial review by a dedicated Inspector Agent.
- **Inspector Mandate:**
  1. Inspect the full `git diff` against the previous stable state.
  2. Verify that newly introduced capabilities, agents, or CLI arguments do not break legacy workflows, component contracts, or starter examples (`examples/nextjs-starter`).
  3. Ensure token names, schema versions, and manifest exports maintain seamless consistency and backwards compatibility across the monorepo.
  4. If any conflict, regression, or inconsistency is detected, deployment is strictly blocked until the defect is resolved.

---

## 5. Zero-Unsolicited-Version Invariant (No Version Spam)
- Agents and swarm orchestrators must **NEVER mention, quote, or announce version numbers** in greetings, chat introductions, status banners, or conversational responses unless the user explicitly asks for the version.
- Version numbers belong exclusively in canonical machine manifests (`version.manifest.json`, `package.json`), CLI `--version` output, and release changelogs.
- Agent specification files, frontmatter descriptions, and prompt headers must never hardcode version numbers.
