# 📸 Curated High-Resolution Unsplash Asset Vault (24 Canonical Domains)

A production-grade, vetted photographic asset directory and responsive CDN delivery standard for Vibe UI Suite v6.0.0. Eliminates gray placeholder rectangles, broken 404 links, and visual drift by providing verified, high-fidelity imagery across all 24 canonical industry domains.

---

## 1. Purpose & Core Philosophy

1. **Zero Gray Placeholder Boxes**: AI-generated interfaces must never resort to hollow `bg-zinc-800` boxes, generic wireframe wireframes, or low-fidelity mockup sketches. Real interfaces convey spatial balance and emotion through curated photography.
2. **Zero Broken 404 Links**: Every URL cataloged in this vault is linked to a permanent, vetted Unsplash asset identifier verified via automated HTTP status validation.
3. **WCAG AAA Contrast Overlays**: Editorial photography utilizes calibrated multi-stop gradients (`from-black/90 via-black/40 to-black/20` or dynamic OKLCH equivalents) ensuring overlay typography satisfies strict WCAG AAA ($\ge 7:1$) readability standards.
4. **Living Visual Feedback**: Grounded visual assets bridge the gap between creative prompt intent and production-ready runtime rendering.

---

## 2. Unsplash CDN Optimization Formula

Unsplash leverages imgix CDN processing parameters to perform server-side format negotiation, focal cropping, and responsive resizing.

### 2.1 Parameter Matrix

| Parameter | Purpose | Value | Technical Effect |
| :--- | :--- | :--- | :--- |
| `auto=format` | Format Negotiation | `format` | Inspects HTTP `Accept` header and automatically delivers WebP or AVIF. |
| `fit=crop` | Geometry & Cropping | `crop` | Crops precisely to target aspect ratio without anamorphic stretching. |
| `w={width}` | Coordinate Width | `1200` / `600` / `400` / `1600` | Scales image to target pixel width, optimizing payload weight. |
| `h={height}` | Coordinate Height | `400` / `900` | Defines target height when combined with specific aspect ratios. |
| `q={quality}` | Compression Quality | `80` | Delivers optimal visual fidelity while slashing byte size by up to 65%. |

### 2.2 Standard Responsive Focal Presets

- **Hero Flagship Display (16:9 / 16:10 / 21:9)**:
  `https://images.unsplash.com/{photo_id}?auto=format&fit=crop&w=1200&q=80`
  *Target payload size: ~120KB - 160KB.*
- **Feature Card & Bento Grid Slot (3:2 / 4:3)**:
  `https://images.unsplash.com/{photo_id}?auto=format&fit=crop&w=600&h=400&q=80`
  *Target payload size: ~40KB - 55KB.*
- **Square Profile / Avatar / Compact HUD (1:1)**:
  `https://images.unsplash.com/{photo_id}?auto=format&fit=crop&w=400&h=400&q=80`
  *Target payload size: ~30KB - 40KB.*
- **Ultrawide Cinema & Panorama Banner (16:9 / 21:9)**:
  `https://images.unsplash.com/{photo_id}?auto=format&fit=crop&w=1600&h=900&q=80`
  *Target payload size: ~180KB - 240KB.*

---

## 3. Master Catalog Matrix (24 Canonical Domains)

All 24 domains are mapped to permanent photo identifiers, categorized by sector, and provided with dual English and Persian semantic titles.

