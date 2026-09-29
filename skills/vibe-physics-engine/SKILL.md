---
name: vibe-physics-engine
description: Physics-based UI motion, anti-template visual architecture, Apple/Linear spring dynamics, velocity handoff, GPU-accelerated compositing, OKLCH perceptual tokens, and strict anti-slop animation rules.
triggers: ["vibe coding", "add physics", "animate", "smooth UI", "framer motion", "gsap", "fluid motion", "lenis", "oklch", "spring physics", "motion review"]
---

# ⚡ Vibe Motion & Physics Engine (v2026 Core)

## 🎯 Purpose
The `vibe-physics-engine` powers bespoke, high-framerate visual and interactive experiences. It mandates mathematical motion curves, critically damped spring mechanics, GPU-accelerated layer compositing, refresh-rate-aware interpolation, OKLCH perceptual color science, and strict anti-slop animation ergonomics.

---

## 🏎️ 1. Critically Damped Springs & Natural Dynamics

Natural interface motion derives from physical spring equations rather than artificial linear or ease-in curves.

### A. Core Spring Constants
- **Default UI Element (Popovers, Tooltips, Menus):** Critically damped with zero overshoot:
  - `damping: 1.0`, `response: 0.3s - 0.4s`
  - Eliminates distracting bounce while maintaining organic responsiveness.
- **Dynamic Flick / Momentum (Drawers, Swipe Gestures):** Slightly under-damped with subtle organic settle:
  - `damping: 0.82`, `response: 0.35s`
- **Reversal & Interruption:** When an ongoing animation is interrupted or reversed, NEVER restart from zero or hit a sudden stop. Retain current velocity and retarget smoothly:
  - Read live presentation value via `getBoundingClientRect()` or continuous CSS transitions.

### B. Touch Gestures & Velocity Handoff (1:1 Direct Manipulation)
- Maintain an exact 1:1 displacement ratio with the user pointer during drag (`setPointerCapture`).
- Upon release, hand off the user gesture release velocity into the spring motion equation:
  $$v_{release} = \frac{\Delta x}{\Delta t}$$
- **Boundary Resistance (Rubber-banding):** Never hard-stop at boundary edges. Apply progressive logarithmic resistance:
  $$x_{rubber} = x_{bound} + (x_{raw} - x_{bound}) \cdot 0.35$$

---

## ⏱️ 2. Asymmetric Enter/Exit Timing Protocol

Human perception interprets entering elements and exiting elements fundamentally differently:
- **Enter Transitions (Informative & Deliberate):**
  - Duration: `200ms - 300ms`
  - Curve: `cubic-bezier(0.16, 1, 0.3, 1)` (snappy ease-out) or critically damped spring.
  - Initial State: Must start from `scale(0.95)` with `opacity: 0`. **NEVER start from `scale(0)`**.
- **Exit Transitions (Instant & Non-Blocking):**
  - Duration: `120ms - 180ms` (30% to 50% faster than enter).
  - Curve: `ease-out` or `cubic-bezier(0.7, 0, 0.84, 0)`.
  - The user has finished the interaction; the UI must get out of the way immediately.
- **Active Press vs. Release:**
  - Active Press: Can be deliberate (`200ms` or linear hold-to-confirm).
  - Release Action: Must be instant (`100ms - 150ms ease-out`).
- **Keyboard Shortcuts (⌘K, Escape, Tabs):**
  - **Zero Animation Delay:** Must open and close with zero latency (instant rendering or ultra-fast ≤80ms fade). Never make keyboard-driven power users wait on motion.

---

## ⚡ 3. Off-Main-Thread GPU Acceleration & WAAPI

Main thread congestion during page loads or heavy React re-renders drops frames in JavaScript-driven animation loops (`requestAnimationFrame`).

### A. Framer Motion Performance Rules
```jsx
// ❌ WRONG: Animates layout properties on main thread, drops frames during loads
<motion.div animate={{ x: 100, width: 300 }} />

// ✅ CORRECT: Pure compositor layer, GPU-accelerated off-main-thread
<motion.div animate={{ transform: "translateX(100px)" }} />
```

