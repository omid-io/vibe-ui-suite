/**
 * Vibe UI Component Registry
 * Production-ready, accessible, AI-native React component templates.
 */

export interface ComponentTemplate {
  name: string;
  filename: string;
  description: string;
  code: string;
}

export const COMPONENT_REGISTRY: Record<string, ComponentTemplate> = {
  'thinking-drawer': {
    name: 'thinking-drawer',
    filename: 'AiThinkingDrawer.tsx',
    description: 'Collapsible AI reasoning drawer with CSS grid zero-JS transition, radar pulse & telemetry chips',
    code: `'use client';

import React, { useState } from 'react';

export interface ThinkingStep {
  id: string;
  label: string;
  status: 'completed' | 'in_progress' | 'pending';
  duration?: string;
}

export interface ToolExecutionChip {
  name: string;
  latency: string;
  status: 'cached' | 'executed' | 'verified';
}

export interface AiThinkingDrawerProps {
  initialOpen?: boolean;
  title?: string;
  durationMs?: number;
  steps?: ThinkingStep[];
  tools?: ToolExecutionChip[];
  className?: string;
}

const DEFAULT_STEPS: ThinkingStep[] = [
  { id: 's1', label: 'Ingested prompt & computed ambiguity budget', status: 'completed', duration: '18ms' },
  { id: 's2', label: 'Validated design-spec against JSON Schema', status: 'completed', duration: '42ms' },
  { id: 's3', label: 'Enforced WCAG AA contrast (>= 4.5:1) in OKLCH space', status: 'completed', duration: '95ms' },
];

const DEFAULT_TOOLS: ToolExecutionChip[] = [
  { name: 'vector_search()', latency: '42ms', status: 'cached' },
  { name: 'contrast_lint()', latency: '18ms', status: 'verified' },
];

export function AiThinkingDrawer({
  initialOpen = false,
  title = 'Reasoning Architecture & Contract Execution',
  durationMs = 155,
  steps = DEFAULT_STEPS,
  tools = DEFAULT_TOOLS,
  className = '',
}: AiThinkingDrawerProps) {
  const [open, setOpen] = useState(initialOpen);

  return (
    <div
      className={\`w-full max-w-2xl mx-auto rounded-xl border border-white/10 bg-slate-950/80 backdrop-blur-md overflow-hidden text-slate-100 font-sans shadow-xl \${className}\`}
      role="region"
      aria-label="AI Reasoning Details"
    >
      <button
        onClick={() => setOpen(!open)}
        aria-expanded={open}
        className="w-full flex items-center justify-between px-4 py-3 text-left hover:bg-white/5 transition-colors focus:outline-none focus:ring-2 focus:ring-indigo-500/50"
      >
        <div className="flex items-center gap-3">
          <span className="relative flex h-2.5 w-2.5">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75" />
            <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-500" />
          </span>
          <span className="text-sm font-medium text-slate-200">{title}</span>
          <span className="text-xs px-2 py-0.5 rounded-full bg-slate-800 text-slate-400 font-mono">
            {durationMs}ms
          </span>
        </div>
        <svg
          className={\`w-4 h-4 text-slate-400 transition-transform duration-200 \${open ? 'rotate-180' : ''}\`}
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
        </svg>
      </button>

      {/* Zero-JS height transition via CSS Grid */}
      <div
        className="grid transition-all duration-300 ease-out"
        style={{ gridTemplateRows: open ? '1fr' : '0fr' }}
      >
        <div className="overflow-hidden">
          <div className="p-4 pt-1 border-t border-white/5 space-y-3">
            <div className="space-y-2">
              {steps.map((step) => (
                <div key={step.id} className="flex items-center justify-between text-xs text-slate-300">
                  <div className="flex items-center gap-2">
                    <svg className="w-3.5 h-3.5 text-emerald-400 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M5 13l4 4L19 7" />
                    </svg>
                    <span>{step.label}</span>
                  </div>
                  {step.duration && <span className="font-mono text-slate-500 text-[11px]">{step.duration}</span>}
                </div>
              ))}
            </div>

            {tools.length > 0 && (
              <div className="pt-2 border-t border-white/5 flex flex-wrap gap-1.5">
                {tools.map((t, idx) => (
                  <span
                    key={idx}
                    className="inline-flex items-center gap-1.5 px-2 py-0.5 rounded bg-slate-900 border border-slate-800 text-[11px] font-mono text-slate-300"
                  >
                    <span className="w-1.5 h-1.5 rounded-full bg-indigo-400" />
                    {t.name}
                    <span className="text-slate-500">{t.latency}</span>
                  </span>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
`,
  },

  'telemetry-hud': {
    name: 'telemetry-hud',
    filename: 'TelemetryHud.tsx',
    description: 'LTR-isolated technical metric HUD with micro-borders for latency, tokens, and model status',
    code: `'use client';

import React from 'react';

export interface TelemetryMetric {
  label: string;
  value: string | number;
  unit?: string;
  status?: 'nominal' | 'warning' | 'alert';
}

export interface TelemetryHudProps {
  metrics?: TelemetryMetric[];
  className?: string;
}

const DEFAULT_METRICS: TelemetryMetric[] = [
  { label: 'Latency', value: '42', unit: 'ms', status: 'nominal' },
  { label: 'Entropy', value: '0.12', status: 'nominal' },
  { label: 'Contrast', value: '9.4:1', unit: 'AAA', status: 'nominal' },
  { label: 'Tokens', value: '1,420', status: 'nominal' },
];

export function TelemetryHud({ metrics = DEFAULT_METRICS, className = '' }: TelemetryHudProps) {
  return (
    <div
      dir="ltr"
      className={\`inline-flex items-center gap-4 px-3 py-1.5 rounded-lg border border-white/10 bg-slate-950/70 backdrop-blur-sm text-xs font-mono text-slate-300 shadow-sm \${className}\`}
    >
      {metrics.map((m, i) => (
        <div key={i} className="flex items-center gap-1.5">
          <span className="text-slate-500 uppercase tracking-wider text-[10px]">{m.label}:</span>
          <span className="font-semibold text-slate-200">
            {m.value}
            {m.unit && <span className="ml-0.5 text-slate-400 text-[10px] font-normal">{m.unit}</span>}
          </span>
          {i < metrics.length - 1 && <span className="text-slate-700">|</span>}
        </div>
      ))}
    </div>
  );
}
`,
  },

  'contrast-badge': {
    name: 'contrast-badge',
    filename: 'ContrastBadge.tsx',
    description: 'WCAG 2.2 contrast compliance badge indicating AA (4.5:1) or AAA (7.0:1) verification',
    code: `'use client';

import React from 'react';

export interface ContrastBadgeProps {
  ratio: number;
  label?: string;
  className?: string;
}

export function ContrastBadge({ ratio, label = 'WCAG 2.2', className = '' }: ContrastBadgeProps) {
  const isAAA = ratio >= 7.0;
  const isAA = ratio >= 4.5;
  const isLargeOnly = ratio >= 3.0;

  const status = isAAA ? 'AAA' : isAA ? 'AA' : isLargeOnly ? 'Large Only' : 'Fail';
  const colorClass = isAA
    ? 'border-emerald-500/30 bg-emerald-950/40 text-emerald-300'
    : isLargeOnly
    ? 'border-amber-500/30 bg-amber-950/40 text-amber-300'
    : 'border-rose-500/30 bg-rose-950/40 text-rose-300';

  return (
    <span
      dir="ltr"
      className={\`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full border text-xs font-mono font-medium \${colorClass} \${className}\`}
    >
      <span className="w-1.5 h-1.5 rounded-full bg-current" />
      <span>{label}</span>
      <span className="opacity-60">•</span>
      <span>{ratio.toFixed(1)}:1</span>
      <span className="px-1 py-0.2 rounded bg-white/10 text-[10px] uppercase">{status}</span>
    </span>
  );
}
`,
  },
  'theme-toggle': {
    name: 'theme-toggle',
    filename: 'ThemeToggle.tsx',
    description: 'Accessible dual-theme switch (light/dark) with SVG vector icons, focus ring, and localStorage persistence',
    code: `'use client';

import React, { useEffect, useState } from 'react';

export interface ThemeToggleProps {
  className?: string;
  defaultTheme?: 'light' | 'dark' | 'system';
}

export function ThemeToggle({ className = '', defaultTheme = 'system' }: ThemeToggleProps) {
  const [theme, setTheme] = useState<'light' | 'dark'>('dark');
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
    const stored = localStorage.getItem('vibe-theme');
    if (stored === 'light' || stored === 'dark') {
      setTheme(stored);
      document.documentElement.classList.toggle('dark', stored === 'dark');
      document.documentElement.setAttribute('data-theme', stored);
    } else {
      const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
      const initial = defaultTheme === 'system' ? (prefersDark ? 'dark' : 'light') : defaultTheme;
      setTheme(initial);
      document.documentElement.classList.toggle('dark', initial === 'dark');
      document.documentElement.setAttribute('data-theme', initial);
    }
  }, [defaultTheme]);

  const toggleTheme = () => {
    const next = theme === 'dark' ? 'light' : 'dark';
    setTheme(next);
    localStorage.setItem('vibe-theme', next);
    document.documentElement.classList.toggle('dark', next === 'dark');
    document.documentElement.setAttribute('data-theme', next);
  };

  if (!mounted) {
    return (
      <button
        type="button"
        aria-label="Toggle theme"
        className={\`inline-flex items-center justify-center min-h-[44px] min-w-[44px] p-2.5 rounded-lg border border-neutral-800 bg-neutral-900/50 text-neutral-400 opacity-60 \${className}\`}
        disabled
      >
        <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <circle cx="12" cy="12" r="4" strokeWidth="2" />
        </svg>
      </button>
    );
  }

  return (
    <button
      type="button"
      onClick={toggleTheme}
      aria-label={\`Switch to \${theme === 'dark' ? 'light' : 'dark'} mode\`}
      className={\`inline-flex items-center justify-center min-h-[44px] min-w-[44px] p-2.5 rounded-lg border transition-all duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-indigo-500 \${
        theme === 'dark'
          ? 'border-neutral-800 bg-neutral-900/80 text-neutral-200 hover:bg-neutral-800 hover:text-white'
          : 'border-neutral-200 bg-white text-neutral-700 hover:bg-neutral-100 hover:text-neutral-900'
      } \${className}\`}
    >
      {theme === 'dark' ? (
        /* Sun Icon for switching to light mode */
        <svg className="w-5 h-5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2" aria-hidden="true">
          <circle cx="12" cy="12" r="4" />
          <path strokeLinecap="round" d="M12 2v2m0 16v2M4.93 4.93l1.41 1.41m11.32 11.32l1.41 1.41M2 12h2m16 0h2M6.34 17.66l-1.41 1.41m14.14-14.14l-1.41 1.41" />
        </svg>
      ) : (
        /* Moon Icon for switching to dark mode */
        <svg className="w-5 h-5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2" aria-hidden="true">
          <path strokeLinecap="round" strokeLinejoin="round" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
        </svg>
      )}
    </button>
  );
}
`,
  },
};
