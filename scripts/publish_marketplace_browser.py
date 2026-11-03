#!/usr/bin/env python3
"""
publish_marketplace_browser.py — Zero-Token Autonomous Marketplace Publisher
Generates an all-in-one end-to-end browser injection script that:
1. Checks page URL and navigates if needed.
2. Dismisses cookie banners automatically.
3. Finds the extension row and clicks "More Actions..." -> "Update".
4. Attaches the latest VSIX package via DataTransfer and triggers React synthetic events.
5. Clicks "Upload" and verifies the status transitions to "Verifying <version>".

Executable via Playwright MCP with:
  browser_run_code_unsafe(filename="run_upload.js")
"""

import sys
import os
import glob
import base64
import subprocess
from pathlib import Path

# Ensure UTF-8 output on Windows consoles
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent.parent
VSCODE_PKG_DIR = ROOT_DIR / "packages" / "vibe-ui-vscode"
ANTIGRAVITY_APP_DIR = Path(os.environ.get("LOCALAPPDATA", "")) / "Programs" / "antigravity"

def get_latest_vsix() -> Path:
    vsix_files = sorted(VSCODE_PKG_DIR.glob("vibe-ui-vscode-*.vsix"), key=os.path.getmtime)
    if not vsix_files:
        raise FileNotFoundError(f"No VSIX package found in {VSCODE_PKG_DIR}. Run 'node build.js' and 'python package_vsix.py' first.")
    return vsix_files[-1]

def build_full_flow_payload(vsix_path: Path) -> str:
    raw_bytes = vsix_path.read_bytes()
    b64 = base64.b64encode(raw_bytes).decode("ascii")
    file_name = vsix_path.name
    version = file_name.replace("vibe-ui-vscode-", "").replace(".vsix", "")

    return f"""async (page) => {{
  const TARGET_URL = "https://marketplace.visualstudio.com/manage/publishers/omid-io";
  const TARGET_VERSION = "{version}";
  const FILE_NAME = "{file_name}";
  const B64_DATA = "{b64}";

  // Helper wait
  const wait = (ms) => new Promise(res => setTimeout(res, ms));

  // 1. Ensure we are on the publisher management page
  if (!page.url().includes("marketplace.visualstudio.com/manage/publishers/omid-io")) {{
    console.log("Navigating to publisher page...");
    await page.goto(TARGET_URL, {{ waitUntil: "networkidle", timeout: 30000 }});
    await wait(2000);
  }}

  // 2. Dismiss cookie alert banner if present
  try {{
    await page.evaluate(() => {{
      const cookieBtn = Array.from(document.querySelectorAll("button")).find(b => 
        b.innerText.trim().toLowerCase().includes("accept") || 
        b.getAttribute("aria-label")?.toLowerCase().includes("accept")
      );
      if (cookieBtn) cookieBtn.click();
    }});
  }} catch (e) {{}}

  // 3. Check if Update dialog is already open
  let isDialogOpen = await page.evaluate(() => !!document.querySelector('input[type="file"]'));

  if (!isDialogOpen) {{
    console.log("Opening Update dialog...");
    // Find More Actions button for Vibe UI Studio
    const clickedActions = await page.evaluate(() => {{
      const rows = Array.from(document.querySelectorAll('[role="row"]'));
      const targetRow = rows.find(r => r.innerText.includes("Vibe UI Studio") || r.innerText.includes("omid-io"));
      if (!targetRow) return false;
      const btn = targetRow.querySelector('button[aria-label="More Actions..."]') || targetRow.querySelector('button[aria-label*="Actions"]');
      if (btn) {{
        btn.click();
        return true;
      }}
      return false;
    }});

    if (!clickedActions) {{
      return {{ error: "Could not locate 'More Actions...' button for Vibe UI Studio extension." }};
    }}

    await wait(800);

    // Click 'Update' in the context menu
    const clickedUpdate = await page.evaluate(() => {{
      const menuItems = Array.from(document.querySelectorAll('.ms-ContextualMenu-itemText, [role="menuitem"]'));
      const updateItem = menuItems.find(el => el.innerText.trim() === "Update");
      if (updateItem) {{
        updateItem.click();
        return true;
      }}
      return false;
    }});

    if (!clickedUpdate) {{
      return {{ error: "Could not find 'Update' item in contextual menu." }};
    }}

    await wait(1500);
  }}

  // 4. Inject VSIX via DataTransfer & synthetic events
  console.log("Injecting VSIX binary payload...");
  const injectResult = await page.evaluate((args) => {{
    const binary = atob(args.b64);
    const bytes = new Uint8Array(binary.length);
    for (let i = 0; i < binary.length; i++) {{
      bytes[i] = binary.charCodeAt(i);
    }}
    const file = new File([bytes], args.fileName, {{ type: "application/vsix" }});
    const dt = new DataTransfer();
    dt.items.add(file);

    const input = document.querySelector('input[type="file"]');
    if (!input) return {{ error: "input[type=file] not found in modal dialog." }};

    input.files = dt.files;

    // Trigger React synthetic event
    let reactPropsKey = Object.keys(input).find(k => k.startsWith("__reactProps"));
    if (reactPropsKey && typeof input[reactPropsKey].onChange === "function") {{
      input[reactPropsKey].onChange({{
        target: input,
        currentTarget: input,
        nativeEvent: new Event("change"),
        persist: () => {{}}
      }});
    }}

    input.dispatchEvent(new Event("input", {{ bubbles: true }}));
    input.dispatchEvent(new Event("change", {{ bubbles: true }}));

    // Dropzone synthetic events
    const dropzone = document.querySelector(".file-select-control") || document.querySelector(".droptarget-region") || document.querySelector(".ms-Dialog-content");
    if (dropzone) {{
      dropzone.dispatchEvent(new DragEvent("dragenter", {{ bubbles: true, cancelable: true, dataTransfer: dt }}));
      dropzone.dispatchEvent(new DragEvent("drop", {{ bubbles: true, cancelable: true, dataTransfer: dt }}));
    }}

    return {{ attached: true, size: file.size }};
  }}, {{ b64: B64_DATA, fileName: FILE_NAME }});

  if (injectResult.error) return injectResult;

  await wait(800);

  // 5. Click the Upload button
  console.log("Clicking Upload button...");
  const uploadClicked = await page.evaluate(() => {{
    const buttons = Array.from(document.querySelectorAll("button"));
    const uploadBtn = buttons.find(b => b.innerText.trim() === "Upload" || b.getAttribute("aria-label") === "Upload");
    if (uploadBtn && !uploadBtn.classList.contains("is-disabled") && !uploadBtn.disabled) {{
      uploadBtn.click();
      return true;
    }}
    return false;
  }});

  if (!uploadClicked) {{
    return {{ error: "Upload button was not clickable or remained disabled after file attachment." }};
  }}

  // 6. Wait for verification status to appear in table
  console.log("Waiting for verification status in extension table...");
  let finalStatus = "SUBMITTED";
  for (let attempt = 0; attempt < 8; attempt++) {{
    await wait(1500);
    const tableInfo = await page.evaluate((targetVer) => {{
      const rows = Array.from(document.querySelectorAll('[role="row"]')).map(r => r.innerText.replace(/\\s+/g, ' '));
      const targetRow = rows.find(r => r.includes("Vibe UI Studio"));
      return {{
        found: !!targetRow,
        rowText: targetRow || "",
        isVerifying: targetRow ? (targetRow.includes("Verifying") || targetRow.includes(targetVer)) : false
      }};
    }}, TARGET_VERSION);

    if (tableInfo.isVerifying) {{
      finalStatus = "VERIFYING_OR_PUBLISHED";
      return {{
        success: true,
        version: TARGET_VERSION,
        status: finalStatus,
        details: tableInfo.rowText
      }};
    }}
  }}

  return {{
    success: true,
    version: TARGET_VERSION,
    status: finalStatus,
    note: "Upload was submitted. Please check table for final confirmation."
  }};
}}"""

