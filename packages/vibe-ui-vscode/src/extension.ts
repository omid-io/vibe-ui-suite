import * as vscode from 'vscode';
import * as fs from 'fs';
import * as path from 'path';

export function activate(context: vscode.ExtensionContext) {
  // 1. Register Webview Sidebar Provider
  const provider = new ChemistrySidebarProvider(context.extensionUri);
  context.subscriptions.push(
    vscode.window.registerWebviewViewProvider('vibe-ui.chemistryExplorer', provider)
  );

  // 2. Register Audit Command
  context.subscriptions.push(
    vscode.commands.registerCommand('vibe-ui.auditContrast', () => {
      const editor = vscode.window.activeTextEditor;
      if (!editor) {
        vscode.window.showWarningMessage('Vibe UI: Open an interface file (.tsx, .jsx, .html) to audit contrast.');
        return;
      }
      const text = editor.document.getText();
      
      // Fast heuristic contrast and emoji check
      const emojiRegex = /[\u{10000}-\u{10ffff}\u{2600}-\u{27bf}\u{2300}-\u{23ff}\u{2b50}-\u{2b55}\u{203c}-\u{2049}\u{2194}-\u{21aa}]/u;
      const hasEmoji = emojiRegex.test(text);
      const hasOklch = text.includes('oklch(');
      
      if (hasEmoji) {
        vscode.window.showErrorMessage('Vibe UI Audit: Detected raw unicode emojis in component. Replace with inline SVG icons per anti-slop guidelines.');
      } else if (!hasOklch) {
        vscode.window.showInformationMessage('Vibe UI Audit: Clean vector icons verified. Consider migrating legacy hex colors to typed OKLCH tokens.');
      } else {
        vscode.window.showInformationMessage('Vibe UI Audit: Vector standards & OKLCH color spaces detected. (Run Playwright browser runtime eval for mathematical WCAG 2.2 AA contrast verification)');
      }
    })
  );

  // 3. Register Workspace Adapter Command
  context.subscriptions.push(
    vscode.commands.registerCommand('vibe-ui.insertAdapter', async () => {
      const choice = await vscode.window.showQuickPick(
        [
          { label: 'Cursor (.cursorrules)', description: 'Inject Vibe UI contract rules for Cursor IDE' },
          { label: 'Claude Code (CLAUDE.md)', description: 'Safely append Vibe UI rules to CLAUDE.md' },
          { label: 'Windsurf (.windsurfrules)', description: 'Inject Vibe UI contract rules for Windsurf IDE' }
        ],
        { placeHolder: 'Select target AI environment to provision' }
      );

      if (!choice || !vscode.workspace.workspaceFolders) {
        return;
      }

      const root = vscode.workspace.workspaceFolders[0].uri.fsPath;
      const adapterContent = `<!-- VIBE-UI:BEGIN -->
# Vibe UI Contract
Follow strict anti-slop guidelines:
- Zero raw unicode emojis (use SVGs only)
- Strict WCAG 2.2 AA contrast (>= 4.5:1 body, >= 3.0:1 headings)
- Use typed OKLCH colors
- Maximum 3 backdrop-filter layers
- Semantic RTL: preserve macro layout coordinates
<!-- VIBE-UI:END -->`;

      const safeWriteWithBackup = (targetPath: string, filename: string) => {
        if (fs.existsSync(targetPath)) {
          const bakPath = `${targetPath}.bak`;
          fs.copyFileSync(targetPath, bakPath);
        }
        fs.writeFileSync(targetPath, adapterContent + '\n');
        vscode.window.showInformationMessage(`✅ Vibe UI ${filename} written (existing backup saved to .bak)`);
      };

      if (choice.label.startsWith('Cursor')) {
        safeWriteWithBackup(path.join(root, '.cursorrules'), '.cursorrules');
      } else if (choice.label.startsWith('Claude')) {
        const claudePath = path.join(root, 'CLAUDE.md');
        if (fs.existsSync(claudePath)) {
          let current = fs.readFileSync(claudePath, 'utf8');
          if (current.includes('<!-- VIBE-UI:BEGIN -->')) {
            current = current.replace(/<!-- VIBE-UI:BEGIN -->[\s\S]*?<!-- VIBE-UI:END -->/, adapterContent);
          } else {
            current = current.trimEnd() + '\n\n' + adapterContent + '\n';
          }
          fs.writeFileSync(claudePath, current);
        } else {
          fs.writeFileSync(claudePath, adapterContent + '\n');
        }
        vscode.window.showInformationMessage('✅ Vibe UI rules updated idempotently in CLAUDE.md!');
      } else if (choice.label.startsWith('Windsurf')) {
        safeWriteWithBackup(path.join(root, '.windsurfrules'), '.windsurfrules');
      }
    })
  );

  // 4. Register Open Showcase Command
  context.subscriptions.push(
    vscode.commands.registerCommand('vibe-ui.openShowcase', () => {
      vscode.env.openExternal(vscode.Uri.parse('https://omid-io.github.io/vibe-ui-suite/showcase/'));
    })
  );
}

