# 🌌 Living Micro-Interactions Catalog & Autonomous Injection Engine

This catalog provides production-ready, zero-hallucination interactive recipes for modern web applications. Each recipe is designed for React 19, Tailwind CSS v4, typed OKLCH color tokens, strict WCAG AA contrast, and zero external runtime bloat.

---

## 🎯 The Autonomous Living Injection Matrix

AI agents and automated pipelines must not generate static, lifeless interfaces. By analyzing the **Domain Archetype**, the agent must proactively inject the corresponding living micro-interactions without requiring manual prompt requests from the user:

| Domain Archetype | Primary Micro-Interactions | Secondary Micro-Interactions | Sensory Role |
| :--- | :--- | :--- | :--- |
| **FinTech / Web3 / Crypto** | `shimmer-button` (Primary CTA), `holographic-card` (Asset / Wallet Tile) | `cyber-loader` (Tx Processing), `tactile-switch` (Testnet Toggle) | High security, institutional glow, immediate physical transaction feedback |
| **DevOps / Cloud / AI SaaS** | `thinking-drawer` (Reasoning HUD), `telemetry-hud` (System Latency) | `glow-input` (Command Prompt), `cyber-loader` (Stream Ingestion) | Precise observability, engineering rigor, zero-latency feedback |
| **E-Commerce & Luxury Retail** | `holographic-card` (Product Showcase), `shimmer-button` (Checkout Action) | `tactile-switch` (Variant Toggle), `glow-input` (Discount / Search) | Tactile materialism, high-end reflection, purchase conviction |
| **Healthcare & Enterprise Apps** | `tactile-switch` (Patient Consent), `glow-input` (Data Ingestion) | `shimmer-button` (Schedule / Submit), `contrast-badge` (Compliance) | Calm ergonomics, unequivocal error clarity, accessible hit zones |
| **Gaming & Creative Studios** | `holographic-card` (Inventory / NFT), `cyber-loader` (Asset Cache) | `shimmer-button` (Launch Game), `glow-input` (In-Game Handle) | Visceral immersion, neon energy, reactive hover physics |

---

## 🛡️ Zero-Hallucination Guardrails

To eliminate code generation errors and phantom dependencies:

1. **Zero Imaginary Packages:**
   - NEVER import non-existent libraries (e.g., `framer-motion-3d`, `vibe-animations`, `tailwind-glow-kit`, or fake icon names).
   - Rely solely on React 19 standard hooks (`useState`, `useRef`, `useId`), pure CSS transitions, or official `lucide-react` / inline SVGs.
2. **Deterministic Tailwind v4 Syntax:**
   - Use standard Tailwind utility classes (`translate-x-full`, `transition-all duration-300`, `backdrop-blur-md`).
   - Limit backdrop-blur filters to a maximum of 3 layers per viewport to maintain 60 FPS on mobile devices.
3. **WCAG 2.2 AA Contrast Invariant:**
   - Ensure all text and interactive state labels maintain $\ge 4.5:1$ contrast against the underlying background.
4. **Touch Target Sizing:**
   - Interactive triggers (`button`, `a`, `[role="switch"]`) must maintain a minimum physical hit area of **44px × 44px**.
5. **Persian & RTL Language Contract:**
   - Persian text must strictly avoid ZWNJ (نیم فاصله); use standard spaces exclusively.
   - Numerical telemetry, code, and latency metrics must remain isolated in LTR (`dir="ltr"`).

---

## 📦 Living Component Recipes

### 1. Shimmer Button (`shimmer-button`)
A tactile action button with a traveling gradient shimmer sweep, subtle hover scale, and high-visibility keyboard focus ring.

```tsx
'use client';

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
      className={`group relative inline-flex items-center justify-center gap-2 overflow-hidden rounded-xl border font-medium tracking-wide transition-all duration-300 active:scale-[0.98] disabled:pointer-events-none disabled:opacity-50 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-indigo-500/70 focus-visible:ring-offset-2 focus-visible:ring-offset-slate-950 ${sizeClasses} ${variantClasses} ${className}`}
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
```

---

### 2. Cyber Loader (`cyber-loader`)
A high-efficiency dual-ring neon pulse spinner engineered for maximum GPU throughput (pure CSS transforms, zero heavy blur loops), fully accessible via `role="status"` and `aria-live`.

