#!/usr/bin/env python3
"""Browser-neutral tests for source heuristics and external browser evidence."""
from pathlib import Path
import sys
ROOT_DIR=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT_DIR))
from vibe_core.physical_critic import PhysicalCritic

def main():
    critic=PhysicalCritic(enable_browser=True)
    clean='<html><head><meta name="viewport"></head><body><button style="min-height:48px">Go</button></body></html>'
    risky='<html><body><main style="width:650px"><button style="height:24px">x</button></main></body></html>'
    clean_report=critic.audit_physical_layout(clean)
    assert clean_report["evidence_status"]=="STATIC_HEURISTIC_ONLY"
    assert clean_report["acceptance_status"]=="NOT_EVALUATED"
    risky_report=critic.audit_physical_layout(risky)
    kinds={item["type"] for item in risky_report["defects"]}
    assert "possible_horizontal_overflow" in kinds and "possible_substandard_touch_target" in kinds
    assert risky_report["acceptance_status"]=="REVISE_REQUIRED"
    runtime=critic.audit_runtime_react_tsx("export default function Demo() { return <button />; }")
    assert runtime["status"]=="NOT_EVALUATED" and runtime["evidence_status"]=="HARNESS_BROWSER_REQUIRED"
    assert critic.audit_runtime_interaction(clean)["status"]=="NOT_EVALUATED"
    assert critic.enable_browser is False
    motion=critic.audit_motion_ergonomics(".x { transition: all 500ms; transform: scale(0); animation: pulse 2s; } .x:hover { color:red; }")
    assert not motion["is_ergonomic"] and len(motion["defects"])>=3
    print("[SUCCESS] Static physical heuristics and harness-owned runtime contract passed.")

if __name__=="__main__":
    main()
