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
import re
import shutil
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


def _extract_wcag_evidence(report: Dict[str, Any]) -> Tuple[float, str]:
    """Return only a measured body-copy contrast ratio; never substitute a target threshold."""
    for record in report.get("evidence_records", []):
        check_name = str(record.get("check_name") or record.get("name") or "").lower()
        if "contrast" not in check_name:
            continue
        measured = str(record.get("measured_value") or "")
        match = re.search(r"(\d+(?:\.\d+)?)\s*:\s*1", measured)
        if not match:
            evidence = str(record.get("evidence") or "")
            match = re.search(r"(?i)body contrast\s+(\d+(?:\.\d+)?)\s*:\s*1", evidence)
        status = str(record.get("status", "")).upper()
        if match and status in {"PASS", "FAIL"}:
            return min(21.0, max(0.0, float(match.group(1)))), status
        return 0.0, "NOT_EVALUATED"
    return 0.0, "NOT_EVALUATED"


def _extract_overflow_status(report: Dict[str, Any]) -> str:
    explicit = str(report.get("overflow_status", "")).upper()
    if explicit in {"PASS", "FAIL"}:
        return explicit
    viewports = report.get("viewports", {})
    if not isinstance(viewports, dict) or not viewports:
        return "NOT_EVALUATED"
    records = list(viewports.values())
    if not all("horizontal_overflow" in record for record in records if isinstance(record, dict)):
        return "NOT_EVALUATED"
    return "FAIL" if any(record.get("horizontal_overflow") for record in records) else "PASS"


def _extract_screenshot_status(report: Dict[str, Any]) -> str:
    explicit = str(report.get("screenshot_status", "")).upper()
    files = report.get("files", {})
    has_both = isinstance(files, dict) and all(files.get(name) for name in ("desktop", "mobile"))
    if explicit in {"PASS", "FAIL"}:
        return explicit if (explicit == "FAIL" or has_both) else "NOT_EVALUATED"
    overall = str(report.get("overall_status", "")).upper()
    if overall == "FAIL":
        return "FAIL"
    return "PASS" if overall == "PASS" and has_both else "NOT_EVALUATED"


def _is_runtime_only_blocker(
    failed_checks: int,
    wcag_status: str,
    critic_status: str,
    critic_hard_gates: bool,
    screenshot_report: Dict[str, Any],
) -> bool:
    """Return True when browser evidence is unavailable and every code gate passed.

    In this case the code-only healer cannot repair the missing browser runtime.
    Keep the result explicitly unaccepted, but avoid repeating identical code edits.
    """
    browser_not_evaluated = bool(
        screenshot_report.get("success") is not True
        and str(screenshot_report.get("overall_status", "")).upper() == "NOT_EVALUATED"
        and _extract_overflow_status(screenshot_report) == "NOT_EVALUATED"
        and _extract_screenshot_status(screenshot_report) == "NOT_EVALUATED"
    )
    return bool(
        browser_not_evaluated
        and failed_checks == 0
        and str(wcag_status).upper() == "PASS"
        and str(critic_status).upper() == "ACCEPTED"
        and critic_hard_gates
    )


def _severity_penalty(severity: Any) -> float:
    """Map the critic's actual severity vocabulary to stable penalty weights."""
    return {
        "critical": 10.0,
        "high": 7.0,
        "medium": 4.0,
        "low": 1.0,
    }.get(str(severity or "").strip().lower(), 0.0)