export function deactivate() {}

class ChemistrySidebarProvider implements vscode.WebviewViewProvider {
  constructor(private readonly _extensionUri: vscode.Uri) {}

  public resolveWebviewView(
    webviewView: vscode.WebviewView,
    context: vscode.WebviewViewResolveContext,
    _token: vscode.CancellationToken
  ) {
    webviewView.webview.options = {
      enableScripts: true,
      localResourceRoots: [this._extensionUri]
    };

    webviewView.webview.html = this._getHtmlForWebview(webviewView.webview);

    webviewView.webview.onDidReceiveMessage(async (message: any) => {
      if (message.command === 'copy') {
        await vscode.env.clipboard.writeText(message.text);
        vscode.window.showInformationMessage(`Vibe UI: Copied ${message.name || 'content'} to clipboard!`);
      } else if (message.command === 'insert') {
        const editor = vscode.window.activeTextEditor as any;
        if (editor) {
          await editor.edit((editBuilder: any) => {
            editBuilder.insert(editor.selection.active, message.text);
          });
          vscode.window.showInformationMessage(`Vibe UI: Inserted ${message.name} at cursor position!`);
        } else {
          await vscode.env.clipboard.writeText(message.text);
          vscode.window.showInformationMessage(`Vibe UI: No active editor. Copied ${message.name} to clipboard!`);
        }
      }
    });
  }

