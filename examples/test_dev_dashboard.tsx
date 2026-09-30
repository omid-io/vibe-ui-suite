"use client";


import React, { useState } from "react";

export interface VibeMasterpieceProps {
  className?: string;
  onAction?: (actionName: string) => void;
}

export const VibeMasterpiece: React.FC<VibeMasterpieceProps> = ({
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
      <div className="relative bg-black border border-emerald-900/60 p-4 sm:p-8 font-mono shadow-none text-emerald-400 transition-all">
        

        {/* Header Badges & Interactive Tab Navigation */}
        <div className="flex flex-wrap items-center justify-between gap-4 border-b border-zinc-200/80 dark:border-zinc-800/80 pb-6">
          <div className="flex items-center space-x-3 rtl:space-x-reverse">
            <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 font-mono text-[11px] font-bold uppercase bg-emerald-950/80 text-emerald-400 border border-emerald-500/40">
              <span className="size-2 rounded-full bg-emerald-500 animate-pulse" />
              <span>System Operational</span>
            </span>
            <span className="text-[11px] font-mono text-emerald-600">
              <bdi>v3.8.0 • OKLCH AAA</bdi>
            </span>
          </div>

          {/* Interactive Tabs with Full Accessibility Role */}
          <div role="tablist" aria-label="Feature Tabs" className="inline-flex border border-emerald-900/80 bg-zinc-950 p-1 font-mono text-xs">
            {tabs.map((tab, idx) => (
              <button
                key={tab.id}
                type="button"
                role="tab"
                aria-selected={activeTab === idx}
                onClick={() => setActiveTab(idx)}
                className={`transition-all duration-200 min-h-[44px] ${
                  activeTab === idx ? "bg-emerald-950 text-emerald-300 font-mono border border-emerald-500 px-3 py-2 min-h-[44px] inline-flex items-center" : "text-emerald-700 hover:text-emerald-400 font-mono px-3 py-2 min-h-[44px] inline-flex items-center"
                }`}
              >
                {tab.label}
              </button>
            ))}
          </div>
        </div>

        {/* Tab Panel 0: Overview & Signature Domain Widget */}
        {activeTab === 0 && (
          <div role="tabpanel" className="space-y-6 pt-6 animate-fadeIn" data-layout-macro="dense_telemetry_hud">
            {/* Command Status Ribbon */}
            <div className="flex flex-wrap items-center justify-between gap-3 px-4 py-2.5 bg-zinc-900/90 dark:bg-black border border-zinc-800 rounded-xl font-mono text-xs">
              <div className="flex items-center gap-2">
                <span className="size-2 rounded-full bg-emerald-400 animate-ping" />
                <span className="text-emerald-400 font-bold">NODE://SYS.ONLINE</span>
                <span className="text-zinc-600">|</span>
                <span className="text-zinc-400">LATENCY: &lt;1.2ms</span>
              </div>
              <div className="flex items-center gap-3">
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
              </div>
            </div>

            {/* Split Cockpit Grid: 8 Cols Telemetry Console + 4 Cols HUD Sidebar */}
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
              <div className="lg:col-span-8 space-y-6">
                <div className="space-y-4">
                  <h1 className="text-2xl sm:text-3xl lg:text-4xl font-mono font-bold tracking-tight text-emerald-400 uppercase leading-snug">
                    Zero-Config Kubernetes Ingress & Edge Orchestration
                  </h1>
                  <p className="text-sm sm:text-base font-mono text-emerald-500/80 leading-relaxed max-w-2xl">
                    Deploy global container clusters in seconds with automatic TLS, wireguard mesh, and sub-10ms P99 latency.
                  </p>
                </div>

                <div className="bg-zinc-950 border border-emerald-900/80 p-5 space-y-4 font-mono">
                  <div className="flex items-center justify-between border-b border-zinc-800 pb-3">
                    <span className="text-xs font-mono font-bold text-zinc-300">
                      // Live Kubectl Pod Terminal & Log Streamer
                    </span>
                    <button
                      type="button"
                      onClick={() => setIsLiveActive(prev => !prev)}
                      className="text-[11px] font-mono px-3 py-1.5 rounded border border-emerald-500/30 text-emerald-400 bg-emerald-950/40 min-h-[44px] inline-flex items-center"
                    >
                      <bdi>{isLiveActive ? "LIVE_TELEMETRY: ACTIVE" : "PAUSED"}</bdi>
                    </button>
                  </div>
                  
              <div className="space-y-4" data-origin="synthetic_demo">
                <div className="space-y-2">
                  <div className="flex justify-between text-xs text-zinc-600 dark:text-zinc-400">
                    <span>Dynamic Node Cluster Capacity</span>
                    <span className="font-mono font-bold text-sky-500">
                      <bdi data-vibe-metric="node-count">{ Math.round(4 + (simulatedValue / 5000)) } Nodes (c6i.4xlarge)</bdi>
                    </span>
                  </div>
                  <input
                    type="range"
                    min="5000"
                    max="100000"
                    step="5000"
                    value={simulatedValue}
                    onChange={(e) => setSimulatedValue(Number(e.target.value))}
                    data-vibe-control="simulated-range"
                    aria-label="Node Cluster Scale Slider"
                    className="w-full accent-sky-500 cursor-pointer min-h-[44px] h-11 py-3 bg-transparent"
                  />
                </div>

                <div className="grid grid-cols-2 gap-3 text-xs font-mono">
                  <div className="p-3 bg-zinc-950 rounded-xl border border-zinc-800">
                    <div className="text-zinc-500 text-[10px]">P99 Edge Latency</div>
                    <div className="text-base font-bold text-emerald-400">
                      <bdi data-vibe-metric="cluster-latency">{ Math.max(12, Math.round(48 - (simulatedValue / 2500))) } ms</bdi>
                    </div>
                  </div>
                  <div className="p-3 bg-zinc-950 rounded-xl border border-zinc-800">
                    <div className="text-zinc-500 text-[10px]">Peak Throughput</div>
                    <div className="text-base font-bold text-sky-400">
                      <bdi data-vibe-metric="network-throughput">{ (simulatedValue * 1.8).toLocaleString() } req/s</bdi>
                    </div>
                  </div>
                </div>
              </div>
                </div>

                <div className="flex flex-wrap gap-4 pt-4">
                <button
                  type="button"
                  onClick={() => onAction?.("primary_click")}
                  className="inline-flex items-center justify-center px-5 py-2.5 font-mono text-xs uppercase bg-emerald-500 text-black font-bold border border-emerald-400 hover:bg-emerald-400 active:bg-emerald-600 transition-none min-h-[44px]"
                >
                  Deploy In 30 Seconds
                </button>
                <button
                  type="button"
                  onClick={() => onAction?.("secondary_click")}
                  className="inline-flex items-center justify-center px-5 py-2.5 font-mono text-xs uppercase text-emerald-400 border border-emerald-800 hover:border-emerald-500 transition-none min-h-[44px]"
                >
                  Read Architecture RFC
                </button>
              </div>
              </div>

              <div className="lg:col-span-4 space-y-6">
                
        <div className="relative overflow-hidden bg-zinc-100 dark:bg-zinc-900 aspect-[16/10] sm:aspect-[16/9] border border-emerald-500/40 font-mono rounded-none flex flex-col justify-between p-4 group select-none" data-origin="synthetic_demo">
          <div className="flex items-center justify-between text-[11px] font-mono text-zinc-500 z-10">
            <span className="px-2 py-0.5 rounded bg-black/5 dark:bg-white/5 backdrop-blur-md border border-zinc-200/50 dark:border-zinc-700/50">
              <bdi>CLUSTER_TOPOLOGY</bdi>
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
            <p className="text-xs font-medium text-white/90"><bdi>Multi-Region Kubernetes Pod Topology & Egress Flow</bdi></p>
          </div>
        </div>
              </div>
            </div>
          </div>
        )}


        {/* Tab Panel 1: Live Telemetry & Metrics Analytics */}
        {activeTab === 1 && (
          <div role="tabpanel" className="grid grid-cols-1 sm:grid-cols-3 gap-6 pt-8 animate-fadeIn" data-origin="synthetic_demo">
            <div className="p-5 bg-zinc-950 border border-emerald-900/80 space-y-2 font-mono">
              <div className="text-xs font-medium text-zinc-500">P99 Edge Latency</div>
              <div className="text-2xl font-bold font-mono text-emerald-600 dark:text-emerald-400">
                <bdi>{"8.4ms"}</bdi>
              </div>
              <div className="text-xs text-zinc-400">Verified production benchmark metric</div>
            </div>

            <div className="p-5 bg-zinc-950 border border-emerald-900/80 space-y-2 font-mono">
              <div className="text-xs font-medium text-zinc-500">Global PoPs</div>
              <div className="text-2xl font-bold font-mono text-sky-600 dark:text-sky-400">
                <bdi>{"120+"}</bdi>
              </div>
              <div className="text-xs text-zinc-400">Real-time telemetry and SLA assurance</div>
            </div>

            <div className="p-5 bg-zinc-950 border border-emerald-900/80 space-y-2 font-mono">
              <div className="text-xs font-medium text-zinc-500">SLA Uptime</div>
              <div className="text-2xl font-bold font-mono text-indigo-600 dark:text-indigo-400">
                <bdi>{"99.999%"}</bdi>
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
                    <td className="py-2.5 px-3 font-mono">devops_cloud_terminal</td>
                    <td className="py-2.5 px-3 text-emerald-600 dark:text-emerald-400 font-semibold">MATCH 100%</td>
                  </tr>
                  <tr>
                    <td className="py-2.5 px-3 font-semibold">Visual Chemistry</td>
                    <td className="py-2.5 px-3 font-mono">data_dense_terminal</td>
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

export default VibeMasterpiece;
