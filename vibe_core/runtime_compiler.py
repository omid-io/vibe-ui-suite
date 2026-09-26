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

    def compile_tsx(self, tsx_code: str, component_name: str = "VibeMasterpiece") -> Tuple[str, Optional[str]]:
        """
        Compiles React TSX component into an executable ES module.
        Appends the React 19 root mounting logic to #root.
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
        cmd = f"{self.esbuild_cmd} --loader=tsx --format=esm --jsx=automatic"
        try:
            p = subprocess.run(
                cmd,
                input=wrapper.encode("utf-8"),
                capture_output=True,
                cwd=str(ROOT_DIR),
                shell=True
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
        Builds a self-contained HTML page that loads Tailwind CSS, React 19,
        and executes the compiled component module inside #root.
        """
        dir_attr = 'dir="rtl" lang="fa"' if is_rtl else 'dir="ltr" lang="en"'
        return f"""<!DOCTYPE html>
<html {dir_attr} class="h-full">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script type="importmap">
  {{
    "imports": {{
      "react": "https://esm.sh/react@19",
      "react/jsx-runtime": "https://esm.sh/react@19/jsx-runtime",
      "react-dom": "https://esm.sh/react-dom@19",
      "react-dom/client": "https://esm.sh/react-dom@19/client"
    }}
  }}
  </script>
  <style>
    bdi {{ direction: ltr !important; unicode-bidi: isolate; }}
    button:focus-visible, a:focus-visible, input:focus-visible {{
      outline: 2px solid #10b981;
      outline-offset: 2px;
    }}
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
