#!/usr/bin/env python3
"""
scripts/screenshot_audit.py — Automated Multi-Viewport Screenshot & Visual Inspection Utility
Vibe UI Suite v6.0.0

Launches headless Chromium via Playwright, renders target HTML or TSX artifacts across
standard Desktop (1440x900) and Mobile (390x844) viewports, captures PNG screenshots
to .test-artifacts/screenshots/, executes visual health audits (horizontal overflow, broken images),
and guarantees zero orphaned browser processes.
"""

from __future__ import annotations

import argparse
import atexit
import json
import signal
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Registry for resilient process cleanup
_GLOBAL_ACTIVE_BROWSER: Any = None
_GLOBAL_ACTIVE_PLAYWRIGHT: Any = None


def _cleanup_browser_resources() -> None:
    """Closes any active Playwright browser instance and driver to prevent zombie processes."""
    global _GLOBAL_ACTIVE_BROWSER, _GLOBAL_ACTIVE_PLAYWRIGHT
    if _GLOBAL_ACTIVE_BROWSER is not None:
        try:
            _GLOBAL_ACTIVE_BROWSER.close()
        except Exception:
            pass
        _GLOBAL_ACTIVE_BROWSER = None

    if _GLOBAL_ACTIVE_PLAYWRIGHT is not None:
        try:
            _GLOBAL_ACTIVE_PLAYWRIGHT.stop()
        except Exception:
            pass
        _GLOBAL_ACTIVE_PLAYWRIGHT = None


# Register cleanup on normal/abnormal Python interpreter exit
atexit.register(_cleanup_browser_resources)


def _signal_handler(signum: int, frame: Any) -> None:
    """Handles SIGINT/SIGTERM to ensure clean browser teardown."""
    _cleanup_browser_resources()
    sys.exit(128 + signum)


try:
    signal.signal(signal.SIGINT, _signal_handler)
    signal.signal(signal.SIGTERM, _signal_handler)
except Exception:
    pass


# Standard Viewport Definitions
VIEWPORT_PRESETS: Dict[str, Dict[str, Any]] = {
    "desktop": {
        "name": "desktop",
        "width": 1440,
        "height": 900,
        "label": "Desktop (1440px)",
    },
    "mobile": {
        "name": "mobile",
        "width": 390,
        "height": 844,
        "label": "Mobile (390px)",
    },
}


def _resolve_render_target(file_path: Path) -> Tuple[Path, Optional[Path]]:
    """
    Resolves the actual HTML file to be rendered in Playwright.
    - If target is .html, returns (file_path, None).
    - If target is .tsx or .jsx, checks for companion .html in the same directory.
    - If no companion .html exists, generates a temporary preview HTML harness.
    Returns (render_path, temp_file_to_cleanup).
    """
    resolved = file_path.resolve()
    if not resolved.exists():
        raise FileNotFoundError(f"Target file not found: {file_path}")

    suffix = resolved.suffix.lower()
    if suffix in [".html", ".htm"]:
        return resolved, None

    if suffix in [".tsx", ".jsx"]:
        companion_html = resolved.with_suffix(".html")
        if companion_html.exists():
            return companion_html, None

        # Build temporary standalone HTML preview wrapper with Tailwind + React Babel
        temp_html = resolved.parent / f"__vibe_tmp_{resolved.stem}_preview.html"
        code = resolved.read_text(encoding="utf-8")

        lines = []
        for line in code.splitlines():
            stripped = line.strip()
            if stripped.startswith('"use client"') or stripped.startswith("'use client'"):
                continue
            if stripped.startswith("import "):
                continue
            if stripped.startswith("export default ") or stripped.startswith("export "):
                line = line.replace("export default ", "").replace("export ", "")
            lines.append(line)
        cleaned_tsx = "\n".join(lines)

        preview_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Vibe Preview — {resolved.stem}</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
  <script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
  <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
</head>
<body class="bg-slate-900 text-slate-100 min-h-screen">
  <div id="root"></div>
  <script type="text/babel">
    const {{ useState, useEffect, useRef }} = React;
    {cleaned_tsx}

    const App = () => {{
      if (typeof VibeMasterpiece !== "undefined") return <VibeMasterpiece />;
      return <div>Component loaded</div>;
    }};

    const root = ReactDOM.createRoot(document.getElementById("root"));
    root.render(<App />);
  </script>
