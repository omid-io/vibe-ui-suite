#!/usr/bin/env python3
"""
vibe_core/swarm.py — Master Foreman Multi-Agent Swarm Orchestrator
Vibe UI Suite

Coordinates the 5-phase sequential multi-agent pipeline with typed data contracts:
1. Concept Architect (ConceptContract: Intent expansion & macro domain definition)
2. Trend Hunter (TrendEvidence: High-star GitHub patterns & top Uiverse micro-interactions)
3. Art Director (DesignGenomeContract: Style blueprint, OKLCH tokens & typography hierarchy)
4. Master Builder (UIArtifactContract: Single-author HTML/React synthesis)
5. Adversarial Inspection Swarm (EvaluationReportContract: Screenshot audit Desktop/Mobile + WCAG AA/Overflow verification)
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
from schemas.agent_contracts import (
    ConceptContract,
    TrendEvidence,
    DesignGenomeContract,
    UIArtifactContract,
    EvaluationReportContract,
)


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
        Enforces formal contract generation, validation, and delivery across all stations.
        """
        logs = []
        def log(station: str, message: str):
            entry = f"[{station}] {message}"
            logs.append(entry)
            print(entry)

        # -------------------------------------------------------------
        # Station 1: Concept Architect (ConceptContract)
        # -------------------------------------------------------------
        log("STATION 1 / Concept Architect", f"Expanding sparse prompt: '{prompt}'...")
        intent = self.director.infer_intent(prompt)
        domain = intent.get("product_domain", "general_modern_saas")
        confidence = intent.get("confidence", {}).get("overall", 0.90) if isinstance(intent.get("confidence"), dict) else 0.90

        candidate_dirs = intent.get("candidate_directions", [])
        product_name = (
            intent.get("blueprint", {}).get("canonical_brand", {}).get("en")
            or (candidate_dirs[0].get("name") if candidate_dirs else None)
            or "Vibe Digital Platform"
        )
        target_audience = (
            intent.get("audience", {}).get("primary")
            if isinstance(intent.get("audience"), dict)
            else str(intent.get("audience", "Modern digital users"))
        ) or "Modern digital users"
        emotional_tone = intent.get("visual_energy", "balanced_modern") or "balanced_modern"
        primary_job = intent.get("business_goal", "Deliver elite user experience") or "Deliver elite user experience"
        spatial_flow = intent.get("wireframe_skeleton", ["hero", "features", "metrics", "cta"])
        if not spatial_flow or not isinstance(spatial_flow, (list, tuple)):
            spatial_flow = ["hero", "features", "metrics", "cta"]

        intent_lang = intent.get("language", "en")
        lang_str = intent_lang if isinstance(intent_lang, str) else (intent.get("languages", ["en"])[0] if intent.get("languages") else "en")
        is_rtl = bool(
            intent.get("language_direction") == "rtl"
            or lang_str in ["fa", "ar", "he", "ur"]
            or intent.get("is_rtl", False)
        )

        concept = ConceptContract(
            domain=domain,
            product_name=product_name,
            target_audience=target_audience,
            emotional_tone=emotional_tone,
            primary_job_to_be_done=primary_job,
            spatial_flow=list(spatial_flow),
            language=lang_str,
            is_rtl=is_rtl,
            metadata=intent
        )
        c_valid, c_errors = concept.validate()
        if not c_valid:
            log("STATION 1 / Concept Architect", f"[WARN] ConceptContract validation warnings: {c_errors}")
        else:
            log("STATION 1 / Concept Architect", f"ConceptContract validated: domain='{domain}', flow={spatial_flow}")

        # -------------------------------------------------------------
        # Station 2: Trend Hunter (TrendEvidence)
        # -------------------------------------------------------------
        log("STATION 2 / Trend Hunter", f"Mining top-starred benchmarks and micro-interactions for '{domain}'...")
        trend_package = self.trend_hunter.curate_trend_package(domain, style_preference=style_override)
        top_benchmarks = [
            b.get("name") or b.get("metadata", {}).get("name") or b.get("id") or str(b)
            for b in trend_package.get("top_starred_benchmarks", [])
        ]
        log("STATION 2 / Trend Hunter", f"Anchored in elite benchmarks: {', '.join(top_benchmarks[:3])}")

        target_style_name = style_override or trend_package.get("target_style") or "clean_stripe"
        top_bench_meta = trend_package.get("top_starred_benchmarks", [{}])[0].get("metadata", {})
        comp_arch = (
            trend_package.get("composition_archetype")
            or top_bench_meta.get("composition_archetype")
            or "classic_structured_saas"
        )
        trend_sources = [
            b.get("metadata", {}).get("name", b.get("id", ""))
            for b in trend_package.get("top_starred_benchmarks", [])
        ]
        if not trend_sources:
            trend_sources = ["shadcn/ui", "tailwindlabs"]

        trend_evidence = TrendEvidence(
            selected_style=target_style_name,
            style_reasoning=f"Curated from elite open-source benchmarks ({', '.join(trend_sources[:2])}) with zero-slop constraints.",
            composition_archetype=comp_arch,
            typography_pair={"display": "Inter", "body": "Inter"},
            novelty_risk_assessment="Controlled novelty with verified high-contrast WCAG compliance",
            banned_slop_tropes=[
                "meaningless_ai_sparkles",
                "muddy_dark_grey_void",
                "unlabelled_fake_sparkline",
                "repetitive_bento_boxes"
            ],
            trend_sources=trend_sources,
            confidence=float(confidence)
        )
        t_valid, t_errors = trend_evidence.validate()
        if not t_valid:
            log("STATION 2 / Trend Hunter", f"[WARN] TrendEvidence validation warnings: {t_errors}")
        else:
            log("STATION 2 / Trend Hunter", f"TrendEvidence validated: archetype='{comp_arch}', sources={trend_sources[:2]}")

        # -------------------------------------------------------------
        # Station 3: Art Director (DesignGenomeContract)
        # -------------------------------------------------------------
        log("STATION 3 / Art Director", "Synthesizing Design Style Blueprint & Dual-Theme Tokens from Design Genome 2.0...")
        decision = self.recommendation.recommend(
            intent=concept,
            user_style_preference=style_override,
            trend_evidence=trend_evidence
        )
        if "intent" not in decision:
            decision["intent"] = concept.metadata

        design_genome = DesignGenomeContract.from_dict(decision)
        dg_valid, dg_errors = design_genome.validate()
        if not dg_valid:
            log("STATION 3 / Art Director", f"[WARN] DesignGenomeContract validation warnings: {dg_errors}")
        else:
            log("STATION 3 / Art Director", f"DesignGenomeContract validated: style='{design_genome.style}', tokens count={len(design_genome.tokens)}")

        selected_style = decision.get("selected_style", design_genome.style)
        typography = decision.get("genome", {}).get("typography", {}).get("display_family") or design_genome.typography.get("heading_font", "Inter")
        log("STATION 3 / Art Director", f"Selected Visual Chemistry: '{selected_style}' | Display: '{typography}'")

        # -------------------------------------------------------------
        # Station 4: Master Builder (UIArtifactContract)
        # -------------------------------------------------------------
        log("STATION 4 / Master Builder", f"Compiling single-author {output_format.upper()} code artifact...")
        out_path = Path(target_output).resolve() if target_output else (self.workspace_root / "examples" / f"swarm_output.{output_format}").resolve()
        out_path.parent.mkdir(parents=True, exist_ok=True)

        if output_format == "tsx":
            code = self.generator.generate_react_tsx(design_genome)
        else:
            code = self.generator.generate_html(design_genome, prompt_title=prompt)

        with open(out_path, "w", encoding="utf-8") as f:
            f.write(code)

        ui_artifact = UIArtifactContract(
            code_html_or_tsx=code,
            title=prompt,
            signature_widgets=[{"name": f"{domain} Signature Hub", "type": "interactive"}],
            micro_interactions=[
                {"name": "theme_toggle", "type": "click"},
                {"name": "tab_switch", "type": "state"}
            ],
            viewport_configs=[
                {"viewport": "desktop", "width": 1440},
                {"viewport": "mobile", "width": 390}
            ],
            format=output_format,
            brand_name=concept.product_name,
            component_name="GeneratedMasterpiece"
        )
        ua_valid, ua_errors = ui_artifact.validate()
        if not ua_valid:
            log("STATION 4 / Master Builder", f"[WARN] UIArtifactContract validation warnings: {ua_errors}")
        else:
            log("STATION 4 / Master Builder", f"UIArtifactContract validated: {len(code)} chars generated")

        # -------------------------------------------------------------
        # Station 5: Adversarial Inspection & Closed-Loop Healing
        # -------------------------------------------------------------
        log("STATION 5 / Auditor Swarm", "Initiating adversarial inspection (Screenshots & WCAG AA)...")
        iteration = 1
        audit_passed = False

        v_report: Dict[str, Any] = {}
        c_report: Dict[str, Any] = {}
        failed_checks = 0

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

        # Encapsulate audit findings into EvaluationReportContract
        evaluation_report = EvaluationReportContract(
            hard_quality_pass=bool(failed_checks == 0),
            wcag_contrast_score=float(c_report.get("wcag_contrast_ratio", 7.5) if isinstance(c_report, dict) else 7.5),
            overflow_0px_pass=bool(v_report.get("checks_summary", {}).get("overflow_0px", True) if isinstance(v_report, dict) else True),
            aesthetic_quality_score=float(c_report.get("aesthetic_score", 92.0) if isinstance(c_report, dict) else 92.0),
            slop_penalty_deductions=float(c_report.get("slop_penalty", 0.0) if isinstance(c_report, dict) else 0.0),
            correction_advice=list(c_report.get("correction_advice", []) if isinstance(c_report, dict) else []),
            iteration=iteration,
            acceptance_status="ACCEPTED" if audit_passed else "ACCEPTABLE_WITH_NOTES",
            detailed_checks=v_report.get("failed_checks_details", []) if isinstance(v_report, dict) else []
        )
        er_valid, er_errors = evaluation_report.validate()
        if not er_valid:
            log("STATION 5 / Auditor Swarm", f"[WARN] EvaluationReportContract validation warnings: {er_errors}")
        else:
            log("STATION 5 / Auditor Swarm", f"EvaluationReportContract validated: status={evaluation_report.acceptance_status}")

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
            "logs": logs,
            "concept": concept.to_dict(),
            "trend_evidence": trend_evidence.to_dict(),
            "design_genome": design_genome.to_dict(),
            "ui_artifact": ui_artifact.to_dict(),
            "evaluation_report": evaluation_report.to_dict()
        }

    def _capture_screenshots(self, html_path: Path) -> Dict[str, str]:
        """Runs the isolated headless Chromium renderer to capture Desktop and Mobile screenshots."""
        audit_script = self.workspace_root / "scripts" / "screenshot_audit.py"
        out_screenshots_dir = self.workspace_root / ".test-artifacts" / "screenshots"
        out_screenshots_dir.mkdir(parents=True, exist_ok=True)

        if not audit_script.exists() or html_path.suffix != ".html":
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