class ForemanSwarmOrchestrator:
    """Master orchestrator running the multi-agent pipeline deterministically."""

    def __init__(self, workspace_root: Optional[Path] = None):
        self.package_root = ROOT_DIR
        self.workspace_root = Path(workspace_root or Path.cwd()).resolve()
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
        max_remediation_loops: int = 3,
        quiet: bool = False
    ) -> Dict[str, Any]:
        """
        Executes the full 5-station pipeline from raw user prompt to verified screenshots.
        Enforces formal contract generation, validation, and delivery across all stations.
        """
        logs = []
        def log(station: str, message: str):
            entry = f"[{station}] {message}"
            logs.append(entry)
            if quiet:
                print(entry, file=sys.stderr)
            else:
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
            style_reasoning=trend_package.get(
                "style_reasoning",
                f"Curated from local Design Genome and open-source benchmarks ({', '.join(trend_sources[:2])})."
            ),
            composition_archetype=comp_arch,
            typography_pair=trend_package.get("typography_pair") or {},
            novelty_risk_assessment="Domain-calibrated novelty; browser and critic gates determine acceptance",
            banned_slop_tropes=trend_package.get("banned_slop_tropes") or [
                "meaningless_ai_sparkles",
                "muddy_dark_grey_void",
                "unlabelled_fake_sparkline",
                "repetitive_bento_boxes"
            ],
            trend_sources=trend_sources,
            confidence=float(trend_package.get("evidence_confidence", confidence))
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
        out_path = Path(target_output).resolve() if target_output else (Path.cwd() / f"swarm_output.{output_format}").resolve()
        out_path.parent.mkdir(parents=True, exist_ok=True)

        if output_format == "tsx":
            code = self.generator.generate_react_tsx(design_genome)
        else:
            code = self.generator.generate_html(design_genome, prompt_title=prompt)

        asset_delivery = self._provision_consumer_assets(code, out_path)
        if asset_delivery["missing"]:
            log("STATION 4 / Master Builder", f"[WARN] {len(asset_delivery['missing'])} referenced curated asset(s) could not be provisioned")

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
        screenshot_report: Dict[str, Any] = {}
        failed_checks = 0

        while iteration <= max_remediation_loops:
            asset_delivery = self._provision_consumer_assets(code, out_path)
            v_report = self.verifier.verify_html(
                code,
                out_path.name,
                mode="fast",
                base_dir=out_path.parent
            )
            failed_checks = v_report.get("checks_summary", {}).get("failed", 0)

            # Browser audit is part of the acceptance gate, not a post-hoc artifact.
            screenshot_report = self._capture_screenshots(out_path)

            c_report = self.critic.critique(code, decision, iteration=iteration)
            critic_status_raw = str(c_report.get("acceptance_status", "NOT_EVALUATED")).upper()
            critic_status = (
                "ACCEPTED" if critic_status_raw == "ACCEPTED"
                else "REJECTED" if critic_status_raw in {"REJECTED", "FAILED"}
                else "NOT_EVALUATED"
            )

            wcag_score, wcag_status = _extract_wcag_evidence(v_report)
            overflow_status = _extract_overflow_status(screenshot_report)
            screenshot_status = _extract_screenshot_status(screenshot_report)
            browser_overall = str(screenshot_report.get("overall_status", "NOT_EVALUATED")).upper()
            critic_hard_gates = c_report.get("hard_gates_pass", True) is not False

            audit_passed = bool(
                failed_checks == 0
                and wcag_status == "PASS"
                and overflow_status == "PASS"
                and screenshot_status == "PASS"
                and browser_overall == "PASS"
                and critic_status == "ACCEPTED"
                and critic_hard_gates
            )
            if audit_passed:
                log("STATION 5 / Auditor Swarm", f"All static, WCAG, browser, screenshot, and critic gates passed on iteration {iteration}.")
                break

            log(
                "STATION 5 / Auditor Swarm",
                f"Iteration {iteration}: static failures={failed_checks}, WCAG={wcag_status}, "
                f"overflow={overflow_status}, screenshot={screenshot_status}, critic={critic_status}."
            )
            if iteration >= max_remediation_loops:
                break

            if _is_runtime_only_blocker(
                failed_checks=failed_checks,
                wcag_status=wcag_status,
                critic_status=critic_status,
                critic_hard_gates=critic_hard_gates,
                screenshot_report=screenshot_report,
            ):
                runtime_reason = str(
                    screenshot_report.get("error")
                    or screenshot_report.get("stderr")
                    or "Playwright/Chromium did not produce browser evidence"
                ).replace("\\n", " ").strip()[:240]
                log(
                    "STATION 5 / Auditor Swarm",
                    "All code-based gates passed, but browser evidence is unavailable; "
                    f"skipping code-only healing because it cannot repair the runtime blocker ({runtime_reason}). "
                    "Acceptance remains ACCEPTABLE_WITH_NOTES until browser verification succeeds."
                )
                break

            # The current healer acts on critic findings; it does not receive pixels.
            # Browser findings therefore block acceptance but are not represented as
            # image-understanding or screenshot-driven LLM remediation.
            code, c_report, correction_prompt = self.healer.heal(
                code, decision, original_prompt=prompt
            )
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(code)
            iteration += 1

        wcag_score, wcag_status = _extract_wcag_evidence(v_report)
        overflow_status = _extract_overflow_status(screenshot_report)
        screenshot_status = _extract_screenshot_status(screenshot_report)
        critic_status_raw = str(c_report.get("acceptance_status", "NOT_EVALUATED")).upper()
        critic_status = (
            "ACCEPTED" if critic_status_raw == "ACCEPTED"
            else "REJECTED" if critic_status_raw in {"REJECTED", "FAILED"}
            else "NOT_EVALUATED"
        )

        critic_score_raw = c_report.get("quality_score", c_report.get("score"))
        try:
            critic_score = max(0.0, min(100.0, float(critic_score_raw))) if critic_score_raw is not None else 0.0
        except (TypeError, ValueError):
            critic_score = 0.0

        slop_penalty = 0.0
        advice_list: List[str] = []
        if isinstance(c_report, dict):
            for defect in c_report.get("defects_ranked", []):
                slop_penalty += _severity_penalty(defect.get("severity", ""))
                msg = defect.get("message") or defect.get("suggested_patch")
                if msg and str(msg) not in advice_list:
                    advice_list.append(str(msg))

        detailed_checks: List[Dict[str, Any]] = []
        detailed_checks.extend(v_report.get("evidence_records", []))
        for vp_name, vp_record in screenshot_report.get("viewports", {}).items():
            detailed_checks.append({
                "pillar": "Browser Runtime",
                "check_name": f"{vp_name.title()} Viewport Screenshot Audit",
                "status": vp_record.get("status", "NOT_EVALUATED"),
                "evidence": (
                    f"overflow={vp_record.get('horizontal_overflow')}; "
                    f"broken_images={vp_record.get('broken_images')}; "
                    f"screenshot_bytes={vp_record.get('file_size_bytes')}; "
                    f"path={vp_record.get('screenshot_path')}"
                )
            })
        detailed_checks.extend(c_report.get("hard_gate_failures", []))

        hard_quality_pass = bool(
            failed_checks == 0
            and wcag_status == "PASS"
            and overflow_status == "PASS"
            and screenshot_status == "PASS"
            and screenshot_report.get("overall_status") == "PASS"
            and critic_status == "ACCEPTED"
            and c_report.get("hard_gates_pass", True) is not False
        )
        evaluation_report = EvaluationReportContract(
            hard_quality_pass=hard_quality_pass,
            wcag_contrast_score=round(wcag_score, 2),
            overflow_0px_pass=(overflow_status == "PASS"),
            aesthetic_quality_score=round(critic_score, 1),
            slop_penalty_deductions=round(slop_penalty, 1),
            correction_advice=advice_list,
            iteration=iteration,
            acceptance_status="ACCEPTED" if hard_quality_pass else "ACCEPTABLE_WITH_NOTES",
            detailed_checks=detailed_checks,
            wcag_contrast_status=wcag_status,
            overflow_status=overflow_status,
            screenshot_status=screenshot_status,
            critic_status=critic_status,
            runtime_mode=(
                "browser_runtime_eval"
                if screenshot_report.get("success") is True
                else str(v_report.get("runtime_mode", "static_only"))
            )
        )
        er_valid, er_errors = evaluation_report.validate()
        if not er_valid:
            log("STATION 5 / Auditor Swarm", f"[WARN] EvaluationReportContract validation warnings: {er_errors}")
        else:
            log("STATION 5 / Auditor Swarm", f"EvaluationReportContract validated: status={evaluation_report.acceptance_status}")

        # Keep a compact file map for existing consumers; retain full audit evidence separately.
        screenshot_results = screenshot_report.get("files", {})
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
            "screenshot_audit": screenshot_report,
            "asset_delivery": asset_delivery,
            "iterations_count": iteration,
            "logs": logs,
            "concept": concept.to_dict(),
            "trend_evidence": trend_evidence.to_dict(),
            "design_genome": design_genome.to_dict(),
            "ui_artifact": ui_artifact.to_dict(),
            "evaluation_report": evaluation_report.to_dict()
        }

    def _provision_consumer_assets(self, html: str, output_path: Path) -> Dict[str, List[str]]:
        """Copy only referenced package assets, without overwriting consumer files."""
        copied: List[str] = []
        missing: List[str] = []
        references = sorted(set(re.findall(r'assets/curated_webp/[^\s"\',)]+', html)))
        for relative in references:
            relative_path = Path(relative)
            if relative_path.is_absolute() or ".." in relative_path.parts:
                missing.append(relative)
                continue
            source = (self.package_root / relative_path).resolve()
            destination = (output_path.parent / relative_path).resolve()
            if output_path.parent.resolve() not in destination.parents:
                missing.append(relative)
                continue
            if destination.is_file():
                continue
            if not source.is_file():
                missing.append(relative)
                continue
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
            copied.append(str(destination))
        return {"copied": copied, "missing": missing}

    def _capture_screenshots(self, html_path: Path) -> Dict[str, Any]:
        """Capture and return full browser audit evidence under the consumer workspace."""
        audit_script = self.package_root / "scripts" / "screenshot_audit.py"
        out_screenshots_dir = self.workspace_root / ".test-artifacts" / "screenshots"
        out_screenshots_dir.mkdir(parents=True, exist_ok=True)

        report: Dict[str, Any] = {
            "overall_status": "NOT_EVALUATED",
            "overflow_status": "NOT_EVALUATED",
            "screenshot_status": "NOT_EVALUATED",
            "success": False,
            "files": {},
            "viewports": {},
        }
        if not audit_script.is_file() or html_path.suffix.lower() not in {".html", ".tsx"}:
            report["error"] = "Browser audit script or supported HTML/TSX artifact is unavailable"
            return report

        try:
            result = subprocess.run(
                [
                    sys.executable,
                    str(audit_script),
                    str(html_path.resolve()),
                    "--json",
                    "-o",
                    str(out_screenshots_dir),
                ],
                capture_output=True,
                text=True,
                timeout=120,
                cwd=str(self.workspace_root),
            )
            if result.stdout.strip():
                try:
                    parsed = json.loads(result.stdout)
                    if isinstance(parsed, dict):
                        report.update(parsed)
                except json.JSONDecodeError:
                    report["error"] = "Screenshot audit did not return valid JSON"
            if result.returncode != 0 and report.get("overall_status") == "PASS":
                report["overall_status"] = "FAIL"
            if result.stderr.strip():
                report["stderr"] = result.stderr.strip()[-4000:]
        except (OSError, subprocess.TimeoutExpired) as exc:
            report["error"] = str(exc)

        files = report.get("files", {})
        if not isinstance(files, dict):
            files = {}
        normalized_files: Dict[str, str] = {}
        for name in ("desktop", "mobile"):
            candidate = files.get(name, "")
            try:
                candidate_path = Path(candidate) if candidate else None
                if candidate_path and candidate_path.is_file() and candidate_path.stat().st_size > 0:
                    normalized_files[name] = str(candidate_path.resolve())
                else:
                    normalized_files[name] = ""
            except OSError:
                normalized_files[name] = ""
        report["files"] = normalized_files

        if report.get("overall_status") == "PASS" and not all(normalized_files.values()):
            report["overall_status"] = "FAIL"
            report["screenshot_status"] = "FAIL"
            report["error"] = "Browser audit reported PASS but one or more screenshot files are missing or empty"
        return report
