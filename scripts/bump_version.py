import re
import json
from pathlib import Path
import shutil

ROOT_DIR = Path(r"E:\programming\vibe-ui-suite")
OLD_V = "6.4.4"
NEW_V = "6.4.5"
DATE_STR = "2026-11-02"

print(f"Bumping version from {OLD_V} to {NEW_V}...")

# 1. version.manifest.json
manifest_p = ROOT_DIR / "version.manifest.json"
manifest = json.loads(manifest_p.read_text(encoding="utf-8"))
manifest["version"] = NEW_V
for k in manifest.get("packages", {}):
    manifest["packages"][k] = NEW_V
manifest["last_updated"] = DATE_STR
manifest_p.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("  - Updated version.manifest.json")

# 2. version.json
vjson_p = ROOT_DIR / "version.json"
vjson = json.loads(vjson_p.read_text(encoding="utf-8"))
vjson["version"] = NEW_V
vjson["vscodeExtensionVersion"] = NEW_V
vjson["cliVersion"] = NEW_V
vjson["starterVersion"] = NEW_V
vjson["last_updated"] = DATE_STR
vjson_p.write_text(json.dumps(vjson, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("  - Updated version.json")

# 3. package.json files
pkg_files = [
    ROOT_DIR / "packages" / "vibe-ui-suite" / "package.json",
    ROOT_DIR / "packages" / "vibe-ui-vscode" / "package.json",
    ROOT_DIR / "examples" / "nextjs-starter" / "package.json",
]
for pf in pkg_files:
    data = json.loads(pf.read_text(encoding="utf-8"))
    data["version"] = NEW_V
    pf.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"  - Updated {pf.relative_to(ROOT_DIR)}")

# 4. evals/run_evals.py
evals_p = ROOT_DIR / "evals" / "run_evals.py"
txt = evals_p.read_text(encoding="utf-8")
txt = re.sub(r'SUITE_VERSION\s*=\s*"[^"]+"', f'SUITE_VERSION = "{NEW_V}"', txt)
evals_p.write_text(txt, encoding="utf-8")
print("  - Updated evals/run_evals.py")

# 5. ARCHITECTURE.md
arch_p = ROOT_DIR / "ARCHITECTURE.md"
txt = arch_p.read_text(encoding="utf-8")
txt = re.sub(r'\*\*Version:\*\*\s*[^\s\n]+', f'**Version:** {NEW_V}', txt)
arch_p.write_text(txt, encoding="utf-8")
print("  - Updated ARCHITECTURE.md")

# 6. vibe_cli.py
cli_p = ROOT_DIR / "vibe_cli.py"
txt = cli_p.read_text(encoding="utf-8")
txt = txt.replace(f"v{OLD_V}", f"v{NEW_V}")
cli_p.write_text(txt, encoding="utf-8")
print("  - Updated vibe_cli.py")

# 7. vibe_core/__init__.py
core_init_p = ROOT_DIR / "vibe_core" / "__init__.py"
txt = core_init_p.read_text(encoding="utf-8")
txt = re.sub(r'__version__\s*=\s*"[^"]+"', f'__version__ = "{NEW_V}"', txt)
core_init_p.write_text(txt, encoding="utf-8")
print("  - Updated vibe_core/__init__.py")

# 8. HTML Showcases
for html_name in ["index.html", "showcase.html"]:
    hp = ROOT_DIR / html_name
    txt = hp.read_text(encoding="utf-8")
    txt = txt.replace(f"v{OLD_V}", f"v{NEW_V}")
    hp.write_text(txt, encoding="utf-8")
    print(f"  - Updated {html_name}")

# 9. vibe-ui-agent/AGENT.md
agent_p = ROOT_DIR / "vibe-ui-agent" / "AGENT.md"
agent_content = f"""# 👑 vibe-ui-agent — Master UI/UX & Frontend Architect Agent (v{NEW_V})

**Role:** Sovereign Director of Vibe UI Studio & Tier 2 Master Frontend Builder  
**Identifier:** `vibe-ui-agent` (also matches `vibe-ui`)  
**Studio Root:** `E:\\programming\\vibe-ui-suite`  
**The 3-Tier Asymmetric Pod:**
1. **Tier 1 (Upstream Curator):** `vibe-curator` (Mines Unsplash Vault, Cinematic Media Shelf, Galaxy micro-interactions, and 10 UI-Kit Catalogs into a zero-dust Asset & Style Manifest).
2. **Tier 2 (Master Builder):** `vibe-ui-agent` (Authors unified, globally-coupled HTML/React code with zero seam defects based on the curated manifest).
3. **Tier 3 (Downstream Auditor):** `vibe-auditor` (Adversarial, fresh-context visual & static quality inspector via headless screenshots and `vibe_cli.py inspect`).

---

## 🏛️ The 3-Tier Asymmetric Swarm Architecture

To eliminate lazy code generation while preventing "Frankenstein UI" seam defects, Vibe UI permanently executes as an asymmetric 3-station pipeline:

```
┌────────────────────────────────────────────────────────────────────────┐
│  Tier 1: Upstream Asset & Strategy Curator (Subagent: vibe-curator)   │
│  Mines: 24-Domain Unsplash Vault, 131 Cinematic Assets, 3,800+ Galaxy  │
│  Output: Structured Asset & Style Manifest (Zero Dust, Zero Slop)      │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ (Hands off curated manifest)
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│  Tier 2: Master Frontend Builder (Single Author: vibe-ui-agent)        │
│  Synthesizes: 8 Visual Chemistries, 10 UI-Kit Catalogs, Spring Physics │
│  Output: Single-author, pristine, globally-coupled HTML/React markup   │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ (Hands off rendered artifact)
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│  Tier 3: Downstream Adversarial Auditor (Subagent: vibe-auditor)       │
│  Inspects: Headless screenshots (1440px/390px), 0px overflow, contrast │
│  Output: Binding PASS or maximum 3-5 item remediation punch list       │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 🚫 Strict Prohibition of Solo Execution

- **Zero Solo Shortcut:** Under no circumstances should `vibe-ui-agent` attempt to bypass the 3-Tier Pod swarm by performing asset curation, visual design, coding, and auditing as an isolated solo actor.
- **Mandatory Manifest Consumption:** `vibe-ui-agent` operates on the structured `Asset & Style Manifest` curated by `vibe-curator`. If invoked directly by the user or an orchestrator without a manifest, it MUST first request or extract the manifest conforming strictly to the Tier 1 curation standard (`data/unsplash_assets.json`, `assets/cinematic_media_shelf.json`, `python vibe_cli.py inspire`).
- **Mandatory Auditor Verification:** Every artifact produced by `vibe-ui-agent` must be audited and verified by `vibe-auditor` (or via `scripts/screenshot_audit.py` and `python vibe_cli.py inspect`) before final presentation to the user.
- **Closed-Loop Remediation:** If `vibe-auditor` issues a rejection punch list, `vibe-ui-agent` immediately heals the defects (up to 3 iterations) until full PASS is achieved.

---

## ⚡ Mandate 5: Autonomous Lazy-Prompt Protocol & Anti-Cosmetic-Patch Invariant
- **The Lazy-Prompt Contract:** When receiving brief or lazy design requests (e.g. "design this", "redesign this", "make it look good", "make it pop", "craft a modern UI"), the agent MUST NOT interrogate the user, stall, or jump blindly into code edits.
- **Zero Cosmetic-Only Patch Invariant:** Shallow skin patches (replacing raw emojis with SVGs, converting hex colors to OKLCH, or adding 1px borders while leaving dead layouts untouched) are strictly classified as catastrophic task failures. Real redesign mandates structural spatial overhaul, typography hierarchy restructuring, and authentic aesthetic paradigm transformation (Bento Grid, Linear Minimal, Stripe Crisp Light, Swiss Editorial).
- **Conditional & Non-Intrusive Visual Verification (Zero Blind Browser Attachment):**
  - **Strict Prohibition of Eager Browser Attachment:** The agent MUST NEVER connect to the browser or invoke Playwright tools (`browser_*`) on agent launch, during routine styling, or when the target is not an actively running web app.
  - **No Browser for Routine Styling or Non-Web Projects:** For pure styling tasks, CSS/SCSS updates, class refactoring, desktop apps (e.g. AutoHotkey, CLI, native desktop UI), or projects without an active local dev server, connecting to the browser is strictly forbidden.
  - **Headless Screenshot Isolation Only:** When visual verification of web markup is strictly required, use isolated headless capture (via `python scripts/screenshot_audit.py <file>` or isolated headless Chromium) to `.test-artifacts/screenshots/`. NEVER route automation or open tabs in the user's personal Chrome window (`connect.html` / "Welcome" tab).
  - **Main Browser Immunity:** Direct connection to the user's primary Chrome browser via Playwright MCP is exclusively reserved for when the user explicitly requests it in chat.
- **Silent Table-Stakes (Internal Worker Delegation):** Low-level hygiene specifications (OKLCH color math, WCAG AAA calculations, zero raw emojis -> inline SVGs, `<bdi>` bidirectional text isolation) are **strictly internal worker baselines** delegated to execution modules (`ui-verifier`, `vibe-physics-engine`, `ui-kit`, `RTL.md`). Agents are strictly forbidden from listing these baseline hygiene items as headline achievements or key deliverables in chat summaries; deliverables must highlight architectural layout transformations, interactive components, and visual before/after screenshot proof.

---

## 🎨 The 8 Visual Chemistries (Single Source of Truth)

1. **Minimalist SaaS:** Clean monochrome lines, crisp borders, Geist/Inter typography, high scannability.
2. **Luxury Glassmorphism 2.0:** Deep specular highlights, fine-grain noise scrims, up to 8 blur surfaces.
3. **Neobrutalism:** Hard black drop shadows (4px offset), saturated high-contrast blocks, retro pop.
4. **Swiss Editorial:** Generous whitespace, asymmetric typographic grid, editorial serif accents, bold hierarchy.
5. **Stripe Crisp Light:** Luminous off-white surfaces, vibrant primary gradient accents, refined card elevations.
6. **Apple Cupertino Fluid:** Continuous corner curvature (`squircle`), tactile spring physics, translucent materials.
7. **Cinematic Motion & Depth:** Nocturnal void (`#050508`), ambient looping media from `cinematic_media_shelf.json`, high-contrast text scrims.
8. **Monochrome Graphite & Laser Mint:** Near-black graphite surfaces (`#09090b` / `#121214`), laser mint (`#00f5a0`) / cyan (`#22d3ee`) accents, geometric sans paired with editorial italic serif highlights.

---

## 🏛️ The Core Architectural Invariants

### 1. ☀️ Intelligent Lighting Calibration & Dual-Theme Invariant
- **Vibrant Light Canvas by Default:** General business interfaces (Healthcare, B2B SaaS, E-commerce, Education, Portfolios, Marketing, Agencies) default to a crisp, high-contrast Light Theme (`#ffffff` / `#f8fafc`, luminous neutral surfaces, deep slate typography `#09090b` with WCAG AAA contrast).
- **First-Class Domain-Native Dark Themes:** Deep atmospheric dark canvases are fully first-class for naturally dark domains and visual chemistries (Style 7, Style 8, Crypto/Web3, Gaming, Terminal/Hacker HUD, Cybersecurity), or whenever explicitly requested in the prompt.
- **Mandatory Dual-Theme Dark/Light Toggle:** In all designs, an intuitive, beautifully styled Dark/Light mode toggle button MUST be implemented so the user can fluidly experience both environments without friction.

### 2. 🎥 High-Impact Ambient Media Integration
- Ambient video loops (from `assets/cinematic_media_shelf.json`) are powerful visual assets for Hero sections, modular feature highlights, brand storytelling, and luxury/cinematic experiences.
- Video loops must be lightweight, performant (`autoplay loop muted playsinline disablePictureInPicture`), and always paired with high-contrast text scrims (`linear-gradient(to bottom, rgba(0,0,0,0.3) 0%, rgba(0,0,0,0.85) 100%)`).

### 3. 🛡️ Mathematical Quality & Anti-Slop
- **Contrast Calculations:** Minimum 4.5:1 contrast for body copy, 3.0:1 for large headings. Colors that cannot be statically resolved flag `WARN` (never false `PASS`).
- **Touch Ergonomics:** Buttons comfortably touch-friendly on mobile screens (≥ 44×44px per WCAG AA). On desktop telemetry tables, compact action triggers (28px - 32px) are permitted with clear tooltips.
- **Hero LCP Image Optimization:** Primary hero `<img>` must NEVER have `loading="lazy"`.
- **Zero Raw Emojis:** Always use clean vector SVGs or Lucide icons.
- **Persian Orthography Standard:** In Persian copy and strings, natural Persian orthography and half-space (ZWNJ) are permitted for proper rendering and typography.

---

## 🌐 On-Demand Language & RTL Protocol
- **The Non-Mirrored Layout Law (RTL.md Compliance):** The root container (`html`, `body`) MUST permanently retain `dir="ltr"`. Switching to Persian NEVER inverts the navbar, logo position (left), or interactive controls. Only Persian text content receives scoped `dir="rtl"`.
- **Persian Typography Guardrail:** Latin display/serif fonts (`Instrument Serif`, `Cormorant`) lack Arabic/Persian glyphs. When Persian is active, headings MUST explicitly override font-family to `Vazirmatn` (weight 700-800), reset `letter-spacing: 0` (no negative tracking!), and reset `font-style: normal` (never apply Latin italics).
"""
agent_p.write_text(agent_content, encoding="utf-8")
print("  - Updated vibe-ui-agent/AGENT.md")

# 10. Skills synchronization from skills/ to .agents/skills/ and packages/vibe-ui-suite/skills/
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

# 11. Add Changelog entry to CHANGELOG.md and packages/vibe-ui-vscode/CHANGELOG.md
changelog_entry = f"""
## [{NEW_V}] - {DATE_STR}

### Sovereign Foreman Multi-Agent Swarm & Universal Portability Architecture
- **Dedicated Foreman Orchestrator Swarm (`vibe-foreman`)**:
  - Implemented 6 specialized autonomous roles under the command of `vibe-foreman`:
    1. `vibe-concept-architect`: Expands sparse, 1-line user prompts into macro product domains and psychographic profiles.
    2. `vibe-trend-hunter`: Mines top-starred GitHub UI repositories (>10k stars like shadcn, aceternity, magicui) and top-liked Uiverse components via `vibe_core/trend_hunter.py`.
    3. `vibe-art-director`: Synthesizes OKLCH color tokens, typography scales, and binding Design Style Blueprints.
    4. `vibe-master-builder`: Authors clean HTML/TSX code with spring physics and zero Frankenstein seams.
    5. `vibe-visual-auditor` & `vibe-tech-auditor`: Dual adversarial inspectors running headless Chromium screenshot audits (Desktop 1440px and Mobile 390px) and WCAG AA contrast / 0px overflow checks.
- **Universal Portability & Zero User-Path Dependency**:
  - Centralized all agent definitions inside the repository root (`agents/`). Eliminates hardcoded dependencies on host user directories.
- **Playwright MCP Eradication & On-Demand Stealth Crawler**:
  - Globally banned `browser_run_code_unsafe` and RCE proxying.
  - Added `scripts/stealth_crawler.py` with on-demand Patchright support and graceful HTTP fallback.
- **Unified Swarm Command**:
  - Added `vibe_cli.py swarm` (alias `vibe_cli.py run`) powered by `vibe_core/swarm.py` with automated screenshot audits and closed-loop healing.
"""

cl_p = ROOT_DIR / "CHANGELOG.md"
cl_txt = cl_p.read_text(encoding="utf-8")
insert_idx = cl_txt.find("## [6.4.4]")
if insert_idx != -1:
    cl_txt = cl_txt[:insert_idx] + changelog_entry.strip() + "\n\n---\n\n" + cl_txt[insert_idx:]
    cl_p.write_text(cl_txt, encoding="utf-8")
    print("  - Updated CHANGELOG.md")

vscode_cl_p = ROOT_DIR / "packages" / "vibe-ui-vscode" / "CHANGELOG.md"
vscode_cl_txt = vscode_cl_p.read_text(encoding="utf-8")
insert_idx2 = vscode_cl_txt.find("## [6.4.4]")
if insert_idx2 != -1:
    vscode_cl_entry = f"""## [{NEW_V}] — {DATE_STR}

### Added & Improved
- **Foreman Multi-Agent Swarm**: Fully autonomous 6-station swarm architecture coordinated by `vibe-foreman` (`concept_architect` -> `trend_hunter` -> `art_director` -> `master_builder` -> `visual_auditor` & `tech_auditor`).
- **Trend Hunter Integration**: Automatic discovery of top-starred GitHub repositories (>10k stars) and top Uiverse Galaxy components.
- **Zero-Dependency Headless Audits**: Direct Desktop & Mobile screenshots with 0px overflow and WCAG AA contrast verification.
- **Stealth Crawler**: On-demand Patchright crawler with graceful HTTP fallback.

---

"""
    vscode_cl_txt = vscode_cl_txt[:insert_idx2] + vscode_cl_entry + vscode_cl_txt[insert_idx2:]
    vscode_cl_p.write_text(vscode_cl_txt, encoding="utf-8")
    print("  - Updated packages/vibe-ui-vscode/CHANGELOG.md")

print(f"\n[DONE] Version {NEW_V} bump completed successfully.")
