# 🤖 AI-Native Primitives: Complete 20-Component Catalog (beautifului.dev)

This catalog contains the complete, production-ready implementation of all 20 AI-native UI primitives from **Beautiful UI**, with zero external dependencies and full Tailwind CSS / framework-agnostic markup.

---

## 1. Loading State (AI In-Flight Pulse)
```html
<div class="flex items-center gap-3 p-3 rounded-xl bg-card border border-border">
  <div class="relative flex h-3 w-3">
    <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-primary opacity-75"></span>
    <span class="relative inline-flex rounded-full h-3 w-3 bg-primary"></span>
  </div>
  <span class="text-xs font-mono text-muted-foreground animate-pulse">Model synthesizing response...</span>
</div>
```

---

## 2. Thinking State (Collapsible Reasoning Box)
```html
<div class="rounded-xl border border-border bg-card/70 p-3.5 backdrop-blur-md">
  <button type="button" 
          aria-expanded="true" 
          aria-controls="thought-content-1" 
          class="w-full flex items-center justify-between cursor-pointer select-none text-left focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary rounded-lg p-0.5" 
          onclick="const b = document.getElementById('thought-content-1'); const exp = this.getAttribute('aria-expanded') === 'true'; this.setAttribute('aria-expanded', !exp); b.classList.toggle('hidden');">
    <div class="flex items-center gap-2.5">
      <svg class="w-4 h-4 text-primary animate-spin" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" /></svg>
      <span class="text-xs font-semibold font-mono text-foreground">Thought Process</span>
    </div>
    <span class="text-[11px] text-muted-foreground font-mono">4 steps</span>
  </button>
  <div id="thought-content-1" class="thought-body mt-3 pt-2.5 border-t border-border/50 text-xs font-mono text-muted-foreground space-y-1">
    <div>1. Scanning AST nodes for dependency cycle</div>
    <div>2. Optimizing memoization hooks</div>
    <div class="text-emerald-500 font-semibold">✓ Ready to output refactored component</div>
  </div>
</div>
```

---

## 3. Streaming Text (With Smooth Token Cursor)
```html
<div class="p-4 rounded-xl bg-card border border-border text-foreground text-sm leading-relaxed font-sans">
  <span>The computed gradient tensor converges after 450 epochs with a loss of 0.012.</span>
  <span class="inline-block w-1.5 h-4 bg-primary align-middle ms-1 rounded-sm animate-pulse"></span>
</div>
```

---

## 4. Approval Card (Human-in-the-Loop Gate)
```html
<div class="rounded-2xl border border-border bg-card/95 p-5 shadow-xl">
  <div class="flex items-start gap-3">
    <div class="p-2 rounded-xl bg-amber-500/10 text-amber-500 border border-amber-500/20">
      <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>
    </div>
    <div>
      <h4 class="text-sm font-bold text-foreground">Review Proposed Changes</h4>
      <p class="text-xs text-muted-foreground mt-0.5">Agent requested write access to target database.</p>
    </div>
  </div>
  <div class="mt-4 flex justify-end gap-2">
    <button class="px-3.5 py-1.5 rounded-lg text-xs font-medium text-muted-foreground hover:bg-muted">Decline</button>
    <button class="px-4 py-1.5 rounded-lg text-xs font-bold bg-primary text-primary-foreground hover:opacity-90">Approve</button>
  </div>
</div>
```

---

## 5. Tool Chips (Execution Status Badges)
```html
<div class="inline-flex items-center gap-2 px-2.5 py-1 rounded-lg bg-secondary/80 border border-border text-xs">
  <svg class="w-3.5 h-3.5 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"/></svg>
  <span class="text-muted-foreground font-mono">tool:</span>
  <span class="text-foreground font-mono font-medium">vector_search</span>
  <span class="px-1.5 py-0.5 rounded bg-emerald-500/10 text-emerald-500 text-[10px] font-mono">18ms</span>
</div>
```

---

## 6. Task Rows (Agent Multi-Step Checklist)
```html
<div class="space-y-1.5">
  <div class="flex items-center justify-between p-2.5 rounded-lg bg-card border border-border text-xs">
    <div class="flex items-center gap-2">
      <span class="w-4 h-4 rounded-full bg-emerald-500/10 text-emerald-500 flex items-center justify-center text-[10px] font-bold">✓</span>
      <span class="text-foreground">Fetch user schema</span>
    </div>
    <span class="text-muted-foreground font-mono text-[11px]">Done</span>
  </div>
  <div class="flex items-center justify-between p-2.5 rounded-lg bg-primary/5 border border-primary/20 text-xs">
    <div class="flex items-center gap-2">
      <div class="w-3.5 h-3.5 rounded-full border-2 border-primary border-t-transparent animate-spin"></div>
      <span class="text-foreground font-semibold">Generate Prisma migration</span>
    </div>
    <span class="text-primary font-mono text-[11px]">Running</span>
  </div>
</div>
```

