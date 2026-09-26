"""
vibe_core.runtime_compiler — Sub-25ms In-Memory React 19 TSX to ESM Compiler
Transforms autonomous Vibe UI React 19 TSX components into standard ECMAScript modules
and builds self-contained, browser-executable harnesses for headless Chromium execution.
"""

import sys
import os
import shutil
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional, Tuple

ROOT_DIR = Path(__file__).resolve().parent.parent

# Cache the detected esbuild command
_CACHED_ESBUILD_CMD: Optional[str] = None


def find_esbuild_command() -> str:
    """Detects available esbuild executable with sub-millisecond cached resolution."""
    global _CACHED_ESBUILD_CMD
    if _CACHED_ESBUILD_CMD is not None:
        return _CACHED_ESBUILD_CMD

    # 1. System PATH
    for candidate in ["esbuild.exe", "esbuild", "esbuild.cmd"]:
        which_path = shutil.which(candidate)
        if which_path:
            _CACHED_ESBUILD_CMD = f'"{which_path}"'
            return _CACHED_ESBUILD_CMD

    # 2. Local node_modules
    local_bin = ROOT_DIR / "node_modules" / ".bin" / ("esbuild.cmd" if sys.platform == "win32" else "esbuild")
    if local_bin.exists():
        _CACHED_ESBUILD_CMD = f'"{local_bin}"'
        return _CACHED_ESBUILD_CMD

    # 3. Known Windows npm cache path
    if sys.platform == "win32":
        npm_cache = Path(os.environ.get("LOCALAPPDATA", "")) / "npm-cache" / "_npx"
        if npm_cache.exists():
            for exe in npm_cache.glob("**/esbuild.exe"):
                _CACHED_ESBUILD_CMD = f'"{exe}"'
                return _CACHED_ESBUILD_CMD

    # 4. Fallback to npx
    _CACHED_ESBUILD_CMD = "npx.cmd esbuild" if sys.platform == "win32" else "npx esbuild"
    return _CACHED_ESBUILD_CMD


