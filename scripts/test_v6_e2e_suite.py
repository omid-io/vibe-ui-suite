#!/usr/bin/env python3
"""Browser-agnostic regression checks for the harness-native verification architecture."""
from pathlib import Path
import sys,tempfile
ROOT=Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
from vibe_core.browser_evidence import SCHEMA_VERSION,build_browser_request
from vibe_core.physical_critic import PhysicalCritic
from vibe_core.verifier import VerificationEngine

def main():
    failures=[]
    def check(condition,message):
        if not condition: failures.append(message); print(f"[FAIL] {message}")
        else: print(f"[PASS] {message}")
    requirements=(ROOT/"requirements.txt").read_text(encoding="utf-8").lower()
    paths=[ROOT/"vibe_core"/"swarm.py",ROOT/"vibe_core"/"physical_critic.py",ROOT/"vibe_core"/"verifier.py",ROOT/"vibe_cli.py",ROOT/".github"/"workflows"/"ci.yml"]
    source="\n".join(p.read_text(encoding="utf-8") for p in paths).lower()
    check("playwright" not in requirements,"Browser driver is not a Python dependency")
    check("playwright" not in source and "sync_playwright" not in source,"Core, CLI and CI do not import or launch browser automation")
    with tempfile.TemporaryDirectory() as temp:
        artifact=Path(temp)/"page.html"
        artifact.write_text("<html><body><h1>Browser evidence</h1></body></html>",encoding="utf-8")
        request=build_browser_request(artifact,Path(temp)/".vibe"/"request.json")
        check(request["schema_version"]==SCHEMA_VERSION,"Request uses the versioned browser evidence contract")
        check([v["width"] for v in request["required_viewports"]]==[390,768,1440],"Request requires mobile, tablet and desktop")
    html='<html><head><meta name="viewport" content="width=device-width"><style>body{background:#fff;color:#111}:focus-visible{outline:2px solid}</style></head><body><button>Go</button></body></html>'
    strict=VerificationEngine().verify_html(html,mode="strict")
    notes=[v for v in strict["evidence_records"] if v.get("check_name")=="Harness Browser Evidence"]
    check(bool(notes) and notes[0]["status"]=="WARN","Strict compatibility mode requests harness evidence without launching a browser")
    report=PhysicalCritic(enable_browser=True).audit_physical_layout("<html><body>static</body></html>")
    check(report["evidence_status"]=="STATIC_HEURISTIC_ONLY","Static heuristics cannot claim rendered geometry acceptance")
    if failures: print(f"\n[FAIL] {len(failures)} regression check(s) failed"); return 1
    print("\n[SUCCESS] Harness-native verification regression suite passed."); return 0
if __name__=="__main__": sys.exit(main())
