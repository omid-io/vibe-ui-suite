#!/usr/bin/env python3
"""
vibe_cli.py — Vibe UI V3 Master Unified CLI & Orchestrator
Production-grade interface connecting Design Director, Recommendation, Genome, Critic, Refiner & Verifier.
"""

import sys
import json
import argparse
from pathlib import Path

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT_DIR))

from vibe_core.director import DesignDirector
from vibe_core.recommendation import RecommendationEngine
from vibe_core.generator import InterfaceGenerator
from vibe_core.critic import DesignCritic
from vibe_core.refiner import AutoRefiner
from vibe_core.verifier import VerificationEngine
from vibe_core.healer import SelfHealingLoop

def cmd_search(args):
    director = DesignDirector()
    engine = RecommendationEngine()
    intent = director.infer_intent(args.query)
    decision = engine.recommend(intent, user_style_preference=args.style)
    brief = {
        "query": args.query,
        "domain": intent["product_domain"],
        "confidence": intent["confidence"]["overall"],
        "style": decision["selected_style"],
        "score": decision["composite_score"],
        "typography": decision["genome"]["typography"],
        "color": decision["genome"]["color"]
    }
    print(json.dumps(brief, indent=2, ensure_ascii=False))

def cmd_plan(args):
    director = DesignDirector()
    engine = RecommendationEngine()
    intent = director.infer_intent(args.query)
    decision = engine.recommend(intent, user_style_preference=args.style)
    print(json.dumps(decision, indent=2, ensure_ascii=False))

def cmd_generate(args):
    director = DesignDirector()
    engine = RecommendationEngine()
    generator = InterfaceGenerator()
    critic = DesignCritic()
    healer = SelfHealingLoop()
    verifier = VerificationEngine()

    print(f"[1/5] Extracting Intent & Directing: '{args.query}'...")
    intent = director.infer_intent(args.query)
    print(f"      Domain: {intent['product_domain']} (Confidence: {intent['confidence']['overall']})")

    print("[2/5] Synthesizing Decision & Genome...")
    decision = engine.recommend(intent, user_style_preference=args.style)
    print(f"      Style: {decision['selected_style']} (Score: {decision['composite_score']})")

    out_format = getattr(args, "format", None)
    if not out_format:
        if args.output and (args.output.endswith(".tsx") or args.output.endswith(".jsx")):
            out_format = "tsx"
        else:
            out_format = "html"

    if out_format == "tsx":
        print("[3/5] Generating React 19 Living TSX Interface Artifact...")
        tsx = generator.generate_react_tsx(decision)
        out_path = Path(args.output).resolve() if args.output else (ROOT_DIR / "examples" / "GeneratedMasterpiece.tsx").resolve()
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(tsx)
        try:
            display_path = out_path.relative_to(ROOT_DIR)
        except ValueError:
            display_path = out_path
        print(f"\n[SUCCESS] Completed React 19 TSX pipeline. Artifact saved to: {display_path}")
        return

    print("[3/5] Generating Initial Interface Artifact...")
    html = generator.generate_html(decision, prompt_title=args.query)

    print("[4/5] Evaluating with Independent Design Critic...")
    critique = critic.critique(html, decision, iteration=1)
    print(f"      Critic Score: {critique['quality_score']}/100 (Status: {critique['acceptance_status']})")

    if critique["acceptance_status"] != "ACCEPTED":
        print("[4.5] Running Self-Healing Loop (static patch + correction prompt)...")
        html, critique, correction_prompt = healer.heal(html, decision, original_prompt=args.query)
        print(healer.format_heal_summary(critique, correction_prompt))
        if correction_prompt:
            print("\n[CORRECTION PROMPT — feed back to AI agent if needed]")
            print("─" * 60)
            print(correction_prompt)
            print("─" * 60 + "\n")

    verify_mode = "strict" if getattr(args, "strict", False) else "fast"
    mode_label = "Runtime Playwright" if verify_mode == "strict" else "Static Fast-Path"
    print(f"[5/5] Executing Verification 2.0 ({mode_label})...")
    verification = verifier.verify_html(html, args.output or "output.html", mode=verify_mode)
    print(f"      Verification: {verification['overall_status']} ({verification['checks_summary']['passed']}/{verification['checks_summary']['total']} checks passed)")

    out_path = Path(args.output).resolve() if args.output else (ROOT_DIR / "examples" / "generated_output.html").resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)

    try:
        display_path = out_path.relative_to(ROOT_DIR)
    except ValueError:
        display_path = out_path

    print(f"\n[SUCCESS] Completed autonomous pipeline. Artifact saved to: {display_path}")

