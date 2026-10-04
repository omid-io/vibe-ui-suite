"""
vibe_core.generator — Autonomous Component & Interface Generator (v3.8.0)
Generates production-grade, responsive, accessible React 19 TSX components
and self-contained HTML interfaces from DesignDecisionContract.
Features:
- Render-Affecting Style Compiler (Neobrutalism, Swiss Editorial, Quiet Luxury, Terminal HUD, Linear Dark, Specular Glass, Clean Stripe)
- 24 Distinct Domain Signature Interactive Widgets
- Functional Living React 19 State (useState, conditional tabs, sliders, toggles)
- Explicit Synthetic Data Demarcation (data-origin="synthetic_demo")
- Full WCAG AAA / AA Contrast & Semantic RTL BiDi Isolation (<bdi>)
"""

from typing import Dict, Any, Optional
from pathlib import Path
import json
from vibe_core.genome import DesignGenomeEngine
from vibe_core.asset_director import AssetDirector
from vibe_core.domain_widgets import render_domain_widget

# 6 Distinct Macro Layout Archetypes mapped to all 24 Canonical Domains (v3.9.0)
DOMAIN_MACRO_ARCHETYPES: Dict[str, str] = {
    # 1. dense_telemetry_hud
    "devops_cloud_terminal": "dense_telemetry_hud",
    "crypto_trading_web3": "dense_telemetry_hud",
    "cybersecurity_identity_auth": "dense_telemetry_hud",
    "logistics_supply_chain": "dense_telemetry_hud",

    # 2. editorial_asymmetric_spread
    "media_editorial_magazine": "editorial_asymmetric_spread",
    "ecommerce_luxury_fashion": "editorial_asymmetric_spread",
    "real_estate_architecture": "editorial_asymmetric_spread",

    # 3. conversion_stepper_funnel
    "fintech_banking": "conversion_stepper_funnel",
    "travel_hospitality_tourism": "conversion_stepper_funnel",
    "healthcare_hospital_medical": "conversion_stepper_funnel",
    "ecommerce_mass_market": "conversion_stepper_funnel",
    "food_restaurant_cafe": "conversion_stepper_funnel",

    # 4. creative_canvas_showcase
    "creative_portfolio_agency": "creative_canvas_showcase",
    "personal_branding_creator": "creative_canvas_showcase",
    "gaming_entertainment_streaming": "creative_canvas_showcase",
    "automotive_ev_mobility": "creative_canvas_showcase",

    # 5. split_laboratory_studio
    "ai_developer_platform": "split_laboratory_studio",
    "energy_greentech_sustainability": "split_laboratory_studio",
    "beauty_clinical_wellness": "split_laboratory_studio",

    # 6. classic_structured_saas
    "saas_b2b_enterprise": "classic_structured_saas",
    "education_edtech_lms": "classic_structured_saas",
    "legal_compliance_law": "classic_structured_saas",
    "nonprofit_charity_social": "classic_structured_saas",
    "general_modern_saas": "classic_structured_saas",
}

