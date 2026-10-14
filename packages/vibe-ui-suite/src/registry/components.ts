/**
 * Vibe UI Component Registry
 * Production-ready, accessible, AI-native React component templates.
 */

export interface ComponentTemplate {
  name: string;
  filename: string;
  description: string;
  category: 'ai-contracts' | 'living-micro-interactions';
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
};
