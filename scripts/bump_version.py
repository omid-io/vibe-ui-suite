#!/usr/bin/env python3
"""
scripts/bump_version.py — Vibe UI Ecosystem Semantic Version Synchronizer
Safely bumps and synchronizes versions across all monorepo manifests, configs,
CLI binaries, MCP servers, agent specifications, and changelogs without breaking
architectural invariants.

Also strips unnecessary version numbers from agent descriptions/titles and ensures
seamless synchronization with global Antigravity custom-agents.
"""

import sys
import re
import json
import shutil
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

def clean_agent_text(text: str) -> str:
    """Removes version annotations from agent descriptions and headers."""
    text = re.sub(r'\(v\d+\.\d+(\.\d+)?\):\s*', '', text)
    text = re.sub(r'\(Vibe UI Suite v\d+\.\d+(\.\d+)?\):\s*', '', text)
    text = re.sub(r'\(v\d+\.\d+(\.\d+)?\)', '', text)
    text = re.sub(r'\(Vibe UI Suite v\d+\.\d+(\.\d+)?\)', '', text)
    text = re.sub(r'\s+:', ':', text)
    text = re.sub(r'# 👑 vibe-ui-agent — Master UI/UX & Frontend Architect Agent(\s*\(v[^\)]+\))?', '# 👑 vibe-ui-agent — Master UI/UX & Frontend Architect Agent', text)
    return text

def ensure_invariant_in_agent(text: str) -> str:
    """Guarantees Zero-Unsolicited-Version Invariant is present in vibe-ui-agent."""
    invariant_block = """### 2. Zero-Unsolicited-Version Invariant (No Version Spam)
- `vibe-ui-agent` and all swarm workers **MUST NEVER mention, announce, or quote version numbers** (e.g. "v6.5.0", "نسخه 6.4.2") in greetings, chat introductions, status banners, or routine dialogues.
- Versions belong exclusively in machine-readable manifests (`version.manifest.json`, `package.json`), CLI `--version` flags, and release changelogs.
- Never state or recite the version unless the user explicitly asks a direct question regarding the version (e.g. "نسخه چند است؟" or "what version is running?")."""

    if "Zero-Unsolicited-Version Invariant" not in text:
        target = "## 🚫 The Absolute Invariant: Zero Direct Code Writing"
        replacement = "## 🚫 The Invariants\n\n### 1. The Absolute Invariant: Zero Direct Code Writing"
        if target in text:
            text = text.replace(target, replacement)
        
        insert_after = "- **Zero Solo Shortcut:** Under no circumstances should `vibe-ui-agent` bypass the multi-agent swarm by performing curation, styling, coding, and auditing as an isolated solo actor."
        if insert_after in text:
            text = text.replace(insert_after, f"{insert_after}\n\n{invariant_block}")
    return text

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

    # 13. Update data and manifest JSON files
    for jf in ["assets/curated_webp/manifest.json", "data/design_vault/archetypes.json", "data/unsplash_assets.json"]:
        jp = ROOT_DIR / jf
        if jp.exists():
            d = json.loads(jp.read_text(encoding="utf-8"))
            if "version" in d:
                d["version"] = new_v
                jp.write_text(json.dumps(d, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
                print(f"  - Updated {jf}")

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

    # 16. Agent definitions sanitization & multi-destination synchronization
    agent_p = ROOT_DIR / "vibe-ui-agent" / "AGENT.md"
    agents_src = ROOT_DIR / "agents"
    agents_dest_plugin = ROOT_DIR / ".agents" / "plugins" / "vibe-ui" / "agents"
    agents_dest_claude = ROOT_DIR / ".claude" / "agents"
    agents_dest_pkg = ROOT_DIR / "packages" / "vibe-ui-suite" / "agents"
    antigravity_custom_agents = Path.home() / ".gemini" / "config" / "plugins" / "custom-agents" / "agents"

    # Sanitize vibe-ui-agent/AGENT.md (Remove version spam & guarantee invariant)
    if agent_p.exists():
        raw_agent = agent_p.read_text(encoding="utf-8")
        cleaned_agent = clean_agent_text(raw_agent)
        cleaned_agent = ensure_invariant_in_agent(cleaned_agent)
        agent_p.write_text(cleaned_agent, encoding="utf-8")
        (agents_src / "vibe-ui-agent.md").write_text(cleaned_agent, encoding="utf-8")

    # Sanitize all agent files in agents/
    for af in agents_src.glob("*.md"):
        txt = af.read_text(encoding="utf-8")
        af.write_text(clean_agent_text(txt), encoding="utf-8")

    canonical_agent_names = [f.name for f in agents_src.glob("*.md")]
    obsolete_agents = ["vibe-curator.md", "vibe-auditor.md"]

    target_agent_dirs = [agents_dest_plugin, agents_dest_claude, agents_dest_pkg]
    if antigravity_custom_agents.exists():
        target_agent_dirs.append(antigravity_custom_agents)

    for dest_dir in target_agent_dirs:
        dest_dir.mkdir(parents=True, exist_ok=True)
        # Remove obsolete Vibe agents
        for obs in obsolete_agents:
            obs_f = dest_dir / obs
            if obs_f.exists():
                obs_f.unlink()
        # Copy canonical agents
        for name in canonical_agent_names:
            src_f = agents_src / name
            if src_f.exists():
                shutil.copy2(src_f, dest_dir / name)

    print("  - Sanitized and synchronized agents across .agents/plugins, .claude, packages, and Antigravity custom-agents")
    print(f"\n[DONE] Version {new_v} bump and full synchronization completed successfully.")

if __name__ == "__main__":
    current_manifest = json.loads((ROOT_DIR / "version.manifest.json").read_text(encoding="utf-8"))
    canonical_v = current_manifest["version"]
    if len(sys.argv) >= 2:
        target_v = sys.argv[1]
        bump(canonical_v, target_v)
    else:
        print(f"Current canonical version is {canonical_v}. Specify target version to bump: python bump_version.py <new_version>")
