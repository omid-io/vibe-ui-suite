# Vibe UI — VS Code, Cursor & Windsurf Extension
### Machine-Checkable Design Contracts, Visual Style Explorer & Mathematical WCAG Contrast Linter

[![Open-VSX Version](https://img.shields.io/open-vsx/v/omid-io/vibe-ui-vscode?color=blue&style=flat-square)](https://open-vsx.org/extension/omid-io/vibe-ui-vscode)
[![Open-VSX Downloads](https://img.shields.io/open-vsx/dt/omid-io/vibe-ui-vscode?color=green&style=flat-square&logo=eclipseche)](https://open-vsx.org/extension/omid-io/vibe-ui-vscode)
[![VS Code Marketplace Installs](https://img.shields.io/visual-studio-marketplace/i/omid-io.vibe-ui-vscode?color=blue&style=flat-square&logo=visual-studio-code)](https://marketplace.visualstudio.com/items?itemName=omid-io.vibe-ui-vscode)
[![NPM Downloads](https://img.shields.io/npm/dm/vibe-ui-suite?color=red&style=flat-square&logo=npm)](https://www.npmjs.com/package/vibe-ui-suite)
[![GitHub Stars](https://img.shields.io/github/stars/omid-io/vibe-ui-suite?style=flat-square&logo=github&color=ffb400)](https://github.com/omid-io/vibe-ui-suite)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](https://github.com/omid-io/vibe-ui-suite/blob/main/LICENSE)

The official IDE extension for **Vibe UI Suite** — an open-source deterministic design architecture and headless Chromium evaluation engine that prevents AI coding assistants (Cursor, Claude Code, Windsurf, Copilot) from generating generic, low-contrast **"AI Design Slop"**.

---

## ⚡ What is Vibe UI?

When AI agents generate frontend code, they almost always converge on the same generic template: flat gray borders, washed-out contrast, decorative purple gradients, and cramped mobile touch targets.

**Vibe UI solves this deterministically inside your editor:**
1. **26 Orthogonal Style Genomes:** Structured machine-checkable contracts spanning Monospace Terminal HUDs, Neo-Brutalism, Minimal Swiss Editorial, Specular Glassmorphism 2.0, and Quiet Luxury.
2. **Pure Mathematical Luminance Gates:** Enforces WCAG AA contrast ($L = 0.2126 R' + 0.7152 G' + 0.0722 B'$) in perceptual OKLCH color space.
3. **Tailwind CSS v4 Native:** Zero-config `@theme` token distribution via NPM (`vibe-ui-suite`).
4. **1-Click AI Workspace Injection:** Immediately injects `.cursorrules`, `CLAUDE.md`, or `.windsurfrules` into your active repository.

---

## 🚀 Key Features

### 1. 🎨 Visual Chemistry Explorer (Sidebar Panel)
Click the **Vibe UI** icon on your activity bar to open the interactive design palette:
* Browse all 26 canonical design systems with live previews.
* Copy color tokens, font stacks, spatial metrics, and Tailwind CSS component recipes with a single click.
* View machine-verified contrast ratios and forbidden pattern anti-patterns.

### 2. 🛡️ In-Editor Mathematical WCAG AA Contrast Linter
Right-click any component file (`.tsx`, `.jsx`, `.html`, `.vue`, `.svelte`) or run from the Command Palette:
* **Command:** `Vibe UI: Audit Component WCAG Contrast & Invariants`
* Audits declared background and foreground pairs against standard WCAG AA thresholds:
  * **Body text:** Minimum **4.5 : 1** contrast ratio.
  * **Headings & Large text:** Minimum **3.0 : 1** contrast ratio.
* Flags interactive click targets below the minimum **48px x 48px** accessible touch boundary.

### 3. 🤖 1-Click AI Agent Workspace Provisioning
Quickly configure your active project for autonomous AI coding:
* **Command:** `Vibe UI: Configure Workspace Adapter (Cursor / Claude Code / Windsurf)`
* Injects project-specific rules preventing AI assistants from slipping into generic styling patterns:
  * `.cursorrules` (for Cursor IDE)
  * `CLAUDE.md` (for Claude Code CLI)
  * `.windsurfrules` (for Windsurf IDE)

### 4. 🌐 Instant Link to Live Compiler Studio
* **Command:** `Vibe UI: Open Live Component Showcase`
* Opens the zero-backend interactive design compiler at [https://omid-io.github.io/vibe-ui-suite/](https://omid-io.github.io/vibe-ui-suite/) directly in an editor webview or your default browser.

---

## 💻 Available Commands

| Command | Title | Shortcut / Trigger |
| :--- | :--- | :--- |
| `vibe-ui.auditContrast` | **Audit Component WCAG Contrast & Invariants** | Editor Context Menu / Command Palette (`Ctrl+Shift+P`) |
| `vibe-ui.insertAdapter` | **Configure Workspace Adapter (Cursor / Claude / Windsurf)** | Activity Bar / Command Palette |
| `vibe-ui.openShowcase` | **Open Live Component Showcase** | Activity Bar Header / Command Palette |

---

## 📦 Installation

### From Open-VSX Registry (VSCodium, Gitpod, Cursor, Eclipse Theia):
Search for **"Vibe UI"** in your Extensions tab (`Ctrl+Shift+X`), or run:
```bash
codium --install-extension omid-io.vibe-ui-vscode
```

### From VSIX Package:
Download the latest `vibe-ui-vscode-3.1.1.vsix` from [GitHub Releases](https://github.com/omid-io/vibe-ui-suite/releases), then:
```bash
code --install-extension vibe-ui-vscode-3.1.1.vsix
```

---

## 🧩 Complete Ecosystem

* **CLI & Design Tokens (NPM):** [`vibe-ui-suite`](https://www.npmjs.com/package/vibe-ui-suite) (`npx vibe-ui-suite init`)
* **Live Design Studio:** [https://omid-io.github.io/vibe-ui-suite/](https://omid-io.github.io/vibe-ui-suite/)
* **GitHub Repository:** [https://github.com/omid-io/vibe-ui-suite](https://github.com/omid-io/vibe-ui-suite)

## ⭐ Support & Star on GitHub
If Vibe UI helps your team build cleaner, higher-contrast UIs without AI slop, please **[star the repository on GitHub](https://github.com/omid-io/vibe-ui-suite)**! Every star directly supports ongoing maintenance, dataset updates, and multi-model evaluations.

[![Star on GitHub](https://img.shields.io/badge/⭐_Star_Repository-omid--io%2Fvibe--ui--suite-blue?style=for-the-badge&logo=github)](https://github.com/omid-io/vibe-ui-suite)

---

## 📄 License

MIT © [Omid Zaferi](https://github.com/omid-io)