class RuntimeCompiler:
    """Compiles React 19 TSX to ESM and generates self-contained browser execution harnesses."""

    def __init__(self):
        self.esbuild_cmd = find_esbuild_command()

    def compile_tsx(
        self,
        tsx_code: str,
        component_name: str = "VibeMasterpiece",
        bundle_local: bool = True
    ) -> Tuple[str, Optional[str]]:
        """
        Compiles React TSX component into an executable ES module.
        Appends the React 19 root mounting logic to #root.
        When bundle_local is True and local node_modules are present,
        produces a 100% offline self-contained bundle with zero remote imports.
        Returns (compiled_js, error_message).
        """
        wrapper = f"""
import React, {{ useState }} from 'react';
import ReactDOM from 'react-dom/client';

{tsx_code}

const rootEl = document.getElementById('root');
if (rootEl) {{
  const root = ReactDOM.createRoot(rootEl);
  root.render(React.createElement({component_name}));
}}
"""
        starter_modules = ROOT_DIR / "examples" / "nextjs-starter" / "node_modules"
        use_bundle = bundle_local and starter_modules.exists()

        if use_bundle:
            cmd = f"{self.esbuild_cmd} --bundle --loader=tsx --format=esm --minify"
            env = os.environ.copy()
            env["NODE_PATH"] = str(starter_modules)
        else:
            cmd = f"{self.esbuild_cmd} --loader=tsx --format=esm --jsx=automatic"
            env = None

        try:
            p = subprocess.run(
                cmd,
                input=wrapper.encode("utf-8"),
                capture_output=True,
                cwd=str(ROOT_DIR),
                shell=True,
                env=env
            )
            if p.returncode != 0:
                err = p.stderr.decode("utf-8", errors="replace")
                return "", err
            stdout = p.stdout.decode("utf-8", errors="replace")
            return stdout, None
        except Exception as e:
            return "", str(e)

    def build_harness(
        self,
        compiled_js: str,
        title: str = "Vibe UI Living Component Preview",
        is_rtl: bool = False
    ) -> str:
        """
        Builds a self-contained HTML page that executes the compiled component module inside #root.
        If compiled_js is bundled (contains React runtime), operates 100% offline without remote CDNs.
        """
        dir_attr = 'dir="rtl" lang="fa"' if is_rtl else 'dir="ltr" lang="en"'
        is_bundled = ("esm.sh" not in compiled_js) and ("import " not in compiled_js[:500])

        importmap_tag = "" if is_bundled else """<script type="importmap">
  {
    "imports": {
      "react": "https://esm.sh/react@19",
      "react/jsx-runtime": "https://esm.sh/react@19/jsx-runtime",
      "react-dom": "https://esm.sh/react-dom@19",
      "react-dom/client": "https://esm.sh/react-dom@19/client"
    }
  }
  </script>"""

        return f"""<!DOCTYPE html>
<html {dir_attr} class="h-full">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  {importmap_tag}
  <style>
    /* Pure Zero-Network Self-Contained Baseline Stylesheet (Air-Gapped & Offline) */
    *, ::before, ::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    html, body {{ height: 100%; font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }}
    bdi {{ direction: ltr !important; unicode-bidi: isolate; }}
    
    /* Layout Primitives */
    .flex, [class*="flex"] {{ display: flex; }}
    .inline-flex, [class*="inline-flex"] {{ display: inline-flex; }}
    .grid, [class*="grid"] {{ display: grid; }}
    .flex-col, [class*="flex-col"] {{ flex-direction: column; }}
    .flex-row, [class*="flex-row"] {{ flex-direction: row; }}
    .items-center, [class*="items-center"] {{ align-items: center; }}
    .justify-between, [class*="justify-between"] {{ justify-content: space-between; }}
    .justify-center, [class*="justify-center"] {{ justify-content: center; }}
    .justify-start, [class*="justify-start"] {{ justify-content: flex-start; }}
    .justify-end, [class*="justify-end"] {{ justify-content: flex-end; }}
    
    /* Grid Columns */
    [class*="grid-cols-1"] {{ grid-template-columns: repeat(1, minmax(0, 1fr)); }}
    [class*="grid-cols-2"] {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
    [class*="grid-cols-3"] {{ grid-template-columns: repeat(3, minmax(0, 1fr)); }}
    [class*="grid-cols-4"] {{ grid-template-columns: repeat(4, minmax(0, 1fr)); }}
    [class*="grid-cols-12"] {{ grid-template-columns: repeat(12, minmax(0, 1fr)); }}
    [class*="col-span-12"] {{ grid-column: span 12 / span 12; }}
    [class*="col-span-8"] {{ grid-column: span 8 / span 8; }}
    [class*="col-span-7"] {{ grid-column: span 7 / span 7; }}
    [class*="col-span-5"] {{ grid-column: span 5 / span 5; }}
    [class*="col-span-4"] {{ grid-column: span 4 / span 4; }}
    
    /* Gaps & Spacing */
    [class*="gap-1"] {{ gap: 0.25rem; }}
    [class*="gap-2"] {{ gap: 0.5rem; }}
    [class*="gap-3"] {{ gap: 0.75rem; }}
    [class*="gap-4"] {{ gap: 1rem; }}
    [class*="gap-6"] {{ gap: 1.5rem; }}
    [class*="gap-8"] {{ gap: 2rem; }}
    [class*="space-y-2"] > :not([hidden]) ~ :not([hidden]) {{ margin-top: 0.5rem; }}
    [class*="space-y-3"] > :not([hidden]) ~ :not([hidden]) {{ margin-top: 0.75rem; }}
    [class*="space-y-4"] > :not([hidden]) ~ :not([hidden]) {{ margin-top: 1rem; }}
    [class*="space-y-6"] > :not([hidden]) ~ :not([hidden]) {{ margin-top: 1.5rem; }}
    [class*="space-x-1.5"] > :not([hidden]) ~ :not([hidden]) {{ margin-left: 0.375rem; }}
    [class*="space-x-2"] > :not([hidden]) ~ :not([hidden]) {{ margin-left: 0.5rem; }}
    [class*="space-x-3"] > :not([hidden]) ~ :not([hidden]) {{ margin-left: 0.75rem; }}
    [class*="space-x-4"] > :not([hidden]) ~ :not([hidden]) {{ margin-left: 1rem; }}
    [dir="rtl"] [class*="space-x-1.5"] > :not([hidden]) ~ :not([hidden]) {{ margin-left: 0; margin-right: 0.375rem; }}
    [dir="rtl"] [class*="space-x-2"] > :not([hidden]) ~ :not([hidden]) {{ margin-left: 0; margin-right: 0.5rem; }}
    [dir="rtl"] [class*="space-x-3"] > :not([hidden]) ~ :not([hidden]) {{ margin-left: 0; margin-right: 0.75rem; }}
    [dir="rtl"] [class*="space-x-4"] > :not([hidden]) ~ :not([hidden]) {{ margin-left: 0; margin-right: 1rem; }}
    
    /* Padding & Margin */
    [class*="p-2"] {{ padding: 0.5rem; }}
    [class*="p-3"] {{ padding: 0.75rem; }}
    [class*="p-4"] {{ padding: 1rem; }}
    [class*="p-5"] {{ padding: 1.25rem; }}
    [class*="p-6"] {{ padding: 1.5rem; }}
    [class*="p-8"] {{ padding: 2rem; }}
    [class*="px-3"] {{ padding-left: 0.75rem; padding-right: 0.75rem; }}
    [class*="px-4"] {{ padding-left: 1rem; padding-right: 1rem; }}
    [class*="px-5"] {{ padding-left: 1.25rem; padding-right: 1.25rem; }}
    [class*="px-6"] {{ padding-left: 1.5rem; padding-right: 1.5rem; }}
    [class*="py-1"] {{ padding-top: 0.25rem; padding-bottom: 0.25rem; }}
    [class*="py-2"] {{ padding-top: 0.5rem; padding-bottom: 0.5rem; }}
    [class*="py-3"] {{ padding-top: 0.75rem; padding-bottom: 0.75rem; }}
    [class*="py-4"] {{ padding-top: 1rem; padding-bottom: 1rem; }}
    
    /* Dimensions & Strict Touch Targets (WCAG 2.5.5 >= 44x44px) */
    .w-full, [class*="w-full"] {{ width: 100%; }}
    .max-w-full, [class*="max-w-full"] {{ max-width: 100%; }}
    .max-w-6xl, [class*="max-w-6xl"] {{ max-width: 72rem; }}
    .max-w-7xl, [class*="max-w-7xl"] {{ max-width: 80rem; }}
    .mx-auto, [class*="mx-auto"] {{ margin-left: auto; margin-right: auto; }}
    button, input[type="range"], a, [role="button"], [data-vibe-control] {{
      min-height: 44px !important;
    }}
    [class*="min-h-[44px]"] {{ min-height: 44px !important; }}
    [class*="min-w-[44px]"], [class*="min-w-[48px]"] {{ min-width: 44px !important; }}
    [class*="h-11"] {{ height: 44px !important; }}
    .cursor-pointer, [class*="cursor-pointer"] {{ cursor: pointer; }}
    
    /* Borders & Radius */
    .border, [class*="border"] {{ border-width: 1px; border-style: solid; }}
    [class*="rounded-md"] {{ border-radius: 0.375rem; }}
    [class*="rounded-lg"] {{ border-radius: 0.5rem; }}
    [class*="rounded-xl"] {{ border-radius: 0.75rem; }}
    [class*="rounded-2xl"] {{ border-radius: 1rem; }}
    [class*="rounded-full"] {{ border-radius: 9999px; }}
    
    /* Typography & Contrast */
    [class*="text-xs"] {{ font-size: 0.75rem; line-height: 1rem; }}
    [class*="text-sm"] {{ font-size: 0.875rem; line-height: 1.25rem; }}
    [class*="text-base"] {{ font-size: 1rem; line-height: 1.5rem; }}
    [class*="text-lg"] {{ font-size: 1.125rem; line-height: 1.75rem; }}
    [class*="text-xl"] {{ font-size: 1.25rem; line-height: 1.75rem; }}
    [class*="text-2xl"] {{ font-size: 1.5rem; line-height: 2rem; }}
    [class*="text-3xl"] {{ font-size: 1.875rem; line-height: 2.25rem; }}
    [class*="text-4xl"] {{ font-size: 2.25rem; line-height: 2.5rem; }}
    [class*="text-5xl"] {{ font-size: 3rem; line-height: 1; }}
    [class*="font-semibold"] {{ font-weight: 600; }}
    [class*="font-bold"] {{ font-weight: 700; }}
    [class*="font-extrabold"] {{ font-weight: 800; }}
    [class*="font-mono"] {{ font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; }}
    [class*="tracking-tight"] {{ letter-spacing: -0.025em; }}
    .tabular-nums, [class*="tabular-nums"] {{ font-variant-numeric: tabular-nums; }}
    
    /* Focus & Animations */
    button:focus-visible, a:focus-visible, input:focus-visible {{
      outline: 2px solid #3b82f6;
      outline-offset: 2px;
    }}
    .animate-pulse, [class*="animate-pulse"] {{ animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite; }}
    @keyframes pulse {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: .5; }} }}
  </style>
</head>
<body class="min-h-full bg-white dark:bg-zinc-950 text-zinc-900 dark:text-zinc-100 antialiased p-4 sm:p-6">
  <div id="root"></div>
  <script type="module">
{compiled_js}
  </script>
</body>
</html>"""

    def compile_and_harness(
        self,
        tsx_code: str,
        component_name: str = "VibeMasterpiece",
        title: str = "Vibe UI Living Component Preview",
        is_rtl: bool = False
    ) -> Tuple[str, Optional[str]]:
        """Compiles TSX and produces a full browser-executable HTML harness."""
        js_code, err = self.compile_tsx(tsx_code, component_name=component_name)
        if err:
            return "", err
        harness = self.build_harness(js_code, title=title, is_rtl=is_rtl)
        return harness, None
