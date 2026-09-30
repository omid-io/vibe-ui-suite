# 🚀 Maintainer Release & Extension Deployment Protocol

> **Official operational standard for releasing Vibe UI Suite packages, VS Code / Cursor extensions, and multi-registry sync.**

---

## 🏛️ Immutable Package Architecture: Flagship `vibe-ui-suite`
- All design tokens, CLI binaries (`vibe-ui-suite` and `vibe-ui`), Tailwind CSS v4 `@theme` integrations, and React 19 recipes are published exclusively under **`vibe-ui-suite`**.
- Published to NPM via:
  ```bash
  cd packages/vibe-ui-suite
  node build.js
  npm publish --access public
  ```

---

## ⚡ Extension Update Checklist ("افزونه‌ها رو آپدیت کن")

Whenever the user instructs to update the extensions, execute this 4-step deployment cycle without omitting any target:

### Step 1: Bump & Document Extension Changelog
1. Bump `version` in `packages/vibe-ui-vscode/package.json` to canonical release version.
2. Document all user-facing changes in `packages/vibe-ui-vscode/CHANGELOG.md` under `[x.y.z]`.
3. Synchronize `CHANGELOG.md` at repository root.
4. Compile extension bundle:
   ```bash
   cd packages/vibe-ui-vscode
   node build.js
   npx @vscode/vsce package --no-git-tag-version
   ```
   *(Produces `vibe-ui-vscode-{version}.vsix` certified with `<GalleryFlags>Public</GalleryFlags>`)*

### Step 2: Publish Flagship NPM Package (`vibe-ui-suite`)
1. Sync `packages/vibe-ui-suite/package.json` to canonical version.
2. Build and publish:
   ```bash
   cd packages/vibe-ui-suite
   node build.js
   npm publish --access public
   ```

### Step 3: Publish to Open-VSX Registry
1. Automated via GitHub Actions workflow (`.github/workflows/publish.yml`) using `OPENVSX_TOKEN` secret:
   ```bash
   gh workflow run publish.yml
   ```
2. Or via local CLI (if token available):
   ```bash
   npx --yes ovsx publish packages/vibe-ui-vscode/vibe-ui-vscode-{version}.vsix -p <OPENVSX_TOKEN>
   ```

### Step 4: Zero-Token Visual Studio Marketplace Deployment
No Personal Access Token (PAT) required. Uses the user's active Chrome publisher session on Microsoft Visual Studio Marketplace:
1. Ensure the user's Chrome is on: `https://marketplace.visualstudio.com/manage/publishers/omid-io`
2. Open the Update dialog: Click `More Actions...` () next to `Vibe UI Studio & Contrast Gate` -> `Update`.
3. Run the automated script:
   ```bash
   python scripts/publish_marketplace_browser.py
   ```
4. In Antigravity main chat, execute:
   ```python
   call_mcp_tool(
       ServerName="playwright",
       ToolName="browser_run_code_unsafe",
       Arguments={"filename": "run_upload.js"}
   )
   ```
   *The script mounts the VSIX into memory, populates the file input via DOM `DataTransfer`, dispatches React synthetic `onChange`, and auto-clicks `Upload`.*
5. Confirm Microsoft verification status: `4.x.xVerifying4.y.y` -> Published.
