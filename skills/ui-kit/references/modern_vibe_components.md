# 🌟 Modern Vibe Components & Motion Recipes (Aceternity & Magic UI Patterns)

Production-grade, AI-ready React + Tailwind CSS + Framer Motion component recipes designed for modern Vibe Coding. Adheres strictly to zero raw emojis (inline SVGs only), bidirectional text resilience with `<bdi>`, WCAG AAA contrast ratios, and native dual-theme support (Light + Dark).

---

## 1. Ambient Backgrounds & Hero Choreography

### 1.1 Aurora Ambient Glow Background
Subtle, high-end organic color waves that elevate landing page heros without layout thrashing.

```tsx
import React from "react";

export interface AuroraBackgroundProps {
  children?: React.ReactNode;
  className?: string;
  showRadialGradient?: boolean;
}

export const AuroraBackground: React.FC<AuroraBackgroundProps> = ({
  children,
  className = "",
  showRadialGradient = true,
}) => {
  return (
    <div
      className={`relative flex flex-col h-full items-center justify-center bg-background text-foreground transition-colors overflow-hidden ${className}`}
    >
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div
          className={`
            [--aurora:repeating-linear-gradient(100deg,var(--color-vibe-primary)_10%,var(--color-vibe-accent)_15%,var(--color-vibe-surface-tint)_20%,var(--color-vibe-primary)_25%,var(--color-vibe-accent)_30%)]
            [background-image:var(--aurora)]
            [background-size:300%,_200%]
            [background-position:50%_50%,50%_50%]
            filter blur-[10px] invert dark:invert-0
            after:content-[''] after:absolute after:inset-0 after:[background-image:var(--aurora)]
            after:[background-size:200%,_100%] 
            after:animate-aurora after:[background-attachment:fixed] after:mix-blend-difference
            pointer-events-none
            absolute -inset-[10px] opacity-40 will-change-transform
            ${showRadialGradient ? "[mask-image:radial-gradient(ellipse_at_100%_0%,black_10%,var(--transparent)_70%)]" : ""}
          `}
        />
      </div>
      <div className="relative z-10 w-full">{children}</div>
    </div>
  );
};
```

### 1.2 Spotlight Hero Section
Directs user focus to high-conversion value propositions with an ambient radial light source.

```tsx
import React from "react";

export interface SpotlightProps {
  className?: string;
  fill?: string;
}

export const Spotlight: React.FC<SpotlightProps> = ({
  className = "",
  fill = "currentColor",
}) => {
  return (
    <svg
      className={`animate-spotlight pointer-events-none absolute z-[1] h-[169%] w-[138%] lg:w-[84%] opacity-0 ${className}`}
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 3787 2842"
      fill="none"
    >
      <g filter="url(#spotlight-filter)">
        <ellipse
          cx="1924.71"
          cy="273.501"
          rx="1924.71"
          ry="273.501"
          transform="matrix(-0.822377 -0.568943 -0.568943 0.822377 3631.88 2291.09)"
          fill={fill}
          fillOpacity="0.21"
        />
      </g>
      <defs>
        <filter
          id="spotlight-filter"
          x="0.860352"
          y="0.838989"
          width="3785.16"
          height="2840.26"
          filterUnits="userSpaceOnUse"
          colorInterpolationFilters="sRGB"
        >
          <feFlood floodOpacity="0" result="BackgroundImageFix" />
          <feBlend mode="normal" in="SourceGraphic" in2="BackgroundImageFix" result="shape" />
          <feGaussianBlur stdDeviation="151" result="effect1_foregroundBlur" />
        </filter>
      </defs>
    </svg>
  );
};
```

---

## 2. Interactive Bento & Ambient Glow Cards

### 2.1 Border-Beam Neon Frame Card
A glowing light beam dynamically traverses the card perimeter using CSS gradients.