```tsx
'use client';

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
      className={`inline-flex flex-col items-center justify-center gap-3 ${className}`}
    >
      <div className={`relative flex items-center justify-center ${sizeMap.container}`}>
        {/* Outer orbital neon ring */}
        <div
          className={`absolute inset-0 rounded-full ${sizeMap.border} border-t-indigo-500 border-r-indigo-400/40 border-b-transparent border-l-transparent animate-spin ${durationClass}`}
        />
        {/* Reverse counter-orbital ring */}
        <div
          className={`absolute ${sizeMap.inner} rounded-full ${sizeMap.border} border-t-transparent border-r-transparent border-b-emerald-400 border-l-emerald-500/50 animate-spin ${durationClass}`}
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
```

---

### 3. Holographic Card (`holographic-card`)
An interactive 3D perspective tilt card with an adaptive specular cursor reflection and subtle depth elevation.

```tsx
'use client';

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
          ? `perspective(1000px) rotateX(${rotate.x}deg) rotateY(${rotate.y}deg)`
          : undefined,
        transition: 'transform 0.15s ease-out',
      }}
      className={`group relative overflow-hidden rounded-2xl border border-white/10 bg-slate-900/80 p-6 text-slate-100 shadow-xl backdrop-blur-md transition-shadow duration-300 hover:shadow-2xl hover:shadow-indigo-500/10 ${className}`}
    >
      {/* Specular Radial Holographic Flare */}
      <div
        aria-hidden="true"
        className="pointer-events-none absolute -inset-px rounded-2xl transition-opacity duration-300"
        style={{
          background: `radial-gradient(circle 250px at ${glow.x}% ${glow.y}%, rgba(99, 102, 241, ${glow.opacity}), transparent 80%)`,
        }}
      />

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
```

---

### 4. Tactile Switch (`tactile-switch`)
An ergonomic physical toggle switch with spring physics, full keyboard operability (`Space` / `Enter`), and screen-reader accessibility (`role="switch"`, `aria-checked`).

```tsx
'use client';

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
  const descId = `${switchId}-desc`;

  const handleKeyDown = (e: React.KeyboardEvent<HTMLButtonElement>) => {
    if (disabled) return;
    if (e.key === ' ' || e.key === 'Enter') {
      e.preventDefault();
      onChange(!checked);
    }
  };

  return (
    <div className={`flex items-center justify-between gap-4 select-none ${disabled ? 'opacity-50 pointer-events-none' : ''} ${className}`}>
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
        className={`relative inline-flex h-7 w-12 shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-indigo-500 focus-visible:ring-offset-2 focus-visible:ring-offset-slate-950 min-h-[44px] min-w-[44px] p-2 items-center ${
          checked ? 'bg-indigo-600' : 'bg-slate-700'
        }`}
      >
        <span
          aria-hidden="true"
          className={`pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow-md ring-0 transition duration-200 ease-out ${
            checked ? 'translate-x-5' : 'translate-x-0'
          }`}
        />
      </button>
    </div>
  );
}
```

---

### 5. Glow Input (`glow-input`)
A floating neon halo input field featuring dynamic focus expansion, clear validation error states, and complete RTL compatibility.

```tsx
'use client';

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
  const errorId = `${inputId}-error`;
  const helperId = `${inputId}-helper`;

  return (
    <div className={`w-full flex flex-col gap-1.5 ${className}`}>
      {label && (
        <label htmlFor={inputId} className="text-xs font-medium text-slate-300 dark:text-slate-200">
          {label}
        </label>
      )}

      <div className="relative group">
        {/* Animated Glow Border Halo on Focus */}
        <div
          aria-hidden="true"
          className={`absolute -inset-0.5 rounded-xl blur-sm transition-opacity duration-300 opacity-0 group-focus-within:opacity-100 pointer-events-none ${
            error ? 'bg-rose-500/30' : 'bg-indigo-500/30'
          }`}
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
            className={`w-full rounded-lg border bg-slate-900/90 text-sm text-slate-100 placeholder:text-slate-500 transition-all duration-200 focus:outline-none min-h-[44px] ${
              icon ? 'ps-10 pe-4' : 'px-4'
            } py-2.5 ${
              error
                ? 'border-rose-500/70 focus:border-rose-400 focus:ring-1 focus:ring-rose-500'
                : 'border-slate-800 focus:border-indigo-500/80 focus:ring-1 focus:ring-indigo-500/50'
            } disabled:opacity-50 disabled:cursor-not-allowed`}
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
```
