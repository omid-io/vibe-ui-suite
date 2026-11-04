#!/usr/bin/env python3
"""
scripts/stealth_crawler.py — On-Demand Stealth Crawler using Patchright / Native Fallback
Vibe UI Suite

Provides bot-undetected web inspection without requiring persistent browser sessions or Playwright MCP.
Gracefully detects Patchright, falls back to standard HTTP requests if not installed,
and guarantees zero orphaned background processes.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, Optional
import urllib.request
import urllib.error

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent.parent

def is_patchright_installed() -> bool:
    """Checks whether patchright is installed in the current Python environment."""
    try:
        import patchright  # type: ignore # noqa: F401
        return True
    except ImportError:
        return False

def install_patchright() -> bool:
    """Installs patchright on demand if requested."""
    print("[INFO] Installing patchright for stealth web crawling...", file=sys.stderr)
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "patchright"],
            check=True,
            capture_output=True,
            timeout=120
        )
        # Install chromium binaries for patchright
        subprocess.run(
            [sys.executable, "-m", "patchright", "install", "chromium"],
            check=True,
            capture_output=True,
            timeout=180
        )
        return True
    except Exception as e:
        print(f"[WARN] Failed to install patchright: {e}", file=sys.stderr)
        return False

def fetch_stealth(url: str, wait_selector: Optional[str] = None, timeout_ms: int = 20000) -> Dict[str, Any]:
    """
    Fetches web content using Patchright if available, or falls back to standard HTTP.
    Returns: {"url": str, "content": str, "method": "patchright" | "http_fallback", "success": bool}
    """
    if is_patchright_installed():
        try:
            from patchright.sync_api import sync_playwright  # type: ignore
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page(
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
                )
                page.goto(url, timeout=timeout_ms, wait_until="domcontentloaded")
                if wait_selector:
                    try:
                        page.wait_for_selector(wait_selector, timeout=5000)
                    except Exception:
                        pass
                content = page.content()
                title = page.title()
                browser.close()
                return {
                    "url": url,
                    "title": title,
                    "content": content,
                    "method": "patchright_stealth",
                    "success": True
                }
        except Exception as err:
            print(f"[WARN] Patchright fetch failed ({err}), falling back to HTTP...", file=sys.stderr)

    # Standard Lightweight HTTP Fallback (Zero external dependency)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    }
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            raw_html = resp.read().decode("utf-8", errors="replace")
            return {
                "url": url,
                "title": "",
                "content": raw_html,
                "method": "http_fallback",
                "success": True
            }
    except Exception as e:
        return {
            "url": url,
            "title": "",
            "content": "",
            "method": "failed",
            "error": str(e),
            "success": False
        }

def main():
    parser = argparse.ArgumentParser(description="Stealth Crawler Utility for Vibe UI")
    parser.add_argument("url", help="Target URL to fetch")
    parser.add_argument("--wait", help="Optional CSS selector to wait for")
    parser.add_argument("--check-install", action="store_true", help="Check and auto-install patchright if missing")
    parser.add_argument("--json", action="store_true", help="Output result as JSON")
    args = parser.parse_args()

    if args.check_install and not is_patchright_installed():
        install_patchright()

    res = fetch_stealth(args.url, wait_selector=args.wait)
    if args.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
    else:
        status = "[SUCCESS]" if res["success"] else "[FAIL]"
        print(f"{status} Fetched {res['url']} using {res['method']} ({len(res.get('content', ''))} chars)")

if __name__ == "__main__":
    main()