---

## 7. Chat Container (Agent & User Message Bubbles)
```html
<div class="space-y-3 p-4 rounded-2xl bg-card border border-border max-w-xl">
  <div class="flex gap-3">
    <div class="w-7 h-7 rounded-full bg-primary/20 text-primary flex items-center justify-center font-bold text-xs">AI</div>
    <div class="p-3 rounded-2xl bg-muted/60 text-xs text-foreground leading-relaxed max-w-[85%]">
      I have analyzed the endpoint and prepared the index optimizations.
    </div>
  </div>
  <div class="flex gap-3 flex-row-reverse">
    <div class="w-7 h-7 rounded-full bg-secondary text-foreground flex items-center justify-center font-bold text-xs">U</div>
    <div class="p-3 rounded-2xl bg-primary text-primary-foreground text-xs leading-relaxed max-w-[85%]">
      Great, run the migration now.
    </div>
  </div>
</div>
```

---

## 8. Prompt Bar (Floating Input HUD)
```html
<div class="relative flex items-center rounded-2xl bg-card/90 border border-border p-2 shadow-2xl backdrop-blur-xl focus-within:border-primary">
  <input type="text" placeholder="Type prompt or command..." class="w-full bg-transparent px-3 text-xs text-foreground placeholder-muted-foreground focus:outline-none">
  <button class="p-2 rounded-xl bg-primary text-primary-foreground hover:opacity-90">
    <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"/></svg>
  </button>
</div>
```

---

## 9. Recommendation Card (Proactive Agent Suggestions)
```html
<div class="rounded-2xl border border-border bg-card p-4 hover:border-primary/50 transition-all shadow-sm">
  <div class="flex justify-between items-center text-xs">
    <span class="px-2 py-0.5 rounded-full bg-primary/10 text-primary font-semibold">Suggestion</span>
    <span class="text-muted-foreground font-mono">92% Match</span>
  </div>
  <h5 class="mt-2 text-xs font-bold text-foreground">Add Redis Cache Layer</h5>
  <p class="text-[11px] text-muted-foreground mt-0.5">Reduces database read pressure by 60% on hot routes.</p>
</div>
```

---

## 10. Context Cards (Retrieved Grounding Documents)
```html
<div class="p-3 rounded-xl bg-muted/40 border border-border flex items-center justify-between text-xs">
  <div class="flex items-center gap-2">
    <svg class="w-4 h-4 text-muted-foreground" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
    <span class="font-medium text-foreground">schema_v2.sql</span>
  </div>
  <span class="text-[10px] font-mono text-muted-foreground">Chunk #4 (Score: 0.89)</span>
</div>
```

---

## 11. Diff Table (Line-by-Line Code/Data Delta)
```html
<div class="rounded-xl border border-border bg-muted/50 p-3 font-mono text-xs overflow-x-auto space-y-1">
  <div class="flex bg-rose-500/10 text-rose-500 px-2 py-1 rounded"><span class="w-6 select-none">-</span><code>cache.set(key, val, 300);</code></div>
  <div class="flex bg-emerald-500/10 text-emerald-500 px-2 py-1 rounded"><span class="w-6 select-none">+</span><code>cache.set(key, val, { ttl: 3600, tag: 'user' });</code></div>
</div>
```

---

## 12. Records Table (Dense Data Grid with Status)
```html
<div class="rounded-xl border border-border bg-card overflow-hidden text-xs">
  <table class="w-full text-start">
    <thead class="bg-muted text-muted-foreground border-b border-border font-medium">
      <tr><th class="p-3">ID</th><th class="p-3">Task Name</th><th class="p-3">Status</th></tr>
    </thead>
    <tbody class="divide-y divide-border">
      <tr><td class="p-3 font-mono">#104</td><td class="p-3 font-semibold text-foreground">Build Artifacts</td><td class="p-3"><span class="px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-500 text-[10px] font-bold">Passed</span></td></tr>
    </tbody>
  </table>
</div>
```

---

## 13. Filter Table (Pill Filtering Header)
```html
<div class="flex items-center gap-2 p-2 rounded-xl bg-card border border-border text-xs">
  <span class="text-muted-foreground px-2 font-medium">Filter:</span>
  <button class="px-2.5 py-1 rounded-lg bg-primary text-primary-foreground font-semibold">All</button>
  <button class="px-2.5 py-1 rounded-lg bg-muted text-muted-foreground hover:text-foreground">Errors Only</button>
  <button class="px-2.5 py-1 rounded-lg bg-muted text-muted-foreground hover:text-foreground">Latency > 100ms</button>
</div>
```