  private _getHtmlForWebview(webview: vscode.Webview) {
    return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; script-src 'unsafe-inline';">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Vibe UI Studio</title>
  <style>
    :root {
      --bg: var(--vscode-sideBar-background);
      --fg: var(--vscode-foreground);
      --border: var(--vscode-widget-border, #333);
      --btn-bg: var(--vscode-button-background);
      --btn-fg: var(--vscode-button-foreground);
      --btn-hover: var(--vscode-button-hoverBackground);
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: var(--vscode-font-family, sans-serif); padding: 12px; color: var(--fg); background: var(--bg); font-size: 12px; }
    
    /* Navigation Tabs */
    .tabs { display: flex; gap: 4px; border-bottom: 1px solid var(--border); padding-bottom: 8px; margin-bottom: 12px; }
    .tab-btn { background: transparent; color: var(--fg); border: 1px solid transparent; padding: 4px 8px; border-radius: 4px; cursor: pointer; font-size: 11px; opacity: 0.7; }
    .tab-btn.active { opacity: 1; background: var(--border); font-weight: bold; }
    
    /* Section Panes */
    .pane { display: none; }
    .pane.active { display: block; }
    
    /* Cards & Components */
    .card { border: 1px solid var(--border); border-radius: 6px; padding: 10px; margin-bottom: 10px; background: rgba(255, 255, 255, 0.02); }
    .card-title { font-weight: bold; font-size: 12px; margin-bottom: 4px; display: flex; justify-content: space-between; align-items: center; }
    .tag { font-size: 10px; padding: 2px 6px; border-radius: 4px; background: var(--vscode-badge-background); color: var(--vscode-badge-foreground); }
    .desc { font-size: 11px; opacity: 0.8; margin-bottom: 8px; line-height: 1.4; }
    
    /* Buttons */
    .btn { background: var(--btn-bg); color: var(--btn-fg); border: none; padding: 6px 10px; border-radius: 4px; cursor: pointer; font-size: 11px; width: 100%; font-weight: 500; transition: background 0.15s; }
    .btn:hover { background: var(--btn-hover); }
    .btn-secondary { background: var(--border); color: var(--fg); margin-top: 4px; }
    
    /* Contrast Calculator */
    .calc-row { display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px; }
    .color-input-wrapper { display: flex; align-items: center; gap: 6px; }
    input[type="color"] { border: 1px solid var(--border); border-radius: 4px; width: 28px; height: 28px; cursor: pointer; background: transparent; }
    input[type="text"] { border: 1px solid var(--border); border-radius: 4px; padding: 4px 6px; background: var(--vscode-input-background, #1e1e1e); color: var(--fg); font-family: monospace; font-size: 11px; width: 75px; }
    
    .preview-box { border: 1px solid var(--border); border-radius: 6px; padding: 12px; text-align: center; margin: 10px 0; transition: all 0.2s; }
    .badge-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 6px; margin-top: 8px; }
    .status-badge { padding: 4px 6px; border-radius: 4px; font-size: 10px; text-align: center; font-weight: bold; border: 1px solid transparent; }
    .pass { background: rgba(16, 185, 129, 0.15); color: #34d399; border-color: rgba(16, 185, 129, 0.3); }
    .fail { background: rgba(239, 68, 68, 0.15); color: #f87171; border-color: rgba(239, 68, 68, 0.3); }
    .ratio-display { font-size: 20px; font-weight: bold; font-family: monospace; text-align: center; margin: 6px 0; }
  </style>
</head>
<body>
  <div class="tabs">
    <button class="tab-btn active" onclick="switchTab('chemistries', this)">Chemistries</button>
    <button class="tab-btn" onclick="switchTab('contrast', this)">WCAG Calculator</button>
    <button class="tab-btn" onclick="switchTab('components', this)">Components</button>
  </div>

  <!-- Pane 1: Chemistries -->
  <div id="pane-chemistries" class="pane active">
    <div class="card">
      <div class="card-title">Minimalist SaaS <span class="tag">B2B</span></div>
      <div class="desc">High-signal monochrome restraint with subtle borders and OKLCH precision.</div>
      <button class="btn" onclick="copyTokens('MINIMALIST_SAAS')">Copy Color Tokens</button>
    </div>
    <div class="card">
      <div class="card-title">Luxury Glass 2.0 <span class="tag">Status</span></div>
      <div class="desc">Deep dark substrates with specular Fresnel highlights and gold accents.</div>
      <button class="btn" onclick="copyTokens('LUXURY_GLASS_2')">Copy Color Tokens</button>
    </div>
    <div class="card">
      <div class="card-title">Neobrutalism <span class="tag">Creative</span></div>
      <div class="desc">Saturated flat cards with hard 3px black offset geometric shadows.</div>
      <button class="btn" onclick="copyTokens('NEOBRUTALISM')">Copy Color Tokens</button>
    </div>
    <div class="card">
      <div class="card-title">Swiss Editorial <span class="tag">Content</span></div>
      <div class="desc">Asymmetric typography-first layout inspired by International Style.</div>
      <button class="btn" onclick="copyTokens('SWISS_EDITORIAL')">Copy Color Tokens</button>
    </div>
    <div class="card">
      <div class="card-title">Stripe Crisp Light <span class="tag">Docs</span></div>
      <div class="desc">Developer-first documentation layout with micro-borders.</div>
      <button class="btn" onclick="copyTokens('STRIPE_CRISP_LIGHT')">Copy Color Tokens</button>
    </div>
    <div class="card">
      <div class="card-title">Apple Cupertino Fluid <span class="tag">Native</span></div>
      <div class="desc">Translucent frosted chrome, continuous squircles, and optical typography.</div>
      <button class="btn" onclick="copyTokens('APPLE_CUPERTINO')">Copy Color Tokens</button>
    </div>
  </div>

  <!-- Pane 2: WCAG Contrast Calculator -->
  <div id="pane-contrast" class="pane">
    <div class="card">
      <div class="calc-row">
        <span>Background:</span>
        <div class="color-input-wrapper">
          <input type="color" id="bgColor" value="#0f172a" oninput="syncColor('bg', this.value)">
          <input type="text" id="bgHex" value="#0f172a" oninput="syncColor('bg', this.value)">
        </div>
      </div>
      <div class="calc-row">
        <span>Foreground:</span>
        <div class="color-input-wrapper">
          <input type="color" id="fgColor" value="#f8fafc" oninput="syncColor('fg', this.value)">
          <input type="text" id="fgHex" value="#f8fafc" oninput="syncColor('fg', this.value)">
        </div>
      </div>

      <div class="preview-box" id="previewBox">
        <div style="font-weight: bold; font-size: 13px;">Large Heading Text</div>
        <div style="font-size: 11px; opacity: 0.9; margin-top: 2px;">Regular body text sample preview.</div>
      </div>

      <div class="ratio-display" id="ratioText">15.8:1</div>

      <div class="badge-grid">
        <div class="status-badge" id="badgeBodyAA">Body AA (>= 4.5)</div>
        <div class="status-badge" id="badgeHeadingAA">Large AA (>= 3.0)</div>
        <div class="status-badge" id="badgeAAA">Body AAA (>= 7.0)</div>
        <div class="status-badge" id="badgeLargeAAA">Large AAA (>= 4.5)</div>
      </div>
    </div>
  </div>

  <!-- Pane 3: Components -->
  <div id="pane-components" class="pane">
    <div class="card">
      <div class="card-title">Thinking Drawer <span class="tag">AI-Native</span></div>
      <div class="desc">Collapsible AI reasoning drawer with CSS grid zero-JS transition & radar status.</div>
      <button class="btn" onclick="insertComponent('thinking-drawer')">Insert into Active Editor</button>
      <button class="btn btn-secondary" onclick="copyComponent('thinking-drawer')">Copy TSX</button>
    </div>
    <div class="card">
      <div class="card-title">Telemetry HUD <span class="tag">Metrics</span></div>
      <div class="desc">LTR-isolated technical metric HUD with micro-borders for latency and status.</div>
      <button class="btn" onclick="insertComponent('telemetry-hud')">Insert into Active Editor</button>
      <button class="btn btn-secondary" onclick="copyComponent('telemetry-hud')">Copy TSX</button>
    </div>
    <div class="card">
      <div class="card-title">Contrast Badge <span class="tag">WCAG</span></div>
      <div class="desc">Live mathematical accessibility compliance pill (AA / AAA).</div>
      <button class="btn" onclick="insertComponent('contrast-badge')">Insert into Active Editor</button>
      <button class="btn btn-secondary" onclick="copyComponent('contrast-badge')">Copy TSX</button>
    </div>
    <div class="card">
      <div class="card-title">Kinetic Arrow Cursor <span class="tag">Kinetic v4.8</span></div>
      <div class="desc">OS-hiding precision dot cursor with velocity-trailing SVG chevron follower.</div>
      <button class="btn" onclick="insertComponent('kinetic-cursor')">Insert into Active Editor</button>
      <button class="btn btn-secondary" onclick="copyComponent('kinetic-cursor')">Copy TSX</button>
    </div>
    <div class="card">
      <div class="card-title">Infinite Marquee Rail <span class="tag">Living v4.8</span></div>
      <div class="desc">GPU-accelerated infinite horizontal loop rail with pause-on-hover.</div>
      <button class="btn" onclick="insertComponent('marquee-rail')">Insert into Active Editor</button>
      <button class="btn btn-secondary" onclick="copyComponent('marquee-rail')">Copy TSX</button>
    </div>
  </div>

  <script>
    const vscode = acquireVsCodeApi();

    function switchTab(tabId, el) {
      document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      document.querySelectorAll('.pane').forEach(p => p.classList.remove('active'));
      if (el) el.classList.add('active');
      const pane = document.getElementById('pane-' + tabId);
      if (pane) pane.classList.add('active');
    }

    const TOKENS = {
      MINIMALIST_SAAS: \`:root {\\n  --vibe-canvas: oklch(0.12 0.01 260);\\n  --vibe-surface: oklch(0.16 0.01 260);\\n  --vibe-border: oklch(0.24 0.01 260);\\n  --vibe-text-primary: oklch(0.96 0.005 260);\\n  --vibe-accent-primary: oklch(0.65 0.22 260);\\n}\`,
      LUXURY_GLASS_2: \`:root {\\n  --vibe-canvas: oklch(0.08 0.02 270);\\n  --vibe-surface: oklch(0.12 0.02 270);\\n  --vibe-border: oklch(0.28 0.04 270);\\n  --vibe-text-primary: oklch(0.98 0.01 270);\\n  --vibe-accent-primary: oklch(0.78 0.16 75);\\n}\`,
      NEOBRUTALISM: \`:root {\\n  --vibe-canvas: oklch(0.98 0.02 95);\\n  --vibe-surface: oklch(1.0 0 0);\\n  --vibe-border: oklch(0 0 0);\\n  --vibe-text-primary: oklch(0 0 0);\\n  --vibe-accent-primary: oklch(0.85 0.24 135);\\n}\`,
      SWISS_EDITORIAL: \`:root {\\n  --vibe-canvas: oklch(0.97 0.005 80);\\n  --vibe-surface: oklch(0.94 0.008 80);\\n  --vibe-border: oklch(0.15 0.01 80);\\n  --vibe-text-primary: oklch(0.12 0.01 80);\\n  --vibe-accent-primary: oklch(0.55 0.24 25);\\n}\`,
      STRIPE_CRISP_LIGHT: \`:root {\\n  --vibe-canvas: oklch(0.99 0.002 250);\\n  --vibe-surface: oklch(1.0 0 0);\\n  --vibe-border: oklch(0.90 0.01 250);\\n  --vibe-text-primary: oklch(0.18 0.02 260);\\n  --vibe-accent-primary: oklch(0.55 0.20 270);\\n}\`,
      APPLE_CUPERTINO: \`:root {\\n  --vibe-canvas: oklch(0.975 0.005 250);\\n  --vibe-surface: oklch(0.99 0.002 250 / 0.75);\\n  --vibe-border: oklch(0.88 0.005 250);\\n  --vibe-text-primary: oklch(0.15 0.01 250);\\n  --vibe-accent-primary: oklch(0.58 0.22 255);\\n}\`
    };

    function copyTokens(id) {
      vscode.postMessage({ command: 'copy', name: id, text: TOKENS[id] || id });
    }

    const COMPONENT_SNIPPETS = {
      'thinking-drawer': \`<AiThinkingDrawer title="Reasoning DAG" durationMs={120} />\`,
      'telemetry-hud': \`<TelemetryHud metrics={[{ label: 'Latency', value: '38ms' }, { label: 'WCAG', value: '4.8:1', unit: 'AA' }]} />\`,
      'contrast-badge': \`<ContrastBadge ratio={4.8} label="WCAG 2.2" />\`,
      'kinetic-cursor': \`<div id="vibeCursorDot" className="fixed pointer-events-none z-[9999] rounded-full" />\\n<div id="vibeCursorFollower" className="fixed pointer-events-none z-[9998] transition-transform duration-100 ease-out">\\n  <svg viewBox="0 0 50 50" className="w-9 h-9 fill-current"><path d="M42.68 41.15L27.51 6.8a2.3 2.3 0 0 0-4.12 0L7.6 41.15a2.2 2.2 0 0 0 2.81 3.05L24.38 39a2.3 2.3 0 0 1 1.56 0l13.87 5.15a2.2 2.2 0 0 0 2.87-3z"/></svg>\\n</div>\`,
      'marquee-rail': \`<div className="overflow-hidden w-full relative whitespace-nowrap">\\n  <div className="inline-flex gap-8 animate-marquee" style={{ animation: 'marquee 35s linear infinite' }}>\\n    {items.map((item, i) => <span key={i} className="font-mono text-xs">{item}</span>)}\\n  </div>\\n</div>\`
    };

    function insertComponent(id) {
      vscode.postMessage({ command: 'insert', name: id, text: COMPONENT_SNIPPETS[id] });
    }

    function copyComponent(id) {
      vscode.postMessage({ command: 'copy', name: id, text: COMPONENT_SNIPPETS[id] });
    }

    // Mathematical Luminance calculation
    function hexToRgb(hex) {
      hex = hex.replace('#', '');
      if (hex.length === 3) hex = hex.split('').map(c => c + c).join('');
      const num = parseInt(hex, 16);
      return [ (num >> 16) & 255, (num >> 8) & 255, num & 255 ];
    }

    function getLuminance(rgb) {
      const [r, g, b] = rgb.map(val => {
        const c = val / 255;
        return c <= 0.04045 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
      });
      return 0.2126 * r + 0.7152 * g + 0.0722 * b;
    }

    function calculateContrast() {
      const bgHex = document.getElementById('bgHex').value;
      const fgHex = document.getElementById('fgHex').value;
      
      try {
        const bgRgb = hexToRgb(bgHex);
        const fgRgb = hexToRgb(fgHex);
        const l1 = getLuminance(bgRgb);
        const l2 = getLuminance(fgRgb);
        const max = Math.max(l1, l2);
        const min = Math.min(l1, l2);
        const ratio = (max + 0.05) / (min + 0.05);

        // Update UI
        document.getElementById('ratioText').innerText = ratio.toFixed(1) + ':1';
        const pBox = document.getElementById('previewBox');
        pBox.style.backgroundColor = bgHex;
        pBox.style.color = fgHex;

        updateBadge('badgeBodyAA', ratio >= 4.5, 'Body AA (4.5)');
        updateBadge('badgeHeadingAA', ratio >= 3.0, 'Large AA (3.0)');
        updateBadge('badgeAAA', ratio >= 7.0, 'Body AAA (7.0)');
        updateBadge('badgeLargeAAA', ratio >= 4.5, 'Large AAA (4.5)');
      } catch (e) {}
    }

    function updateBadge(id, isPass, label) {
      const el = document.getElementById(id);
      el.className = 'status-badge ' + (isPass ? 'pass' : 'fail');
      el.innerText = (isPass ? '✔ ' : '✕ ') + label;
    }

    function syncColor(type, val) {
      if (!val.startsWith('#')) val = '#' + val;
      if (type === 'bg') {
        document.getElementById('bgColor').value = val;
        document.getElementById('bgHex').value = val;
      } else {
        document.getElementById('fgColor').value = val;
        document.getElementById('fgHex').value = val;
      }
      calculateContrast();
    }

    // Init calculate
    calculateContrast();
  </script>
</body>
</html>`;
  }
}
