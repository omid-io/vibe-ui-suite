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
import re
from vibe_core.genome import DesignGenomeEngine
from vibe_core.asset_director import AssetDirector
from vibe_core.domain_widgets import render_domain_widget
from vibe_core.sections_compiler import compile_domain_sections, get_domain_nav_links

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

# Curated Domain Canonical Brands (en, fa) to eliminate raw user prompt leakage into brand names
DOMAIN_CANONICAL_BRANDS: Dict[str, Dict[str, str]] = {
    "food_restaurant_cafe": {"en": "L'Artisan Bistro", "fa": "کافه رستوران نارنج"},
    "fintech_banking": {"en": "Aura Wealth", "fa": "مدیریت سرمایه آئورا"},
    "crypto_trading_web3": {"en": "Nexus Exchange", "fa": "صرافی نکسوس"},
    "devops_cloud_terminal": {"en": "OpsCore Command", "fa": "آپزکور"},
    "saas_b2b_enterprise": {"en": "Stratum Enterprise", "fa": "استراتوم"},
    "ai_developer_platform": {"en": "Cognition Studio", "fa": "استودیو شناختی هوش مصنوعی"},
    "ecommerce_luxury_fashion": {"en": "Maison Atelier", "fa": "مزون آتلیه"},
    "ecommerce_mass_market": {"en": "OmniStore", "fa": "فروشگاه آنلاین اومنی"},
    "real_estate_architecture": {"en": "Archstone Realty", "fa": "املاک آرچ‌استون"},
    "healthcare_hospital_medical": {"en": "Apex Health Clinic", "fa": "کلینیک جامع سلامت"},
    "education_edtech_lms": {"en": "Skillforge Academy", "fa": "آکادمی مهارت‌آموزی"},
    "creative_portfolio_agency": {"en": "Vanguard Studio", "fa": "استودیو پیشرو"},
    "media_editorial_magazine": {"en": "The Chronos Review", "fa": "نشریه کرونوس"},
    "beauty_clinical_wellness": {"en": "Lumina Dermal Care", "fa": "کلینیک لومینا"},
    "travel_hospitality_tourism": {"en": "Wanderlust Retreats", "fa": "اقامتگاه‌های وندرلاست"},
    "legal_compliance_law": {"en": "Veritas Law Partners", "fa": "موسسه حقوقی وریتاس"},
    "gaming_entertainment_streaming": {"en": "Vortex Gaming", "fa": "ورتکس گیمینگ"},
    "automotive_ev_mobility": {"en": "VoltDynamics Mobility", "fa": "ولت داینامیکس"},
    "logistics_supply_chain": {"en": "FreightFlow Global", "fa": "سامانه لجستیک فریت‌فلو"},
    "energy_greentech_sustainability": {"en": "Verdant Energy", "fa": "انرژی سبز وردانت"},
    "nonprofit_charity_social": {"en": "Compassion Foundation", "fa": "بنیاد نیکوکاری همیاران"},
    "personal_branding_creator": {"en": "Apex Athletic Lab", "fa": "استودیو ورزشی اپکس"},
    "cybersecurity_identity_auth": {"en": "CipherShield Zero-Trust", "fa": "امنیت سایبری سایفرشیلد"},
    "general_modern_saas": {"en": "Vibe Modern Platform", "fa": "سامانه مدرن وایب"}
}

