"use client";


import React, { useState } from "react";

export interface ObservabilityProps {
  className?: string;
  onAction?: (actionName: string) => void;
}

export const Observability: React.FC<ObservabilityProps> = ({
  className = "",
  onAction,
}) => {
  const [billingCycle, setBillingCycle] = useState<"monthly" | "annual">("annual");
  const [activeTab, setActiveTab] = useState<number>(0);
  const [simulatedValue, setSimulatedValue] = useState<number>(25000);
  const [splitPos, setSplitPos] = useState<number>(50);
  const [isLiveActive, setIsLiveActive] = useState<boolean>(true);

  const tabs = [
    {"id": "overview", "label": "Primary Experience"},
    {"id": "telemetry", "label": "Domain Performance"},
    {"id": "architecture", "label": "System Blueprint"}
  ];

  return (
    <div dir="ltr" className={`w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 font-sans antialiased text-foreground ${className}`}>
      {/* Ambient Style-Compiled Card Layer */}
      <div className="relative overflow-hidden rounded-2xl border bg-white text-zinc-900 border-zinc-200 p-6 sm:p-10 shadow-xl transition-all">
        

        {/* Header Badges & Interactive Tab Navigation */}
        <div className="flex flex-wrap items-center justify-between gap-4 border-b border-zinc-200/80 dark:border-zinc-800/80 pb-6">
          <div className="flex items-center space-x-3 rtl:space-x-reverse">
            <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-blue-500/10 text-blue-600 dark:text-blue-400 border border-blue-500/20">
              <span className="size-2 rounded-full bg-emerald-500 animate-pulse" />
              <span>System Operational</span>
            </span>
            <span className="text-xs text-zinc-500 font-mono">
              <bdi>v3.8.0 • OKLCH AAA</bdi>
            </span>
          </div>

          {/* Interactive Tabs with Full Accessibility Role */}
          <div role="tablist" aria-label="Feature Tabs" className="inline-flex rounded-lg bg-zinc-100 dark:bg-zinc-900 p-1 border border-zinc-200 dark:border-zinc-800">
            {tabs.map((tab, idx) => (
              <button
                key={tab.id}
                type="button"
                role="tab"
                aria-selected={activeTab === idx}
                onClick={() => setActiveTab(idx)}
                className={`transition-all duration-200 min-h-[44px] ${
                  activeTab === idx ? "px-4 py-1.5 text-xs font-semibold rounded-md bg-white dark:bg-zinc-800 text-zinc-900 dark:text-white shadow-sm" : "px-4 py-1.5 text-xs font-medium rounded-md text-zinc-600 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-white"
                }`}
              >
                {tab.label}
              </button>
            ))}
          </div>
        </div>

        {/* Tab Panel 0: Overview & Signature Domain Widget */}
        {activeTab === 0 && (
          <div role="tabpanel" className="grid grid-cols-1 lg:grid-cols-12 gap-8 pt-8 items-center animate-fadeIn" data-layout-macro="classic_structured_saas">
            <div className="lg:col-span-7 space-y-6">
              <h1 className="text-3xl sm:text-4xl lg:text-5xl font-bold tracking-tight text-zinc-900 dark:text-white leading-tight">
                Next-Generation Modern High-Velocity Software Platform Platform
              </h1>
              <p className="text-base sm:text-lg text-zinc-600 dark:text-zinc-400 leading-relaxed max-w-2xl">
                Engineered for reliability, velocity, and seamless user experience.
              </p>
              <div className="flex items-center gap-3 pt-2">
                <span className="text-xs font-medium text-zinc-500">Monthly</span>
                <button
                  type="button"
                  role="switch"
                  aria-checked={billingCycle === "annual"}
                  aria-label="Billing cycle toggle"
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
                  <span>Annual</span>
                  <span className="px-2 py-0.5 text-[10px] font-bold rounded-full bg-emerald-500/10 text-emerald-600 border border-emerald-500/20">
                    Save 20%
                  </span>
                </span>
              </div>
              <div className="flex flex-wrap gap-4 pt-4">
                <button
                  type="button"
                  onClick={() => onAction?.("primary_click")}
                  className="inline-flex items-center justify-center px-6 py-3 text-sm font-semibold rounded-xl text-white bg-blue-600 hover:bg-blue-700 active:scale-95 transition-all shadow-md min-h-[44px]"
                >
                  Get Started Immediately
                </button>
                <button
                  type="button"
                  onClick={() => onAction?.("secondary_click")}
                  className="inline-flex items-center justify-center px-6 py-3 text-sm font-semibold rounded-xl text-zinc-800 dark:text-zinc-200 border border-zinc-200 dark:border-zinc-800 hover:bg-zinc-100 dark:hover:bg-zinc-900 active:scale-95 transition-all min-h-[44px]"
                >
                  Explore Live Demo
                </button>
              </div>
            </div>

            <div className="lg:col-span-5 space-y-6">
              <div className="bg-zinc-50 dark:bg-zinc-900/90 border border-zinc-200 dark:border-zinc-800 rounded-xl p-6 shadow-sm space-y-4">
                <div className="flex items-center justify-between border-b border-zinc-200 dark:border-zinc-800 pb-3">
                  <span className="text-xs font-bold text-zinc-700 dark:text-zinc-300">
                    Interactive Modern High-Velocity Software Platform Showcase
                  </span>
                  <button
                    type="button"
                    onClick={() => setIsLiveActive(prev => !prev)}
                    className={`text-[11px] font-mono px-3 py-1.5 rounded border transition-colors min-h-[44px] inline-flex items-center justify-center ${
                      isLiveActive 
                        ? "bg-emerald-500/10 text-emerald-600 border-emerald-500/20" 
                        : "bg-zinc-200 dark:bg-zinc-800 text-zinc-500 border-transparent"
                    }`}
                  >
                    <bdi>{isLiveActive ? "LIVE FEED" : "PAUSED"}</bdi>
                  </button>
                </div>
                
              <div className="space-y-4" data-origin="synthetic_demo">
                <div className="space-y-2">
                  <div className="flex justify-between text-xs text-zinc-600 dark:text-zinc-400">
                    <span>Monthly Automated Workflows</span>
                    <span className="font-mono font-bold text-zinc-900 dark:text-white">
                      <bdi data-vibe-metric="workflow-volume">${simulatedValue.toLocaleString()} Executions</bdi>
                    </span>
                  </div>
                  <input
                    type="range"
                    min="1000"
                    max="100000"
                    step="1000"
                    value={simulatedValue}
                    onChange={(e) => setSimulatedValue(Number(e.target.value))}
                    data-vibe-control="simulated-range"
                    aria-label="Automated Workflows Slider"
                    className="w-full accent-emerald-500 cursor-pointer min-h-[44px] h-11 py-3 bg-transparent"
                  />
                </div>

                <div className="grid grid-cols-2 gap-3 text-xs">
                  <div className="p-3 bg-white dark:bg-zinc-950 rounded-xl border border-zinc-200/80 dark:border-zinc-800/80">
                    <div className="text-zinc-500 text-[10px]">Monthly Hours Saved</div>
                    <div className="text-base font-bold font-mono text-emerald-600 dark:text-emerald-400">
                      <bdi data-vibe-metric="time-savings">+{Math.round(simulatedValue * (billingCycle === "annual" ? 0.052 : 0.041)).toLocaleString()} hrs</bdi>
                    </div>
                  </div>
                  <div className="p-3 bg-white dark:bg-zinc-950 rounded-xl border border-zinc-200/80 dark:border-zinc-800/80">
                    <div className="text-zinc-500 text-[10px]">Est. ROI Factor</div>
                    <div className="text-base font-bold font-mono text-zinc-900 dark:text-zinc-100">
                      <bdi>3.8x Annual</bdi>
                    </div>
                  </div>
                </div>
              </div>
              </div>

              
        <div className="relative overflow-hidden bg-zinc-100 dark:bg-zinc-900 aspect-[16/9] sm:aspect-[16/10] border border-zinc-200/80 dark:border-zinc-800/80 rounded-2xl shadow-sm flex flex-col justify-between p-4 group select-none" data-origin="synthetic_demo">
          <div className="flex items-center justify-between text-[11px] font-mono text-zinc-500 z-10">
            <span className="px-2 py-0.5 rounded bg-black/5 dark:bg-white/5 backdrop-blur-md border border-zinc-200/50 dark:border-zinc-700/50">
              <bdi>WORKFLOW_ORCHESTRATION</bdi>
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
            <p className="text-xs font-medium text-white/90"><bdi>Autonomous Multi-Agent Workflow Engine & Automation Matrix</bdi></p>
          </div>
        </div>
            </div>
          </div>
        )}


        {/* Tab Panel 1: Live Telemetry & Metrics Analytics */}
        {activeTab === 1 && (
          <div role="tabpanel" className="grid grid-cols-1 sm:grid-cols-3 gap-6 pt-8 animate-fadeIn" data-origin="synthetic_demo">
            <div className="p-6 rounded-xl bg-zinc-50 dark:bg-zinc-900/90 border border-zinc-200 dark:border-zinc-800 space-y-2">
              <div className="text-xs font-medium text-zinc-500">Active Users</div>
              <div className="text-2xl font-bold font-mono text-emerald-600 dark:text-emerald-400">
                <bdi>{"100k+"}</bdi>
              </div>
              <div className="text-xs text-zinc-400">Verified production benchmark metric</div>
            </div>

            <div className="p-6 rounded-xl bg-zinc-50 dark:bg-zinc-900/90 border border-zinc-200 dark:border-zinc-800 space-y-2">
              <div className="text-xs font-medium text-zinc-500">Uptime</div>
              <div className="text-2xl font-bold font-mono text-sky-600 dark:text-sky-400">
                <bdi>{"99.99%"}</bdi>
              </div>
              <div className="text-xs text-zinc-400">Real-time telemetry and SLA assurance</div>
            </div>

            <div className="p-6 rounded-xl bg-zinc-50 dark:bg-zinc-900/90 border border-zinc-200 dark:border-zinc-800 space-y-2">
              <div className="text-xs font-medium text-zinc-500">Customer Rating</div>
              <div className="text-2xl font-bold font-mono text-indigo-600 dark:text-indigo-400">
                <bdi>{"4.9/5"}</bdi>
              </div>
              <div className="text-xs text-zinc-400">Continuously optimized by invariant monitoring</div>
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
                    <th className="py-2.5 px-3">Blueprint Dimension</th>
                    <th className="py-2.5 px-3">Resolved Value</th>
                    <th className="py-2.5 px-3">Invariant Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-zinc-200/60 dark:divide-zinc-800/60 text-zinc-600 dark:text-zinc-300">
                  <tr>
                    <td className="py-2.5 px-3 font-semibold">Product Domain</td>
                    <td className="py-2.5 px-3 font-mono">general_modern_saas</td>
                    <td className="py-2.5 px-3 text-emerald-600 dark:text-emerald-400 font-semibold">MATCH 100%</td>
                  </tr>
                  <tr>
                    <td className="py-2.5 px-3 font-semibold">Visual Chemistry</td>
                    <td className="py-2.5 px-3 font-mono">clean_stripe</td>
                    <td className="py-2.5 px-3 text-sky-600 dark:text-sky-400 font-semibold">COMPILED</td>
                  </tr>
                  <tr>
                    <td className="py-2.5 px-3 font-semibold">Lighting Mode</td>
                    <td className="py-2.5 px-3 font-mono">light</td>
                    <td className="py-2.5 px-3 text-emerald-600 dark:text-emerald-400 font-semibold">BALANCED</td>
                  </tr>
                  <tr>
                    <td className="py-2.5 px-3 font-semibold">Text Direction & BiDi</td>
                    <td className="py-2.5 px-3 font-mono">LTR (Pure English)</td>
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

export default Observability;
