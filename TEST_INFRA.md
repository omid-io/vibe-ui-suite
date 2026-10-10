# E2E Test Infra: vibe-ui-suite

## Test Philosophy
- Opaque-box, requirement-driven verification derived directly from `ORIGINAL_REQUEST.md`.
- Multi-tier testing methodology: Category-Partition, Boundary Value Analysis, Pairwise Combinations, Real-World Application Workloads, and Automated Acceptance Gates.

## Feature Inventory & Test Mapping
| # | Feature | Source (Requirement) | Tier 1 (Coverage) | Tier 2 (Boundaries) | Tier 3 (Interactions) |
|---|---------|---------------------|:-----------------:|:-------------------:|:---------------------:|
| 1 | Architecture & Docs (R1) | ORIGINAL_REQUEST §R1 | ARCHITECTURE.md completeness | Link resolution, format edge cases | Polish across locales |
| 2 | Mathematical WCAG Contrast (R2) | ORIGINAL_REQUEST §R2 | Relative luminance formula | Contrast limits (4.5:1, 3:1) | Multi-chemistry token contrast |
| 3 | Schema Negative Testing (R2) | ORIGINAL_REQUEST §R2 | Fixture validation | Boundary values (entropy, touch target) | Recursive nested object checks |
| 4 | Machine-Readable JSON (R2) | ORIGINAL_REQUEST §R2 | `--json` flag output format | Exit code 0 on pass, 1 on fail | CI stdout parsing |
| 5 | Next.js 15 Starter (R3) | ORIGINAL_REQUEST §R3 | Starter structure & compilation | TypeScript types & package.json syntax | AI primitives & semantic RTL |
| 6 | Version Pinning & Supply Chain (R4) | ORIGINAL_REQUEST §R4 | `-Version` parameter | Tag normalization, 404 handling | Archive extraction dynamics |

## Automated Verification Acceptance Criteria
1. `python evals/run_evals.py --json` exits with code 0 and emits valid JSON summary.
2. All negative schema test cases fail validation as expected (`invalid_archetype.json`, `out_of_range_entropy.json`, `touch_target_below_24px.json` each exit with code 1).
3. `examples/nextjs-starter/package.json` validates JSON syntax via `python -m json.tool` and `node -e "require('./examples/nextjs-starter/package.json')"`.
4. 100% of internal links in documentation resolve to valid files.

## Test Runner Invocation
- Full Suite: `python evals/run_evals.py --json`
- Fixture Runner: `python evals/run_evals.py --fixture <path>`
- Link Checker: Python stdlib link validation script
