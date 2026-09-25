'use client';

import React from 'react';
import { cn } from '@/lib/utils';
import { VisualChemistryId, VISUAL_CHEMISTRIES } from '@/lib/tokens';
import { AiThinkingDrawer, ThinkingStep, ToolExecutionChip } from './AiThinkingDrawer';

export interface HeroSectionProps {
  chemistry?: VisualChemistryId;
  isRtl?: boolean;
  className?: string;
  onDeployClick?: () => void;
  onSpecClick?: () => void;
}

export function HeroSection({
  chemistry = 'MINIMALIST_SAAS',
  isRtl = false,
  className,
  onDeployClick,
  onSpecClick,
}: HeroSectionProps) {
  const currentChemistry = VISUAL_CHEMISTRIES[chemistry] || VISUAL_CHEMISTRIES.MINIMALIST_SAAS;

  const persianSteps: ThinkingStep[] = [
    {
      id: 'fa-s1',
      label: 'پردازش پرامپت کاربر و محاسبه سقف ابهام (سطح ۱)',
      status: 'completed',
      duration: '18ms',
    },
    {
      id: 'fa-s2',
      label: 'اعتبارسنجی قرارداد ماشین design-spec.json طبق استاندارد Draft 2020-12',
      status: 'completed',
      duration: '42ms',
    },
    {
      id: 'fa-s3',
      label: 'محاسبه درخشندگی نسبی رنگ های OKLCH و رعایت کنتراست ۴.۵:۱',
      status: 'completed',
      duration: '112ms',
    },
    {
      id: 'fa-s4',
      label: 'قفل موقعیت فیزیکی گریدها و اعمال جهت دهی معنایی به متون فارسی',
      status: 'completed',
      duration: '256ms',
    },
  ];

  const tools: ToolExecutionChip[] = [
    { name: 'query_rag()', latency: '48ms', status: 'cached' },
    { name: 'compile_spec()', latency: '124ms', status: 'executed' },
    { name: 'verify_a11y()', latency: '16ms', status: 'verified' },
  ];

  return (
    <section
      aria-label="Vibe UI Starter Hero"
      className={cn(
        'relative w-full overflow-hidden border-b border-border bg-canvas text-textPrimary transition-colors duration-200 py-12 md:py-20 lg:py-24',
        className
      )}
    >
      {/* Decorative Ambient Background Glow (Compositing Budget <= 1 blur layer) */}
      <div
        className="pointer-events-none absolute -top-28 start-1/2 -translate-x-1/2 h-80 w-[42rem] max-w-[90vw] rounded-full bg-accent/10 blur-3xl"
        aria-hidden="true"
      />

      <div className="container mx-auto px-4 sm:px-6 lg:px-8 relative z-10 max-w-7xl">
        {/* Physical 2-Column Responsive Layout (Preserved Physically Across LTR and RTL) */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-12 items-start">
          
          {/* Column 1: Editorial Value & Action Copy (7 Cols) */}
          <div className="lg:col-span-7 flex flex-col items-start text-start space-y-6">
            
            {/* Architecture Pill / Domain Badge */}
            <div className="inline-flex items-center gap-2 rounded-full border border-border bg-surface px-3.5 py-1.5 text-xs font-mono font-medium text-textMuted shadow-xs">
              <span className="flex h-2 w-2 rounded-full bg-accent animate-pulse" aria-hidden="true" />
              {isRtl ? (
                <span>
                  معماری <bdi className="font-semibold text-textPrimary">Vibe UI</bdi> // استارتر پروداکشن
                </span>
              ) : (
                <span>
                  VIBE UI // PRODUCTION STARTER // <span className="text-textPrimary font-semibold">{currentChemistry.name}</span>
                </span>
              )}
            </div>

            {/* Headline */}
            <h1 className="text-3xl sm:text-4xl lg:text-5xl font-extrabold tracking-tight text-textPrimary leading-[1.15]">
              {isRtl ? (
                <>
                  معماری قطعی رابط کاربری برای ایجنت های کدنویسی{' '}
                  <span className="text-accent underline decoration-accent/40 decoration-2 underline-offset-4">
                    هوش مصنوعی
                  </span>
                </>
              ) : (
                <>
                  Deterministic UI Architecture for Autonomous{' '}
                  <span className="text-accent underline decoration-accent/40 decoration-2 underline-offset-4">
                    AI Coding Agents
                  </span>
                </>
              )}
            </h1>

            {/* Value-Focused Copy with BiDi Isolation */}
            <p className="text-base sm:text-lg text-textMuted leading-relaxed max-w-2xl">
              {isRtl ? (
                <>
                  پایان خطاهای رندوم طراحی با توکن های رنگی{' '}
                  <bdi className="font-mono font-semibold text-textPrimary">OKLCH</bdi>، موتور فیزیک مستقل از نرخ
                  فریم، آیکون های وکتور خالص <bdi className="font-mono font-semibold text-textPrimary">SVG</bdi> و
                  ثبات ساختاری <bdi className="font-mono font-semibold text-textPrimary">Semantic RTL</bdi> در پشته{' '}
                  <bdi className="font-mono font-semibold text-textPrimary">Next.js 15 App Router</bdi>.
                </>
              ) : (
                <>
                  Eliminate unpredictable AI design drift with typed <bdi className="font-mono font-medium text-textPrimary">OKLCH</bdi> color
                  spaces, frame-rate-independent physics, zero-emoji SVG iconography, and fixed-structure semantic RTL.
                </>
              )}
            </p>

            {/* Action CTAs */}
            <div className="flex flex-wrap items-center gap-3 pt-2 w-full sm:w-auto">
              <button
                type="button"
                onClick={onDeployClick}
                className="inline-flex items-center justify-center gap-2 rounded-lg bg-accent px-5 py-2.5 text-sm font-semibold text-white shadow-sm transition-all duration-150 hover:opacity-90 active:scale-[0.98] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring min-h-[44px] cursor-pointer"
              >
                {/* Pure SVG Rocket / Deploy Icon */}
                <svg
                  className="h-4 w-4"
                  viewBox="0 0 16 16"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  aria-hidden="true"
                >
                  <path d="M9.5 2.5C9.5 2.5 13.5 3 13.5 6.5C13.5 10 9 13.5 9 13.5L8 11.5L4.5 8L2.5 7C2.5 7 6 2.5 9.5 2.5Z" />
                  <path d="M6 10L3.5 12.5" />
                  <circle cx="9.5" cy="6.5" r="1" fill="currentColor" />
                </svg>
                <span>{isRtl ? 'استقرار پایپ لاین' : 'Deploy Pipeline'}</span>
              </button>

              <button
                type="button"
                onClick={onSpecClick}
                className="inline-flex items-center justify-center gap-2 rounded-lg border border-border bg-surface px-5 py-2.5 text-sm font-semibold text-textPrimary shadow-xs transition-all duration-150 hover:bg-border/20 active:scale-[0.98] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring min-h-[44px] cursor-pointer"
              >
                {/* Pure SVG Document Spec Icon */}
                <svg
                  className="h-4 w-4 text-textMuted"
                  viewBox="0 0 16 16"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="1.75"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  aria-hidden="true"
                >
                  <path d="M3 2.5H9.5L13 6V13.5H3V2.5Z" />
                  <path d="M9.5 2.5V6H13" />
                  <path d="M5.5 9H10.5" />
                  <path d="M5.5 11.5H8.5" />
                </svg>
                <span>{isRtl ? 'مشاهده سند دیزاین' : 'View Design Spec'}</span>
              </button>
            </div>

            {/* Telemetry Metric HUD (Always in Strict LTR Monospace) */}
            <div className="w-full pt-4">
              <div className="ltr-code inline-flex flex-wrap items-center gap-3 rounded-lg border border-border bg-surface/80 px-3.5 py-2 text-xs font-mono text-textMuted shadow-xs">
                <span className="flex items-center gap-1 text-textPrimary font-semibold">
                  <svg
                    className="h-3 w-3 text-emerald-500"
                    viewBox="0 0 12 12"
                    fill="currentColor"
                    aria-hidden="true"
                  >
                    <circle cx="6" cy="6" r="4" />
                  </svg>
                  TELEMETRY
                </span>
                <span className="text-border">|</span>
                <span>
                  LATENCY: <strong className="text-textPrimary">1.2ms</strong>
                </span>
                <span className="text-border">|</span>
                <span>
                  UPTIME: <strong className="text-emerald-500">99.99%</strong>
                </span>
                <span className="text-border">|</span>
                <span>
                  CONTRAST: <strong className="text-emerald-500">&gt;= 4.5:1 (PASS)</strong>
                </span>
                <span className="text-border">|</span>
                <span>
                  PHYSICS: <strong className="text-textPrimary">120Hz DAMPED</strong>
                </span>
              </div>
            </div>

          </div>

          {/* Column 2: Live AI Primitive Showcase (5 Cols) */}
          <div className="lg:col-span-5 flex flex-col space-y-4">
            
            {/* Embedded Live AiThinkingDrawer */}
            <AiThinkingDrawer
              initialOpen={true}
              title={isRtl ? 'تحلیل زنده ایجنت دیزاین' : 'Live Agent Reasoning Trace'}
              durationMs={428}
              steps={isRtl ? persianSteps : undefined}
              tools={tools}
              isRtl={isRtl}
            />

            {/* Chemistry Architecture Details Card */}
            <div className="rounded-xl border border-border bg-surface/60 p-4 text-xs space-y-2">
              <div className="flex items-center justify-between">
                <span className="font-semibold text-textPrimary uppercase tracking-wider">
                  {isRtl ? 'خصوصیات ساختاری کمستری' : 'Chemistry Invariants'}
                </span>
                <span className="ltr-code font-mono text-accent font-semibold">
                  {chemistry}
                </span>
              </div>
              <p className="text-textMuted leading-relaxed">
                {currentChemistry.surfaceTreatment}
              </p>
              <div className="pt-2 flex flex-wrap gap-2 text-[11px] font-mono">
                <span className="ltr-code rounded bg-border/40 px-2 py-0.5 text-textPrimary">
                  canvas: {currentChemistry.colors.canvas}
                </span>
                <span className="ltr-code rounded bg-border/40 px-2 py-0.5 text-textPrimary">
                  accent: {currentChemistry.colors.primaryAccent}
                </span>
              </div>
            </div>

          </div>

        </div>
      </div>
    </section>
  );
}

export default HeroSection;
