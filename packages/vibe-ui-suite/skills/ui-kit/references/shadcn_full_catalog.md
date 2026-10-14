# 🧩 Shadcn UI: Complete 50+ Component Catalog (ui.shadcn.com)

Production-ready, accessible, and theme-token compatible implementations of the entire Shadcn UI component ecosystem.

---

## 1. Forms & Inputs

### 1.1 Input & Textarea
```html
<div class="space-y-1.5 text-xs">
  <label class="font-medium text-foreground">Email Address</label>
  <input type="email" placeholder="name@example.com" class="w-full px-3 py-2 rounded-xl bg-background border border-input text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:border-transparent">
</div>
```

### 1.2 Select Dropdown (Native-Accessible)
```html
<div class="space-y-1.5 text-xs">
  <label class="font-medium text-foreground">Model Family</label>
  <select class="w-full px-3 py-2 rounded-xl bg-background border border-input text-foreground focus:outline-none focus:ring-2 focus:ring-ring">
    <option value="gemini">Gemini 3.7 Pro</option>
    <option value="claude">Claude 3.7 Sonnet</option>
    <option value="gpt">GPT-4o</option>
  </select>
</div>
```

### 1.3 Checkbox & Switch Toggle
```html
<div class="flex items-center gap-4 text-xs">
  <!-- Checkbox -->
  <label class="flex items-center gap-2 cursor-pointer">
    <input type="checkbox" class="w-4 h-4 rounded border-input text-primary focus:ring-ring accent-primary">
    <span class="text-foreground font-medium">Auto-deploy</span>
  </label>
  <!-- Switch -->
  <label class="relative inline-flex items-center cursor-pointer">
    <input type="checkbox" class="sr-only peer">
    <div class="w-9 h-5 bg-input peer-checked:bg-primary rounded-full peer peer-checked:after:translate-x-full after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-background after:rounded-full after:h-4 after:w-4 after:transition-all"></div>
  </label>
</div>
```

### 1.4 Input OTP (One-Time Password Matrix)
```html
<div class="flex gap-2">
  <input maxlength="1" class="w-10 h-12 text-center font-mono font-bold text-lg rounded-xl border border-input bg-background focus:ring-2 focus:ring-ring focus:outline-none">
  <input maxlength="1" class="w-10 h-12 text-center font-mono font-bold text-lg rounded-xl border border-input bg-background focus:ring-2 focus:ring-ring focus:outline-none">
  <input maxlength="1" class="w-10 h-12 text-center font-mono font-bold text-lg rounded-xl border border-input bg-background focus:ring-2 focus:ring-ring focus:outline-none">
  <input maxlength="1" class="w-10 h-12 text-center font-mono font-bold text-lg rounded-xl border border-input bg-background focus:ring-2 focus:ring-ring focus:outline-none">
</div>
```

---

## 2. Overlays & Dialogs

### 2.1 Modal Dialog
```html
<div class="fixed inset-0 z-50 bg-background/80 backdrop-blur-sm flex items-center justify-center p-4">
  <div class="w-full max-w-lg rounded-2xl border border-border bg-card p-6 shadow-2xl space-y-4">
    <div class="flex justify-between items-center">
      <h3 class="text-base font-bold text-foreground">Confirm Cluster Deletion</h3>
      <button class="text-muted-foreground hover:text-foreground">✕</button>
    </div>
    <p class="text-xs text-muted-foreground leading-relaxed">This action cannot be undone. All database partitions will be permanently unmounted.</p>
    <div class="flex justify-end gap-2 pt-2">
      <button class="px-4 py-2 rounded-xl text-xs font-medium text-muted-foreground hover:bg-muted">Cancel</button>
      <button class="px-4 py-2 rounded-xl text-xs font-bold bg-destructive text-destructive-foreground hover:opacity-90">Delete</button>
    </div>
  </div>
</div>
```

### 2.2 Slide-Over Sheet / Drawer
```html
<div class="fixed inset-y-0 end-0 z-50 w-full max-w-md bg-card border-s border-border shadow-2xl p-6 flex flex-col justify-between">
  <div>
    <h3 class="text-base font-bold text-foreground">Inspector Panel</h3>
    <p class="text-xs text-muted-foreground mt-1">Live runtime parameters and memory telemetry.</p>
  </div>
  <button class="w-full py-2.5 rounded-xl bg-primary text-primary-foreground text-xs font-bold">Apply Settings</button>
</div>
```