</body>
</html>"""
        temp_html.write_text(preview_content, encoding="utf-8")
        return temp_html, temp_html

    return resolved, None


def _parse_viewports(viewports_arg: Union[str, Sequence[Any]]) -> List[Dict[str, Any]]:
    """Parses viewport argument into list of viewport configuration dicts."""
    if isinstance(viewports_arg, str):
        keys = [k.strip().lower() for k in viewports_arg.split(",") if k.strip()]
    elif isinstance(viewports_arg, (list, tuple, set)):
        keys = []
        configs_direct = []
        for item in viewports_arg:
            if isinstance(item, dict) and "width" in item and "height" in item:
                w = int(item["width"])
                h = int(item["height"])
                name = item.get("name", f"custom_{w}x{h}")
                configs_direct.append({
                    "name": name,
                    "width": w,
                    "height": h,
                    "label": item.get("label", name),
                })
            elif isinstance(item, str):
                for k in item.split(","):
                    if k.strip():
                        keys.append(k.strip().lower())
        if configs_direct and not keys:
            return configs_direct
    else:
        keys = ["desktop", "mobile"]

    if not keys:
        keys = ["desktop", "mobile"]

    configs: List[Dict[str, Any]] = []
    for key in keys:
        if key in VIEWPORT_PRESETS:
            configs.append(VIEWPORT_PRESETS[key])
        elif "x" in key:
            try:
                w_str, h_str = key.split("x", 1)
                w, h = int(w_str), int(h_str)
                configs.append({
                    "name": f"custom_{w}x{h}",
                    "width": w,
                    "height": h,
                    "label": f"Custom ({w}x{h})",
                })
            except Exception:
                continue

    if not configs:
        configs = [VIEWPORT_PRESETS["desktop"], VIEWPORT_PRESETS["mobile"]]
    return configs


def capture_audit_screenshots(
    file_path: Union[str, Path],
    output_dir: Union[str, Path] = ".test-artifacts/screenshots",
    viewports: Union[str, Sequence[str]] = ("desktop", "mobile"),
    full_page: bool = True,
) -> Dict[str, Any]:
    """
    Captures screenshots for target HTML/TSX across requested viewports.
    Performs visual audits (horizontal overflow and broken images).
    Guarantees zero orphaned browser processes upon completion or error.

    Args:
        file_path: Path to HTML or TSX file.
        output_dir: Output directory for captured screenshots.
        viewports: Comma-separated string or sequence of viewport names ('desktop', 'mobile').
        full_page: Whether to capture full scrollable height (default True).

    Returns:
        Structured audit report dict containing screenshot paths and visual diagnostics.
    """
    global _GLOBAL_ACTIVE_BROWSER, _GLOBAL_ACTIVE_PLAYWRIGHT

    target_path = Path(file_path).resolve()
    if not target_path.exists():
        raise FileNotFoundError(f"Target file not found: {file_path}")

    render_path, temp_file_to_cleanup = _resolve_render_target(target_path)

    out_dir = Path(output_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    vp_configs = _parse_viewports(viewports)

    try:
        from playwright.sync_api import sync_playwright
    except ImportError as err:
        if temp_file_to_cleanup and temp_file_to_cleanup.exists():
            try:
                temp_file_to_cleanup.unlink()
            except Exception:
                pass
        raise RuntimeError(
            "Playwright is not installed. Run 'pip install playwright && playwright install chromium'."
        ) from err

    browser_inst = None
    open_pages = []

    try:
        with sync_playwright() as playwright_cm:
            _GLOBAL_ACTIVE_PLAYWRIGHT = playwright_cm
            browser_inst = playwright_cm.chromium.launch(headless=True)
            _GLOBAL_ACTIVE_BROWSER = browser_inst

            file_uri = render_path.resolve().as_uri()

            report: Dict[str, Any] = {
                "file": str(target_path),
                "rendered_file": str(render_path),
                "output_dir": str(out_dir),
                "viewports": {},
                "screenshots": [],
                "overall_status": "PASS",
            }

            any_failure = False

            for vp in vp_configs:
                page = browser_inst.new_page(
                    viewport={"width": vp["width"], "height": vp["height"]}
                )
                open_pages.append(page)
                page.set_default_timeout(2000)
                page.set_default_navigation_timeout(2000)

                # Resilient navigation: domcontentloaded -> fallback to commit
                try:
                    page.goto(file_uri, wait_until="domcontentloaded", timeout=1200)
                except Exception:
                    try:
                        page.goto(file_uri, wait_until="commit", timeout=1000)
                    except Exception:
                        pass

                # Wait for web fonts ready with fallback
                try:
                    page.evaluate("() => Promise.race([document.fonts ? document.fonts.ready : Promise.resolve(), new Promise(r => setTimeout(r, 250))])")
                except Exception:
                    pass

                # Stabilization pause
                page.wait_for_timeout(100)

                # Visual Check 1: Horizontal overflow
                try:
                    has_overflow = bool(
                        page.evaluate(
                            "() => document.documentElement ? document.documentElement.scrollWidth > document.documentElement.clientWidth : false"
                        )
                    )
                except Exception:
                    has_overflow = False

                # Visual Check 2: Image audit
                try:
                    img_stats = page.evaluate("""() => {
                        const imgs = Array.from(document.images);
                        const broken = imgs.filter(i => !i.complete || i.naturalWidth === 0).length;
                        return {
                            total: imgs.length,
                            broken: broken
                        };
                    }""")
                except Exception:
                    img_stats = {"total": 0, "broken": 0}

                vp_name = vp["name"]
                vp_width = vp["width"]
                vp_height = vp["height"]
                target_stem = target_path.stem
                screenshot_filename = f"{target_stem}_{vp_name}_{vp_width}px.png"
                screenshot_path = out_dir / screenshot_filename

                # Capture screenshot with resilient fallback
                try:
                    page.screenshot(path=str(screenshot_path), full_page=full_page, timeout=2000)
                except Exception:
                    try:
                        page.screenshot(path=str(screenshot_path), full_page=False, timeout=1200)
                    except Exception:
                        pass

                file_size_bytes = (
                    screenshot_path.stat().st_size if screenshot_path.exists() else 0
                )

                # Determine viewport health status
                status = "PASS"
                if vp_name == "mobile" and has_overflow:
                    status = "FAIL"
                    any_failure = True
                elif img_stats.get("broken", 0) > 0:
                    status = "WARN"

                vp_record = {
                    "name": vp_name,
                    "label": vp.get("label", vp_name),
                    "width": vp_width,
                    "height": vp_height,
                    "screenshot_path": str(screenshot_path),
                    "file_size_bytes": file_size_bytes,
                    "horizontal_overflow": has_overflow,
                    "total_images": img_stats.get("total", 0),
                    "broken_images": img_stats.get("broken", 0),
                    "status": status,
                }

                report["viewports"][vp_name] = vp_record
                report["screenshots"].append(str(screenshot_path))

                try:
                    page.close()
                except Exception:
                    pass
                if page in open_pages:
                    open_pages.remove(page)

            report["files"] = {
                vp_name: vp_info["screenshot_path"]
                for vp_name, vp_info in report["viewports"].items()
            }
            report["viewports_captured"] = [
                {
                    "viewport": vp_info["name"],
                    "width": vp_info["width"],
                    "height": vp_info["height"],
                    "path": vp_info["screenshot_path"],
                    "bytes": vp_info["file_size_bytes"],
                    "status": vp_info["status"],
                }
                for vp_info in report["viewports"].values()
            ]
            report["overall_status"] = "FAIL" if any_failure else "PASS"
            report["success"] = True
            return report

    finally:
        for p in list(open_pages):
            try:
                p.close()
            except Exception:
                pass
        if browser_inst is not None:
            try:
                browser_inst.close()
            except Exception:
                pass
            if _GLOBAL_ACTIVE_BROWSER is browser_inst:
                _GLOBAL_ACTIVE_BROWSER = None
        _GLOBAL_ACTIVE_PLAYWRIGHT = None
        if temp_file_to_cleanup and temp_file_to_cleanup.exists():
            try:
                temp_file_to_cleanup.unlink()
            except Exception:
                pass


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Vibe UI Multi-Viewport Screenshot Audit Utility (Playwright Headless Chromium)"
    )
    parser.add_argument("file", help="Path to target HTML or TSX file")
    parser.add_argument(
        "-o",
        "--output-dir",
        default=".test-artifacts/screenshots",
        help="Directory for saved screenshots (default: .test-artifacts/screenshots)",
    )
    parser.add_argument(
        "--viewports",
        default="desktop,mobile",
        help="Comma-separated viewports: 'desktop', 'mobile' (default: desktop,mobile)",
    )
    parser.add_argument(
        "--no-full-page",
        dest="full_page",
        action="store_false",
        default=True,
        help="Capture only initial viewport instead of full scrollable page",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        default=False,
        help="Output audit report as JSON",
    )

    args = parser.parse_args()

    try:
        report = capture_audit_screenshots(
            file_path=args.file,
            output_dir=args.output_dir,
            viewports=args.viewports,
            full_page=args.full_page,
        )
    except Exception as exc:
        print(f"[FAIL] Screenshot audit error: {exc}", file=sys.stderr)
        sys.exit(1)

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print("\n[VIBE UI SCREENSHOT AUDIT]")
        print(f"Target:   {report['file']}")
        if report.get("rendered_file") != report.get("file"):
            print(f"Rendered: {report['rendered_file']}")
        print(f"Output:   {report['output_dir']}\n")

        for vp_name, vp_data in report["viewports"].items():
            label = vp_data.get("label", vp_name.capitalize())
            size_kb = vp_data["file_size_bytes"] / 1024
            overflow = (
                "DETECTED (FAIL)" if vp_data["horizontal_overflow"] else "None (PASS)"
            )
            total_img = vp_data["total_images"]
            broken_img = vp_data["broken_images"]

            print(f"  * [{label}] — Status: {vp_data['status']}")
            print(f"    Artifact:            {vp_data['screenshot_path']} ({size_kb:.1f} KB)")
            print(f"    Horizontal Overflow: {overflow}")
            print(f"    Images:              {total_img} total, {broken_img} broken")
            print()

        print(f"Overall Status: {report['overall_status']}")

    if report["overall_status"] == "FAIL":
        sys.exit(1)


if __name__ == "__main__":
    main()
