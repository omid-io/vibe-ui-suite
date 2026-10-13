#!/usr/bin/env python3
"""
cache_assets.py — Curated WebP Asset Vault Cacher & Optimizer for Vibe UI Suite.
Downloads, optimizes, crops, and converts the 24 canonical domain Unsplash images
into lightweight, local WebP files for 100% offline and intranet resilience.
"""

import sys
import json
import time
import urllib.request
from io import BytesIO
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    from PIL import Image
except ImportError:
    print("Error: Pillow is required. Run 'pip install Pillow'", file=sys.stderr)
    sys.exit(1)

# Ensure UTF-8 output on Windows consoles
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent.parent
DEFAULT_VAULT_JSON = ROOT_DIR / "data" / "unsplash_assets.json"
DEFAULT_OUTPUT_DIR = ROOT_DIR / "assets" / "curated_webp"

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"

def download_and_optimize(url: str, output_path: Path, max_size: tuple, quality: int = 80, force: bool = False) -> dict:
    """Downloads an image from URL, resizes/crops, and saves as WebP."""
    if output_path.exists() and output_path.stat().st_size > 1000 and not force:
        # Validate existing WebP
        try:
            with Image.open(output_path) as img:
                return {
                    "path": str(output_path.relative_to(ROOT_DIR)),
                    "status": "cached",
                    "width": img.width,
                    "height": img.height,
                    "bytes": output_path.stat().st_size
                }
        except Exception:
            pass # re-download if corrupt

    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    retries = 3
    last_err = None
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = resp.read()
            break
        except Exception as e:
            last_err = e
            time.sleep(1.0 * (attempt + 1))
    else:
        raise RuntimeError(f"Failed to download {url} after {retries} attempts: {last_err}")

    # Process image with Pillow
    with Image.open(BytesIO(data)) as img:
        img = img.convert("RGB")
        target_w, target_h = max_size
        
        # Calculate resize keeping cover aspect
        src_w, src_h = img.size
        aspect = src_w / src_h
        target_aspect = target_w / target_h

        if aspect > target_aspect:
            # Source is wider, scale by height then crop width
            new_h = target_h
            new_w = int(target_h * aspect)
        else:
            # Source is taller, scale by width then crop height
            new_w = target_w
            new_h = int(target_w / aspect)

        img_resized = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
        
        # Center crop
        left = (new_w - target_w) // 2
        top = (new_h - target_h) // 2
        right = left + target_w
        bottom = top + target_h
        img_cropped = img_resized.crop((left, top, right, bottom))

        output_path.parent.mkdir(parents=True, exist_ok=True)
        img_cropped.save(output_path, "WEBP", quality=quality, method=6)

    return {
        "path": str(output_path.relative_to(ROOT_DIR)),
        "status": "downloaded",
        "width": target_w,
        "height": target_h,
        "bytes": output_path.stat().st_size
    }