def cmd_critique(args):
    path = Path(args.file)
    if not path.exists():
        print(f"[FAIL] File not found: {args.file}", file=sys.stderr)
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    critic = DesignCritic()
    report = critic.critique(content)
    print(json.dumps(report, indent=2, ensure_ascii=False))

def cmd_verify(args):
    path = Path(args.file)
    if not path.exists():
        print(f"[FAIL] File not found: {args.file}", file=sys.stderr)
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    mode = "strict" if getattr(args, "strict", False) else "fast"
    verifier = VerificationEngine()
    report = verifier.verify_html(content, path.name, mode=mode)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    if report["overall_status"] == "FAIL":
        sys.exit(1)


def cmd_heal(args):
    """Runs Self-Healing Loop on an existing HTML file and prints the correction prompt."""
    path = Path(args.file)
    if not path.exists():
        print(f"[FAIL] File not found: {args.file}", file=sys.stderr)
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    healer = SelfHealingLoop()
    final_html, final_report, correction_prompt = healer.heal(
        content, original_prompt=args.prompt or path.stem
    )
    print(healer.format_heal_summary(final_report, correction_prompt))

    if correction_prompt:
        print("\n[CORRECTION PROMPT]")
        print("─" * 60)
        print(correction_prompt)
        print("─" * 60)
        sys.exit(2)  # Exit code 2 = correction needed (not fatal error)
    else:
        print("[ACCEPTED] No correction prompt needed.")
        if args.output:
            out = Path(args.output)
            out.write_text(final_html, encoding="utf-8")
            print(f"[SAVED] Healed artifact: {args.output}")

def main():
    parser = argparse.ArgumentParser(description="Vibe UI Master CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # search
    p_search = subparsers.add_parser("search", help="Search Knowledge Base (<10ms)")
    p_search.add_argument("query", help="Prompt or query")
    p_search.add_argument("-s", "--style", help="Style override")

    # plan
    p_plan = subparsers.add_parser("plan", help="Synthesize DesignDecisionContract")
    p_plan.add_argument("query", help="Prompt or query")
    p_plan.add_argument("-s", "--style", help="Style override")

    # generate
    p_gen = subparsers.add_parser("generate", help="Run full autonomous generation pipeline")
    p_gen.add_argument("query", help="Prompt or query")
    p_gen.add_argument("-o", "--output", help="Output file path (.html or .tsx)")
    p_gen.add_argument("-f", "--format", choices=["html", "tsx"], default=None, help="Output format: 'html' (default) or 'tsx' (React 19 component)")
    p_gen.add_argument("-s", "--style", help="Style override")
    p_gen.add_argument("--strict", action="store_true", help="Run Playwright runtime verification after generation")

    # critique
    p_crit = subparsers.add_parser("critique", help="Run independent Design Critic on HTML file")
    p_crit.add_argument("file", help="Path to HTML file")

    # verify
    p_ver = subparsers.add_parser("verify", help="Run Verification 2.0 evidence checks on HTML file")
    p_ver.add_argument("file", help="Path to HTML file")
    p_ver.add_argument("--strict", action="store_true", help="Add Playwright headless DOM runtime assertions")

    # heal
    p_heal = subparsers.add_parser("heal", help="Run Self-Healing Loop on an existing HTML artifact")
    p_heal.add_argument("file", help="Path to HTML file to heal")
    p_heal.add_argument("-p", "--prompt", help="Original design prompt for context in correction output")
    p_heal.add_argument("-o", "--output", help="Save healed HTML to this path (if ACCEPTED)")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == "search":
        cmd_search(args)
    elif args.command == "plan":
        cmd_plan(args)
    elif args.command == "generate":
        cmd_generate(args)
    elif args.command == "critique":
        cmd_critique(args)
    elif args.command == "verify":
        cmd_verify(args)
    elif args.command == "heal":
        cmd_heal(args)

if __name__ == "__main__":
    main()
