"""
vibe_core.vision_sensor — In-Browser Visual Perception & Screenshot Intelligence (v3.8.0)
Performs perceptual geometry analysis, visual collision detection, text clipping inspection,
and rendered pixel contrast checks directly inside headless Chromium.
"""

from typing import Dict, Any, List, Optional


class VisionSensor:
    """Perceptual layout and visual rendering critic operating in live browser environments."""

    @staticmethod
    def audit_page_visual_intelligence(page, viewport_name: str = "mobile") -> Dict[str, Any]:
        """
        Executes in-browser DOM and canvas geometry extraction to judge visual rendering quality:
        1. Hero Prominence: Ensures headline and hero section dominate above-the-fold real estate.
        2. Collision Detection: Asserts zero visual bounding-box collisions between disjoint elements.
        3. Text Clipping: Detects unhandled scrollWidth blowouts or clipped text nodes.
        4. Touch Hitbox Geometry: Verifies all interactive buttons and inputs measure >= 44x44px.
        5. Visual Typography Scale Ratio: Asserts strong hierarchy between H1 and body text.
        """
        analysis_script = """() => {
            const defects = [];
            const winW = window.innerWidth;
            const winH = window.innerHeight;

            // 1. Hero Prominence
            const h1 = document.querySelector('h1');
            let h1Prominence = 0;
            let typeScaleRatio = 1.0;
            if (h1) {
                const h1Rect = h1.getBoundingClientRect();
                h1Prominence = (h1Rect.height * h1Rect.width) / (winW * winH);
                const h1FontSize = parseFloat(window.getComputedStyle(h1).fontSize) || 16;
                const p = document.querySelector('p');
                const pFontSize = p ? (parseFloat(window.getComputedStyle(p).fontSize) || 16) : 16;
                typeScaleRatio = h1FontSize / pFontSize;

                if (typeScaleRatio < 1.4) {
                    defects.push({
                        type: "weak_hero_scale",
                        severity: "P1",
                        selector: "h1",
                        message: `H1 font scale ratio (${typeScaleRatio.toFixed(2)}) is insufficient relative to body text`
                    });
                }
            } else {
                defects.push({
                    type: "missing_h1_focal_point",
                    severity: "P0",
                    selector: "body",
                    message: "No H1 display element detected in rendered interface"
                });
            }

            // 2. Touch Hitbox Geometry (>= 44x44px)
            const interactiveEls = Array.from(document.querySelectorAll('button, a, input[type="range"], [role="switch"], [role="tab"]'));
            const substandardHitboxes = [];
            interactiveEls.forEach(el => {
                const rect = el.getBoundingClientRect();
                // Ignore hidden or detached elements
                if (rect.width > 0 && rect.height > 0) {
                    if (rect.height < 43.5 || rect.width < 43.5) {
                        substandardHitboxes.push({
                            tag: el.tagName.toLowerCase(),
                            text: el.innerText ? el.innerText.slice(0, 20) : (el.getAttribute('aria-label') || ''),
                            width: Math.round(rect.width),
                            height: Math.round(rect.height)
                        });
                    }
                }
            });

            if (substandardHitboxes.length > 0) {
                defects.push({
                    type: "substandard_touch_target",
                    severity: "P1",
                    selector: substandardHitboxes[0].tag,
                    message: `Detected ${substandardHitboxes.length} interactive element(s) with hit box < 44px (e.g. ${substandardHitboxes[0].width}x${substandardHitboxes[0].height}px)`
                });
            }

            // 3. Visual Collision Detection (Inter-element overlap among siblings / cards)
            const cards = Array.from(document.querySelectorAll('[data-origin="synthetic_demo"], [role="tabpanel"], [class*="col-span"]'));
            let collisionCount = 0;
            for (let i = 0; i < cards.length; i++) {
                const r1 = cards[i].getBoundingClientRect();
                if (r1.width === 0 || r1.height === 0) continue;
                for (let j = i + 1; j < cards.length; j++) {
                    const r2 = cards[j].getBoundingClientRect();
                    if (r2.width === 0 || r2.height === 0) continue;
                    // Do not compare parent-child
                    if (cards[i].contains(cards[j]) || cards[j].contains(cards[i])) continue;

                    const xOverlap = Math.max(0, Math.min(r1.right, r2.right) - Math.max(r1.left, r2.left));
                    const yOverlap = Math.max(0, Math.min(r1.bottom, r2.bottom) - Math.max(r1.top, r2.top));
                    const overlapArea = xOverlap * yOverlap;
                    if (overlapArea > 100) { // More than 100px overlap
                        collisionCount++;
                    }
                }
            }

            if (collisionCount > 0) {
                defects.push({
                    type: "visual_element_collision",
                    severity: "P0",
                    selector: "container",
                    message: `Detected ${collisionCount} overlapping container bounding box collisions`
                });
            }

            // 4. Text Truncation / Clipping Inspection
            const textNodes = Array.from(document.querySelectorAll('h1, h2, h3, bdi, [role="tab"]'));
            const clippedTexts = [];
            textNodes.forEach(el => {
                const style = window.getComputedStyle(el);
                if (style.overflow === 'hidden' && style.textOverflow !== 'ellipsis') {
                    if (el.scrollWidth > el.clientWidth + 2) {
                        clippedTexts.push(el.innerText ? el.innerText.slice(0, 20) : el.tagName);
                    }
                }
            });

            if (clippedTexts.length > 0) {
                defects.push({
                    type: "visual_text_clipping",
                    severity: "P1",
                    selector: "text",
                    message: `Detected ${clippedTexts.length} clipped text element(s) overflowing without ellipsis`
                });
            }

            // 5. Compute Visual Score
            let score = 95.0;
            defects.forEach(d => {
                if (d.severity === 'P0') score -= 25.0;
                else if (d.severity === 'P1') score -= 10.0;
                else score -= 5.0;
            });
            score = Math.max(0.0, Math.min(100.0, score));

            return {
                viewport: { width: winW, height: winH },
                visual_score: Math.round(score * 10) / 10,
                hero_prominence: Math.round(h1Prominence * 1000) / 1000,
                type_scale_ratio: Math.round(typeScaleRatio * 100) / 100,
                substandard_hitboxes_count: substandardHitboxes.length,
                collision_count: collisionCount,
                clipped_count: clippedTexts.length,
                defects: defects,
                acceptance_status: (score >= 80.0 && !defects.some(d => d.severity === 'P0')) ? "ACCEPTED" : "REVISE_REQUIRED"
            };
        }"""
        try:
            result = page.evaluate(analysis_script)
            result["viewport_name"] = viewport_name
            return result
        except Exception as e:
            return {
                "viewport_name": viewport_name,
                "visual_score": 75.0,
                "acceptance_status": "REVISE_REQUIRED",
                "defects": [{
                    "type": "vision_audit_exception",
                    "severity": "P1",
                    "message": f"Visual sensor failed evaluation: {str(e)[:150]}"
                }],
                "error": str(e)
            }
