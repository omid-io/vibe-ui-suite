#!/usr/bin/env python3
"""Regression tests for evidence-backed acceptance and consumer runtime behavior."""

from pathlib import Path
import tempfile

from schemas.agent_contracts import EvaluationReportContract, TrendEvidence
from vibe_core.swarm import (
    ForemanSwarmOrchestrator,
    _extract_overflow_status,
    _extract_screenshot_status,
    _extract_wcag_evidence,
    _severity_penalty,
)
from vibe_core.verifier import VerificationEngine


def assert_true(condition, message):
    if not condition:
        raise AssertionError(message)
    print(f"[PASS] {message}")


def run():
    ratio, status = _extract_wcag_evidence({
        "evidence_records": [{
            "check_name": "Body Copy Contrast Ratio",
            "status": "PASS",
            "measured_value": "18.10:1",
            "evidence": "Body contrast 18.10:1 exceeds threshold (>= 4.5:1)",
        }]
    })
    assert_true(ratio == 18.10 and status == "PASS", "WCAG score reads measured_value and check_name")

    ratio, status = _extract_wcag_evidence({
        "evidence_records": [{
            "check_name": "Body Copy Contrast Ratio",
            "status": "WARN",
            "measured_value": "unresolved",
            "evidence": "Runtime browser verification required; threshold >= 4.5:1",
        }]
    })
    assert_true(ratio == 0.0 and status == "NOT_EVALUATED", "WCAG threshold is never mistaken for measured contrast")

    assert_true(
        _extract_overflow_status({"viewports": {
            "desktop": {"horizontal_overflow": False},
            "mobile": {"horizontal_overflow": True},
        }}) == "FAIL",
        "Overflow evidence checks every viewport",
    )
    assert_true(
        _extract_screenshot_status({
            "overall_status": "PASS",
            "screenshot_status": "PASS",
            "files": {"desktop": "/tmp/desktop.png", "mobile": ""},
        }) == "NOT_EVALUATED",
        "Missing screenshot file map cannot be accepted",
    )
    assert_true(
        [_severity_penalty(v) for v in ("critical", "high", "medium", "low")] == [10.0, 7.0, 4.0, 1.0],
        "Critic severity vocabulary maps to distinct penalty weights",
    )

    default_report = EvaluationReportContract()
    valid, errors = default_report.validate()
    assert_true(valid, f"Unevaluated evidence remains explicit and valid: {errors}")

    invalid_report = EvaluationReportContract(
        overflow_0px_pass=True,
        overflow_status="FAIL",
    )
    valid, _ = invalid_report.validate()
    assert_true(not valid, "Evaluation contract rejects contradictory overflow evidence")

    trend = TrendEvidence(
        selected_style="editorial",
        style_reasoning="Matched local genome",
        composition_archetype="asymmetric_editorial_split",
        typography_pair={},
        novelty_risk_assessment="Not provided by source",
        banned_slop_tropes=[],
    )
    valid, errors = trend.validate()
    assert_true(valid, f"Absent typography suggestion is represented honestly: {errors}")

    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        package_root = root / "package"
        consumer_root = root / "consumer"
        source_asset = package_root / "assets" / "curated_webp" / "sample.webp"
        source_asset.parent.mkdir(parents=True)
        source_asset.write_bytes(b"package asset")
        output_path = consumer_root / "generated" / "index.html"
        output_path.parent.mkdir(parents=True)
        orchestrator = ForemanSwarmOrchestrator.__new__(ForemanSwarmOrchestrator)
        orchestrator.package_root = package_root
        delivered = orchestrator._provision_consumer_assets(
            '<img src="assets/curated_webp/sample.webp">', output_path
        )
        consumer_asset = output_path.parent / "assets" / "curated_webp" / "sample.webp"
        assert_true(consumer_asset.is_file() and delivered["copied"], "Package provisions referenced assets beside consumer output")
        consumer_asset.write_bytes(b"consumer-owned")
        orchestrator._provision_consumer_assets(
            '<img src="assets/curated_webp/sample.webp">', output_path
        )
        assert_true(consumer_asset.read_bytes() == b"consumer-owned", "Asset provisioning never overwrites consumer-owned files")

        asset = root / "assets" / "curated_webp" / "sample.webp"
        asset.parent.mkdir(parents=True)
        asset.write_bytes(b"test")
        html = (
            '<html><head><meta name="viewport" content="width=device-width, initial-scale=1.0">'
            '<style>body { background: #ffffff; color: #111111; } :focus-visible { outline: 2px solid; }'
            '</style></head><body><img src="assets/curated_webp/sample.webp"></body></html>'
        )
        report = VerificationEngine().verify_html(html, base_dir=root)
        asset_check = next(
            item for item in report["evidence_records"]
            if item.get("check_name") == "Asset Media Integrity"
        )
        assert_true(asset_check["status"] == "PASS", "Verifier confirms referenced consumer asset exists on disk")

        missing_report = VerificationEngine().verify_html(
            html.replace("sample.webp", "missing.webp"),
            base_dir=root,
        )
        missing_check = next(
            item for item in missing_report["evidence_records"]
            if item.get("check_name") == "Asset Media Integrity"
        )
        assert_true(missing_check["status"] == "FAIL", "Verifier fails when a referenced consumer asset is absent")


if __name__ == "__main__":
    run()
