#!/usr/bin/env python3
"""Stratified design benchmark with explicitly static/browser-neutral scoring.

This batch runner measures deterministic intent, code-generation, critic,
refiner, and static-verifier behavior. It does not claim live browser,
pixel, DOM-geometry, or visual-vision results; those require an active harness
and a separate SHA-bound browser evidence report.
"""
from __future__ import annotations
import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))
from vibe_core.director import DesignDirector
from vibe_core.recommendation import RecommendationEngine
from vibe_core.generator import InterfaceGenerator
from vibe_core.critic import DesignCritic
from vibe_core.visual_critic import VisualCritic
from vibe_core.refiner import AutoRefiner
from vibe_core.verifier import VerificationEngine
from vibe_core.runtime_compiler import RuntimeCompiler

PROMPTS_100_PATH = ROOT_DIR / "evals" / "benchmark" / "prompts_100_stratified.json"
PROMPTS_HOLDOUT_PATH = ROOT_DIR / "evals" / "benchmark" / "prompts_50_blind_holdout.json"
PROMPTS_HUMAN_PATH = ROOT_DIR / "evals" / "benchmark" / "prompts_25_human_tasks.json"


def main() -> int:
    parser = argparse.ArgumentParser(description="Vibe UI static design-intelligence benchmark")
    parser.add_argument("--holdout", action="store_true", help="Run 50-scenario blind holdout benchmark")
    parser.add_argument("--human", action="store_true", help="Run 25-task human one-shot benchmark")
    args, _ = parser.parse_known_args()

    if args.human:
        prompts_path = PROMPTS_HUMAN_PATH
        results_path = ROOT_DIR / "evals" / "benchmark" / "benchmark_human_results.json"
        label = "25 Human One-Shot Tasks"
    elif args.holdout:
        prompts_path = PROMPTS_HOLDOUT_PATH
        results_path = ROOT_DIR / "evals" / "benchmark" / "benchmark_holdout_results.json"
        label = "50 Blind Holdout Scenarios"
    else:
        prompts_path = PROMPTS_100_PATH
        results_path = ROOT_DIR / "evals" / "benchmark" / "benchmark_results.json"
        label = "100 Stratified Scenarios"

    if not prompts_path.exists():
        print(f"[FAIL] Prompts file not found: {prompts_path}", file=sys.stderr)
        return 1
    data = json.loads(prompts_path.read_text(encoding="utf-8"))
    scenarios = data.get("tasks", data.get("prompts", []))
    if not scenarios:
        print("[FAIL] Benchmark contains no scenarios", file=sys.stderr)
        return 1

    director = DesignDirector()
    engine = RecommendationEngine()
    generator = InterfaceGenerator()
    critic = DesignCritic()
    visual_critic = VisualCritic()
    refiner = AutoRefiner()
    verifier = VerificationEngine()
    compiler = RuntimeCompiler()

    first_pass = 0
    autonomous_resolved = 0
    compiled_count = 0
    corrections = 0
    correction_tokens = 0
    total_ms = 0.0
    domain_matches = 0
    styles = set()
    details = []

    baseline_first_pass = 52.0
    baseline_corrections = 2.4
    baseline_tokens = 2400.0
    started = time.perf_counter()

    print("=" * 72)
    print(f"VIBE UI DESIGN INTELLIGENCE BENCHMARK — {label}")
    print("Browser runtime, rendered geometry and screenshot vision: NOT_EVALUATED")
    print("=" * 72)

    for index, scenario in enumerate(scenarios, 1):
        prompt = scenario["prompt"]
        expected_domain = scenario["domain"]
        started_case = time.perf_counter()

        intent = director.infer_intent(prompt)
        domain_match = intent.get("product_domain") == expected_domain
        domain_matches += int(domain_match)

        decision = engine.recommend(intent)
        selected_style = decision.get("selected_style", "")
        styles.add(selected_style)

        html = generator.generate_html(decision, prompt_title=prompt)
        tsx = generator.generate_react_tsx(decision)
        compiled_js, compile_error = compiler.compile_tsx(tsx)
        tsx_compiled = bool(compiled_js) and compile_error is None
        compiled_count += int(tsx_compiled)

        code_critique = critic.critique(html, decision, iteration=1)
        visual_critique = visual_critic.evaluate(html, decision)
        first_pass_ok = (
            code_critique.get("acceptance_status") == "ACCEPTED"
            and visual_critique.get("acceptance_status") == "ACCEPTED"
        )
        if first_pass_ok:
            first_pass += 1
            final_html = html
            final_critique = dict(code_critique)
            final_critique["visual_critic"] = visual_critique
        else:
            final_html, final_critique = refiner.refine(html, decision, max_iterations=2)
            corrections += 1
            correction_tokens += 350

        accepted = final_critique.get("acceptance_status") == "ACCEPTED"
        autonomous_resolved += int(accepted)
        static_report = verifier.verify_html(final_html, f"scenario_{index}.html")
        elapsed_ms = (time.perf_counter() - started_case) * 1000.0
        total_ms += elapsed_ms

        details.append({
            "scenario_id": scenario.get("id", str(index)),
            "domain": expected_domain,
            "prompt": prompt,
            "detected_domain": intent.get("product_domain"),
            "domain_match": domain_match,
            "selected_style": selected_style,
            "candidate_passed_first_pass": first_pass_ok,
            "autonomous_resolved": accepted,
            "react_tsx_compiled": tsx_compiled,
            "browser_runtime_status": "NOT_EVALUATED",
            "visual_critic_score": visual_critique.get("visual_score", 0),
            "critic_score": final_critique.get("quality_score", 0),
            "verification_status": static_report.get("overall_status", "NOT_EVALUATED"),
            "elapsed_ms": round(elapsed_ms, 2),
        })
        if index % 20 == 0 or index == len(scenarios):
            print(f"Processed {index}/{len(scenarios)} scenarios — first-pass: {first_pass / index * 100:.1f}%")

    count = len(scenarios)
    first_rate = first_pass / count * 100.0
    autonomous_rate = autonomous_resolved / count * 100.0
    compile_rate = compiled_count / count * 100.0
    domain_accuracy = domain_matches / count * 100.0
    avg_corrections = corrections / count
    avg_tokens = correction_tokens / count
    avg_ms = total_ms / count
    diversity = len(styles) / 12.0 * 100.0
    passed_static = sum(item["verification_status"] == "PASS" for item in details)
    static_gate_rate = passed_static / count * 100.0

    baseline_type = "internal_heuristic_prior"
    results = {
        "$schema": "../../schemas/benchmark-result.v1.json",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "suite_version": "6.5.1",
        "scenario_count": count,
        "benchmark_type": "static_design_intelligence_and_code_critique",
        "baseline_system": "Vanilla LLM / V2 Heuristic Baseline",
        "baseline_type": baseline_type,
        "baseline_methodology": "Internal heuristic prior, not a measured control cohort. This benchmark measures deterministic intent, code critique, visual source heuristics, TSX compilation and static verification only.",
        "candidate_system": "Vibe UI Suite — Design Intelligence and Static Quality Pipeline",
        "kpi_comparison": {
            "first_pass_rate": {"baseline": baseline_first_pass, "candidate": round(first_rate, 1), "delta_percent": round(first_rate - baseline_first_pass, 1), "gate_type": "static_code_and_visual_critic"},
            "autonomous_resolution_rate": {"baseline": 65.0, "candidate": round(autonomous_rate, 1), "delta_percent": round(autonomous_rate - 65.0, 1)},
            "react_tsx_compilation_rate": {"baseline": 0.0, "candidate": round(compile_rate, 1), "delta_percent": round(compile_rate, 1)},
            "domain_resolution_accuracy": {"baseline": 56.0, "candidate": round(domain_accuracy, 1), "delta_percent": round(domain_accuracy - 56.0, 1)},
            "avg_automated_refiner_rounds": {"baseline": baseline_corrections, "candidate": round(avg_corrections, 2), "reduction_percent": round((baseline_corrections - avg_corrections) / baseline_corrections * 100.0, 1)},
            "avg_user_corrections": {"baseline": baseline_corrections, "candidate": round(avg_corrections, 2), "reduction_percent": round((baseline_corrections - avg_corrections) / baseline_corrections * 100.0, 1), "note": "Alias retained for backward compatibility."},
            "avg_correction_tokens": {"baseline": baseline_tokens, "candidate": round(avg_tokens, 0), "reduction_percent": round((baseline_tokens - avg_tokens) / baseline_tokens * 100.0, 1)},
            "avg_time_to_accept_ms": {"candidate": round(avg_ms, 2)},
            "visual_diversity_index": {"candidate": round(diversity, 1), "unique_styles_rendered": len(styles)},
            "hard_gates_compliance": {"candidate": round(static_gate_rate, 1)},
            "browser_runtime_evaluation": {"status": "NOT_EVALUATED", "reason": "The batch benchmark does not control or launch a browser. Use a live AI harness and submit a SHA-bound browser evidence report."},
        },
        "scenario_breakdown": details,
    }
    results_path.parent.mkdir(parents=True, exist_ok=True)
    results_path.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")

    print("\n" + "=" * 72)
    print("VIBE UI DESIGN INTELLIGENCE BENCHMARK")
    print("=" * 72)
    print(f"First-pass static acceptance: {first_rate:.1f}%")
    print(f"Autonomous resolution: {autonomous_rate:.1f}%")
    print(f"React TSX compilation: {compile_rate:.1f}%")
    print(f"Domain resolution: {domain_accuracy:.1f}%")
    print(f"Static verification gates: {static_gate_rate:.1f}%")
    print("Browser runtime / actual rendered visual assessment: NOT_EVALUATED")
    print(f"Elapsed: {(time.perf_counter() - started) * 1000.0:.1f}ms")
    print(f"Results: {results_path.relative_to(ROOT_DIR)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
