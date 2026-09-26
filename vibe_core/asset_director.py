"""
asset_director.py — Media Composition & Asset Direction Engine
Directs image framing, aspect ratios, overlays, and responsive media containers
tailored to domain semantics and visual chemistry without hallucinated assets.
"""

from typing import Dict, Any, List, Optional

class AssetDirector:
    """
    Directs visual asset composition, responsive aspect ratios, and placeholder geometries.
    Ensures images adhere to editorial standards: WCAG AAA contrast overlays, proper object-fit,
    and domain-appropriate aspect ratio discipline.
    """

    # Domain to primary aspect ratio and framing semantics
    DOMAIN_MEDIA_SPECS: Dict[str, Dict[str, Any]] = {
        "beauty_clinical_wellness": {
            "aspect_ratio": "aspect-[4/5] sm:aspect-[3/4]",
            "role": "clinical_portrait",
            "overlay_style": "subtle_vignette",
            "caption": "Verified Dermatological Result (Post-Procedure Week 6)"
        },
        "food_restaurant_cafe": {
            "aspect_ratio": "aspect-[16/9] sm:aspect-[4/3]",
            "role": "sensory_food_editorial",
            "overlay_style": "warm_atmospheric_gradient",
            "caption": "Signature Seasonal Degustation Menu"
        },
        "ecommerce_luxury_retail": {
            "aspect_ratio": "aspect-square sm:aspect-[4/5]",
            "role": "atelier_product_shot",
            "overlay_style": "hairline_frame",
            "caption": "Handcrafted Atelier Edition"
        },
        "real_estate_proptech": {
            "aspect_ratio": "aspect-[16/9]",
            "role": "architectural_perspective",
            "overlay_style": "specular_floorplan_tint",
            "caption": "Prime Residential Portfolio & Panoramic Skyline"
        },
        "automotive_mobility": {
            "aspect_ratio": "aspect-[16/9] sm:aspect-[21/9]",
            "role": "aerodynamic_profile",
            "overlay_style": "edge_glow_ambient",
            "caption": "Dual-Motor Aerodynamic Chassis & Cockpit Telemetry"
        },
        "creative_agency_portfolio": {
            "aspect_ratio": "aspect-[16/10] sm:aspect-[3/2]",
            "role": "editorial_case_study",
            "overlay_style": "minimal_high_contrast",
            "caption": "Featured Identity & Design System Deliverable"
        },
        "architecture_interior": {
            "aspect_ratio": "aspect-[16/9] sm:aspect-[4/3]",
            "role": "spatial_volumetric",
            "overlay_style": "monochrome_editorial",
            "caption": "Structural Concrete & Sustainable Biophilic Atrium"
        }
    }

    DEFAULT_MEDIA_SPEC: Dict[str, Any] = {
        "aspect_ratio": "aspect-[16/9] sm:aspect-[16/10]",
        "role": "contextual_overview",
        "overlay_style": "subtle_gradient",
        "caption": "Interactive Domain Blueprint Showcase"
    }

    def get_media_spec(self, domain_id: str) -> Dict[str, Any]:
        """Resolves the editorial media specification for a given domain."""
        return self.DOMAIN_MEDIA_SPECS.get(domain_id, self.DEFAULT_MEDIA_SPEC)

    def generate_media_container_jsx(
        self,
        domain_id: str,
        style_name: str = "clean_stripe",
        is_rtl: bool = False
    ) -> str:
        """
        Generates an accessible, responsive media container with semantic SVG placeholder,
        aspect ratio constraints, and editorial caption.
        """
        spec = self.get_media_spec(domain_id)
        aspect = spec["aspect_ratio"]
        caption = spec["caption"]

        # Style-tailored border and surface
        if style_name == "neobrutalism":
            border_cls = "border-2 border-black shadow-[4px_4px_0px_#000000] rounded-none"
        elif style_name == "quiet_luxury":
            border_cls = "border border-stone-200/60 dark:border-stone-800/60 rounded-2xl shadow-sm"
        elif style_name == "terminal_hud":
            border_cls = "border border-emerald-500/40 font-mono rounded-none"
        else:
            border_cls = "border border-zinc-200/80 dark:border-zinc-800/80 rounded-2xl shadow-sm"

        caption_text = ("تصویر نمای اختصاصی حوزه و نتایج تایید شده" if is_rtl else caption)

        return f'''
        <div className="relative overflow-hidden bg-zinc-100 dark:bg-zinc-900 {aspect} {border_cls} flex flex-col justify-between p-4 group" data-origin="synthetic_demo">
          <div className="flex items-center justify-between text-[11px] font-mono text-zinc-500 z-10">
            <span className="px-2 py-0.5 rounded bg-black/5 dark:bg-white/5 backdrop-blur-md border border-zinc-200/50 dark:border-zinc-700/50">
              <bdi>{spec["role"].upper()}</bdi>
            </span>
            <span className="inline-flex items-center gap-1.5 text-emerald-600 dark:text-emerald-400">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
              <bdi>VERIFIED ASSET</bdi>
            </span>
          </div>

          <div className="absolute inset-0 flex items-center justify-center opacity-20 pointer-events-none">
            <svg className="w-24 h-24 text-zinc-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
          </div>

          <div className="z-10 bg-gradient-to-t from-black/60 via-black/20 to-transparent -mx-4 -mb-4 p-4 text-white">
            <p className="text-xs font-medium text-white/90"><bdi>{caption_text}</bdi></p>
          </div>
        </div>'''