---

## 14. Sidebar Nav (Agentic Multi-Workspace Navigation)
```html
<nav class="w-64 p-3 rounded-2xl bg-card border border-border space-y-1 text-xs">
  <a href="#" class="flex items-center gap-2.5 px-3 py-2 rounded-xl bg-primary/10 text-primary font-bold">
    <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/></svg>
    <span>Overview</span>
  </a>
  <a href="#" class="flex items-center gap-2.5 px-3 py-2 rounded-xl text-muted-foreground hover:bg-muted hover:text-foreground">
    <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/></svg>
    <span>Agent Tools</span>
  </a>
</nav>
```

---

## 15. Search HUD (Omni-Search with Key Indicator)
```html
<div class="flex items-center justify-between px-3 py-2 rounded-xl bg-card border border-border text-xs text-muted-foreground">
  <div class="flex items-center gap-2">
    <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
    <span>Search actions, tools, sessions...</span>
  </div>
  <kbd class="px-1.5 py-0.5 rounded bg-muted text-[10px] font-mono border border-border">Ctrl K</kbd>
</div>
```

---

## 16. Flowchart (Trigger -> Condition -> Action Canvas)
```html
<div class="p-6 rounded-2xl bg-card border border-border space-y-3 max-w-sm mx-auto text-xs">
  <div class="p-3 rounded-xl border border-primary/30 bg-primary/5 font-semibold text-foreground">Trigger: Event Incoming</div>
  <div class="w-0.5 h-4 bg-border mx-auto"></div>
  <div class="p-3 rounded-xl border border-amber-500/30 bg-amber-500/5 font-semibold text-foreground">Condition: Confidence > 0.9</div>
  <div class="w-0.5 h-4 bg-border mx-auto"></div>
  <div class="p-3 rounded-xl border border-emerald-500/30 bg-emerald-500/5 font-semibold text-foreground">Action: Dispatch Job</div>
</div>
```

---

## 17. Insight Cards (Live Metrics + Inline Sparkline)
```html
<div class="p-4 rounded-2xl bg-card border border-border shadow-sm">
  <div class="flex justify-between items-center text-xs">
    <span class="text-muted-foreground font-medium">Throughput</span>
    <span class="text-emerald-500 font-bold font-mono">+32%</span>
  </div>
  <div class="text-xl font-extrabold text-foreground font-mono mt-1">4.2M req/s</div>
  <svg class="w-full h-8 mt-2 stroke-primary fill-none" viewBox="0 0 100 25">
    <path d="M0,20 Q25,5 50,15 T100,5" stroke-width="2" stroke-linecap="round"/>
  </svg>
</div>
```

---

## 18. Code Block (Syntax Highlight Header + Copy Button)
```html
<div class="rounded-xl border border-border bg-muted/60 overflow-hidden text-xs font-mono">
  <div class="flex items-center justify-between px-3 py-1.5 bg-muted border-b border-border text-muted-foreground">
    <span>handler.ts</span>
    <button class="hover:text-foreground" onclick="navigator.clipboard.writeText('const x = 1;')">Copy</button>
  </div>
  <pre class="p-3 text-foreground overflow-x-auto"><code>const handler = async (req: Request) =&gt; Response.json({ ok: true });</code></pre>
</div>
```

---

## 19. Fine-Tune Card (Hyperparameter Slider & Metrics)
```html
<div class="p-4 rounded-2xl bg-card border border-border space-y-3 text-xs">
  <div class="flex justify-between font-medium text-foreground">
    <span>Temperature:</span>
    <span class="font-mono text-primary font-bold">0.7</span>
  </div>
  <input type="range" min="0" max="1" step="0.05" value="0.7" class="w-full accent-primary">
</div>
```

---

## 20. Selection Actions Bar (Floating Context HUD)
```html
<div class="inline-flex items-center gap-2 p-1.5 rounded-2xl bg-card border border-border shadow-2xl backdrop-blur-xl text-xs">
  <button class="px-3 py-1.5 rounded-xl hover:bg-muted text-foreground font-medium">Summarize</button>
  <button class="px-3 py-1.5 rounded-xl hover:bg-muted text-foreground font-medium">Translate</button>
  <button class="px-3 py-1.5 rounded-xl bg-primary text-primary-foreground font-bold">Explain Code</button>
</div>
```
