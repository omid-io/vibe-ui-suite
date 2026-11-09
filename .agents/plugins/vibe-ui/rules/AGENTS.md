# 🎨 Vibe UI Suite — Workspace Directives & Architecture

> **Single Source of Truth for Frontend, UI/UX, and Web Design across the ecosystem.**

---

## 1. Core Architecture: Sovereign Foreman & Background Swarm
All UI design in this repository executes via `vibe-ui-agent` (Sovereign Swarm Foreman):
- **Single Point of Contact & Zero-Chat-Spam Invariant:** The host agent dispatches `vibe-ui-agent` via `invoke_subagent`. `vibe-ui-agent` executes the 5-phase swarm silently in the background (via `python vibe_cli.py swarm "<prompt>" --json`) without polluting the primary conversation with intermediate subagent turns.
- **The 5 Autonomous Stations:**
  1. **Phase 1 (Concept & Intent):** Macro Concept Manifest (Domain, Psychographics, Spatial Flow).
  2. **Phase 2 (Trend & Asset Mining):** GitHub >10k stars, Uiverse micro-interactions, and Living Media Shelf.
  3. **Phase 3 (Art Direction):** Binding Design Style Blueprint (OKLCH tokens, typography scales, hierarchy).
  4. **Phase 4 (Master Engineering Build):** Pristine single-author HTML/React markup with spring physics and zero seams.
  5. **Phase 5 (Adversarial Inspection Gate):** Harness-owned multi-viewport screenshots (390px / 768px / 1440px), WCAG AA contrast (>=4.5:1), and 0px overflow closed-loop healing (<=3 loops).
- **Consolidated Delivery:** `vibe-ui-agent` delivers the final verified artifact, screenshots, and audit metrics in a single consolidated presentation.

---

## 2. Spatial & Aesthetic Standards
- **Peak Creativity & Maximum Innovation Mandate:** All agents across the swarm (`vibe-concept-architect`, `vibe-trend-hunter`, `vibe-art-director`, `vibe-master-builder`, `vibe-visual-auditor`, `vibe-tech-auditor`) MUST ALWAYS operate with the highest level of creativity, boldness, and artistic depth. Generic, cookie-cutter, or repetitive boilerplate solutions are strictly forbidden. Every interface, spatial composition, visual rhythm, micro-interaction, and layout archetype must reflect tailored domain-specific elegance, bold aesthetic innovation, and elite craftsmanship.
- **Anti-Cosmetic-Patch Invariant:** Shallow skin patches (tweaking colors or emojis while leaving dead layouts untouched) are strictly forbidden. UI work mandates structural spatial overhaul, dual-theme support, and living browser screenshot verification.
- **Anti-Bento-Dogma Invariant:** Never dogmatically default to repetitive "Bento Grid" card boxes. Form follows function: employ asymmetric flows, single hero focal points, continuous timelines, or high-density operational tables.
- **Creative Synthesis Standard:** Never clone benchmark templates (Mobbin, Dribbble, Awwwards) verbatim. Synthesize core mechanics into bespoke interfaces authentic to the specific project domain.
- **Mandatory Light-First Canonical Standard:** The LIGHT THEME is ALWAYS the primary, default, and canonical design. All layouts, typography, shadows, micro-interactions, and contrast ratios MUST be designed, rendered, and visually audited in LIGHT THEME first. Palette: Pure crisp surfaces (`#ffffff`, `#f8fafc`), subtle slate borders (`#e2e8f0`), deep graphite typography (`#0f172a` / `#334155`), and vibrant, high-clarity brand accents.
- **Anti-Suffocating Rule (Absolute Prohibition of Flat Muddy Dark Themes):** NEVER generate flat, pitch-black (`#000000`, `#0a0a0a`) or muddy grey voids with dull low-contrast text. Dark theme is strictly a SECONDARY layer. When implemented, it must feel like a premium OLED cockpit:
  - Deep midnight blue/slate foundations (`#0b0f19`, `#0f172a`), NOT dirty charcoal.
  - Specular glass highlights (`box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.08)`), luminous neon badges, and crisp AA/AAA contrast ratios.
- **On-Demand RTL Protocol:** Root stays `dir="ltr"`. Persian text is scoped with Vazirmatn fallback, `<bdi>` token isolation, and non-mirrored coordinates per `RTL.md`.
---

## 3. Mandatory Multi-Registry Release Law ("Publish")
Whenever publishing or releasing this suite:
1. **Version Bump & Skill Sync:** Synchronize canonical semantic version across all manifests (`version.manifest.json`, `package.json` in root, packages, starter) and sync all skills from `skills/` to `.agents/skills/` and `packages/vibe-ui-suite/skills/`.
2. **Changelog & Readme Update:** Record changes in root `CHANGELOG.md` and `packages/vibe-ui-vscode/CHANGELOG.md`. Update `README.md` if features, tokens, or options changed.
3. **Mandatory Pre-Release Inspector Agent Audit (Regression & Compatibility Gate):** Before proceeding to deployment, always dispatch an independent Inspector/Auditor Agent (or run adversarial multi-file diff inspection) to audit all code changes. The inspector must verify that newly added features or modifications do not introduce regressions, break backwards compatibility, or create conflicts/inconsistencies with existing components, templates, CLI commands, tokens, or prior architectural standards.
4. **Build & Automated Quality Gates:** Run `python scripts/validate_versions.py`, `python evals/run_evals.py --json`, and Gitleaks scan (`E:\programming\Tools\gitleaks\gitleaks.exe`).
5. **NPM & Open-VSX Publishing:** Build `packages/vibe-ui-suite` and package `vibe-ui-vscode-*.vsix`. Commit, tag (`vX.Y.Z`), and push to GitHub to trigger automated publishing to **NPM** and **Open-VSX** via `.github/workflows/publish.yml`.
6. **Microsoft Visual Studio Marketplace Upload:** Upload the VSIX through the publisher dashboard at `https://marketplace.visualstudio.com/manage/publishers/omid-io` using browser capabilities exposed by the active harness, then verify marketplace status.

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
- Agent specification files, frontmatter descriptions, prompt headers, and README documentation must never hardcode version numbers (`README.md`, `README.fa.md`, and package READMEs remain strictly evergreen).
