import os

# 1. Update PROJECT.md
with open("PROJECT.md", "r", encoding="utf-8") as f:
    proj = f.read()

protocol = """
## Mandatory Multi-Registry Release Protocol ("منتشر کن")
Whenever prompted to publish or release ("منتشر کن"), the agent must strictly execute the full 5-stage deployment:
1. **Version Bump & Skill Sync**: Update canonical version across manifests and synchronize all 6 skills.
2. **Documentation & Changelog**: Append release notes in root `CHANGELOG.md` and `packages/vibe-ui-vscode/CHANGELOG.md`. Update `README.md` / `README.fa.md` if options or architectures changed.
3. **Build & Automated Testing**: Validate versions (`python scripts/validate_versions.py`) and evals (`python evals/run_evals.py --json`).
4. **NPM & Open-VSX**: Build `packages/vibe-ui-suite` and package `vibe-ui-vscode-*.vsix`. Commit, tag (`vX.Y.Z`), push to GitHub triggering `.github/workflows/publish.yml`.
5. **Microsoft Visual Studio Marketplace**: Run `python scripts/publish_marketplace_browser.py`, connect to `https://marketplace.visualstudio.com/manage/publishers/omid-io` via Playwright MCP, open Update dialog, run `browser_run_code_unsafe(filename='run_upload.js')`, and verify status reaches "Verifying" or "Published".
"""

if "Mandatory Multi-Registry Release Protocol" not in proj:
    proj += protocol
    with open("PROJECT.md", "w", encoding="utf-8", newline="\n") as f:
        f.write(proj)
    print("PROJECT.md updated.")

# 2. Update ARCHITECTURE.md
with open("ARCHITECTURE.md", "r", encoding="utf-8") as f:
    arch = f.read()

if "Mandatory Multi-Registry Release Protocol" not in arch:
    arch += "\n---\n" + protocol
    with open("ARCHITECTURE.md", "w", encoding="utf-8", newline="\n") as f:
        f.write(arch)
    print("ARCHITECTURE.md updated.")
