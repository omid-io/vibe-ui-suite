#!/usr/bin/env python3
"""Regression tests for evidence-backed acceptance and consumer runtime behavior."""

from pathlib import Path
import sys
import tempfile

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from schemas.agent_contracts import EvaluationReportContract, TrendEvidence
from vibe_core.director import DesignDirector, normalize_text
from vibe_core.swarm import (
    _is_runtime_only_blocker,
    ForemanSwarmOrchestrator,
    _extract_overflow_status,
    _extract_screenshot_status,
    _extract_wcag_evidence,
    _severity_penalty,
)
from vibe_core.verifier import VerificationEngine
from vibe_core.browser_evidence import SCHEMA_VERSION, build_browser_request, validate_browser_evidence


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

    unavailable_browser = {
        "success": False,
        "overall_status": "NOT_EVALUATED",
        "overflow_status": "NOT_EVALUATED",
        "screenshot_status": "NOT_EVALUATED",
    }
    assert_true(
        _is_runtime_only_blocker(0, "PASS", "ACCEPTED", True, unavailable_browser),
        "Unavailable browser runtime skips image-agnostic healing when all code gates pass",
    )
    assert_true(
        not _is_runtime_only_blocker(1, "PASS", "ACCEPTED", True, unavailable_browser),
        "Static code failures still permit a healing attempt when browser runtime is unavailable",
    )
    assert_true(
        not _is_runtime_only_blocker(0, "PASS", "REJECTED", True, unavailable_browser),
        "Critic rejection still permits a healing attempt when browser runtime is unavailable",
    )

    director = DesignDirector()
    domain, confidence, reasons = director._match_domain(
        normalize_text("modern dark luxury real estate showcase")
    )
    assert_true(
        domain.get("id") == "real_estate_architecture" and confidence >= 0.80,
        f"Luxury real-estate showcase prompt gets high-confidence domain match ({confidence:.2f}; {reasons})",
    )

    default_report = EvaluationReportContract()
    valid, errors = default_report.validate()
    assert_true(valid, f"Unevaluated evidence remains explicit and valid: {errors}")

    # Harness-native evidence is bound to the exact artifact and inspected viewports.
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        artifact = root / "index.html"
        artifact.write_text("<!doctype html><title>Evidence fixture</title>", encoding="utf-8")
        import hashlib
        digest = hashlib.sha256(artifact.read_bytes()).hexdigest()
        shots = {}
        for name in ("mobile", "tablet", "desktop"):
            shot = root / f"{name}.png"
            shot.write_bytes(b"non-empty test screenshot bytes")
            shots[name] = shot
        evidence = {
            "schema_version": SCHEMA_VERSION,
            "artifact": {"path": str(artifact), "sha256": digest},
            "runtime": {"harness": "test-harness", "browser": "WebKit", "browser_version": "stable", "platform": "linux"},
            "captured_at": "2026-11-09T12:00:00Z", "overall_status": "PASS",
            "viewports": [
                {"name": name, "width": width, "height": height, "horizontal_overflow": False,
                 "broken_images": 0, "console_errors": [],
                 "screenshot": {"path": str(shots[name]), "sha256": hashlib.sha256(shots[name].read_bytes()).hexdigest()}}
                for name, width, height in (("mobile",390,844),("tablet",768,1024),("desktop",1440,900))
            ],
            "checks": [
                {"id":"responsive_layout","status":"PASS","summary":"No overflow at required viewports"},
                {"id":"runtime_errors","status":"PASS","summary":"No page or console errors"},
                {"id":"accessibility","status":"PASS","summary":"Keyboard and accessible names passed"},
                {"id":"interaction_smoke","status":"PASS","summary":"Navigation and controls exercised"},
                {"id":"visual_review","status":"PASS","summary":"All screenshots inspected"},
            ],
            "visual_review": {"status":"PASS","reviewer":"vision-enabled-test-agent",
                "summary":"Balanced layout at all viewport classes",
                "inspected_screenshots":["mobile","tablet","desktop"],"findings":[],"score":94}
        }
        request = build_browser_request(artifact, root / ".vibe" / "browser-evidence-request.json")
        assert_true(request["artifact"]["sha256"] == digest, "Browser request binds to final artifact SHA-256")
        accepted, errors = validate_browser_evidence(evidence, artifact, root / "browser-evidence.json")
        assert_true(not errors and accepted["overall_status"] == "PASS", f"Valid harness evidence passes gates: {errors}")
        stale = dict(evidence); stale["artifact"] = dict(evidence["artifact"], sha256="0" * 64)
        rejected, stale_errors = validate_browser_evidence(stale, artifact, root / "browser-evidence.json")
        assert_true(rejected["overall_status"] == "NOT_EVALUATED" and any("SHA-256" in item for item in stale_errors), "Stale browser evidence is rejected")
        failing = dict(evidence); failing["viewports"] = [dict(item) for item in evidence["viewports"]]
        failing["viewports"][0]["horizontal_overflow"] = True
        failing_report, failing_errors = validate_browser_evidence(failing, artifact, root / "browser-evidence.json")
        assert_true(not failing_errors and failing_report["overall_status"] == "FAIL", "Measured overflow blocks acceptance")
        no_vision = dict(evidence); no_vision["visual_review"] = dict(evidence["visual_review"], status="FAIL")
        no_vision_report, no_vision_errors = validate_browser_evidence(no_vision, artifact, root / "browser-evidence.json")
        assert_true(not no_vision_errors and no_vision_report["overall_status"] == "FAIL", "Visual rejection blocks runtime acceptance")


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