```tsx
import React from "react";

export interface BorderBeamProps {
  className?: string;
  size?: number;
  duration?: number;
  borderWidth?: number;
  anchor?: number;
  colorFrom?: string;
  colorTo?: string;
  delay?: number;
}

export const BorderBeam: React.FC<BorderBeamProps> = ({
  className = "",
  size = 200,
  duration = 15,
  anchor = 90,
  borderWidth = 1.5,
  colorFrom = "var(--color-vibe-primary, #6366f1)",
  colorTo = "var(--color-vibe-accent, #ec4899)",
  delay = 0,
}) => {
  return (
    <div
      style={
        {
          "--size": size,
          "--duration": duration,
          "--anchor": anchor,
          "--border-width": borderWidth,
          "--color-from": colorFrom,
          "--color-to": colorTo,
          "--delay": `-${delay}s`,
        } as React.CSSProperties
      }
      className={`pointer-events-none absolute inset-0 rounded-[inherit] [border:calc(var(--border-width)*1px)_solid_transparent] ![mask-clip:padding-box,border-box] ![mask-composite:intersect] [mask:linear-gradient(transparent,transparent),linear-gradient(white,white)] after:absolute after:aspect-square after:w-[calc(var(--size)*1px)] after:animate-border-beam after:[animation-delay:var(--delay)] after:[background:linear-gradient(to_left,var(--color-from),var(--color-to),transparent)] after:[offset-anchor:calc(var(--anchor)*1%)_50%] after:[offset-path:rect(0_auto_auto_0_round_calc(var(--size)*1px))] ${className}`}
    />
  );
};
```

### 2.2 3D Physics Spring Tilt Card
Interactive perspective tilt that tracks cursor position with smooth damping.

```tsx
import React, { useRef, useState } from "react";

export interface TiltCardProps {
  children: React.ReactNode;
  className?: string;
}

export const TiltCard: React.FC<TiltCardProps> = ({ children, className = "" }) => {
  const cardRef = useRef<HTMLDivElement>(null);
  const [rotation, setRotation] = useState({ x: 0, y: 0 });
  const [isHovered, setIsHovered] = useState(false);

  const handleMouseMove = (e: React.MouseEvent<HTMLDivElement>) => {
    if (!cardRef.current) return;
    const rect = cardRef.current.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    const centerX = rect.width / 2;
    const centerY = rect.height / 2;

    const rotX = ((y - centerY) / centerY) * -10;
    const rotY = ((x - centerX) / centerX) * 10;
    setRotation({ x: rotX, y: rotY });
  };

  const handleMouseLeave = () => {
    setIsHovered(false);
    setRotation({ x: 0, y: 0 });
  };

  return (
    <div
      ref={cardRef}
      onMouseMove={handleMouseMove}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={handleMouseLeave}
      style={{
        transform: `perspective(1000px) rotateX(${rotation.x}deg) rotateY(${rotation.y}deg) scale3d(${isHovered ? 1.02 : 1}, ${isHovered ? 1.02 : 1}, 1)`,
        transition: isHovered ? "none" : "transform 0.5s cubic-bezier(0.16, 1, 0.3, 1)",
      }}
      className={`relative overflow-hidden rounded-2xl border border-border/60 bg-card p-6 shadow-xl will-change-transform ${className}`}
    >
      {children}
    </div>
  );
};
```

---

## 3. Kinetic Motion & Dynamic Typography

### 3.1 Infinite Smooth Marquee (Brands, Metrics & Testimonials)
Zero-lag, hardware-accelerated looping banner with pause-on-hover and direction support.

```tsx
import React from "react";

export interface MarqueeProps {
  children: React.ReactNode;
  direction?: "left" | "right";
  pauseOnHover?: boolean;
  speed?: number;
  className?: string;
}

export const InfiniteMarquee: React.FC<MarqueeProps> = ({
  children,
  direction = "left",
  pauseOnHover = true,
  speed = 40,
  className = "",
}) => {
  return (
    <div
      className={`group relative flex overflow-hidden p-2 [--gap:1rem] [gap:var(--gap)] ${className}`}
    >
      <div
        style={{
          animationDuration: `${speed}s`,
          animationDirection: direction === "right" ? "reverse" : "normal",
        }}
        className={`flex min-w-full shrink-0 items-center justify-around [gap:var(--gap)] animate-marquee ${
          pauseOnHover ? "group-hover:[animation-play-state:paused]" : ""
        }`}
      >
        {children}
      </div>
      <div
        style={{
          animationDuration: `${speed}s`,
          animationDirection: direction === "right" ? "reverse" : "normal",
        }}
        aria-hidden="true"
        className={`flex min-w-full shrink-0 items-center justify-around [gap:var(--gap)] animate-marquee ${
          pauseOnHover ? "group-hover:[animation-play-state:paused]" : ""
        }`}
      >
        {children}
      </div>
    </div>
  );
};
```

### 3.2 Shimmer Glow Button
CTA button with animated high-contrast light sweep across its surface.

