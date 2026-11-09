#!/usr/bin/env python3
"""Harness-neutral browser evidence contracts. This package never owns a browser."""
from __future__ import annotations
import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

SCHEMA_VERSION = "vibe.browser-evidence/v1"
REQUIRED_VIEWPORTS = {"mobile": lambda w: 320 <= w <= 430, "tablet": lambda w: 600 <= w <= 900, "desktop": lambda w: w >= 1200}
REQUIRED_CHECKS = ("responsive_layout", "runtime_errors", "accessibility", "interaction_smoke", "visual_review")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_browser_request(artifact_path: Path, request_path: Optional[Path] = None) -> Dict[str, Any]:
    artifact_path = artifact_path.resolve(strict=True)
    request = {
        "schema_version": SCHEMA_VERSION,
        "artifact": {"path": str(artifact_path), "sha256": sha256_file(artifact_path)},
        "required_viewports": [
            {"name": "mobile", "width": 390, "height": 844},
            {"name": "tablet", "width": 768, "height": 1024},
            {"name": "desktop", "width": 1440, "height": 900},
        ],
        "required_checks": list(REQUIRED_CHECKS),
        "instructions": [
            "Use only browser capabilities already exposed by the active AI harness; never install or launch a browser through this package.",
            "Render the exact artifact or the consumer project that imports it; use the host project's normal runtime for framework components.",
            "Capture full-page screenshots at every required viewport and inspect every image with a vision-capable reviewer.",
            "Measure horizontal overflow, broken images, page/console errors, computed accessibility, and real interaction outcomes.",
            "Exercise navigation, buttons, forms, menus, dialogs, keyboard focus, Escape dismissal and reduced-motion behavior where applicable.",
            "Do not edit the artifact after capture. Any source change invalidates this request and requires a fresh browser pass.",
            "Write a vibe.browser-evidence/v1 JSON report and validate it before claiming runtime acceptance.",
        ],
    }
    if request_path:
        request_path.parent.mkdir(parents=True, exist_ok=True)
        request_path.write_text(json.dumps(request, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return request


def _screenshot_ref(value: Any, report_dir: Optional[Path]) -> Tuple[str, Optional[str]]:
    if not isinstance(value, dict):
        return "", "screenshot must be an object"
    uri = value.get("uri") or value.get("attachment_id")
    if isinstance(uri, str) and uri.strip():
        return uri.strip(), None
    raw_path = value.get("path")
    if not isinstance(raw_path, str) or not raw_path.strip():
        return "", "screenshot requires path, uri, or attachment_id"
    path = Path(raw_path)
    if not path.is_absolute() and report_dir:
        path = report_dir / path
    try:
        path = path.resolve(strict=True)
        if not path.is_file() or path.stat().st_size <= 0:
            return "", f"screenshot is empty or not a file: {raw_path}"
        if value.get("sha256") and str(value["sha256"]).lower() != sha256_file(path):
            return "", f"screenshot SHA-256 mismatch: {raw_path}"
    except OSError:
        return "", f"screenshot file not found: {raw_path}"
    return str(path), None


def validate_browser_evidence(evidence: Dict[str, Any], artifact_path: Path, report_path: Optional[Path] = None) -> Tuple[Dict[str, Any], List[str]]:
    """Return normalized evidence and structural/identity errors.

    A well-formed report with failed measurements is valid evidence with FAIL.
    A stale, malformed or incomplete report is NOT_EVALUATED and cannot pass.
    """
    errors: List[str] = []
    if not isinstance(evidence, dict):
        return {}, ["report root must be a JSON object"]
    if evidence.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"schema_version must be {SCHEMA_VERSION}")
    artifact = evidence.get("artifact")
    if not isinstance(artifact, dict) or not isinstance(artifact.get("sha256"), str):
        errors.append("artifact.sha256 is required")
    else:
        try:
            if artifact["sha256"].lower() != sha256_file(artifact_path.resolve(strict=True)):
                errors.append("artifact SHA-256 mismatch: report is stale or belongs to another artifact")
        except OSError as exc:
            errors.append(f"cannot hash target artifact: {exc}")

    runtime = evidence.get("runtime")
    if not isinstance(runtime, dict):
        runtime = {}
        errors.append("runtime must be an object")
    for key in ("harness", "browser", "browser_version", "platform"):
        if not isinstance(runtime.get(key), str) or not runtime[key].strip():
            errors.append(f"runtime.{key} is required")

    captured_at = evidence.get("captured_at")
    if not isinstance(captured_at, str) or not captured_at.strip():
        errors.append("captured_at is required")
    else:
        try:
            datetime.fromisoformat(captured_at.replace("Z", "+00:00"))
        except ValueError:
            errors.append("captured_at must be an ISO-8601 timestamp")
    if evidence.get("overall_status") not in {"PASS", "FAIL"}:
        errors.append("overall_status must be PASS or FAIL")

    raw_viewports = evidence.get("viewports")
    if not isinstance(raw_viewports, list):
        raw_viewports = []
        errors.append("viewports must be an array")
    normalized: Dict[str, Dict[str, Any]] = {}
    refs: Dict[str, str] = {}
    for i, vp in enumerate(raw_viewports):
        p = f"viewports[{i}]"
        if not isinstance(vp, dict):
            errors.append(f"{p} must be an object")
            continue
        name, width, height = vp.get("name"), vp.get("width"), vp.get("height")
        if not isinstance(name, str) or not name.strip():
            errors.append(f"{p}.name is required")
            continue
        if not isinstance(width, int) or isinstance(width, bool) or width < 1:
            errors.append(f"{p}.width must be a positive integer")
            continue
        if not isinstance(height, int) or isinstance(height, bool) or height < 1:
            errors.append(f"{p}.height must be a positive integer")
            continue
        if not isinstance(vp.get("horizontal_overflow"), bool):
            errors.append(f"{p}.horizontal_overflow must be boolean")
        broken = vp.get("broken_images")
        if not isinstance(broken, int) or isinstance(broken, bool) or broken < 0:
            errors.append(f"{p}.broken_images must be a non-negative integer")
            broken = -1
        console = vp.get("console_errors", [])
        if not isinstance(console, list) or not all(isinstance(item, str) for item in console):
            errors.append(f"{p}.console_errors must be an array of strings")
            console = ["invalid console error payload"]
        ref, error = _screenshot_ref(vp.get("screenshot"), report_path.parent if report_path else None)
        if error:
            errors.append(f"{p}: {error}")
        else:
            refs[name] = ref
        normalized[name] = {
            "name": name, "width": width, "height": height,
            "horizontal_overflow": vp.get("horizontal_overflow"),
            "broken_images": broken, "console_errors": console,
            "screenshot_path": ref, "file_size_bytes": vp.get("screenshot", {}).get("bytes") if isinstance(vp.get("screenshot"), dict) else None,
            "status": "PASS" if vp.get("horizontal_overflow") is False and broken == 0 and not console and ref else "FAIL",
        }

    coverage = {name: any(test(vp["width"]) for vp in normalized.values()) for name, test in REQUIRED_VIEWPORTS.items()}
    for name, ok in coverage.items():
        if not ok:
            errors.append(f"missing required {name} viewport evidence")

    checks_raw = evidence.get("checks")
    if not isinstance(checks_raw, list):
        checks_raw = []
        errors.append("checks must be an array")
    checks: Dict[str, Dict[str, Any]] = {}
    for i, check in enumerate(checks_raw):
        if not isinstance(check, dict) or not isinstance(check.get("id"), str) or not check["id"].strip():
            errors.append(f"checks[{i}].id is required")
            continue
        check_id = check["id"]
        if check_id in checks:
            errors.append(f"duplicate check id: {check_id}")
        if check.get("status") not in {"PASS", "FAIL", "WARN", "NOT_EVALUATED"}:
            errors.append(f"checks[{i}].status is invalid")
        if not isinstance(check.get("summary"), str) or not check["summary"].strip():
            errors.append(f"checks[{i}].summary is required")
        checks[check_id] = check
    for required in REQUIRED_CHECKS:
        if required not in checks:
            errors.append(f"missing required check: {required}")

    visual = evidence.get("visual_review")
    if not isinstance(visual, dict):
        visual = {}
        errors.append("visual_review must be an object")
    for key in ("reviewer", "summary"):
        if not isinstance(visual.get(key), str) or not visual[key].strip():
            errors.append(f"visual_review.{key} is required")
    if visual.get("status") not in {"PASS", "FAIL"}:
        errors.append("visual_review.status must be PASS or FAIL")
    inspected = visual.get("inspected_screenshots")
    if not isinstance(inspected, list) or not all(isinstance(v, str) for v in inspected):
        inspected = []
        errors.append("visual_review.inspected_screenshots must be an array")
    for profile in REQUIRED_VIEWPORTS:
        if profile not in inspected:
            errors.append(f"visual reviewer did not inspect {profile} screenshot")
    if not isinstance(visual.get("findings"), list):
        errors.append("visual_review.findings must be an array")

    if errors:
        return {
            "success": False, "overall_status": "NOT_EVALUATED",
            "overflow_status": "NOT_EVALUATED", "screenshot_status": "NOT_EVALUATED",
            "files": {}, "viewports": normalized, "error": "; ".join(errors),
        }, errors

    checks_pass = all(checks[key]["status"] == "PASS" for key in REQUIRED_CHECKS)
    viewports_pass = all(vp["status"] == "PASS" for vp in normalized.values())
    overall = "PASS" if evidence["overall_status"] == "PASS" and checks_pass and viewports_pass and visual["status"] == "PASS" else "FAIL"
    mobile_ref = next((ref for name, ref in refs.items() if normalized[name]["width"] <= 430), "")
    desktop_ref = next((ref for name, ref in refs.items() if normalized[name]["width"] >= 1200), "")
    overflow_status = "PASS" if all(vp["horizontal_overflow"] is False for vp in normalized.values()) else "FAIL"
    screenshot_status = "PASS" if mobile_ref and desktop_ref and visual["status"] == "PASS" else "FAIL"
    return {
        "success": True, "overall_status": overall,
        "overflow_status": overflow_status, "screenshot_status": screenshot_status,
        "files": {"desktop": desktop_ref, "mobile": mobile_ref},
        "viewports": normalized, "runtime": runtime, "visual_review": visual,
        "checks": checks, "artifact_sha256": artifact["sha256"], "captured_at": captured_at,
    }, []


def load_browser_evidence(report_path: Path, artifact_path: Path) -> Tuple[Dict[str, Any], List[str]]:
    try:
        report = json.loads(report_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return {
            "success": False, "overall_status": "NOT_EVALUATED",
            "overflow_status": "NOT_EVALUATED", "screenshot_status": "NOT_EVALUATED",
            "files": {}, "viewports": {}, "error": f"cannot read evidence report: {exc}",
        }, [str(exc)]
    return validate_browser_evidence(report, artifact_path, report_path)
