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

## 2. Thinking State: Collapsible Thinking Accordion with Elapsed Timer
```html
<!-- Accessible AI Reasoning Accordion with CSS Grid 0fr -> 1fr height transition & elapsed timer -->
<div class="rounded-2xl border border-border bg-card/80 backdrop-blur-md shadow-sm overflow-hidden text-xs">
  <button type="button" 
          aria-expanded="true" 
          aria-controls="thinking-accordion-body" 
          id="thinking-accordion-trigger"
          class="w-full flex items-center justify-between px-4 py-3 cursor-pointer select-none text-left hover:bg-muted/40 ease-vibe-spring transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary" 
          onclick="const b = document.getElementById('thinking-accordion-wrapper'); const exp = this.getAttribute('aria-expanded') === 'true'; this.setAttribute('aria-expanded', !exp); b.classList.toggle('grid-rows-[1fr]'); b.classList.toggle('grid-rows-[0fr]'); document.getElementById('thinking-chevron').classList.toggle('rotate-180');">
    <div class="flex items-center gap-3">
      <!-- Radar Pulse Indicator -->
      <span class="relative flex h-3 w-3">
        <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-primary/60 opacity-75"></span>
        <span class="relative inline-flex rounded-full h-3 w-3 bg-primary"></span>
      </span>
      <span class="font-semibold font-mono text-foreground flex items-center gap-2">
        <span>Reasoning Architecture</span>
        <span class="text-[10px] font-normal px-2 py-0.5 rounded-full bg-primary/10 text-primary border border-primary/20">Active</span>
      </span>
    </div>
    <div class="flex items-center gap-3">
      <!-- Elapsed Timer Badge -->
      <span class="font-mono text-[11px] text-muted-foreground flex items-center gap-1.5 bg-muted/60 px-2 py-0.5 rounded-md border border-border/40">
        <svg class="w-3 h-3 text-muted-foreground" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
        <bdi id="thinking-elapsed-timer">Thinking (2.4s)...</bdi>
      </span>
      <!-- Chevron Indicator -->
      <svg id="thinking-chevron" class="w-4 h-4 text-muted-foreground ease-vibe-spring transition-all duration-300 transform rotate-180" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
      </svg>
    </div>
  </button>
  
  <!-- CSS Grid Height Transition Container -->
  <div id="thinking-accordion-wrapper" class="grid grid-rows-[1fr] ease-vibe-spring transition-all duration-300">
    <div class="overflow-hidden">
      <div id="thinking-accordion-body" role="region" aria-labelledby="thinking-accordion-trigger" class="px-4 pb-4 pt-1 space-y-2.5 border-t border-border/40 font-mono text-[11px]">
        <!-- Step 1: Completed -->
        <div class="flex items-start justify-between p-2 rounded-lg bg-muted/30 border border-border/40">
          <div class="flex items-center gap-2">
            <span class="w-4 h-4 rounded-full bg-emerald-500/10 text-emerald-500 flex items-center justify-center text-[10px] font-bold">✓</span>
            <span class="text-foreground">Parsed prompt intent & calculated ambiguity budget</span>
          </div>
          <span class="text-muted-foreground text-[10px]">18ms</span>
        </div>
        <!-- Step 2: Completed -->
        <div class="flex items-start justify-between p-2 rounded-lg bg-muted/30 border border-border/40">
          <div class="flex items-center gap-2">
            <span class="w-4 h-4 rounded-full bg-emerald-500/10 text-emerald-500 flex items-center justify-center text-[10px] font-bold">✓</span>
            <span class="text-foreground">Audited color tokens in OKLCH space (contrast >= 4.5:1)</span>
          </div>
          <span class="text-muted-foreground text-[10px]">42ms</span>
        </div>
        <!-- Step 3: In-Progress -->
        <div class="flex items-start justify-between p-2 rounded-lg bg-primary/5 border border-primary/20">
          <div class="flex items-center gap-2">
            <div class="w-3.5 h-3.5 rounded-full border-2 border-primary border-t-transparent animate-spin"></div>
            <span class="text-foreground font-semibold">Synthesizing responsive Tailwind v4 grid layout</span>
          </div>
          <span class="text-primary font-bold text-[10px]">running</span>
        </div>
      </div>
    </div>
  </div>
</div>
```

---

