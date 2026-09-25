'use client';

import React, { useState, useEffect } from 'react';
import { VisualChemistryId, VISUAL_CHEMISTRIES } from '@/lib/tokens';
import { HeroSection } from '@/components/HeroSection';
import { cn } from '@/lib/utils';

export default function HomePage() {
  const [chemistry, setChemistry] = useState<VisualChemistryId>('MINIMALIST_SAAS');
  const [lang, setLang] = useState<'en' | 'fa'>('en');

  const isRtl = lang === 'fa';
  const currentTheme = VISUAL_CHEMISTRIES[chemistry];

  // Sync data-chemistry and dir attribute to document element for global styles
  useEffect(() => {
    document.documentElement.setAttribute('data-chemistry', chemistry);
    document.documentElement.setAttribute('dir', isRtl ? 'rtl' : 'ltr');
    document.documentElement.setAttribute('lang', lang);
  }, [chemistry, isRtl, lang]);

  return (
    <div
      data-chemistry={chemistry}
      dir={isRtl ? 'rtl' : 'ltr'}
      className="min-h-screen bg-canvas text-textPrimary transition-colors duration-200 flex flex-col font-sans"
    >
      {/* Top Navigation Bar */}
      <header className="sticky top-0 z-50 w-full border-b border-border bg-surface/90 backdrop-blur-md transition-colors">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8 max-w-7xl h-16 flex items-center justify-between gap-4">
          
          {/* Logo & Version */}
          <div className="flex items-center gap-3">
            <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-accent text-white shadow-xs">
              {/* Pure SVG Vibe UI Logo */}
              <svg
                className="h-5 w-5"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2.5"
                strokeLinecap="round"
                strokeLinejoin="round"
                aria-hidden="true"
              >
                <path d="M4 4L12 20L20 4" />
                <path d="M8 4L12 14L16 4" />
              </svg>
            </div>
            <div className="flex flex-col">
              <span className="font-bold tracking-tight text-sm text-textPrimary leading-none">
                VIBE UI
              </span>
              <span className="ltr-code text-[11px] font-mono text-textMuted">
                nextjs-starter v2.2.1
              </span>
            </div>
          </div>

          {/* Center / Actions: Visual Chemistry & Language Toggles */}
          <div className="flex items-center gap-2 sm:gap-3">
            
            {/* Visual Chemistry Dropdown / Selector */}
            <div className="flex items-center gap-1.5">
              <label htmlFor="chemistry-select" className="text-xs font-medium text-textMuted hidden md:inline-block">
                {isRtl ? 'استایل دیزاین:' : 'Chemistry:'}
              </label>
              <select
                id="chemistry-select"
                value={chemistry}
                onChange={(e) => setChemistry(e.target.value as VisualChemistryId)}
                aria-label="Select Visual Chemistry"
                className="rounded-lg border border-border bg-surface px-2.5 py-1.5 text-xs font-semibold text-textPrimary shadow-xs transition-colors hover:border-accent focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent cursor-pointer min-h-[36px]"
              >
                <option value="MINIMALIST_SAAS">Minimalist SaaS</option>
                <option value="LUXURY_GLASS_2">Luxury Glass 2.0</option>
                <option value="NEOBRUTALISM">Neobrutalism</option>
                <option value="SWISS_EDITORIAL">Swiss Editorial</option>
                <option value="STRIPE_CRISP_LIGHT">Stripe Crisp Light</option>
              </select>
            </div>

            {/* Language Toggle (EN / FA) */}
            <button
              type="button"
              onClick={() => setLang((prev) => (prev === 'en' ? 'fa' : 'en'))}
              aria-label={isRtl ? 'تغییر زبان به انگلیسی' : 'Switch language to Persian'}
              className="inline-flex items-center gap-1.5 rounded-lg border border-border bg-surface px-2.5 py-1.5 text-xs font-semibold text-textPrimary shadow-xs transition-all hover:bg-border/20 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent min-h-[36px] cursor-pointer"
            >
              {/* Globe Pure SVG Icon */}
              <svg
                className="h-3.5 w-3.5 text-accent"
                viewBox="0 0 16 16"
                fill="none"
                stroke="currentColor"
                strokeWidth="1.75"
                strokeLinecap="round"
                strokeLinejoin="round"
                aria-hidden="true"
              >
                <circle cx="8" cy="8" r="6.25" />
                <path d="M1.75 8H14.25" />
                <path d="M8 1.75C9.5 3.5 10.5 5.7 10.5 8C10.5 10.3 9.5 12.5 8 14.25C6.5 12.5 5.5 10.3 5.5 8C5.5 5.7 6.5 3.5 8 1.75Z" />
              </svg>
              <span>{lang === 'en' ? 'فارسی (RTL)' : 'English (LTR)'}</span>
            </button>

            {/* GitHub Repo Link */}
            <a
              href="https://github.com/omid-io/vibe-ui-suite"
              target="_blank"
              rel="noopener noreferrer"
              aria-label="View Vibe UI repository on GitHub"
              className="hidden sm:inline-flex items-center gap-1.5 rounded-lg border border-border bg-surface px-2.5 py-1.5 text-xs font-medium text-textMuted shadow-xs transition-colors hover:text-textPrimary hover:bg-border/20 min-h-[36px]"
            >
              {/* GitHub SVG Octocat */}
              <svg
                className="h-3.5 w-3.5 text-textPrimary"
                viewBox="0 0 16 16"
                fill="currentColor"
                aria-hidden="true"
              >
                <path d="M8 0C3.58 0 0 3.58 0 8C0 11.54 2.29 14.53 5.47 15.59C5.87 15.66 6.02 15.42 6.02 15.21C6.02 15.02 6.01 14.39 6.01 13.72C4 14.09 3.48 13.23 3.32 12.78C3.23 12.55 2.84 11.84 2.5 11.65C2.22 11.5 1.82 11.13 2.49 11.12C3.12 11.11 3.57 11.7 3.72 11.94C4.44 13.15 5.59 12.81 6.05 12.6C6.12 12.08 6.33 11.73 6.56 11.53C4.78 11.33 2.92 10.64 2.92 7.58C2.92 6.71 3.23 5.99 3.74 5.43C3.66 5.23 3.38 4.41 3.82 3.31C3.82 3.31 4.49 3.1 6.02 4.13C6.66 3.95 7.34 3.86 8.02 3.86C8.7 3.86 9.38 3.95 10.02 4.13C11.55 3.09 12.22 3.31 12.22 3.31C12.66 4.41 12.38 5.23 12.3 5.43C12.81 5.99 13.12 6.7 13.12 7.58C13.12 10.65 11.25 11.33 9.47 11.53C9.76 11.78 10.01 12.26 10.01 13.01C10.01 14.08 10 14.94 10 15.21C10 15.42 10.15 15.67 10.55 15.59C13.71 14.53 16 11.53 16 8C16 3.58 12.42 0 8 0Z" />
              </svg>
              <span>GitHub</span>
            </a>

          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1">
        {/* Hero Section with Embedded AiThinkingDrawer */}
        <HeroSection
          chemistry={chemistry}
          isRtl={isRtl}
          onDeployClick={() => alert(isRtl ? 'دستور استقرار پایپ لاین ارسال شد' : 'Pipeline deployment initiated')}
          onSpecClick={() => alert(isRtl ? 'سند دیزاین در حال بارگذاری است' : 'Opening canonical design-spec.json')}
        />

        {/* Visual Chemistries Showcase Matrix */}
        <section className="container mx-auto px-4 sm:px-6 lg:px-8 max-w-7xl py-12 border-b border-border">
          <div className="flex flex-col items-start text-start space-y-2 mb-8">
            <span className="text-xs font-mono font-semibold uppercase tracking-wider text-accent">
              {isRtl ? 'مجموعه ۵ استایل اصلی' : 'Anti-Repetition Protocol'}
            </span>
            <h2 className="text-2xl sm:text-3xl font-bold tracking-tight text-textPrimary">
              {isRtl ? 'تنوع بصری هوشمند و ضد یکنواختی' : '5 Bespoke Visual Chemistries'}
            </h2>
            <p className="text-sm text-textMuted max-w-2xl">
              {isRtl
                ? 'به جای تولید صفحات تکراری و کلیشه ای، ایجنت به صورت خودکار یکی از ۵ ساختار دیزاین زیر را متناسب با حوزه انتخاب می کند.'
                : 'Vibe UI eliminates monotonous AI slop by actively alternating across 5 production-grade design archetypes.'}
            </p>
          </div>

          {/* Interactive Chemistry Cards Grid */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
            {(Object.keys(VISUAL_CHEMISTRIES) as VisualChemistryId[]).map((id) => {
              const theme = VISUAL_CHEMISTRIES[id];
              const isSelected = chemistry === id;

              return (
                <button
                  key={id}
                  type="button"
                  onClick={() => setChemistry(id)}
                  className={cn(
                    'flex flex-col items-start text-start p-4 rounded-xl border transition-all duration-150 cursor-pointer min-h-[44px]',
                    isSelected
                      ? 'border-accent bg-surface ring-2 ring-accent shadow-md'
                      : 'border-border bg-surface/50 hover:bg-surface hover:border-border/80 shadow-xs'
                  )}
                >
                  <div className="flex items-center justify-between w-full mb-2">
                    <span className="text-xs font-mono font-bold text-accent">
                      0{Object.keys(VISUAL_CHEMISTRIES).indexOf(id) + 1}
                    </span>
                    {isSelected && (
                      <span className="flex h-2 w-2 rounded-full bg-accent" aria-hidden="true" />
                    )}
                  </div>
                  <h3 className="text-sm font-bold text-textPrimary leading-snug mb-1">
                    {theme.name}
                  </h3>
                  <p className="text-xs text-textMuted line-clamp-2">
                    {theme.tagline}
                  </p>
                  <div className="mt-3 pt-2 border-t border-border/40 w-full flex items-center justify-between text-[11px] font-mono text-textMuted">
                    <span className="ltr-code">{id.split('_')[0]}</span>
                    <span className="text-accent font-medium">Select &rarr;</span>
                  </div>
                </button>
              );
            })}
          </div>
        </section>

        {/* 4-Pillar Engineering Bento Grid */}
        <section className="container mx-auto px-4 sm:px-6 lg:px-8 max-w-7xl py-12">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            
            {/* Tile 1: WCAG AA Mathematical Contrast */}
            <div className="rounded-xl border border-border bg-surface p-6 space-y-3 shadow-xs">
              <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-accent/15 text-accent">
                <svg className="h-5 w-5" viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="2">
                  <circle cx="8" cy="8" r="6.25" />
                  <path d="M8 1.75V14.25C11.45 14.25 14.25 11.45 14.25 8C14.25 4.55 11.45 1.75 8 1.75Z" fill="currentColor" />
                </svg>
              </div>
              <h3 className="text-base font-bold text-textPrimary">
                {isRtl ? 'محاسبه ریاضی کنتراست WCAG' : 'Mathematical WCAG AA'}
              </h3>
              <p className="text-xs text-textMuted leading-relaxed">
                {isRtl
                  ? 'تمامی رنگ ها در فضای OKLCH اعتبارسنجی شده و حداقل کنتراست ۴.۵:۱ برای متن و ۳:۱ برای تیترها تضمین می شود.'
                  : 'Calculates exact relative luminance in OKLCH space, guaranteeing >= 4.5:1 for body copy and >= 3.0:1 for headlines.'}
              </p>
              <div className="ltr-code text-xs font-mono bg-canvas rounded-md p-2 border border-border text-emerald-500">
                RATIO: 19.07:1 (WCAG AA PASS)
              </div>
            </div>

            {/* Tile 2: Frame-Rate-Independent Physics */}
            <div className="rounded-xl border border-border bg-surface p-6 space-y-3 shadow-xs">
              <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-accent/15 text-accent">
                <svg className="h-5 w-5" viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M2.5 8H13.5M13.5 8L9.5 4M13.5 8L9.5 12" strokeLinecap="round" strokeLinejoin="round" />
                </svg>
              </div>
              <h3 className="text-base font-bold text-textPrimary">
                {isRtl ? 'فیزیک مستقل از نرخ فریم' : 'DeltaTime Motion Physics'}
              </h3>
              <p className="text-xs text-textMuted leading-relaxed">
                {isRtl
                  ? 'حرکات نرم و اسکرول پیوسته بدون وابستگی به فریم ریت با فرمول میراشوندگی نمایی یکپارچه اجرا می شوند.'
                  : 'Exponential decay integration across 60Hz, 120Hz, and 144Hz displays with lambda decay physics.'}
              </p>
              <div className="ltr-code text-xs font-mono bg-canvas rounded-md p-2 border border-border text-textPrimary">
                alpha = 1 - exp(-14 * dt)
              </div>
            </div>

            {/* Tile 3: Fixed-Structure Semantic RTL */}
            <div className="rounded-xl border border-border bg-surface p-6 space-y-3 shadow-xs">
              <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-accent/15 text-accent">
                <svg className="h-5 w-5" viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M3 4.5H13M3 8H9.5M3 11.5H13" strokeLinecap="round" strokeLinejoin="round" />
                </svg>
              </div>
              <h3 className="text-base font-bold text-textPrimary">
                {isRtl ? 'ثبات ساختاری راست چین' : 'Fixed-Structure Semantic RTL'}
              </h3>
              <p className="text-xs text-textMuted leading-relaxed">
                {isRtl
                  ? 'گریدها و ستون های ماکرو قفل می مانند؛ تغییر جهت صرفاً روی پاراگراف ها و کلمات انگلیسی در تگ bdi اعمال می شود.'
                  : 'Macro grid coordinates remain physically locked while typography adopts semantic RTL with bidi isolation.'}
              </p>
              <div className="ltr-code text-xs font-mono bg-canvas rounded-md p-2 border border-border text-accent">
                LAYOUT: STABLE | BIDI: ISOLATED
              </div>
            </div>

          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="border-t border-border bg-surface/50 py-8 text-xs text-textMuted">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8 max-w-7xl flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <span className="font-bold text-textPrimary">Vibe UI</span>
            <span>—</span>
            <span>Next.js 15 App Router Production Starter</span>
          </div>
          <div className="ltr-code font-mono">
            MIT License &copy; 2026 Omid Zaferi. Part of Vibe UI Skills.
          </div>
        </div>
      </footer>
    </div>
  );
}