| # | Domain ID | Category | English Title | Persian Title | Vetted Photo ID | Recommended Aspect | Role |
| :- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `beauty_clinical_wellness` | Health & Lifestyle | Beauty, Clinical & Wellness | کلینیک زیبایی، پوست و سلامت | `photo-1629909613654-28e377c37b09` | `aspect-[4/5] sm:aspect-[3/4]` | `clinical_portrait` |
| 2 | `fintech_banking` | Finance | FinTech & Digital Banking | فین تک و بانکداری دیجیتال | `photo-1642543492481-44e81e3914a7` | `aspect-[16/9] sm:aspect-[16/10]` | `capital_portfolio` |
| 3 | `crypto_trading_web3` | Finance & Web3 | Crypto, Web3 & DeFi | رمزارز و پلتفرم معاملاتی غیرمتمرکز | `photo-1639762681485-074b7f938ba0` | `aspect-[16/9] sm:aspect-[21/9]` | `orderbook_depth` |
| 4 | `devops_cloud_terminal` | Developer Tools | DevOps & Cloud Infrastructure | دواپس و زیرساخت های ابری | `photo-1558494949-ef010cbdcc31` | `aspect-[16/10] sm:aspect-[16/9]` | `cluster_topology` |
| 5 | `saas_b2b_enterprise` | Enterprise Software | B2B Enterprise SaaS | نرم افزار سازمانی ابری | `photo-1460925895917-afdab827c52f` | `aspect-[16/9] sm:aspect-[16/10]` | `enterprise_dashboard` |
| 6 | `ai_developer_platform` | Artificial Intelligence | AI Developer Platform | پلتفرم توسعه هوش مصنوعی مولد | `photo-1618005182384-a83a8bd57fbe` | `aspect-[16/9] sm:aspect-[21/9]` | `neural_latent_canvas` |
| 7 | `ecommerce_luxury_fashion` | Luxury Retail | Haute Horology & Luxury Fashion | مد فاخر و ساعت سازی لوکس | `photo-1539109136881-3be0616acf4b` | `aspect-square sm:aspect-[4/5]` | `atelier_lookbook` |
| 8 | `ecommerce_mass_market` | Retail & Commerce | E-Commerce Retail Storefront | فروشگاه آنلاین و خرده فروشی دیجیتال | `photo-1441986300917-64674bd600d8` | `aspect-square sm:aspect-[4/3]` | `product_catalog_showcase` |
| 9 | `real_estate_architecture` | Real Estate | Prime Architecture & Real Estate | املاک لوکس و معماری معاصر | `photo-1600585154340-be6161a56a0c` | `aspect-[16/9] sm:aspect-[3/2]` | `architectural_perspective` |
| 10 | `healthcare_hospital_medical` | Healthcare | Hospital & Clinical Diagnostics | بیمارستان و خدمات تشخیصی سلامت | `photo-1519494026892-80bbd2d6fd0d` | `aspect-[4/3] sm:aspect-[16/10]` | `clinical_diagnostic` |
| 11 | `education_edtech_lms` | Education | EdTech & Digital Learning | سامانه آموزش تعاملی و دانشگاهی | `photo-1523240795612-9a054b0db644` | `aspect-[16/9] sm:aspect-[16/10]` | `curriculum_interactive` |
| 12 | `creative_portfolio_agency` | Design & Creative | Creative Design Agency | استودیو طراحی خلاق و برندینگ | `photo-1507238691740-187a5b1d37b8` | `aspect-[16/10] sm:aspect-[3/2]` | `editorial_case_study` |
| 13 | `media_editorial_magazine` | Media & Publishing | Editorial Media & Longform Journalism | نشریه تخصصی و رسانه تحلیلی | `photo-1505373877841-8d25f7d46678` | `aspect-[3/4] sm:aspect-[4/5]` | `longform_journalism` |
| 14 | `food_restaurant_cafe` | Food & Hospitality | Artisanal Food & Restaurant | رستوران و کافه تجربی | `photo-1555396273-367ea4eb4db5` | `aspect-[16/9] sm:aspect-[4/3]` | `sensory_food_editorial` |
| 15 | `travel_hospitality_tourism` | Hospitality & Travel | Luxury Travel & Hospitality | هتل داری و گردشگری لوکس | `photo-1566073771259-6a8506099945` | `aspect-[16/9] sm:aspect-[3/2]` | `destination_panoramic` |
| 16 | `legal_compliance_law` | Legal & Corporate | Legal & Corporate Compliance | مشاوره حقوقی و ممیزی مقرراتی | `photo-1589829545856-d10d557cf95f` | `aspect-[16/9] sm:aspect-[4/3]` | `statutory_compliance` |
| 17 | `gaming_entertainment_streaming` | Gaming & Media | Esports & Interactive Gaming | گیمینگ و استریمینگ تعاملی | `photo-1542751371-adc38448a05e` | `aspect-[16/9] sm:aspect-[21/9]` | `gameplay_cinematic` |
| 18 | `automotive_ev_mobility` | Automotive | Next-Gen EV Mobility & Automotive | خودروهای برقی و حمل ونقل نوین | `photo-1617814076367-b759c7d7e738` | `aspect-[16/9] sm:aspect-[21/9]` | `aerodynamic_chassis` |
| 19 | `logistics_supply_chain` | Logistics | Global Freight & Supply Chain | لجستیک بین الملل و زنجیره تامین | `photo-1586528116311-ad8dd3c8310d` | `aspect-[16/9] sm:aspect-[16/10]` | `supply_telematics` |
| 20 | `energy_greentech_sustainability` | CleanTech & Energy | GreenTech & Clean Energy Grid | انرژی پاک و فناوری های پایدار | `photo-1497435334941-8c899ee9e8e9` | `aspect-[16/9] sm:aspect-[3/2]` | `renewable_grid` |
| 21 | `nonprofit_charity_social` | Social Impact | Social Impact & Humanitarian Aid | توانمندسازی مدنی و امور بشردوستانه | `photo-1488521787991-ed7bbaae773c` | `aspect-[16/9] sm:aspect-[4/3]` | `humanitarian_impact` |
| 22 | `personal_branding_creator` | Creator Economy | Executive Personal Branding | برند شخصی و تولید محتوای تخصصی | `photo-1534528741775-53994a69daeb` | `aspect-[4/5] sm:aspect-[1/1]` | `creator_signature` |
| 23 | `cybersecurity_identity_auth` | Cybersecurity | Zero-Trust Cybersecurity | امنیت ابری و احراز هویت یکپارچه | `photo-1563986768609-322da13575f3` | `aspect-[16/9] sm:aspect-[21/9]` | `zero_trust_matrix` |
| 24 | `general_modern_saas` | Cloud Software | General Modern Cloud SaaS | نرم افزار ابری نوین و اتوماسیون | `photo-1551288049-bebda4e38f71` | `aspect-[16/9] sm:aspect-[16/10]` | `workflow_orchestration` |