def main():
    print("=" * 70)
    print("  🚀 Vibe UI Suite — Full-Flow Autonomous Marketplace Publisher")
    print("=" * 70)

    vsix_path = get_latest_vsix()
    print(f"📦 Detected latest VSIX: {vsix_path.name} ({vsix_path.stat().st_size:,} bytes)")

    payload = build_full_flow_payload(vsix_path)

    # 1. Save runner snippet to scripts/run_upload.js
    runner_file = ROOT_DIR / "scripts" / "run_upload.js"
    runner_file.write_text(payload, encoding="utf-8")
    print(f"✅ Generated local runner script: {runner_file}")

    # 2. Mirror into Antigravity server dir if available for instant browser_run_code_unsafe execution
    if ANTIGRAVITY_APP_DIR.exists():
        antigravity_target = ANTIGRAVITY_APP_DIR / "run_upload.js"
        antigravity_target.write_text(payload, encoding="utf-8")
        
        # Also mirror into scripts/ subfolder inside antigravity runtime
        antigravity_scripts = ANTIGRAVITY_APP_DIR / "scripts"
        antigravity_scripts.mkdir(parents=True, exist_ok=True)
        (antigravity_scripts / "run_upload.js").write_text(payload, encoding="utf-8")
        print(f"✅ Mirrored to Antigravity runtime roots: {antigravity_target}")

    print("\n⚡ Execution Instruction:")
    print("  Run in chat / Playwright MCP:")
    print("  call_mcp_tool(ServerName: 'playwright', ToolName: 'browser_run_code_unsafe', Arguments: { 'filename': 'run_upload.js' })")
    print("  Everything (navigation, cookies, dialog, upload, verification) happens completely automatically in 1 call!")
    print("=" * 70)

if __name__ == "__main__":
    main()
