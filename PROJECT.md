# Project: Vibe UI Suite (Deep Architectural Hardening)

## Architecture
The `vibe-ui-suite` (Vibe UI Suite) repository is an autonomous AI agent UI design system. Master orchestrator `vibe-ui-agent` commands 6 specialized sub-skills and a unified Python design core (`vibe_core`):
1. `autonomous-intent-expander` & `vibe_core/director.py`: Ingests user prompt, evaluates intent, selects domain archetype and visual chemistry.
2. `vibe_core/generator.py`: Emits contract-declared semantic HTML adhering to design tokens.
3. `vibe_core/critic.py`: Evaluates HTML designs across 9 scorecard dimensions (100-point scale) and enforces binary hard-gate invariants.
4. `vibe_core/refiner.py`: Iteratively repairs critic defects, balances DOM tags, and enforces anti-regression hard-gate monotonic progression.
5. `vibe_core/verifier.py`: 5-pillar autonomous quality gate certifying WCAG AA contrast, compositing blur budget, and semantic RTL.
6. `evals/run_evals.py` & `evals/benchmark/`: Mathematical luminance validation, negative schema tests, browser runtime audits, and empirical benchmark suites.

## Feature Inventory
| # | Feature | Description | Milestone | Source |
|---|---------|-------------|-----------|--------|
| 1 | AutoRefiner HTML Tag-Pair Balancing | Implement pure-Python stdlib stack-based token scanner in `vibe_core/refiner.py` to balance `<button type="button">...</button>` replacing `<div onclick>`, handling attributes with `>` and nested children. | M1 | ORIGINAL_REQUEST §R1 |
| 2 | Hard-Gate Anti-Regression Decision Engine | Upgrade `vibe_core/refiner.py` with 5-Rule Invariant Gate (Gate Monotonicity, Tag Balance Invariant, Mobile Overflow Invariant) immediately rejecting any patch that regresses hard gates. | M1 | ORIGINAL_REQUEST §R1 |
| 3 | Refiner Unit Test Suite Expansion | Expand `scripts/test_critic_refiner.py` with 8 edge-case tests asserting tag balancing, nested divs, javascript attributes, and hard-gate regression rejection. | M1 | Survey 1 |
| 4 | Dynamic Measurement-Based Critic | Replace static hardcoded points (`domain_fit = 14`, `brand_coherence = 9`, flat toggles) in `vibe_core/critic.py` with dynamic computed measurements (tokens, color variance, typography hierarchy, contrast). | M2 | ORIGINAL_REQUEST §R2 |
| 5 | Blur Threshold Harmonization (`MAX_BLUR_SURFACES = 3`) | Unify blur budget to constant `MAX_BLUR_SURFACES = 3` across `vibe_core/critic.py`, `vibe_core/verifier.py`, `evals/run_evals.py`, `ARCHITECTURE.md`, and `data/anti-patterns.json`. | M2 | ORIGINAL_REQUEST §R2 |
| 6 | Touch Target Policy Standardization | Codify dual-tier touch target constants `HARD_MIN_TOUCH = 24` (WCAG AA) and `RECOMMENDED_TOUCH = 44` (HIG) across `critic.py`, `verifier.py`, and `run_evals.py`. | M2 | ORIGINAL_REQUEST §R2 |
| 7 | Transparent Benchmark Metadata & Schemas | Add `baseline_type: "estimated_prior_study"` and detailed methodological notes to `evals/benchmark/run_benchmark.py` and `schemas/benchmark-result.v1.json`, harmonizing property names. | M3 | ORIGINAL_REQUEST §R3 |
| 8 | Ecosystem Version Synchronization (v3.0.0) | Synchronize version to `3.0.0` across 18 files with alpha drift (`data/styles.json`, all `data/*.json`, `vibe_core/__init__.py`, `install.ps1`, `install.sh`, `schemas/design-spec.v1.schema.json`). | M3 | ORIGINAL_REQUEST §R3 |
| 9 | Version Validation Script Hardening | Update `scripts/validate_versions.py` to assert version synchronization across all 18 data and installer files. | M3 | Survey 3 |
| 10 | Multi-Agent Zero-Regression Verification | Verify all 7 test suites pass 100% in `python scripts/run_all_tests.py`, verify Next.js 15 TypeScript build, verify Playwright headless browser runtime, and run forensic audit. | M4 | ORIGINAL_REQUEST §R4 |

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| M1 | AutoRefiner HTML Repair & Hard-Gate Anti-Regression | `vibe_core/refiner.py`, `scripts/test_critic_refiner.py` | Survey completed | IN_PROGRESS |
| M2 | Measurement-Based Critic & Threshold Harmonization | `vibe_core/critic.py`, `vibe_core/verifier.py`, `evals/run_evals.py`, `ARCHITECTURE.md`, `data/anti-patterns.json` | M1 | PLANNED |
| M3 | Transparent Benchmark Metadata & Version Sync | `evals/benchmark/run_benchmark.py`, `schemas/benchmark-result.v1.json`, `data/styles.json`, `data/*.json`, `scripts/validate_versions.py` | M1, M2 | PLANNED |
| M4 | Multi-Agent Verification & Zero-Regression Proof | All 7 test suites via `scripts/run_all_tests.py`, Next.js 15 starter compilation, Playwright runtime checks, forensic integrity audit | M1, M2, M3 | PLANNED |

## Interface Contracts
### AutoRefiner ↔ DesignCritic
- Input: `html_content: str`, `decision: dict`
- Output: `(refined_html: str, final_report: dict)`
- Invariant: Every repair patch must satisfy:
  1. `len(new_failures - curr_failures) == 0 and len(new_failures) <= len(curr_failures)`
  2. `open_buttons == close_buttons`
  3. No mobile overflow blowout classes
  4. `re_critique["quality_score"] >= current_report["quality_score"]`

### DesignCritic Dynamic Scorecard Contract
- Input: `html_content: str`, `decision: dict`, `iteration: int`
- Output conformant with `schemas/critic-report.v1.json`:
  - `visual_hierarchy`: [0, 15]
  - `anti_slop_distinctiveness`: [0, 15]
  - `domain_fit`: [0, 15]
  - `usability`: [0, 10]
  - `typography`: [0, 10]
  - `responsive`: [0, 10]
  - `state_completeness`: [0, 10]
  - `brand_coherence`: [0, 10]
  - `performance_budget`: [0, 5]
- Sum of scorecard = `quality_score` in [0, 100].

### Ecosystem Constants Contract
- `MAX_BLUR_SURFACES = 3`
- `HARD_MIN_TOUCH = 24`
- `RECOMMENDED_TOUCH = 44`

## Code Layout
- `vibe_core/refiner.py` — AutoRefiner HTML repair & anti-regression gate
- `vibe_core/critic.py` — DesignCritic measurement-based scoring engine
- `vibe_core/verifier.py` — 5-pillar autonomous quality gate
- `evals/run_evals.py` — Mathematical evaluation suite & Playwright browser audits
- `evals/benchmark/run_benchmark.py` — Benchmark execution & KPI comparisons
- `schemas/benchmark-result.v1.json` — JSON schema for benchmark result objects
- `schemas/design-spec.v1.schema.json` — Design specification schema
- `data/styles.json` & `data/*.json` — 26 orthogonal style families & design tokens
- `scripts/test_critic_refiner.py` — Unit tests for critic & refiner
- `scripts/validate_versions.py` — Global version synchronization validator
- `scripts/run_all_tests.py` — Master test runner for all 7 test suites