def cache_all_assets(vault_json: Path = DEFAULT_VAULT_JSON, output_dir: Path = DEFAULT_OUTPUT_DIR, force: bool = False, quality: int = 80) -> bool:
    """Processes all 24 canonical domains and caches hero + card WebP images."""
    if not vault_json.exists():
        print(f"[FAIL] Vault JSON not found: {vault_json}", file=sys.stderr)
        return False

    with open(vault_json, "r", encoding="utf-8") as f:
        catalog = json.load(f)

    domains = catalog.get("domains", {})
    total_domains = len(domains)
    print(f"[INFO] Caching curated WebP assets for {total_domains} domains into {output_dir.relative_to(ROOT_DIR)}...")

    tasks = []
    manifest_records = {}

    for domain_id, d_data in domains.items():
        hero_url = d_data.get("hero", {}).get("url")
        card_url = d_data.get("card", {}).get("url")

        hero_dest = output_dir / f"{domain_id}_hero.webp"
        card_dest = output_dir / f"{domain_id}_card.webp"

        tasks.append((domain_id, "hero", hero_url, hero_dest, (1200, 800)))
        tasks.append((domain_id, "card", card_url, card_dest, (600, 400)))

    results = []
    failed = []

    with ThreadPoolExecutor(max_workers=6) as executor:
        future_map = {
            executor.submit(download_and_optimize, url, dest, size, quality, force): (dom, slot, dest)
            for dom, slot, url, dest, size in tasks
        }
        for future in as_completed(future_map):
            dom, slot, dest = future_map[future]
            try:
                info = future.result()
                results.append((dom, slot, info))
                if dom not in manifest_records:
                    manifest_records[dom] = {}
                manifest_records[dom][slot] = info
                print(f"  [{info['status'].upper()}] {dom} ({slot}): {info['bytes'] // 1024} KB")
            except Exception as e:
                print(f"  [FAIL] {dom} ({slot}): {e}", file=sys.stderr)
                failed.append((dom, slot, str(e)))

    # Save manifest.json
    manifest_file = output_dir / "manifest.json"
    manifest_data = {
        "version": "6.0.0",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "total_domains": len(manifest_records),
        "total_assets": len(results),
        "domains": manifest_records
    }
    with open(manifest_file, "w", encoding="utf-8") as f:
        json.dump(manifest_data, f, indent=2, ensure_ascii=False)

    print(f"\n[SUMMARY] {len(results)}/{len(tasks)} assets processed successfully.")
    if failed:
        print(f"[WARNING] {len(failed)} assets failed to download: {failed}", file=sys.stderr)
        return False
    
    print(f"[SUCCESS] All 24 canonical domain assets cached as WebP in {manifest_file.relative_to(ROOT_DIR)}")
    return True

def verify_assets(output_dir: Path = DEFAULT_OUTPUT_DIR, vault_json: Path = DEFAULT_VAULT_JSON) -> bool:
    """Verifies that all 24 domains have valid WebP hero and card assets."""
    if not vault_json.exists():
        print(f"[FAIL] Missing vault JSON: {vault_json}", file=sys.stderr)
        return False

    with open(vault_json, "r", encoding="utf-8") as f:
        catalog = json.load(f)

    domains = catalog.get("domains", {})
    missing = []
    invalid = []

    for domain_id in domains.keys():
        for slot in ["hero", "card"]:
            p = output_dir / f"{domain_id}_{slot}.webp"
            if not p.exists():
                missing.append(f"{domain_id}_{slot}.webp")
                continue
            if p.stat().st_size < 1000:
                invalid.append(f"{domain_id}_{slot}.webp (too small: {p.stat().st_size} bytes)")
                continue
            try:
                with Image.open(p) as img:
                    if img.format != "WEBP":
                        invalid.append(f"{domain_id}_{slot}.webp (format is {img.format})")
            except Exception as e:
                invalid.append(f"{domain_id}_{slot}.webp (corrupt: {e})")

    if missing or invalid:
        print(f"[FAIL] Asset verification failed: Missing={len(missing)}, Invalid={len(invalid)}", file=sys.stderr)
        for m in missing[:5]:
            print(f"  Missing: {m}", file=sys.stderr)
        for inv in invalid[:5]:
            print(f"  Invalid: {inv}", file=sys.stderr)
        return False

    print(f"[SUCCESS] All 48 WebP assets (24 domains x 2) verified and intact in {output_dir.relative_to(ROOT_DIR)}.")
    return True

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Cache and optimize Unsplash assets as local WebP")
    parser.add_argument("--force", action="store_true", help="Force re-download and re-process existing assets")
    parser.add_argument("--verify", action="store_true", help="Verify integrity of cached assets")
    parser.add_argument("--quality", type=int, default=80, help="WebP compression quality (default: 80)")
    parser.add_argument("--output-dir", type=str, default=str(DEFAULT_OUTPUT_DIR), help="Output directory")

    args = parser.parse_args()
    out_dir = Path(args.output_dir)

    if args.verify:
        success = verify_assets(output_dir=out_dir)
    else:
        success = cache_all_assets(output_dir=out_dir, force=args.force, quality=args.quality)
    sys.exit(0 if success else 1)