---

## 4. Standardized Accessible HTML Markup Patterns

### 4.1 Responsive Hero `<picture>` Implementation

Use when the asset is placed above-the-fold or requires dynamic viewport density negotiation.

```html
<figure class="relative overflow-hidden rounded-3xl bg-zinc-950 aspect-[16/9] sm:aspect-[21/9] border border-zinc-200/20 dark:border-zinc-800/80 shadow-2xl group select-none m-0" data-origin="synthetic_demo">
  <picture>
    <source
      media="(min-width: 1024px)"
      srcset="https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=1600&h=900&q=80"
    />
    <source
      media="(min-width: 640px)"
      srcset="https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=1200&q=80"
    />
    <img
      src="https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=600&h=400&q=80"
      alt="Transformer Attention Map and Cluster Latency Telemetry"
      loading="eager"
      fetchpriority="high"
      decoding="async"
      class="absolute inset-0 w-full h-full object-cover transition-transform duration-700 ease-out group-hover:scale-105 opacity-85"
    />
  </picture>

  <!-- WCAG AAA Calibrated Contrast Overlay -->
  <div class="absolute inset-0 bg-gradient-to-t from-black/95 via-black/40 to-black/20 pointer-events-none" />

  <!-- Synthetic Slot Demarcation Badge -->
  <div class="absolute top-4 start-4 end-4 flex items-center justify-between text-[11px] font-mono text-zinc-300 z-10">
    <span class="px-2.5 py-0.5 rounded-full bg-black/60 dark:bg-white/10 backdrop-blur-md border border-white/20 text-white font-semibold">
      <bdi>NEURAL_LATENT_CANVAS</bdi>
    </span>
    <span class="inline-flex items-center gap-1.5 text-zinc-300 font-mono text-[10px] bg-black/50 px-2.5 py-0.5 rounded-full backdrop-blur-sm border border-white/10">
      <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
      <bdi>SYNTHETIC MEDIA SLOT — AWAITING SOURCE ASSET</bdi>
    </span>
  </div>

  <!-- Editorial Caption with Bidirectional Isolation -->
  <figcaption class="absolute bottom-0 inset-x-0 p-6 z-10 text-white">
    <p class="text-sm font-medium text-white/95 leading-relaxed drop-shadow-sm">
      <bdi>Transformer Attention Map & Cluster Latency Telemetry</bdi>
    </p>
  </figcaption>
</figure>
```

