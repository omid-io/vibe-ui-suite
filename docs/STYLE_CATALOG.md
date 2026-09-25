# 🎨 Vibe UI V3 — Canonical Style Catalog (26 Orthogonal Families)

This document provides the authoritative reference catalog for all **26 orthogonal style families** in Vibe UI V3. Every style defines independent dimensions across geometry, typography, spatial density, material texture, motion physics, and anti-pattern avoid lists.

---

## Catalog Index

| # | Style ID | English Name | Persian Name | Family | Density | Elevation |
| :---: | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `minimal_swiss` | Minimal Swiss / International | سوئیسی مینیمال و دقیق | Swiss International | Dense | Flat |
| 2 | `clean_stripe` | Clean Stripe SaaS | استرایپ مدرن و شرکتی | Modern Corporate SaaS | Balanced | Micro Shadow |
| 3 | `linear_dark` | Linear Deep Dark | دارک عمیق مهندسی | Technical Dark | Dense | Diffused Soft |
| 4 | `quiet_luxury` | Quiet Luxury | مجلل آرام و اصیل | Prestige Heritage | Airy | Diffused Soft |
| 5 | `data_dense_terminal` | Data-Dense Terminal HUD | ترمینال داده محور و مونو | Monospace HUD | Dense | Flat |
| 6 | `neobrutalism` | Neo-Brutalism | نئوبروتالیسم پرانرژی | Raw High-Contrast | Balanced | Hard Drop |
| 7 | `soft_humanist` | Soft Humanist | انسان محور نرم و درمانی | Human Centered | Balanced | Micro Shadow |
| 8 | `organic_nordic` | Organic Nordic | ارگانیک نوردیک و آرام | Scandinavian Organic | Airy | Diffused Soft |
| 9 | `bauhaus_geometric` | Bauhaus Geometric | باهاوس هندسی و آوانگارد | Constructivist Geometric | Balanced | Flat |
| 10 | `modern_glass_2` | Specular Glassmorphism 2.0 | شیشه ای مدرن و کالیبره | Luminous Depth | Balanced | Specular Glass 2 |
| 11 | `retro_futurism` | Retro Futurism / Cyber | سایبرپانک و رترو-فیوچریسم | Synthwave Cybernetic | Dense | Diffused Soft |
| 12 | `editorial_magazine` | Swiss Editorial Magazine | نشریه و ادیتوریال مدرن | Editorial Typographic | Balanced | Flat |
| 13 | `industrial_utility` | Industrial Utility | صنعتی و ابزار مهندسی | Heavy Industrial | Dense | Flat |
| 14 | `biophilic_wellness` | Biophilic Wellness | زیست محور، طبیعت و آرامش | Organic Naturalist | Airy | Diffused Soft |
| 15 | `futuristic_tech` | Futuristic Aerotech HUD | فناوری آینده و هوانوردی | Aerospace Telemetry | Dense | Micro Shadow |
| 16 | `retro_computing_80s`| Retro Computing CRT Phosphor | محاسبات کلاسیک و نمایشگر فسفری | Early Digital Hardware | Dense | Flat |
| 17 | `y2k_aesthetic` | Y2K Cyber Optimism | خوش بینی دیجیتال Y2K و ژله ای | Millennium Chrome | Balanced | Specular Glass 2 |
| 18 | `enterprise_dense` | Enterprise Dense Data Grid | سازمانی داده فشرده و جدول محور | Enterprise Workflow | Dense | Micro Shadow |
| 19 | `financial_terminal` | High-Frequency Financial Terminal | ترمینال مالی و بازارهای سرمایه | Capital Markets | Dense | Flat |
| 20 | `civic_institutional` | Civic Institutional Public | نهادی و خدمات عمومی دولتی | Public Utility Governance | Balanced | Micro Shadow |
| 21 | `playful_consumer` | Playful Consumer / Bubbly | مصرف کننده شاداب و تعاملی | Consumer Engagement | Airy | Diffused Soft |
| 22 | `mobile_native_consumer` | Mobile-Native Sheet & Stack | نیتیو موبایل و ارگونومیک | Handheld Ergonomics | Balanced | Specular Glass 2 |
| 23 | `art_gallery` | Monochrome Art Gallery | گالری هنری، استوار و مینیمال | Curatorial Spatial | Airy | Flat |
| 24 | `high_end_hospitality` | High-End Hospitality & Dining | هتلداری لوکس و رستوران های مجلل | Opulent Sensory | Airy | Diffused Soft |
| 25 | `cultural_heritage` | Cultural Heritage & Archives | میراث فرهنگی، تاریخ و آرشیو | Historical Archival | Balanced | Flat |
| 26 | `scientific_dashboard` | Scientific Instrumentation & Bio | تجهیزات آزمایشگاهی و داده های علمی | Empirical Scientific | Dense | Micro Shadow |

