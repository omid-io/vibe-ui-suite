#!/usr/bin/env python3
"""
run_all_tests.py — Vibe UI Master Quality Gates & Regression Suite
Runs full end-to-end audit: Versions, Schemas, Knowledge Base, Search, Critic, Benchmark, and Evals.
"""

import sys
import subprocess
import time
from pathlib import Path

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent.parent

TEST_SUITES = [
    ("Version Synchronization", ["python", "scripts/validate_versions.py"]),
    ("Schema Validation (8 Schemas)", ["python", "scripts/validate_schemas.py"]),
    ("Knowledge Base Validation (15 Datasets)", ["python", "scripts/validate_data.py"]),
    ("Search & Recommendation Unit Tests", ["python", "scripts/test_search.py"]),
    ("Design Critic & AutoRefiner Unit Tests", ["python", "scripts/test_critic_refiner.py"]),
    ("Visual Critic Multi-Dimensional Tests", ["python", "scripts/test_visual_critic.py"]),
    ("24-Domain Canonical Widget & Causal Model Suite", ["python", "scripts/test_domain_registry.py"]),
    ("Asset Director 24-Domain Alignment Suite", ["python", "scripts/test_asset_director.py"]),
    ("Headless Physical Viewport Critic Suite", ["python", "scripts/test_physical_critic.py"]),
    ("In-Browser Pixel Buffer Critic Unit Tests", ["python", "scripts/test_pixel_critic.py"]),
    ("Full Pipeline Integration Tests (E2E)", ["python", "scripts/test_pipeline_e2e.py"]),
    ("Vibe UI Feature Verification", ["python", "scripts/test_v32_features.py"]),
    ("Stratified 100-Scenario Benchmark", ["python", "evals/benchmark/run_benchmark.py"]),
    ("Blind Holdout 50-Scenario Benchmark", ["python", "evals/benchmark/run_benchmark.py", "--holdout"]),
    ("Physical Runtime Evals (WCAG AA & DOM)", ["python", "evals/run_evals.py", "--json"])
]

def main():
    print("=" * 70)
    print("🛡️  VIBE UI V3 PRODUCTION VALIDATION & QUALITY GATES")
    print("=" * 70)

    overall_failures = []
    start_total = time.perf_counter()

    for name, cmd in TEST_SUITES:
        print(f"\n[RUNNING] {name}...")
        t0 = time.perf_counter()
        res = subprocess.run(cmd, cwd=ROOT_DIR, capture_output=True, text=True, encoding="utf-8")
        elapsed = (time.perf_counter() - t0) * 1000.0

        if res.returncode == 0:
            print(f"  [PASS] {name} ({elapsed:.1f}ms)")
        else:
            print(f"  [FAIL] {name} exited with code {res.returncode}")
            print(res.stderr or res.stdout)
            overall_failures.append(name)

    total_time_ms = (time.perf_counter() - start_total) * 1000.0
    print("\n" + "=" * 70)
    if overall_failures:
        print(f"❌ QUALITY GATES FAILED ({len(overall_failures)} failure(s)):")
        for f in overall_failures:
            print(f"  - {f}")
        return 1
    else:
        print(f"✅ ALL QUALITY GATES PASSED (Total time: {total_time_ms:.1f}ms)")
        print(f"   - 100% of {len(TEST_SUITES)} test suites clean")
        print("   - Zero regression blockers detected")
        print("=" * 70)
        return 0

if __name__ == "__main__":
    sys.exit(main())