```tsx
import React from "react";

export interface ShimmerButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  shimmerColor?: string;
  borderRadius?: string;
  background?: string;
  children: React.ReactNode;
}

export const ShimmerButton: React.FC<ShimmerButtonProps> = ({
  shimmerColor = "#ffffff",
  borderRadius = "100px",
  background = "var(--color-vibe-primary, #6366f1)",
  children,
  className = "",
  ...props
}) => {
  return (
    <button
      style={
        {
          "--spread": "90deg",
          "--shimmer-color": shimmerColor,
          "--radius": borderRadius,
          "--speed": "3s",
          "--cut": "0.1em",
          "--bg": background,
        } as React.CSSProperties
      }
      className={`group relative z-0 flex cursor-pointer items-center justify-center overflow-hidden whitespace-nowrap border border-white/20 px-6 py-3 font-semibold text-white [background:var(--bg)] [border-radius:var(--radius)] shadow-lg transition-transform duration-200 active:scale-95 ${className}`}
      {...props}
    >
      <div className="-z-30 absolute inset-0 overflow-visible [container-type:size]">
        <div className="absolute inset-0 h-[100cqh] animate-shimmer-slide [aspect-ratio:1] [border-radius:0] [mask:none]">
          <div className="animate-spin-around absolute -inset-full w-auto rotate-0 [background:conic-gradient(from_calc(270deg-(var(--spread)*0.5)),transparent_0,var(--shimmer-color)_var(--spread),transparent_var(--spread))] [translate:0_0]" />
        </div>
      </div>
      <bdi className="relative z-10 flex items-center gap-2">{children}</bdi>
    </button>
  );
};
```

---

## 4. Floating Navigation & Micro-HUD Controls

### 4.1 Floating Dock Island (macOS-style Magnification)
Dock container providing smooth cubic magnification as the user sweeps across icons.

```tsx
import React, { useRef, useState } from "react";

export interface DockItem {
  id: string;
  title: string;
  icon: React.ReactNode;
  onClick?: () => void;
}

export interface FloatingDockProps {
  items: DockItem[];
  className?: string;
}

export const FloatingDock: React.FC<FloatingDockProps> = ({ items, className = "" }) => {
  const [hoveredIndex, setHoveredIndex] = useState<number | null>(null);

  return (
    <nav
      aria-label="Quick Actions Dock"
      className={`fixed bottom-6 left-1/2 -translate-x-1/2 z-50 flex items-end gap-3 rounded-full border border-border/50 bg-background/80 px-4 py-3 shadow-2xl backdrop-blur-xl ${className}`}
    >
      {items.map((item, idx) => {
        const isHovered = hoveredIndex === idx;
        const isNeighbor = hoveredIndex !== null && Math.abs(hoveredIndex - idx) === 1;
        const scale = isHovered ? 1.35 : isNeighbor ? 1.15 : 1;

        return (
          <button
            key={item.id}
            onClick={item.onClick}
            onMouseEnter={() => setHoveredIndex(idx)}
            onMouseLeave={() => setHoveredIndex(null)}
            title={item.title}
            aria-label={item.title}
            style={{
              transform: `scale(${scale}) translateY(${isHovered ? -6 : 0}px)`,
              transition: "transform 0.25s cubic-bezier(0.16, 1, 0.3, 1)",
            }}
            className="flex h-11 w-11 items-center justify-center rounded-full bg-card/80 border border-border/60 text-foreground shadow-sm hover:border-primary/50 hover:bg-card focus-visible:outline-2 focus-visible:outline-primary"
          >
            {item.icon}
          </button>
        );
      })}
    </nav>
  );
};
```

---

## 5. Architectural Quality Checklist for AI Agents

Whenever implementing components from this catalog:
1. **Color Token Alignment:** Always bind color values to CSS design tokens (`--color-vibe-primary`, `--color-vibe-surface`, etc.) rather than hardcoded Hex values.
2. **Accessible Interaction (`bdi` & `aria`):** Wrap labels in `<bdi>` to isolate mixed LTR/RTL text. Provide explicit `aria-label` for icon-only action triggers.
3. **Hardware Acceleration:** Ensure motion elements use `will-change-transform` or CSS transforms to prevent CPU reflows.
4. **WCAG AAA Contrast:** Pair primary buttons with certified `--color-vibe-on-primary` foreground values (minimum 4.5:1, target 7:1).