### 2.3 Popover & Tooltip
```html
<div class="relative group inline-block">
  <button class="px-3 py-1.5 rounded-lg bg-secondary text-secondary-foreground text-xs">Hover Me</button>
  <div class="absolute bottom-full mb-2 left-1/2 -translate-x-1/2 hidden group-hover:block px-2.5 py-1 rounded-md bg-popover border border-border text-[11px] text-popover-foreground shadow-lg whitespace-nowrap">
    Tooltip information
  </div>
</div>
```

---

## 3. Navigation & Structure

### 3.1 Command Palette (`Cmd+K`)
```html
<div class="w-full max-w-lg rounded-2xl border border-border bg-popover shadow-2xl overflow-hidden text-xs">
  <div class="flex items-center px-4 border-b border-border">
    <input type="text" placeholder="Search commands..." class="w-full bg-transparent py-3 text-xs placeholder:text-muted-foreground focus:outline-none">
    <kbd class="px-1.5 py-0.5 rounded bg-muted text-[10px] font-mono text-muted-foreground border border-border">ESC</kbd>
  </div>
  <div class="p-2 space-y-1">
    <button class="w-full flex items-center justify-between px-3 py-2 rounded-lg hover:bg-accent text-start">
      <span>New Project Workspace</span>
      <kbd class="text-[10px] font-mono text-muted-foreground">⌘N</kbd>
    </button>
  </div>
</div>
```

### 3.2 Segmented Tabs
```html
<div class="inline-flex p-1 rounded-xl bg-muted border border-border text-xs">
  <button class="px-4 py-1.5 rounded-lg font-semibold bg-background text-foreground shadow-sm">Metrics</button>
  <button class="px-4 py-1.5 rounded-lg font-medium text-muted-foreground hover:text-foreground">Logs</button>
  <button class="px-4 py-1.5 rounded-lg font-medium text-muted-foreground hover:text-foreground">Config</button>
</div>
```

### 3.3 Breadcrumb Navigation
```html
<nav class="flex items-center gap-2 text-xs text-muted-foreground">
  <a href="#" class="hover:text-foreground">Home</a>
  <span>/</span>
  <a href="#" class="hover:text-foreground">Pipelines</a>
  <span>/</span>
  <span class="text-foreground font-semibold">Production-v3</span>
</nav>
```

---

## 4. Feedback & Status

### 4.1 Sonner / Floating Toast
```html
<div class="fixed bottom-4 end-4 z-50 flex items-center gap-3 p-4 rounded-2xl bg-card border border-border shadow-2xl text-xs max-w-sm">
  <span class="w-2 h-2 rounded-full bg-emerald-500"></span>
  <div class="flex-1">
    <h5 class="font-bold text-foreground">Pipeline Deployed</h5>
    <p class="text-muted-foreground text-[11px]">Successfully synced with 4 worker pods.</p>
  </div>
  <button class="text-muted-foreground hover:text-foreground">✕</button>
</div>
```

### 4.2 Skeleton Shimmer Loader
```html
<div class="space-y-2 max-w-sm animate-pulse">
  <div class="h-4 bg-muted rounded-md w-3/4"></div>
  <div class="h-3 bg-muted rounded-md w-full"></div>
  <div class="h-3 bg-muted rounded-md w-5/6"></div>
</div>
```

### 4.3 Progress Bar
```html
<div class="w-full bg-muted rounded-full h-2 overflow-hidden">
  <div class="bg-primary h-full rounded-full transition-all duration-500" style="width: 68%;"></div>
</div>
```

---

## 5. Data Display

### 5.1 Avatar & User Badge
```html
<div class="flex items-center gap-3">
  <div class="relative w-9 h-9 rounded-full bg-primary/20 text-primary font-bold flex items-center justify-center text-xs">
    JD
    <span class="absolute bottom-0 right-0 w-2.5 h-2.5 rounded-full bg-emerald-500 ring-2 ring-background"></span>
  </div>
  <div>
    <h5 class="text-xs font-bold text-foreground">John Doe</h5>
    <p class="text-[11px] text-muted-foreground">Lead Architect</p>
  </div>
</div>
```

### 5.2 Accordion (Accessible Collapse)
```html
<div class="border border-border rounded-xl divide-y divide-border text-xs">
  <details class="group p-3">
    <summary class="flex justify-between items-center cursor-pointer font-semibold text-foreground list-none">
      <span>How are API limits enforced?</span>
      <span class="transition group-open:rotate-180">▼</span>
    </summary>
    <p class="mt-2 text-muted-foreground leading-relaxed">Limits are enforced on a per-second sliding window via distributed Redis counters.</p>
  </details>
</div>
```