class InterfaceGenerator:

    def __init__(self):
        self.genome_engine = DesignGenomeEngine()
        self.asset_director = AssetDirector()
        self.blueprints = self._load_blueprints()

    def _load_blueprints(self) -> Dict[str, Any]:
        bp_path = Path(__file__).resolve().parent.parent / "data" / "domain_blueprints.json"
        if not bp_path.exists():
            return {}
        try:
            with open(bp_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}

    def _compile_style(self, selected_style: str, theme_strategy: str = "light") -> Dict[str, str]:
        """
        Compiles visual chemistry style into concrete, render-affecting Tailwind classes.
        Guarantees that Neobrutalism, Swiss Editorial, Luxury, Terminal, etc.
        completely reshape the container geometry, borders, typography, and CTA morphology.
        """
        is_dark = theme_strategy == "dark" or selected_style in ["linear_dark", "data_dense_terminal", "cyberpunk", "midnight_executive"]

        if selected_style == "neobrutalism":
            return {
                "container": "relative bg-[#fffdf0] dark:bg-[#1a1708] border-4 border-black dark:border-amber-400 p-6 sm:p-10 shadow-[8px_8px_0px_0px_#000] dark:shadow-[8px_8px_0px_0px_#fbbf24] transition-all",
                "border_beam": "",
                "header_badge": "inline-flex items-center gap-1.5 px-3 py-1 font-mono text-xs font-black uppercase bg-yellow-300 text-black border-2 border-black shadow-[2px_2px_0px_0px_#000]",
                "version_tag": "text-xs font-mono font-bold text-black dark:text-amber-300",
                "tab_container": "inline-flex border-2 border-black dark:border-amber-400 bg-white dark:bg-black p-1 shadow-[3px_3px_0px_0px_#000]",
                "tab_btn_active": "bg-yellow-300 text-black font-mono font-black uppercase border border-black shadow-[2px_2px_0px_0px_#000]",
                "tab_btn_inactive": "text-black dark:text-zinc-300 font-mono font-bold uppercase hover:bg-zinc-100 dark:hover:bg-zinc-900",
                "headline": "text-3xl sm:text-4xl lg:text-5xl font-mono font-black uppercase tracking-tight text-black dark:text-amber-300 leading-tight",
                "body_text": "text-base sm:text-lg font-mono text-zinc-800 dark:text-zinc-200 leading-relaxed max-w-2xl",
                "primary_cta": "inline-flex items-center justify-center px-6 py-3 font-mono font-black uppercase text-sm bg-yellow-400 text-black border-2 border-black shadow-[4px_4px_0px_0px_#000] hover:translate-x-[2px] hover:translate-y-[2px] hover:shadow-[2px_2px_0px_0px_#000] active:translate-x-[4px] active:translate-y-[4px] active:shadow-none transition-all min-h-[44px]",
                "secondary_cta": "inline-flex items-center justify-center px-6 py-3 font-mono font-bold uppercase text-sm bg-white dark:bg-zinc-900 text-black dark:text-white border-2 border-black dark:border-white shadow-[3px_3px_0px_0px_#000] hover:bg-zinc-100 transition-all min-h-[44px]",
                "widget_card": "bg-white dark:bg-zinc-900 border-2 border-black dark:border-amber-400 shadow-[4px_4px_0px_0px_#000] p-6 space-y-4",
                "telemetry_card": "p-6 bg-white dark:bg-zinc-900 border-2 border-black dark:border-amber-400 shadow-[4px_4px_0px_0px_#000] space-y-2",
                "switch_bg": "bg-black dark:bg-amber-400",
                "switch_dot": "bg-yellow-300 dark:bg-black",
                "style_badge": "border-black bg-yellow-300 text-black font-mono font-bold"
            }
        elif selected_style == "minimal_swiss":
            return {
                "container": "relative bg-white dark:bg-zinc-950 border border-zinc-900 dark:border-zinc-100 p-6 sm:p-10 shadow-none transition-all",
                "border_beam": "",
                "header_badge": "inline-flex items-center gap-1.5 px-3 py-1 text-xs font-bold uppercase tracking-widest bg-zinc-900 text-white dark:bg-white dark:text-zinc-900",
                "version_tag": "text-xs font-mono text-zinc-500",
                "tab_container": "inline-flex border-b border-zinc-900 dark:border-zinc-100 gap-2 pb-0",
                "tab_btn_active": "border-b-2 border-black dark:border-white text-black dark:text-white font-bold tracking-tight pb-2",
                "tab_btn_inactive": "text-zinc-400 hover:text-black dark:hover:text-white font-medium pb-2",
                "headline": "text-3xl sm:text-4xl lg:text-5xl font-sans font-extrabold tracking-tighter text-zinc-900 dark:text-zinc-50 leading-[1.1]",
                "body_text": "text-base sm:text-lg font-sans text-zinc-600 dark:text-zinc-300 leading-relaxed max-w-2xl",
                "primary_cta": "inline-flex items-center justify-center px-6 py-3 font-sans font-bold text-sm bg-black text-white dark:bg-white dark:text-black border border-black dark:border-white hover:bg-zinc-800 dark:hover:bg-zinc-200 transition-colors tracking-tight min-h-[44px]",
                "secondary_cta": "inline-flex items-center justify-center px-6 py-3 font-sans font-medium text-sm text-zinc-900 dark:text-zinc-100 border border-zinc-400 dark:border-zinc-600 hover:border-black transition-colors min-h-[44px]",
                "widget_card": "bg-zinc-50 dark:bg-zinc-900 border border-zinc-300 dark:border-zinc-700 p-6 space-y-4",
                "telemetry_card": "p-6 bg-zinc-50 dark:bg-zinc-900 border border-zinc-300 dark:border-zinc-700 space-y-2",
                "switch_bg": "bg-zinc-900 dark:bg-zinc-100",
                "switch_dot": "bg-white dark:bg-zinc-900",
                "style_badge": "border-zinc-900 bg-zinc-900 text-white font-sans"
            }
        elif selected_style == "quiet_luxury":
            return {
                "container": "relative bg-[#faf8f5] dark:bg-[#121110] border border-stone-200 dark:border-stone-800 rounded-sm p-6 sm:p-12 shadow-sm transition-all",
                "border_beam": "",
                "header_badge": "inline-flex items-center gap-1.5 px-3 py-1 font-serif text-xs italic tracking-widest text-stone-800 dark:text-stone-200 border border-stone-300 dark:border-stone-700",
                "version_tag": "text-xs font-serif text-stone-500",
                "tab_container": "inline-flex border-b border-stone-200 dark:border-stone-800 gap-6 pb-2",
                "tab_btn_active": "text-stone-900 dark:text-stone-100 font-serif italic border-b border-stone-900 dark:border-stone-100 pb-2",
                "tab_btn_inactive": "text-stone-400 hover:text-stone-700 dark:hover:text-stone-300 font-serif pb-2",
                "headline": "text-3xl sm:text-4xl lg:text-5xl font-serif font-normal italic tracking-wide text-stone-900 dark:text-stone-100 leading-tight",
                "body_text": "text-base sm:text-lg font-sans text-stone-600 dark:text-stone-400 leading-relaxed max-w-2xl font-light",
                "primary_cta": "inline-flex items-center justify-center px-8 py-3 font-serif tracking-widest text-xs uppercase bg-stone-900 text-stone-50 dark:bg-stone-100 dark:text-stone-900 border border-stone-800 hover:bg-stone-800 dark:hover:bg-stone-200 transition-all min-h-[44px]",
                "secondary_cta": "inline-flex items-center justify-center px-8 py-3 font-serif tracking-widest text-xs uppercase text-stone-800 dark:text-stone-200 border border-stone-300 dark:border-stone-700 hover:border-stone-900 transition-all min-h-[44px]",
                "widget_card": "bg-[#f5f2ed] dark:bg-[#181716] border border-stone-200 dark:border-stone-800 rounded-sm p-6 space-y-4",
                "telemetry_card": "p-6 bg-[#f5f2ed] dark:bg-[#181716] border border-stone-200 dark:border-stone-800 rounded-sm space-y-2",
                "switch_bg": "bg-stone-800 dark:bg-stone-200",
                "switch_dot": "bg-[#faf8f5] dark:bg-[#121110]",
                "style_badge": "border-stone-400 bg-stone-100 text-stone-800 font-serif"
            }
        elif selected_style == "data_dense_terminal":
            return {
                "container": "relative bg-black border border-emerald-900/60 p-4 sm:p-8 font-mono shadow-none text-emerald-400 transition-all",
                "border_beam": "",
                "header_badge": "inline-flex items-center gap-1.5 px-2.5 py-0.5 font-mono text-[11px] font-bold uppercase bg-emerald-950/80 text-emerald-400 border border-emerald-500/40",
                "version_tag": "text-[11px] font-mono text-emerald-600",
                "tab_container": "inline-flex border border-emerald-900/80 bg-zinc-950 p-1 font-mono text-xs",
                "tab_btn_active": "bg-emerald-950 text-emerald-300 font-mono border border-emerald-500 px-3 py-2 min-h-[44px] inline-flex items-center",
                "tab_btn_inactive": "text-emerald-700 hover:text-emerald-400 font-mono px-3 py-2 min-h-[44px] inline-flex items-center",
                "headline": "text-2xl sm:text-3xl lg:text-4xl font-mono font-bold tracking-tight text-emerald-400 uppercase leading-snug",
                "body_text": "text-sm sm:text-base font-mono text-emerald-500/80 leading-relaxed max-w-2xl",
                "primary_cta": "inline-flex items-center justify-center px-5 py-2.5 font-mono text-xs uppercase bg-emerald-500 text-black font-bold border border-emerald-400 hover:bg-emerald-400 active:bg-emerald-600 transition-none min-h-[44px]",
                "secondary_cta": "inline-flex items-center justify-center px-5 py-2.5 font-mono text-xs uppercase text-emerald-400 border border-emerald-800 hover:border-emerald-500 transition-none min-h-[44px]",
                "widget_card": "bg-zinc-950 border border-emerald-900/80 p-5 space-y-4 font-mono",
                "telemetry_card": "p-5 bg-zinc-950 border border-emerald-900/80 space-y-2 font-mono",
                "switch_bg": "bg-emerald-950 border border-emerald-600",
                "switch_dot": "bg-emerald-400",
                "style_badge": "border-emerald-600 bg-emerald-950 text-emerald-300 font-mono"
            }
        elif selected_style == "specular_glass":
            return {
                "container": "relative overflow-hidden rounded-3xl border border-white/40 dark:border-white/10 bg-white/70 dark:bg-zinc-950/70 backdrop-blur-2xl p-6 sm:p-10 shadow-2xl transition-all",
                "border_beam": '<div aria-hidden="true" className="pointer-events-none absolute -inset-px rounded-3xl opacity-40 transition-opacity duration-500 bg-gradient-to-r from-teal-500/20 via-sky-500/20 to-emerald-500/20" />',
                "header_badge": "inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border border-emerald-500/20 backdrop-blur-md",
                "version_tag": "text-xs text-zinc-500 font-mono",
                "tab_container": "inline-flex rounded-full bg-zinc-100/80 dark:bg-zinc-900/80 backdrop-blur-md p-1 border border-zinc-200/60 dark:border-zinc-800/60",
                "tab_btn_active": "px-4 py-1.5 text-xs font-semibold rounded-full bg-white dark:bg-zinc-800 text-zinc-900 dark:text-white shadow-sm",
                "tab_btn_inactive": "px-4 py-1.5 text-xs font-medium rounded-full text-zinc-600 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-white",
                "headline": "text-3xl sm:text-4xl lg:text-5xl font-extrabold tracking-tight text-zinc-900 dark:text-white leading-[1.15]",
                "body_text": "text-base sm:text-lg text-zinc-600 dark:text-zinc-400 leading-relaxed max-w-2xl",
                "primary_cta": "inline-flex items-center justify-center px-6 py-3 text-sm font-semibold rounded-full text-white bg-gradient-to-r from-sky-500 to-indigo-600 hover:opacity-90 active:scale-95 transition-all shadow-lg min-h-[44px]",
                "secondary_cta": "inline-flex items-center justify-center px-6 py-3 text-sm font-semibold rounded-full text-zinc-800 dark:text-zinc-200 border border-zinc-200 dark:border-zinc-800 hover:bg-zinc-100/60 backdrop-blur-md min-h-[44px]",
                "widget_card": "bg-zinc-50/80 dark:bg-zinc-900/80 backdrop-blur-md border border-zinc-200/80 dark:border-zinc-800/80 rounded-2xl p-6 shadow-inner space-y-4",
                "telemetry_card": "p-6 rounded-2xl bg-zinc-50/80 dark:bg-zinc-900/80 backdrop-blur-md border border-zinc-200 dark:border-zinc-800 space-y-2",
                "switch_bg": "bg-zinc-300 dark:bg-zinc-700",
                "switch_dot": "bg-white shadow-lg",
                "style_badge": "border-sky-500/20 bg-sky-500/10 text-sky-600"
            }
        elif selected_style in ["apple_cupertino", "cupertino_fluid", "apple_design"]:
            return {
                "container": "relative overflow-hidden rounded-[28px] border border-black/5 dark:border-white/10 bg-white/75 dark:bg-zinc-900/75 backdrop-blur-2xl p-6 sm:p-10 shadow-[0_20px_50px_rgba(0,0,0,0.08)] dark:shadow-[0_20px_50px_rgba(0,0,0,0.4)] transition-all",
                "border_beam": '<div aria-hidden="true" className="pointer-events-none absolute inset-x-0 top-0 h-px bg-gradient-to-r from-transparent via-white/25 to-transparent z-10" />',
                "header_badge": "inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-blue-500/10 text-blue-600 dark:text-blue-400 border border-blue-500/20 backdrop-blur-md",
                "version_tag": "text-xs text-zinc-500 font-mono tracking-tight",
                "tab_container": "inline-flex rounded-full bg-zinc-200/60 dark:bg-zinc-800/60 backdrop-blur-md p-1 border border-black/5 dark:border-white/5",
                "tab_btn_active": "px-4 py-1.5 text-xs font-semibold rounded-full bg-white dark:bg-zinc-700 text-zinc-900 dark:text-white shadow-sm transition-all",
                "tab_btn_inactive": "px-4 py-1.5 text-xs font-medium rounded-full text-zinc-600 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-white transition-all",
                "headline": "text-3xl sm:text-4xl lg:text-5xl font-sans font-bold tracking-[-0.025em] text-zinc-900 dark:text-white leading-[1.08]",
                "body_text": "text-base sm:text-lg text-zinc-600 dark:text-zinc-300 leading-relaxed max-w-2xl font-normal",
                "primary_cta": "inline-flex items-center justify-center px-6 py-3 text-sm font-semibold rounded-full text-white bg-[#0071e3] hover:bg-[#0077ed] active:scale-[0.98] transition-all shadow-md min-h-[44px]",
                "secondary_cta": "inline-flex items-center justify-center px-6 py-3 text-sm font-semibold rounded-full text-zinc-800 dark:text-zinc-200 border border-black/10 dark:border-white/10 hover:bg-black/5 dark:hover:bg-white/5 active:scale-[0.98] backdrop-blur-md transition-all min-h-[44px]",
                "widget_card": "bg-white/60 dark:bg-zinc-800/60 backdrop-blur-xl border border-black/5 dark:border-white/10 rounded-[22px] p-6 shadow-sm space-y-4",
                "telemetry_card": "p-6 rounded-[22px] bg-white/60 dark:bg-zinc-800/60 backdrop-blur-xl border border-black/5 dark:border-white/10 space-y-2",
                "switch_bg": "bg-zinc-300 dark:bg-zinc-700",
                "switch_dot": "bg-white shadow-md",
                "style_badge": "border-blue-500/20 bg-blue-500/10 text-[#0071e3]"
            }
        else: # Default Clean Corporate SaaS (clean_stripe / linear_dark fallback)
            bg_card = "bg-zinc-950 text-zinc-100 border-zinc-800" if is_dark else "bg-white text-zinc-900 border-zinc-200"
            return {
                "container": f"relative overflow-hidden rounded-2xl border {bg_card} p-6 sm:p-10 shadow-xl transition-all",
                "border_beam": '<div aria-hidden="true" className="pointer-events-none absolute inset-x-0 top-0 h-px bg-gradient-to-r from-transparent via-white/20 to-transparent z-10" />',
                "header_badge": "inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-blue-500/10 text-blue-600 dark:text-blue-400 border border-blue-500/20",
                "version_tag": "text-xs text-zinc-500 font-mono",
                "tab_container": "inline-flex rounded-lg bg-zinc-100 dark:bg-zinc-900 p-1 border border-zinc-200 dark:border-zinc-800",
                "tab_btn_active": "px-4 py-1.5 text-xs font-semibold rounded-md bg-white dark:bg-zinc-800 text-zinc-900 dark:text-white shadow-sm",
                "tab_btn_inactive": "px-4 py-1.5 text-xs font-medium rounded-md text-zinc-600 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-white",
                "headline": "text-3xl sm:text-4xl lg:text-5xl font-bold tracking-tight text-zinc-900 dark:text-white leading-tight",
                "body_text": "text-base sm:text-lg text-zinc-600 dark:text-zinc-400 leading-relaxed max-w-2xl",
                "primary_cta": "inline-flex items-center justify-center px-6 py-3 text-sm font-semibold rounded-xl text-white bg-blue-600 hover:bg-blue-700 active:scale-95 transition-all shadow-md min-h-[44px]",
                "secondary_cta": "inline-flex items-center justify-center px-6 py-3 text-sm font-semibold rounded-xl text-zinc-800 dark:text-zinc-200 border border-zinc-200 dark:border-zinc-800 hover:bg-zinc-100 dark:hover:bg-zinc-900 active:scale-95 transition-all min-h-[44px]",
                "widget_card": "bg-zinc-50 dark:bg-zinc-900/90 border border-zinc-200 dark:border-zinc-800 rounded-xl p-6 shadow-sm space-y-4",
                "telemetry_card": "p-6 rounded-xl bg-zinc-50 dark:bg-zinc-900/90 border border-zinc-200 dark:border-zinc-800 space-y-2",
                "switch_bg": "bg-zinc-300 dark:bg-zinc-700",
                "switch_dot": "bg-white shadow-md",
                "style_badge": "border-blue-500/20 bg-blue-500/10 text-blue-600"
            }

    def _render_domain_widget(self, domain_id: str, is_rtl: bool, style_cfg: Dict[str, str], blueprint: Dict[str, Any]) -> str:
        """
        Renders rich, functional signature widget JSX tailored to the exact domain via canonical registry.
        Features real causal reactive calculations connecting simulatedValue and splitPos to business metrics.
        Guarantees zero generic fallbacks across all 24 canonical domains.
        """
        return render_domain_widget(domain_id, is_rtl, style_cfg, blueprint)

    def _render_macro_panel(
        self,
        domain_id: str,
        is_rtl: bool,
        style_cfg: Dict[str, str],
        headline: str,
        subheadline: str,
        cta_primary: str,
        cta_secondary: str,
        sig_widget_name: str,
        domain_widget_code: str,
        media_container_code: str
    ) -> str:
        """
        Renders one of 6 distinct macro layout compositions based on domain archetype:
        1. dense_telemetry_hud (DevOps, Crypto, Cybersecurity, Logistics)
        2. editorial_asymmetric_spread (Media, Luxury Fashion, Architecture)
        3. conversion_stepper_funnel (Fintech, Travel, Healthcare, Mass Market, Food)
        4. creative_canvas_showcase (Creative Agency, Creator Brand, Gaming, Auto)
        5. split_laboratory_studio (AI Dev, Greentech, Clinical Wellness)
        6. classic_structured_saas (SaaS Enterprise, EdTech, Legal, NonProfit, General SaaS)
        """
        archetype = DOMAIN_MACRO_ARCHETYPES.get(domain_id, "classic_structured_saas")

        billing_switch = f'''<div className="flex items-center gap-3 pt-2">
                <span className="text-xs font-medium text-zinc-500">{"ماهانه" if is_rtl else "Monthly"}</span>
                <button
                  type="button"
                  role="switch"
                  aria-checked={{billingCycle === "annual"}}
                  aria-label="{"تغییر دوره پرداخت" if is_rtl else "Billing cycle toggle"}"
                  onClick={{() => setBillingCycle(prev => prev === "annual" ? "monthly" : "annual")}}
                  className="relative inline-flex min-h-[44px] min-w-[48px] items-center justify-center p-2 rounded-full cursor-pointer focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:ring-offset-2"
                >
                  <span className="relative inline-flex h-6 w-11 shrink-0 rounded-full border-2 border-transparent bg-zinc-300 dark:bg-zinc-700 transition-colors duration-200 ease-in-out">
                    <span
                      aria-hidden="true"
                      className={{`pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow-lg ring-0 transition duration-200 ease-in-out ${{
                        billingCycle === "annual" ? "translate-x-5 rtl:-translate-x-5" : "translate-x-0"
                      }}`}}
                    />
                  </span>
                </button>
                <span className="text-xs font-medium text-zinc-900 dark:text-white flex items-center gap-1.5">
                  <span>{"سالانه" if is_rtl else "Annual"}</span>
                  <span className="px-2 py-0.5 text-[10px] font-bold rounded-full bg-emerald-500/10 text-emerald-600 border border-emerald-500/20">
                    {"۲۰٪ تخفیف ویژه" if is_rtl else "Save 20%"}
                  </span>
                </span>
              </div>'''

        cta_group = f'''<div className="flex flex-wrap gap-4 pt-4">
                <button
                  type="button"
                  onClick={{() => onAction?.("primary_click")}}
                  className="{style_cfg['primary_cta']}"
                >
                  {cta_primary}
                </button>
                <button
                  type="button"
                  onClick={{() => onAction?.("secondary_click")}}
                  className="{style_cfg['secondary_cta']}"
                >
                  {cta_secondary}
                </button>
              </div>'''

        if archetype == "dense_telemetry_hud":
            return f'''<div role="tabpanel" className="space-y-6 pt-6 animate-fadeIn" data-layout-macro="dense_telemetry_hud">
            {{/* Command Status Ribbon */}}
            <div className="flex flex-wrap items-center justify-between gap-3 px-4 py-2.5 bg-zinc-900/90 dark:bg-black border border-zinc-800 rounded-xl font-mono text-xs">
              <div className="flex items-center gap-2">
                <span className="size-2 rounded-full bg-emerald-400 animate-ping" />
                <span className="text-emerald-400 font-bold">NODE://SYS.ONLINE</span>
                <span className="text-zinc-600">|</span>
                <span className="text-zinc-400">LATENCY: &lt;1.2ms</span>
              </div>
              <div className="flex items-center gap-3">
                {billing_switch}
              </div>
            </div>

            {{/* Split Cockpit Grid: 8 Cols Telemetry Console + 4 Cols HUD Sidebar */}}
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
              <div className="lg:col-span-8 space-y-6">
                <div className="space-y-4">
                  <h1 className="{style_cfg['headline']}">
                    {headline}
                  </h1>
                  <p className="{style_cfg['body_text']}">
                    {subheadline}
                  </p>
                </div>

                <div className="{style_cfg['widget_card']}">
                  <div className="flex items-center justify-between border-b border-zinc-800 pb-3">
                    <span className="text-xs font-mono font-bold text-zinc-300">
                      // {sig_widget_name}
                    </span>
                    <button
                      type="button"
                      onClick={{() => setIsLiveActive(prev => !prev)}}
                      className="text-[11px] font-mono px-3 py-1.5 rounded border border-emerald-500/30 text-emerald-400 bg-emerald-950/40 min-h-[44px] inline-flex items-center"
                    >
                      <bdi>{{isLiveActive ? "LIVE_TELEMETRY: ACTIVE" : "PAUSED"}}</bdi>
                    </button>
                  </div>
                  {domain_widget_code}
                </div>

                {cta_group}
              </div>

              <div className="lg:col-span-4 space-y-6">
                {media_container_code}
              </div>
            </div>
          </div>'''

        elif archetype == "editorial_asymmetric_spread":
            return f'''<div role="tabpanel" className="space-y-8 pt-8 animate-fadeIn" data-layout-macro="editorial_asymmetric_spread">
            {{/* Masthead Headline Spread */}}
            <div className="max-w-4xl space-y-4">
              <div className="text-xs font-mono tracking-widest uppercase text-emerald-600 dark:text-emerald-400 font-semibold">
                {"نسخه اختصاصی حوزه" if is_rtl else "Exclusive Curated Spread"}
              </div>
              <h1 className="{style_cfg['headline']}">
                {headline}
              </h1>
              <p className="{style_cfg['body_text']}">
                {subheadline}
              </p>
            </div>

            {{/* Asymmetric 7/5 Spread: Media Leading */}}
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
              <div className="lg:col-span-7">
                {media_container_code}
              </div>
              <div className="lg:col-span-5 space-y-6">
                <div className="{style_cfg['widget_card']}">
                  <div className="flex items-center justify-between border-b border-zinc-200 dark:border-zinc-800 pb-3">
                    <span className="text-xs font-bold text-zinc-700 dark:text-zinc-300">
                      {sig_widget_name}
                    </span>
                    <button
                      type="button"
                      onClick={{() => setIsLiveActive(prev => !prev)}}
                      className="text-[11px] font-mono px-3 py-1.5 rounded border transition-colors min-h-[44px] inline-flex items-center justify-center bg-zinc-100 dark:bg-zinc-800 text-zinc-600 dark:text-zinc-300"
                    >
                      <bdi>{{isLiveActive ? "LIVE FEED" : "PAUSED"}}</bdi>
                    </button>
                  </div>
                  {domain_widget_code}
                </div>

                {billing_switch}
                {cta_group}
              </div>
            </div>
          </div>'''

        elif archetype == "conversion_stepper_funnel":
            return f'''<div role="tabpanel" className="space-y-8 pt-8 animate-fadeIn max-w-5xl mx-auto" data-layout-macro="conversion_stepper_funnel">
            {{/* Conversion Stepper Header */}}
            <div className="text-center space-y-4 max-w-3xl mx-auto">
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-600 border border-emerald-500/20">
                {"۳ مرحله ساده تا نتیجه" if is_rtl else "3 Step Transactional Flow"}
              </div>
              <h1 className="{style_cfg['headline']}">
                {headline}
              </h1>
              <p className="{style_cfg['body_text']} mx-auto">
                {subheadline}
              </p>
            </div>

            {{/* Step Indicators */}}
            <div className="grid grid-cols-3 gap-3 text-center text-xs font-medium">
              <div className="p-3 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-600 dark:text-emerald-400 font-bold">
                {"۱. تنظیم پارامترها" if is_rtl else "1. Configure Inputs"}
              </div>
              <div className="p-3 rounded-xl bg-zinc-100 dark:bg-zinc-800/60 border border-zinc-200 dark:border-zinc-700 text-zinc-600 dark:text-zinc-300">
                {"۲. شبیه سازی زنده" if is_rtl else "2. Real-Time Simulation"}
              </div>
              <div className="p-3 rounded-xl bg-zinc-100 dark:bg-zinc-800/60 border border-zinc-200 dark:border-zinc-700 text-zinc-600 dark:text-zinc-300">
                {"۳. تایید و صدور" if is_rtl else "3. Instant Execution"}
              </div>
            </div>

            {{/* Central Funnel Card */}}
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
              <div className="lg:col-span-7">
                <div className="{style_cfg['widget_card']}">
                  <div className="flex items-center justify-between border-b border-zinc-200 dark:border-zinc-800 pb-3">
                    <span className="text-xs font-bold text-zinc-700 dark:text-zinc-300">
                      {sig_widget_name}
                    </span>
                    <button
                      type="button"
                      onClick={{() => setIsLiveActive(prev => !prev)}}
                      className="text-[11px] font-mono px-3 py-1.5 rounded border transition-colors min-h-[44px] inline-flex items-center justify-center bg-emerald-500/10 text-emerald-600 border-emerald-500/20"
                    >
                      <bdi>{{isLiveActive ? "SIMULATOR: ACTIVE" : "PAUSED"}}</bdi>
                    </button>
                  </div>
                  {domain_widget_code}
                </div>
              </div>

              <div className="lg:col-span-5 space-y-6">
                {media_container_code}
                {billing_switch}
                {cta_group}
              </div>
            </div>
          </div>'''

        elif archetype == "creative_canvas_showcase":
            return f'''<div role="tabpanel" className="space-y-8 pt-8 animate-fadeIn" data-layout-macro="creative_canvas_showcase">
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
              <div className="lg:col-span-6 space-y-6">
                <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider bg-purple-500/10 text-purple-600 dark:text-purple-400 border border-purple-500/20">
                  {"استودیو تعاملی و خلاق" if is_rtl else "Creative Canvas Showcase"}
                </span>
                <h1 className="{style_cfg['headline']}">
                  {headline}
                </h1>
                <p className="{style_cfg['body_text']}">
                  {subheadline}
                </p>
                {billing_switch}
                {cta_group}
              </div>
              <div className="lg:col-span-6">
                {media_container_code}
              </div>
            </div>

            {{/* Floating Interactive Widget Deck */}}
            <div className="{style_cfg['widget_card']} max-w-4xl mx-auto shadow-2xl">
              <div className="flex items-center justify-between border-b border-zinc-200 dark:border-zinc-800 pb-3">
                <span className="text-xs font-bold text-zinc-700 dark:text-zinc-300">
                  {sig_widget_name}
                </span>
                <button
                  type="button"
                  onClick={{() => setIsLiveActive(prev => !prev)}}
                  className="text-[11px] font-mono px-3 py-1.5 rounded border transition-colors min-h-[44px] inline-flex items-center justify-center bg-purple-500/10 text-purple-600 border-purple-500/20"
                >
                  <bdi>{{isLiveActive ? "RENDER ACTIVE" : "PAUSED"}}</bdi>
                </button>
              </div>
              {domain_widget_code}
            </div>
          </div>'''

        elif archetype == "split_laboratory_studio":
            return f'''<div role="tabpanel" className="space-y-6 pt-6 animate-fadeIn" data-layout-macro="split_laboratory_studio">
            <div className="flex items-center justify-between border-b border-zinc-200 dark:border-zinc-800 pb-4">
              <div className="space-y-1">
                <div className="text-xs font-mono text-emerald-600 dark:text-emerald-400 uppercase tracking-wider">
                  {"آزمایشگاه پژوهش و کالیبراسیون داده" if is_rtl else "RESEARCH LAB & DIAGNOSTIC STUDIO"}
                </div>
                <h1 className="{style_cfg['headline']}">
                  {headline}
                </h1>
              </div>
              <div className="hidden sm:block">
                {billing_switch}
              </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
              {{/* Parameter Console (5 Cols) */}}
              <div className="lg:col-span-5 space-y-6">
                <p className="{style_cfg['body_text']}">
                  {subheadline}
                </p>
                <div className="{style_cfg['widget_card']}">
                  <div className="flex items-center justify-between border-b border-zinc-200 dark:border-zinc-800 pb-3">
                    <span className="text-xs font-mono font-bold text-zinc-700 dark:text-zinc-300">
                      LAB://{sig_widget_name}
                    </span>
                    <button
                      type="button"
                      onClick={{() => setIsLiveActive(prev => !prev)}}
                      className="text-[11px] font-mono px-3 py-1.5 rounded border transition-colors min-h-[44px] inline-flex items-center justify-center bg-emerald-500/10 text-emerald-600 border-emerald-500/20"
                    >
                      <bdi>{{isLiveActive ? "ACTIVE TEST" : "IDLE"}}</bdi>
                    </button>
                  </div>
                  {domain_widget_code}
                </div>
                {cta_group}
              </div>

              {{/* Viewport Visualizer (7 Cols) */}}
              <div className="lg:col-span-7 space-y-6">
                {media_container_code}
              </div>
            </div>
          </div>'''

        else: # classic_structured_saas
            return f'''<div role="tabpanel" className="grid grid-cols-1 lg:grid-cols-12 gap-8 pt-8 items-center animate-fadeIn" data-layout-macro="classic_structured_saas">
            <div className="lg:col-span-7 space-y-6">
              <h1 className="{style_cfg['headline']}">
                {headline}
              </h1>
              <p className="{style_cfg['body_text']}">
                {subheadline}
              </p>
              {billing_switch}
              {cta_group}
            </div>

            <div className="lg:col-span-5 space-y-6">
              <div className="{style_cfg['widget_card']}">
                <div className="flex items-center justify-between border-b border-zinc-200 dark:border-zinc-800 pb-3">
                  <span className="text-xs font-bold text-zinc-700 dark:text-zinc-300">
                    {sig_widget_name}
                  </span>
                  <button
                    type="button"
                    onClick={{() => setIsLiveActive(prev => !prev)}}
                    className={{`text-[11px] font-mono px-3 py-1.5 rounded border transition-colors min-h-[44px] inline-flex items-center justify-center ${{
                      isLiveActive 
                        ? "bg-emerald-500/10 text-emerald-600 border-emerald-500/20" 
                        : "bg-zinc-200 dark:bg-zinc-800 text-zinc-500 border-transparent"
                    }}`}}
                  >
                    <bdi>{{isLiveActive ? "LIVE FEED" : "PAUSED"}}</bdi>
                  </button>
                </div>
                {domain_widget_code}
              </div>

              {media_container_code}
            </div>
          </div>'''

    def generate_react_tsx(self, decision: Dict[str, Any], component_name: str = "VibeMasterpiece") -> str:

        """
        Generates a modular, living React 19 / TypeScript component (.tsx)
        featuring render-affecting style compiler, living micro-states (useState),
        domain-calibrated signature widgets, and complete WCAG AAA / BiDi isolation.
        """
        domain_id = decision.get("genome", {}).get("domain") or decision.get("intent", {}).get("product_domain", "general_modern_saas")
        blueprint = decision.get("intent", {}).get("blueprint") or self.blueprints.get("domains", {}).get(domain_id, {})
        sig_widget = blueprint.get("signature_widget", {})
        selected_style = decision.get("selected_style", "clean_stripe")
        theme_strategy = decision.get("intent", {}).get("theme_strategy", "light")
        is_rtl = decision.get("genome", {}).get("platform", {}).get("rtl_support", False) or (decision.get("intent", {}).get("language", ["en"])[0] == "fa" if decision.get("intent", {}).get("language") else False)
        dir_attr = 'dir="rtl"' if is_rtl else 'dir="ltr"'

        style_cfg = self._compile_style(selected_style, theme_strategy)

        mock_data_all = blueprint.get("mock_data", {})
        mock_data_dict = mock_data_all.get("fa" if is_rtl else "en", {}) if isinstance(mock_data_all.get("en"), dict) else mock_data_all
        title_fa = mock_data_dict.get("headline", "پلتفرم نوآورانه نسل جدید")
        title_en = mock_data_dict.get("headline", "Next-Generation Autonomous Intelligence")
        headline = mock_data_dict.get("headline", title_fa if is_rtl else title_en)
        subheadline = mock_data_dict.get("subheadline", "تجربه ای منحصربه فرد، بدون کلیشه و مهندسی شده با پیشرفته ترین معیارهای دسترسی پذیری نوری و تعاملات روان." if is_rtl else "Autonomous precision interface engineered with strict WCAG AAA contrast, physics spring motion, and domain priors.")
        cta_primary = mock_data_dict.get("cta_primary", "شروع آنی پروژه" if is_rtl else "Get Started Now")
        cta_secondary = mock_data_dict.get("cta_secondary", "مشاهده دموی تعاملی" if is_rtl else "Explore Interactive Demo")
        sig_widget_name = sig_widget.get("name", "ماژول تعاملی هوشمند" if is_rtl else "Interactive Intelligence Hub")

        domain_metrics = mock_data_dict.get("metrics", [])
        metric1 = domain_metrics[0] if len(domain_metrics) > 0 else {"label": "نرخ انطباق دسترسی پذیری" if is_rtl else "Accessibility Compliance", "value": "100% WCAG AAA"}
        metric2 = domain_metrics[1] if len(domain_metrics) > 1 else {"label": "زمان پاسخگویی سنسور" if is_rtl else "Sensor Latency", "value": "< 0.5 ms"}
        metric3 = domain_metrics[2] if len(domain_metrics) > 2 else {"label": "کاهش چرخه های اصلاح" if is_rtl else "Iteration Reduction", "value": "- 78.4%"}

        domain_widget_code = self._render_domain_widget(domain_id, is_rtl, style_cfg, blueprint)
        media_container_code = self.asset_director.generate_media_container_jsx(domain_id, selected_style, is_rtl)

        macro_panel_jsx = self._render_macro_panel(
            domain_id=domain_id,
            is_rtl=is_rtl,
            style_cfg=style_cfg,
            headline=headline,
            subheadline=subheadline,
            cta_primary=cta_primary,
            cta_secondary=cta_secondary,
            sig_widget_name=sig_widget_name,
            domain_widget_code=domain_widget_code,
            media_container_code=media_container_code
        )

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
  const [simulatedValue, setSimulatedValue] = useState<number>(25000);
  const [splitPos, setSplitPos] = useState<number>(50);
  const [isLiveActive, setIsLiveActive] = useState<boolean>(true);

  const tabs = [
    {{"id": "overview", "label": "{"نمای اصلی و ویجت تعاملی" if is_rtl else "Primary Experience"}"}},
    {{"id": "telemetry", "label": "{"شاخص های عملکردی حوزه" if is_rtl else "Domain Performance"}"}},
    {{"id": "architecture", "label": "{"معماری و مشخصات فنی" if is_rtl else "System Blueprint"}"}}
  ];

  return (
    <div {dir_attr} className={{`w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 font-sans antialiased text-foreground ${{className}}`}}>
      {{/* Ambient Style-Compiled Card Layer */}}
      <div className="{style_cfg['container']}">
        {style_cfg['border_beam']}

        {{/* Header Badges & Interactive Tab Navigation */}}
        <div className="flex flex-wrap items-center justify-between gap-4 border-b border-zinc-200/80 dark:border-zinc-800/80 pb-6">
          <div className="flex items-center space-x-3 rtl:space-x-reverse">
            <span className="{style_cfg['header_badge']}">
              <span className="size-2 rounded-full bg-emerald-500 animate-pulse" />
              <span>{"سامانه فعال و تایید شده" if is_rtl else "System Operational"}</span>
            </span>
            <span className="{style_cfg['version_tag']}">
              <bdi>v3.8.0 • OKLCH AAA</bdi>
            </span>
          </div>

          {{/* Interactive Tabs with Full Accessibility Role */}}
          <div role="tablist" aria-label="Feature Tabs" className="{style_cfg['tab_container']}">
            {{tabs.map((tab, idx) => (
              <button
                key={{tab.id}}
                type="button"
                role="tab"
                aria-selected={{activeTab === idx}}
                onClick={{() => setActiveTab(idx)}}
                className={{`transition-all duration-200 min-h-[44px] ${{
                  activeTab === idx ? "{style_cfg['tab_btn_active']}" : "{style_cfg['tab_btn_inactive']}"
                }}`}}
              >
                {{tab.label}}
              </button>
            ))}}
          </div>
        </div>

        {{/* Tab Panel 0: Overview & Signature Domain Widget */}}
        {{activeTab === 0 && (
          {macro_panel_jsx}
        )}}


        {{/* Tab Panel 1: Live Telemetry & Metrics Analytics */}}
        {{activeTab === 1 && (
          <div role="tabpanel" className="grid grid-cols-1 sm:grid-cols-3 gap-6 pt-8 animate-fadeIn" data-origin="synthetic_demo">
            <div className="{style_cfg['telemetry_card']}">
              <div className="text-xs font-medium text-zinc-500">{metric1['label']}</div>
              <div className="text-2xl font-bold font-mono text-emerald-600 dark:text-emerald-400">
                <bdi>{{{json.dumps(metric1['value'], ensure_ascii=False)}}}</bdi>
              </div>
              <div className="text-xs text-zinc-400">{"شاخص عملکردی تایید شده حوزه" if is_rtl else "Verified production benchmark metric"}</div>
            </div>

            <div className="{style_cfg['telemetry_card']}">
              <div className="text-xs font-medium text-zinc-500">{metric2['label']}</div>
              <div className="text-2xl font-bold font-mono text-sky-600 dark:text-sky-400">
                <bdi>{{{json.dumps(metric2['value'], ensure_ascii=False)}}}</bdi>
              </div>
              <div className="text-xs text-zinc-400">{"پایش لحظه ای و تضمین سطح خدمت" if is_rtl else "Real-time telemetry and SLA assurance"}</div>
            </div>

            <div className="{style_cfg['telemetry_card']}">
              <div className="text-xs font-medium text-zinc-500">{metric3['label']}</div>
              <div className="text-2xl font-bold font-mono text-indigo-600 dark:text-indigo-400">
                <bdi>{{{json.dumps(metric3['value'], ensure_ascii=False)}}}</bdi>
              </div>
              <div className="text-xs text-zinc-400">{"بهینه سازی مداوم با رصد الگوریتمی رویدادها" if is_rtl else "Continuously optimized by invariant monitoring"}</div>
            </div>
          </div>
        )}}

        {{/* Tab Panel 2: Architecture & Domain Blueprint Specification */}}
        {{activeTab === 2 && (
          <div role="tabpanel" className="pt-8 space-y-6 animate-fadeIn">
            <div className="overflow-x-auto">
              <table className="w-full text-xs text-left rtl:text-right border-collapse">
                <thead>
                  <tr className="border-b border-zinc-200 dark:border-zinc-800 text-zinc-400 font-mono uppercase">
                    <th className="py-2.5 px-3">{"شاخص معماری" if is_rtl else "Blueprint Dimension"}</th>
                    <th className="py-2.5 px-3">{"مقدار پیکربندی شده" if is_rtl else "Resolved Value"}</th>
                    <th className="py-2.5 px-3">{"تضمین کیفیت" if is_rtl else "Invariant Status"}</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-zinc-200/60 dark:divide-zinc-800/60 text-zinc-600 dark:text-zinc-300">
                  <tr>
                    <td className="py-2.5 px-3 font-semibold">{"حوزه تخصصی محصول" if is_rtl else "Product Domain"}</td>
                    <td className="py-2.5 px-3 font-mono">{domain_id}</td>
                    <td className="py-2.5 px-3 text-emerald-600 dark:text-emerald-400 font-semibold">MATCH 100%</td>
                  </tr>
                  <tr>
                    <td className="py-2.5 px-3 font-semibold">{"سبک بصری کانونی" if is_rtl else "Visual Chemistry"}</td>
                    <td className="py-2.5 px-3 font-mono">{selected_style}</td>
                    <td className="py-2.5 px-3 text-sky-600 dark:text-sky-400 font-semibold">COMPILED</td>
                  </tr>
                  <tr>
                    <td className="py-2.5 px-3 font-semibold">{"استراتژی تم و نور" if is_rtl else "Lighting Mode"}</td>
                    <td className="py-2.5 px-3 font-mono">{theme_strategy}</td>
                    <td className="py-2.5 px-3 text-emerald-600 dark:text-emerald-400 font-semibold">BALANCED</td>
                  </tr>
                  <tr>
                    <td className="py-2.5 px-3 font-semibold">{"جهت رندر و تایپوگرافی" if is_rtl else "Text Direction & BiDi"}</td>
                    <td className="py-2.5 px-3 font-mono">{"RTL (Persian Isolated)" if is_rtl else "LTR (Pure English)"}</td>
                    <td className="py-2.5 px-3 text-emerald-600 dark:text-emerald-400 font-semibold">&lt;bdi&gt; SECURED</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        )}}
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

        domain_id = decision.get("genome", {}).get("domain") or decision.get("intent", {}).get("product_domain", "")
        blueprint = decision.get("intent", {}).get("blueprint") or self.blueprints.get("domains", {}).get(domain_id, {})
        mock_data_all = blueprint.get("mock_data", {})
        mock_data_dict = mock_data_all.get("fa" if is_rtl else "en", {}) if isinstance(mock_data_all.get("en"), dict) else mock_data_all
        blueprint_headline = mock_data_dict.get("headline")
        blueprint_subheadline = mock_data_dict.get("subheadline")
        blueprint_cta_primary = mock_data_dict.get("cta_primary")
        blueprint_cta_secondary = mock_data_dict.get("cta_secondary")
        blueprint_metrics = mock_data_dict.get("metrics")

        # Resolve clean display title and navbar brand name
        raw_prompt_indicators = [
            "میخوام", "بساز", "طراحی", "سایت", "یک", "یه", "برای", "رزرو", "خرید", "سفارش",
            "نوبت", "سامانه", "اپلیکیشن", "create", "build", "make", "want", "for a", "landing", "app", "book"
        ]
        is_raw_prompt = any(ind in prompt_title.lower() for ind in raw_prompt_indicators) or len(prompt_title.split()) > 3
        display_title = blueprint_headline if (blueprint_headline and is_raw_prompt) else prompt_title
        hero_headline = blueprint_headline or display_title
        brand_name = (decision.get("intent", {}).get("audience", {}).get("type") or ("پلتفرم تخصصی" if is_rtl else "Vibe Studio")) if is_raw_prompt else prompt_title
        hero_subheadline = blueprint_subheadline or ("تجربه ای منحصربه فرد با معماری مدرن، سرعت بالا و هماهنگی کامل با نیازهای کسب وکار شما." if is_rtl else "Autonomous precision interface engineered with strict accessibility, responsive geometry, and domain priors.")
        cta_primary_label = blueprint_cta_primary or ("شروع همکاری" if is_rtl else "Get Started")
        cta_secondary_label = blueprint_cta_secondary or ("مشاهده خدمات" if is_rtl else "Explore Services")

        # Smart sub-intent adaptation for loans and credit in fintech domain
        lower_prompt = prompt_title.lower()
        if domain_id == "fintech_banking" and any(k in lower_prompt for k in ["وام", "قرض", "تسهیلات", "loan", "credit"]):
            if is_rtl:
                hero_headline = "سامانه دریافت آنلاین تسهیلات و وام قرض الحسنه"
                hero_subheadline = "محاسبه هوشمند اقساط، اعتبارسنجی دیجیتال و واریز سریع تسهیلات بدون ضامن با حداقل کارمزد بانکی."
                cta_primary_label = "درخواست آنلاین تسهیلات"
                cta_secondary_label = "محاسبه اقساط و شرایط"
                blueprint_metrics = [
                    {"label": "سقف تسهیلات آنلاین", "value": "تا ۵۰۰ میلیون تومان"},
                    {"label": "مدت زمان اعتبارسنجی", "value": "< ۲۴ ساعت"},
                    {"label": "کارمزد تسهیلات", "value": "۴٪ سالانه"}
                ]
            else:
                hero_headline = "Fast Digital Loans & Personal Credit Financing"
                hero_subheadline = "Instant credit scoring, transparent terms, and rapid disbursement directly to your account."
                cta_primary_label = "Apply for Loan"
                cta_secondary_label = "Calculate Payments"
                blueprint_metrics = [
                    {"label": "Max Loan Amount", "value": "$50,000"},
                    {"label": "Approval Time", "value": "< 24 Hours"},
                    {"label": "Starting APR", "value": "4.2% Fixed"}
                ]

        # Prepare domain metrics cards
        if not blueprint_metrics:
            blueprint_metrics = [
                {"label": "شاخص اعتماد مشتریان" if is_rtl else "Customer Trust", "value": "۹۹.۴٪" if is_rtl else "99.4%"},
                {"label": "سرعت پاسخگویی" if is_rtl else "Response Speed", "value": "< ۵ دقیقه" if is_rtl else "< 5 mins"},
                {"label": "کیفیت خدمات" if is_rtl else "Service Rating", "value": "۴.۹ از ۵" if is_rtl else "4.9 / 5"}
            ]

        metrics_html_items = []
        for m in blueprint_metrics[:3]:
            lbl = str(m.get("label", "")).replace("<", "&lt;").replace(">", "&gt;")
            val = str(m.get("value", "")).replace("<", "&lt;").replace(">", "&gt;")
            metrics_html_items.append(f"""            <div class="p-3.5 bg-[var(--canvas-bg)] rounded-[var(--radius-base)] border border-[var(--border-subtle)]">
              <div class="text-xs text-[var(--text-muted)] mb-1">{lbl}</div>
              <div class="text-2xl font-bold text-[var(--accent)]"><bdi>{val}</bdi></div>
            </div>""")
        metrics_block_html = "\n".join(metrics_html_items)

        # Assemble Domain-Specific macOS Window Chrome Canvas
        if domain_id == "devops_cloud_terminal":
            window_chrome_content_html = f"""            <div class="space-y-3 font-mono">
              <div class="flex items-center justify-between p-3 bg-[var(--canvas-bg)] rounded-[var(--radius-base)] border border-[var(--border-subtle)]">
                <div class="flex items-center gap-2">
                  <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
                  <span class="text-xs text-[var(--text-muted)]">Ingress Telemetry</span>
                </div>
                <span class="text-xs font-bold text-emerald-500"><bdi>12.4 ms (p50)</bdi></span>
              </div>
              <div class="p-3 bg-[var(--canvas-bg)] rounded-[var(--radius-base)] border border-[var(--border-subtle)]">
                <div class="flex justify-between text-[11px] text-[var(--text-muted)] mb-1">
                  <span>Pod Mesh Throughput</span>
                  <span class="text-[var(--accent)] font-bold"><bdi>3.2k req/s</bdi></span>
                </div>
                <svg class="w-full h-8 text-[var(--accent)]" viewBox="0 0 100 25" fill="none" stroke="currentColor" stroke-width="1.75">
                  <path d="M0 20 Q 20 5, 40 18 T 80 10 T 100 6" />
                </svg>
              </div>
              <div class="p-3 bg-black/90 rounded-[var(--radius-base)] border border-emerald-900/40 text-[11px] text-emerald-400 font-mono space-y-1">
                <div class="text-zinc-500"># kubectl get mesh --namespace=prod</div>
                <div>[OK] 12/12 microservices healthy</div>
                <div class="text-emerald-300">&gt; telemetry stream synchronized</div>
              </div>
            </div>"""
        elif domain_id in ["beauty_clinical_wellness", "healthcare_clinical_dental", "health_medical_clinic", "healthcare_hospital_medical"]:
            window_chrome_content_html = f"""            <div class="space-y-3">
              <div class="p-3.5 bg-[var(--canvas-bg)] rounded-[var(--radius-base)] border border-[var(--border-subtle)] flex items-center justify-between">
                <div>
                  <div class="text-xs text-[var(--text-muted)]">{"وضعیت پذیرش امروز" if is_rtl else "Today's Clinic Availability"}</div>
                  <div class="text-sm font-bold text-emerald-500 flex items-center gap-1.5 mt-0.5">
                    <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
                    <span>{"۳ نوبت مشاوره خالی" if is_rtl else "3 VIP Consultations Open"}</span>
                  </div>
                </div>
                <span class="px-2.5 py-1 rounded-full text-[11px] font-bold bg-[var(--accent)]/10 text-[var(--accent)] border border-[var(--accent)]/20">{"پذیرش فوری" if is_rtl else "Express"}</span>
              </div>
              <div class="p-3.5 bg-[var(--canvas-bg)] rounded-[var(--radius-base)] border border-[var(--border-subtle)]">
                <div class="text-xs text-[var(--text-muted)] mb-2">{"نزدیک ترین ساعات قابل رزرو" if is_rtl else "Next Available Slots"}</div>
                <div class="grid grid-cols-3 gap-2">
                  <span class="px-2 py-1 text-center text-xs font-semibold rounded bg-[var(--surface-bg)] border border-[var(--border-subtle)] text-[var(--text-primary)]"><bdi>۱۰:۳۰</bdi></span>
                  <span class="px-2 py-1 text-center text-xs font-semibold rounded bg-[var(--accent)] text-[var(--vibe-on-primary,#fff)]"><bdi>۱۲:۰۰</bdi></span>
                  <span class="px-2 py-1 text-center text-xs font-semibold rounded bg-[var(--surface-bg)] border border-[var(--border-subtle)] text-[var(--text-primary)]"><bdi>۱۶:۳۰</bdi></span>
                </div>
              </div>
              <div class="p-3 bg-[var(--surface-bg)] rounded-[var(--radius-base)] border border-amber-500/20 text-xs text-amber-600 dark:text-amber-400 flex items-center gap-2">
                <svg class="w-4 h-4 text-amber-500 flex-shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>
                <span>{"ویزیت و اسکن سه بعدی دندان با گارانتی رسمی کلینیک" if is_rtl else "Includes 3D digital scan & specialist warranty"}</span>
              </div>
            </div>"""
        else:
            window_chrome_content_html = f"""            <div class="space-y-3">
{metrics_block_html}
            </div>"""

        # Determine domain-specific navigation and sections
        if domain_id == "devops_cloud_terminal":
            nav_links = [
                {"href": "#cluster", "label": "Cluster Health"},
                {"href": "#latency", "label": "P95/P99 Latency"},
                {"href": "#services", "label": "Services Mesh"},
                {"href": "#logs", "label": "Live Terminal"}
            ]
        elif domain_id in ["beauty_clinical_wellness", "healthcare_clinical_dental", "health_medical_clinic", "healthcare_hospital_medical"]:
            nav_links = [
                {"href": "#services", "label": "خدمات و تعرفه ها" if is_rtl else "Treatments & Pricing"},
                {"href": "#portfolio", "label": "نمونه کارها" if is_rtl else "Before & After"},
                {"href": "#doctors", "label": "تیم متخصصین" if is_rtl else "Specialists"},
                {"href": "#booking", "label": "نوبت دهی آنلاین" if is_rtl else "Book Appointment"}
            ]
        else:
            nav_links = [
                {"href": "#features", "label": "ویژگی ها" if is_rtl else "Features"},
                {"href": "#services", "label": "خدمات و تعرفه ها" if is_rtl else "Services & Pricing"},
                {"href": "#contact", "label": "ارتباط با ما" if is_rtl else "Contact"}
            ]

        nav_links_html = "\n".join([
            f'        <a href="{link["href"]}" class="text-sm font-medium hover:text-[var(--accent)] transition-colors min-h-[44px] inline-flex items-center">{link["label"]}</a>'
            for link in nav_links
        ])

        # Generate Domain-Specific Sections HTML
        if domain_id == "devops_cloud_terminal":
            domain_sections_html = f"""
    <!-- DevOps Section 1: Cluster Health -->
    <section id="cluster" class="mt-12 pt-8 border-t border-[var(--border-subtle)]" aria-labelledby="cluster-heading">
      <div class="flex items-center justify-between mb-6">
        <div>
          <h2 id="cluster-heading" class="text-2xl font-bold tracking-tight">Kubernetes Cluster Status</h2>
          <p class="text-xs text-[var(--text-muted)] mt-1">Real-time health telemetry across active worker nodes and pods.</p>
        </div>
        <span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-mono font-semibold bg-emerald-500/10 text-emerald-500 border border-emerald-500/20">
          <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
          All Systems Operational (99.99%)
        </span>
      </div>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 font-mono text-xs">
        <div class="p-4 bg-[var(--surface-bg)] {card_border} rounded-[var(--radius-container)] {card_shadow} space-y-2">
          <div class="flex justify-between text-[var(--text-muted)]"><span>ingress-nginx</span><span class="text-emerald-500 font-bold">READY</span></div>
          <div class="text-base font-bold text-[var(--text-primary)]">6/6 Pods Running</div>
          <div class="w-full bg-[var(--canvas-bg)] rounded-full h-1.5"><div class="bg-emerald-500 h-1.5 rounded-full" style="width: 100%"></div></div>
        </div>
        <div class="p-4 bg-[var(--surface-bg)] {card_border} rounded-[var(--radius-container)] {card_shadow} space-y-2">
          <div class="flex justify-between text-[var(--text-muted)]"><span>api-gateway-mesh</span><span class="text-emerald-500 font-bold">READY</span></div>
          <div class="text-base font-bold text-[var(--text-primary)]">12/12 Pods Running</div>
          <div class="w-full bg-[var(--canvas-bg)] rounded-full h-1.5"><div class="bg-emerald-500 h-1.5 rounded-full" style="width: 100%"></div></div>
        </div>
        <div class="p-4 bg-[var(--surface-bg)] {card_border} rounded-[var(--radius-container)] {card_shadow} space-y-2">
          <div class="flex justify-between text-[var(--text-muted)]"><span>auth-worker-daemon</span><span class="text-amber-500 font-bold">SYNCING</span></div>
          <div class="text-base font-bold text-[var(--text-primary)]">4/4 Pods (88% CPU)</div>
          <div class="w-full bg-[var(--canvas-bg)] rounded-full h-1.5"><div class="bg-amber-500 h-1.5 rounded-full" style="width: 88%"></div></div>
        </div>
        <div class="p-4 bg-[var(--surface-bg)] {card_border} rounded-[var(--radius-container)] {card_shadow} space-y-2">
          <div class="flex justify-between text-[var(--text-muted)]"><span>redis-cluster-cache</span><span class="text-emerald-500 font-bold">READY</span></div>
          <div class="text-base font-bold text-[var(--text-primary)]">3 Master / 3 Replica</div>
          <div class="w-full bg-[var(--canvas-bg)] rounded-full h-1.5"><div class="bg-emerald-500 h-1.5 rounded-full" style="width: 100%"></div></div>
        </div>
      </div>
    </section>

    <!-- DevOps Section 2: P95/P99 Latency & SLO -->
    <section id="latency" class="mt-12 pt-8 border-t border-[var(--border-subtle)]" aria-labelledby="latency-heading">
      <h2 id="latency-heading" class="text-2xl font-bold tracking-tight mb-6">Throughput & Latency Profiling</h2>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 font-mono">
        <div class="vibe-spotlight-card p-6 bg-[var(--surface-bg)] {card_border} rounded-[var(--radius-container)] {card_shadow} space-y-2">
          <div class="text-xs text-[var(--text-muted)] uppercase tracking-wider">Median Latency (p50)</div>
          <div class="text-3xl font-extrabold text-[var(--accent)]"><bdi>12.4 ms</bdi></div>
          <div class="text-xs text-emerald-500 flex items-center gap-1.5"><svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true"><polyline points="20 6 9 17 4 12"></polyline></svg><span>-4.2% vs 7-day average</span></div>
        </div>
        <div class="vibe-spotlight-card p-6 bg-[var(--surface-bg)] {card_border} rounded-[var(--radius-container)] {card_shadow} space-y-2">
          <div class="text-xs text-[var(--text-muted)] uppercase tracking-wider">Tail Latency (p95)</div>
          <div class="text-3xl font-extrabold text-[var(--accent)]"><bdi>38.2 ms</bdi></div>
          <div class="text-xs text-emerald-500 flex items-center gap-1.5"><svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true"><polyline points="20 6 9 17 4 12"></polyline></svg><span>Well within 50ms SLO threshold</span></div>
        </div>
        <div class="vibe-spotlight-card p-6 bg-[var(--surface-bg)] {card_border} rounded-[var(--radius-container)] {card_shadow} space-y-2">
          <div class="text-xs text-[var(--text-muted)] uppercase tracking-wider">Peak Latency (p99)</div>
          <div class="text-3xl font-extrabold text-amber-500"><bdi>84.1 ms</bdi></div>
          <div class="text-xs text-[var(--text-muted)]">SLO target: &lt; 100ms</div>
        </div>
      </div>
    </section>

    <!-- DevOps Section 3: Services Mesh -->
    <section id="services" class="mt-12 pt-8 border-t border-[var(--border-subtle)]" aria-labelledby="services-mesh-heading">
      <h2 id="services-mesh-heading" class="text-2xl font-bold tracking-tight mb-6">Microservices Mesh Health</h2>
      <div class="overflow-x-auto {card_border} rounded-[var(--radius-container)] bg-[var(--surface-bg)] {card_shadow}">
        <table class="w-full text-start text-xs font-mono">
          <thead class="bg-[var(--canvas-bg)] text-[var(--text-muted)] uppercase border-b border-[var(--border-subtle)]">
            <tr>
              <th scope="col" class="px-6 py-3 text-start">Service Name</th>
              <th scope="col" class="px-6 py-3 text-start">Protocol</th>
              <th scope="col" class="px-6 py-3 text-start">HTTP Status</th>
              <th scope="col" class="px-6 py-3 text-start">Uptime</th>
              <th scope="col" class="px-6 py-3 text-start">Action</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-[var(--border-subtle)]">
            <tr>
              <td class="px-6 py-4 font-bold text-[var(--text-primary)]">edge-ingress-proxy</td>
              <td class="px-6 py-4 text-[var(--text-muted)]">HTTP/3 QUIC</td>
              <td class="px-6 py-4"><span class="px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-500 font-bold">200 OK</span></td>
              <td class="px-6 py-4"><bdi>99.999%</bdi></td>
              <td class="px-6 py-4"><button type="button" class="btn-action text-xs text-[var(--accent)] hover:underline min-h-[44px] inline-flex items-center">Inspect Traces</button></td>
            </tr>
            <tr>
              <td class="px-6 py-4 font-bold text-[var(--text-primary)]">billing-event-worker</td>
              <td class="px-6 py-4 text-[var(--text-muted)]">gRPC / TLS</td>
              <td class="px-6 py-4"><span class="px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-500 font-bold">200 OK</span></td>
              <td class="px-6 py-4"><bdi>99.985%</bdi></td>
              <td class="px-6 py-4"><button type="button" class="btn-action text-xs text-[var(--accent)] hover:underline min-h-[44px] inline-flex items-center">Inspect Traces</button></td>
            </tr>
            <tr>
              <td class="px-6 py-4 font-bold text-[var(--text-primary)]">telemetry-aggregator</td>
              <td class="px-6 py-4 text-[var(--text-muted)]">Kafka / TCP</td>
              <td class="px-6 py-4"><span class="px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-500 font-bold">200 OK</span></td>
              <td class="px-6 py-4"><bdi>99.994%</bdi></td>
              <td class="px-6 py-4"><button type="button" class="btn-action text-xs text-[var(--accent)] hover:underline min-h-[44px] inline-flex items-center">Inspect Traces</button></td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <!-- DevOps Section 4: Live Terminal & Log Stream -->
    <section id="logs" class="mt-12 pt-8 border-t border-[var(--border-subtle)]" aria-labelledby="logs-heading">
      <div class="flex items-center justify-between mb-4">
        <h2 id="logs-heading" class="text-2xl font-bold tracking-tight">Live Kubectl Telemetry Console</h2>
        <div class="flex gap-2">
          <button type="button" id="toggle-log-stream" class="px-3 py-1.5 text-xs font-mono font-bold rounded-[var(--radius-button)] bg-[var(--canvas-bg)] border border-[var(--border-subtle)] hover:bg-[var(--surface-bg)] min-h-[44px] transition-colors">
            Pause Stream
          </button>
          <button type="button" id="copy-curl-btn" class="px-3 py-1.5 text-xs font-mono font-bold rounded-[var(--radius-button)] bg-[var(--accent)] text-[var(--vibe-on-primary,#fff)] min-h-[44px] transition-colors">
            Copy Curl Snippet
          </button>
        </div>
      </div>
      <div class="p-5 bg-black border border-emerald-900/60 rounded-[var(--radius-container)] font-mono text-xs text-emerald-400 space-y-1.5 overflow-x-auto shadow-inner">
        <div class="text-zinc-500"># Connected to cluster: us-east-prod-k8s-mesh [Active Context]</div>
        <div>[2026-09-30T04:00:12Z] INFO  ingress-controller: sync service target 10.244.2.14:8080 (healthy)</div>
        <div>[2026-09-30T04:00:15Z] INFO  auth-worker: Token verification latency p95=8.2ms, status=AUTHORIZED</div>
        <div>[2026-09-30T04:00:18Z] DEBUG redis-cache: Cache hit ratio: 98.4% (3.2k ops/sec)</div>
        <div>[2026-09-30T04:00:22Z] WARN  worker-node-4: Memory saturation approaching 82% threshold; auto-scaler standing by</div>
        <div class="text-emerald-300 font-bold animate-pulse">&gt; tail -f /var/log/syslog --follow [LIVE STREAMING]</div>
      </div>
    </section>
"""
        elif domain_id in ["beauty_clinical_wellness", "healthcare_clinical_dental", "health_medical_clinic", "healthcare_hospital_medical"]:
            domain_sections_html = f"""
    <!-- Healthcare Section 1: Services & Treatments -->
    <section id="services" class="mt-12 pt-8 border-t border-[var(--border-subtle)]" aria-labelledby="services-heading">
      <div class="max-w-2xl mb-8">
        <h2 id="services-heading" class="text-2xl sm:text-3xl font-bold tracking-tight">{"خدمات تخصصی و تعرفه های شفاف" if is_rtl else "Specialized Treatments & Transparent Pricing"}</h2>
        <p class="text-sm text-[var(--text-muted)] mt-2">{"کلیه درمان ها با پیشرفته ترین تجهیزات دیجیتال، مواد درجه یک بین المللی و ضمانت کتبی ارائه می شوند." if is_rtl else "All treatments performed with digital imaging, premium biocompatible materials, and certified warranties."}</p>
      </div>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <div class="p-6 bg-[var(--surface-bg)] {card_border} rounded-[var(--radius-container)] {card_shadow} flex flex-col justify-between space-y-4">
          <div>
            <span class="inline-flex px-2.5 py-0.5 rounded-full text-xs font-semibold bg-[var(--accent)]/10 text-[var(--accent)] mb-2">{"طراحی لبخند" if is_rtl else "Cosmetic"}</span>
            <h3 class="text-lg font-bold">{"کامپوزیت ونیر نانو سرامیک" if is_rtl else "Nano-Ceramic Composite"}</h3>
            <p class="text-xs text-[var(--text-muted)] mt-1">{"اصلاح بدفرمی و بدرنگی دندان ها با استحکام و شفافیت طبیعی بدون تراش." if is_rtl else "Non-invasive smile enhancement with ultra-durable natural translucency."}</p>
          </div>
          <div class="pt-4 border-t border-[var(--border-subtle)]">
            <div class="text-xs text-[var(--text-muted)]">{"هزینه هر واحد" if is_rtl else "Starting from"}</div>
            <div class="text-lg font-bold text-[var(--accent)]"><bdi>{"از ۵,۵۰۰,۰۰۰ تومان" if is_rtl else "$350 / tooth"}</bdi></div>
          </div>
        </div>

        <div class="p-6 bg-[var(--surface-bg)] {card_border} rounded-[var(--radius-container)] {card_shadow} flex flex-col justify-between space-y-4">
          <div>
            <span class="inline-flex px-2.5 py-0.5 rounded-full text-xs font-semibold bg-[var(--accent)]/10 text-[var(--accent)] mb-2">{"کاشت دندان" if is_rtl else "Implantology"}</span>
            <h3 class="text-lg font-bold">{"ایمپلنت دیجیتال فوری" if is_rtl else "Immediate Digital Implant"}</h3>
            <p class="text-xs text-[var(--text-muted)] mt-1">{"جراحی با راهنمای سه بعدی و بارگذاری فوری روکش با کمترین درد و خونریزی." if is_rtl else "3D surgical guide placement with immediate crown loading."}</p>
          </div>
          <div class="pt-4 border-t border-[var(--border-subtle)]">
            <div class="text-xs text-[var(--text-muted)]">{"هزینه هر واحد" if is_rtl else "Starting from"}</div>
            <div class="text-lg font-bold text-[var(--accent)]"><bdi>{"از ۱۸,۰۰۰,۰۰۰ تومان" if is_rtl else "$950 / unit"}</bdi></div>
          </div>
        </div>

        <div class="p-6 bg-[var(--surface-bg)] {card_border} rounded-[var(--radius-container)] {card_shadow} flex flex-col justify-between space-y-4">
          <div>
            <span class="inline-flex px-2.5 py-0.5 rounded-full text-xs font-semibold bg-[var(--accent)]/10 text-[var(--accent)] mb-2">{"سفید کردن دندان" if is_rtl else "Whitening"}</span>
            <h3 class="text-lg font-bold">{"بلیچینگ تخصصی با لیزر" if is_rtl else "Laser Office Bleaching"}</h3>
            <p class="text-xs text-[var(--text-muted)] mt-1">{"روشن سازی دندان ها تا ۴ درجه در یک جلسه کوتاه ۴۵ دقیقه ای." if is_rtl else "In-office laser whitening up to 4 shades lighter in 45 minutes."}</p>
          </div>
          <div class="pt-4 border-t border-[var(--border-subtle)]">
            <div class="text-xs text-[var(--text-muted)]">{"هر دو فک" if is_rtl else "Full arch"}</div>
            <div class="text-lg font-bold text-[var(--accent)]"><bdi>{"۴,۲۰۰,۰۰۰ تومان" if is_rtl else "$280 total"}</bdi></div>
          </div>
        </div>

        <div class="p-6 bg-[var(--surface-bg)] {card_border} rounded-[var(--radius-container)] {card_shadow} flex flex-col justify-between space-y-4">
          <div>
            <span class="inline-flex px-2.5 py-0.5 rounded-full text-xs font-semibold bg-[var(--accent)]/10 text-[var(--accent)] mb-2">{"ارتودنسی" if is_rtl else "Orthodontics"}</span>
            <h3 class="text-lg font-bold">{"ارتودنسی نامرئی (الاینر)" if is_rtl else "Clear Aligners"}</h3>
            <p class="text-xs text-[var(--text-muted)] mt-1">{"مرتب سازی دندان ها با پلاک های شفاف متحرک بدون نیاز به براکت های فلزی." if is_rtl else "Discreet teeth alignment using custom removable clear trays."}</p>
          </div>
          <div class="pt-4 border-t border-[var(--border-subtle)]">
            <div class="text-xs text-[var(--text-muted)]">{"طرح درمان کامل" if is_rtl else "Full package"}</div>
            <div class="text-lg font-bold text-[var(--accent)]"><bdi>{"از ۲۹,۰۰۰,۰۰۰ تومان" if is_rtl else "$1,800 package"}</bdi></div>
          </div>
        </div>
      </div>
    </section>

    <!-- Healthcare Section 2: Portfolio Before / After -->
    <section id="portfolio" class="mt-12 pt-8 border-t border-[var(--border-subtle)]" aria-labelledby="portfolio-heading">
      <div class="flex items-center justify-between mb-6">
        <div>
          <h2 id="portfolio-heading" class="text-2xl font-bold tracking-tight">{"نتایج مستند و گالری درمان ها" if is_rtl else "Clinical Before & After Gallery"}</h2>
          <p class="text-xs text-[var(--text-muted)] mt-1">{"نمونه درمان های انجام شده توسط متخصصین کلینیک با رضایت تایید شده مراجعین." if is_rtl else "Authentic outcomes documented with patient consent and verified results."}</p>
        </div>
        <div class="flex gap-2">
          <button type="button" class="portfolio-tab px-3 py-1.5 text-xs font-semibold rounded-[var(--radius-button)] bg-[var(--accent)] text-[var(--vibe-on-primary,#fff)] min-h-[44px]" data-view="before">{"تصویر قبل" if is_rtl else "Before"}</button>
          <button type="button" class="portfolio-tab px-3 py-1.5 text-xs font-semibold rounded-[var(--radius-button)] bg-[var(--canvas-bg)] border border-[var(--border-subtle)] hover:bg-[var(--surface-bg)] min-h-[44px]" data-view="after">{"نتیجه درمان" if is_rtl else "After Treatment"}</button>
        </div>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- Interactive Drag Slider Card 1 -->
        <div class="vibe-spotlight-card p-6 bg-[var(--surface-bg)] {card_border} rounded-[var(--radius-container)] {card_shadow} space-y-4">
          <div class="flex justify-between items-center text-xs font-semibold">
            <span>{"۱۰ واحد ونیر سرامیکی E-Max" if is_rtl else "10 Units E-Max Veneers"}</span>
            <span class="px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-500 font-mono text-[10px] font-bold"><bdi>98.4% Match</bdi></span>
          </div>
          <!-- Interactive Before / After Split Slider -->
          <div class="relative h-48 w-full rounded-[var(--radius-base)] overflow-hidden border border-[var(--border-subtle)] bg-[var(--canvas-bg)] select-none">
            <div class="absolute inset-0 bg-gradient-to-r from-stone-300 to-amber-100 dark:from-stone-800 dark:to-amber-950/40 flex items-center justify-start p-4">
              <span class="text-xs font-bold text-stone-500 uppercase tracking-widest">{"قبل از درمان" if is_rtl else "Baseline"}</span>
            </div>
            <div id="before-after-layer-1" class="absolute inset-y-0 end-0 bg-gradient-to-l from-emerald-100 to-rose-50 dark:from-emerald-950/40 dark:to-rose-950/20 border-s-2 border-emerald-500 flex items-center justify-end p-4 transition-all duration-75" style="width: 50%">
              <span class="text-xs font-bold text-emerald-700 dark:text-emerald-400 uppercase tracking-widest">{"نتیجه درمان" if is_rtl else "After Result"}</span>
            </div>
            <input type="range" min="0" max="100" value="50" class="before-after-range absolute inset-0 opacity-0 cursor-ew-resize w-full h-full z-20" data-target="before-after-layer-1" data-divider="divider-line-1" aria-label="Before and After Comparison Slider">
            <div id="divider-line-1" class="absolute inset-y-0 w-1 bg-white shadow-[0_0_10px_rgba(0,0,0,0.4)] pointer-events-none z-10 flex items-center justify-center" style="left: 50%">
              <div class="w-6 h-6 rounded-full bg-white dark:bg-zinc-900 border border-zinc-300 dark:border-zinc-700 shadow-md flex items-center justify-center">
                <svg class="w-3.5 h-3.5 text-zinc-500" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true"><polyline points="7 17 2 12 7 7"></polyline><polyline points="17 7 22 12 17 17"></polyline><line x1="2" y1="12" x2="22" y2="12"></line></svg>
              </div>
            </div>
          </div>
          <p class="text-xs text-[var(--text-muted)] text-center">{"دستگیره را بکشید تا تغییرات قبل و بعد از درمان را به صورت زنده مقایسه کنید." if is_rtl else "Drag the slider to compare baseline versus clinical post-treatment result."}</p>
        </div>

        <!-- Interactive Drag Slider Card 2 -->
        <div class="vibe-spotlight-card p-6 bg-[var(--surface-bg)] {card_border} rounded-[var(--radius-container)] {card_shadow} space-y-4">
          <div class="flex justify-between items-center text-xs font-semibold">
            <span>{"ایمپلنت فوری دندان جلو" if is_rtl else "Immediate Anterior Implant"}</span>
            <span class="px-2 py-0.5 rounded-full bg-sky-500/10 text-sky-500 font-mono text-[10px] font-bold"><bdi>100% Titanium Bond</bdi></span>
          </div>
          <!-- Interactive Before / After Split Slider -->
          <div class="relative h-48 w-full rounded-[var(--radius-base)] overflow-hidden border border-[var(--border-subtle)] bg-[var(--canvas-bg)] select-none">
            <div class="absolute inset-0 bg-gradient-to-r from-zinc-300 to-sky-100 dark:from-zinc-800 dark:to-sky-950/40 flex items-center justify-start p-4">
              <span class="text-xs font-bold text-zinc-500 uppercase tracking-widest">{"وضعیت اولیه" if is_rtl else "Baseline"}</span>
            </div>
            <div id="before-after-layer-2" class="absolute inset-y-0 end-0 bg-gradient-to-l from-sky-100 to-indigo-50 dark:from-sky-950/40 dark:to-indigo-950/20 border-s-2 border-sky-500 flex items-center justify-end p-4 transition-all duration-75" style="width: 50%">
              <span class="text-xs font-bold text-sky-700 dark:text-sky-400 uppercase tracking-widest">{"کاشت نهایی" if is_rtl else "Final Crown"}</span>
            </div>
            <input type="range" min="0" max="100" value="50" class="before-after-range absolute inset-0 opacity-0 cursor-ew-resize w-full h-full z-20" data-target="before-after-layer-2" data-divider="divider-line-2" aria-label="Before and After Comparison Slider">
            <div id="divider-line-2" class="absolute inset-y-0 w-1 bg-white shadow-[0_0_10px_rgba(0,0,0,0.4)] pointer-events-none z-10 flex items-center justify-center" style="left: 50%">
              <div class="w-6 h-6 rounded-full bg-white dark:bg-zinc-900 border border-zinc-300 dark:border-zinc-700 shadow-md flex items-center justify-center">
                <svg class="w-3.5 h-3.5 text-zinc-500" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true"><polyline points="7 17 2 12 7 7"></polyline><polyline points="17 7 22 12 17 17"></polyline><line x1="2" y1="12" x2="22" y2="12"></line></svg>
              </div>
            </div>
          </div>
          <p class="text-xs text-[var(--text-muted)] text-center">{"پایداری بی نقص بافت نرم لثه و انطباق کامل رنگ با دندان های مجاور." if is_rtl else "Painless placement with soft tissue graft and certified zirconia crown."}</p>
        </div>
      </div>
    </section>

    <!-- Healthcare Section 3: Specialist Doctors -->
    <section id="doctors" class="mt-12 pt-8 border-t border-[var(--border-subtle)]" aria-labelledby="doctors-heading">
      <h2 id="doctors-heading" class="text-2xl font-bold tracking-tight mb-6">{"تیم پزشکان و متخصصین کلینیک" if is_rtl else "Specialist Medical Staff"}</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div class="p-6 bg-[var(--surface-bg)] {card_border} rounded-[var(--radius-container)] {card_shadow} flex items-start gap-4">
          <div class="w-14 h-14 rounded-full bg-[var(--accent)]/10 text-[var(--accent)] flex items-center justify-center flex-shrink-0">
            <svg class="w-7 h-7" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>
          </div>
          <div class="space-y-1">
            <h3 class="text-lg font-bold">{"دکتر آریا پارسا" if is_rtl else "Dr. Aria Parsa, DDS"}</h3>
            <p class="text-xs text-[var(--accent)] font-semibold">{"متخصص دندانپزشکی ترمیمی و زیبایی | نظام پزشکی: ۱۴۸۲۹۱" if is_rtl else "Board Certified Aesthetic & Restorative Dentist"}</p>
            <p class="text-xs text-[var(--text-muted)] leading-relaxed mt-2">{"فلوشیپ بین المللی طراحی لبخند دیجیتال از دانشگاه زوریخ با بیش از ۱۲ سال تجربه تخصصی." if is_rtl else "International Fellow in Digital Smile Design with 12+ years clinical experience."}</p>
          </div>
        </div>
        <div class="p-6 bg-[var(--surface-bg)] {card_border} rounded-[var(--radius-container)] {card_shadow} flex items-start gap-4">
          <div class="w-14 h-14 rounded-full bg-[var(--accent)]/10 text-[var(--accent)] flex items-center justify-center flex-shrink-0">
            <svg class="w-7 h-7" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>
          </div>
          <div class="space-y-1">
            <h3 class="text-lg font-bold">{"دکتر سارا شمس" if is_rtl else "Dr. Sara Shams, MS"}</h3>
            <p class="text-xs text-[var(--accent)] font-semibold">{"جراح فک و متخصص ایمپلنت های دندانی | نظام پزشکی: ۱۵۳۸۲۰" if is_rtl else "Oral Surgeon & Digital Implantologist"}</p>
            <p class="text-xs text-[var(--text-muted)] leading-relaxed mt-2">{"رتبه برتر بورد تخصصی، عضو انجمن ایمپلنتولوژی اروپا (EAO) و مجری جراحی های با هدایت سه بعدی." if is_rtl else "European Association for Osseointegration member specializing in guided surgery."}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Healthcare Section 4: Interactive Quick Booking -->
    <section id="booking" class="mt-12 pt-8 border-t border-[var(--border-subtle)]" aria-labelledby="booking-heading">
      <div class="p-6 sm:p-10 bg-[var(--surface-bg)] {card_border} rounded-[var(--radius-container)] {card_shadow}">
        <h2 id="booking-heading" class="text-2xl font-bold tracking-tight mb-2">{"رزرو آنلاین نوبت معاینه و مشاوره" if is_rtl else "Book Online Consultation"}</h2>
        <p class="text-xs text-[var(--text-muted)] mb-6">{"روز و ساعت مورد نظر خود را انتخاب کنید تا نوبت اولیه شما به صورت اختصاصی ثبت شود." if is_rtl else "Select your preferred appointment date and time for priority confirmation."}</p>
        
        <form id="quick-booking-form" class="space-y-6">
          <!-- Day selector -->
          <div>
            <label class="block text-xs font-semibold mb-2">{"انتخاب روز ویزیت" if is_rtl else "Select Appointment Day"}</label>
            <div class="flex flex-wrap gap-2">
              <button type="button" class="day-slot-btn px-4 py-2 text-xs font-bold rounded-[var(--radius-button)] bg-[var(--accent)] text-[var(--vibe-on-primary,#fff)] min-h-[44px]">{"شنبه" if is_rtl else "Saturday"}</button>
              <button type="button" class="day-slot-btn px-4 py-2 text-xs font-bold rounded-[var(--radius-button)] bg-[var(--canvas-bg)] border border-[var(--border-subtle)] hover:bg-[var(--surface-bg)] min-h-[44px]">{"یکشنبه" if is_rtl else "Sunday"}</button>
              <button type="button" class="day-slot-btn px-4 py-2 text-xs font-bold rounded-[var(--radius-button)] bg-[var(--canvas-bg)] border border-[var(--border-subtle)] hover:bg-[var(--surface-bg)] min-h-[44px]">{"دوشنبه" if is_rtl else "Monday"}</button>
              <button type="button" class="day-slot-btn px-4 py-2 text-xs font-bold rounded-[var(--radius-button)] bg-[var(--canvas-bg)] border border-[var(--border-subtle)] hover:bg-[var(--surface-bg)] min-h-[44px]">{"سه شنبه" if is_rtl else "Tuesday"}</button>
            </div>
          </div>

          <!-- Time slot selector -->
          <div>
            <label class="block text-xs font-semibold mb-2">{"انتخاب بازه ساعتی" if is_rtl else "Select Time Window"}</label>
            <div class="flex flex-wrap gap-2">
              <button type="button" class="time-slot-btn px-4 py-2 text-xs font-bold rounded-[var(--radius-button)] bg-[var(--accent)] text-[var(--vibe-on-primary,#fff)] min-h-[44px]"><bdi>۱۰:۳۰</bdi></button>
              <button type="button" class="time-slot-btn px-4 py-2 text-xs font-bold rounded-[var(--radius-button)] bg-[var(--canvas-bg)] border border-[var(--border-subtle)] hover:bg-[var(--surface-bg)] min-h-[44px]"><bdi>۱۲:۰۰</bdi></button>
              <button type="button" class="time-slot-btn px-4 py-2 text-xs font-bold rounded-[var(--radius-button)] bg-[var(--canvas-bg)] border border-[var(--border-subtle)] hover:bg-[var(--surface-bg)] min-h-[44px]"><bdi>۱۶:۳۰</bdi></button>
              <button type="button" class="time-slot-btn px-4 py-2 text-xs font-bold rounded-[var(--radius-button)] bg-[var(--canvas-bg)] border border-[var(--border-subtle)] hover:bg-[var(--surface-bg)] min-h-[44px]"><bdi>۱۸:۰۰</bdi></button>
            </div>
          </div>

          <!-- Patient information -->
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label for="patient-name" class="block text-xs font-semibold mb-1">{"نام و نام خانوادگی مراجع" if is_rtl else "Patient Full Name"}</label>
              <input type="text" id="patient-name" required placeholder="{"مثال: سهراب سپهری" if is_rtl else "e.g. John Doe"}" class="w-full px-4 py-2.5 text-xs rounded-[var(--radius-button)] bg-[var(--canvas-bg)] border border-[var(--border-subtle)] focus:border-[var(--accent)] min-h-[44px] outline-none">
            </div>
            <div>
              <label for="patient-phone" class="block text-xs font-semibold mb-1">{"شماره تماس مستقیم" if is_rtl else "Mobile Phone Number"}</label>
              <input type="tel" id="patient-phone" required placeholder="{"۰۹۱۲۳۴۵۶۷۸۹" if is_rtl else "+1 (555) 000-0000"}" class="w-full px-4 py-2.5 text-xs rounded-[var(--radius-button)] bg-[var(--canvas-bg)] border border-[var(--border-subtle)] focus:border-[var(--accent)] min-h-[44px] outline-none">
            </div>
          </div>

          <div class="pt-2">
            <button type="submit" id="submit-booking-btn" class="w-full sm:w-auto inline-flex items-center justify-center px-8 py-3 text-sm font-semibold rounded-[var(--radius-button)] text-[var(--vibe-on-primary,#fff)] bg-[var(--accent)] hover:opacity-90 min-h-[44px] transition-all">
              {"ثبت قطعی و ارسال تاییدیه نوبت" if is_rtl else "Confirm & Reserve Appointment"}
            </button>
          </div>
        </form>
      </div>
    </section>
"""
        else:
            domain_sections_html = f"""
    <!-- General Section 1: Asymmetric Bento Grid Features -->
    <section id="features" class="mt-12 pt-8 border-t border-[var(--border-subtle)]" aria-labelledby="features-heading">
      <div class="flex items-center justify-between mb-8">
        <div>
          <h2 id="features-heading" class="text-2xl font-bold tracking-tight">
            {"معماری نوین و قابلیت های بنیادین" if is_rtl else "Engineered Capabilities & Bento Architecture"}
          </h2>
          <p class="text-xs text-[var(--text-muted)] mt-1">
            {"طراحی شده با استانداردهای مدرن فرانت اند، دسترسی پذیری کامل و سرعت بارگذاری آنی." if is_rtl else "Built with strict WCAG standards, fluid physics, and sub-millisecond execution."}
          </p>
        </div>
        <span class="hidden sm:inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-[var(--accent)]/10 text-[var(--accent)] border border-[var(--accent)]/20">
          <span class="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
          {"تاییدیه کیفی Vibe UI" if is_rtl else "Vibe UI 4.1.1 Certified"}
        </span>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <!-- Tile 1: Hero Bento Feature (Span 2) -->
        <div class="vibe-spotlight-card md:col-span-2 p-6 sm:p-8 bg-[var(--surface-bg)] {card_border} rounded-[var(--radius-container)] {card_shadow} flex flex-col justify-between">
          <div>
            <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-semibold bg-[var(--accent)]/10 text-[var(--accent)] mb-4">
              <svg class="w-4 h-4 text-[var(--accent)]" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>
              <span>{"تضمین کیفیت و اصالت مهندسی" if is_rtl else "Quality Guarantee & Core Engine"}</span>
            </div>
            <h3 class="text-xl font-bold mb-3">{"معماری استاندارد بدون کلیشه های هوش مصنوعی" if is_rtl else "Deterministic Architecture Free of AI-Slop"}</h3>
            <p class="text-xs sm:text-sm text-[var(--text-muted)] leading-relaxed max-w-xl">
              {"پایبندی به بالاترین معیارهای تخصصی، استانداردهای دسترسی پذیری نوری WCAG AAA و بهینه سازی ساختار یافته با حذف کدهای اضافه و انیمیشن های مزاحم." if is_rtl else "Engineered with strict accessibility, responsive geometry, zero inline CSS, and mathematically proven contrast ratios across light and dark modes."}
            </p>
          </div>
          <div class="mt-6 pt-4 border-t border-[var(--border-subtle)] flex flex-wrap items-center gap-3 text-xs text-[var(--text-muted)]">
            <span class="px-2.5 py-1 rounded-md bg-[var(--canvas-bg)] border border-[var(--border-subtle)] font-mono">OKLCH Palette</span>
            <span class="px-2.5 py-1 rounded-md bg-[var(--canvas-bg)] border border-[var(--border-subtle)] font-mono">BiDi Isolation</span>
            <span class="px-2.5 py-1 rounded-md bg-[var(--canvas-bg)] border border-[var(--border-subtle)] font-mono">0.01ms Motion Guards</span>
          </div>
        </div>

        <!-- Tile 2: Vital Metric KPI with Inline Sparkline (Span 1) -->
        <div class="vibe-spotlight-card p-6 bg-[var(--surface-bg)] {card_border} rounded-[var(--radius-container)] {card_shadow} flex flex-col justify-between">
          <div>
            <div class="text-xs font-semibold text-[var(--text-muted)] uppercase tracking-wider mb-2">{"پایداری و در دسترس بودن" if is_rtl else "Uptime & Reliability"}</div>
            <div class="text-3xl font-extrabold text-emerald-500 mb-2"><bdi>99.98%</bdi></div>
            <p class="text-xs text-[var(--text-muted)] leading-relaxed">
              {"پایش مداوم وضعیت سرویس و تضمین پایداری بدون وقفه در مقیاس بالا." if is_rtl else "Real-time health verification with automated self-healing resilience."}
            </p>
          </div>
          <!-- Inline Vector Sparkline -->
          <div class="mt-4 pt-4 border-t border-[var(--border-subtle)]">
            <svg class="w-full h-10 text-emerald-500" viewBox="0 0 120 30" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
              <path d="M0 25 L20 22 L40 24 L60 14 L80 16 L100 8 L120 6"></path>
              <circle cx="120" cy="6" r="3" fill="currentColor"></circle>
            </svg>
            <div class="flex justify-between text-[10px] text-[var(--text-muted)] mt-1 font-mono">
              <span>-30d</span>
              <span>Today: 100%</span>
            </div>
          </div>
        </div>

        <!-- Tile 3: Live Latency & Pulse Indicator (Span 1) -->
        <div class="vibe-spotlight-card p-6 bg-[var(--surface-bg)] {card_border} rounded-[var(--radius-container)] {card_shadow} flex flex-col justify-between">
          <div>
            <div class="w-10 h-10 rounded-lg bg-[var(--accent)]/10 text-[var(--accent)] flex items-center justify-center mb-4">
              <svg class="w-5 h-5 text-[var(--accent)]" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon></svg>
            </div>
            <h3 class="text-base font-bold mb-2">{"سرعت و سهولت کاربری" if is_rtl else "Speed & Precision"}</h3>
            <p class="text-xs text-[var(--text-muted)] leading-relaxed">
              {"طراحی شده برای بیشترین سرعت بارگذاری، سازگاری کامل با دستگاه های موبایل و رابط کاربری روان." if is_rtl else "Optimized for lightning-fast delivery, mobile ergonomics, and seamless user interaction."}
            </p>
          </div>
          <div class="mt-4 pt-3 border-t border-[var(--border-subtle)] flex items-center justify-between text-xs">
            <span class="text-[var(--text-muted)]">Response Time</span>
            <span class="font-mono font-bold text-[var(--accent)]">&lt; 0.4s</span>
          </div>
        </div>

        <!-- Tile 4: Governance & Certifications Bento Card (Span 2) -->
        <div class="vibe-spotlight-card md:col-span-2 p-6 bg-[var(--surface-bg)] {card_border} rounded-[var(--radius-container)] {card_shadow} flex flex-col justify-between">
          <div>
            <div class="w-10 h-10 rounded-lg bg-[var(--accent)]/10 text-[var(--accent)] flex items-center justify-center mb-4">
              <svg class="w-5 h-5 text-[var(--accent)]" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 14 14"></polyline></svg>
            </div>
            <h3 class="text-base font-bold mb-2">{"شفافیت و استاندارد سازمانی" if is_rtl else "Enterprise Governance & Security"}</h3>
            <p class="text-xs text-[var(--text-muted)] leading-relaxed">
              {"فرآیند پیگیری شفاف، پشتیبانی فعال و همراهی در تمامی مراحل استفاده از خدمات مطابق با بالاترین توافق نامه های سطح خدمات." if is_rtl else "Strict data retention policies, zero secrets leakage compliance, and verified enterprise security baselines."}
            </p>
          </div>
          <div class="mt-6 pt-4 border-t border-[var(--border-subtle)] grid grid-cols-2 sm:grid-cols-4 gap-2 text-[11px] font-medium text-[var(--text-muted)]">
            <div class="flex items-center gap-1.5"><svg class="w-3.5 h-3.5 text-emerald-500" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"></polyline></svg><span>WCAG AAA</span></div>
            <div class="flex items-center gap-1.5"><svg class="w-3.5 h-3.5 text-emerald-500" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"></polyline></svg><span>BiDi Isolated</span></div>
            <div class="flex items-center gap-1.5"><svg class="w-3.5 h-3.5 text-emerald-500" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"></polyline></svg><span>Zero Slop</span></div>
            <div class="flex items-center gap-1.5"><svg class="w-3.5 h-3.5 text-emerald-500" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"></polyline></svg><span>100% SVG</span></div>
          </div>
        </div>
      </div>
    </section>

    <!-- General Section 2: Services & Pricing -->
    <section id="services" class="mt-12 pt-8 border-t border-[var(--border-subtle)]" aria-labelledby="general-services-heading">
      <h2 id="general-services-heading" class="text-2xl font-bold tracking-tight mb-6">{"خدمات و پلن های تخصصی" if is_rtl else "Services & Architecture Plans"}</h2>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div class="p-6 bg-[var(--surface-bg)] {card_border} rounded-[var(--radius-container)] {card_shadow} space-y-3">
          <h3 class="text-lg font-bold">{"پلن استاندارد پایه" if is_rtl else "Core Essentials"}</h3>
          <p class="text-xs text-[var(--text-muted)]">{"مناسب شروع پروژه ها با ساختار استاندارد و دسترسی پذیری کامل." if is_rtl else "Complete foundational setup with certified WCAG compliance."}</p>
          <div class="text-2xl font-bold text-[var(--accent)]"><bdi>{"شروع رایگان" if is_rtl else "Open Source"}</bdi></div>
        </div>
        <div class="p-6 bg-[var(--surface-bg)] {card_border} rounded-[var(--radius-container)] {card_shadow} space-y-3 ring-2 ring-[var(--accent)]">
          <span class="inline-flex px-2 py-0.5 rounded text-xs font-bold bg-[var(--accent)] text-[var(--vibe-on-primary,#fff)]">RECOMMENDED</span>
          <h3 class="text-lg font-bold">{"پلن حرفه ای شرکتی" if is_rtl else "Professional Studio"}</h3>
          <p class="text-xs text-[var(--text-muted)]">{"به همراه کامپوننت های هوش مصنوعی، تله متری زنده و پشتیبانی ویژه." if is_rtl else "AI primitive components, spring physics & telemetry HUD."}</p>
          <div class="text-2xl font-bold text-[var(--accent)]"><bdi>{"تخصیص اختصاصی" if is_rtl else "Custom Tier"}</bdi></div>
        </div>
        <div class="p-6 bg-[var(--surface-bg)] {card_border} rounded-[var(--radius-container)] {card_shadow} space-y-3">
          <h3 class="text-lg font-bold">{"پلن سازمانی Enterprise" if is_rtl else "Enterprise Governance"}</h3>
          <p class="text-xs text-[var(--text-muted)]">{"قراردادهای ماشین دقیق، اعتبارسنجی استقرار و ممیزی های مستمر." if is_rtl else "Deterministic machine contracts, CI/CD integration & SLAs."}</p>
          <div class="text-2xl font-bold text-[var(--accent)]"><bdi>{"تماس با ما" if is_rtl else "Contact Sales"}</bdi></div>
        </div>
      </div>
    </section>

    <!-- General Section 3: Contact & Inquiry -->
    <section id="contact" class="mt-12 pt-8 border-t border-[var(--border-subtle)]" aria-labelledby="contact-heading">
      <div class="p-6 sm:p-10 bg-[var(--surface-bg)] {card_border} rounded-[var(--radius-container)] {card_shadow} max-w-2xl mx-auto">
        <h2 id="contact-heading" class="text-2xl font-bold tracking-tight mb-2">{"ارتباط و استقرار سریع" if is_rtl else "Quick Contact & Inquiry"}</h2>
        <p class="text-xs text-[var(--text-muted)] mb-6">{"پیام خود را ارسال کنید تا کارشناسان ما در سریع ترین زمان ممکن با شما گفتگو کنند." if is_rtl else "Leave your information and our engineering team will get back to you promptly."}</p>
        <form id="contact-form" class="space-y-4">
          <div>
            <label for="contact-name" class="block text-xs font-semibold mb-1">{"نام و نام خانوادگی" if is_rtl else "Full Name"}</label>
            <input type="text" id="contact-name" required placeholder="{"مثال: علی رضایی" if is_rtl else "e.g. Alex Miller"}" class="w-full px-4 py-2.5 text-xs rounded-[var(--radius-button)] bg-[var(--canvas-bg)] border border-[var(--border-subtle)] focus:border-[var(--accent)] min-h-[44px] outline-none">
          </div>
          <div>
            <label for="contact-email" class="block text-xs font-semibold mb-1">{"آدرس ایمیل یا شماره تماس" if is_rtl else "Email or Phone Number"}</label>
            <input type="text" id="contact-email" required placeholder="{"info@example.com" if is_rtl else "user@company.com"}" class="w-full px-4 py-2.5 text-xs rounded-[var(--radius-button)] bg-[var(--canvas-bg)] border border-[var(--border-subtle)] focus:border-[var(--accent)] min-h-[44px] outline-none">
          </div>
          <div class="pt-2">
            <button type="submit" id="submit-contact-btn" class="w-full sm:w-auto inline-flex items-center justify-center px-8 py-3 text-sm font-semibold rounded-[var(--radius-button)] text-[var(--vibe-on-primary,#fff)] bg-[var(--accent)] hover:opacity-90 min-h-[44px] transition-all">
              {"ارسال پیام و استقرار" if is_rtl else "Submit Request"}
            </button>
          </div>
        </form>
      </div>
    </section>
"""

        html = f"""<!DOCTYPE html>
<html {dir_attr} data-domain="{domain_id}" class="h-full">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{hero_headline}</title>
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

    /* Masterpiece Visual Engine: Atmospheric Lighting & Specular Physics */
    .vibe-gradient-heading {{
      background: linear-gradient(180deg, var(--text-primary) 0%, color-mix(in oklch, var(--text-primary) 72%, transparent) 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }}

    .vibe-spotlight-card {{
      position: relative;
      overflow: hidden;
      transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    }}

    .vibe-spotlight-card::before {{
      content: '';
      position: absolute;
      inset: 0;
      top: 0;
      height: 1px;
      background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.22), transparent);
      z-index: 10;
      pointer-events: none;
    }}

    .vibe-spotlight-card::after {{
      content: '';
      position: absolute;
      inset: 0;
      border-radius: inherit;
      background: radial-gradient(450px circle at var(--mouse-x, 50%) var(--mouse-y, 50%), color-mix(in oklch, var(--accent) 10%, transparent), transparent 75%);
      pointer-events: none;
      opacity: 0;
      transition: opacity 0.35s ease;
      z-index: 5;
    }}

    .vibe-spotlight-card:hover::after {{
      opacity: 1;
    }}

    .vibe-shimmer-btn {{
      position: relative;
      overflow: hidden;
      transition: transform 0.2s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    }}

    .vibe-shimmer-btn:hover {{
      box-shadow: 0 0 25px -4px var(--accent);
    }}

    .vibe-shimmer-btn:active {{
      transform: scale(0.98);
    }}

    .vibe-shimmer-btn::after {{
      content: '';
      position: absolute;
      top: 0;
      left: -100%;
      width: 60%;
      height: 100%;
      background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.28), transparent);
      transform: skewX(-20deg);
      transition: none;
      pointer-events: none;
    }}

    .vibe-shimmer-btn:hover::after {{
      left: 140%;
      transition: left 0.75s ease-in-out;
    }}

    /* Lightswind Trailing Arrow Pointer & Spotlight Physics */
    @media (pointer: fine) {{
      #vibeCursorDot {{
        position: fixed;
        top: 0;
        left: 0;
        width: 8px;
        height: 8px;
        background-color: var(--accent);
        border-radius: 9999px;
        pointer-events: none;
        z-index: 10000;
        transform: translate(-50%, -50%);
        transition: opacity 0.2s ease;
      }}
      #vibeCursorFollower {{
        position: fixed;
        top: 0;
        left: 0;
        pointer-events: none;
        z-index: 9999;
        will-change: transform;
        color: var(--accent);
        filter: drop-shadow(0 0 10px color-mix(in oklch, var(--accent) 55%, transparent));
        transition: opacity 0.25s ease;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
      }}
      #vibeCursorFollower svg {{
        width: 36px;
        height: 39px;
        display: block;
        transition: transform 0.2s cubic-bezier(0.16, 1, 0.3, 1);
      }}
      #vibeCursorFollower.hover-active svg {{
        transform: scale(1.2);
      }}
      #vibeCursorFollower.click-active svg {{
        transform: scale(0.85);
      }}
      #vibeCursorBadge {{
        position: absolute;
        top: 100%;
        margin-top: 4px;
        padding: 2px 7px;
        border-radius: 9999px;
        background-color: var(--surface-bg);
        border: 1px solid var(--border-subtle);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        font-family: var(--font-body);
        font-size: 9px;
        font-weight: 800;
        color: var(--accent);
        letter-spacing: 0.05em;
        opacity: 0;
        transform: scale(0.85);
        transition: opacity 0.2s ease, transform 0.2s ease;
        white-space: nowrap;
      }}
      #vibeCursorFollower.hover-active #vibeCursorBadge {{
        opacity: 1;
        transform: scale(1);
      }}
    }}

    .ambient-spotlight-layer {{
      position: fixed;
      inset: 0;
      pointer-events: none;
      z-index: 1;
      background: radial-gradient(550px circle at var(--mouse-x, 50%) var(--mouse-y, 50%), color-mix(in oklch, var(--accent) 6%, transparent), transparent 70%);
      transition: opacity 0.3s ease;
    }}
  </style>
</head>
<body class="min-h-full flex flex-col antialiased relative">
  <!-- Lightswind Trailing Arrow Pointer -->
  <div id="vibeCursorDot" class="hidden md:block" aria-hidden="true"></div>
  <div id="vibeCursorFollower" class="hidden md:flex" aria-hidden="true">
    <svg xmlns="http://www.w3.org/2000/svg" width="36" height="39" viewBox="0 0 50 54" fill="none" class="pointer-events-none drop-shadow-md">
      <path d="M42.6817 41.1495L27.5103 6.79925C26.7269 5.02557 24.2082 5.02558 23.3927 6.79925L7.59814 41.1495C6.75833 42.9759 8.52712 44.8902 10.4125 44.1954L24.3757 39.0496C24.8829 38.8627 25.4385 38.8627 25.9422 39.0496L39.8121 44.1954C41.6849 44.8902 43.4884 42.9759 42.6817 41.1495Z" fill="currentColor"/>
      <path d="M43.7146 40.6933L28.5431 6.34306C27.3556 3.65428 23.5772 3.69516 22.3668 6.32755L6.57226 40.6778C5.3134 43.4156 7.97238 46.298 10.803 45.2549L24.7662 40.109C25.0221 40.0147 25.2999 40.0156 25.5494 40.1082L39.4193 45.254C42.2261 46.2953 44.9254 43.4347 43.7146 40.6933Z" stroke="currentColor" stroke-width="1.5"/>
    </svg>
    <span id="vibeCursorBadge"></span>
  </div>

  <!-- Ambient Cursor Spotlight Overlay -->
  <div id="ambientSpotlightOverlay" class="ambient-spotlight-layer" aria-hidden="true"></div>

  <!-- Atmospheric Canvas Background: Ambient Lighting & Grid System -->
  <div class="fixed inset-0 pointer-events-none z-0 overflow-hidden" aria-hidden="true">
    <div class="absolute inset-0 bg-[linear-gradient(to_right,rgba(128,128,128,0.06)_1px,transparent_1px),linear-gradient(to_bottom,rgba(128,128,128,0.06)_1px,transparent_1px)] bg-[size:36px_36px] [mask-image:radial-gradient(ellipse_60%_50%_at_50%_0%,#000_70%,transparent_100%)]"></div>
    <div class="absolute -top-32 start-1/2 -translate-x-1/2 rtl:translate-x-1/2 w-[760px] h-[520px] bg-[var(--accent)]/[0.08] blur-[140px] rounded-full"></div>
  </div>

  <!-- Top Navigation Bar -->
  <header class="w-full border-b border-[var(--border-subtle)] bg-[var(--surface-bg)]/85 backdrop-blur-md sticky top-0 z-30">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
      <div class="flex items-center space-x-3 rtl:space-x-reverse">
        <svg class="w-8 h-8 text-[var(--accent)]" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
          <polygon points="12 2 2 7 12 12 22 7 12 2"></polygon>
          <polyline points="2 17 12 22 22 17"></polyline>
          <polyline points="2 12 12 17 22 12"></polyline>
        </svg>
        <span class="text-xl font-bold tracking-tight display-font">{brand_name}</span>
      </div>
      <nav class="hidden md:flex items-center space-x-6 rtl:space-x-reverse" aria-label="Main Navigation">
{nav_links_html}
      </nav>
      <div class="flex items-center space-x-3 rtl:space-x-reverse">
        <button type="button" id="header-cta-btn" class="inline-flex items-center justify-center px-4 py-2.5 text-sm font-medium rounded-[var(--radius-button)] text-[var(--vibe-on-primary,#fff)] bg-[var(--accent)] hover:opacity-90 min-h-[44px] min-w-[44px] transition-all">
          {cta_primary_label}
        </button>
      </div>
    </div>
  </header>

  <!-- Main Hero & Content Section -->
  <main class="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-12 lg:py-16 relative z-10">
    <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-stretch">
      <!-- Main Bento Hero Card with Asymmetric Layout -->
      <section class="vibe-spotlight-card lg:col-span-7 bg-[var(--surface-bg)] {card_border} {card_shadow} rounded-[var(--radius-container)] p-6 sm:p-8 lg:p-10 flex flex-col justify-between" aria-labelledby="hero-title">
        <div>
          <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-semibold bg-[var(--accent)]/10 text-[var(--accent)] border border-[var(--accent)]/20 mb-4 shadow-sm">
            <span class="relative flex h-2 w-2">
              <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              <span class="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
            </span>
            <span>{"مهندسی دقیق و اصیل" if is_rtl else "Vibe UI Verified"}</span>
          </div>
          <h1 id="hero-title" class="text-3xl sm:text-4xl lg:text-5xl font-extrabold tracking-tight mb-4 vibe-gradient-heading">
            {hero_headline}
          </h1>
          <p class="text-[var(--text-muted)] text-base sm:text-lg leading-relaxed max-w-2xl mb-8">
            {hero_subheadline}
          </p>
        </div>

        <div class="flex flex-wrap gap-4 items-center pt-4 border-t border-[var(--border-subtle)]">
          <button type="button" id="hero-primary-btn" class="vibe-shimmer-btn inline-flex items-center justify-center px-6 py-3 text-base font-semibold rounded-[var(--radius-button)] text-[var(--vibe-on-primary,#fff)] bg-[var(--accent)] min-h-[44px]">
            {cta_primary_label}
          </button>
          <button type="button" id="hero-secondary-btn" class="inline-flex items-center justify-center px-6 py-3 text-base font-semibold rounded-[var(--radius-button)] text-[var(--text-primary)] border border-[var(--border-subtle)] bg-[var(--canvas-bg)] hover:bg-[var(--surface-bg)] min-h-[44px] transition-all hover:scale-[1.02] active:scale-[0.98]">
            {cta_secondary_label}
          </button>
        </div>
      </section>

      <!-- Secondary Domain Highlights: Ultra-Crisp macOS Window Chrome Mockup -->
      <aside class="vibe-spotlight-card lg:col-span-5 bg-[var(--surface-bg)] {card_border} {card_shadow} rounded-[var(--radius-container)] overflow-hidden flex flex-col justify-between" aria-label="Domain Highlights">
        <!-- Window Chrome Titlebar -->
        <div class="px-4 py-3 bg-[var(--canvas-bg)]/80 border-b border-[var(--border-subtle)] flex items-center justify-between backdrop-blur-md">
          <div class="flex items-center space-x-2 rtl:space-x-reverse">
            <span class="w-3 h-3 rounded-full bg-rose-500/80 inline-block border border-rose-600/40"></span>
            <span class="w-3 h-3 rounded-full bg-amber-500/80 inline-block border border-amber-600/40"></span>
            <span class="w-3 h-3 rounded-full bg-emerald-500/80 inline-block border border-emerald-600/40"></span>
          </div>
          <div class="text-[11px] font-mono text-[var(--text-muted)] flex items-center gap-1.5 opacity-80">
            <svg class="w-3.5 h-3.5 text-[var(--accent)]" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg>
            <span>{domain_id}.vibe // live</span>
          </div>
          <div class="flex items-center space-x-1.5 rtl:space-x-reverse">
            <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-ping"></span>
            <span class="text-[10px] font-mono text-emerald-500 font-semibold uppercase">SECURE</span>
          </div>
        </div>

        <div class="p-6 flex-1 flex flex-col justify-between">
          <div>
            <h2 class="text-base font-bold mb-4 flex items-center space-x-2 rtl:space-x-reverse">
              <svg class="w-4 h-4 text-[var(--accent)]" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M22 12h-4l-3 9L9 3l-3 9H2"></path></svg>
              <span>{"شاخص های کلیدی و وضعیت" if is_rtl else "Highlights & Status"}</span>
            </h2>
{window_chrome_content_html}
          </div>
          <div class="mt-6 pt-4 border-t border-[var(--border-subtle)] text-xs text-[var(--text-muted)] flex items-center justify-between">
            <div class="flex items-center space-x-1.5 rtl:space-x-reverse">
              <span class="w-2 h-2 rounded-full bg-emerald-500"></span>
              <span>{"سرویس آنلاین و آماده پذیرش" if is_rtl else "Active & Ready"}</span>
            </div>
            <span class="font-mono text-[10px] opacity-70"><bdi>99.99% SLO</bdi></span>
          </div>
        </div>
      </aside>
    </div>

{domain_sections_html}
  </main>

  <footer class="w-full border-t border-[var(--border-subtle)] bg-[var(--surface-bg)] py-6 mt-12">
    <div class="max-w-7xl mx-auto px-4 text-center text-xs text-[var(--text-muted)]">
      &copy; 2026 {brand_name}. {"تمامی حقوق محفوظ است." if is_rtl else "All rights reserved."}
    </div>
  </footer>

  <!-- Interactive Client-side Script (Zero Dead Buttons & Zero Broken Anchors) -->
  <script>
    (function() {{
      // 1. Toast Notification Utility
      function showToast(message) {{
        let toast = document.getElementById('vibe-toast');
        if (!toast) {{
          toast = document.createElement('div');
          toast.id = 'vibe-toast';
          toast.setAttribute('role', 'status');
          toast.setAttribute('aria-live', 'polite');
          toast.className = 'fixed bottom-5 end-5 z-50 px-5 py-3 rounded-lg shadow-xl text-xs font-semibold transition-all transform duration-300 opacity-0 translate-y-2 pointer-events-none border';
          document.body.appendChild(toast);
        }}
        toast.style.backgroundColor = 'var(--surface-bg)';
        toast.style.color = 'var(--text-primary)';
        toast.style.borderColor = 'var(--accent)';
        toast.textContent = message;
        toast.classList.remove('opacity-0', 'translate-y-2', 'pointer-events-none');
        setTimeout(function() {{
          toast.classList.add('opacity-0', 'translate-y-2', 'pointer-events-none');
        }}, 3500);
      }}

      // 2. Smooth Scrolling for all Internal Anchors
      document.querySelectorAll('a[href^="#"]').forEach(function(anchor) {{
        anchor.addEventListener('click', function(e) {{
          var targetId = anchor.getAttribute('href');
          var targetEl = document.querySelector(targetId);
          if (targetEl) {{
            e.preventDefault();
            targetEl.scrollIntoView({{ behavior: 'smooth' }});
          }}
        }});
      }});

      // 3. Header & Hero CTAs
      var headerCta = document.getElementById('header-cta-btn');
      var heroPrimary = document.getElementById('hero-primary-btn');
      var heroSecondary = document.getElementById('hero-secondary-btn');

      if (headerCta) {{
        headerCta.addEventListener('click', function() {{
          var bookingEl = document.getElementById('booking') || document.getElementById('services') || document.getElementById('contact');
          if (bookingEl) bookingEl.scrollIntoView({{ behavior: 'smooth' }});
          else showToast('{cta_primary_label} - Active');
        }});
      }}
      if (heroPrimary) {{
        heroPrimary.addEventListener('click', function() {{
          var bookingEl = document.getElementById('booking') || document.getElementById('services') || document.getElementById('contact');
          if (bookingEl) bookingEl.scrollIntoView({{ behavior: 'smooth' }});
          else showToast('{cta_primary_label} - Started');
        }});
      }}
      if (heroSecondary) {{
        heroSecondary.addEventListener('click', function() {{
          var targetEl = document.getElementById('portfolio') || document.getElementById('services') || document.getElementById('features') || document.getElementById('cluster');
          if (targetEl) targetEl.scrollIntoView({{ behavior: 'smooth' }});
          else showToast('{cta_secondary_label}');
        }});
      }}

      // 4. Interactive Action Buttons
      document.querySelectorAll('.btn-action').forEach(function(btn) {{
        btn.addEventListener('click', function() {{
          showToast('Telemetry traces inspection opened.');
        }});
      }});

      // 5. Booking Day & Time Slot Selection
      document.querySelectorAll('.day-slot-btn').forEach(function(btn) {{
        btn.addEventListener('click', function() {{
          document.querySelectorAll('.day-slot-btn').forEach(function(b) {{
            b.className = 'day-slot-btn px-4 py-2 text-xs font-bold rounded-[var(--radius-button)] bg-[var(--canvas-bg)] border border-[var(--border-subtle)] hover:bg-[var(--surface-bg)] min-h-[44px]';
          }});
          btn.className = 'day-slot-btn px-4 py-2 text-xs font-bold rounded-[var(--radius-button)] bg-[var(--accent)] text-[var(--vibe-on-primary,#fff)] min-h-[44px]';
        }});
      }});

      document.querySelectorAll('.time-slot-btn').forEach(function(btn) {{
        btn.addEventListener('click', function() {{
          document.querySelectorAll('.time-slot-btn').forEach(function(b) {{
            b.className = 'time-slot-btn px-4 py-2 text-xs font-bold rounded-[var(--radius-button)] bg-[var(--canvas-bg)] border border-[var(--border-subtle)] hover:bg-[var(--surface-bg)] min-h-[44px]';
          }});
          btn.className = 'time-slot-btn px-4 py-2 text-xs font-bold rounded-[var(--radius-button)] bg-[var(--accent)] text-[var(--vibe-on-primary,#fff)] min-h-[44px]';
        }});
      }});

      // 6. Portfolio Before/After Tab Switching
      document.querySelectorAll('.portfolio-tab').forEach(function(tab) {{
        tab.addEventListener('click', function() {{
          var view = tab.getAttribute('data-view');
          document.querySelectorAll('.portfolio-tab').forEach(function(t) {{
            t.className = 'portfolio-tab px-3 py-1.5 text-xs font-semibold rounded-[var(--radius-button)] bg-[var(--canvas-bg)] border border-[var(--border-subtle)] hover:bg-[var(--surface-bg)] min-h-[44px]';
          }});
          tab.className = 'portfolio-tab px-3 py-1.5 text-xs font-semibold rounded-[var(--radius-button)] bg-[var(--accent)] text-[var(--vibe-on-primary,#fff)] min-h-[44px]';
          showToast(view === 'before' ? 'نمایش تصاویر قبل از درمان' : 'نمایش نتایج نهایی پس از اتمام درمان');
        }});
      }});

      // 6.5. Interactive Before/After Split Comparison Sliders
      document.querySelectorAll('.before-after-range').forEach(function(slider) {{
        slider.addEventListener('input', function(e) {{
          var targetId = slider.getAttribute('data-target');
          var dividerId = slider.getAttribute('data-divider');
          var targetEl = document.getElementById(targetId);
          var dividerEl = document.getElementById(dividerId);
          var val = e.target.value;
          if (targetEl) targetEl.style.width = (100 - val) + '%';
          if (dividerEl) dividerEl.style.left = val + '%';
        }});
      }});

      // 7. DevOps Log Stream Toggle & Copy
      var streamToggle = document.getElementById('toggle-log-stream');
      if (streamToggle) {{
        var isStreaming = true;
        streamToggle.addEventListener('click', function() {{
          isStreaming = !isStreaming;
          streamToggle.textContent = isStreaming ? 'Pause Stream' : 'Resume Stream';
          showToast(isStreaming ? 'Live log telemetry resumed' : 'Log stream paused for inspection');
        }});
      }}
      var copyCurlBtn = document.getElementById('copy-curl-btn');
      if (copyCurlBtn) {{
        copyCurlBtn.addEventListener('click', function() {{
          showToast('curl command copied to clipboard');
        }});
      }}

      // 8. Forms Submission with Feedback
      var bookingForm = document.getElementById('quick-booking-form');
      if (bookingForm) {{
        bookingForm.addEventListener('submit', function(e) {{
          e.preventDefault();
          showToast('درخواست نوبت شما با موفقیت ثبت شد. مشاوران کلینیک به زودی با شما تماس خواهند گرفت.');
          bookingForm.reset();
        }});
      }}

      var contactForm = document.getElementById('contact-form');
      if (contactForm) {{
        contactForm.addEventListener('submit', function(e) {{
          e.preventDefault();
          showToast('درخواست شما با موفقیت ارسال شد. کارشناسان ما به زودی با شما تماس می گیرند.');
          contactForm.reset();
        }});
      }}

      // 9. Mouse-tracking Spotlight Cards (Guarded for Mobile Performance)
      if (window.matchMedia('(hover: hover) and (pointer: fine)').matches) {{
        document.querySelectorAll('.vibe-spotlight-card').forEach(function(card) {{
          card.addEventListener('mousemove', function(e) {{
            var rect = card.getBoundingClientRect();
            var x = e.clientX - rect.left;
            var y = e.clientY - rect.top;
            card.style.setProperty('--mouse-x', x + 'px');
            card.style.setProperty('--mouse-y', y + 'px');
          }});
        }});
      }}

      // 10. Lightswind Kinetic Trailing Arrow Pointer Engine
      var cursorDot = document.getElementById('vibeCursorDot');
      var cursorFollower = document.getElementById('vibeCursorFollower');
      var cursorBadge = document.getElementById('vibeCursorBadge');

      if (cursorDot && cursorFollower && window.matchMedia('(pointer: fine)').matches) {{
        var mouseX = window.innerWidth / 2;
        var mouseY = window.innerHeight / 2;
        var prevMouseX = mouseX;
        var prevMouseY = mouseY;
        var followerX = mouseX;
        var followerY = mouseY;
        var currentAngle = 0;
        var targetAngle = 0;
        var cursorVisible = false;

        window.addEventListener('pointermove', function(e) {{
          mouseX = e.clientX;
          mouseY = e.clientY;
          if (!cursorVisible) {{
            cursorVisible = true;
            cursorDot.style.opacity = '1';
            cursorFollower.style.opacity = '1';
          }}
          cursorDot.style.transform = 'translate(' + mouseX + 'px, ' + mouseY + 'px) translate(-50%, -50%)';
          document.documentElement.style.setProperty('--mouse-x', mouseX + 'px');
          document.documentElement.style.setProperty('--mouse-y', mouseY + 'px');
        }});

        document.addEventListener('mouseleave', function() {{
          cursorVisible = false;
          cursorDot.style.opacity = '0';
          cursorFollower.style.opacity = '0';
        }});

        document.addEventListener('mousedown', function() {{
          cursorFollower.classList.add('click-active');
        }});
        document.addEventListener('mouseup', function() {{
          cursorFollower.classList.remove('click-active');
        }});

        function renderKineticFollower() {{
          var vx = mouseX - followerX;
          var vy = mouseY - followerY;
          followerX += vx * 0.18;
          followerY += vy * 0.18;

          var dx = mouseX - prevMouseX;
          var dy = mouseY - prevMouseY;
          var speed = Math.hypot(dx, dy);

          if (speed > 1.2) {{
            targetAngle = Math.atan2(dy, dx) * (180 / Math.PI) + 90;
            var diff = targetAngle - currentAngle;
            if (diff > 180) diff -= 360;
            if (diff < -180) diff += 360;
            currentAngle += diff * 0.22;
          }}
          prevMouseX = mouseX;
          prevMouseY = mouseY;

          cursorFollower.style.transform = 'translate(' + followerX.toFixed(2) + 'px, ' + followerY.toFixed(2) + 'px) translate(-50%, -50%) rotate(' + currentAngle.toFixed(2) + 'deg)';
          requestAnimationFrame(renderKineticFollower);
        }}
        requestAnimationFrame(renderKineticFollower);

        document.querySelectorAll('a, button, input, .vibe-spotlight-card').forEach(function(el) {{
          el.addEventListener('pointerenter', function() {{
            cursorFollower.classList.add('hover-active');
            if (cursorBadge) {{
              if (el.tagName.toLowerCase() === 'button') cursorBadge.textContent = 'ACTIVATE';
              else if (el.tagName.toLowerCase() === 'a') cursorBadge.textContent = 'EXPLORE';
              else cursorBadge.textContent = 'VIEW';
            }}
          }});
          el.addEventListener('pointerleave', function() {{
            cursorFollower.classList.remove('hover-active');
            if (cursorBadge) cursorBadge.textContent = '';
          }});
        }});
      }}
    }})();
  </script>
</body>
</html>
"""
        return html
