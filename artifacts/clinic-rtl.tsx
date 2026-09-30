"use client";


import React, { useState } from "react";

export interface ClinicRtlProps {
  className?: string;
  onAction?: (actionName: string) => void;
}

export const ClinicRtl: React.FC<ClinicRtlProps> = ({
  className = "",
  onAction,
}) => {
  const [billingCycle, setBillingCycle] = useState<"monthly" | "annual">("annual");
  const [activeTab, setActiveTab] = useState<number>(0);
  const [simulatedValue, setSimulatedValue] = useState<number>(25000);
  const [splitPos, setSplitPos] = useState<number>(50);
  const [isLiveActive, setIsLiveActive] = useState<boolean>(true);

  const tabs = [
    {"id": "overview", "label": "نمای اصلی و ویجت تعاملی"},
    {"id": "telemetry", "label": "شاخص های عملکردی حوزه"},
    {"id": "architecture", "label": "معماری و مشخصات فنی"}
  ];

  return (
    <div dir="rtl" className={`w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 font-sans antialiased text-foreground ${className}`}>
      {/* Ambient Style-Compiled Card Layer */}
      <div className="relative bg-[#faf8f5] dark:bg-[#121110] border border-stone-200 dark:border-stone-800 rounded-sm p-6 sm:p-12 shadow-sm transition-all">
        

        {/* Header Badges & Interactive Tab Navigation */}
        <div className="flex flex-wrap items-center justify-between gap-4 border-b border-zinc-200/80 dark:border-zinc-800/80 pb-6">
          <div className="flex items-center space-x-3 rtl:space-x-reverse">
            <span className="inline-flex items-center gap-1.5 px-3 py-1 font-serif text-xs italic tracking-widest text-stone-800 dark:text-stone-200 border border-stone-300 dark:border-stone-700">
              <span className="size-2 rounded-full bg-emerald-500 animate-pulse" />
              <span>سامانه فعال و تایید شده</span>
            </span>
            <span className="text-xs font-serif text-stone-500">
              <bdi>v3.8.0 • OKLCH AAA</bdi>
            </span>
          </div>

          {/* Interactive Tabs with Full Accessibility Role */}
          <div role="tablist" aria-label="Feature Tabs" className="inline-flex border-b border-stone-200 dark:border-stone-800 gap-6 pb-2">
            {tabs.map((tab, idx) => (
              <button
                key={tab.id}
                type="button"
                role="tab"
                aria-selected={activeTab === idx}
                onClick={() => setActiveTab(idx)}
                className={`transition-all duration-200 min-h-[44px] ${
                  activeTab === idx ? "text-stone-900 dark:text-stone-100 font-serif italic border-b border-stone-900 dark:border-stone-100 pb-2" : "text-stone-400 hover:text-stone-700 dark:hover:text-stone-300 font-serif pb-2"
                }`}
              >
                {tab.label}
              </button>
            ))}
          </div>
        </div>

        {/* Tab Panel 0: Overview & Signature Domain Widget */}
        {activeTab === 0 && (
          <div role="tabpanel" className="space-y-6 pt-6 animate-fadeIn" data-layout-macro="split_laboratory_studio">
            <div className="flex items-center justify-between border-b border-zinc-200 dark:border-zinc-800 pb-4">
              <div className="space-y-1">
                <div className="text-xs font-mono text-emerald-600 dark:text-emerald-400 uppercase tracking-wider">
                  آزمایشگاه پژوهش و کالیبراسیون داده
                </div>
                <h1 className="text-3xl sm:text-4xl lg:text-5xl font-serif font-normal italic tracking-wide text-stone-900 dark:text-stone-100 leading-tight">
                  مراقبت پیشرفته پوست، زیبایی و جوانسازی بالینی
                </h1>
              </div>
              <div className="hidden sm:block">
                <div className="flex items-center gap-3 pt-2">
                <span className="text-xs font-medium text-zinc-500">ماهانه</span>
                <button
                  type="button"
                  role="switch"
                  aria-checked={billingCycle === "annual"}
                  aria-label="تغییر دوره پرداخت"
                  onClick={() => setBillingCycle(prev => prev === "annual" ? "monthly" : "annual")}
                  className="relative inline-flex min-h-[44px] min-w-[48px] items-center justify-center p-2 rounded-full cursor-pointer focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:ring-offset-2"
                >
                  <span className="relative inline-flex h-6 w-11 shrink-0 rounded-full border-2 border-transparent bg-zinc-300 dark:bg-zinc-700 transition-colors duration-200 ease-in-out">
                    <span
                      aria-hidden="true"
                      className={`pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow-lg ring-0 transition duration-200 ease-in-out ${
                        billingCycle === "annual" ? "translate-x-5 rtl:-translate-x-5" : "translate-x-0"
                      }`}
                    />
                  </span>
                </button>
                <span className="text-xs font-medium text-zinc-900 dark:text-white flex items-center gap-1.5">
                  <span>سالانه</span>
                  <span className="px-2 py-0.5 text-[10px] font-bold rounded-full bg-emerald-500/10 text-emerald-600 border border-emerald-500/20">
                    ۲۰٪ تخفیف ویژه
                  </span>
                </span>
              </div>
              </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
              {/* Parameter Console (5 Cols) */}
              <div className="lg:col-span-5 space-y-6">
                <p className="text-base sm:text-lg font-sans text-stone-600 dark:text-stone-400 leading-relaxed max-w-2xl font-light">
                  متخصصان دارای بورد با پروتکل های تایید شده بین المللی برای نتایج طبیعی و درخشان.
                </p>
                <div className="bg-[#f5f2ed] dark:bg-[#181716] border border-stone-200 dark:border-stone-800 rounded-sm p-6 space-y-4">
                  <div className="flex items-center justify-between border-b border-zinc-200 dark:border-zinc-800 pb-3">
                    <span className="text-xs font-mono font-bold text-zinc-700 dark:text-zinc-300">
                      LAB://Clinical Before/After Visualizer & Slot Picker
                    </span>
                    <button
                      type="button"
                      onClick={() => setIsLiveActive(prev => !prev)}
                      className="text-[11px] font-mono px-3 py-1.5 rounded border transition-colors min-h-[44px] inline-flex items-center justify-center bg-emerald-500/10 text-emerald-600 border-emerald-500/20"
                    >
                      <bdi>{isLiveActive ? "ACTIVE TEST" : "IDLE"}</bdi>
                    </button>
                  </div>
                  
              <div className="space-y-4" data-origin="synthetic_demo">
                <div className="flex justify-between items-center text-xs font-semibold text-stone-700 dark:text-stone-300">
                  <span>پروتکل لیزر جوانسازی پوست - نتایج بالینی</span>
                  <span className="px-2 py-0.5 rounded-full bg-emerald-100 dark:bg-emerald-950/60 text-emerald-700 dark:text-emerald-400 font-mono text-[10px] font-bold">
                    <bdi>98.4% بهبود بافت</bdi>
                  </span>
                </div>

                {/* Interactive Before/After Split Comparison */}
                <div className="relative h-44 rounded-xl overflow-hidden border border-stone-200 dark:border-stone-800 bg-stone-100 dark:bg-stone-900 select-none">
                  <div className="absolute inset-0 bg-gradient-to-r from-stone-300 to-amber-100 dark:from-stone-800 dark:to-amber-950/40 flex items-center justify-start p-4">
                    <span className="text-xs font-bold text-stone-500 uppercase tracking-widest">قبل از درمان</span>
                  </div>
                  <div
                    className="absolute inset-y-0 right-0 bg-gradient-to-l from-emerald-100 to-rose-50 dark:from-emerald-950/40 dark:to-rose-950/20 border-l-2 border-emerald-500 flex items-center justify-end p-4 transition-all duration-75"
                    style={{ width: `${100 - splitPos}%` }}
                  >
                    <span className="text-xs font-bold text-emerald-700 dark:text-emerald-400 uppercase tracking-widest">نتیجه ۴ هفته بعد</span>
                  </div>
                  <input
                    type="range"
                    min="0"
                    max="100"
                    value={splitPos}
                    onChange={(e) => setSplitPos(Number(e.target.value))}
                    data-vibe-control="split-slider"
                    aria-label="اسلایدر مقایسه نتایج بالینی پوست"
                    className="absolute inset-0 opacity-0 cursor-ew-resize w-full h-full z-10"
                  />
                  <div
                    className="absolute inset-y-0 w-1 bg-white shadow-[0_0_8px_rgba(0,0,0,0.3)] pointer-events-none z-0"
                    style={{ left: `${splitPos}%` }}
                  />
                </div>

                <div className="grid grid-cols-2 gap-3 text-xs">
                  <div className="p-2.5 rounded-lg bg-stone-50 dark:bg-stone-900/60 border border-stone-200 dark:border-stone-800">
                    <div className="text-stone-500 text-[10px]">یکنواختی ملانین</div>
                    <div className="font-mono font-bold text-stone-900 dark:text-stone-100"><bdi data-vibe-metric="melanin-uniformity">+{(splitPos * 0.42).toFixed(1)}%</bdi></div>
                  </div>
                  <div className="p-2.5 rounded-lg bg-stone-50 dark:bg-stone-900/60 border border-stone-200 dark:border-stone-800">
                    <div className="text-stone-500 text-[10px]">چگالی کلاژن لایه درم</div>
                    <div className="font-mono font-bold text-emerald-600 dark:text-emerald-400"><bdi data-vibe-metric="collagen-index">{Math.round(62 + splitPos * 0.36)} / 100</bdi></div>
                  </div>
                </div>
              </div>
                </div>
                <div className="flex flex-wrap gap-4 pt-4">
                <button
                  type="button"
                  onClick={() => onAction?.("primary_click")}
                  className="inline-flex items-center justify-center px-8 py-3 font-serif tracking-widest text-xs uppercase bg-stone-900 text-stone-50 dark:bg-stone-100 dark:text-stone-900 border border-stone-800 hover:bg-stone-800 dark:hover:bg-stone-200 transition-all min-h-[44px]"
                >
                  رزرو وقت مشاوره تخصصی
                </button>
                <button
                  type="button"
                  onClick={() => onAction?.("secondary_click")}
                  className="inline-flex items-center justify-center px-8 py-3 font-serif tracking-widest text-xs uppercase text-stone-800 dark:text-stone-200 border border-stone-300 dark:border-stone-700 hover:border-stone-900 transition-all min-h-[44px]"
                >
                  مشاهده تعرفه و لیست خدمات
                </button>
              </div>
              </div>

              {/* Viewport Visualizer (7 Cols) */}
              <div className="lg:col-span-7 space-y-6">
                
        <div className="relative overflow-hidden bg-zinc-100 dark:bg-zinc-900 aspect-[4/5] sm:aspect-[3/4] border border-stone-200/60 dark:border-stone-800/60 rounded-2xl shadow-sm flex flex-col justify-between p-4 group select-none" data-origin="synthetic_demo">
          <div className="flex items-center justify-between text-[11px] font-mono text-zinc-500 z-10">
            <span className="px-2 py-0.5 rounded bg-black/5 dark:bg-white/5 backdrop-blur-md border border-zinc-200/50 dark:border-zinc-700/50">
              <bdi>CLINICAL_PORTRAIT</bdi>
            </span>
            <span className="inline-flex items-center gap-1.5 text-zinc-600 dark:text-zinc-400 font-mono text-[10px]">
              <span className="w-1.5 h-1.5 rounded-full bg-sky-500 animate-pulse"></span>
              <bdi>SYNTHETIC MEDIA SLOT — AWAITING SOURCE ASSET</bdi>
            </span>
          </div>

          <div className="absolute inset-0 flex items-center justify-center opacity-15 pointer-events-none">
            <svg className="w-20 h-20 text-zinc-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
          </div>

          <div className="z-10 bg-gradient-to-t from-black/70 via-black/30 to-transparent -mx-4 -mb-4 p-4 text-white">
            <p className="text-xs font-medium text-white/90"><bdi>فریم نتایج بالینی جوانسازی پوست و پروتکل درمانی</bdi></p>
          </div>
        </div>
              </div>
            </div>
          </div>
        )}


        {/* Tab Panel 1: Live Telemetry & Metrics Analytics */}
        {activeTab === 1 && (
          <div role="tabpanel" className="grid grid-cols-1 sm:grid-cols-3 gap-6 pt-8 animate-fadeIn" data-origin="synthetic_demo">
            <div className="p-6 bg-[#f5f2ed] dark:bg-[#181716] border border-stone-200 dark:border-stone-800 rounded-sm space-y-2">
              <div className="text-xs font-medium text-zinc-500">رضایت مراجعین</div>
              <div className="text-2xl font-bold font-mono text-emerald-600 dark:text-emerald-400">
                <bdi>{"۹۹.۴٪"}</bdi>
              </div>
              <div className="text-xs text-zinc-400">شاخص عملکردی تایید شده حوزه</div>
            </div>

            <div className="p-6 bg-[#f5f2ed] dark:bg-[#181716] border border-stone-200 dark:border-stone-800 rounded-sm space-y-2">
              <div className="text-xs font-medium text-zinc-500">پزشک متخصص بورد</div>
              <div className="text-2xl font-bold font-mono text-sky-600 dark:text-sky-400">
                <bdi>{"۱۲"}</bdi>
              </div>
              <div className="text-xs text-zinc-400">پایش لحظه ای و تضمین سطح خدمت</div>
            </div>

            <div className="p-6 bg-[#f5f2ed] dark:bg-[#181716] border border-stone-200 dark:border-stone-800 rounded-sm space-y-2">
              <div className="text-xs font-medium text-zinc-500">پرونده موفق بالینی</div>
              <div className="text-2xl font-bold font-mono text-indigo-600 dark:text-indigo-400">
                <bdi>{"+۱۸,۰۰۰"}</bdi>
              </div>
              <div className="text-xs text-zinc-400">بهینه سازی مداوم با رصد الگوریتمی رویدادها</div>
            </div>
          </div>
        )}

        {/* Tab Panel 2: Architecture & Domain Blueprint Specification */}
        {activeTab === 2 && (
          <div role="tabpanel" className="pt-8 space-y-6 animate-fadeIn">
            <div className="overflow-x-auto">
              <table className="w-full text-xs text-left rtl:text-right border-collapse">
                <thead>
                  <tr className="border-b border-zinc-200 dark:border-zinc-800 text-zinc-400 font-mono uppercase">
                    <th className="py-2.5 px-3">شاخص معماری</th>
                    <th className="py-2.5 px-3">مقدار پیکربندی شده</th>
                    <th className="py-2.5 px-3">تضمین کیفیت</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-zinc-200/60 dark:divide-zinc-800/60 text-zinc-600 dark:text-zinc-300">
                  <tr>
                    <td className="py-2.5 px-3 font-semibold">حوزه تخصصی محصول</td>
                    <td className="py-2.5 px-3 font-mono">beauty_clinical_wellness</td>
                    <td className="py-2.5 px-3 text-emerald-600 dark:text-emerald-400 font-semibold">MATCH 100%</td>
                  </tr>
                  <tr>
                    <td className="py-2.5 px-3 font-semibold">سبک بصری کانونی</td>
                    <td className="py-2.5 px-3 font-mono">quiet_luxury</td>
                    <td className="py-2.5 px-3 text-sky-600 dark:text-sky-400 font-semibold">COMPILED</td>
                  </tr>
                  <tr>
                    <td className="py-2.5 px-3 font-semibold">استراتژی تم و نور</td>
                    <td className="py-2.5 px-3 font-mono">light</td>
                    <td className="py-2.5 px-3 text-emerald-600 dark:text-emerald-400 font-semibold">BALANCED</td>
                  </tr>
                  <tr>
                    <td className="py-2.5 px-3 font-semibold">جهت رندر و تایپوگرافی</td>
                    <td className="py-2.5 px-3 font-mono">RTL (Persian Isolated)</td>
                    <td className="py-2.5 px-3 text-emerald-600 dark:text-emerald-400 font-semibold">&lt;bdi&gt; SECURED</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ClinicRtl;
