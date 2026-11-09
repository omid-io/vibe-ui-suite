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

> [!NOTE]
> **Consolidated Architecture: `@omid-io/tokens` Eliminated**  
> The legacy `packages/tokens` package has been completely deleted and consolidated directly into `packages/vibe-ui-suite`. All CLI binaries, tokens, recipes, and TypeScript typings are compiled and published solely from `vibe-ui-suite`.

---

## ⚡ Extension & Monorepo Release Checklist ("افزونه ها رو آپدیت کن" / "منتشر کن")

Whenever the user instructs to publish or update releases, execute this 5-step deployment cycle without omitting any target:

### Step 1: Bump & Document Changelog
1. Bump canonical version across manifests (`version.manifest.json`, `version.json`, `packages/vibe-ui-suite/package.json`, `packages/vibe-ui-vscode/package.json`).
2. Document all user-facing changes in `CHANGELOG.md` and `packages/vibe-ui-vscode/CHANGELOG.md` under `[x.y.z]`.
3. Synchronize skills to `.agents/skills` and `packages/vibe-ui-suite/skills`.
4. Synchronize agent definitions to `agents/`, `.agents/plugins/vibe-ui/agents/`, `.claude/agents/`, and `packages/vibe-ui-suite/agents/`.
5. Compile extension bundle:
   ```bash
   cd packages/vibe-ui-vscode
   node build.js
   npx @vscode/vsce package --no-git-tag-version
   ```
   *(Produces `vibe-ui-vscode-{version}.vsix` certified with `<GalleryFlags>Public</GalleryFlags>`)*

### Step 2: Mandatory Pre-Release Adversarial Inspector Agent Gate
- **Zero-Regression Law:** Dispatch an independent Inspector/Auditor Agent to perform a full diff audit against the previous release.
- **Verification Criteria:**
  1. No regressions or conflicts introduced by new features or CLI commands against existing components, templates, or legacy workflows.
  2. 100% pass on `python scripts/validate_versions.py` and `python evals/run_evals.py --json`.
  3. Gitleaks scan (`E:\programming\Tools\gitleaks\gitleaks.exe`) yields 0 leaks.
- *Publishing is strictly blocked until the Inspector Agent returns a definitive PASS verdict.*

### Step 3: Publish Flagship NPM Package (`vibe-ui-suite`)
1. Sync `packages/vibe-ui-suite/package.json` to canonical version.
2. Build and publish:
   ```bash
   cd packages/vibe-ui-suite
   node build.js
   npm publish --access public
   ```

### Step 4: Publish to Open-VSX Registry
1. Automated via GitHub Actions workflow (`.github/workflows/publish.yml`) using `OPENVSX_TOKEN` secret:
   ```bash
   gh workflow run publish.yml
   ```
2. Or via local CLI (if token available):
   ```bash
   npx --yes ovsx publish packages/vibe-ui-vscode/vibe-ui-vscode-{version}.vsix -p <OPENVSX_TOKEN>
   ```

### Step 5: Manual Visual Studio Marketplace Deployment
No Personal Access Token (PAT) is required for the dashboard upload. Use any browser already available in the active AI harness; this repository does not install, launch, or automate a browser.
1. Open the publisher dashboard: `https://marketplace.visualstudio.com/manage/publishers/omid-io`
2. Open the Update dialog: Click `More Actions...` () next to `Vibe UI Studio & Contrast Gate` -> `Update`.
3. Upload the generated VSIX through the dashboard's file picker.
4. Confirm Microsoft verification status reaches `Verifying` and then `Published`.
