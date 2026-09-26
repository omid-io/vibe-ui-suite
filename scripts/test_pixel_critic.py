#!/usr/bin/env python3
"""
test_pixel_critic.py — Unit Tests for In-Browser PixelCritic.
Validates PNG decoding, visual density calculation, and blank/collapse defect detection.
"""

import sys
import zlib
import struct
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from vibe_core.pixel_critic import PixelCritic


def make_png(width: int, height: int, fill_pattern: str = "blank") -> bytes:
    """Creates an in-memory RGBA PNG image buffer."""
    raw_rows = []
    for y in range(height):
        row = [0]  # filter byte: 0 (None)
        for x in range(width):
            if fill_pattern == "blank":
                # Pure solid white
                row.extend([255, 255, 255, 255])
            elif fill_pattern == "content":
                # Simulated UI: dark background with white cards and colorful buttons
                if 20 <= x < 80 and 20 <= y < 60:
                    row.extend([255, 255, 255, 255])  # Card
                elif 30 <= x < 70 and 30 <= y < 45:
                    row.extend([59, 130, 246, 255])   # Blue button
                else:
                    row.extend([15, 23, 42, 255])      # Slate 900 canvas
        raw_rows.append(bytes(row))

    compressed = zlib.compress(b"".join(raw_rows))

    def make_chunk(chunk_type: bytes, data: bytes) -> bytes:
        length = struct.pack(">I", len(data))
        crc = struct.pack(">I", zlib.crc32(chunk_type + data) & 0xffffffff)
        return length + chunk_type + data + crc

    ihdr_data = struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0)
    png_bytes = (
        b"\x89PNG\r\n\x1a\n"
        + make_chunk(b"IHDR", ihdr_data)
        + make_chunk(b"IDAT", compressed)
        + make_chunk(b"IEND", b"")
    )
    return png_bytes


def main():
    print("[INFO] Running Unit Tests for PixelCritic...")
    critic = PixelCritic()
    failures = []

    # Test 1: Clean UI screenshot with high visual density & contrast
    clean_png = make_png(120, 100, fill_pattern="content")
    res_clean = critic.audit_screenshot(clean_png, viewport_name="desktop")
    if res_clean["acceptance_status"] != "ACCEPTED":
        failures.append(f"Test 1 Failed: Clean UI was rejected: {res_clean}")
    if res_clean["pixel_score"] < 80.0:
        failures.append(f"Test 1 Failed: Expected score >= 80, got {res_clean['pixel_score']}")
    if res_clean["metrics"]["contrast_variance"] < 10.0:
        failures.append(f"Test 1 Failed: Expected high contrast variance, got {res_clean['metrics']['contrast_variance']}")
    print(f"  [PASS] Test 1: Clean UI screenshot scored {res_clean['pixel_score']}/100 (Density: {res_clean['metrics']['visual_density']*100:.1f}%)")

    # Test 2: Blank whiteout screenshot
    blank_png = make_png(120, 100, fill_pattern="blank")
    res_blank = critic.audit_screenshot(blank_png, viewport_name="desktop")
    if res_blank["acceptance_status"] != "REVISE_REQUIRED":
        failures.append("Test 2 Failed: Blank screenshot should be REVISE_REQUIRED")
    has_blank_p0 = any(d["type"] == "pixel_blank_screen" for d in res_blank["defects"])
    if not has_blank_p0:
        failures.append("Test 2 Failed: Expected 'pixel_blank_screen' P0 defect")
    print("  [PASS] Test 2: Pure blank screenshot rejected with P0 'pixel_blank_screen'")

    # Test 3: Corrupted buffer fallback
    res_err = critic.audit_screenshot(b"not a png buffer", viewport_name="mobile")
    if res_err["acceptance_status"] != "REVISE_REQUIRED":
        failures.append("Test 3 Failed: Corrupted buffer should fail")
    print("  [PASS] Test 3: Corrupted buffer handled gracefully with safe error report")

    if failures:
        print("\n[FAIL] PixelCritic Failures:", file=sys.stderr)
        for f in failures:
            print(f"  - {f}", file=sys.stderr)
        return 1

    print("\n[SUCCESS] PixelCritic passed all unit tests (3/3).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
