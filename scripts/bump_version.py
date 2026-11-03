#!/usr/bin/env python3
"""
scripts/bump_version.py — Vibe UI Ecosystem Semantic Version Synchronizer
Safely bumps and synchronizes versions across all monorepo manifests, configs,
CLI binaries, MCP servers, agent specifications, and changelogs without breaking
architectural invariants.
"""

import sys
import re
import json
import shutil
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

def bump(old_v: str, new_v: str, date_str: str = "2026-11-03"):
    print(f"Bumping version from {old_v} to {new_v}...")

    # 1. version.manifest.json
    manifest_p = ROOT_DIR / "version.manifest.json"
    if manifest_p.exists():
        manifest = json.loads(manifest_p.read_text(encoding="utf-8"))
        manifest["version"] = new_v
        for k in manifest.get("packages", {}):
            manifest["packages"][k] = new_v
        manifest["last_updated"] = date_str
        manifest_p.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print("  - Updated version.manifest.json")

    # 2. version.json
    vjson_p = ROOT_DIR / "version.json"
    if vjson_p.exists():
        vjson = json.loads(vjson_p.read_text(encoding="utf-8"))
        vjson["version"] = new_v
        vjson["vscodeExtensionVersion"] = new_v
        vjson["cliVersion"] = new_v
        vjson["starterVersion"] = new_v
        vjson["last_updated"] = date_str
        vjson_p.write_text(json.dumps(vjson, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print("  - Updated version.json")

    # 3. package.json files
    pkg_files = [
        ROOT_DIR / "packages" / "vibe-ui-suite" / "package.json",
        ROOT_DIR / "packages" / "vibe-ui-vscode" / "package.json",
        ROOT_DIR / "examples" / "nextjs-starter" / "package.json",
    ]
    for pf in pkg_files:
        if pf.exists():
            data = json.loads(pf.read_text(encoding="utf-8"))
            data["version"] = new_v
            pf.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            print(f"  - Updated {pf.relative_to(ROOT_DIR)}")

    # 4. evals/run_evals.py
    evals_p = ROOT_DIR / "evals" / "run_evals.py"
    if evals_p.exists():
        txt = evals_p.read_text(encoding="utf-8")
        txt = re.sub(r'SUITE_VERSION\s*=\s*"[^"]+"', f'SUITE_VERSION = "{new_v}"', txt)
        evals_p.write_text(txt, encoding="utf-8")
        print("  - Updated evals/run_evals.py")

    # 5. ARCHITECTURE.md
    arch_p = ROOT_DIR / "ARCHITECTURE.md"
    if arch_p.exists():
        txt = arch_p.read_text(encoding="utf-8")
        txt = re.sub(r'\*\*Version:\*\*\s*[^\s\n]+', f'**Version:** {new_v}', txt)
        arch_p.write_text(txt, encoding="utf-8")
        print("  - Updated ARCHITECTURE.md")

    # 6. vibe_cli.py
    cli_p = ROOT_DIR / "vibe_cli.py"
    if cli_p.exists():
        txt = cli_p.read_text(encoding="utf-8")
        txt = txt.replace(f"v{old_v}", f"v{new_v}")
        txt = txt.replace(f"Suite v{old_v}", f"Suite v{new_v}")
        cli_p.write_text(txt, encoding="utf-8")
        print("  - Updated vibe_cli.py")

    # 7. vibe_core/__init__.py
    core_init_p = ROOT_DIR / "vibe_core" / "__init__.py"
    if core_init_p.exists():
        txt = core_init_p.read_text(encoding="utf-8")
        txt = re.sub(r'__version__\s*=\s*"[^"]+"', f'__version__ = "{new_v}"', txt)
        core_init_p.write_text(txt, encoding="utf-8")
        print("  - Updated vibe_core/__init__.py")

    # 8. HTML Showcases
    for html_name in ["index.html", "showcase.html"]:
        hp = ROOT_DIR / html_name
        if hp.exists():
            txt = hp.read_text(encoding="utf-8")
            txt = txt.replace(f"v{old_v}", f"v{new_v}")
            hp.write_text(txt, encoding="utf-8")
            print(f"  - Updated {html_name}")

    # 9. packages/vibe-ui-suite/src/cli.ts and mcp.ts
    ts_cli_p = ROOT_DIR / "packages" / "vibe-ui-suite" / "src" / "cli.ts"
    if ts_cli_p.exists():
        txt = ts_cli_p.read_text(encoding="utf-8")
        txt = re.sub(r"const VERSION = '[^']+';", f"const VERSION = '{new_v}';", txt)
        ts_cli_p.write_text(txt, encoding="utf-8")
        print("  - Updated packages/vibe-ui-suite/src/cli.ts")

    mcp_p = ROOT_DIR / "packages" / "vibe-ui-suite" / "src" / "mcp.ts"
    if mcp_p.exists():
        txt = mcp_p.read_text(encoding="utf-8")
        txt = re.sub(r"const SERVER_VERSION = '[^']+';", f"const SERVER_VERSION = '{new_v}';", txt)
        mcp_p.write_text(txt, encoding="utf-8")
        print("  - Updated packages/vibe-ui-suite/src/mcp.ts")

    # 10. Local plugin.json
    plugin_p = ROOT_DIR / ".agents" / "plugins" / "vibe-ui" / "plugin.json"
    if plugin_p.exists():
        p_data = json.loads(plugin_p.read_text(encoding="utf-8"))
        p_data["version"] = new_v
        plugin_p.write_text(json.dumps(p_data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print("  - Updated .agents/plugins/vibe-ui/plugin.json")

    # 11. Installers
    sh_p = ROOT_DIR / "scripts" / "install.sh"
    if sh_p.exists():
        txt = sh_p.read_text(encoding="utf-8")
        txt = re.sub(r'VERSION="v?[^"]+"', f'VERSION="v{new_v}"', txt)
        sh_p.write_text(txt, encoding="utf-8")
        print("  - Updated scripts/install.sh")

    ps1_p = ROOT_DIR / "scripts" / "install.ps1"
    if ps1_p.exists():
        txt = ps1_p.read_text(encoding="utf-8")
        txt = re.sub(r'\[string\]\$Version = "v?[^"]+"', f'[string]$Version = "v{new_v}"', txt)
        ps1_p.write_text(txt, encoding="utf-8")
        print("  - Updated scripts/install.ps1")

    # 12. vibe_core/trend_hunter.py User-Agent
    th_p = ROOT_DIR / "vibe_core" / "trend_hunter.py"
    if th_p.exists():
        txt = th_p.read_text(encoding="utf-8")
        txt = re.sub(r'Vibe-UI-TrendHunter/[^\s",]+', f'Vibe-UI-TrendHunter/{new_v}', txt)
        th_p.write_text(txt, encoding="utf-8")
        print("  - Updated vibe_core/trend_hunter.py")

    # 13. Update version headers in vibe-ui-agent/AGENT.md (preserving full invariant body)
    agent_p = ROOT_DIR / "vibe-ui-agent" / "AGENT.md"
    if agent_p.exists():
        txt = agent_p.read_text(encoding="utf-8")
        txt = re.sub(r'\(v\d+\.\d+\.\d+\)', f'(v{new_v})', txt)
        agent_p.write_text(txt, encoding="utf-8")
        print("  - Updated version in vibe-ui-agent/AGENT.md")

    # 14. Skills synchronization
    skills_src = ROOT_DIR / "skills"
    skills_dest1 = ROOT_DIR / ".agents" / "skills"
    skills_dest2 = ROOT_DIR / "packages" / "vibe-ui-suite" / "skills"

    for s in ["ui-kit", "ui-verifier", "vibe-physics-engine", "visual-chemistry-engine", "autonomous-intent-expander", "conversion-copy-engine"]:
        src = skills_src / s
        if src.exists():
            d1 = skills_dest1 / s
            d2 = skills_dest2 / s
            d1.mkdir(parents=True, exist_ok=True)
            d2.mkdir(parents=True, exist_ok=True)
            for f in src.rglob("*"):
                if f.is_file():
                    rel = f.relative_to(src)
                    t1 = d1 / rel
                    t2 = d2 / rel
                    t1.parent.mkdir(parents=True, exist_ok=True)
                    t2.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(f, t1)
                    shutil.copy2(f, t2)
    print("  - Synchronized skills to .agents/skills and packages/vibe-ui-suite/skills")

    # 15. Agent definitions synchronization
    agents_src = ROOT_DIR / "agents"
    agents_dest_plugin = ROOT_DIR / ".agents" / "plugins" / "vibe-ui" / "agents"
    agents_dest_claude = ROOT_DIR / ".claude" / "agents"
    agents_dest_pkg = ROOT_DIR / "packages" / "vibe-ui-suite" / "agents"

    # Ensure vibe-ui-agent.md is updated from vibe-ui-agent/AGENT.md
    if agent_p.exists():
        shutil.copy2(agent_p, agents_src / "vibe-ui-agent.md")

    for dest_dir in [agents_dest_plugin, agents_dest_claude, agents_dest_pkg]:
        dest_dir.mkdir(parents=True, exist_ok=True)
        # Clean obsolete files in destination
        for existing in dest_dir.glob("*.md"):
            if not (agents_src / existing.name).exists():
                existing.unlink()
        # Copy canonical agents
        for f in agents_src.glob("*.md"):
            shutil.copy2(f, dest_dir / f.name)
    print("  - Synchronized agents across .agents/plugins/vibe-ui, .claude, and packages/vibe-ui-suite")

    print(f"\n[DONE] Version {new_v} bump completed successfully.")

if __name__ == "__main__":
    current_manifest = json.loads((ROOT_DIR / "version.manifest.json").read_text(encoding="utf-8"))
    canonical_v = current_manifest["version"]
    if len(sys.argv) >= 2:
        target_v = sys.argv[1]
        bump(canonical_v, target_v)
    else:
        print(f"Current canonical version is {canonical_v}. Specify target version to bump: python bump_version.py <new_version>")