### B. High-Performance Web Animations API (WAAPI)
For dynamic programmatic control without bulky external library overhead:
```javascript
element.animate(
  [
    { opacity: 0, transform: 'translateY(8px) scale(0.96)' },
    { opacity: 1, transform: 'translateY(0) scale(1)' }
  ],
  {
    duration: 220,
    easing: 'cubic-bezier(0.16, 1, 0.3, 1)',
    fill: 'forwards'
  }
);
```

---

## 🌊 4. Stagger Delay Protocol (Cascading Entrances)

When rendering lists, bento grids, or card collections:
- Apply a tight stagger interval of **30ms to 60ms** between items.
- **Maximum Stagger Cap:** Total stagger cycle must never exceed `300ms`, regardless of item count (batch remaining items together).
- Never block user interaction or clicks while stagger animations are active.
```css
.stagger-item {
  opacity: 0;
  transform: translateY(8px);
  animation: vibeEntrance 240ms cubic-bezier(0.16, 1, 0.3, 1) forwards;
}
.stagger-item:nth-child(1) { animation-delay: 0ms; }
.stagger-item:nth-child(2) { animation-delay: 40ms; }
.stagger-item:nth-child(3) { animation-delay: 80ms; }
.stagger-item:nth-child(4) { animation-delay: 120ms; }
```

---

## ♿ 5. Accessibility & Environmental Adaptability

### A. `prefers-reduced-motion`
Respect vestibular disorders. Reduce does not mean zero visual feedback; replace position/scale translations with instantaneous or gentle opacity cross-fades:
```css
@media (prefers-reduced-motion: reduce) {
  *, ::before, ::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
  .vibe-sheet, .vibe-dialog {
    transition: opacity 150ms ease !important;
    transform: none !important;
  }
}
```

### B. `prefers-reduced-transparency`
For high-contrast glassmorphism surfaces:
```css
@media (prefers-reduced-transparency: reduce) {
  .vibe-glass {
    backdrop-filter: none !important;
    background: oklch(0.14 0.005 260) !important; /* Fully opaque surface */
  }
}
```

### C. Touch Device Hover Guard
Touchscreens trigger hover states on tap, causing sticky hover artifacts on iOS Safari and Android Chrome. Always gate hover effects:
```css
@media (hover: hover) and (pointer: fine) {
  .vibe-button:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  }
}
```

---

## 🚫 6. Motion Anti-Patterns Checklist (Anti-Slop Hard Gates)

| Anti-Pattern Violation | Consequence | Mandated Vibe UI Fix |
| :--- | :--- | :--- |
| `transition: all` | Recalculates all layout props, causes severe jank | Specify exact targets: `transition: transform 200ms ease-out, opacity 200ms` |
| `scale(0)` entrance | Looks comical and unnatural (balloon popping in) | Start at `scale(0.95)` with `opacity: 0` |
| `ease-in` on enter | Sluggish start, gives impression of software latency | Use `ease-out` or `cubic-bezier(0.16, 1, 0.3, 1)` |
| Duration > 300ms on UI | Interface feels unresponsive and bloated | Cap UI micro-interactions at `150ms - 250ms` |
| Keyframes for rapid UI | Restarts abruptly upon re-trigger | Use interruptible CSS transitions or springs |
| Sticky touch hover | Mobile button looks active after tap finishes | Wrap hover rules in `@media (hover: hover) and (pointer: fine)` |
| Raw Unicode emojis in UI | Degrades visual craft into generic template slop | Use custom inline SVG vectors with `currentColor` |

---

## 🏎️ 7. Frame-Rate-Independent DeltaTime Physics

For custom canvas simulations, magnetic cursors, or interactive comparison sliders:
```javascript
let currentX = 0;
let targetX = 0;
let lastTime = performance.now();
const lambda = 14; // Decay rate constant

function updatePosition(currentTime) {
  const dt = Math.min((currentTime - lastTime) / 1000, 0.1);
  lastTime = currentTime;
  
  const alpha = 1 - Math.exp(-lambda * dt);
  currentX += (targetX - currentX) * alpha;
  element.style.transform = `translate3d(${currentX.toFixed(2)}px, 0, 0)`;
  
  if (Math.abs(targetX - currentX) > 0.05) {
    requestAnimationFrame(updatePosition);
  }
}
```