### 4.2 Bento Grid Feature Card `<img>` Implementation

Use when the asset resides in a multi-card grid, feature section, or below-the-fold catalog.

```html
<div class="relative overflow-hidden rounded-2xl bg-zinc-950 aspect-[3/2] border border-zinc-200/80 dark:border-zinc-800/80 shadow-md group select-none" data-origin="synthetic_demo">
  <img
    src="https://images.unsplash.com/photo-1642543492481-44e81e3914a7?auto=format&fit=crop&w=600&h=400&q=80"
    alt="Smart Capital Allocation and Real-Time Liquidity Chart"
    loading="lazy"
    decoding="async"
    class="absolute inset-0 w-full h-full object-cover transition-transform duration-500 ease-out group-hover:scale-105 opacity-80"
  />

  <div class="absolute inset-0 bg-gradient-to-t from-black/90 via-black/35 to-transparent pointer-events-none" />

  <div class="absolute top-3 start-3 end-3 flex items-center justify-between text-[10px] font-mono text-zinc-300 z-10">
    <span class="px-2 py-0.5 rounded bg-black/60 backdrop-blur-md border border-white/15 text-white font-bold">
      <bdi>CAPITAL_PORTFOLIO</bdi>
    </span>
    <span class="inline-flex items-center gap-1 text-[9px] text-zinc-300 bg-black/40 px-2 py-0.5 rounded backdrop-blur-sm border border-white/10">
      <span class="w-1 h-1 rounded-full bg-emerald-400 animate-pulse"></span>
      <bdi>SYNTHETIC MEDIA</bdi>
    </span>
  </div>

  <div class="absolute bottom-0 inset-x-0 p-4 z-10 text-white">
    <p class="text-xs font-semibold text-white/95 leading-snug">
      <bdi>Smart Capital Allocation & Real-Time Liquidity Chart</bdi>
    </p>
  </div>
</div>
```

---

## 5. React 19 Living TSX Component Pattern

The following component provides a unified, typed interface for rendering curated domain assets with zero configuration, dynamic fallbacks, and bidirectional isolation.

