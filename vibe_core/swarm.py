#!/usr/bin/env python3
"""
vibe_core/swarm.py — Master Foreman Multi-Agent Swarm Orchestrator
Vibe UI Suite

Coordinates the 5-phase sequential multi-agent pipeline:
1. Concept Architect (Intent expansion & macro domain definition)
2. Trend Hunter (High-star GitHub patterns & top Uiverse micro-interactions)
3. Art Director (Style blueprint, OKLCH tokens & typography hierarchy)
4. Master Builder (Single-author HTML/React synthesis)
5. Adversarial Inspection Swarm (Screenshot audit Desktop/Mobile + WCAG AA/Overflow verification)
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

ROOT_DIR = Path(__file__).resolve().parent.parent

from vibe_core.director import DesignDirector
from vibe_core.recommendation import RecommendationEngine
from vibe_core.generator import InterfaceGenerator
from vibe_core.critic import DesignCritic
from vibe_core.refiner import AutoRefiner
from vibe_core.verifier import VerificationEngine
from vibe_core.healer import SelfHealingLoop
from vibe_core.trend_hunter import TrendHunter

class ForemanSwarmOrchestrator:
    """Master orchestrator running the multi-agent pipeline deterministically."""

    def __init__(self, workspace_root: Optional[Path] = None):
        self.workspace_root = workspace_root or ROOT_DIR
        self.director = DesignDirector()
        self.recommendation = RecommendationEngine()
        self.generator = InterfaceGenerator()
        self.critic = DesignCritic()
        self.healer = SelfHealingLoop()
        self.verifier = VerificationEngine()
        self.trend_hunter = TrendHunter()

    def run_swarm(
        self,
        prompt: str,
        target_output: Optional[str] = None,
        style_override: Optional[str] = None,
        output_format: str = "html",
        max_remediation_loops: int = 3
    ) -> Dict[str, Any]:
        """
        Executes the full 5-station pipeline from raw user prompt to verified screenshots.
        """
        logs = []
        def log(station: str, message: str):
            entry = f"[{station}] {message}"
            logs.append(entry)
            print(entry)

        # -------------------------------------------------------------
        # Station 1: Concept Architect (Expansion & Psychographics)
        # -------------------------------------------------------------
        log("STATION 1 / Concept Architect", f"Expanding sparse prompt: '{prompt}'...")
        intent = self.director.infer_intent(prompt)
        domain = intent.get("product_domain", "general")
        confidence = intent.get("confidence", {}).get("overall", 0.9)
        log("STATION 1 / Concept Architect", f"Identified Domain: '{domain}' (Confidence: {confidence})")

        # -------------------------------------------------------------
        # Station 2: Dual Trend Hunter (GitHub Stars + Uiverse Likes)
        # -------------------------------------------------------------
        log("STATION 2 / Trend Hunter", f"Mining top-starred benchmarks and micro-interactions for '{domain}'...")
        trend_package = self.trend_hunter.curate_trend_package(domain, style_preference=style_override)
        top_benchmarks = [b["name"] for b in trend_package.get("top_starred_benchmarks", [])]
        log("STATION 2 / Trend Hunter", f"Anchored in elite benchmarks: {', '.join(top_benchmarks[:3])}")

        # -------------------------------------------------------------
        # Station 3: Art Director (Style Blueprint & OKLCH Tokens)
        # -------------------------------------------------------------
        log("STATION 3 / Art Director", "Synthesizing Design Style Blueprint & Dual-Theme Tokens...")
        decision = self.recommendation.recommend(intent, user_style_preference=style_override)
        selected_style = decision.get("selected_style", "Minimalist SaaS")
        typography = decision.get("genome", {}).get("typography", {}).get("display", "Inter")
        log("STATION 3 / Art Director", f"Selected Visual Chemistry: '{selected_style}' | Display: '{typography}'")

        # -------------------------------------------------------------
        # Station 4: Master Builder (Code Authoring)
        # -------------------------------------------------------------
        log("STATION 4 / Master Builder", f"Compiling single-author {output_format.upper()} code artifact...")
        out_path = Path(target_output).resolve() if target_output else (self.workspace_root / "examples" / f"swarm_output.{output_format}").resolve()
        out_path.parent.mkdir(parents=True, exist_ok=True)

        if output_format == "tsx":
            code = self.generator.generate_react_tsx(decision)
        else:
            code = self.generator.generate_html(decision, prompt_title=prompt)

        with open(out_path, "w", encoding="utf-8") as f:
            f.write(code)

        # -------------------------------------------------------------
        # Station 5: Adversarial Inspection & Closed-Loop Healing
        # -------------------------------------------------------------
        log("STATION 5 / Auditor Swarm", "Initiating adversarial inspection (Screenshots & WCAG AA)...")
        iteration = 1
        audit_passed = False
        punch_list = []

        while iteration <= max_remediation_loops:
            # 5A: Technical Verification (WCAG AA, 0px overflow)
            v_report = self.verifier.verify_html(code, out_path.name, mode="fast")
            failed_checks = v_report.get("checks_summary", {}).get("failed", 0)
            score = v_report.get("overall_status", "UNKNOWN")

            # 5B: Design Critic Evaluation
            c_report = self.critic.critique(code, decision, iteration=iteration)
            critic_status = c_report.get("acceptance_status", "PENDING")

            if failed_checks == 0 and critic_status == "ACCEPTED":
                log("STATION 5 / Auditor Swarm", f"Passed all technical & visual quality gates on iteration {iteration}!")
                audit_passed = True
                break

            log("STATION 5 / Auditor Swarm", f"Iteration {iteration}: {failed_checks} checks failed (Critic: {critic_status}). Triggering closed-loop healing...")
            code, c_report, correction_prompt = self.healer.heal(code, decision, original_prompt=prompt)
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(code)
            iteration += 1

        # 5C: Multi-Viewport Headless Screenshot Capture
        screenshot_results = self._capture_screenshots(out_path)

        # Final Delivery Packaging
        status = "PASS" if audit_passed else "ACCEPTABLE_WITH_NOTES"
        log("DELIVERY GATE", f"Pipeline completed with status [{status}]. Artifact ready at: {out_path.name}")

        return {
            "status": status,
            "prompt": prompt,
            "domain": domain,
            "style": selected_style,
            "artifact_path": str(out_path),
            "screenshots": screenshot_results,
            "iterations_count": iteration,
            "logs": logs
        }

    def _capture_screenshots(self, html_path: Path) -> Dict[str, str]:
        """Runs the isolated headless Chromium renderer to capture Desktop and Mobile screenshots."""
        audit_script = self.workspace_root / "scripts" / "screenshot_audit.py"
        out_screenshots_dir = self.workspace_root / ".test-artifacts" / "screenshots"
        out_screenshots_dir.mkdir(parents=True, exist_ok=True)

        if not audit_script.exists():
            return {}

        try:
            res = subprocess.run(
                [sys.executable, str(audit_script), str(html_path), "--json", "-o", str(out_screenshots_dir)],
                capture_output=True,
                text=True,
                timeout=30
            )
            if res.returncode == 0 and res.stdout.strip():
                try:
                    data = json.loads(res.stdout)
                    return data.get("saved_screenshots", {})
                except Exception:
                    pass
        except Exception as e:
            print(f"[WARN] Headless screenshot capture skipped: {e}", file=sys.stderr)

        stem = html_path.stem
        desktop_img = out_screenshots_dir / f"{stem}_desktop.png"
        mobile_img = out_screenshots_dir / f"{stem}_mobile.png"
        return {
            "desktop": str(desktop_img) if desktop_img.exists() else "",
            "mobile": str(mobile_img) if mobile_img.exists() else ""
        }
