# ⚡ Physics Transitions & Motion Catalog (transitions.dev)

Zero-dependency, high-performance CSS and lightweight JS motion primitives for high-framerate, refresh-rate-aware interfaces.

---

## 1. Zero-JS Dynamic Height Accordion (CSS Grid Interpolation)

Animates naturally to any dynamic height without hardcoding pixel limits or calculating `scrollHeight` in JS.

```html
<div class="accordion-primitive rounded-2xl border border-border bg-card overflow-hidden">
  <button class="w-full flex items-center justify-between p-4 text-start font-semibold text-xs text-foreground" onclick="this.nextElementSibling.classList.toggle('is-open')">
    <span>How is zero-JS expansion calculated?</span>
    <svg class="w-4 h-4 text-muted-foreground transform transition-transform duration-300 group-hover:text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
    </svg>
  </button>
  <div class="grid grid-rows-[0fr] transition-[grid-template-rows] duration-300 ease-[cubic-bezier(0.16,1,0.3,1)] [&.is-open]:grid-rows-[1fr]">
    <div class="overflow-hidden px-4 pb-4 text-xs text-muted-foreground leading-relaxed border-t border-border/50 pt-3">
      By transitioning CSS Grid rows from `0fr` to `1fr`, the browser computes the natural layout height on the composite layer without triggering multiple expensive reflows.
    </div>
  </div>
</div>
```

---

## 2. Spring Physics Easing Curves & Presets

Standard cubic-bezier curves for fluid, tactile, Apple-grade spring physics:

```css
:root {
  /* Fast snappy spring (buttons, toggles, badges) */
  --ease-spring-snappy: cubic-bezier(0.34, 1.56, 0.64, 1);
  
  /* Smooth gentle deceleration (sheets, dialogs, drawers) */
  --ease-spring-smooth: cubic-bezier(0.16, 1, 0.3, 1);
  
  /* Bouncy elastic (badges, alerts, popover enter) */
  --ease-spring-elastic: cubic-bezier(0.68, -0.6, 0.32, 1.6);
}
```

---

## 3. Staggered List Entrance (Fade & Slide-Up)

```html
<ul class="space-y-2">
  <li class="p-3 rounded-xl bg-card border border-border text-xs animate-in fade-in slide-in-from-bottom-2 duration-200 fill-mode-both" style="animation-delay: 50ms;">
    Cluster Node A initialized
  </li>
  <li class="p-3 rounded-xl bg-card border border-border text-xs animate-in fade-in slide-in-from-bottom-2 duration-200 fill-mode-both" style="animation-delay: 100ms;">
    PostgreSQL replica synced
  </li>
  <li class="p-3 rounded-xl bg-card border border-border text-xs animate-in fade-in slide-in-from-bottom-2 duration-200 fill-mode-both" style="animation-delay: 150ms;">
    Edge workers ready
  </li>
</ul>
```

---

## 4. Number Flip Counter (Lightweight JS Primitive)

```html
<div class="font-mono text-2xl font-black text-foreground" id="metric-counter" data-target="14280">0</div>

<script>
function animateCounter(el, target, duration = 1200) {
  const start = 0;
  const startTime = performance.now();
  function update(currentTime) {
    const elapsed = currentTime - startTime;
    const progress = Math.min(elapsed / duration, 1);
    const easeProgress = 1 - Math.pow(1 - progress, 4); // easeOutQuart
    el.textContent = Math.floor(start + (target - start) * easeProgress).toLocaleString();
    if (progress < 1) requestAnimationFrame(update);
  }
  requestAnimationFrame(update);
}
// Usage: animateCounter(document.getElementById('metric-counter'), 14280);
</script>
```

---

## 5. 3D Card Tilt Interaction (Mouse Follow)

```javascript
document.querySelectorAll('.tilt-card').forEach(card => {
  card.addEventListener('mousemove', (e) => {
    const rect = card.getBoundingClientRect();
    const x = e.clientX - rect.left - rect.width / 2;
    const y = e.clientY - rect.top - rect.height / 2;
    card.style.transform = `perspective(1000px) rotateX(${-y / 15}deg) rotateY(${x / 15}deg) scale3d(1.02, 1.02, 1.02)`;
  });
  card.addEventListener('mouseleave', () => {
    card.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1)';
  });
});
```
