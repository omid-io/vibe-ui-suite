"""Static quality heuristics and harness-evidence adapters.

This module deliberately owns no browser, renderer, driver, or automation API.
Real geometry, interaction and visual truth must be supplied by the active AI
harness through vibe_core.browser_evidence.
"""
from __future__ import annotations
import re
from typing import Any, Dict, List, Optional
from vibe_core.pixel_critic import PixelCritic


class PhysicalCritic:
    """Conservative source-level hints; never upgrades heuristics to visual PASS."""
    STANDARD_VIEWPORTS = [
        {"name":"mobile","width":390,"height":844},
        {"name":"tablet","width":768,"height":1024},
        {"name":"desktop","width":1440,"height":900},
    ]

    def __init__(self, enable_browser: bool = False):
        # Retain the argument for source compatibility; browser control is external.
        self.enable_browser = False

    def audit_physical_layout(self, html_content: str, viewports: Optional[List[Dict[str,int]]] = None, page: Any = None) -> Dict[str, Any]:
        """Detect obvious CSS risks without pretending to measure rendered geometry."""
        viewports = viewports or self.STANDARD_VIEWPORTS
        fixed_widths = [int(v) for v in re.findall(r"(?<![a-zA-Z-])width\s*:\s*(\d{3,})px", html_content, re.I)]
        has_blowout = any(width > 430 for width in fixed_widths)
        has_small_target = bool(re.search(r"(?:min-height|height)\s*:\s*(?:[0-3]?\d|4[0-3])px", html_content, re.I))
        defects = []
        if has_blowout:
            defects.append({"type":"possible_horizontal_overflow","severity":"P1","message":"A fixed width above 430px may overflow narrow mobile viewports; confirm in the host harness."})
        if has_small_target:
            defects.append({"type":"possible_substandard_touch_target","severity":"P2","message":"A fixed control dimension below 44px may reduce touch usability; measure in the host harness."})
        score = max(0.0, 100.0 - (20.0 if has_blowout else 0.0) - (8.0 if has_small_target else 0.0))
        return {
            "physical_score": round(score,1),
            "acceptance_status":"REVISE_REQUIRED" if has_blowout else "NOT_EVALUATED",
            "evidence_status":"STATIC_HEURISTIC_ONLY",
            "viewports_tested":[item.get("width") for item in viewports],
            "defects":defects,
            "metrics":{"horizontal_overflow":None,"static_mode":True,"motion_ergonomics":self.audit_motion_ergonomics(html_content)},
            "engine":"static_heuristic",
        }

    def _static_fallback_audit(self, html_content: str, viewports: List[Dict[str,int]], error_note: Optional[str]=None) -> Dict[str,Any]:
        result=self.audit_physical_layout(html_content,viewports=viewports)
        if error_note: result["note"]=error_note
        return result

    def audit_motion_ergonomics(self, code_content: str) -> Dict[str,Any]:
        """Check source patterns only; rendered motion must be observed by the harness."""
        has_motion=bool(re.search(r"@keyframes|animation\s*:|transition\s*:",code_content,re.I))
        checks={
            "has_transition_all":bool(re.search(r"transition\s*:\s*all|transition-all",code_content,re.I)),
            "has_scale_zero":bool(re.search(r"scale\s*\(\s*0(?:\.0+)?\s*\)|scale-0\b",code_content,re.I)),
            "has_excessive_duration":bool(re.search(r"(?:duration|transition-duration)\s*:\s*(?:[3-9]\d{2,}|\d{4,})ms",code_content,re.I)),
            "has_motion":has_motion,
            "has_reduced_motion_guard":bool(re.search(r"prefers-reduced-motion\s*:\s*reduce",code_content,re.I)),
            "has_hover_guard":not bool(re.search(r":hover",code_content,re.I)) or bool(re.search(r"hover\s*:\s*hover.*pointer\s*:\s*fine",code_content,re.I|re.S)),
        }
        defects=[]
        for key,kind,message in [
            ("has_transition_all","motion_transition_all_anti_pattern","Avoid transition: all; animate only changing properties."),
            ("has_scale_zero","motion_scale_zero_entry_anti_pattern","Avoid scaling interactive content from zero."),
            ("has_excessive_duration","motion_excessive_duration","Keep interaction transitions short and intentional."),
            ("has_hover_guard","motion_sticky_touch_hover","Scope hover-only effects to fine pointers."),
        ]:
            if checks[key]: defects.append({"type":kind,"severity":"P2","message":message})
        if has_motion and not checks["has_reduced_motion_guard"]:
            defects.append({"type":"motion_missing_reduced_motion_guard","severity":"P2","message":"Provide a prefers-reduced-motion fallback."})
        return {"motion_score":max(0.0,100.0-10.0*len(defects)),"is_ergonomic":not defects,"defects":defects,"checks":checks}

    @staticmethod
    def _browser_evidence_required(scope: str) -> Dict[str,Any]:
        return {"interactive_verified":False,"status":"NOT_EVALUATED","evidence_status":"HARNESS_BROWSER_REQUIRED",
            "message":f"{scope} must be tested with the browser already exposed by the active AI harness. This package does not launch or control browsers.","defects":[]}

    def audit_runtime_react_tsx(self, tsx_code: str, target_slider_value: Optional[float]=None, is_rtl: bool=False, capture_screenshots: bool=False, domain_id: Optional[str]=None, page: Any=None) -> Dict[str,Any]:
        return self._browser_evidence_required("React/TSX runtime, render and interaction evaluation")

    def audit_runtime_interaction(self, html_content: str, slider_selector: str='input[type="range"]', metric_selector: str="[data-vibe-metric]", target_value: Optional[float]=None, domain_id: Optional[str]=None) -> Dict[str,Any]:
        return self._browser_evidence_required("causal interaction evaluation")

    def audit_screenshot(self, screenshot_bytes: bytes, viewport_name: str="desktop") -> Dict[str,Any]:
        """Apply pure-Python pixel heuristics to screenshot bytes supplied by the harness."""
        return PixelCritic().audit_screenshot(screenshot_bytes, viewport_name=viewport_name)
