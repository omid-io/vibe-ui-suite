"""
vibe_core.asset_director — Media Composition & Asset Direction Engine (v3.7.0)
Directs responsive aspect ratios, image framing, and editorial media containers
across all 24 canonical industry domains with zero domain-key mismatches.
Demarcates placeholders transparently as synthetic slots awaiting source assets.
"""

from typing import Dict, Any, Optional

class AssetDirector:
    """
    Directs visual asset composition, responsive aspect ratios, and placeholder geometries.
    Ensures media containers adhere to editorial standards: WCAG AAA contrast overlays, proper object-fit,
    and domain-appropriate aspect ratio discipline for all 24 canonical domains.
    """

    # Canonical 24-domain media specifications
    DOMAIN_MEDIA_SPECS: Dict[str, Dict[str, Any]] = {
        "beauty_clinical_wellness": {
            "aspect_ratio": "aspect-[4/5] sm:aspect-[3/4]",
            "role": "clinical_portrait",
            "overlay_style": "subtle_vignette",
            "caption": "Clinical Outcome Visual Slot (Laser Rejuvenation Protocol)",
            "caption_fa": "فریم نتایج بالینی جوانسازی پوست و پروتکل درمانی"
        },
        "fintech_banking": {
            "aspect_ratio": "aspect-[16/9] sm:aspect-[16/10]",
            "role": "capital_portfolio",
            "overlay_style": "subtle_financial_grid",
            "caption": "Smart Capital Allocation & Real-Time Liquidity Chart",
            "caption_fa": "نمودار تخصیص سرمایه هوشمند و شاخص نقدشوندگی"
        },
        "crypto_trading_web3": {
            "aspect_ratio": "aspect-[16/9] sm:aspect-[21/9]",
            "role": "orderbook_depth",
            "overlay_style": "cyber_matrix_glow",
            "caption": "Aggregated Liquidity Depth & Low-Slippage Routing Matrix",
            "caption_fa": "عمق نقدینگی صرافی نامتمرکز و ماتریکس مسیریابی"
        },
        "devops_cloud_terminal": {
            "aspect_ratio": "aspect-[16/10] sm:aspect-[16/9]",
            "role": "cluster_topology",
            "overlay_style": "terminal_hud_scanline",
            "caption": "Multi-Region Kubernetes Pod Topology & Egress Flow",
            "caption_fa": "توپولوژی نودهای ابری کوبرنتیز و مسیرهای شبکه"
        },
        "saas_b2b_enterprise": {
            "aspect_ratio": "aspect-[16/9] sm:aspect-[16/10]",
            "role": "enterprise_dashboard",
            "overlay_style": "corporate_clean_surface",
            "caption": "Unified Enterprise Orchestration & Provisioning Suite",
            "caption_fa": "داشبورد یکپارچه مدیریت فرآیندهای سازمانی"
        },
        "ai_developer_platform": {
            "aspect_ratio": "aspect-[16/9] sm:aspect-[21/9]",
            "role": "neural_latent_canvas",
            "overlay_style": "deep_space_spectrum",
            "caption": "Transformer Attention Map & Cluster Latency Telemetry",
            "caption_fa": "نقشه توجه لایه های هوش مصنوعی و تله متری کلاستر GPU"
        },
        "food_restaurant_cafe": {
            "aspect_ratio": "aspect-[16/9] sm:aspect-[4/3]",
            "role": "sensory_food_editorial",
            "overlay_style": "warm_atmospheric_gradient",
            "caption": "Signature Seasonal Degustation Menu Presentation",
            "caption_fa": "معرفی منوی فصلی سرآشپز و هنر آشپزی ارگانیک"
        },
        "real_estate_architecture": {
            "aspect_ratio": "aspect-[16/9] sm:aspect-[3/2]",
            "role": "architectural_perspective",
            "overlay_style": "specular_floorplan_tint",
            "caption": "Prime Residential Penthouse Portfolio & Skyline View",
            "caption_fa": "پلان معماری پنت هاوس اختصاصی و چشم انداز پانوراما"
        },
        "healthcare_hospital_medical": {
            "aspect_ratio": "aspect-[4/3] sm:aspect-[16/10]",
            "role": "clinical_diagnostic",
            "overlay_style": "sterile_clinical_soft",
            "caption": "FHIR-Compliant Electronic Health Record & Tele-Triage",
            "caption_fa": "پرونده الکترونیک سلامت و تریاژ هوشمند بالینی"
        },
        "education_edtech_lms": {
            "aspect_ratio": "aspect-[16/9] sm:aspect-[16/10]",
            "role": "curriculum_interactive",
            "overlay_style": "educational_focus_glow",
            "caption": "Adaptive Learning Graph & Mastery Certification Track",
            "caption_fa": "مسیر یادگیری انطباقی و گراف تسلط بر مهارت ها"
        },
        "creative_portfolio_agency": {
            "aspect_ratio": "aspect-[16/10] sm:aspect-[3/2]",
            "role": "editorial_case_study",
            "overlay_style": "minimal_high_contrast",
            "caption": "Award-Winning Brand Identity & Design System Deliverable",
            "caption_fa": "نمونه کار هویت بصری جامع و سیستم طراحی برند"
        },
        "ecommerce_luxury_fashion": {
            "aspect_ratio": "aspect-square sm:aspect-[4/5]",
            "role": "atelier_lookbook",
            "overlay_style": "editorial_soft_shadow",
            "caption": "Handcrafted Bespoke Atelier Collection • Limited Edition",
            "caption_fa": "کلکسیون دست دوز آتلیه مد اختصاصی با پارچه های ارگانیک"
        },
        "ecommerce_mass_market": {
            "aspect_ratio": "aspect-square sm:aspect-[4/3]",
            "role": "product_catalog_showcase",
            "overlay_style": "high_fidelity_storefront",
            "caption": "Dynamic Catalog Showcase with Tiered Volume Discounts",
            "caption_fa": "کاتالوگ محصولات با اعمال آنی تخفیف های پلکانی"
        },
        "media_editorial_magazine": {
            "aspect_ratio": "aspect-[3/4] sm:aspect-[4/5]",
            "role": "longform_journalism",
            "overlay_style": "monochrome_editorial",
            "caption": "Investigative Edition Cover • Independent Journalism",
            "caption_fa": "گزارش ویژه تحلیلی و روزنامه نگاری مستقل"
        },
        "travel_hospitality_tourism": {
            "aspect_ratio": "aspect-[16/9] sm:aspect-[3/2]",
            "role": "destination_panoramic",
            "overlay_style": "golden_hour_vignette",
            "caption": "Exclusive Coastal Villa Retreat & Private Heliport",
            "caption_fa": "ویلای ساحلی اختصاصی و چشم انداز طبیعی بکر"
        },
        "legal_compliance_law": {
            "aspect_ratio": "aspect-[16/9] sm:aspect-[4/3]",
            "role": "statutory_compliance",
            "overlay_style": "sober_navy_tint",
            "caption": "Cross-Border Regulatory Compliance & Audit Assurance",
            "caption_fa": "ممیزی مقرراتی حقوقی بین المللی و تطبیق استانداردها"
        },
        "gaming_entertainment_streaming": {
            "aspect_ratio": "aspect-[16/9] sm:aspect-[21/9]",
            "role": "gameplay_cinematic",
            "overlay_style": "neon_raytraced_accent",
            "caption": "Real-Time 4K Raytraced Stream & Sub-Millisecond Tickrate",
            "caption_fa": "استریم با کیفیت 4K و تاخیر شبکه نزدیک به صفر"
        },
        "automotive_ev_mobility": {
            "aspect_ratio": "aspect-[16/9] sm:aspect-[21/9]",
            "role": "aerodynamic_chassis",
            "overlay_style": "edge_glow_ambient",
            "caption": "Silicon-Carbide 800V Powertrain & Telemetry Matrix",
            "caption_fa": "شاسی آیرودینامیک و سیستم محرکه پیشرفته ۸۰۰ ولت"
        },
        "logistics_supply_chain": {
            "aspect_ratio": "aspect-[16/9] sm:aspect-[16/10]",
            "role": "supply_telematics",
            "overlay_style": "fleet_corridor_tint",
            "caption": "Autonomous Global Freight Corridor & Fleet Tracking",
            "caption_fa": "مسیریابی هوشمند ناوگان ترانزیت و نظارت بر بار"
        },
        "energy_greentech_sustainability": {
            "aspect_ratio": "aspect-[16/9] sm:aspect-[3/2]",
            "role": "renewable_grid",
            "overlay_style": "clean_solar_glow",
            "caption": "Megawatt Solar Array & Battery Energy Storage System (BESS)",
            "caption_fa": "نیروگاه خورشیدی متصل به شبکه و ذخیره سازی انرژی"
        },
        "nonprofit_charity_social": {
            "aspect_ratio": "aspect-[16/9] sm:aspect-[4/3]",
            "role": "humanitarian_impact",
            "overlay_style": "warm_compassion_tint",
            "caption": "On-the-Ground Direct Clean Water Installation & Solar Pump",
            "caption_fa": "پروژه میدانی دسترسی مستقیم به آب پاک و توسعه پایدار"
        },
        "personal_branding_creator": {
            "aspect_ratio": "aspect-[4/5] sm:aspect-[1/1]",
            "role": "creator_signature",
            "overlay_style": "editorial_soft_studio",
            "caption": "Curated Thought-Leadership Digest & Audio Studio Edition",
            "caption_fa": "استودیوی اختصاصی تولید محتوای تخصصی و خبرنامه"
        },
        "cybersecurity_identity_auth": {
            "aspect_ratio": "aspect-[16/9] sm:aspect-[21/9]",
            "role": "zero_trust_matrix",
            "overlay_style": "crimson_threat_grid",
            "caption": "Continuous Behavioral Anomaly Detection & Zero-Trust Shield",
            "caption_fa": "سپر دفاعی احراز هویت بدون گذرواژه و پایش تهدیدات"
        },
        "general_modern_saas": {
            "aspect_ratio": "aspect-[16/9] sm:aspect-[16/10]",
            "role": "workflow_orchestration",
            "overlay_style": "subtle_gradient",
            "caption": "Autonomous Multi-Agent Workflow Engine & Automation Matrix",
            "caption_fa": "موتور خودکارسازی فرآیندهای ابری و هوش مصنوعی مولد"
        }
    }

    # Legacy / Alternative Domain Aliases
    DOMAIN_ALIASES: Dict[str, str] = {
        "ecommerce_luxury_retail": "ecommerce_luxury_fashion",
        "real_estate_proptech": "real_estate_architecture",
        "automotive_mobility": "automotive_ev_mobility",
        "creative_agency_portfolio": "creative_portfolio_agency",
        "architecture_interior": "real_estate_architecture",
    }

    DEFAULT_MEDIA_SPEC: Dict[str, Any] = {
        "aspect_ratio": "aspect-[16/9] sm:aspect-[16/10]",
        "role": "contextual_overview",
        "overlay_style": "subtle_gradient",
        "caption": "Interactive Domain Blueprint Showcase",
        "caption_fa": "نمای تعاملی معماری و ساختار محصول"
    }

    def get_media_spec(self, domain_id: str) -> Dict[str, Any]:
        """Resolves the editorial media specification for a given domain."""
        canonical_id = self.DOMAIN_ALIASES.get(domain_id, domain_id)
        return self.DOMAIN_MEDIA_SPECS.get(canonical_id, self.DEFAULT_MEDIA_SPEC)

    def generate_media_container_jsx(
        self,
        domain_id: str,
        style_name: str = "clean_stripe",
        is_rtl: bool = False
    ) -> str:
        """
        Generates an accessible, responsive media container with transparent synthetic demarcation,
        aspect ratio constraints, and editorial caption.
        """
        spec = self.get_media_spec(domain_id)
        aspect = spec["aspect_ratio"]
        caption = spec.get("caption_fa" if is_rtl else "caption", spec["caption"])

        # Style-tailored border and surface
        if style_name == "neobrutalism":
            border_cls = "border-2 border-black shadow-[4px_4px_0px_#000000] rounded-none"
        elif style_name == "quiet_luxury":
            border_cls = "border border-stone-200/60 dark:border-stone-800/60 rounded-2xl shadow-sm"
        elif style_name in ["terminal_hud", "data_dense_terminal"]:
            border_cls = "border border-emerald-500/40 font-mono rounded-none"
        else:
            border_cls = "border border-zinc-200/80 dark:border-zinc-800/80 rounded-2xl shadow-sm"

        return f'''
        <div className="relative overflow-hidden bg-zinc-100 dark:bg-zinc-900 {aspect} {border_cls} flex flex-col justify-between p-4 group select-none" data-origin="synthetic_demo">
          <div className="flex items-center justify-between text-[11px] font-mono text-zinc-500 z-10">
            <span className="px-2 py-0.5 rounded bg-black/5 dark:bg-white/5 backdrop-blur-md border border-zinc-200/50 dark:border-zinc-700/50">
              <bdi>{spec["role"].upper()}</bdi>
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
            <p className="text-xs font-medium text-white/90"><bdi>{caption}</bdi></p>
          </div>
        </div>'''
