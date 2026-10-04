"""
vibe_core.asset_director — Media Composition & Asset Direction Engine (v4.4.0)
Directs responsive aspect ratios, curated high-resolution editorial photography,
and tactile image framing across all 24 canonical industry domains with zero domain-key mismatches.
Demarcates placeholders transparently as synthetic slots awaiting source assets while
providing rich, domain-calibrated visual inspiration via high-fidelity Unsplash editorial photography.
"""

from typing import Dict, Any, Optional

class AssetDirector:
    """
    Directs visual asset composition, responsive aspect ratios, and curated editorial photography.
    Ensures media containers adhere to luxury editorial standards: WCAG AAA contrast overlays,
    proper object-fit, responsive aspect ratios, and domain-appropriate photography for all 24 canonical domains.
    """

    # Canonical 24-domain media specifications with curated high-resolution Unsplash photography
    DOMAIN_MEDIA_SPECS: Dict[str, Dict[str, Any]] = {
        "beauty_clinical_wellness": {
            "aspect_ratio": "aspect-[4/5] sm:aspect-[3/4]",
            "role": "clinical_portrait",
            "overlay_style": "subtle_vignette",
            "caption": "Clinical Outcome Visual Slot (Laser Rejuvenation Protocol)",
            "caption_fa": "فریم نتایج بالینی جوانسازی پوست و پروتکل درمانی",
            "unsplash_url": "https://images.unsplash.com/photo-1629909613654-28e377c37b09?auto=format&fit=crop&w=1200&q=80"
        },
        "fintech_banking": {
            "aspect_ratio": "aspect-[16/9] sm:aspect-[16/10]",
            "role": "capital_portfolio",
            "overlay_style": "subtle_financial_grid",
            "caption": "Smart Capital Allocation & Real-Time Liquidity Chart",
            "caption_fa": "نمودار تخصیص سرمایه هوشمند و شاخص نقدشوندگی",
            "unsplash_url": "https://images.unsplash.com/photo-1642543492481-44e81e3914a7?auto=format&fit=crop&w=1200&q=80"
        },
        "crypto_trading_web3": {
            "aspect_ratio": "aspect-[16/9] sm:aspect-[21/9]",
            "role": "orderbook_depth",
            "overlay_style": "cyber_matrix_glow",
            "caption": "Aggregated Liquidity Depth & Low-Slippage Routing Matrix",
            "caption_fa": "عمق نقدینگی صرافی نامتمرکز و ماتریکس مسیریابی",
            "unsplash_url": "https://images.unsplash.com/photo-1639762681485-074b7f938ba0?auto=format&fit=crop&w=1200&q=80"
        },
        "devops_cloud_terminal": {
            "aspect_ratio": "aspect-[16/10] sm:aspect-[16/9]",
            "role": "cluster_topology",
            "overlay_style": "terminal_hud_scanline",
            "caption": "Multi-Region Kubernetes Pod Topology & Egress Flow",
            "caption_fa": "توپولوژی نودهای ابری کوبرنتیز و مسیرهای شبکه",
            "unsplash_url": "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?auto=format&fit=crop&w=1200&q=80"
        },
        "saas_b2b_enterprise": {
            "aspect_ratio": "aspect-[16/9] sm:aspect-[16/10]",
            "role": "enterprise_dashboard",
            "overlay_style": "corporate_clean_surface",
            "caption": "Unified Enterprise Orchestration & Provisioning Suite",
            "caption_fa": "داشبورد یکپارچه مدیریت فرآیندهای سازمانی",
            "unsplash_url": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=1200&q=80"
        },
        "ai_developer_platform": {
            "aspect_ratio": "aspect-[16/9] sm:aspect-[21/9]",
            "role": "neural_latent_canvas",
            "overlay_style": "deep_space_spectrum",
            "caption": "Transformer Attention Map & Cluster Latency Telemetry",
            "caption_fa": "نقشه توجه لایه های هوش مصنوعی و تله متری کلاستر GPU",
            "unsplash_url": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=1200&q=80"
        },
        "food_restaurant_cafe": {
            "aspect_ratio": "aspect-[16/9] sm:aspect-[4/3]",
            "role": "sensory_food_editorial",
            "overlay_style": "warm_atmospheric_gradient",
            "caption": "Signature Seasonal Degustation Menu Presentation",
            "caption_fa": "معرفی منوی فصلی سرآشپز و هنر آشپزی ارگانیک",
            "unsplash_url": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?auto=format&fit=crop&w=1200&q=80"
        },
        "real_estate_architecture": {
            "aspect_ratio": "aspect-[16/9] sm:aspect-[3/2]",
            "role": "architectural_perspective",
            "overlay_style": "specular_floorplan_tint",
            "caption": "Prime Residential Penthouse Portfolio & Skyline View",
            "caption_fa": "پلان معماری پنت هاوس اختصاصی و چشم انداز پانوراما",
            "unsplash_url": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=1200&q=80"
        },
        "healthcare_hospital_medical": {
            "aspect_ratio": "aspect-[4/3] sm:aspect-[16/10]",
            "role": "clinical_diagnostic",
            "overlay_style": "sterile_clinical_soft",
            "caption": "FHIR-Compliant Electronic Health Record & Tele-Triage",
            "caption_fa": "پرونده الکترونیک سلامت و تریاژ هوشمند بالینی",
            "unsplash_url": "https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?auto=format&fit=crop&w=1200&q=80"
        },
        "education_edtech_lms": {
            "aspect_ratio": "aspect-[16/9] sm:aspect-[16/10]",
            "role": "curriculum_interactive",
            "overlay_style": "educational_focus_glow",
            "caption": "Adaptive Learning Graph & Mastery Certification Track",
            "caption_fa": "مسیر یادگیری انطباقی و گراف تسلط بر مهارت ها",
            "unsplash_url": "https://images.unsplash.com/photo-1523240795612-9a054b0db644?auto=format&fit=crop&w=1200&q=80"
        },
        "creative_portfolio_agency": {
            "aspect_ratio": "aspect-[16/10] sm:aspect-[3/2]",
            "role": "editorial_case_study",
            "overlay_style": "minimal_high_contrast",
            "caption": "Award-Winning Brand Identity & Design System Deliverable",
            "caption_fa": "نمونه کار هویت بصری جامع و سیستم طراحی برند",
            "unsplash_url": "https://images.unsplash.com/photo-1507238691740-187a5b1d37b8?auto=format&fit=crop&w=1200&q=80"
        },
        "ecommerce_luxury_fashion": {
            "aspect_ratio": "aspect-square sm:aspect-[4/5]",
            "role": "atelier_lookbook",
            "overlay_style": "editorial_soft_shadow",
            "caption": "Handcrafted Bespoke Atelier Collection • Limited Edition",
            "caption_fa": "کلکسیون دست دوز آتلیه مد اختصاصی با پارچه های ارگانیک",
            "unsplash_url": "https://images.unsplash.com/photo-1539109136881-3be0616acf4b?auto=format&fit=crop&w=1200&q=80"
        },
        "ecommerce_mass_market": {
            "aspect_ratio": "aspect-square sm:aspect-[4/3]",
            "role": "product_catalog_showcase",
            "overlay_style": "high_fidelity_storefront",
            "caption": "Dynamic Catalog Showcase with Tiered Volume Discounts",
            "caption_fa": "کاتالوگ محصولات با اعمال آنی تخفیف های پلکانی",
            "unsplash_url": "https://images.unsplash.com/photo-1441986300917-64674bd600d8?auto=format&fit=crop&w=1200&q=80"
        },
        "media_editorial_magazine": {
            "aspect_ratio": "aspect-[3/4] sm:aspect-[4/5]",
            "role": "longform_journalism",
            "overlay_style": "monochrome_editorial",
            "caption": "Investigative Edition Cover • Independent Journalism",
            "caption_fa": "گزارش ویژه تحلیلی و روزنامه نگاری مستقل",
            "unsplash_url": "https://images.unsplash.com/photo-1505373877841-8d25f7d46678?auto=format&fit=crop&w=1200&q=80"
        },
        "travel_hospitality_tourism": {
            "aspect_ratio": "aspect-[16/9] sm:aspect-[3/2]",
            "role": "destination_panoramic",
            "overlay_style": "golden_hour_vignette",
            "caption": "Exclusive Coastal Villa Retreat & Private Heliport",
            "caption_fa": "ویلای ساحلی اختصاصی و چشم انداز طبیعی بکر",
            "unsplash_url": "https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=1200&q=80"
        },
        "legal_compliance_law": {
            "aspect_ratio": "aspect-[16/9] sm:aspect-[4/3]",
            "role": "statutory_compliance",
            "overlay_style": "sober_navy_tint",
            "caption": "Cross-Border Regulatory Compliance & Audit Assurance",
            "caption_fa": "ممیزی مقرراتی حقوقی بین المللی و تطبیق استانداردها",
            "unsplash_url": "https://images.unsplash.com/photo-1589829545856-d10d557cf95f?auto=format&fit=crop&w=1200&q=80"
        },
        "gaming_entertainment_streaming": {
            "aspect_ratio": "aspect-[16/9] sm:aspect-[21/9]",
            "role": "gameplay_cinematic",
            "overlay_style": "neon_raytraced_accent",
            "caption": "Real-Time 4K Raytraced Stream & Sub-Millisecond Tickrate",
            "caption_fa": "استریم با کیفیت 4K و تاخیر شبکه نزدیک به صفر",
            "unsplash_url": "https://images.unsplash.com/photo-1542751371-adc38448a05e?auto=format&fit=crop&w=1200&q=80"
        },
        "automotive_ev_mobility": {
            "aspect_ratio": "aspect-[16/9] sm:aspect-[21/9]",
            "role": "aerodynamic_chassis",
            "overlay_style": "edge_glow_ambient",
            "caption": "Silicon-Carbide 800V Powertrain & Telemetry Matrix",
            "caption_fa": "شاسی آیرودینامیک و سیستم محرکه پیشرفته ۸۰۰ ولت",
            "unsplash_url": "https://images.unsplash.com/photo-1617814076367-b759c7d7e738?auto=format&fit=crop&w=1200&q=80"
        },
        "logistics_supply_chain": {
            "aspect_ratio": "aspect-[16/9] sm:aspect-[16/10]",
            "role": "supply_telematics",
            "overlay_style": "fleet_corridor_tint",
            "caption": "Autonomous Global Freight Corridor & Fleet Tracking",
            "caption_fa": "مسیریابی هوشمند ناوگان ترانزیت و نظارت بر بار",
            "unsplash_url": "https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?auto=format&fit=crop&w=1200&q=80"
        },
        "energy_greentech_sustainability": {
            "aspect_ratio": "aspect-[16/9] sm:aspect-[3/2]",
            "role": "renewable_grid",
            "overlay_style": "clean_solar_glow",
            "caption": "Megawatt Solar Array & Battery Energy Storage System (BESS)",
            "caption_fa": "نیروگاه خورشیدی متصل به شبکه و ذخیره سازی انرژی",
            "unsplash_url": "https://images.unsplash.com/photo-1497435334941-8c899ee9e8e9?auto=format&fit=crop&w=1200&q=80"
        },
        "nonprofit_charity_social": {
            "aspect_ratio": "aspect-[16/9] sm:aspect-[4/3]",
            "role": "humanitarian_impact",
            "overlay_style": "warm_compassion_tint",
            "caption": "On-the-Ground Direct Clean Water Installation & Solar Pump",
            "caption_fa": "پروژه میدانی دسترسی مستقیم به آب پاک و توسعه پایدار",
            "unsplash_url": "https://images.unsplash.com/photo-1488521787991-ed7bbaae773c?auto=format&fit=crop&w=1200&q=80"
        },
        "personal_branding_creator": {
            "aspect_ratio": "aspect-[4/5] sm:aspect-[1/1]",
            "role": "creator_signature",
            "overlay_style": "editorial_soft_studio",
            "caption": "Curated Thought-Leadership Digest & Audio Studio Edition",
            "caption_fa": "استودیوی اختصاصی تولید محتوای تخصصی و خبرنامه",
            "unsplash_url": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=1200&q=80"
        },
        "cybersecurity_identity_auth": {
            "aspect_ratio": "aspect-[16/9] sm:aspect-[21/9]",
            "role": "zero_trust_matrix",
            "overlay_style": "crimson_threat_grid",
            "caption": "Continuous Behavioral Anomaly Detection & Zero-Trust Shield",
            "caption_fa": "سپر دفاعی احراز هویت بدون گذرواژه و پایش تهدیدات",
            "unsplash_url": "https://images.unsplash.com/photo-1563986768609-322da13575f3?auto=format&fit=crop&w=1200&q=80"
        },
        "general_modern_saas": {
            "aspect_ratio": "aspect-[16/9] sm:aspect-[16/10]",
            "role": "workflow_orchestration",
            "overlay_style": "subtle_gradient",
            "caption": "Autonomous Multi-Agent Workflow Engine & Automation Matrix",
            "caption_fa": "موتور خودکارسازی فرآیندهای ابری و هوش مصنوعی مولد",
            "unsplash_url": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=1200&q=80"
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
        "caption_fa": "نمای تعاملی معماری و ساختار محصول",
        "unsplash_url": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=1200&q=80"
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
        aspect ratio constraints, curated high-resolution photography, and editorial caption.
        """
        spec = self.get_media_spec(domain_id)
        aspect = spec["aspect_ratio"]
        caption = spec.get("caption_fa" if is_rtl else "caption", spec["caption"])
        unsplash_url = spec.get("unsplash_url", self.DEFAULT_MEDIA_SPEC["unsplash_url"])

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
        <div className="relative overflow-hidden bg-zinc-950 {aspect} {border_cls} flex flex-col justify-between p-4 group select-none" data-origin="synthetic_demo">
          <img
            src="{unsplash_url}"
            alt="{caption}"
            loading="lazy"
            decoding="async"
            className="absolute inset-0 w-full h-full object-cover transition-transform duration-700 ease-out group-hover:scale-105 opacity-80"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-black/90 via-black/40 to-black/20 pointer-events-none" />

          <div className="flex items-center justify-between text-[11px] font-mono text-zinc-300 z-10">
            <span className="px-2 py-0.5 rounded bg-black/60 dark:bg-white/10 backdrop-blur-md border border-white/20 text-white font-bold">
              <bdi>{spec["role"].upper()}</bdi>
            </span>
            <span className="inline-flex items-center gap-1.5 text-zinc-300 font-mono text-[10px] bg-black/50 px-2 py-0.5 rounded backdrop-blur-sm border border-white/10">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
              <bdi>SYNTHETIC MEDIA SLOT — AWAITING SOURCE ASSET</bdi>
            </span>
          </div>

          <div className="z-10 -mx-4 -mb-4 p-4 text-white">
            <p className="text-xs font-semibold text-white/95 leading-snug drop-shadow-sm"><bdi>{caption}</bdi></p>
          </div>
        </div>'''
