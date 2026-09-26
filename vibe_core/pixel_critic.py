"""
vibe_core.pixel_critic — In-Browser Pixel-Level Screenshot Inspector (v3.9.0)
Analyzes rendered Chromium PNG screenshot buffers using pure Python (zlib & struct):
- PNG chunk decoding (IHDR, IDAT) and scanline decompression
- Canvas whitespace ratio & visual content density
- Mean luminance & contrast variance across the viewport
- Detection of visual collapse, blank screens, and monochrome washouts
"""

import struct
import zlib
import math
from typing import Dict, Any, List, Optional, Tuple


class PixelCritic:
    """
    Genuine pixel-level visual critic that inspects decoded PNG screenshots
    captured from headless Chromium viewports.
    """

    @staticmethod
    def decode_png(png_bytes: bytes) -> Tuple[int, int, List[int]]:
        """
        Decodes PNG bytes into width, height, and sample luminance values (0-255).
        Handles RGBA (color type 6) and RGB (color type 2).
        """
        if not png_bytes or len(png_bytes) < 8:
            raise ValueError("PNG buffer too short or empty")

        if png_bytes[:8] != b"\x89PNG\r\n\x1a\n":
            raise ValueError("Invalid PNG signature")

        offset = 8
        width = 0
        height = 0
        color_type = 6
        idat_chunks = []

        while offset < len(png_bytes):
            length = struct.unpack(">I", png_bytes[offset:offset+4])[0]
            chunk_type = png_bytes[offset+4:offset+8]
            data = png_bytes[offset+8:offset+8+length]
            offset += 12 + length  # length + type(4) + data + crc(4)

            if chunk_type == b"IHDR":
                width, height, bit_depth, color_type = struct.unpack(">IIBB", data[:10])
            elif chunk_type == b"IDAT":
                idat_chunks.append(data)
            elif chunk_type == b"IEND":
                break

        if not idat_chunks or width == 0 or height == 0:
            raise ValueError("Incomplete PNG data or missing IDAT")

        decompressed = zlib.decompress(b"".join(idat_chunks))
        channels = 4 if color_type == 6 else (3 if color_type == 2 else 1)
        stride = 1 + width * channels

        luminance_samples = []
        # Sample every 4th scanline for sub-5ms performance on large viewports
        step = max(1, height // 120)

        for y in range(0, height, step):
            row_start = y * stride
            if row_start + stride > len(decompressed):
                break
            filter_type = decompressed[row_start]
            row_bytes = decompressed[row_start + 1: row_start + stride]

            # Sample every 4th pixel horizontally
            for x in range(0, width, max(1, width // 160)):
                px_idx = x * channels
                if px_idx + (3 if channels >= 3 else 1) <= len(row_bytes):
                    if channels >= 3:
                        r, g, b = row_bytes[px_idx], row_bytes[px_idx+1], row_bytes[px_idx+2]
                        lum = int(0.2126 * r + 0.7152 * g + 0.0722 * b)
                    else:
                        lum = row_bytes[px_idx]
                    luminance_samples.append(lum)

        return width, height, luminance_samples

    def audit_screenshot(
        self,
        png_bytes: bytes,
        viewport_name: str = "desktop"
    ) -> Dict[str, Any]:
        """
        Audits pixel distribution and visual density of a screenshot PNG buffer.
        Returns structured metrics and flags visual collapse defects.
        """
        if not png_bytes or len(png_bytes) < 32:
            return {
                "pixel_score": 0.0,
                "acceptance_status": "REVISE_REQUIRED",
                "viewport": viewport_name,
                "dimensions": {"width": 0, "height": 0},
                "metrics": {
                    "mean_luminance": 0.0,
                    "whitespace_ratio": 1.0,
                    "visual_density": 0.0,
                    "contrast_variance": 0.0
                },
                "defects": [{
                    "type": "pixel_invalid_screenshot_buffer",
                    "severity": "P0",
                    "message": "Screenshot buffer was empty or corrupted."
                }]
            }

        try:
            width, height, samples = self.decode_png(png_bytes)
        except Exception as e:
            return {
                "pixel_score": 0.0,
                "acceptance_status": "REVISE_REQUIRED",
                "viewport": viewport_name,
                "dimensions": {"width": 0, "height": 0},
                "metrics": {
                    "mean_luminance": 0.0,
                    "whitespace_ratio": 1.0,
                    "visual_density": 0.0,
                    "contrast_variance": 0.0
                },
                "defects": [{
                    "type": "pixel_decoding_error",
                    "severity": "P0",
                    "message": f"Failed to decode PNG screenshot: {e}"
                }]
            }

        if not samples:
            return {
                "pixel_score": 0.0,
                "acceptance_status": "REVISE_REQUIRED",
                "viewport": viewport_name,
                "dimensions": {"width": width, "height": height},
                "metrics": {
                    "mean_luminance": 0.0,
                    "whitespace_ratio": 1.0,
                    "visual_density": 0.0,
                    "contrast_variance": 0.0
                },
                "defects": [{
                    "type": "pixel_blank_screen",
                    "severity": "P0",
                    "message": "Zero pixel samples extracted from rendered viewport."
                }]
            }

        n = len(samples)
        mean_lum = sum(samples) / n

        # Canvas background detection: find dominant mode near extremes (near white >240 or near dark <20)
        dark_canvas = sum(1 for s in samples if s < 25)
        light_canvas = sum(1 for s in samples if s > 235)
        is_dark_theme = dark_canvas > light_canvas

        if is_dark_theme:
            bg_pixels = sum(1 for s in samples if s < 30)
        else:
            bg_pixels = sum(1 for s in samples if s > 230)

        whitespace_ratio = round(bg_pixels / n, 4)
        visual_density = round(1.0 - whitespace_ratio, 4)

        # Standard deviation of luminance (contrast dynamic range)
        variance = sum((s - mean_lum) ** 2 for s in samples) / n
        std_dev = round(math.sqrt(variance), 2)

        defects = []
        score = 100.0

        # P0 Check: Visually collapsed or pure blank canvas
        if visual_density < 0.005 or std_dev < 1.0:
            defects.append({
                "type": "pixel_blank_screen",
                "severity": "P0",
                "message": f"Rendered viewport is visually blank or pure solid monochrome (visual density: {visual_density*100:.2f}%, std: {std_dev})."
            })
            score -= 50.0

        # P1 Check: Contrast collapse (muddy low-contrast wash)
        elif std_dev < 8.0:
            defects.append({
                "type": "pixel_contrast_collapse",
                "severity": "P1",
                "message": f"Luminance dynamic range is severely compressed (std dev: {std_dev}, expected >= 8.0)."
            })
            score -= 25.0

        # P2 Check: Extreme whitespace blowout (> 96% empty on desktop)
        if whitespace_ratio > 0.96 and viewport_name == "desktop":
            defects.append({
                "type": "pixel_excessive_whitespace",
                "severity": "P2",
                "message": f"Viewport has excessive empty canvas ({whitespace_ratio*100:.1f}% whitespace)."
            })
            score -= 10.0

        score = round(max(0.0, min(100.0, score)), 1)
        has_p0 = any(d.get("severity") == "P0" for d in defects)
        is_accepted = (score >= 80.0) and not has_p0

        return {
            "pixel_score": score,
            "acceptance_status": "ACCEPTED" if is_accepted else "REVISE_REQUIRED",
            "viewport": viewport_name,
            "dimensions": {"width": width, "height": height},
            "metrics": {
                "mean_luminance": round(mean_lum, 1),
                "whitespace_ratio": whitespace_ratio,
                "visual_density": visual_density,
                "contrast_variance": std_dev
            },
            "defects": defects
        }
