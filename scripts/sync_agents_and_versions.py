#!/usr/bin/env python3
"""
scripts/sync_agents_and_versions.py
Synchronizes all agent specifications across internal and global directories,
removes all unsolicited version numbers from agent metadata/titles,
and cleans up obsolete agent files.
"""

import os
import re
import shutil
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
AGENTS_SRC = ROOT_DIR / "agents"
AGENT_MD = ROOT_DIR / "vibe-ui-agent" / "AGENT.md"

DEST_DIRS = [
    ROOT_DIR / ".agents" / "plugins" / "vibe-ui" / "agents",
    ROOT_DIR / ".claude" / "agents",
    ROOT_DIR / "packages" / "vibe-ui-suite" / "agents",
    Path.home() / ".gemini" / "config" / "plugins" / "custom-agents" / "agents"
]

CANONICAL_AGENTS = [
    "vibe-ui-agent.md",
    "vibe-concept-architect.md",
    "vibe-trend-hunter.md",
    "vibe-art-director.md",
    "vibe-master-builder.md",
    "vibe-visual-auditor.md",
    "vibe-tech-auditor.md"
]

OBSOLETE_VIBE_AGENTS = [
    "vibe-curator.md",
    "vibe-auditor.md"
]

def clean_agent_text(text: str) -> str:
    # Remove version from description: "... (v6.5.0): ..." -> "...: ..."
    text = re.sub(r'\(v\d+\.\d+(\.\d+)?\):\s*', '', text)
    text = re.sub(r'\(Vibe UI Suite v\d+\.\d+(\.\d+)?\):\s*', '', text)
    text = re.sub(r'\(v\d+\.\d+(\.\d+)?\)', '', text)
    text = re.sub(r'\(Vibe UI Suite v\d+\.\d+(\.\d+)?\)', '', text)
    # Remove extra spaces before colon or at end of title
    text = re.sub(r'\s+:', ':', text)
    text = re.sub(r'# 👑 vibe-ui-agent — Master UI/UX & Frontend Architect Agent(\s*\(v[^\)]+\))?', '# 👑 vibe-ui-agent — Master UI/UX & Frontend Architect Agent', text)
    return text

def ensure_invariant_in_agent(text: str) -> str:
    invariant_block = """### 2. Zero-Unsolicited-Version Invariant (No Version Spam)
- `vibe-ui-agent` and all swarm workers **MUST NEVER mention, announce, or quote version numbers** (e.g. "v6.5.0", "نسخه 6.4.2") in greetings, chat introductions, status banners, or routine dialogues.
- Versions belong exclusively in machine-readable manifests (`version.manifest.json`, `package.json`), CLI `--version` flags, and release changelogs.
- Never state or recite the version unless the user explicitly asks a direct question regarding the version (e.g. "نسخه چند است؟" or "what version is running?")."""

    if "Zero-Unsolicited-Version Invariant" not in text:
        target = "## 🚫 The Absolute Invariant: Zero Direct Code Writing"
        replacement = f"## 🚫 The Invariants\n\n### 1. The Absolute Invariant: Zero Direct Code Writing"
        if target in text:
            text = text.replace(target, replacement)
        
        # Insert after Zero Direct Code Writing block
        insert_after = "- **Zero Solo Shortcut:** Under no circumstances should `vibe-ui-agent` bypass the multi-agent swarm by performing curation, styling, coding, and auditing as an isolated solo actor."
        if insert_after in text:
            text = text.replace(insert_after, f"{insert_after}\n\n{invariant_block}")
    return text

def main():
    print("[INFO] Cleaning and synchronizing Vibe UI agents...")
    
    # 1. Update vibe-ui-agent/AGENT.md
    if AGENT_MD.exists():
        raw = AGENT_MD.read_text(encoding="utf-8")
        cleaned = clean_agent_text(raw)
        cleaned = ensure_invariant_in_agent(cleaned)
        AGENT_MD.write_text(cleaned, encoding="utf-8")
        print("  [OK] Updated vibe-ui-agent/AGENT.md (stripped versions & added Zero-Unsolicited-Version Invariant)")
        # Copy to agents/vibe-ui-agent.md
        (AGENTS_SRC / "vibe-ui-agent.md").write_text(cleaned, encoding="utf-8")
        print("  [OK] Updated agents/vibe-ui-agent.md")

    # 2. Clean all files in agents/
    for agent_file in AGENTS_SRC.glob("*.md"):
        txt = agent_file.read_text(encoding="utf-8")
        cleaned = clean_agent_text(txt)
        agent_file.write_text(cleaned, encoding="utf-8")

    # 3. Synchronize to destinations
    for dest in DEST_DIRS:
        if not dest.exists():
            dest.mkdir(parents=True, exist_ok=True)
        print(f"  [SYNC] Synchronizing to {dest}...")
        
        # Remove obsolete Vibe agents
        for obs in OBSOLETE_VIBE_AGENTS:
            obs_path = dest / obs
            if obs_path.exists():
                obs_path.unlink()
                print(f"    - Removed obsolete {obs} from {dest.name}")

        # Copy canonical agents
        for agent_name in CANONICAL_AGENTS:
            src = AGENTS_SRC / agent_name
            if src.exists():
                shutil.copy2(src, dest / agent_name)
                print(f"    + Synced {agent_name}")

    print("[SUCCESS] All agent definitions sanitized and synchronized.")

if __name__ == "__main__":
    main()