---

## Detailed Style Specifications

### 1. Minimal Swiss / International (`minimal_swiss`)
- **Visual Rationale:** Precision mathematical grid inspired by the Swiss Style (Müller-Brockmann). Sharp borders, zero border radius, stark black and white contrast.
- **Key Signatures:** `font-sans`, `border-zinc-900`, `bg-white`, `rounded-none`, `tracking-tight`.
- **Motion:** Linear fast (\(\lambda=16\)), spring stiffness 300, damping ratio 1.0.
- **Avoid:** Generic purple gradients, soft blurry shadows, decorative emojis.
- **Ideal Domains:** Architecture, Design Systems, Legal, Publishing.

### 2. Clean Stripe SaaS (`clean_stripe`)
- **Visual Rationale:** High-conversion modern corporate web application aesthetic with subtle edge lighting, micro elevations, and comfortable whitespace.
- **Key Signatures:** `font-sans`, `border-slate-200`, `bg-slate-50`, `rounded-md`, `shadow-sm`.
- **Motion:** Spring smooth (\(\lambda=14\)), spring stiffness 260, damping ratio 0.85.
- **Avoid:** Harsh black borders, saturated neon backgrounds, playful script fonts.
- **Ideal Domains:** B2B SaaS, Payments, Cloud Infrastructure, Developer Tools.

### 3. Linear Deep Dark (`linear_dark`)
- **Visual Rationale:** Obsidian matte surface with 1px borders, specular glow accents, and tight information density tailored for engineers.
- **Key Signatures:** `font-sans`, `border-zinc-800`, `bg-zinc-950`, `text-zinc-100`, `rounded-lg`.
- **Motion:** Cubic snappy (\(\lambda=14\)), spring stiffness 280, damping ratio 0.9.
- **Avoid:** Bright white surfaces, loud saturated rainbow gradients, playful doodles.
- **Ideal Domains:** Issue Trackers, CI/CD, Crypto, AI Devtools.

### 4. Quiet Luxury (`quiet_luxury`)
- **Visual Rationale:** Generous editorial canvas with warm limestone surfaces, refined serif typography, and understated prestige.
- **Key Signatures:** `font-serif`, `border-stone-200`, `bg-stone-50`, `text-stone-900`, `tracking-wide`.
- **Motion:** Gentle float (\(\lambda=10\)), spring stiffness 180, damping ratio 1.1.
- **Avoid:** High-saturation neon, noisy flash animations, cheap plastic glass.
- **Ideal Domains:** Private Wealth, Haute Horlogerie, Luxury Real Estate, Premium Clinics.

### 5. Data-Dense Terminal HUD (`data_dense_terminal`)
- **Visual Rationale:** Monospace command center with phosphor emerald accents, tabular figures, and zero decorative fluff.
- **Key Signatures:** `font-mono`, `border-emerald-900/40`, `bg-black`, `text-emerald-400`, `tabular-nums`.
- **Motion:** Instant telemetry (\(\lambda=20\)), spring stiffness 400, damping ratio 1.2.
- **Avoid:** Rounded corners > 4px, serif fonts, large hero illustrations.
- **Ideal Domains:** Kubernetes Monitors, Cyber Security SOCs, High-Frequency Trading.

### 6. Neo-Brutalism (`neobrutalism`)
- **Visual Rationale:** Raw, unapologetic high-contrast interface featuring thick 2px black borders, solid offset drop-shadows, and vivid pigment fills.
- **Key Signatures:** `font-sans`, `border-black`, `shadow-[4px_4px_0px_0px_rgba(0,0,0,1)]`, `font-black`.
- **Motion:** Punchy pop (\(\lambda=16\)), spring stiffness 320, damping ratio 0.75.
- **Avoid:** Soft diffuse blur, low-contrast text, rounded pills, subtle glass.
- **Ideal Domains:** Creative Agencies, Indie Products, Creator Tools, Event Ticketing.

---

*(All 26 styles are programmatically loaded and validated via `data/styles.json` and tested across the test suites).*
