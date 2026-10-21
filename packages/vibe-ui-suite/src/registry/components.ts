/**
 * Vibe UI Component Registry
 * Production-ready, accessible, AI-native React component templates.
 */

export interface ComponentTemplate {
  name: string;
  filename: string;
  description: string;
  category: 'ai-contracts' | 'living-micro-interactions' | 'section-blocks';
  code: string;
}

export const COMPONENT_REGISTRY: Record<string, ComponentTemplate> = {
  // ─── AI Contracts & Observation Primitives ───────────────────────────
  'thinking-drawer': {
    name: 'thinking-drawer',
    filename: 'AiThinkingDrawer.tsx',
    category: 'ai-contracts',
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
    category: 'ai-contracts',
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
    category: 'ai-contracts',
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
    category: 'ai-contracts',
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
        <svg className="w-5 h-5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2" aria-hidden="true">
          <circle cx="12" cy="12" r="4" />
          <path strokeLinecap="round" d="M12 2v2m0 16v2M4.93 4.93l1.41 1.41m11.32 11.32l1.41 1.41M2 12h2m16 0h2M6.34 17.66l-1.41 1.41m14.14-14.14l-1.41 1.41" />
        </svg>
      ) : (
        <svg className="w-5 h-5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2" aria-hidden="true">
          <path strokeLinecap="round" strokeLinejoin="round" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
        </svg>
      )}
    </button>
  );
}
`,
  },

  // ─── Curated Living Micro-Interactions ────────────────────────────────
  'shimmer-button': {
    name: 'shimmer-button',
    filename: 'ShimmerButton.tsx',
    category: 'living-micro-interactions',
    description: 'Animated shimmer gradient button with smooth scale, OKLCH accents, SVG slot, and WCAG focus ring',
    code: `'use client';

import React from 'react';

export interface ShimmerButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  children: React.ReactNode;
  variant?: 'primary' | 'secondary' | 'outline';
  size?: 'sm' | 'md' | 'lg';
  icon?: React.ReactNode;
  shimmerColor?: string;
  className?: string;
}

