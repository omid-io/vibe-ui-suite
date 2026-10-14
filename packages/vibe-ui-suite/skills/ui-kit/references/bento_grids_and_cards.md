# 🍱 Bento Grids & Micro-Interactions Catalog (BeUI & Rare UI)

Complete catalog of modern Bento grid layouts, glassmorphism cards, interactive metric HUDs, and ambient glow containers.

---

## 1. Bento Grid Archetypes

### 1.1 The 3-Column Asymmetric Matrix (Product / SaaS Hero)
```html
<div class="grid grid-cols-1 md:grid-cols-3 gap-4 max-w-6xl mx-auto">
  <!-- Card A: Span 2 Cols (Hero Feature) -->
  <div class="md:col-span-2 rounded-3xl border border-border bg-card/60 p-6 backdrop-blur-xl flex flex-col justify-between hover:border-primary/40 transition-all shadow-lg">
    <div>
      <span class="px-2.5 py-1 rounded-full bg-primary/10 text-primary text-xs font-semibold">Flagship Engine</span>
      <h3 class="text-xl font-bold text-foreground mt-3">Autonomous Multi-Agent Orchestration</h3>
      <p class="text-xs text-muted-foreground mt-1 max-w-md">Decompose complex user objectives into parallelized sub-tasks with real-time feedback loops.</p>
    </div>
    <div class="mt-6 h-36 rounded-2xl bg-muted/40 border border-border flex items-center justify-center font-mono text-xs text-muted-foreground">
      [Interactive Subagent Graph Canvas]
    </div>
  </div>

  <!-- Card B: Span 1 Col (Telemetry / Latency) -->
  <div class="rounded-3xl border border-border bg-card/60 p-6 backdrop-blur-xl flex flex-col justify-between hover:border-primary/40 transition-all shadow-lg">
    <div>
      <span class="text-xs font-medium text-muted-foreground">P99 Inference Latency</span>
      <div class="text-3xl font-black text-foreground font-mono mt-2">12.4ms</div>
      <span class="text-emerald-500 font-mono text-xs font-semibold">↑ 400% throughput gain</span>
    </div>
    <div class="mt-4 pt-4 border-t border-border/40 text-xs text-muted-foreground">
      Compiled with hardware-level AVX-512 acceleration.
    </div>
  </div>

  <!-- Card C: Span 1 Col (Security Shield) -->
  <div class="rounded-3xl border border-border bg-card/60 p-6 backdrop-blur-xl hover:border-primary/40 transition-all shadow-lg">
    <div class="w-8 h-8 rounded-xl bg-primary/10 text-primary flex items-center justify-center mb-3">
      <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/></svg>
    </div>
    <h4 class="text-sm font-bold text-foreground">Zero-Trust Sandbox</h4>
    <p class="text-xs text-muted-foreground mt-1">Every code generation task runs in an isolated ephemeral container.</p>
  </div>

  <!-- Card D: Span 2 Cols (Global Mesh Network) -->
  <div class="md:col-span-2 rounded-3xl border border-border bg-card/60 p-6 backdrop-blur-xl flex items-center justify-between hover:border-primary/40 transition-all shadow-lg">
    <div>
      <h4 class="text-base font-bold text-foreground">Distributed Edge Deployment</h4>
      <p class="text-xs text-muted-foreground mt-1">Replicate models across 35 global edge locations instantly.</p>
    </div>
    <button class="px-4 py-2 rounded-xl bg-primary text-primary-foreground text-xs font-bold shrink-0">Configure Mesh</button>
  </div>
</div>
```

---

## 2. Interactive Micro-Interactions (BeUI & Rare UI)

### 2.1 Animated Gradient Shimmer Border Button
```html
<button class="relative inline-flex items-center justify-center p-0.5 overflow-hidden rounded-2xl font-bold group shadow-lg">
  <span class="absolute inset-0 w-full h-full bg-gradient-to-r from-primary via-accent to-secondary rounded-2xl opacity-75 group-hover:opacity-100 transition-opacity duration-300 animate-gradient-x"></span>
  <span class="relative px-5 py-2.5 transition-all ease-out bg-background rounded-[14px] text-xs font-bold text-foreground group-hover:bg-opacity-90 flex items-center gap-2">
    <span>Launch Live Terminal</span>
    <svg class="w-4 h-4 group-hover:translate-x-0.5 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"/></svg>
  </span>
</button>
```

### 2.2 Glassmorphism 2.0 Inset Specular Card
```css
.glass-fresnel-card {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.06) 0%, rgba(255, 255, 255, 0.02) 100%);
  backdrop-filter: blur(24px) saturate(180%);
  -webkit-backdrop-filter: blur(24px) saturate(180%);
  border-radius: 24px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 
    inset 0 1px 1px 0 rgba(255, 255, 255, 0.2), /* Fresnel Highlight */
    0 10px 30px -10px rgba(0, 0, 0, 0.4),
    0 20px 40px -15px rgba(0, 0, 0, 0.6);
}
```

### 2.3 Metric HUD Tile with Live Delta
```html
<div class="p-4 rounded-2xl bg-card border border-border flex items-center justify-between">
  <div>
    <span class="text-[11px] font-medium text-muted-foreground uppercase tracking-wider">Active Concurrency</span>
    <div class="text-2xl font-black font-mono text-foreground mt-0.5">8,420</div>
  </div>
  <div class="px-2.5 py-1 rounded-full bg-emerald-500/10 text-emerald-500 text-xs font-mono font-bold">
    +14.2%
  </div>
</div>
```
