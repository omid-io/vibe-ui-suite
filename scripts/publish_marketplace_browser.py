#!/usr/bin/env python3
"""
publish_marketplace_browser.py — Zero-Token Automated Marketplace Publisher
Uploads packaged VSIX extensions directly to Microsoft Visual Studio Marketplace
via in-memory DOM DataTransfer & React synthetic event injection, requiring ZERO Personal Access Tokens (PAT).
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

def build_upload_payload(vsix_path: Path) -> str:
    raw_bytes = vsix_path.read_bytes()
    b64 = base64.b64encode(raw_bytes).decode("ascii")
    file_name = vsix_path.name

    return f"""async (page) => {{
  const b64 = "{b64}";
  return await page.evaluate((base64Str) => {{
    const binary = atob(base64Str);
    const bytes = new Uint8Array(binary.length);
    for (let i = 0; i < binary.length; i++) {{
      bytes[i] = binary.charCodeAt(i);
    }}
    const file = new File([bytes], "{file_name}", {{ type: "application/vsix" }});
    const dt = new DataTransfer();
    dt.items.add(file);

    const input = document.querySelector('input[type="file"]');
    if (!input) return {{ error: "input[type=file] not found. Make sure Update dialog is open." }};

    input.files = dt.files;

    // React synthetic event trigger
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

    // Dropzone events
    const dropzone = document.querySelector(".file-select-control") || document.querySelector(".droptarget-region") || document.querySelector(".ms-Dialog-content");
    if (dropzone) {{
      const dragEnter = new DragEvent("dragenter", {{ bubbles: true, cancelable: true, dataTransfer: dt }});
      dropzone.dispatchEvent(dragEnter);
      const dropEvent = new DragEvent("drop", {{ bubbles: true, cancelable: true, dataTransfer: dt }});
      dropzone.dispatchEvent(dropEvent);
    }}

    const uploadBtn = Array.from(document.querySelectorAll("button")).find(b => b.innerText.trim() === "Upload");
    if (uploadBtn && !uploadBtn.classList.contains("is-disabled") && !uploadBtn.disabled) {{
      uploadBtn.click();
      return {{
        status: "SUCCESS_UPLOAD_CLICKED",
        fileAttached: input.files[0]?.name,
        fileSize: input.files[0]?.size
      }};
    }}

    return {{
      status: "ATTACHED_AWAITING_CLICK",
      fileAttached: input.files[0]?.name,
      fileSize: input.files[0]?.size,
      uploadBtnFound: !!uploadBtn,
      uploadBtnDisabled: uploadBtn ? (uploadBtn.classList.contains("is-disabled") || uploadBtn.disabled) : null
    }};
  }}, b64);
}}"""

def main():
    print("=" * 70)
    print("  🚀 Vibe UI Suite — Zero-Token Marketplace Publisher")
    print("=" * 70)

    vsix_path = get_latest_vsix()
    print(f"📦 Detected latest VSIX: {vsix_path.name} ({vsix_path.stat().st_size:,} bytes)")

    payload = build_upload_payload(vsix_path)

    # 1. Save runner snippet to scripts/run_upload.js
    runner_file = ROOT_DIR / "scripts" / "run_upload.js"
    runner_file.write_text(payload, encoding="utf-8")
    print(f"✅ Generated local runner script: {runner_file}")

    # 2. Mirror into Antigravity server dir if available for instant browser_run_code_unsafe execution
    if ANTIGRAVITY_APP_DIR.exists():
        antigravity_target = ANTIGRAVITY_APP_DIR / "run_upload.js"
        antigravity_target.write_text(payload, encoding="utf-8")
        print(f"✅ Mirrored to Antigravity runtime: {antigravity_target}")

    # 3. Copy standalone browser console snippet to clipboard
    console_snippet = f"""(() => {{
  {payload.replace('async (page) => {', '').rstrip('}')}
  return eval('(' + {payload} + ')')(null);
}})()"""
    try:
        subprocess.run(
            ["powershell", "-NoProfile", "-Command", f"Set-Clipboard -Value (Get-Content '{runner_file}' -Raw)"],
            check=True,
            capture_output=True
        )
        print("📋 Upload script copied to Windows Clipboard automatically!")
    except Exception:
        pass

    print("\n💡 Operational Workflow:")
    print("  1. In Chrome, navigate to: https://marketplace.visualstudio.com/manage/publishers/omid-io")
    print("  2. Click 'More Actions...' () next to 'Vibe UI Studio & Contrast Gate' -> Click 'Update'")
    print("  3. Run either via Antigravity: call_mcp_tool(browser_run_code_unsafe, filename='run_upload.js')")
    print("     OR simply open DevTools Console (F12) in Chrome and press Ctrl+V -> Enter!")
    print("=" * 70)

if __name__ == "__main__":
    main()