## 3. Streaming Text: Smooth Token Cursor with Stop/Resume Controls
```html
<!-- AI Live Streaming Response with Smooth Cursor, Speed Telemetry, and Interactive Play/Pause/Stop HUD -->
<div class="rounded-2xl border border-border bg-card shadow-md p-5 text-foreground space-y-4">
  <!-- Header Telemetry Bar -->
  <div class="flex items-center justify-between pb-3 border-b border-border text-xs">
    <div class="flex items-center gap-2">
      <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
      <span class="font-mono font-medium text-muted-foreground">claude-3-5-sonnet</span>
    </div>
    <div class="flex items-center gap-3 font-mono text-[11px] text-muted-foreground">
      <span><bdi>48.2 tok/s</bdi></span>
      <span>•</span>
      <span><bdi>384 tokens</bdi></span>
    </div>
  </div>

  <!-- Streaming Message Text with Smooth Token Cursor -->
  <div class="text-sm leading-relaxed font-sans text-foreground/90 space-y-2">
    <p>
      The generated design system establishes a high-fidelity light-first canonical foundation, mapping semantic OKLCH tokens to CSS custom properties with strict WCAG AA contrast compliance.
      <!-- Smooth Animated Token Cursor -->
      <span class="inline-block w-1.5 h-4.5 bg-primary ms-1 align-middle rounded-sm animate-pulse shadow-[0_0_8px_rgba(99,102,241,0.6)]"></span>
    </p>
  </div>

  <!-- Stream Control HUD Actions -->
  <div class="flex items-center justify-between pt-3 border-t border-border text-xs">
    <div class="flex items-center gap-2">
      <!-- Pause / Resume Button -->
      <button type="button" 
              class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-border bg-muted/50 hover:bg-muted text-foreground font-medium ease-vibe-spring transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary">
        <svg class="w-3.5 h-3.5 text-muted-foreground" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 9v6m4-6v6m7-3a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
        <span>Pause Stream</span>
      </button>
      <!-- Stop Generation Button -->
      <button type="button" 
              class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-rose-500/30 bg-rose-500/10 hover:bg-rose-500/20 text-rose-500 font-medium ease-vibe-spring transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-rose-500">
        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 10a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1h-4a1 1 0 01-1-1v-4z" /></svg>
        <span>Stop</span>
      </button>
    </div>

    <!-- Copy & Auto-scroll Toggle -->
    <div class="flex items-center gap-3">
      <label class="inline-flex items-center gap-2 text-muted-foreground text-[11px] cursor-pointer select-none">
        <input type="checkbox" checked class="rounded border-border text-primary focus:ring-primary w-3.5 h-3.5">
        <span>Auto-scroll</span>
      </label>
      <button type="button" class="p-1.5 rounded-lg text-muted-foreground hover:text-foreground hover:bg-muted ease-vibe-spring transition-all" title="Copy to clipboard">
        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" /></svg>
      </button>
    </div>
  </div>
</div>
```

---

## 4. Human-in-the-Loop Approval Blocks: Critical Mutation Permission Gate
```html
<!-- High-Contrast Human-in-the-Loop Approval Gate with Risk Severity Badges, Diff Preview, and Security Countdown -->
<div class="rounded-2xl border-2 border-amber-500/40 bg-card p-6 shadow-2xl space-y-4 max-w-xl">
  <!-- Header: Severity & Target Resource -->
  <div class="flex items-start justify-between">
    <div class="flex items-center gap-3">
      <div class="p-2.5 rounded-xl bg-amber-500/10 text-amber-500 border border-amber-500/20">
        <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>
      </div>
      <div>
        <div class="flex items-center gap-2">
          <span class="px-2 py-0.5 rounded text-[10px] font-bold font-mono tracking-wider bg-amber-500/20 text-amber-600 dark:text-amber-400 border border-amber-500/30">
            HIGH-PRIVILEGE MUTATION
          </span>
          <span class="text-xs text-muted-foreground font-mono">auto-reject in 58s</span>
        </div>
        <h4 class="text-base font-bold text-foreground mt-0.5">Approve Database Schema Migration</h4>
      </div>
    </div>
  </div>

  <!-- Operational Summary & Monospace Parameter Diff -->
  <p class="text-xs text-muted-foreground leading-relaxed">
    The agent requested permission to apply destructive column mutations to the production PostgreSQL cluster. Review the proposed SQL statement before execution:
  </p>

  <div class="rounded-xl border border-border bg-muted/60 p-3 font-mono text-xs overflow-x-auto space-y-1">
    <div class="text-[10px] uppercase text-muted-foreground tracking-wider pb-1 border-b border-border/50">SQL Mutation Payload:</div>
    <div class="flex text-rose-500 bg-rose-500/10 px-2 py-0.5 rounded"><span class="w-6 select-none">-</span><code>ALTER TABLE users DROP COLUMN legacy_auth_hash;</code></div>
    <div class="flex text-emerald-500 bg-emerald-500/10 px-2 py-0.5 rounded"><span class="w-6 select-none">+</span><code>ALTER TABLE users ADD COLUMN passkey_credential_id VARCHAR(255);</code></div>
  </div>

  <!-- Impact Metadata Chips -->
  <div class="flex flex-wrap items-center gap-2 text-[11px] font-mono">
    <span class="px-2.5 py-1 rounded-md bg-muted text-muted-foreground border border-border">Target: prod_db_us_east</span>
    <span class="px-2.5 py-1 rounded-md bg-muted text-muted-foreground border border-border">Estimated lock: ~45ms</span>
    <span class="px-2.5 py-1 rounded-md bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border border-emerald-500/20">Backup Verified ✓</span>
  </div>

  <!-- Decision Action Buttons -->
  <div class="flex items-center justify-between pt-2">
    <button type="button" class="text-xs text-muted-foreground hover:text-foreground font-medium underline underline-offset-4">
      Modify Parameters
    </button>
    <div class="flex items-center gap-2.5">
      <button type="button" class="px-4 py-2 rounded-xl text-xs font-semibold border border-border bg-muted/50 hover:bg-muted text-foreground ease-vibe-spring transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-border">
        Decline (Esc)
      </button>
      <button type="button" class="px-5 py-2 rounded-xl text-xs font-bold bg-amber-500 text-slate-950 hover:bg-amber-400 shadow-lg shadow-amber-500/20 ease-vibe-spring transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-amber-500">
        Approve & Execute (↵)
      </button>
    </div>
  </div>
</div>
```