# Curated Domain Canonical Badges (en, fa) to purge framework telemetry badges ("Vibe UI Verified")
DOMAIN_CANONICAL_BADGES: Dict[str, Dict[str, str]] = {
    "food_restaurant_cafe": {"en": "Curated Culinary Experience", "fa": "طعم و کیفیت برگزیده"},
    "fintech_banking": {"en": "Institutional Grade Security", "fa": "امنیت و اعتبار مالی"},
    "crypto_trading_web3": {"en": "Real-Time Liquidity Mesh", "fa": "نقدینگی لحظه‌ای و امن"},
    "devops_cloud_terminal": {"en": "Live Cluster Ingress", "fa": "سامانه مانیتورینگ زنده"},
    "saas_b2b_enterprise": {"en": "Enterprise Cloud Platform", "fa": "سامانه ابری سازمانی"},
    "ai_developer_platform": {"en": "Autonomous Intelligence Engine", "fa": "موتور مدل‌های هوش مصنوعی"},
    "ecommerce_luxury_fashion": {"en": "Limited Haute Couture", "fa": "مجموعه اختصاصی لوکس"},
    "ecommerce_mass_market": {"en": "Verified Merchant Guarantee", "fa": "ضمانت اصالت و سلامت کالا"},
    "real_estate_architecture": {"en": "Prime Architectural Properties", "fa": "املاک و ویلاهای برتر"},
    "healthcare_hospital_medical": {"en": "Board-Certified Specialists", "fa": "کادر فوق تخصصی پزشکی"},
    "education_edtech_lms": {"en": "Accredited Curriculum", "fa": "دوره‌های تایید شده آموزشی"},
    "creative_portfolio_agency": {"en": "Award-Winning Creative Studio", "fa": "استودیو طراحی خلاق"},
    "media_editorial_magazine": {"en": "In-Depth Investigative Journalism", "fa": "گزارش‌های تحلیلی و تخصصی"},
    "beauty_clinical_wellness": {"en": "Clinical Aesthetics Certified", "fa": "خدمات تخصصی پوست و زیبایی"},
    "travel_hospitality_tourism": {"en": "Handpicked Boutique Escapes", "fa": "اقامتگاه‌های بومگردی منتخب"},
    "legal_compliance_law": {"en": "Confidential Legal Counsel", "fa": "مشاوره تخصصی حقوقی"},
    "gaming_entertainment_streaming": {"en": "Ultra-Low Latency Engine", "fa": "سرورهای فوق سریع گیمینگ"},
    "automotive_ev_mobility": {"en": "Next-Gen EV Powertrain", "fa": "فناوری پیشرفته خودرو برقی"},
    "logistics_supply_chain": {"en": "Autonomous Route Intelligence", "fa": "شبکه هوشمند حمل‌ونقل"},
    "energy_greentech_sustainability": {"en": "Zero-Emission Certified", "fa": "گواهی انرژی پاک و پایدار"},
    "nonprofit_charity_social": {"en": "100% Transparent Aid Delivery", "fa": "کمک‌رسانی شفاف و مستقیم"},
    "personal_branding_creator": {"en": "Elite Athlete & Performance Lab", "fa": "تمرینات تخصصی و مربیگری حرفه‌ای"},
    "cybersecurity_identity_auth": {"en": "FIDO2 & Zero-Trust Certified", "fa": "استاندارد احراز هویت امن"},
    "general_modern_saas": {"en": "Production-Grade Platform", "fa": "کیفیت و عملکرد استاندارد"}
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
                <span className="text-xs font-medium text-zinc-500">Monthly</span>
                <button
                  type="button"
                  role="switch"
                  aria-checked={{billingCycle === "annual"}}
                  aria-label="Billing cycle toggle"
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
                  <span>Annual</span>
                  <span className="px-2 py-0.5 text-[10px] font-bold rounded-full bg-emerald-500/10 text-emerald-600 border border-emerald-500/20">
                    Save 20%
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
                Exclusive Curated Spread
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
                3 Step Transactional Flow
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
                1. Configure Inputs
              </div>
              <div className="p-3 rounded-xl bg-zinc-100 dark:bg-zinc-800/60 border border-zinc-200 dark:border-zinc-700 text-zinc-600 dark:text-zinc-300">
                2. Real-Time Simulation
              </div>
              <div className="p-3 rounded-xl bg-zinc-100 dark:bg-zinc-800/60 border border-zinc-200 dark:border-zinc-700 text-zinc-600 dark:text-zinc-300">
                3. Instant Execution
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
                  Creative Canvas Showcase
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
                  RESEARCH LAB & DIAGNOSTIC STUDIO
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

    def generate(
        self,
        decision_or_intent: Dict[str, Any],
        decision_opt: Optional[Dict[str, Any]] = None,
        format_type: str = "html",
        **kwargs
    ) -> str:
        """
        Universal generation method dispatching to generate_html or generate_react_tsx.
        Accepts either (intent), (decision), or (intent, decision).
        """
        decision = decision_opt or decision_or_intent
        # If raw intent was passed, synthesize decision context
        if "intent" not in decision and "product_domain" in decision:
            decision = {
                "intent": decision,
                "genome": {
                    "domain": decision.get("product_domain"),
                    "platform": {"rtl_support": decision.get("language") == "fa" or "fa" in decision.get("languages", [])}
                },
                "selected_style": decision.get("selected_style", "clean_stripe"),
            }
        elif "intent" not in decision and decision_or_intent is not decision:
            decision["intent"] = decision_or_intent

        if format_type.lower() in ["react", "tsx"]:
            return self.generate_react_tsx(decision, **kwargs)
        return self.generate_html(decision, **kwargs)

    def generate_react_tsx(self, decision: Any, component_name: str = "VibeMasterpiece") -> str:
        """
        Generates a modular, living React 19 / TypeScript component (.tsx)
        featuring render-affecting style compiler, living micro-states (useState),
        domain-calibrated signature widgets, and complete WCAG AAA / BiDi isolation.
        """
        if hasattr(decision, "to_dict"):
            decision_dict = decision.to_dict()
        elif isinstance(decision, dict):
            decision_dict = decision
        else:
            decision_dict = {}

        domain_id = (
            decision_dict.get("domain")
            or decision_dict.get("genome", {}).get("domain")
            or decision_dict.get("intent", {}).get("product_domain", "general_modern_saas")
        )
        blueprint = decision_dict.get("intent", {}).get("blueprint") or self.blueprints.get("domains", {}).get(domain_id, {})
        sig_widget = blueprint.get("signature_widget", {})
        selected_style = (
            decision_dict.get("style")
            or decision_dict.get("selected_style")
            or decision_dict.get("genome", {}).get("style", "clean_stripe")
        )
        theme_strategy = decision_dict.get("intent", {}).get("theme_strategy", "light")
        intent_obj = decision_dict.get("intent", {})
        intent_lang = intent_obj.get("language", "en")
        has_fa = (
            intent_lang == "fa"
            or (isinstance(intent_lang, (list, tuple)) and "fa" in intent_lang)
            or ("fa" in intent_obj.get("languages", []))
        )
        is_rtl = (
            decision_dict.get("genome", {}).get("platform", {}).get("rtl_support", False)
            or decision_dict.get("is_rtl", False)
            or has_fa
        )
        dir_attr = 'dir="rtl"' if is_rtl else 'dir="ltr"'

        style_cfg = self._compile_style(selected_style, theme_strategy)

        mock_data_all = blueprint.get("mock_data", {})
        mock_data_dict = mock_data_all.get("en", {}) if isinstance(mock_data_all.get("en"), dict) else mock_data_all
        headline = mock_data_dict.get("headline", "Next-Generation Autonomous Intelligence")
        subheadline = mock_data_dict.get("subheadline", "تجربه‌ای اصیل و منحصربه‌فرد با طراحی مدرن و کیفیتی متمایز." if is_rtl else "Engineered for uncompromising quality, modern elegance, and seamless customer experiences.")
        cta_primary = mock_data_dict.get("cta_primary", "Get Started Now")
        cta_secondary = mock_data_dict.get("cta_secondary", "Explore Interactive Demo")
        sig_widget_name = sig_widget.get("name", "Interactive Intelligence Hub")

        domain_metrics = mock_data_dict.get("metrics", [])
        metric1 = domain_metrics[0] if len(domain_metrics) > 0 else ({"label": "رضایت مراجعین", "value": "۹۹.۲٪"} if is_rtl else {"label": "Customer Satisfaction", "value": "99.2%"})
        metric2 = domain_metrics[1] if len(domain_metrics) > 1 else ({"label": "سرعت ارائه خدمات", "value": "کمتر از ۲ ساعت"} if is_rtl else {"label": "Response Velocity", "value": "< 2 Hours"})
        metric3 = domain_metrics[2] if len(domain_metrics) > 2 else ({"label": "امتیاز خدمات", "value": "۴.۹ از ۵"} if is_rtl else {"label": "Verified Experience", "value": "4.9 / 5"})

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
    {{"id": "overview", "label": "Primary Experience"}},
    {{"id": "telemetry", "label": "Domain Performance"}},
    {{"id": "architecture", "label": "Key Architecture"}}
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
              <span>System Operational</span>
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
              <div className="text-xs text-zinc-400">{"شاخص عملکرد و بازخورد مراجعین" if is_rtl else "Verified customer satisfaction rating"}</div>
            </div>

            <div className="{style_cfg['telemetry_card']}">
              <div className="text-xs font-medium text-zinc-500">{metric2['label']}</div>
              <div className="text-2xl font-bold font-mono text-sky-600 dark:text-sky-400">
                <bdi>{{{json.dumps(metric2['value'], ensure_ascii=False)}}}</bdi>
              </div>
              <div className="text-xs text-zinc-400">{"پایداری خدمات و تضمین کیفیت" if is_rtl else "Service availability and quality guarantee"}</div>
            </div>

            <div className="{style_cfg['telemetry_card']}">
              <div className="text-xs font-medium text-zinc-500">{metric3['label']}</div>
              <div className="text-2xl font-bold font-mono text-indigo-600 dark:text-indigo-400">
                <bdi>{{{json.dumps(metric3['value'], ensure_ascii=False)}}}</bdi>
              </div>
              <div className="text-xs text-zinc-400">{"تطبیق کامل با استانداردهای تخصصی" if is_rtl else "Optimized for seamless performance and speed"}</div>
            </div>
          </div>
        )}}

        {{/* Tab Panel 2: Product Capabilities & Architecture Solutions */}}
        {{activeTab === 2 && (
          <div role="tabpanel" className="pt-8 space-y-6 animate-fadeIn">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="{style_cfg['widget_card']}">
                <div className="size-10 rounded-xl bg-blue-500/10 text-blue-600 dark:text-blue-400 flex items-center justify-center font-bold text-sm">01</div>
                <h4 className="text-base font-bold text-zinc-900 dark:text-white">Enterprise Scalability</h4>
                <p className="text-xs text-zinc-500 dark:text-zinc-400 leading-relaxed">
                  Engineered with sub-millisecond responsiveness and zero-latency state synchronization.
                </p>
              </div>
              <div className="{style_cfg['widget_card']}">
                <div className="size-10 rounded-xl bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 flex items-center justify-center font-bold text-sm">02</div>
                <h4 className="text-base font-bold text-zinc-900 dark:text-white">Institutional Security</h4>
                <p className="text-xs text-zinc-500 dark:text-zinc-400 leading-relaxed">
                  Continuous cryptographic verification, end-to-end encryption, and full compliance auditing.
                </p>
              </div>
              <div className="{style_cfg['widget_card']}">
                <div className="size-10 rounded-xl bg-indigo-500/10 text-indigo-600 dark:text-indigo-400 flex items-center justify-center font-bold text-sm">03</div>
                <h4 className="text-base font-bold text-zinc-900 dark:text-white">Autonomous Ergonomics</h4>
                <p className="text-xs text-zinc-500 dark:text-zinc-400 leading-relaxed">
                  Tailored micro-interactions and accessible geometry designed for mission-critical workflows.
                </p>
              </div>
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

    def _build_google_fonts_url(self, typography: Dict[str, Any]) -> str:
        """Assembles a clean Google Fonts URL for display, body, mono, and Vazirmatn."""
        disp = typography.get("display_family") or typography.get("heading_font") or typography.get("heading", "Inter")
        body = typography.get("body_family") or typography.get("body_font") or typography.get("body", "Inter")
        mono = typography.get("mono_family") or typography.get("mono_font") or typography.get("mono", "JetBrains Mono")

        font_specs = {
            "Inter": "family=Inter:wght@400;500;600;700;800",
            "Newsreader": "family=Newsreader:ital,opsz,wght@0,6..72,400..700;1,6..72,400..700",
            "Space Grotesk": "family=Space+Grotesk:wght@400;500;600;700",
            "Space Mono": "family=Space+Mono:wght@400;700",
            "IBM Plex Mono": "family=IBM+Plex+Mono:wght@400;500;600",
            "JetBrains Mono": "family=JetBrains+Mono:wght@400;500",
            "Plus Jakarta Sans": "family=Plus+Jakarta+Sans:wght@400;500;600;700;800",
            "Playfair Display": "family=Playfair+Display:ital,wght@0,600;1,400",
            "Vazirmatn": "family=Vazirmatn:wght@400;500;600;700",
            "Cabinet Grotesk": "family=Plus+Jakarta+Sans:wght@400;600;700;800",
            "Satoshi": "family=Inter:wght@400;500;600;700",
            "Courier Prime": "family=JetBrains+Mono:wght@400;500"
        }

        families = []
        for f in [disp, body, mono, "Vazirmatn"]:
            spec = font_specs.get(f)
            if not spec and f and str(f).strip():
                clean_f = str(f).strip().replace(" ", "+")
                spec = f"family={clean_f}:wght@400;500;600;700"
            if spec and spec not in families:
                families.append(spec)

        if not families:
            families = ["family=Inter:wght@400;500;600;700", "family=Vazirmatn:wght@400;500;600;700"]

        return f"https://fonts.googleapis.com/css2?{'&'.join(families)}&display=swap"

    def generate_html(self, decision: Any, prompt_title: str = "Vibe UI Component") -> str:
        """Generates a complete, self-contained, accessible HTML page from DesignDecisionContract or DesignGenomeContract."""
        if hasattr(decision, "to_dict"):
            decision_dict = decision.to_dict()
        elif isinstance(decision, dict):
            decision_dict = decision
        else:
            decision_dict = {}

        genome = decision_dict.get("genome", {}) or {}
        tokens = decision_dict.get("tokens", {}) or genome.get("tokens", {}) or genome.get("color", {})
        typography = decision_dict.get("typography", {}) or genome.get("typography", {})
        geometry = decision_dict.get("geometry", {}) or genome.get("geometry", {}) or genome.get("radius", {})
        density = decision_dict.get("density", genome.get("density", "balanced"))
        surfaces = decision_dict.get("surfaces", {})
        depth = surfaces.get("depth") if isinstance(surfaces, dict) else genome.get("depth", "diffused_soft")
        domain_id = (
            decision_dict.get("domain")
            or genome.get("domain")
            or decision_dict.get("intent", {}).get("product_domain", "")
        )
        selected_style = (
            decision_dict.get("style")
            or decision_dict.get("selected_style")
            or genome.get("style", "clean_stripe")
        )

        genome["tokens"] = tokens
        genome["color"] = {
            "canvas": tokens.get("canvas", "oklch(0.99 0.005 0.0)"),
            "surface": tokens.get("surface", "oklch(0.96 0.007 0.0)"),
            "accent": tokens.get("accent", "oklch(0.58 0.080 0.0)"),
            "border": tokens.get("border", "oklch(0.90 0.006 0.0)"),
            "text": tokens.get("text_primary") or tokens.get("text", "oklch(0.12 0.020 0.0)"),
            "muted_text": tokens.get("text_secondary") or tokens.get("text_muted", "oklch(0.40 0.016 0.0)")
        }
        genome["typography"] = typography
        genome["geometry"] = geometry
        genome["radius"] = {
            "base": geometry.get("border_radius") or geometry.get("radius_base", "8px"),
            "container": geometry.get("container", "12px"),
            "button": geometry.get("button", "8px")
        }
        genome["depth"] = depth
        genome["domain"] = domain_id
        genome["style"] = selected_style

        intent_obj = decision_dict.get("intent", {})
        intent_lang = intent_obj.get("language", "en")
        has_fa_lang = (
            intent_lang == "fa"
            or (isinstance(intent_lang, (list, tuple)) and "fa" in intent_lang)
            or ("fa" in intent_obj.get("languages", []))
        )
        is_rtl = (
            genome.get("platform", {}).get("rtl_support", False)
            or decision_dict.get("is_rtl", False)
            or has_fa_lang
            or intent_obj.get("language_direction") == "rtl"
            or intent_lang in ["fa", "ar", "he", "ur"]
        )
        dir_attr = 'dir="rtl" lang="fa"' if is_rtl else 'dir="ltr" lang="en"'

        css_vars = self.genome_engine.to_css_variables(genome)
        font_url = self._build_google_fonts_url(typography)

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
        media_spec = self.asset_director.get_media_spec(domain_id)
        hero_image_url = media_spec.get("unsplash_url", "https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=1200&q=80")
        hero_webp_url = media_spec.get("hero_webp", "assets/curated_webp/general_modern_saas_hero.webp")
        hero_image_caption = media_spec.get("caption_fa" if is_rtl else "caption", "High-Resolution Domain Showcase")
        blueprint = decision.get("intent", {}).get("blueprint") or self.blueprints.get("domains", {}).get(domain_id, {})
        mock_data_all = blueprint.get("mock_data", {})
        mock_data_dict = mock_data_all.get("fa" if is_rtl else "en", {}) if isinstance(mock_data_all.get("en"), dict) else mock_data_all
        blueprint_headline = mock_data_dict.get("headline")
        blueprint_subheadline = mock_data_dict.get("subheadline")
        blueprint_cta_primary = mock_data_dict.get("cta_primary")
        blueprint_cta_secondary = mock_data_dict.get("cta_secondary")
        blueprint_metrics = mock_data_dict.get("metrics")

        # Resolve clean display title, navbar brand name, and domain badge
        raw_prompt_indicators = [
            "create", "build", "make", "want", "for a", "landing", "app", "book", "generate", "design", "page", "website", "site",
            "بساز", "طراحی", "میخوام", "می‌خوام", "سایت", "یک", "یه", "برای", "صفحه"
        ]
        lower_prompt = prompt_title.lower()
        is_raw_prompt = (
            any(ind in lower_prompt for ind in raw_prompt_indicators)
            or len(prompt_title.split()) > 2
            or any(w in prompt_title for w in ["میخوام", "می‌خوام", "بساز", "طراحی"])
            or prompt_title.strip() == "Vibe UI Component"
        )

        domain_brands = DOMAIN_CANONICAL_BRANDS.get(domain_id, {"en": "Vibe Studio", "fa": "استودیو وایب"})
        canonical_brand = domain_brands.get("fa" if is_rtl else "en", "Vibe Studio")

        if is_raw_prompt or not prompt_title.strip():
            brand_name = canonical_brand
        else:
            brand_name = prompt_title.strip()

        # Hero Headline: prioritize domain blueprint copy over raw user prompt
        if blueprint_headline:
            hero_headline = blueprint_headline
        else:
            hero_headline = f"{brand_name} — {'تجربه متمایز و پیشرو' if is_rtl else 'Premium Digital Experience'}"

        # Hero Subheadline: clean business copy, zero telemetry jargon
        if blueprint_subheadline:
            hero_subheadline = blueprint_subheadline
        else:
            hero_subheadline = (
                "تجربه‌ای اصیل، کارآمد و منحصربه‌فرد با طراحی مدرن و خدماتی در تراز استانداردهای روز دنیا."
                if is_rtl
                else "Engineered for uncompromising quality, modern elegance, and seamless customer experiences."
            )

        # Domain Badge: authentic domain guarantee, zero framework telemetry
        domain_badges = DOMAIN_CANONICAL_BADGES.get(domain_id, {"en": "Verified Experience", "fa": "تضمین اصالت و کیفیت"})
        hero_badge_text = domain_badges.get("fa" if is_rtl else "en", "Verified Experience")

        cta_primary_label = blueprint_cta_primary or ("شروع تجربه" if is_rtl else "Get Started")
        cta_secondary_label = blueprint_cta_secondary or ("مشاهده خدمات" if is_rtl else "Explore Services")

        # Smart sub-intent adaptation for loans and credit in fintech domain
        lower_prompt = prompt_title.lower()
        if domain_id == "fintech_banking" and any(k in lower_prompt for k in ["loan", "credit", "lending", "financing"]):
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
                {"label": "Customer Trust", "value": "99.4%"},
                {"label": "Response Speed", "value": "< 5 mins"},
                {"label": "Service Rating", "value": "4.9 / 5"}
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
                  <div class="text-xs text-[var(--text-muted)]">Today's Clinic Availability</div>
                  <div class="text-sm font-bold text-emerald-500 flex items-center gap-1.5 mt-0.5">
                    <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
                    <span>3 VIP Consultations Open</span>
                  </div>
                </div>
                <span class="px-2.5 py-1 rounded-full text-[11px] font-bold bg-[var(--accent)]/10 text-[var(--accent)] border border-[var(--accent)]/20">Express</span>
              </div>
              <div class="p-3.5 bg-[var(--canvas-bg)] rounded-[var(--radius-base)] border border-[var(--border-subtle)]">
                <div class="text-xs text-[var(--text-muted)] mb-2">Next Available Slots</div>
                <div class="grid grid-cols-3 gap-2">
                  <span class="px-2 py-1 text-center text-xs font-semibold rounded bg-[var(--surface-bg)] border border-[var(--border-subtle)] text-[var(--text-primary)]"><bdi>10:30 AM</bdi></span>
                  <span class="px-2 py-1 text-center text-xs font-semibold rounded bg-[var(--accent)] text-[var(--vibe-on-primary,#fff)]"><bdi>12:00 PM</bdi></span>
                  <span class="px-2 py-1 text-center text-xs font-semibold rounded bg-[var(--surface-bg)] border border-[var(--border-subtle)] text-[var(--text-primary)]"><bdi>04:30 PM</bdi></span>
                </div>
              </div>
              <div class="p-3 bg-[var(--surface-bg)] rounded-[var(--radius-base)] border border-amber-500/20 text-xs text-amber-600 dark:text-amber-400 flex items-center gap-2">
                <svg class="w-4 h-4 text-amber-500 flex-shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>
                <span>Includes 3D digital scan & specialist warranty</span>
              </div>
            </div>"""
        else:
            window_chrome_content_html = f"""            <div class="space-y-3">
{metrics_block_html}
            </div>"""

        # Determine domain-calibrated navigation and dynamic multi-archetype sections
        selected_style = decision.get("genome", {}).get("style", "stripe_crisp")
        theme_strat = decision.get("intent", {}).get("theme_strategy", "light")
        style_cfg = self._compile_style(selected_style, theme_strat)

        nav_links = get_domain_nav_links(domain_id, blueprint)
        nav_links_html = "\n".join([
            f'            <a href="{link["href"]}" class="text-sm font-medium hover:text-[var(--accent)] transition-colors min-h-[44px] inline-flex items-center">{link["label"]}</a>'
            for link in nav_links
        ])
        nav_links_mobile_html = "\n".join([
            f'            <a href="{link["href"]}" class="block py-2.5 px-3 rounded-[var(--radius-button)] text-sm font-medium text-[var(--text-main)] hover:bg-[var(--accent)]/10 hover:text-[var(--accent)] transition-colors min-h-[44px] flex items-center">{link["label"]}</a>'
            for link in nav_links
        ])

        domain_sections_html = compile_domain_sections(
            domain_id=domain_id,
            blueprint=blueprint,
            style_cfg=style_cfg,
            card_border=card_border,
            card_shadow=card_shadow,
            is_rtl=is_rtl
        )

        # Context-aware aside titlebar (DevOps / Terminal gets console header, all other domains get elegant business badge)
        is_terminal_domain = domain_id in ["devops_cloud_terminal", "cyber_terminal", "developer_cloud_platform"]
        if is_terminal_domain:
            aside_header_html = f"""          <div class="flex items-center space-x-2 rtl:space-x-reverse">
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
          </div>"""
        else:
            aside_header_html = f"""          <div class="flex items-center space-x-2 rtl:space-x-reverse">
            <span class="size-2 rounded-full bg-[var(--accent)]"></span>
            <span class="text-xs font-bold text-[var(--text-primary)] tracking-tight">Verified Platform Highlights</span>
          </div>
          <div class="flex items-center space-x-1.5 rtl:space-x-reverse">
            <span class="w-2 h-2 rounded-full bg-emerald-500"></span>
            <span class="text-[10px] font-medium text-emerald-600 dark:text-emerald-400 uppercase tracking-wider">ACTIVE</span>
          </div>"""

        # Custom cursor opt-in (strictly for creative portfolios & gaming)
        enable_custom_cursor = domain_id in ["creative_portfolio_agency", "gaming_entertainment_streaming"] or any(k in prompt_title.lower() for k in ["portfolio", "agency", "creative", "gaming"])
        cursor_css = """    @media (pointer: fine) {
      /* Non-destructive cursor dot enhancement without suppressing native cursor */
      #vibeCursorDot {
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
        box-shadow: 0 0 10px var(--accent);
        transition: opacity 0.2s ease, transform 0.15s cubic-bezier(0.16, 1, 0.3, 1), background-color 0.2s ease;
      }
      #vibeCursorDot.hover-target {
        transform: translate(-50%, -50%) scale(1.5);
        background-color: #ffffff;
        box-shadow: 0 0 14px var(--accent), 0 0 25px var(--accent);
      }
      #vibeCursorFollower {
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
      }
      #vibeCursorFollower svg {
        width: 36px;
        height: 39px;
        display: block;
        transition: transform 0.2s cubic-bezier(0.16, 1, 0.3, 1);
      }
      #vibeCursorFollower.hover-active svg {
        transform: scale(1.2);
      }
      #vibeCursorFollower.click-active svg {
        transform: scale(0.85);
      }
      #vibeCursorBadge {
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
      }
      #vibeCursorFollower.hover-active #vibeCursorBadge {
        opacity: 1;
        transform: scale(1);
      }
    }""" if enable_custom_cursor else ""

        cursor_html = """  <!-- Lightswind Trailing Arrow Pointer -->
  <div id="vibeCursorDot" class="hidden md:block" aria-hidden="true"></div>
  <div id="vibeCursorFollower" class="hidden md:flex" aria-hidden="true">
    <svg xmlns="http://www.w3.org/2000/svg" width="36" height="39" viewBox="0 0 50 54" fill="none" class="pointer-events-none drop-shadow-md">
      <path d="M42.6817 41.1495L27.5103 6.79925C26.7269 5.02557 24.2082 5.02558 23.3927 6.79925L7.59814 41.1495C6.75833 42.9759 8.52712 44.8902 10.4125 44.1954L24.3757 39.0496C24.8829 38.8627 25.4385 38.8627 25.9422 39.0496L39.8121 44.1954C41.6849 44.8902 43.4884 42.9759 42.6817 41.1495Z" fill="currentColor"/>
      <path d="M43.7146 40.6933L28.5431 6.34306C27.3556 3.65428 23.5772 3.69516 22.3668 6.32755L6.57226 40.6778C5.3134 43.4156 7.97238 46.298 10.803 45.2549L24.7662 40.109C25.0221 40.0147 25.2999 40.0156 25.5494 40.1082L39.4193 45.254C42.2261 46.2953 44.9254 43.4347 43.7146 40.6933Z" stroke="currentColor" stroke-width="1.5"/>
    </svg>
    <span id="vibeCursorBadge"></span>
  </div>""" if enable_custom_cursor else ""


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

{cursor_css}

    .ambient-spotlight-layer {{
      position: fixed;
      inset: 0;
      pointer-events: none;
      z-index: 1;
      background: radial-gradient(550px circle at var(--mouse-x, 50%) var(--mouse-y, 50%), color-mix(in oklch, var(--accent) 6%, transparent), transparent 70%);
      transition: opacity 0.3s ease;
    }}

    /* Scroll-Driven Kinetic Stagger Reveal & Lazy Loading Standard */
    .vibe-reveal-node {{
      opacity: 0;
      transform: translateY(28px);
      transition: opacity 0.75s cubic-bezier(0.16, 1, 0.3, 1), transform 0.75s cubic-bezier(0.16, 1, 0.3, 1);
      will-change: opacity, transform;
    }}
    .vibe-reveal-node.vibe-revealed {{
      opacity: 1 !important;
      transform: translateY(0) !important;
    }}
    @media (prefers-reduced-motion: reduce) {{
      .vibe-reveal-node {{
        opacity: 1 !important;
        transform: none !important;
        transition: none !important;
      }}
    }}
    /* Lazy Editorial Image Smooth Fade-In */
    img[loading="lazy"] {{
      opacity: 0;
      transition: opacity 0.6s ease-in-out;
    }}
    img[loading="lazy"].loaded {{
      opacity: 1 !important;
    }}
  </style>
</head>
<body class="min-h-full flex flex-col antialiased relative">
{cursor_html}

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
        <!-- Mobile Navigation Menu Toggle Button -->
        <button type="button" id="vibeMobileMenuBtn" class="md:hidden inline-flex items-center justify-center p-2 rounded-[var(--radius-button)] text-[var(--text-main)] hover:bg-[var(--accent)]/10 min-h-[44px] min-w-[44px] border border-[var(--border-subtle)] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--accent)]" aria-expanded="false" aria-controls="vibeMobileMenu" aria-label="Toggle navigation menu">
          <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" aria-hidden="true">
            <path stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>
      </div>
    </div>
    <!-- Responsive Mobile Navigation Drawer -->
    <div id="vibeMobileMenu" class="md:hidden hidden border-t border-[var(--border-subtle)] bg-[var(--surface-bg)] px-4 pt-3 pb-4 space-y-2" aria-label="Mobile Navigation">
{nav_links_mobile_html}
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
            <span>{hero_badge_text}</span>
          </div>
          <h1 id="hero-title" class="text-3xl sm:text-4xl lg:text-5xl font-extrabold tracking-tight mb-4 vibe-gradient-heading">
            {hero_headline}
          </h1>
          <p class="text-[var(--text-muted)] text-base sm:text-lg leading-relaxed max-w-2xl mb-6">
            {hero_subheadline}
          </p>

          <!-- Editorial Domain Asset Showcase -->
          <div class="relative w-full h-44 sm:h-56 rounded-[var(--radius-button)] overflow-hidden border border-[var(--border-subtle)] mb-6 shadow-sm">
            <img src="{hero_image_url}" alt="{hero_image_caption}" class="w-full h-full object-cover" loading="lazy" decoding="async" onerror="this.src='https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=1200&q=80'" />
            <div class="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent pointer-events-none"></div>
            <div class="absolute bottom-2 start-3 end-3 text-[11px] font-mono text-white/95 flex items-center justify-between">
              <span class="truncate"><bdi>{hero_image_caption}</bdi></span>
              <span class="px-1.5 py-0.5 rounded bg-black/40 text-[10px] uppercase font-mono">Verified CDN</span>
            </div>
          </div>
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
{aside_header_html}
        </div>

        <div class="p-6 flex-1 flex flex-col justify-between">
          <div>
            <h2 class="text-base font-bold mb-4 flex items-center space-x-2 rtl:space-x-reverse">
              <svg class="w-4 h-4 text-[var(--accent)]" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M22 12h-4l-3 9L9 3l-3 9H2"></path></svg>
              <span>Highlights & Status</span>
            </h2>
{window_chrome_content_html}
          </div>
          <div class="mt-6 pt-4 border-t border-[var(--border-subtle)] text-xs text-[var(--text-muted)] flex items-center justify-between">
            <div class="flex items-center space-x-1.5 rtl:space-x-reverse">
              <span class="w-2 h-2 rounded-full bg-emerald-500"></span>
              <span>{"آماده ارائه خدمات" if is_rtl else "Active & Ready"}</span>
            </div>
            <span class="font-mono text-[10px] opacity-70"><bdi>{"تضمین کیفیت ۱۰۰٪" if is_rtl else "100% Guaranteed"}</bdi></span>
          </div>
        </div>
      </aside>
    </div>

{domain_sections_html}
  </main>

  <footer class="w-full border-t border-[var(--border-subtle)] bg-[var(--surface-bg)] py-6 mt-12">
    <div class="max-w-7xl mx-auto px-4 text-center text-xs text-[var(--text-muted)]">
      &copy; 2026 {brand_name}. All rights reserved.
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
          showToast(document.documentElement.getAttribute('dir') === 'rtl' ? 'جزئیات و امکانات مشاهده شد.' : 'Details and services overview opened.');
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
          showToast(view === 'before' ? 'Showing baseline pre-treatment gallery' : 'Showing post-treatment results gallery');
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

      // 6.6. Responsive Mobile Navigation Drawer Toggle
      var mobileBtn = document.getElementById('vibeMobileMenuBtn');
      var mobileMenu = document.getElementById('vibeMobileMenu');
      if (mobileBtn && mobileMenu) {{
        mobileBtn.addEventListener('click', function() {{
          var isOpen = mobileBtn.getAttribute('aria-expanded') === 'true';
          mobileBtn.setAttribute('aria-expanded', !isOpen);
          mobileMenu.classList.toggle('hidden');
        }});
      }}

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
          showToast('Appointment request confirmed. A clinic specialist will contact you shortly.');
          bookingForm.reset();
        }});
      }}

      var contactForm = document.getElementById('contact-form');
      if (contactForm) {{
        contactForm.addEventListener('submit', function(e) {{
          e.preventDefault();
          showToast('Thank you! Your message has been sent successfully.');
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
            cursorDot.classList.add('hover-target');
            cursorFollower.classList.add('hover-active');
            if (cursorBadge) {{
              if (el.tagName.toLowerCase() === 'button') cursorBadge.textContent = 'ACTIVATE';
              else if (el.tagName.toLowerCase() === 'a') cursorBadge.textContent = 'EXPLORE';
              else cursorBadge.textContent = 'VIEW';
            }}
          }});
          el.addEventListener('pointerleave', function() {{
            cursorDot.classList.remove('hover-target');
            cursorFollower.classList.remove('hover-active');
            if (cursorBadge) cursorBadge.textContent = '';
          }});
        }});
      }}

      // 11. Scroll-Driven Kinetic Stagger Entrance Observers
      var revealTargets = document.querySelectorAll('section > div:not(.animate-marquee), .vibe-spotlight-card');
      revealTargets.forEach(function(el, index) {{
        if (el.classList.contains('animate-marquee') || el.closest('.animate-marquee')) return;
        el.classList.add('vibe-reveal-node');
        var delay = (index % 3) * 0.08;
        if (delay > 0) {{
          el.style.transitionDelay = delay.toFixed(2) + 's';
        }}
      }});

      var scrollObserver = new IntersectionObserver(function(entries) {{
        entries.forEach(function(entry) {{
          if (entry.isIntersecting) {{
            entry.target.classList.add('vibe-revealed');
            scrollObserver.unobserve(entry.target);
          }}
        }});
      }}, {{ threshold: 0.08, rootMargin: '0px 0px -30px 0px' }});

      revealTargets.forEach(function(el) {{
        scrollObserver.observe(el);
      }});

      // Lazy Loading Image Progressive Fade-In
      var lazyImages = document.querySelectorAll('img[loading="lazy"]');
      lazyImages.forEach(function(img) {{
        if (img.complete) {{
          img.classList.add('loaded');
        }} else {{
          img.addEventListener('load', function() {{ img.classList.add('loaded'); }});
          img.addEventListener('error', function() {{ img.classList.add('loaded'); }});
        }}
      }});
    }})();
  </script>
</body>
</html>
"""
        return html