```tsx
import React, { useState } from "react";

export type VaultVariant = "hero" | "card" | "square" | "wide";

export interface CuratedMediaAssetProps {
  domainId: string;
  variant?: VaultVariant;
  styleName?: "clean_stripe" | "neobrutalism" | "quiet_luxury" | "terminal_hud";
  isRtl?: boolean;
  customCaption?: string;
  className?: string;
}

interface DomainSpec {
  photoId: string;
  aspectRatio: string;
  role: string;
  captionEn: string;
  captionFa: string;
  altText: string;
}

const VAULT_REGISTRY: Record<string, DomainSpec> = {
  beauty_clinical_wellness: {
    photoId: "photo-1629909613654-28e377c37b09",
    aspectRatio: "aspect-[4/5] sm:aspect-[3/4]",
    role: "clinical_portrait",
    captionEn: "Clinical Outcome Visual Slot (Laser Rejuvenation Protocol)",
    captionFa: "فریم نتایج بالینی جوانسازی پوست و پروتکل درمانی",
    altText: "Clinical outcome visual slot for dermatology and laser therapy",
  },
  fintech_banking: {
    photoId: "photo-1642543492481-44e81e3914a7",
    aspectRatio: "aspect-[16/9] sm:aspect-[16/10]",
    role: "capital_portfolio",
    captionEn: "Smart Capital Allocation & Real-Time Liquidity Chart",
    captionFa: "نمودار تخصیص سرمایه هوشمند و شاخص نقدشوندگی",
    altText: "Real-time financial capital allocation dashboard and analytics",
  },
  crypto_trading_web3: {
    photoId: "photo-1639762681485-074b7f938ba0",
    aspectRatio: "aspect-[16/9] sm:aspect-[21/9]",
    role: "orderbook_depth",
    captionEn: "Aggregated Liquidity Depth & Low-Slippage Routing Matrix",
    captionFa: "عمق نقدینگی صرافی نامتمرکز و ماتریکس مسیریابی",
    altText: "Decentralized crypto orderbook depth and liquidity routing visualization",
  },
  devops_cloud_terminal: {
    photoId: "photo-1558494949-ef010cbdcc31",
    aspectRatio: "aspect-[16/10] sm:aspect-[16/9]",
    role: "cluster_topology",
    captionEn: "Multi-Region Kubernetes Pod Topology & Egress Flow",
    captionFa: "توپولوژی نودهای ابری کوبرنتیز و مسیرهای شبکه",
    altText: "High-density cloud server racks and Kubernetes network infrastructure",
  },
  saas_b2b_enterprise: {
    photoId: "photo-1460925895917-afdab827c52f",
    aspectRatio: "aspect-[16/9] sm:aspect-[16/10]",
    role: "enterprise_dashboard",
    captionEn: "Unified Enterprise Orchestration & Provisioning Suite",
    captionFa: "داشبورد یکپارچه مدیریت فرآیندهای سازمانی",
    altText: "Enterprise dashboard analytics and business performance metrics",
  },
  ai_developer_platform: {
    photoId: "photo-1618005182384-a83a8bd57fbe",
    aspectRatio: "aspect-[16/9] sm:aspect-[21/9]",
    role: "neural_latent_canvas",
    captionEn: "Transformer Attention Map & Cluster Latency Telemetry",
    captionFa: "نقشه توجه لایه های هوش مصنوعی و تله متری کلاستر GPU",
    altText: "Generative neural latent spectrum and abstract compute visualization",
  },
  ecommerce_luxury_fashion: {
    photoId: "photo-1539109136881-3be0616acf4b",
    aspectRatio: "aspect-square sm:aspect-[4/5]",
    role: "atelier_lookbook",
    captionEn: "Handcrafted Bespoke Atelier Collection • Limited Edition",
    captionFa: "کلکسیون دست دوز آتلیه مد اختصاصی با پارچه های ارگانیک",
    altText: "High-fashion editorial model in bespoke luxury designer garments",
  },
  ecommerce_mass_market: {
    photoId: "photo-1441986300917-64674bd600d8",
    aspectRatio: "aspect-square sm:aspect-[4/3]",
    role: "product_catalog_showcase",
    captionEn: "Dynamic Catalog Showcase with Tiered Volume Discounts",
    captionFa: "کاتالوگ محصولات با اعمال آنی تخفیف های پلکانی",
    altText: "Modern bright retail storefront display and product collection",
  },
  real_estate_architecture: {
    photoId: "photo-1600585154340-be6161a56a0c",
    aspectRatio: "aspect-[16/9] sm:aspect-[3/2]",
    role: "architectural_perspective",
    captionEn: "Prime Residential Penthouse Portfolio & Skyline View",
    captionFa: "پلان معماری پنت هاوس اختصاصی و چشم انداز پانوراما",
    altText: "Contemporary luxury architectural villa with warm ambient lighting",
  },
  healthcare_hospital_medical: {
    photoId: "photo-1519494026892-80bbd2d6fd0d",
    aspectRatio: "aspect-[4/3] sm:aspect-[16/10]",
    role: "clinical_diagnostic",
    captionEn: "FHIR-Compliant Electronic Health Record & Tele-Triage",
    captionFa: "پرونده الکترونیک سلامت و تریاژ هوشمند بالینی",
    altText: "Clean modern hospital corridor and clinical medical diagnostic facility",
  },
  education_edtech_lms: {
    photoId: "photo-1523240795612-9a054b0db644",
    aspectRatio: "aspect-[16/9] sm:aspect-[16/10]",
    role: "curriculum_interactive",
    captionEn: "Adaptive Learning Graph & Mastery Certification Track",
    captionFa: "مسیر یادگیری انطباقی و گراف تسلط بر مهارت ها",
    altText: "University students collaborating with digital laptops and learning materials",
  },
  creative_portfolio_agency: {
    photoId: "photo-1507238691740-187a5b1d37b8",
    aspectRatio: "aspect-[16/10] sm:aspect-[3/2]",
    role: "editorial_case_study",
    captionEn: "Award-Winning Brand Identity & Design System Deliverable",
    captionFa: "نمونه کار هویت بصری جامع و سیستم طراحی برند",
    altText: "Designer workspace with sketches, brand typography, and laptop displays",
  },
  media_editorial_magazine: {
    photoId: "photo-1505373877841-8d25f7d46678",
    aspectRatio: "aspect-[3/4] sm:aspect-[4/5]",
    role: "longform_journalism",
    captionEn: "Investigative Edition Cover • Independent Journalism",
    captionFa: "گزارش ویژه تحلیلی و روزنامه نگاری مستقل",
    altText: "Large keynote conference hall and editorial symposium auditorium",
  },
  food_restaurant_cafe: {
    photoId: "photo-1555396273-367ea4eb4db5",
    aspectRatio: "aspect-[16/9] sm:aspect-[4/3]",
    role: "sensory_food_editorial",
    captionEn: "Signature Seasonal Degustation Menu Presentation",
    captionFa: "معرفی منوی فصلی سرآشپز و هنر آشپزی ارگانیک",
    altText: "Gourmet dining restaurant interior with ambient warm chandeliers and tables",
  },
  travel_hospitality_tourism: {
    photoId: "photo-1566073771259-6a8506099945",
    aspectRatio: "aspect-[16/9] sm:aspect-[3/2]",
    role: "destination_panoramic",
    captionEn: "Exclusive Coastal Villa Retreat & Private Heliport",
    captionFa: "ویلای ساحلی اختصاصی و چشم انداز طبیعی بکر",
    altText: "Luxury resort infinity pool overlooking tranquil coastal waters",
  },
  legal_compliance_law: {
    photoId: "photo-1589829545856-d10d557cf95f",
    aspectRatio: "aspect-[16/9] sm:aspect-[4/3]",
    role: "statutory_compliance",
    captionEn: "Cross-Border Regulatory Compliance & Audit Assurance",
    captionFa: "ممیزی مقرراتی حقوقی بین المللی و تطبیق استانداردها",
    altText: "Classic brass Lady Justice scales and legal reference volumes in library",
  },
  gaming_entertainment_streaming: {
    photoId: "photo-1542751371-adc38448a05e",
    aspectRatio: "aspect-[16/9] sm:aspect-[21/9]",
    role: "gameplay_cinematic",
    captionEn: "Real-Time 4K Raytraced Stream & Sub-Millisecond Tickrate",
    captionFa: "استریم با کیفیت 4K و تاخیر شبکه نزدیک به صفر",
    altText: "High-end esports gaming battlestation with neon ambient RGB lighting",
  },
  automotive_ev_mobility: {
    photoId: "photo-1617814076367-b759c7d7e738",
    aspectRatio: "aspect-[16/9] sm:aspect-[21/9]",
    role: "aerodynamic_chassis",
    captionEn: "Silicon-Carbide 800V Powertrain & Telemetry Matrix",
    captionFa: "شاسی آیرودینامیک و سیستم محرکه پیشرفته ۸۰۰ ولت",
    altText: "Sleek aerodynamic electric sports car profile with laser LED headlights",
  },
  logistics_supply_chain: {
    photoId: "photo-1586528116311-ad8dd3c8310d",
    aspectRatio: "aspect-[16/9] sm:aspect-[16/10]",
    role: "supply_telematics",
    captionEn: "Autonomous Global Freight Corridor & Fleet Tracking",
    captionFa: "مسیریابی هوشمند ناوگان ترانزیت و نظارت بر بار",
    altText: "High-bay automated logistics fulfillment warehouse with organized cargo pallets",
  },
  energy_greentech_sustainability: {
    photoId: "photo-1497435334941-8c899ee9e8e9",
    aspectRatio: "aspect-[16/9] sm:aspect-[3/2]",
    role: "renewable_grid",
    captionEn: "Megawatt Solar Array & Battery Energy Storage System (BESS)",
    captionFa: "نیروگاه خورشیدی متصل به شبکه و ذخیره سازی انرژی",
    altText: "Expansive photovoltaic solar farm panels basking in bright natural sunlight",
  },
  nonprofit_charity_social: {
    photoId: "photo-1488521787991-ed7bbaae773c",
    aspectRatio: "aspect-[16/9] sm:aspect-[4/3]",
    role: "humanitarian_impact",
    captionEn: "On-the-Ground Direct Clean Water Installation & Solar Pump",
    captionFa: "پروژه میدانی دسترسی مستقیم به آب پاک و توسعه پایدار",
    altText: "Heartwarming community volunteers and children engaged in humanitarian support",
  },
  personal_branding_creator: {
    photoId: "photo-1534528741775-53994a69daeb",
    aspectRatio: "aspect-[4/5] sm:aspect-[1/1]",
    role: "creator_signature",
    captionEn: "Curated Thought-Leadership Digest & Audio Studio Edition",
    captionFa: "استودیوی اختصاصی تولید محتوای تخصصی و خبرنامه",
    altText: "High-fashion executive portrait with natural studio lighting and warm tones",
  },
  cybersecurity_identity_auth: {
    photoId: "photo-1563986768609-322da13575f3",
    aspectRatio: "aspect-[16/9] sm:aspect-[21/9]",
    role: "zero_trust_matrix",
    captionEn: "Continuous Behavioral Anomaly Detection & Zero-Trust Shield",
    captionFa: "سپر دفاعی احراز هویت بدون گذرواژه و پایش تهدیدات",
    altText: "Modern cybersecurity operations screen monitoring network traffic and digital locks",
  },
  general_modern_saas: {
    photoId: "photo-1551288049-bebda4e38f71",
    aspectRatio: "aspect-[16/9] sm:aspect-[16/10]",
    role: "workflow_orchestration",
    captionEn: "Autonomous Multi-Agent Workflow Engine & Automation Matrix",
    captionFa: "موتور خودکارسازی فرآیندهای ابری و هوش مصنوعی مولد",
    altText: "Interactive modern cloud SaaS data analytics charts and collaboration platform",
  },
};

const DEFAULT_SPEC: DomainSpec = {
  photoId: "photo-1551288049-bebda4e38f71",
  aspectRatio: "aspect-[16/9] sm:aspect-[16/10]",
  role: "workflow_orchestration",
  captionEn: "Autonomous Multi-Agent Workflow Engine & Automation Matrix",
  captionFa: "موتور خودکارسازی فرآیندهای ابری و هوش مصنوعی مولد",
  altText: "Cloud workflow automation analytics dashboard",
};

export const CuratedMediaAsset: React.FC<CuratedMediaAssetProps> = ({
  domainId,
  variant = "hero",
  styleName = "clean_stripe",
  isRtl = false,
  customCaption,
  className = "",
}) => {
  const [hasError, setHasError] = useState(false);
  const spec = VAULT_REGISTRY[domainId] || DEFAULT_SPEC;

  // Build focal CDN URL
  const buildUrl = (photoId: string, v: VaultVariant): string => {
    const base = `https://images.unsplash.com/${photoId}?auto=format&fit=crop`;
    switch (v) {
      case "card":
        return `${base}&w=600&h=400&q=80`;
      case "square":
        return `${base}&w=400&h=400&q=80`;
      case "wide":
        return `${base}&w=1600&h=900&q=80`;
      case "hero":
      default:
        return `${base}&w=1200&q=80`;
    }
  };

  const imgUrl = buildUrl(spec.photoId, variant);
  const caption = customCaption || (isRtl ? spec.captionFa : spec.captionEn);

  // Surface border class mapping
  let borderClass = "border border-zinc-200/80 dark:border-zinc-800/80 rounded-2xl shadow-sm";
  if (styleName === "neobrutalism") {
    borderClass = "border-2 border-black shadow-[4px_4px_0px_#000000] rounded-none";
  } else if (styleName === "quiet_luxury") {
    borderClass = "border border-stone-200/60 dark:border-stone-800/60 rounded-2xl shadow-sm";
  } else if (styleName === "terminal_hud") {
    borderClass = "border border-emerald-500/40 font-mono rounded-none";
  }

  const aspectClass = variant === "card" ? "aspect-[3/2]" : variant === "square" ? "aspect-square" : spec.aspectRatio;

  return (
    <div
      className={`relative overflow-hidden bg-zinc-950 ${aspectClass} ${borderClass} flex flex-col justify-between p-4 group select-none ${className}`}
      data-origin="synthetic_demo"
    >
      {!hasError ? (
        <img
          src={imgUrl}
          alt={spec.altText}
          loading={variant === "hero" ? "eager" : "lazy"}
          decoding="async"
          onError={() => setHasError(true)}
          className="absolute inset-0 w-full h-full object-cover transition-transform duration-700 ease-out group-hover:scale-105 opacity-80"
        />
      ) : (
        <div className="absolute inset-0 bg-gradient-to-br from-zinc-900 via-zinc-950 to-black flex items-center justify-center p-6 text-center">
          <span className="font-mono text-xs text-zinc-500 uppercase tracking-widest">
            Media Asset Fallback — {spec.role}
          </span>
        </div>
      )}

      {/* WCAG AAA Contrast Layer */}
      <div className="absolute inset-0 bg-gradient-to-t from-black/95 via-black/40 to-black/20 pointer-events-none" />

      {/* Top HUD Controls */}
      <div className="flex items-center justify-between text-[11px] font-mono text-zinc-300 z-10">
        <span className="px-2 py-0.5 rounded bg-black/60 dark:bg-white/10 backdrop-blur-md border border-white/20 text-white font-bold">
          <bdi>{spec.role.toUpperCase()}</bdi>
        </span>
        <span className="inline-flex items-center gap-1.5 text-zinc-300 font-mono text-[10px] bg-black/50 px-2 py-0.5 rounded backdrop-blur-sm border border-white/10">
          <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
          <bdi>SYNTHETIC MEDIA SLOT — AWAITING SOURCE ASSET</bdi>
        </span>
      </div>

      {/* Bottom Editorial Caption */}
      <div className="z-10 -mx-4 -mb-4 p-4 text-white">
        <p className="text-xs font-semibold text-white/95 leading-snug drop-shadow-sm">
          <bdi>{caption}</bdi>
        </p>
      </div>
    </div>
  );
};
```

---

## 6. BiDi & Fixed-Structure RTL Handling

When deploying components across Persian, Arabic, or bilingual viewports:

1. **Macro Coordinate Stability**: Layout coordinates, grid columns, and card boundaries remain physically stable. Do not indiscriminately invert overall column flow or flip horizontal aspect ratios.
2. **Bidirectional Isolation with `<bdi>`**:
   Mixed English identifiers, brand names, or technical terms inside Persian captions must not corrupt punctuation or scramble reading order. Every dynamic caption, role tag, and telemetry metric must be encapsulated inside `<bdi>`:
   ```html
   <p><bdi>کلینیک زیبایی، پوست و سلامت (Clinical Outcome Protocol)</bdi></p>
   ```
3. **Strict Zero ZWNJ Protocol**:
   All Persian strings in code, configuration, and documentation must use standard spaces exclusively. The zero-width non-joiner character (`\u200c`) is strictly prohibited.
4. **Directional CSS Logical Properties**:
   Use `start-*`, `end-*`, `ms-*`, and `me-*` instead of static `left-*` and `right-*` to ensure natural bidirectional adaptation.

---

## 7. Synthetic Demarcation Badge & CSS Fallbacks

### 7.1 The Synthetic Demarcation Contract

To maintain full transparency and trust during development and client preview cycles, media assets generated by the AI agent must carry a clear synthetic demarcation badge:

```html
<span class="inline-flex items-center gap-1.5 text-zinc-300 font-mono text-[10px] bg-black/50 px-2 py-0.5 rounded backdrop-blur-sm border border-white/10">
  <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
  <bdi>SYNTHETIC MEDIA SLOT — AWAITING SOURCE ASSET</bdi>
</span>
```

### 7.2 Graceful CSS Gradient Fallbacks

In offline sandboxes or restricted network environments where external CDN calls are blocked, media containers gracefully fall back to domain-calibrated CSS gradients:

```css
/* Dark surface fallback with radial depth */
.media-fallback-gradient {
  background: radial-gradient(circle at 50% 30%, oklch(0.25 0.04 260), oklch(0.12 0.01 260));
}

/* Light surface fallback with subtle ambient illumination */
.media-fallback-gradient-light {
  background: radial-gradient(circle at 50% 20%, oklch(0.96 0.02 240), oklch(0.91 0.01 240));
}
```
