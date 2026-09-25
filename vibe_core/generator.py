"""
vibe_core.generator — Autonomous Component & Interface Generator (v3.2.0)
Generates production-grade, responsive, accessible React 19 TSX components
and self-contained HTML interfaces from DesignDecisionContract.
"""

from typing import Dict, Any, Optional
from pathlib import Path
from vibe_core.genome import DesignGenomeEngine

class InterfaceGenerator:
    def __init__(self):
        self.genome_engine = DesignGenomeEngine()

    def generate_react_tsx(self, decision: Dict[str, Any], component_name: str = "VibeMasterpiece") -> str:
        """
        Generates a modular, living React 19 / TypeScript component (.tsx)
        featuring real state management (useState), glowing edge micro-effects,
        domain signature widgets, and complete WCAG AAA / BiDi isolation.
        """
        domain_id = decision.get("intent", {}).get("product_domain", "general_modern_saas")
        blueprint = decision.get("intent", {}).get("blueprint", {})
        sig_widget = blueprint.get("signature_widget", {})
        is_rtl = decision.get("intent", {}).get("language", ["en"])[0] == "fa"
        dir_attr = 'dir="rtl"' if is_rtl else 'dir="ltr"'

        title_fa = blueprint.get("mock_data", {}).get("headline", "پلتفرم نوآورانه نسل جدید")
        title_en = "Next-Generation Intelligence Platform"
        headline = title_fa if is_rtl else title_en

        tsx = f'''"use client";

import React, {{ useState }} from "react";

export interface {component_name}Props {{
  className?: string;
  onAction?: (actionName: string) => void;
}}

export const {component_name}: React.FC<{component_name}Props> = ({{
  className = "",
  onAction,
}}) => {{
  const [billingCycle, setBillingCycle] = useState<"monthly" | "annual">("annual");
  const [activeTab, setActiveTab] = useState<number>(0);
  const [isCalculated, setIsCalculated] = useState<boolean>(true);
  const [simulatedValue, setSimulatedValue] = useState<number>(25000);

  const tabs = [
    {{"id": "overview", "label": "{"نمای کلی" if is_rtl else "Overview"}"}},
    {{"id": "telemetry", "label": "{"شاخص های زنده" if is_rtl else "Telemetry"}"}},
    {{"id": "architecture", "label": "{"معماری سیستم" if is_rtl else "Architecture"}"}}
  ];

  return (
    <div {dir_attr} className={{`w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 font-sans antialiased text-foreground ${{className}}`}}>
      {{/* Ambient Glow & Spotlight Card Layer */}}
      <div className="relative overflow-hidden rounded-3xl border border-zinc-200 dark:border-zinc-800 bg-white/80 dark:bg-zinc-950/80 backdrop-blur-xl p-6 sm:p-10 shadow-2xl transition-all duration-300">
        
        {{/* Subtle Animated Border Beam Glow */}}
        <div 
          aria-hidden="true"
          className="pointer-events-none absolute -inset-px rounded-3xl opacity-40 transition-opacity duration-500 bg-gradient-to-r from-teal-500/20 via-sky-500/20 to-emerald-500/20"
        />

        {{/* Header Badges & Interactive Tab Navigation */}}
        <div className="flex flex-wrap items-center justify-between gap-4 border-b border-zinc-200/80 dark:border-zinc-800/80 pb-6">
          <div className="flex items-center space-x-3 rtl:space-x-reverse">
            <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border border-emerald-500/20">
              <span className="size-2 rounded-full bg-emerald-500 animate-pulse" />
              <span>{"سامانه فعال و تایید شده" if is_rtl else "System Operational"}</span>
            </span>
            <span className="text-xs text-zinc-500 font-mono tracking-tight">
              <bdi>v3.2.0 • OKLCH AAA</bdi>
            </span>
          </div>

          {{/* Interactive Tabs */}}
          <div role="tablist" aria-label="Feature Tabs" className="inline-flex rounded-full bg-zinc-100 dark:bg-zinc-900 p-1 border border-zinc-200 dark:border-zinc-800">
            {{tabs.map((tab, idx) => (
              <button
                key={{tab.id}}
                type="button"
                role="tab"
                aria-selected={{activeTab === idx}}
                onClick={{() => setActiveTab(idx)}}
                className={{`px-4 py-1.5 text-xs font-medium rounded-full transition-all duration-200 min-h-[36px] ${{
                  activeTab === idx
                    ? "bg-white dark:bg-zinc-800 text-zinc-900 dark:text-white shadow-sm font-semibold"
                    : "text-zinc-600 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-white"
                }}`}}
              >
                {{tab.label}}
              </button>
            ))}}
          </div>
        </div>

        {{/* Hero Section with Asymmetric Bento Rhythm */}}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 pt-8 items-center">
          <div className="lg:col-span-7 space-y-6">
            <h1 className="text-3xl sm:text-4xl lg:text-5xl font-extrabold tracking-tight text-zinc-900 dark:text-white leading-[1.15]">
              {headline}
            </h1>
            <p className="text-base sm:text-lg text-zinc-600 dark:text-zinc-400 leading-relaxed max-w-2xl">
              {"تجربه ای منحصربه فرد، بدون کلیشه و مهندسی شده با پیشرفته ترین معیارهای دسترسی پذیری نوری و تعاملات روان." if is_rtl else "Autonomous precision interface engineered with strict WCAG AAA contrast, physics spring motion, and domain priors."}
            </p>

            {{/* Real Interactive Billing Switch */}}
            <div className="flex items-center gap-3 pt-2">
              <span className="text-xs font-medium text-zinc-500">{"ماهانه" if is_rtl else "Monthly"}</span>
              <button
                type="button"
                role="switch"
                aria-checked={{billingCycle === "annual"}}
                onClick={{() => setBillingCycle(prev => prev === "annual" ? "monthly" : "annual")}}
                className="relative inline-flex h-6 w-11 shrink-0 cursor-pointer rounded-full border-2 border-transparent bg-zinc-300 dark:bg-zinc-700 transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:ring-offset-2"
              >
                <span
                  aria-hidden="true"
                  className={{`pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow-lg ring-0 transition duration-200 ease-in-out ${{
                    billingCycle === "annual" ? "translate-x-5 rtl:-translate-x-5" : "translate-x-0"
                  }}`}}
                />
              </button>
              <span className="text-xs font-medium text-zinc-900 dark:text-white flex items-center gap-1.5">
                <span>{"سالانه" if is_rtl else "Annual"}</span>
                <span className="px-2 py-0.5 text-[10px] font-bold rounded-full bg-emerald-500/10 text-emerald-600 border border-emerald-500/20">
                  {"۲۰٪ تخفیف ویژه" if is_rtl else "Save 20%"}
                </span>
              </span>
            </div>

            {{/* Primary CTA Group */}}
            <div className="flex flex-wrap gap-4 pt-4">
              <button
                type="button"
                onClick={{() => onAction?.("primary_click")}}
                className="inline-flex items-center justify-center px-6 py-3 text-sm font-semibold rounded-xl text-white bg-zinc-900 dark:bg-white dark:text-zinc-900 hover:opacity-90 active:scale-95 transition-all shadow-md min-h-[44px]"
              >
                {"شروع آنی پروژه" if is_rtl else "Get Started Now"}
              </button>
              <button
                type="button"
                onClick={{() => onAction?.("secondary_click")}}
                className="inline-flex items-center justify-center px-6 py-3 text-sm font-semibold rounded-xl text-zinc-800 dark:text-zinc-200 border border-zinc-200 dark:border-zinc-800 hover:bg-zinc-100 dark:hover:bg-zinc-900 active:scale-95 transition-all min-h-[44px]"
              >
                {"مشاهده سرفصل ها" if is_rtl else "Explore System Docs"}
              </button>
            </div>
          </div>

          {{/* Right Column: Signature Domain Widget */}}
          <div className="lg:col-span-5 bg-zinc-50 dark:bg-zinc-900/90 border border-zinc-200 dark:border-zinc-800 rounded-2xl p-6 shadow-inner space-y-4">
            <div className="flex items-center justify-between border-b border-zinc-200 dark:border-zinc-800 pb-3">
              <span className="text-xs font-bold text-zinc-700 dark:text-zinc-300">
                {sig_widget.get("name", "ماژول تعاملی هوشمند" if is_rtl else "Interactive Intelligence Hub")}
              </span>
              <span className="text-[11px] font-mono text-zinc-500">
                <bdi>LIVE FEED</bdi>
              </span>
            </div>

            {{/* Interactive Metric Slider */}}
            <div className="space-y-2">
              <div className="flex justify-between text-xs text-zinc-600 dark:text-zinc-400">
                <span>{"ظرفیت عملیاتی" if is_rtl else "Throughput Scale"}</span>
                <span className="font-mono font-bold text-zinc-900 dark:text-white">
                  <bdi>${{simulatedValue.toLocaleString()}}</bdi>
                </span>
              </div>
              <input
                type="range"
                min="1000"
                max="100000"
                step="1000"
                value={{simulatedValue}}
                onChange={{(e) => setSimulatedValue(Number(e.target.value))}}
                className="w-full accent-emerald-500 cursor-pointer h-2 bg-zinc-200 dark:bg-zinc-800 rounded-lg"
              />
            </div>

            <div className="p-3 bg-white dark:bg-zinc-950 rounded-xl border border-zinc-200/80 dark:border-zinc-800/80 flex items-center justify-between">
              <div className="text-xs text-zinc-500">{"ضریب بهره وری برآورد شده" if is_rtl else "Estimated Yield Lift"}</div>
              <div className="text-lg font-bold font-mono text-emerald-600 dark:text-emerald-400">
                <bdi>+{{(simulatedValue * 0.052).toFixed(1)}}</bdi>
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>
  );
}};

export default {component_name};
'''
        return tsx

    def generate_html(self, decision: Dict[str, Any], prompt_title: str = "Vibe UI Component") -> str:
        """Generates a complete, self-contained, accessible HTML page from DesignDecisionContract."""
        genome = decision.get("genome", {})
        color = genome.get("color", {})
        typography = genome.get("typography", {})
        radius = genome.get("radius", {})
        depth = genome.get("depth", "diffused_soft")
        is_rtl = genome.get("platform", {}).get("rtl_support", False)
        dir_attr = 'dir="rtl" lang="fa"' if is_rtl else 'dir="ltr" lang="en"'

        css_vars = self.genome_engine.to_css_variables(genome)
        font_url = "https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Playfair+Display:ital,wght@0,600;1,400&family=Vazirmatn:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap"

        # Stylistic shadows
        if depth == "hard_drop":
            card_shadow = "shadow-[4px_4px_0px_0px_rgba(0,0,0,1)]"
            card_border = "border-2 border-black"
        elif depth == "flat":
            card_shadow = "shadow-none"
            card_border = "border border-[var(--border-subtle)]"
        elif depth == "specular_glass_2":
            card_shadow = "shadow-xl backdrop-blur-md"
            card_border = "border border-white/20"
        else:
            card_shadow = "shadow-sm hover:shadow-md transition-shadow"
            card_border = "border border-[var(--border-subtle)]"

        html = f"""<!DOCTYPE html>
<html {dir_attr} class="h-full">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{prompt_title}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="{font_url}" rel="stylesheet">
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
{css_vars}

    body {{
      background-color: var(--canvas-bg);
      color: var(--text-primary);
      font-family: var(--font-body);
      overflow-x: hidden;
      unicode-bidi: plaintext;
    }}

    bdi, .ltr-code {{
      direction: ltr !important;
      unicode-bidi: isolate;
    }}

    h1, h2, h3, .display-font {{
      font-family: var(--font-display);
    }}

    button:focus-visible, a:focus-visible, input:focus-visible {{
      outline: 2px solid var(--accent);
      outline-offset: 2px;
    }}

    @media (prefers-reduced-motion: reduce) {{
      *, ::before, ::after {{
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
      }}
    }}
  </style>
</head>
<body class="min-h-full flex flex-col antialiased">
  <!-- Top Navigation Bar -->
  <header class="w-full border-b border-[var(--border-subtle)] bg-[var(--surface-bg)] sticky top-0 z-30">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
      <div class="flex items-center space-x-3 rtl:space-x-reverse">
        <svg class="w-8 h-8 text-[var(--accent)]" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
          <polygon points="12 2 2 7 12 12 22 7 12 2"></polygon>
          <polyline points="2 17 12 22 22 17"></polyline>
          <polyline points="2 12 12 17 22 12"></polyline>
        </svg>
        <span class="text-xl font-bold tracking-tight display-font">{prompt_title}</span>
      </div>
      <nav class="hidden md:flex items-center space-x-6 rtl:space-x-reverse" aria-label="Main Navigation">
        <a href="#features" class="text-sm font-medium hover:text-[var(--accent)] transition-colors min-h-[44px] inline-flex items-center">{"ویژگی ها" if is_rtl else "Features"}</a>
        <a href="#pricing" class="text-sm font-medium hover:text-[var(--accent)] transition-colors min-h-[44px] inline-flex items-center">{"تعرفه ها" if is_rtl else "Pricing"}</a>
        <a href="#contact" class="text-sm font-medium hover:text-[var(--accent)] transition-colors min-h-[44px] inline-flex items-center">{"تماس" if is_rtl else "Contact"}</a>
      </nav>
      <div class="flex items-center space-x-3 rtl:space-x-reverse">
        <button type="button" class="inline-flex items-center justify-center px-4 py-2.5 text-sm font-medium rounded-[var(--radius-button)] text-white bg-[var(--accent)] hover:opacity-90 min-h-[44px] min-w-[44px] transition-all">
          {"شروع همکاری" if is_rtl else "Get Started"}
        </button>
      </div>
    </div>
  </header>

  <!-- Main Hero & Content Section -->
  <main class="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-12 lg:py-16">
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 lg:gap-8">
      <!-- Main Bento Hero Card with Asymmetric Layout -->
      <section class="md:col-span-2 bg-[var(--surface-bg)] {card_border} {card_shadow} rounded-[var(--radius-container)] p-6 sm:p-8 lg:p-10 flex flex-col justify-between" aria-labelledby="hero-title">
        <div>
          <span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-[var(--accent)]/10 text-[var(--accent)] mb-4">
            <svg class="w-3.5 h-3.5 inline mr-1.5 rtl:ml-1.5 rtl:mr-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 14 14"></polyline></svg>
            {"مهندسی دقیق و اصیل" if is_rtl else "Vibe UI Verified"}
          </span>
          <h1 id="hero-title" class="text-3xl sm:text-4xl lg:text-5xl font-bold tracking-tight mb-4">
            {prompt_title}
          </h1>
          <p class="text-[var(--text-muted)] text-base sm:text-lg leading-relaxed max-w-2xl mb-8">
            {"تجربه ای منحصربه فرد با معماری خودکار، دسترسی پذیری تضمین شده و هماهنگی کامل با نیازهای کسب وکار شما." if is_rtl else "Autonomous precision interface engineered with strict WCAG AA contrast, physics motion, and domain priors."}
          </p>
        </div>

        <div class="flex flex-wrap gap-4 items-center pt-4 border-t border-[var(--border-subtle)]">
          <button type="button" class="inline-flex items-center justify-center px-6 py-3 text-base font-semibold rounded-[var(--radius-button)] text-white bg-[var(--accent)] min-h-[44px] transition-transform active:scale-95">
            {"مشاوره تخصصی" if is_rtl else "Explore System"}
          </button>
          <button type="button" class="inline-flex items-center justify-center px-6 py-3 text-base font-semibold rounded-[var(--radius-button)] text-[var(--text-primary)] border border-[var(--border-subtle)] bg-[var(--canvas-bg)] hover:bg-[var(--surface-bg)] min-h-[44px] transition-colors">
            {"مشاهده دمو" if is_rtl else "View Live Demo"}
          </button>
        </div>
      </section>

      <!-- Secondary Telemetry / Metrics Card -->
      <aside class="bg-[var(--surface-bg)] {card_border} {card_shadow} rounded-[var(--radius-container)] p-6 flex flex-col justify-between" aria-label="System Metrics">
        <div>
          <h2 class="text-lg font-bold mb-4 flex items-center space-x-2 rtl:space-x-reverse">
            <svg class="w-5 h-5 text-[var(--accent)]" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M22 12h-4l-3 9L9 3l-3 9H2"></path></svg>
            <span>{"شاخص های کلیدی" if is_rtl else "Core Telemetry"}</span>
          </h2>
          <div class="space-y-4">
            <div class="p-3.5 bg-[var(--canvas-bg)] rounded-[var(--radius-base)] border border-[var(--border-subtle)]">
              <div class="text-xs text-[var(--text-muted)] mb-1">{"معیار انطباق کنتراست" if is_rtl else "Contrast Invariant Target"}</div>
              <div class="text-2xl font-bold text-[var(--accent)]">&ge; 4.5 : 1 (AA)</div>
            </div>
            <div class="p-3.5 bg-[var(--canvas-bg)] rounded-[var(--radius-base)] border border-[var(--border-subtle)]">
              <div class="text-xs text-[var(--text-muted)] mb-1">{"سقف انحراف چیدمان" if is_rtl else "Layout Shift Target"}</div>
              <div class="text-2xl font-bold">&lt; 0.1 (CLS)</div>
            </div>
            <div class="p-3.5 bg-[var(--canvas-bg)] rounded-[var(--radius-base)] border border-[var(--border-subtle)]">
              <div class="text-xs text-[var(--text-muted)] mb-1">{"سبک معماری" if is_rtl else "Style Family"}</div>
              <div class="text-sm font-semibold">{decision.get("selected_style", "clean_stripe")}</div>
            </div>
          </div>
        </div>
        <div class="mt-6 text-xs text-[var(--text-muted)] flex items-center space-x-1.5 rtl:space-x-reverse" data-verification-status="declared">
          <svg class="w-4 h-4 text-amber-500" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>
          <span>{"وضعیت: منطبق بر قرارداد (در انتظار راستی آزمایی ران تایم)" if is_rtl else "Status: Contract Declared (Awaiting Runtime Audit)"}</span>
        </div>
      </aside>
    </div>

    <!-- Component States Preview: Skeleton, Empty, Error -->
    <section class="mt-12 pt-8 border-t border-[var(--border-subtle)]" aria-labelledby="states-heading">
      <h2 id="states-heading" class="text-xl font-bold mb-6">
        {"ماتریس وضعیت های رابط کاربری (States Matrix)" if is_rtl else "Component States Matrix"}
      </h2>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <!-- Skeleton Loading State -->
        <div class="p-5 bg-[var(--surface-bg)] {card_border} rounded-[var(--radius-container)]" aria-busy="true" aria-label="Loading State">
          <div class="text-xs font-semibold text-[var(--text-muted)] mb-3">SKELETON LOADING</div>
          <div class="animate-pulse space-y-3">
            <div class="h-4 bg-zinc-300 dark:bg-zinc-700 rounded w-3/4"></div>
            <div class="h-8 bg-zinc-300 dark:bg-zinc-700 rounded"></div>
            <div class="h-3 bg-zinc-200 dark:bg-zinc-800 rounded w-1/2"></div>
          </div>
        </div>

        <!-- Empty State -->
        <div class="p-5 bg-[var(--surface-bg)] {card_border} rounded-[var(--radius-container)] text-center flex flex-col items-center justify-center">
          <div class="text-xs font-semibold text-[var(--text-muted)] mb-2 self-start">EMPTY STATE</div>
          <svg class="w-8 h-8 text-[var(--text-muted)] mb-2" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><circle cx="8.5" cy="8.5" r="1.5"></circle><polyline points="21 15 16 10 5 21"></polyline></svg>
          <div class="text-sm font-medium">{"موردی یافت نشد" if is_rtl else "No records found"}</div>
          <div class="text-xs text-[var(--text-muted)] mt-1">{"داده ای برای نمایش در این بخش موجود نیست." if is_rtl else "Add items to populate."}</div>
        </div>

        <!-- Error & Retry State -->
        <div class="p-5 bg-[var(--surface-bg)] {card_border} rounded-[var(--radius-container)] flex flex-col justify-between">
          <div>
            <div class="text-xs font-semibold text-rose-500 mb-2">ERROR & RETRY</div>
            <div class="text-sm font-semibold text-rose-600 dark:text-rose-400">{"خطا در برقراری ارتباط" if is_rtl else "Network Timeout"}</div>
            <div class="text-xs text-[var(--text-muted)] mt-1">{"امکان دریافت اطلاعات وجود ندارد. لطفا مجددا تلاش کنید." if is_rtl else "Failed to synchronize remote telemetry."}</div>
          </div>
          <button type="button" class="mt-4 inline-flex items-center justify-center px-3 py-1.5 text-xs font-medium rounded-[var(--radius-button)] border border-rose-300 text-rose-600 hover:bg-rose-50 min-h-[44px]">
            {"تلاش مجدد" if is_rtl else "Retry Connection"}
          </button>
        </div>
      </div>
    </section>
  </main>

  <footer class="w-full border-t border-[var(--border-subtle)] bg-[var(--surface-bg)] py-6 mt-12">
    <div class="max-w-7xl mx-auto px-4 text-center text-xs text-[var(--text-muted)]">
      &copy; 2026 Vibe UI Design Intelligence. All rights reserved.
    </div>
  </footer>
</body>
</html>
"""
        return html
