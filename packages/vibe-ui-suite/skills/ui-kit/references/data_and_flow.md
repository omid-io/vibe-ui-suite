# 📊 Data Visualization, Canvas & Workflow Primitives

Framework-agnostic components for workflow builders, interactive canvas nodes, live insight metrics, and data comparison.

---

## 1. Interactive Flowchart / Automation Canvas Node (Beautiful UI)

Renders node triggers, conditional branching, and action executions on a modular canvas.

```html
<div class="flowchart-canvas relative rounded-3xl border border-border bg-background p-8 overflow-hidden">
  <!-- Dotted Canvas Grid Background -->
  <div class="absolute inset-0 bg-[radial-gradient(currentColor_1px,transparent_1px)] [background-size:16px_16px] text-border/60 pointer-events-none"></div>

  <div class="relative z-10 flex flex-col items-center space-y-5 max-w-sm mx-auto">
    <!-- Trigger Node -->
    <div class="w-full rounded-2xl border border-border bg-card/90 p-4 shadow-xl backdrop-blur-xl">
      <div class="flex items-center justify-between">
        <span class="px-2 py-0.5 rounded bg-primary/10 text-primary text-[10px] font-bold uppercase tracking-wider">Trigger</span>
        <svg class="w-4 h-4 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>
      </div>
      <h5 class="mt-2 text-xs font-bold text-foreground">Webhook Event Received</h5>
      <p class="text-[11px] text-muted-foreground mt-0.5">Payload ingested from external service</p>
    </div>

    <!-- Connector -->
    <div class="w-0.5 h-6 bg-border"></div>

    <!-- Conditional Node -->
    <div class="w-full rounded-2xl border border-border bg-card/90 p-4 shadow-xl backdrop-blur-xl">
      <div class="flex items-center justify-between">
        <span class="px-2 py-0.5 rounded bg-amber-500/10 text-amber-500 text-[10px] font-bold uppercase tracking-wider">If / Else Rule</span>
        <svg class="w-4 h-4 text-amber-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4"/></svg>
      </div>
      <div class="mt-2 p-2.5 rounded-xl bg-muted/60 border border-border text-xs text-foreground font-mono space-y-1">
        <div><span class="text-amber-500">IF</span> response_code === 200</div>
        <div><span class="text-primary">AND</span> confidence_score > 0.85</div>
      </div>
    </div>

    <!-- Connector -->
    <div class="w-0.5 h-6 bg-border"></div>

    <!-- Action Node -->
    <div class="w-full rounded-2xl border border-emerald-500/30 bg-card/90 p-4 shadow-xl backdrop-blur-xl">
      <div class="flex items-center justify-between">
        <span class="px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-500 text-[10px] font-bold uppercase tracking-wider">Action</span>
        <svg class="w-4 h-4 text-emerald-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>
      </div>
      <h5 class="mt-2 text-xs font-bold text-foreground">Execute Notification Pipeline</h5>
    </div>
  </div>
</div>
```

---

## 2. Live Insight Cards with Scrubbable Sparklines

Real-time metric summary card with percentage deltas and inline vector charts.

```html
<div class="insight-card rounded-2xl border border-border bg-card/80 p-5 backdrop-blur-xl shadow-lg">
  <div class="flex items-center justify-between">
    <div>
      <span class="text-xs font-medium text-muted-foreground">Monthly Active Inferences</span>
      <div class="mt-1 flex items-baseline gap-2">
        <span class="text-2xl font-black text-foreground font-mono tracking-tight">1,429,800</span>
      </div>
    </div>
    <div class="flex items-center gap-1 px-2.5 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-500 text-xs font-bold font-mono">
      <span>+24.8%</span>
      <svg class="w-3.5 h-3.5 transform -rotate-45" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 10l7-7m0 0l7 7m-7-7v18"/></svg>
    </div>
  </div>

  <!-- SVG Sparkline Trend -->
  <div class="mt-4 pt-2">
    <svg class="w-full h-12 stroke-primary fill-none" viewBox="0 0 200 40">
      <path d="M0,32 Q30,8 60,20 T120,12 T160,4 T200,6" stroke-width="2.5" stroke-linecap="round" />
      <path d="M0,32 Q30,8 60,20 T120,12 T160,4 T200,6 L200,40 L0,40 Z" fill="currentColor" class="text-primary/10" />
    </svg>
  </div>
</div>
```

---

## 3. Data & Code Diff Table Viewer

Two-column or line-by-line diff comparison with syntax coloring.

```html
<div class="diff-table-container rounded-2xl border border-border bg-muted/40 p-4 font-mono text-xs overflow-x-auto">
  <div class="space-y-1">
    <!-- Removed Row -->
    <div class="flex items-center bg-rose-500/10 text-rose-500 px-3 py-1.5 rounded-lg border border-rose-500/20">
      <span class="w-8 select-none text-rose-400">- 14</span>
      <code>const modelConfig = { temperature: 0.9, maxTokens: 500 };</code>
    </div>
    <!-- Added Row -->
    <div class="flex items-center bg-emerald-500/10 text-emerald-500 px-3 py-1.5 rounded-lg border border-emerald-500/20">
      <span class="w-8 select-none text-emerald-400">+ 14</span>
      <code>const modelConfig = { temperature: 0.2, maxTokens: 2048, streaming: true };</code>
    </div>
  </div>
</div>
```