---

## 5. Tool Invocation Chips & Cards: Real-Time Status Badges (Running, Success, Error)
```html
<!-- Multi-State Tool Invocation Suite: Compact Inline Chips & Expanded Execution Cards -->
<div class="space-y-4">
  <!-- A. Compact Inline Status Chips -->
  <div class="flex flex-wrap items-center gap-2">
    <!-- Running State Chip -->
    <div class="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-indigo-500/10 border border-indigo-500/30 text-xs">
      <div class="w-3 h-3 rounded-full border-2 border-indigo-500 border-t-transparent animate-spin"></div>
      <span class="text-muted-foreground font-mono">tool:</span>
      <span class="font-mono font-semibold text-foreground">vector_search</span>
      <span class="px-1.5 py-0.2 rounded bg-indigo-500/20 text-indigo-500 font-mono text-[10px]">running 210ms</span>
    </div>

    <!-- Success State Chip -->
    <div class="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-xs">
      <svg class="w-3.5 h-3.5 text-emerald-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" /></svg>
      <span class="text-muted-foreground font-mono">tool:</span>
      <span class="font-mono font-semibold text-foreground">contrast_lint</span>
      <span class="px-1.5 py-0.2 rounded bg-emerald-500/20 text-emerald-600 dark:text-emerald-400 font-mono text-[10px]">18ms (Passed)</span>
    </div>

    <!-- Error State Chip -->
    <div class="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-rose-500/10 border border-rose-500/30 text-xs">
      <svg class="w-3.5 h-3.5 text-rose-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
      <span class="text-muted-foreground font-mono">tool:</span>
      <span class="font-mono font-semibold text-foreground">fetch_schema</span>
      <span class="px-1.5 py-0.2 rounded bg-rose-500/20 text-rose-600 dark:text-rose-400 font-mono text-[10px]">failed: E_TIMEOUT</span>
    </div>
  </div>

  <!-- B. Expanded Execution Card with Arguments & Return Payload -->
  <div class="rounded-xl border border-border bg-card p-4 shadow-sm text-xs space-y-3 max-w-lg">
    <div class="flex items-center justify-between">
      <div class="flex items-center gap-2">
        <span class="p-1.5 rounded-lg bg-primary/10 text-primary">
          <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" /></svg>
        </span>
        <span class="font-mono font-bold text-foreground">vector_search(query, k=5)</span>
      </div>
      <span class="px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-500 text-[10px] font-mono font-bold border border-emerald-500/20">
        Status 200 • 34ms
      </span>
    </div>

    <!-- Arguments Tray -->
    <div class="rounded-lg bg-muted/60 p-2.5 font-mono text-[11px] text-muted-foreground">
      <span class="text-foreground/70 font-semibold">Args:</span> { "query": "Tailwind v4 @theme configuration", "limit": 5, "rerank": true }
    </div>

    <!-- Output Summary -->
    <div class="flex items-center justify-between text-[11px] text-muted-foreground pt-1 border-t border-border/40">
      <span>Returned 5 high-confidence chunks (max score: 0.94)</span>
      <button type="button" class="text-primary hover:underline font-mono">Inspect Payload →</button>
    </div>
  </div>
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


---

## 21. Artifact Canvas Workspace Split-Pane: Interactive Agent Sidecar Workspace
```html
<!-- Split-Pane Agent Workspace with Conversational Stream on Left and Living Artifact Canvas on Right -->
<div class="grid grid-cols-1 lg:grid-cols-12 rounded-2xl border border-border bg-canvas overflow-hidden shadow-2xl min-h-[580px]">
  <!-- Left Column: Conversational Agent Chat Stream (5 cols) -->
  <div class="lg:col-span-5 flex flex-col justify-between border-b lg:border-b-0 lg:border-e border-border bg-card/60 p-4 space-y-4">
    <div class="space-y-3">
      <!-- Session Header -->
      <div class="flex items-center justify-between pb-3 border-b border-border text-xs">
        <div class="flex items-center gap-2">
          <span class="w-2.5 h-2.5 rounded-full bg-primary animate-pulse"></span>
          <span class="font-bold text-foreground font-mono">Vibe Assistant Swarm</span>
        </div>
        <span class="text-[11px] font-mono text-muted-foreground">Session #4092</span>
      </div>

      <!-- Agent Message -->
      <div class="p-3 rounded-xl bg-muted/50 text-xs text-foreground leading-relaxed space-y-2">
        <p>I have designed and synthesized the interactive <strong>DesignGenomeHero</strong> component with dual-theme Tailwind v4 variables.</p>
        <div class="inline-flex items-center gap-2 px-2.5 py-1 rounded-lg bg-primary/10 border border-primary/20 text-[11px] font-mono text-primary">
          <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
          <span>Rendered Artifact: DesignGenomeHero.tsx</span>
        </div>
      </div>
    </div>

    <!-- Chat Prompt Input HUD -->
    <div class="relative flex items-center rounded-xl bg-card border border-border p-1.5 shadow-sm">
      <input type="text" placeholder="Refine artifact or ask question..." class="w-full bg-transparent px-2.5 text-xs text-foreground placeholder-muted-foreground focus:outline-none">
      <button class="p-1.5 rounded-lg bg-primary text-primary-foreground hover:opacity-90">
        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"/></svg>
      </button>
    </div>
  </div>

  <!-- Right Column: Living Artifact Canvas (7 cols) -->
  <div class="lg:col-span-7 flex flex-col bg-card/90">
    <!-- Artifact Toolbar -->
    <div class="flex items-center justify-between px-4 py-2.5 border-b border-border bg-muted/40 text-xs">
      <div class="flex items-center gap-3">
        <span class="font-mono font-bold text-foreground">DesignGenomeHero.tsx</span>
        <span class="px-2 py-0.5 rounded-md bg-primary/10 text-primary font-mono text-[10px] font-semibold">v2.1</span>
      </div>

      <!-- Tab Switcher: Preview / Code / Diff -->
      <div class="flex items-center rounded-lg bg-muted p-0.5 text-[11px] font-medium text-muted-foreground">
        <button class="px-2.5 py-1 rounded-md bg-card text-foreground shadow-sm font-semibold">Preview</button>
        <button class="px-2.5 py-1 rounded-md hover:text-foreground">Code</button>
        <button class="px-2.5 py-1 rounded-md hover:text-foreground">Diff</button>
      </div>

      <!-- Action Icons: Copy, Popout, Re-run -->
      <div class="flex items-center gap-1.5 text-muted-foreground">
        <button class="p-1 rounded hover:bg-muted hover:text-foreground" title="Copy code"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"/></svg></button>
        <button class="p-1 rounded hover:bg-muted hover:text-foreground" title="Fullscreen popout"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/></svg></button>
      </div>
    </div>

    <!-- Living Preview Container / Sandboxed Canvas -->
    <div class="flex-1 p-6 flex items-center justify-center bg-canvas/50">
      <div class="w-full max-w-md p-6 rounded-2xl border border-border bg-card shadow-lg text-center space-y-3">
        <div class="w-10 h-10 rounded-xl bg-primary/10 text-primary flex items-center justify-center mx-auto">
          <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>
        </div>
        <h3 class="text-base font-bold text-foreground">Interactive Hero Prototype</h3>
        <p class="text-xs text-muted-foreground">Rendered live inside the artifact sandbox with active Spring physics.</p>
        <button class="px-4 py-2 rounded-xl bg-primary text-primary-foreground text-xs font-bold shadow-md hover:opacity-90 ease-vibe-spring transition-all">
          Explore Features
        </button>
      </div>
    </div>
  </div>
</div>
```
