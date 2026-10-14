#!/usr/bin/env python3
"""
vibe_cli.py — Vibe UI Suite v6.1.0 Master Unified CLI & Orchestrator
Production-grade interface connecting Design Director, Recommendation, Genome, Critic, Refiner, Verifier & Visual Auditor.
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
from vibe_core.galaxy_engine import GalaxyEngine

def cmd_inspire(args):
    """Searches or extracts components from the offline Galaxy repository (3000+ items)."""
    engine = GalaxyEngine()
    if not engine.ensure_galaxy_dataset():
        print("[FAIL] Could not access or clone Galaxy repository. Please verify network or clone manually.", file=sys.stderr)
        sys.exit(1)

    extract_target = getattr(args, "extract", None)
    if extract_target:
        comp = engine.get_component(extract_target)
        if not comp:
            print(f"[FAIL] Component not found: {extract_target}", file=sys.stderr)
            sys.exit(1)
        if getattr(args, "json", False):
            print(json.dumps(comp, indent=2, ensure_ascii=False))
        else:
            print(f"\n✨ Component: {comp['title']} [{comp['category']}]")
            print(f"Tags: {', '.join(comp['tags'])}")
            print(f"File: {comp['relative_path']}")
            print("-" * 60)
            print("<!-- HTML Structure -->")
            print(comp["html"])
            print("-" * 60)
            print("/* CSS Styles */")
            print(comp["css"][:500] + ("\n... [truncated]" if len(comp["css"]) > 500 else ""))
            print("-" * 60)
        return

    query = args.query or ""
    results = engine.search(query, category=getattr(args, "category", None), limit=getattr(args, "limit", 5))

    if getattr(args, "json", False):
        print(json.dumps(results, indent=2, ensure_ascii=False))
        return

    if not results:
        print(f"No Galaxy components found matching query: '{query}'")
        return

    print(f"\n🌌 Uiverse Galaxy Inspiration ({len(results)} matches for '{query}'):")
    print(f"   Indexed: {len(engine._index)} components | Search Latency: {results[0].get('search_time_ms', 0)} ms\n")
    for idx, r in enumerate(results, 1):
        print(f" [{idx}] {r['title']} ({r['category']})")
        print(f"     Tags: {', '.join(r['tags'])}")
        print(f"     Path: data/uiverse-galaxy/{r['relative_path']}")
        print(f"     Extract command: python vibe_cli.py inspire --extract \"{r['relative_path']}\"\n")


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

def cmd_screenshot(args):
    """Executes multi-viewport headless screenshot audit on an HTML/TSX artifact."""
    from scripts.screenshot_audit import capture_audit_screenshots

    file_path = Path(args.file)
    if not file_path.exists():
        print(f"[FAIL] Target file not found: {args.file}", file=sys.stderr)
        sys.exit(1)

    out_dir = getattr(args, "output_dir", None) or getattr(args, "output", ".test-artifacts/screenshots")
    viewports = getattr(args, "viewports", "desktop,mobile")
    full_page = getattr(args, "full_page", True)
    if getattr(args, "no_full_page", False):
        full_page = False

    try:
        report = capture_audit_screenshots(
            file_path=file_path,
            output_dir=out_dir,
            viewports=viewports,
            full_page=full_page,
        )
        if getattr(args, "json", False):
            print(json.dumps(report, indent=2, ensure_ascii=False))
        else:
            rendered_target = report.get("rendered_file", str(file_path))
            print(f"[SUCCESS] Multi-viewport screenshots captured for: {rendered_target}")
            for item in report.get("viewports_captured", []):
                rel_path = Path(item["path"]).name
                size_kb = item["bytes"] / 1024
                print(f"  * {item['viewport'].upper()} ({item['width']}px): {rel_path} ({size_kb:.1f} KB, Status: {item['status']})")
            print(f"\nOverall Status: {report['overall_status']}")
    except Exception as e:
        print(f"[FAIL] Screenshot capture failed: {e}", file=sys.stderr)
        sys.exit(1)

    if report.get("overall_status") == "FAIL":
        sys.exit(1)

def cmd_assets(args):
    from scripts.cache_assets import cache_all_assets, verify_assets, DEFAULT_OUTPUT_DIR
    action = getattr(args, "action", "verify")
    out_dir = Path(getattr(args, "output_dir", None) or str(DEFAULT_OUTPUT_DIR))
    if action == "download":
        success = cache_all_assets(output_dir=out_dir, force=getattr(args, "force", False), quality=getattr(args, "quality", 80))
    elif action == "verify":
        success = verify_assets(output_dir=out_dir)
    else:
        print(f"Unknown action: {action}", file=sys.stderr)
        sys.exit(1)
    if not success:
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Vibe UI Suite v6.1.0 Master CLI")
    parser.add_argument("--version", action="version", version="Vibe UI Suite v6.1.0")
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

    # screenshot
    p_ss = subparsers.add_parser("screenshot", help="Capture multi-viewport screenshots (Desktop 1440px, Mobile 390px) via Playwright")
    p_ss.add_argument("file", help="Path to target HTML or TSX file to render")
    p_ss.add_argument("-o", "--output", "--output-dir", dest="output", default=".test-artifacts/screenshots", help="Directory for saved screenshots (default: .test-artifacts/screenshots)")
    p_ss.add_argument("--viewports", default="desktop,mobile", help="Comma-separated viewports: 'desktop', 'mobile' (default: desktop,mobile)")
    p_ss.add_argument("--no-full-page", dest="full_page", action="store_false", default=True, help="Capture only initial viewport area instead of full page")
    p_ss.add_argument("--json", action="store_true", default=False, help="Output audit report as JSON")

    # assets
    p_assets = subparsers.add_parser("assets", help="Manage curated WebP assets (download, verify)")
    p_assets.add_argument("action", choices=["download", "verify"], default="verify", nargs="?", help="Action: 'download' or 'verify'")
    p_assets.add_argument("--force", action="store_true", help="Force re-download of existing assets")
    p_assets.add_argument("--quality", type=int, default=80, help="WebP compression quality (default: 80)")
    p_assets.add_argument("--output-dir", default=None, help="Output directory for assets")

    # inspire (Galaxy offline repository search)
    p_inspire = subparsers.add_parser("inspire", help="Offline search across 3000+ Uiverse Galaxy micro-interactions (<10ms)")
    p_inspire.add_argument("query", nargs="?", default="", help="Search query (e.g. 'neon button', 'loader', 'cyberpunk')")
    p_inspire.add_argument("-c", "--category", help="Category filter (Buttons, Cards, loaders, Inputs, Toggle-switches, etc.)")
    p_inspire.add_argument("-l", "--limit", type=int, default=5, help="Number of results to return (default: 5)")
    p_inspire.add_argument("-e", "--extract", help="Component relative path or name to extract raw HTML/CSS")
    p_inspire.add_argument("--json", action="store_true", help="Output results strictly as JSON")

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
    elif args.command == "screenshot":
        cmd_screenshot(args)
    elif args.command == "assets":
        cmd_assets(args)
    elif args.command == "inspire":
        cmd_inspire(args)

if __name__ == "__main__":
    main()