export function ShimmerButton({
  children,
  variant = 'primary',
  size = 'md',
  icon,
  shimmerColor = 'rgba(255, 255, 255, 0.25)',
  className = '',
  disabled,
  ...props
}: ShimmerButtonProps) {
  const sizeClasses = {
    sm: 'px-3.5 py-1.5 text-xs min-h-[36px]',
    md: 'px-5 py-2.5 text-sm min-h-[44px]',
    lg: 'px-6 py-3.5 text-base min-h-[50px]',
  }[size];

  const variantClasses = {
    primary: 'bg-indigo-600 hover:bg-indigo-500 text-white shadow-lg shadow-indigo-500/25 border-indigo-400/30',
    secondary: 'bg-slate-900 hover:bg-slate-800 text-slate-100 border-slate-700/60 shadow-md shadow-black/20',
    outline: 'bg-transparent hover:bg-white/5 text-slate-200 border-slate-600/60',
  }[variant];

  return (
    <button
      type="button"
      disabled={disabled}
      className={\`group relative inline-flex items-center justify-center gap-2 overflow-hidden rounded-xl border font-medium tracking-wide transition-all duration-300 active:scale-[0.98] disabled:pointer-events-none disabled:opacity-50 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-indigo-500/70 focus-visible:ring-offset-2 focus-visible:ring-offset-slate-950 \${sizeClasses} \${variantClasses} \${className}\`}
      {...props}
    >
      {/* Dynamic Animated Shimmer Flare */}
      <span
        aria-hidden="true"
        className="pointer-events-none absolute inset-0 -translate-x-full transition-transform duration-1000 ease-out group-hover:translate-x-full bg-gradient-to-r from-transparent via-[var(--shimmer-color,rgba(255,255,255,0.25))] to-transparent"
        style={{ '--shimmer-color': shimmerColor } as React.CSSProperties}
      />

      {icon && (
        <span className="shrink-0 transition-transform duration-200 group-hover:scale-110" aria-hidden="true">
          {icon}
        </span>
      )}
      <span className="relative z-10">{children}</span>
    </button>
  );
}
`,
  },

  'cyber-loader': {
    name: 'cyber-loader',
    filename: 'CyberLoader.tsx',
    category: 'living-micro-interactions',
    description: 'High-efficiency dual-ring neon pulse spinner without heavy blur lag, with ARIA live region',
    code: `'use client';

import React from 'react';

export interface CyberLoaderProps {
  size?: 'sm' | 'md' | 'lg';
  label?: string;
  speed?: 'normal' | 'fast' | 'slow';
  className?: string;
}

export function CyberLoader({
  size = 'md',
  label = 'Loading system telemetry...',
  speed = 'normal',
  className = '',
}: CyberLoaderProps) {
  const sizeMap = {
    sm: { container: 'w-8 h-8', inner: 'w-4 h-4', border: 'border-2' },
    md: { container: 'w-12 h-12', inner: 'w-6 h-6', border: 'border-2' },
    lg: { container: 'w-16 h-16', inner: 'w-8 h-8', border: 'border-[3px]' },
  }[size];

  const durationClass = {
    fast: 'duration-700',
    normal: 'duration-1000',
    slow: 'duration-1500',
  }[speed];

  return (
    <div
      role="status"
      aria-live="polite"
      className={\`inline-flex flex-col items-center justify-center gap-3 \${className}\`}
    >
      <div className={\`relative flex items-center justify-center \${sizeMap.container}\`}>
        {/* Outer orbital neon ring */}
        <div
          className={\`absolute inset-0 rounded-full \${sizeMap.border} border-t-indigo-500 border-r-indigo-400/40 border-b-transparent border-l-transparent animate-spin \${durationClass}\`}
        />
        {/* Reverse counter-orbital ring */}
        <div
          className={\`absolute \${sizeMap.inner} rounded-full \${sizeMap.border} border-t-transparent border-r-transparent border-b-emerald-400 border-l-emerald-500/50 animate-spin \${durationClass}\`}
          style={{ animationDirection: 'reverse' }}
        />
        {/* Center core pulse */}
        <div className="w-1.5 h-1.5 rounded-full bg-indigo-400 animate-ping opacity-75" />
      </div>

      {label && (
        <span className="text-xs font-mono font-medium tracking-wider uppercase text-slate-400 dark:text-slate-300">
          {label}
        </span>
      )}
      <span className="sr-only">{label}</span>
    </div>
  );
}
`,
  },

  'holographic-card': {
    name: 'holographic-card',
    filename: 'HolographicCard.tsx',
    category: 'living-micro-interactions',
    description: 'Interactive 3D tilt card with specular border highlight, glass gradient reflection, and depth control',
    code: `'use client';

import React, { useRef, useState } from 'react';

export interface HolographicCardProps {
  title?: string;
  description?: string;
  badge?: string;
  children?: React.ReactNode;
  interactive?: boolean;
  className?: string;
}

export function HolographicCard({
  title,
  description,
  badge,
  children,
  interactive = true,
  className = '',
}: HolographicCardProps) {
  const cardRef = useRef<HTMLDivElement>(null);
  const [rotate, setRotate] = useState({ x: 0, y: 0 });
  const [glow, setGlow] = useState({ x: 50, y: 50, opacity: 0 });

  const handleMouseMove = (e: React.MouseEvent<HTMLDivElement>) => {
    if (!interactive || !cardRef.current) return;
    const rect = cardRef.current.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    const centerX = rect.width / 2;
    const centerY = rect.height / 2;

    const rotX = ((y - centerY) / centerY) * -7;
    const rotY = ((x - centerX) / centerX) * 7;
    setRotate({ x: rotX, y: rotY });
    setGlow({
      x: (x / rect.width) * 100,
      y: (y / rect.height) * 100,
      opacity: 0.15,
    });
  };

  const handleMouseLeave = () => {
    if (!interactive) return;
    setRotate({ x: 0, y: 0 });
    setGlow({ x: 50, y: 50, opacity: 0 });
  };

  return (
    <div
      ref={cardRef}
      onMouseMove={handleMouseMove}
      onMouseLeave={handleMouseLeave}
      style={{
        transform: interactive
          ? \`perspective(1000px) rotateX(\${rotate.x}deg) rotateY(\${rotate.y}deg)\`
          : undefined,
        transition: 'transform 0.15s ease-out',
      }}
      className={\`group relative overflow-hidden rounded-2xl border border-white/10 bg-slate-900/80 p-6 text-slate-100 shadow-xl backdrop-blur-md transition-shadow duration-300 hover:shadow-2xl hover:shadow-indigo-500/10 \${className}\`}
    >
      {/* Specular Radial Holographic Flare */}
      <div
        aria-hidden="true"
        className="pointer-events-none absolute -inset-px rounded-2xl transition-opacity duration-300"
        style={{
          background: \`radial-gradient(circle 250px at \${glow.x}% \${glow.y}%, rgba(99, 102, 241, \${glow.opacity}), transparent 80%)\`,
        }}
      />

      {/* Header section */}
      {(title || badge) && (
        <div className="relative z-10 flex items-start justify-between gap-4 mb-3">
          {title && <h3 className="text-lg font-semibold tracking-tight text-white">{title}</h3>}
          {badge && (
            <span className="inline-flex items-center rounded-full border border-indigo-400/30 bg-indigo-500/10 px-2.5 py-0.5 text-xs font-medium text-indigo-300">
              {badge}
            </span>
          )}
        </div>
      )}

      {description && (
        <p className="relative z-10 text-sm text-slate-400 mb-4 leading-relaxed">{description}</p>
      )}

      <div className="relative z-10">{children}</div>
    </div>
  );
}
`,
  },

  'tactile-switch': {
    name: 'tactile-switch',
    filename: 'TactileSwitch.tsx',
    category: 'living-micro-interactions',
    description: 'Ergonomic tactile toggle switch with spring-bounce animation physics and full keyboard accessibility',
    code: `'use client';

import React, { useId } from 'react';

export interface TactileSwitchProps {
  checked: boolean;
  onChange: (checked: boolean) => void;
  label?: string;
  description?: string;
  disabled?: boolean;
  id?: string;
  className?: string;
}

export function TactileSwitch({
  checked,
  onChange,
  label,
  description,
  disabled = false,
  id: customId,
  className = '',
}: TactileSwitchProps) {
  const generatedId = useId();
  const switchId = customId || generatedId;
  const descId = \`\${switchId}-desc\`;

  const handleKeyDown = (e: React.KeyboardEvent<HTMLButtonElement>) => {
    if (disabled) return;
    if (e.key === ' ' || e.key === 'Enter') {
      e.preventDefault();
      onChange(!checked);
    }
  };

  return (
    <div className={\`flex items-center justify-between gap-4 select-none \${disabled ? 'opacity-50 pointer-events-none' : ''} \${className}\`}>
      {(label || description) && (
        <label htmlFor={switchId} className="cursor-pointer flex flex-col text-sm">
          {label && <span className="font-medium text-slate-200 dark:text-slate-100">{label}</span>}
          {description && <span id={descId} className="text-xs text-slate-400 dark:text-slate-400">{description}</span>}
        </label>
      )}

      <button
        id={switchId}
        type="button"
        role="switch"
        aria-checked={checked}
        aria-describedby={description ? descId : undefined}
        disabled={disabled}
        onClick={() => onChange(!checked)}
        onKeyDown={handleKeyDown}
        className={\`relative inline-flex h-7 w-12 shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-indigo-500 focus-visible:ring-offset-2 focus-visible:ring-offset-slate-950 min-h-[44px] min-w-[44px] p-2 items-center \${
          checked ? 'bg-indigo-600' : 'bg-slate-700'
        }\`}
      >
        <span
          aria-hidden="true"
          className={\`pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow-md ring-0 transition duration-200 ease-out \${
            checked ? 'translate-x-5' : 'translate-x-0'
          }\`}
        />
      </button>
    </div>
  );
}
`,
  },

  'glow-input': {
    name: 'glow-input',
    filename: 'GlowInput.tsx',
    category: 'living-micro-interactions',
    description: 'Floating neon halo input field with dynamic focus state, error styling, and RTL compatibility',
    code: `'use client';

import React, { useId } from 'react';

export interface GlowInputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  helperText?: string;
  icon?: React.ReactNode;
}

export function GlowInput({
  label,
  error,
  helperText,
  icon,
  id: customId,
  className = '',
  disabled,
  ...props
}: GlowInputProps) {
  const generatedId = useId();
  const inputId = customId || generatedId;
  const errorId = \`\${inputId}-error\`;
  const helperId = \`\${inputId}-helper\`;

  return (
    <div className={\`w-full flex flex-col gap-1.5 \${className}\`}>
      {label && (
        <label htmlFor={inputId} className="text-xs font-medium text-slate-300 dark:text-slate-200">
          {label}
        </label>
      )}

      <div className="relative group">
        {/* Animated Glow Border Halo on Focus */}
        <div
          aria-hidden="true"
          className={\`absolute -inset-0.5 rounded-xl blur-sm transition-opacity duration-300 opacity-0 group-focus-within:opacity-100 pointer-events-none \${
            error ? 'bg-rose-500/30' : 'bg-indigo-500/30'
          }\`}
        />

        <div className="relative flex items-center">
          {icon && (
            <div className="absolute inset-y-0 start-0 flex items-center ps-3.5 pointer-events-none text-slate-400" aria-hidden="true">
              {icon}
            </div>
          )}

          <input
            id={inputId}
            disabled={disabled}
            aria-invalid={Boolean(error)}
            aria-describedby={error ? errorId : helperText ? helperId : undefined}
            className={\`w-full rounded-lg border bg-slate-900/90 text-sm text-slate-100 placeholder:text-slate-500 transition-all duration-200 focus:outline-none min-h-[44px] \${
              icon ? 'ps-10 pe-4' : 'px-4'
            } py-2.5 \${
              error
                ? 'border-rose-500/70 focus:border-rose-400 focus:ring-1 focus:ring-rose-500'
                : 'border-slate-800 focus:border-indigo-500/80 focus:ring-1 focus:ring-indigo-500/50'
            } disabled:opacity-50 disabled:cursor-not-allowed\`}
            {...props}
          />
        </div>
      </div>

      {error ? (
        <p id={errorId} className="text-xs text-rose-400 flex items-center gap-1 mt-0.5" role="alert">
          <svg className="w-3.5 h-3.5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          {error}
        </p>
      ) : helperText ? (
        <p id={helperId} className="text-xs text-slate-500 mt-0.5">
          {helperText}
        </p>
      ) : null}
    </div>
  );
}
`,
  },

  // ─── Flagship Living Primitives ───────────────────────────────────────
  'device-mockup': {
    name: 'device-mockup',
    filename: 'DeviceMockup.tsx',
    category: 'living-micro-interactions',
    description: '3D titanium iPhone frame mockup with gyroscopic hover tilt, dynamic island, and specular glass reflex',
    code: `'use client';

import React, { useRef, useState } from 'react';

export interface DeviceMockupProps {
  children?: React.ReactNode;
  model?: 'iphone-16-pro' | 'minimal-frame';
  className?: string;
  enableTilt?: boolean;
}

export function DeviceMockup({
  children,
  model = 'iphone-16-pro',
  className = '',
  enableTilt = true,
}: DeviceMockupProps) {
  const frameRef = useRef<HTMLDivElement>(null);
  const [rotate, setRotate] = useState({ x: 0, y: 0 });

  const handleMouseMove = (e: React.MouseEvent<HTMLDivElement>) => {
    if (!enableTilt || !frameRef.current) return;
    const rect = frameRef.current.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    const centerX = rect.width / 2;
    const centerY = rect.height / 2;

    const rotX = ((y - centerY) / centerY) * -10;
    const rotY = ((x - centerX) / centerX) * 10;
    setRotate({ x: rotX, y: rotY });
  };

  const handleMouseLeave = () => {
    if (!enableTilt) return;
    setRotate({ x: 0, y: 0 });
  };

  return (
    <div
      className={\`relative mx-auto w-full max-w-[340px] select-none \${className}\`}
      style={{ perspective: '1000px' }}
      onMouseMove={handleMouseMove}
      onMouseLeave={handleMouseLeave}
    >
      <div
        ref={frameRef}
        style={{
          transform: enableTilt
            ? \`rotateX(\${rotate.x}deg) rotateY(\${rotate.y}deg)\`
            : undefined,
          transition: 'transform 0.4s cubic-bezier(0.25, 1, 0.5, 1), box-shadow 0.4s ease',
        }}
        className="relative overflow-hidden rounded-[48px] border-[10px] border-[#1c1c1e] bg-black p-3.5 shadow-2xl shadow-indigo-950/30 ring-1 ring-white/20"
      >
        {/* Dynamic Island */}
        <div className="absolute top-4 left-1/2 -translate-x-1/2 z-30 h-[26px] w-[95px] rounded-full bg-black flex items-center justify-between px-2.5 shadow-sm">
          <div className="h-2 w-2 rounded-full bg-indigo-950/80 ring-1 ring-indigo-500/30" />
          <div className="h-2.5 w-2.5 rounded-full bg-emerald-500/20 flex items-center justify-center">
            <span className="h-1.5 w-1.5 rounded-full bg-emerald-400 animate-pulse" />
          </div>
        </div>

        {/* Specular Edge Sheen */}
        <div
          aria-hidden="true"
          className="pointer-events-none absolute inset-0 z-20 rounded-[38px] bg-gradient-to-tr from-white/10 via-transparent to-transparent opacity-60"
        />

        {/* Screen Content Container */}
        <div className="relative z-10 min-h-[580px] w-full overflow-hidden rounded-[36px] bg-slate-950 text-white flex flex-col">
          {children || (
            <div className="flex flex-1 flex-col items-center justify-center p-6 text-center">
              <div className="h-12 w-12 rounded-2xl bg-indigo-500/20 border border-indigo-400/30 flex items-center justify-center mb-4 text-indigo-400">
                <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z" />
                </svg>
              </div>
              <h4 className="text-base font-semibold text-slate-100 mb-1">Vibe UI Native Screen</h4>
              <p className="text-xs text-slate-400 max-w-[200px]">
                Drop any responsive React or Tailwind component inside children.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
`,
  },

  'before-after-lens': {
    name: 'before-after-lens',
    filename: 'BeforeAfterLens.tsx',
    category: 'living-micro-interactions',
    description: 'Interactive split-screen comparison slider with drag physics, touch support, and accessible ARIA keyboard navigation',
    code: `'use client';

import React, { useRef, useState, useCallback } from 'react';

export interface BeforeAfterLensProps {
  beforeContent?: React.ReactNode;
  afterContent?: React.ReactNode;
  beforeLabel?: string;
  afterLabel?: string;
  initialPosition?: number;
  className?: string;
}

export function BeforeAfterLens({
  beforeContent,
  afterContent,
  beforeLabel = 'Before (Flat Baseline)',
  afterLabel = 'After (Vibe Masterpiece)',
  initialPosition = 50,
  className = '',
}: BeforeAfterLensProps) {
  const [sliderPos, setSliderPos] = useState(initialPosition);
  const [isDragging, setIsDragging] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);

  const updatePosition = useCallback((clientX: number) => {
    if (!containerRef.current) return;
    const rect = containerRef.current.getBoundingClientRect();
    const x = clientX - rect.left;
    const percent = Math.max(5, Math.min(95, (x / rect.width) * 100));
    setSliderPos(percent);
  }, []);

  const handleMouseDown = () => setIsDragging(true);
  const handleMouseUp = () => setIsDragging(false);

  const handleMouseMove = (e: React.MouseEvent<HTMLDivElement>) => {
    if (!isDragging) return;
    updatePosition(e.clientX);
  };

  const handleTouchMove = (e: React.TouchEvent<HTMLDivElement>) => {
    if (e.touches[0]) {
      updatePosition(e.touches[0].clientX);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLDivElement>) => {
    if (e.key === 'ArrowLeft') {
      setSliderPos((prev) => Math.max(5, prev - 5));
    } else if (e.key === 'ArrowRight') {
      setSliderPos((prev) => Math.min(95, prev + 5));
    } else if (e.key === 'Home') {
      setSliderPos(5);
    } else if (e.key === 'End') {
      setSliderPos(95);
    }
  };

  return (
    <div
      ref={containerRef}
      onMouseMove={handleMouseMove}
      onMouseUp={handleMouseUp}
      onTouchMove={handleTouchMove}
      className={\`relative w-full overflow-hidden rounded-2xl border border-white/10 select-none \${className}\`}
      style={{ minHeight: '380px' }}
    >
      {/* After Layer (Background / Base) */}
      <div className="absolute inset-0 h-full w-full bg-slate-900 text-white p-6 flex flex-col justify-center">
        {afterContent || (
          <div className="max-w-md mx-auto text-center space-y-3">
            <span className="inline-flex px-3 py-1 rounded-full bg-indigo-500/20 text-indigo-400 text-xs font-mono font-medium border border-indigo-500/30">
              {afterLabel}
            </span>
            <h3 className="text-2xl font-bold text-white tracking-tight">Vibe UI Living Experience</h3>
            <p className="text-sm text-slate-300">
              Refined spatial rhythm, OKLCH perceptual colors, tactile micro-interactions, and fluid spring physics.
            </p>
          </div>
        )}
      </div>

      {/* Before Layer (Foreground clipped by slider percentage) */}
      <div
        className="absolute inset-0 h-full w-full bg-slate-950 text-slate-300 p-6 flex flex-col justify-center border-r border-indigo-400/50"
        style={{ clipPath: \`polygon(0 0, \${sliderPos}% 0, \${sliderPos}% 100%, 0 100%)\` }}
      >
        {beforeContent || (
          <div className="max-w-md mx-auto text-center space-y-3 opacity-70">
            <span className="inline-flex px-3 py-1 rounded-full bg-slate-800 text-slate-400 text-xs font-mono font-medium border border-slate-700">
              {beforeLabel}
            </span>
            <h3 className="text-2xl font-medium text-slate-400 tracking-tight">Generic AI Code Baseline</h3>
            <p className="text-sm text-slate-500">
              Dead layout, generic purple gradients, harsh contrast, raw emojis, and missing accessible states.
            </p>
          </div>
        )}
      </div>

      {/* Draggable Divider Line & Handle */}
      <div
        role="slider"
        tabIndex={0}
        aria-label="Before and After visual comparison"
        aria-valuenow={Math.round(sliderPos)}
        aria-valuemin={0}
        aria-valuemax={100}
        onKeyDown={handleKeyDown}
        onMouseDown={handleMouseDown}
        style={{ left: \`\${sliderPos}%\` }}
        className="absolute top-0 bottom-0 w-1 -ml-0.5 bg-gradient-to-b from-indigo-400 via-white to-indigo-400 cursor-ew-resize flex items-center justify-center z-30 focus:outline-none focus:ring-2 focus:ring-indigo-400"
      >
        <div className="h-9 w-9 rounded-full bg-slate-900 border-2 border-indigo-400 shadow-xl flex items-center justify-center text-indigo-300 text-xs transition-transform hover:scale-110 active:scale-95">
          <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M8 9l-3 3 3 3m8-6l3 3-3 3" />
          </svg>
        </div>
      </div>
    </div>
  );
}
`,
  },

  'specular-card': {
    name: 'specular-card',
    filename: 'SpecularCard.tsx',
    category: 'living-micro-interactions',
    description: 'Photographic visual card with dynamic specular light sweep, category badge, and hover zoom physics',
    code: `'use client';

import React from 'react';

export interface SpecularCardProps {
  title: string;
  category?: string;
  description?: string;
  imageSrc?: string;
  children?: React.ReactNode;
  className?: string;
}

export function SpecularCard({
  title,
  category,
  description,
  imageSrc,
  children,
  className = '',
}: SpecularCardProps) {
  return (
    <div
      className={\`group relative overflow-hidden rounded-2xl border border-white/10 bg-slate-900/80 p-5 text-white shadow-xl backdrop-blur-md transition-all duration-300 hover:-translate-y-1 hover:border-indigo-500/40 hover:shadow-2xl hover:shadow-indigo-500/10 \${className}\`}
    >
      {/* Dynamic Specular Sheen Sweep on Hover */}
      <div
        aria-hidden="true"
        className="pointer-events-none absolute inset-0 -translate-x-full bg-gradient-to-r from-transparent via-white/10 to-transparent transition-transform duration-1000 ease-out group-hover:translate-x-full"
      />

      {imageSrc && (
        <div className="relative mb-4 h-48 w-full overflow-hidden rounded-xl bg-slate-800">
          <img
            src={imageSrc}
            alt={title}
            className="h-full w-full object-cover transition-transform duration-500 ease-out group-hover:scale-105"
            loading="lazy"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-slate-950/80 via-transparent to-transparent" />
        </div>
      )}

      {category && (
        <span className="inline-flex items-center text-[11px] font-mono font-medium uppercase tracking-wider text-indigo-400 mb-2">
          {category}
        </span>
      )}

      <h3 className="text-lg font-semibold tracking-tight text-white mb-2">{title}</h3>

      {description && (
        <p className="text-sm text-slate-400 leading-relaxed mb-4">{description}</p>
      )}

      {children && <div className="mt-auto">{children}</div>}
    </div>
  );
}
`,
  },

  // ─── Section Blocks (Full Page Composable Architecture) ─────────────
  'bento-hero': {
    name: 'bento-hero',
    filename: 'BentoHero.tsx',
    category: 'section-blocks',
    description: 'Asymmetric 12-column Bento Grid hero section with live SVG sparkline, action pills & specular highlights',
    code: `'use client';

import React, { useState } from 'react';

export interface BentoHeroProps {
  badge?: string;
  title?: string;
  highlightedText?: string;
  description?: string;
  primaryActionText?: string;
  secondaryActionText?: string;
  metricValue?: string;
  metricLabel?: string;
  className?: string;
}

export function BentoHero({
  badge = 'Next-Gen Interface Protocol',
  title = 'Autonomous Design Meets',
  highlightedText = 'Kinetic Precision',
  description = 'Deterministic design contracts, OKLCH perceptual tokens, and responsive micro-interactions engineered for the modern web.',
  primaryActionText = 'Deploy Architecture',
  secondaryActionText = 'Explore Sandbox',
  metricValue = '$12,480.90',
  metricLabel = 'Realtime Protocol Yield',
  className = '',
}: BentoHeroProps) {
  const [activeTab, setActiveTab] = useState<'vault' | 'stats'>('vault');

  return (
    <section className={\`relative w-full overflow-hidden px-4 py-16 md:py-24 lg:py-32 font-sans text-slate-900 dark:text-slate-100 \${className}\`}>
      {/* Ambient background glow */}
      <div className="pointer-events-none absolute left-1/2 top-1/4 -translate-x-1/2 -translate-y-1/2 h-96 w-96 rounded-full bg-indigo-500/10 blur-[120px] dark:bg-indigo-500/20" />

      <div className="relative mx-auto max-w-7xl">
        <div className="grid grid-cols-1 gap-12 lg:grid-cols-12 lg:items-center">
          {/* Left Column: Hero Copy (Span 7) */}
          <div className="flex flex-col items-start lg:col-span-7">
            {badge && (
              <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-indigo-500/20 bg-indigo-50/50 px-3 py-1 text-xs font-semibold uppercase tracking-wider text-indigo-600 backdrop-blur-sm dark:bg-indigo-950/40 dark:text-indigo-400">
                <span className="h-1.5 w-1.5 rounded-full bg-indigo-500 animate-pulse" />
                {badge}
              </div>
            )}

            <h1 className="text-4xl font-extrabold tracking-tight sm:text-5xl md:text-6xl lg:text-7xl leading-[1.1]">
              {title}{' '}
              <span className="bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 bg-clip-text text-transparent">
                {highlightedText}
              </span>
            </h1>

            <p className="mt-6 max-w-2xl text-lg text-slate-600 dark:text-slate-400 leading-relaxed sm:text-xl">
              {description}
            </p>

            <div className="mt-8 flex flex-wrap items-center gap-4">
              <button
                type="button"
                className="inline-flex items-center justify-center rounded-xl bg-indigo-600 px-6 py-3.5 text-sm font-semibold text-white shadow-lg shadow-indigo-600/25 transition-all duration-200 hover:bg-indigo-500 hover:shadow-indigo-600/40 focus:outline-none focus:ring-2 focus:ring-indigo-500/50 active:scale-[0.98]"
              >
                {primaryActionText}
                <svg className="ml-2 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14 5l7 7m0 0l-7 7m7-7H3" />
                </svg>
              </button>

              <button
                type="button"
                className="inline-flex items-center justify-center rounded-xl border border-slate-300 bg-white/70 px-6 py-3.5 text-sm font-semibold text-slate-700 backdrop-blur-md transition-all duration-200 hover:bg-slate-100 hover:text-slate-900 focus:outline-none focus:ring-2 focus:ring-slate-400/50 active:scale-[0.98] dark:border-slate-800 dark:bg-slate-900/60 dark:text-slate-300 dark:hover:bg-slate-800"
              >
                {secondaryActionText}
              </button>
            </div>
          </div>

          {/* Right Column: Polymorphic Bento Matrix (Span 5) */}
          <div className="w-full lg:col-span-5">
            <div className="relative rounded-3xl border border-slate-200/80 bg-white/80 p-6 shadow-2xl backdrop-blur-xl dark:border-slate-800/80 dark:bg-slate-900/80 sm:p-8">
              {/* Card Header & Switcher */}
              <div className="flex items-center justify-between border-b border-slate-100 pb-5 dark:border-slate-800">
                <div>
                  <span className="text-xs font-semibold uppercase tracking-wider text-slate-400 dark:text-slate-500">
                    Live Telemetry
                  </span>
                  <div className="text-2xl font-bold tracking-tight text-slate-900 dark:text-white">
                    {metricValue}
                  </div>
                </div>

                <div className="flex rounded-xl bg-slate-100 p-1 dark:bg-slate-800">
                  <button
                    type="button"
                    onClick={() => setActiveTab('vault')}
                    className={\`rounded-lg px-3 py-1 text-xs font-medium transition-colors \${
                      activeTab === 'vault'
                        ? 'bg-white text-slate-900 shadow-sm dark:bg-slate-700 dark:text-white'
                        : 'text-slate-500 hover:text-slate-900 dark:text-slate-400 dark:hover:text-white'
                    }\`}
                  >
                    Vault
                  </button>
                  <button
                    type="button"
                    onClick={() => setActiveTab('stats')}
                    className={\`rounded-lg px-3 py-1 text-xs font-medium transition-colors \${
                      activeTab === 'stats'
                        ? 'bg-white text-slate-900 shadow-sm dark:bg-slate-700 dark:text-white'
                        : 'text-slate-500 hover:text-slate-900 dark:text-slate-400 dark:hover:text-white'
                    }\`}
                  >
                    Stats
                  </button>
                </div>
              </div>

              {/* Dynamic SVG Sparkline */}
              <div className="my-6">
                <div className="mb-2 flex items-center justify-between text-xs text-slate-500">
                  <span>{metricLabel}</span>
                  <span className="font-semibold text-emerald-500">+18.4% APY</span>
                </div>
                <div className="h-28 w-full overflow-hidden rounded-xl bg-slate-50 p-2 dark:bg-slate-950/50">
                  <svg className="h-full w-full" viewBox="0 0 300 80" preserveAspectRatio="none">
                    <defs>
                      <linearGradient id="bentoGradient" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="0%" stopColor="#6366f1" stopOpacity="0.4" />
                        <stop offset="100%" stopColor="#6366f1" stopOpacity="0.0" />
                      </linearGradient>
                    </defs>
                    <path
                      d="M0,60 C40,55 70,30 110,35 C150,40 180,15 220,20 C260,25 280,5 300,8 L300,80 L0,80 Z"
                      fill="url(#bentoGradient)"
                    />
                    <path
                      d="M0,60 C40,55 70,30 110,35 C150,40 180,15 220,20 C260,25 280,5 300,8"
                      fill="none"
                      stroke="#6366f1"
                      strokeWidth="2.5"
                    />
                  </svg>
                </div>
              </div>

              {/* Status Chips */}
              <div className="grid grid-cols-2 gap-3 pt-2">
                <div className="flex items-center gap-2 rounded-xl border border-slate-100 bg-slate-50/50 p-3 dark:border-slate-800 dark:bg-slate-950/40">
                  <span className="h-2 w-2 rounded-full bg-emerald-500" />
                  <span className="text-xs font-medium text-slate-600 dark:text-slate-300">60 FPS Smooth</span>
                </div>
                <div className="flex items-center gap-2 rounded-xl border border-slate-100 bg-slate-50/50 p-3 dark:border-slate-800 dark:bg-slate-950/40">
                  <span className="h-2 w-2 rounded-full bg-indigo-500" />
                  <span className="text-xs font-medium text-slate-600 dark:text-slate-300">WCAG AAA Valid</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
`,
  },

  'pricing-matrix': {
    name: 'pricing-matrix',
    filename: 'PricingMatrix.tsx',
    category: 'section-blocks',
    description: 'Tiered responsive 3-column pricing matrix with monthly/annual discount toggle & highlighted popular tier',
    code: `'use client';

import React, { useState } from 'react';

export interface PricingTier {
  id: string;
  name: string;
  description: string;
  priceMonthly: number;
  priceAnnual: number;
  features: string[];
  isPopular?: boolean;
  ctaText?: string;
}

export interface PricingMatrixProps {
  title?: string;
  subtitle?: string;
  annualDiscountLabel?: string;
  tiers?: PricingTier[];
  className?: string;
}

const DEFAULT_TIERS: PricingTier[] = [
  {
    id: 'starter',
    name: 'Developer Community',
    description: 'Essential tokens and components for independent hackers & open source builders.',
    priceMonthly: 0,
    priceAnnual: 0,
    features: ['11 Visual Paradigms', 'React 19 & Tailwind v4 Primitives', 'WCAG AA Auto-Check', 'Community Discord Support'],
    ctaText: 'Get Started Free',
  },
  {
    id: 'pro',
    name: 'Pro Sovereign',
    description: 'Autonomous AI design tokens, full micro-interactions and unlimited code audits.',
    priceMonthly: 29,
    priceAnnual: 24,
    isPopular: true,
    features: [
      'Everything in Community',
      'Full 12-Column Bento Primitives',
      'Continuous Headless Playwright Audits',
      'Zero-JS Height Transitions',
      'Priority Agent Skills Sync',
    ],
    ctaText: 'Start Pro Trial',
  },
  {
    id: 'enterprise',
    name: 'Protocol Enterprise',
    description: 'Dedicated design systems, custom archetype compilers, and 24/7 SLA.',
    priceMonthly: 99,
    priceAnnual: 79,
    features: [
      'Everything in Pro Sovereign',
      'Custom Design Token Compilers',
      'Enterprise SSO & Team Workspaces',
      'Custom LLM Fine-Tuned Models',
      'Dedicated Design Architect',
    ],
    ctaText: 'Contact Architecture Team',
  },
];

export function PricingMatrix({
  title = 'Predictable, Transparent Pricing',
  subtitle = 'Choose the architectural capacity that scales with your autonomous engineering velocity.',
  annualDiscountLabel = 'Save 20%',
  tiers = DEFAULT_TIERS,
  className = '',
}: PricingMatrixProps) {
  const [isAnnual, setIsAnnual] = useState(true);

  return (
    <section className={\`relative w-full px-4 py-16 md:py-24 font-sans text-slate-900 dark:text-slate-100 \${className}\`}>
      <div className="mx-auto max-w-7xl">
        {/* Header & Toggle */}
        <div className="text-center max-w-3xl mx-auto">
          <h2 className="text-3xl font-extrabold tracking-tight sm:text-4xl md:text-5xl">
            {title}
          </h2>
          <p className="mt-4 text-base text-slate-600 dark:text-slate-400 sm:text-lg">
            {subtitle}
          </p>

          {/* Billing Switcher */}
          <div className="mt-8 inline-flex items-center gap-3 rounded-full border border-slate-200 bg-slate-50 p-1.5 dark:border-slate-800 dark:bg-slate-900">
            <button
              type="button"
              onClick={() => setIsAnnual(false)}
              className={\`rounded-full px-4 py-2 text-sm font-semibold transition-all \${
                !isAnnual
                  ? 'bg-white text-slate-900 shadow-md dark:bg-slate-800 dark:text-white'
                  : 'text-slate-600 hover:text-slate-900 dark:text-slate-400 dark:hover:text-white'
              }\`}
            >
              Monthly
            </button>
            <button
              type="button"
              onClick={() => setIsAnnual(true)}
              className={\`inline-flex items-center gap-2 rounded-full px-4 py-2 text-sm font-semibold transition-all \${
                isAnnual
                  ? 'bg-white text-slate-900 shadow-md dark:bg-slate-800 dark:text-white'
                  : 'text-slate-600 hover:text-slate-900 dark:text-slate-400 dark:hover:text-white'
              }\`}
            >
              <span>Annual</span>
              <span className="rounded-full bg-emerald-100 px-2 py-0.5 text-[11px] font-bold text-emerald-700 dark:bg-emerald-950 dark:text-emerald-300">
                {annualDiscountLabel}
              </span>
            </button>
          </div>
        </div>

        {/* 3-Column Tier Grid */}
        <div className="mt-16 grid grid-cols-1 gap-8 lg:grid-cols-3 items-stretch">
          {tiers.map((tier) => {
            const price = isAnnual ? tier.priceAnnual : tier.priceMonthly;

            return (
              <div
                key={tier.id}
                className={\`relative flex flex-col justify-between rounded-3xl p-8 transition-all duration-300 \${
                  tier.isPopular
                    ? 'border-2 border-indigo-500 bg-white/90 shadow-2xl shadow-indigo-500/10 dark:bg-slate-900/90 dark:border-indigo-500 lg:-translate-y-2'
                    : 'border border-slate-200/80 bg-white/60 shadow-lg dark:border-slate-800/80 dark:bg-slate-900/60'
                }\`}
              >
                {tier.isPopular && (
                  <div className="absolute -top-3.5 left-1/2 -translate-x-1/2 rounded-full bg-gradient-to-r from-indigo-500 to-purple-600 px-3.5 py-1 text-xs font-bold uppercase tracking-wider text-white shadow-md">
                    Most Popular
                  </div>
                )}

                <div>
                  <div className="flex items-center justify-between">
                    <h3 className="text-xl font-bold text-slate-900 dark:text-white">{tier.name}</h3>
                  </div>

                  <p className="mt-3 text-sm text-slate-600 dark:text-slate-400 leading-relaxed">
                    {tier.description}
                  </p>

                  <div className="mt-6 flex items-baseline gap-1">
                    <span className="text-4xl font-extrabold tracking-tight text-slate-900 dark:text-white sm:text-5xl">
                      \${price}
                    </span>
                    <span className="text-sm font-medium text-slate-500 dark:text-slate-400">
                      / month
                    </span>
                  </div>

                  <div className="mt-8 space-y-3.5">
                    {tier.features.map((feat, i) => (
                      <div key={i} className="flex items-start gap-3">
                        <svg className="h-5 w-5 flex-shrink-0 text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M5 13l4 4L19 7" />
                        </svg>
                        <span className="text-sm text-slate-700 dark:text-slate-300">{feat}</span>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="mt-10 pt-4 border-t border-slate-100 dark:border-slate-800">
                  <button
                    type="button"
                    className={\`w-full rounded-xl py-3.5 px-4 text-sm font-semibold transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 active:scale-[0.98] \${
                      tier.isPopular
                        ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-600/30 hover:bg-indigo-500 focus:ring-indigo-500'
                        : 'border border-slate-300 bg-white text-slate-700 hover:bg-slate-50 focus:ring-slate-400 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-200 dark:hover:bg-slate-700'
                    }\`}
                  >
                    {tier.ctaText || 'Get Started'}
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
`,
  },

  'feature-grid': {
    name: 'feature-grid',
    filename: 'FeatureGrid.tsx',
    category: 'section-blocks',
    description: 'Modern interactive feature grid with kinetic hover states, glass cards & micro-HUD metrics',
    code: `'use client';

import React from 'react';

export interface FeatureItem {
  id: string;
  title: string;
  description: string;
  metric?: string;
  tag?: string;
}

export interface FeatureGridProps {
  badge?: string;
  title?: string;
  subtitle?: string;
  features?: FeatureItem[];
  className?: string;
}

const DEFAULT_FEATURES: FeatureItem[] = [
  {
    id: 'f1',
    title: 'Deterministic OKLCH Tokens',
    description: 'Mathematically verified color spaces delivering guaranteed perceptual contrast and natural lightness curves across light and dark modes.',
    metric: '18.80:1 Contrast',
    tag: 'Design Core',
  },
  {
    id: 'f2',
    title: 'Spring Kinematics Engine',
    description: 'Critically damped spring dynamics (ζ = 0.82) with velocity handoff, eliminating sluggish cubic-bezier CSS animations.',
    metric: '60 FPS Pure GPU',
    tag: 'Motion',
  },
  {
    id: 'f3',
    title: 'Semantic RTL & BiDi Resilience',
    description: 'Strict W3C bidirectional text isolation using <bdi> wrappers, preventing numeric inversion and mixed Persian/English punctuation bugs.',
    metric: '100% W3C Valid',
    tag: 'Accessibility',
  },
  {
    id: 'f4',
    title: 'Zero-JS Height Transitions',
    description: 'Fluid accordion disclosure utilizing modern CSS Grid 0fr to 1fr transitions without expensive DOM height recalculations.',
    metric: '0ms Layout Shift',
    tag: 'Performance',
  },
  {
    id: 'f5',
    title: 'Autonomous Multi-Gate Critic',
    description: 'Continuous headless Playwright evaluation measuring sub-pixel horizontal overflow and interactive clickable semantics.',
    metric: '16/16 Gate Pass',
    tag: 'Reliability',
  },
  {
    id: 'f6',
    title: 'Zero-Dependency Primitives',
    description: 'Standalone React 19 + Tailwind v4 components with zero foreign library bloat, ensuring instant builds without dependency conflicts.',
    metric: '0 External Deps',
    tag: 'Simplicity',
  },
];

export function FeatureGrid({
  badge = 'Architectural Capabilities',
  title = 'Engineered to Eliminate AI Slop',
  subtitle = 'Every primitive in Vibe UI Suite is calibrated against the 5 Master Execution Gates.',
  features = DEFAULT_FEATURES,
  className = '',
}: FeatureGridProps) {
  return (
    <section className={\`relative w-full px-4 py-16 md:py-24 font-sans text-slate-900 dark:text-slate-100 \${className}\`}>
      <div className="mx-auto max-w-7xl">
        <div className="text-center max-w-3xl mx-auto mb-16">
          {badge && (
            <span className="mb-4 inline-block text-xs font-semibold uppercase tracking-widest text-indigo-600 dark:text-indigo-400">
              {badge}
            </span>
          )}
          <h2 className="text-3xl font-extrabold tracking-tight sm:text-4xl md:text-5xl">
            {title}
          </h2>
          <p className="mt-4 text-base text-slate-600 dark:text-slate-400 sm:text-lg">
            {subtitle}
          </p>
        </div>

        <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {features.map((feat) => (
            <div
              key={feat.id}
              className="group relative flex flex-col justify-between rounded-2xl border border-slate-200/80 bg-white/70 p-6 shadow-sm backdrop-blur-md transition-all duration-300 hover:-translate-y-1 hover:border-indigo-500/50 hover:shadow-xl dark:border-slate-800/80 dark:bg-slate-900/60"
            >
              <div>
                <div className="flex items-center justify-between mb-4">
                  {feat.tag && (
                    <span className="rounded-md bg-indigo-50 px-2.5 py-1 text-[11px] font-semibold text-indigo-600 dark:bg-indigo-950/60 dark:text-indigo-400">
                      {feat.tag}
                    </span>
                  )}
                  {feat.metric && (
                    <span className="text-xs font-mono font-medium text-slate-400 dark:text-slate-500">
                      {feat.metric}
                    </span>
                  )}
                </div>

                <h3 className="text-lg font-bold text-slate-900 dark:text-white group-hover:text-indigo-600 dark:group-hover:text-indigo-400 transition-colors">
                  {feat.title}
                </h3>

                <p className="mt-2 text-sm text-slate-600 dark:text-slate-400 leading-relaxed">
                  {feat.description}
                </p>
              </div>

              <div className="mt-6 flex items-center text-xs font-semibold text-indigo-600 dark:text-indigo-400">
                <span>Explore Architecture</span>
                <svg className="ml-1 h-3.5 w-3.5 transition-transform group-hover:translate-x-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                </svg>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
`,
  },

  'glass-navbar': {
    name: 'glass-navbar',
    filename: 'GlassNavbar.tsx',
    category: 'section-blocks',
    description: 'Responsive glassmorphism navigation header with accessible mobile drawer & theme switcher',
    code: `'use client';

import React, { useState } from 'react';

export interface NavLink {
  label: string;
  href: string;
}

export interface GlassNavbarProps {
  brandName?: string;
  links?: NavLink[];
  ctaText?: string;
  onCtaClick?: () => void;
  className?: string;
}

const DEFAULT_LINKS: NavLink[] = [
  { label: 'Paradigms', href: '#paradigms' },
  { label: 'Architecture', href: '#architecture' },
  { label: 'Components', href: '#components' },
  { label: 'Pricing', href: '#pricing' },
];

export function GlassNavbar({
  brandName = 'Vibe UI',
  links = DEFAULT_LINKS,
  ctaText = 'Get Started',
  onCtaClick,
  className = '',
}: GlassNavbarProps) {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <header className={\`sticky top-0 z-50 w-full px-4 py-3 font-sans transition-all \${className}\`}>
      <div className="mx-auto flex max-w-7xl items-center justify-between rounded-2xl border border-white/20 bg-white/70 px-4 py-2.5 shadow-lg shadow-black/5 backdrop-blur-xl dark:border-white/10 dark:bg-slate-950/70 sm:px-6">
        {/* Brand Logo */}
        <a href="#" className="flex items-center gap-2.5 text-base font-bold tracking-tight text-slate-900 dark:text-white">
          <div className="flex h-8 w-8 items-center justify-center rounded-xl bg-indigo-600 text-white shadow-md shadow-indigo-600/30">
            <span className="font-mono text-sm font-black">▲</span>
          </div>
          <span>{brandName}</span>
        </a>

        {/* Desktop Navigation Links */}
        <nav className="hidden items-center gap-6 md:flex" aria-label="Main Navigation">
          {links.map((link) => (
            <a
              key={link.label}
              href={link.href}
              className="text-sm font-medium text-slate-600 transition-colors hover:text-slate-900 dark:text-slate-300 dark:hover:text-white"
            >
              {link.label}
            </a>
          ))}
        </nav>

        {/* CTA & Hamburger */}
        <div className="flex items-center gap-3">
          <button
            type="button"
            onClick={onCtaClick}
            className="hidden sm:inline-flex items-center justify-center rounded-xl bg-indigo-600 px-4 py-2 text-xs font-semibold text-white shadow-md shadow-indigo-600/25 transition-all hover:bg-indigo-500 active:scale-95 focus:outline-none focus:ring-2 focus:ring-indigo-500/50"
          >
            {ctaText}
          </button>

          {/* Accessible Hamburger Menu Button */}
          <button
            type="button"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            aria-expanded={mobileMenuOpen}
            aria-label="Toggle Navigation Menu"
            className="inline-flex md:hidden items-center justify-center rounded-xl p-2 text-slate-600 hover:bg-slate-100 dark:text-slate-300 dark:hover:bg-slate-800"
          >
            <svg className="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              {mobileMenuOpen ? (
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              ) : (
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              )}
            </svg>
          </button>
        </div>
      </div>

      {/* Responsive Mobile Drawer */}
      {mobileMenuOpen && (
        <div className="md:hidden mt-2 rounded-2xl border border-white/20 bg-white/95 p-4 shadow-xl backdrop-blur-xl dark:border-white/10 dark:bg-slate-950/95">
          <nav className="flex flex-col gap-3">
            {links.map((link) => (
              <a
                key={link.label}
                href={link.href}
                onClick={() => setMobileMenuOpen(false)}
                className="rounded-lg px-3 py-2 text-sm font-medium text-slate-700 hover:bg-slate-100 dark:text-slate-300 dark:hover:bg-slate-800"
              >
                {link.label}
              </a>
            ))}
            <div className="pt-2 border-t border-slate-100 dark:border-slate-800">
              <button
                type="button"
                onClick={() => {
                  setMobileMenuOpen(false);
                  onCtaClick?.();
                }}
                className="w-full rounded-xl bg-indigo-600 py-2.5 text-xs font-semibold text-white shadow-md shadow-indigo-600/25"
              >
                {ctaText}
              </button>
            </div>
          </nav>
        </div>
      )}
    </header>
  );
}
`,
  },

  'conversion-cta': {
    name: 'conversion-cta',
    filename: 'ConversionCta.tsx',
    category: 'section-blocks',
    description: 'High-impact conversion pre-footer CTA with copyable terminal CLI snippet & social proof cluster',
    code: `'use client';

import React, { useState } from 'react';

export interface ConversionCtaProps {
  title?: string;
  subtitle?: string;
  command?: string;
  ctaText?: string;
  ratingText?: string;
  className?: string;
}

export function ConversionCta({
  title = 'Ready to Eliminate AI Slop in Production?',
  subtitle = 'Integrate deterministic OKLCH tokens, 11 visual paradigms, and automated WCAG evaluation into your workflow in 30 seconds.',
  command = 'npx vibe-ui-suite@latest init',
  ctaText = 'Initialize Architecture',
  ratingText = '4.98 / 5.0 rated by autonomous engineering agents',
  className = '',
}: ConversionCtaProps) {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard?.writeText(command);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <section className={\`relative w-full px-4 py-16 md:py-24 font-sans text-slate-900 dark:text-slate-100 \${className}\`}>
      <div className="relative mx-auto max-w-5xl overflow-hidden rounded-3xl border border-indigo-500/20 bg-gradient-to-br from-indigo-950 via-slate-950 to-purple-950 p-8 md:p-14 text-center text-white shadow-2xl">
        {/* Glow circle */}
        <div className="pointer-events-none absolute -right-20 -top-20 h-64 w-64 rounded-full bg-indigo-500/20 blur-3xl" />
        <div className="pointer-events-none absolute -left-20 -bottom-20 h-64 w-64 rounded-full bg-purple-500/20 blur-3xl" />

        <div className="relative z-10 mx-auto max-w-2xl">
          <h2 className="text-3xl font-extrabold tracking-tight sm:text-4xl md:text-5xl text-white">
            {title}
          </h2>

          <p className="mt-4 text-base text-slate-300 sm:text-lg leading-relaxed">
            {subtitle}
          </p>

          {/* Copyable CLI Snippet */}
          <div className="mt-8 flex flex-col sm:flex-row items-center justify-center gap-3">
            <div className="flex w-full sm:w-auto items-center justify-between gap-3 rounded-xl border border-white/10 bg-slate-900/90 px-4 py-3 font-mono text-sm text-indigo-300 shadow-inner">
              <span className="text-slate-500">$</span>
              <span>{command}</span>
              <button
                type="button"
                onClick={handleCopy}
                aria-label="Copy CLI Command"
                className="ml-2 rounded-lg p-1.5 text-slate-400 hover:text-white transition-colors hover:bg-white/10"
              >
                {copied ? (
                  <svg className="h-4 w-4 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M5 13l4 4L19 7" />
                  </svg>
                ) : (
                  <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                  </svg>
                )}
              </button>
            </div>

            <button
              type="button"
              className="w-full sm:w-auto rounded-xl bg-indigo-600 px-6 py-3.5 text-sm font-semibold text-white shadow-lg shadow-indigo-600/30 transition-all hover:bg-indigo-500 active:scale-[0.98]"
            >
              {ctaText}
            </button>
          </div>

          {ratingText && (
            <div className="mt-8 flex items-center justify-center gap-2 text-xs text-slate-400">
              <div className="flex text-amber-400">
                {'★★★★★'}
              </div>
              <span>{ratingText}</span>
            </div>
          )}
        </div>
      </div>
    </section>
  );
}
`,
  },

  'faq-accordion': {
    name: 'faq-accordion',
    filename: 'FaqAccordion.tsx',
    category: 'section-blocks',
    description: 'Zero-JS accessible HTML5 details/summary accordion FAQ section with animated SVG chevrons',
    code: `'use client';

import React from 'react';

export interface FaqItem {
  question: string;
  answer: string;
}

export interface FaqAccordionProps {
  title?: string;
  subtitle?: string;
  items?: FaqItem[];
  className?: string;
}

const DEFAULT_FAQ: FaqItem[] = [
  {
    question: 'How does Vibe UI prevent generic AI Slop in generated interfaces?',
    answer: 'By replacing unconstrained LLM heuristics with deterministic mathematical contracts: strict WCAG AA/AAA contrast calculated in OKLCH space, mandatory light-first canvas policies, and verified spring physics curves.',
  },
  {
    question: 'Are there external CSS or animation library dependencies?',
    answer: 'Zero foreign dependencies. All primitives compile into native React 19 and Tailwind v4 CSS variables without requiring framer-motion, lucide-react, or bulky runtime packages.',
  },
  {
    question: 'How do autonomous coding agents use this suite?',
    answer: 'AI agents like Cursor, Windsurf, Claude Code, and Antigravity connect via the Vibe UI MCP Server (npx vibe-ui-suite mcp) or inspect local skills in .agents/skills/ to retrieve optimal design tokens and run automated audits before delivering code.',
  },
  {
    question: 'How is RTL and bidirectional text handled?',
    answer: 'All primitives adhere to W3C bidi standards by isolating numbers, currencies, and technical metrics inside semantic <bdi> wrappers, eliminating punctuation inversion bugs in Persian, Arabic, or Hebrew.',
  },
];

export function FaqAccordion({
  title = 'Frequently Asked Questions',
  subtitle = 'Technical details on our design token architecture and verification loop.',
  items = DEFAULT_FAQ,
  className = '',
}: FaqAccordionProps) {
  return (
    <section className={\`relative w-full px-4 py-16 md:py-24 font-sans text-slate-900 dark:text-slate-100 \${className}\`}>
      <div className="mx-auto max-w-4xl">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-extrabold tracking-tight sm:text-4xl">
            {title}
          </h2>
          <p className="mt-3 text-base text-slate-600 dark:text-slate-400">
            {subtitle}
          </p>
        </div>

        <div className="space-y-4">
          {items.map((item, index) => (
            <details
              key={index}
              className="group rounded-2xl border border-slate-200/80 bg-white/70 p-6 shadow-sm backdrop-blur-md transition-all duration-200 open:bg-white dark:border-slate-800/80 dark:bg-slate-900/60 dark:open:bg-slate-900"
            >
              <summary className="flex cursor-pointer list-none items-center justify-between text-left font-semibold text-slate-900 dark:text-white focus:outline-none">
                <span className="text-base sm:text-lg">{item.question}</span>
                <span className="ml-4 flex h-7 w-7 flex-shrink-0 items-center justify-center rounded-full bg-slate-100 text-slate-500 transition-transform duration-200 group-open:rotate-180 dark:bg-slate-800 dark:text-slate-400">
                  <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                  </svg>
                </span>
              </summary>
              <p className="mt-4 text-sm leading-relaxed text-slate-600 dark:text-slate-400 sm:text-base">
                {item.answer}
              </p>
            </details>
          ))}
        </div>
      </div>
    </section>
  );
}
`,
  },
};


