#!/usr/bin/env python3
"""
scripts/update_studio_26_styles.py
Generates full 26-style interactive scenarios for Vibe UI Studio in index.html & showcase/index.html.
Each style includes:
- Prompt (EN & FA)
- Inferred Domain & Confidence
- Style & Material DNA
- Decision Trace & Forbidden Patterns
- Mathematical WCAG Contrast & Quality Scorecard
- Tailwind CSS Component Code matching the style's canonical genome
"""

import json
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parent.parent
INDEX_PATH = ROOT_DIR / "index.html"
SHOWCASE_PATH = ROOT_DIR / "showcase" / "index.html"
STYLES_JSON = ROOT_DIR / "data" / "styles.json"

def get_scenarios():
    return {
        # 1. Linear Deep Dark (Fintech / Crypto)
        "crypto": {
            "prompt_en": "Decentralized crypto swap with real-time orderbook, live depth chart, and zero gas routing",
            "prompt_fa": "صرافی غیرمتمرکز رمزارز با ثبت آنی سفارشات، دفتر معاملات لایو، و معامله بدون کارمزد",
            "domain": "fintech_banking",
            "confidence": "97%",
            "style_en": "Linear Deep Dark (Technical HUD)",
            "style_fa": "دارک عمیق مهندسی (Linear HUD)",
            "material_en": "Obsidian Matte + Tabular Matrix (Dense)",
            "material_fa": "ابسیدین مات + ماتریس جدولی داده محور",
            "decision_en": "High-frequency trading context mandates zero blur, tabular font numerals, and high-visibility status tags.",
            "decision_fa": "کانتکست معاملات رمزارز نیازمند حذف هرگونه بلر، فونت اعداد جدولی و تگ های استاتوس پرکنتراست است.",
            "avoid_en": "Zero raw emojis, no soft blurry shadows, no pastel washes, no low-contrast text.",
            "avoid_fa": "صفر اموجی خام، بدون سایه های محو شلخته، بدون رنگ های پاستلی کم رنگ.",
            "contrast": "17.8 : 1 (AAA)",
            "quality": "98 / 100",
            "touch": "48px (Compliant)",
            "bidi": "Preserved (Vazirmatn)",
            "title_en": "ETH / USDT Perpetual Contract",
            "title_fa": "قرارداد فیوچرز دائمی ETH / USDT",
            "subtitle_en": "Index Price: $3,482.50 • 24h Vol: $1.82B",
            "subtitle_fa": "قیمت شاخص: $3,482.50 • حجم ۲۴ ساعته: $1.82B",
            "badge_en": "LIVE 120HZ",
            "badge_fa": "نرخ زنده ۱۲۰ هرتز",
            "value": "$3,482.50",
            "subval_en": "+4.25% (+$142.10)",
            "subval_fa": "+۴.۲۵٪ (+$142.10)",
            "action_en": "Execute Instant Swap",
            "action_fa": "اجرای معامله آنی",
            "secondary_en": "Order History",
            "secondary_fa": "تاریخچه سفارشات",
            "codeTailwind": """<div class="rounded-xl border border-zinc-800 bg-zinc-950 p-5 text-zinc-100 font-sans shadow-2xl">
  <div class="flex items-center justify-between border-b border-zinc-800 pb-3">
    <div class="flex items-center gap-2">
      <span class="h-2.5 w-2.5 rounded-full bg-emerald-500 animate-pulse"></span>
      <h3 class="font-mono text-sm font-semibold tracking-wide">ETH / USDT</h3>
    </div>
    <span class="rounded bg-emerald-950/60 px-2 py-0.5 font-mono text-xs text-emerald-400 border border-emerald-800/40">LIVE</span>
  </div>
  <div class="my-4">
    <div class="font-mono text-2xl font-bold tracking-tight text-white">$3,482.50</div>
    <div class="text-xs text-emerald-400 font-mono mt-0.5">+4.25% (24h high: $3,510.00)</div>
  </div>
  <button type="button" class="w-full rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white font-medium py-2.5 text-xs transition-colors">Execute Instant Swap</button>
</div>"""
        },

        # 2. Data-Dense Terminal HUD (DevOps / Kubernetes)
        "k8s": {
            "prompt_en": "High-Throughput Kubernetes Cluster Observability HUD with CPU core saturation telemetry",
            "prompt_fa": "سامانه پایش زیرساخت کلاستر کوبرنتیز و نرخ اشغال هسته های پردازشی سرور",
            "domain": "dev_tools_terminal",
            "confidence": "95%",
            "style_en": "Data-Dense Terminal HUD (Monospace)",
            "style_fa": "ترمینال داده محور و مونو اسپیس HUD",
            "material_en": "Pitch Black + Phosphor Matrix",
            "material_fa": "مشکی مطلق + ماتریکس فسفری",
            "decision_en": "SRE incident response mandates instant scannability, strict 0px radius, and high-density tabular grid.",
            "decision_fa": "پایش سریع زیرساخت نیازمند اسکن فوری چشم، گوشه های ۰ پیکسل و گرید داده با تراکم بالا است.",
            "avoid_en": "Rounded pills above 4px, decorative gradients, serif typography, slow animations.",
            "avoid_fa": "انحنای بالای ۴ پیکسل، گرادیان های تزئینی، تایپوگرافی سریف، انیمیشن های کند.",
            "contrast": "19.4 : 1 (AAA)",
            "quality": "99 / 100",
            "touch": "44px (Compliant)",
            "bidi": "LTR Fixed Coordinates",
            "title_en": "Cluster: prod-us-east-1a",
            "title_fa": "کلاستر: prod-us-east-1a",
            "subtitle_en": "128 Nodes • 1,420 Pods Active",
            "subtitle_fa": "۱۲۸ نود فعال • ۱۴۲۰ پاد در حال اجرا",
            "badge_en": "STATUS: NOMINAL",
            "badge_fa": "وضعیت: پایدار",
            "value": "99.98% Healthy",
            "subval_en": "Avg P99 Latency: 4.2ms",
            "subval_fa": "میانگین تاخیر P99: ۴.۲ میلی ثانیه",
            "action_en": "Inspect Pod Metrics",
            "action_fa": "بررسی متریک های پاد",
            "secondary_en": "View CrashLoopLogs",
            "secondary_fa": "لاگ های زنده کرش",
            "codeTailwind": """<div class="rounded-none border border-emerald-900/60 bg-black p-5 text-emerald-400 font-mono">
  <div class="flex items-center justify-between border-b border-emerald-950 pb-2 text-xs">
    <span>SYSTEM TELEMETRY HUD</span>
    <span class="text-emerald-300 animate-pulse">RECORDING 60FPS</span>
  </div>
  <div class="my-4 space-y-1">
    <div class="text-3xl font-bold tracking-wider text-emerald-300">99.98%</div>
    <p class="text-xs text-emerald-500">Nodes Healthy: 128 / 128 • P99: 4.2ms</p>
  </div>
  <button type="button" class="w-full border border-emerald-500 bg-emerald-950/40 hover:bg-emerald-900/60 text-emerald-200 py-2 text-xs uppercase tracking-wider">Inspect Pod Metrics</button>
</div>"""
        },

        # 3. Quiet Luxury (Architecture / Real Estate)
        "luxury": {
            "prompt_en": "Luxury Architecture & Penthouse Portfolio with curated gallery and private viewing request",
            "prompt_fa": "پورتفولیو پنت هاوس و معماری لوکس نیاوران با گالری عکس و رزرو اختصاصی بازدید",
            "domain": "real_estate_architecture",
            "confidence": "96%",
            "style_en": "Quiet Luxury (Prestige Heritage)",
            "style_fa": "مجلل آرام و اصیل (Quiet Luxury)",
            "material_en": "Warm Limestone + Editorial Serif",
            "material_fa": "سنگ آهک گرم + سریف ادیتوریال",
            "decision_en": "Ultra-high-net-worth persona requires 180% increased whitespace, understated serif typography, and zero flashy motion.",
            "decision_fa": "پرسونای لوکس نیازمند ۱۸۰٪ فضای تنفس بیشتر، فونت سریف باوقار و حذف انیمیشن های پرسرعت است.",
            "avoid_en": "Saturated neon gradients, bouncy animations, harsh black borders, cheap plastic glass.",
            "avoid_fa": "گرادیان های اشباع نئونی، انیمیشن های جهنده، بوردرهای تیز مشکی، افکت های شیشه ای پلاستیکی.",
            "contrast": "15.6 : 1 (AAA)",
            "quality": "96 / 100",
            "touch": "48px (Compliant)",
            "bidi": "Editorial RTL Balanced",
            "title_en": "The Royal Court Penthouse",
            "title_fa": "پنت هاوس نیاوران رویال کورت",
            "subtitle_en": "720 sq.m Duplex • 360 Panoramic Views",
            "subtitle_fa": "۷۲۰ متر دوبلکس • دید ابدی ۳۶۰ درجه البرز",
            "badge_en": "BY INVITATION",
            "badge_fa": "رزرو اختصاصی",
            "value": "Niavaran Royal Penthouse",
            "subval_en": "Handover Autumn 2026 • Milan Studio Design",
            "subval_fa": "تحویل پاییز ۲۰۲۶ • طراحی دفتر معماری میلان",
            "action_en": "Request Private Viewing",
            "action_fa": "درخواست بازدید خصوصی",
            "secondary_en": "Download Monograph",
            "secondary_fa": "دانلود مونوگراف معماری",
            "codeTailwind": """<div class="rounded border border-stone-200 bg-stone-50 p-6 text-stone-900 font-serif shadow-sm">
  <div class="flex items-center justify-between border-b border-stone-200 pb-3">
    <span class="text-xs uppercase tracking-widest text-stone-500 font-sans">Niavaran Residence</span>
    <span class="text-xs italic text-stone-600">By Invitation Only</span>
  </div>
  <div class="my-5">
    <h3 class="text-2xl font-normal tracking-wide text-stone-950">The Royal Court Penthouse</h3>
    <p class="text-xs text-stone-600 font-sans mt-1 leading-relaxed">720 sq.m duplex with uncompromised 360-degree panoramic views.</p>
  </div>
  <button type="button" class="w-full border border-stone-900 bg-stone-900 text-stone-50 py-3 text-xs font-sans uppercase tracking-wider hover:bg-stone-800 transition-colors">Request Private Viewing</button>
</div>"""
        },

        # 4. Soft Humanist (Health & Clinical)
        "clinic": {
            "prompt_en": "Luxury Dermatology & Aesthetic Skin Clinic with online doctor appointment and consultation",
            "prompt_fa": "کلینیک تخصصی پوست و زیبایی لوکس با رزرو آنلاین نوبت و مشاوره پزشکان فوق تخصص",
            "domain": "health_wellness_clinical",
            "confidence": "98%",
            "style_en": "Soft Humanist (Healing Clinical)",
            "style_fa": "انسان محور نرم و درمانی (Soft Humanist)",
            "material_en": "Porcelain Soft + Calming Mint",
            "material_fa": "پرسلن نرم + نعنایی آرامش بخش",
            "decision_en": "Medical care context requires soothing rounded cards, high empathy whitespace, and zero jarring alerts.",
            "decision_fa": "محیط درمانی نیازمند کارت های با انحنای نرم، فضای آرامش بخش و پرهیز از هشدارهای استرس زا است.",
            "avoid_en": "Sharp 90-degree corners, pure black backgrounds, aggressive neon shadows.",
            "avoid_fa": "گوشه های تیز ۹۰ درجه، پس زمینه های مشکی تیره، سایه های نئونی تند.",
            "contrast": "16.1 : 1 (AAA)",
            "quality": "97 / 100",
            "touch": "48px (Compliant)",
            "bidi": "RTL Persian Vazirmatn",
            "title_en": "Ariana Dermatology & Laser Clinic",
            "title_fa": "کلینیک پوست و لیزر آریانا",
            "subtitle_en": "Board-Certified Aesthetic Specialists",
            "subtitle_fa": "فوق تخصص درماتولوژی و جوان سازی پوست",
            "badge_en": "BOOKING OPEN",
            "badge_fa": "نوبت دهی آنلاین",
            "value": "Specialist Consultation",
            "subval_en": "Advanced 2026 Laser Technology Suite",
            "subval_fa": "تجهیزات لیزر پیشرفته ۲۰۲۶ با کادر مجرب",
            "action_en": "Book Online Appointment",
            "action_fa": "رزرو آنلاین نوبت پزشک",
            "secondary_en": "View Clinical Services",
            "secondary_fa": "مشاهده لیست خدمات",
            "codeTailwind": """<div class="rounded-2xl border border-teal-100 bg-teal-50/40 p-6 text-slate-800 font-sans shadow-sm">
  <div class="flex items-center justify-between border-b border-teal-100 pb-3">
    <span class="text-xs font-medium text-teal-700">کلینیک تخصصی درماتولوژی</span>
    <span class="rounded-full bg-teal-100 px-2.5 py-0.5 text-xs text-teal-800">نوبت دهی آنلاین</span>
  </div>
  <div class="my-4">
    <h3 class="text-xl font-bold text-slate-900">مشاوره فوق تخصصی جوان سازی</h3>
    <p class="text-xs text-slate-600 mt-1">با پیشرفته ترین تجهیزات لیزر ۲۰۲۶ و کادر مجرب پزشکی</p>
  </div>
  <button type="button" class="w-full rounded-xl bg-teal-600 hover:bg-teal-700 text-white font-medium py-3 text-xs shadow-sm transition-colors">رزرو آنلاین و انتخاب پزشک</button>
</div>"""
        },

        # 5. Clean Stripe SaaS (Billing & SaaS)
        "stripe": {
            "prompt_en": "B2B Enterprise SaaS Subscription Billing & Usage-based Metric Metering",
            "prompt_fa": "سامانه مدیریت اشتراک های سالانه و صدور فاکتور سازمانی B2B",
            "domain": "ecommerce_saas_billing",
            "confidence": "95%",
            "style_en": "Clean Stripe SaaS (Corporate Polished)",
            "style_fa": "استرایپ مدرن و شرکتی (Clean Stripe)",
            "material_en": "Crisp Light Tint + Bento Grid",
            "material_fa": "پس زمینه روشن شفاف + ساختار بنتو",
            "decision_en": "Corporate buyer persona demands high conversion clarity, subtle micro-shadows, and trustworthy blue accents.",
            "decision_fa": "خریدار سازمانی نیازمند وضوح بالا، سایه های بسیار ظریف و رنگ های آبی قابل اعتماد است.",
            "avoid_en": "Harsh pure-black borders, saturated neon backgrounds, playful script typography.",
            "avoid_fa": "بوردرهای خشک مشکی، پس زمینه های جیغ نئونی، تایپوگرافی های شکسته فانتزی.",
            "contrast": "18.2 : 1 (AAA)",
            "quality": "98 / 100",
            "touch": "44px (Compliant)",
            "bidi": "Bilingual Resilient",
            "title_en": "Enterprise Subscription Plan",
            "title_fa": "پلن اشتراک سازمانی انترپرایز",
            "subtitle_en": "Billed Annually • Unlimited AI Seats",
            "subtitle_fa": "پرداخت سالانه • دسترسی نامحدود برای تیم",
            "badge_en": "ACTIVE TIER",
            "badge_fa": "پلن فعال",
            "value": "$299 / seat / mo",
            "subval_en": "Includes SOC2 Type II, 99.99% SLA & Dedicated AM",
            "subval_fa": "شامل گواهی SOC2، پایداری ۹۹.۹۹٪ و مدیر اختصاصی",
            "action_en": "Manage Subscription",
            "action_fa": "مدیریت و ارتقای اشتراک",
            "secondary_en": "Download Invoice",
            "secondary_fa": "دانلود فاکتور رسمی",
            "codeTailwind": """<div class="rounded-lg border border-slate-200 bg-white p-5 text-slate-900 font-sans shadow-sm">
  <div class="flex items-center justify-between border-b border-slate-100 pb-3">
    <span class="font-semibold text-sm text-slate-700">Enterprise Subscription</span>
    <span class="rounded bg-indigo-50 px-2 py-0.5 text-xs font-medium text-indigo-600 border border-indigo-100">ANNUAL</span>
  </div>
  <div class="my-4">
    <div class="text-2xl font-bold text-slate-900">$299<span class="text-xs font-normal text-slate-500"> / seat / mo</span></div>
    <p class="text-xs text-slate-600 mt-1">Includes 99.99% Uptime SLA and SOC2 Type II compliance.</p>
  </div>
  <button type="button" class="w-full rounded-md bg-indigo-600 hover:bg-indigo-700 text-white font-medium py-2.5 text-xs transition-colors">Manage Subscription</button>
</div>"""
        },

        # 6. Minimal Swiss / International
        "minimal_swiss": {
            "prompt_en": "Swiss International Typographic poster and editorial index with strict modular hierarchy",
            "prompt_fa": "پوستر و ایندکس ادیتوریال تایپوگرافی سوئیسی با سلسله مراتب دقیق مدولار",
            "domain": "media_editorial",
            "confidence": "98%",
            "style_en": "Minimal Swiss / International",
            "style_fa": "سوئیسی مینیمال و دقیق (Swiss International)",
            "material_en": "Matte Paper + Strict Modular Grid",
            "material_fa": "کاغذ مات + گرید مدولار ۱۲ ستونه",
            "decision_en": "Rational Swiss design enforces 0px radius, pure black-and-white contrast, and strict sans-serif hierarchy.",
            "decision_fa": "دیزاین عقلانی سوئیسی گوشه های کاملاً صفر، کنتراست مطلق سیاه و سفید و تایپوگرافی دقیق سنز-سریف را تحمیل می کند.",
            "avoid_en": "Generic purple gradients, soft blurry shadows, decorative emojis, rounded pills.",
            "avoid_fa": "گرادیان های بنفش کلیشه ای، سایه های محو، اموجی های تزئینی، گوشه های گرد پلاستیکی.",
            "contrast": "21.0 : 1 (AAA)",
            "quality": "99 / 100",
            "touch": "44px (Compliant)",
            "bidi": "Strict Left/Right Alignment",
            "title_en": "Die Neue Grafik • Issue 42",
            "title_fa": "گرافیک نوین • شماره ۴۲",
            "subtitle_en": "Zurich Typographic Archive • 1958-2026",
            "subtitle_fa": "آرشیو تایپوگرافی زوریخ • ۱۹۵۸-۲۰۲۶",
            "badge_en": "MODULAR GRID",
            "badge_fa": "گرید مدولار",
            "value": "Typographic Order",
            "subval_en": "Grid Density: 12 Cols • Baseline: 8pt",
            "subval_fa": "تراکم گرید: ۱۲ ستون • خط کرسی: ۸ پوینت",
            "action_en": "Read Archival Essay",
            "action_fa": "مطالعه مقاله آرشیوی",
            "secondary_en": "View Grid Specs",
            "secondary_fa": "مشخصات فنی گرید",
            "codeTailwind": """<div class="rounded-none border-2 border-zinc-950 bg-white p-6 text-zinc-950 font-sans">
  <div class="flex items-center justify-between border-b-2 border-zinc-950 pb-3">
    <span class="text-xs font-bold tracking-widest uppercase">ZURICH ARCHIVE</span>
    <span class="text-xs font-mono">№ 42/26</span>
  </div>
  <div class="my-6">
    <h2 class="text-3xl font-black tracking-tight uppercase leading-none">DIE NEUE GRAFIK</h2>
    <p class="text-xs font-medium text-zinc-600 mt-2 leading-relaxed max-w-sm">Rational construction, standardized asymmetric balance, and objective communication.</p>
  </div>
  <button type="button" class="w-full border-2 border-zinc-950 bg-zinc-950 hover:bg-white text-white hover:text-zinc-950 py-3 text-xs font-bold uppercase tracking-wider transition-colors">Access Public Archive</button>
</div>"""
        },

        # 7. Neo-Brutalism (Raw High-Contrast)
        "neobrutalism": {
            "prompt_en": "High-energy Neobrutalist creative design merchandise shop with hard 4px drop shadows",
            "prompt_fa": "فروشگاه محصولات خلاقانه با سبک نئوبروتالیسم پرانرژی و سایه های خشک ۴ پیکسلی",
            "domain": "ecommerce_fashion",
            "confidence": "96%",
            "style_en": "Neo-Brutalism (Raw High-Contrast)",
            "style_fa": "نئوبروتالیسم پرانرژی (Neo-Brutalism)",
            "material_en": "Flat Pigment + Hard Offset Shadows",
            "material_fa": "پیگمنت تخت رنگی + سایه های سخت بدون بلر",
            "decision_en": "Rebellious counter-culture aesthetic mandates 3px black borders, vibrant pop hues, and 0px radius buttons.",
            "decision_fa": "استایل ساختارشکن نئوبروتال بوردرهای ضخیم ۳ پیکسلی، رنگ های جیغ زرد/آبی و سایه های سخت زاویه دار را می طلبد.",
            "avoid_en": "Soft diffused blur, pastel translucency, low contrast, delicate rounded pills.",
            "avoid_fa": "بلرهای نرم، پس زمینه های شفاف کم رنگ، کنتراست پایین، المان های گرد ظریف.",
            "contrast": "16.4 : 1 (AAA)",
            "quality": "97 / 100",
            "touch": "48px (Compliant)",
            "bidi": "Bold LTR/RTL Blocks",
            "title_en": "Cyber Acid Hoodie v3",
            "title_fa": "هودی سایبر اسید نسخه ۳",
            "subtitle_en": "Limited Drop • 100% Organic Cotton Heavyweight",
            "subtitle_fa": "دراپ محدود • پنبه سنگین وزن ۱۰۰٪ ارگانیک",
            "badge_en": "ONLY 14 LEFT",
            "badge_fa": "فقط ۱۴ عدد مانده",
            "value": "$140.00 USD",
            "subval_en": "Free Global Shipping + Holographic Sticker Pack",
            "subval_fa": "ارسال رایگان + پک استیکر هولوگرافیک اختصاصی",
            "action_en": "Grab Limited Drop",
            "action_fa": "خرید قطعی سفارش",
            "secondary_en": "Size Guide",
            "secondary_fa": "راهنمای سایز",
            "codeTailwind": """<div class="border-4 border-black bg-yellow-300 p-6 text-black font-sans shadow-[6px_6px_0px_0px_rgba(0,0,0,1)]">
  <div class="flex items-center justify-between border-b-2 border-black pb-3">
    <span class="text-xs font-black uppercase tracking-wider bg-black text-white px-2 py-0.5">LIMITED DROP</span>
    <span class="text-xs font-black">⚡ 14 PIECES LEFT</span>
  </div>
  <div class="my-5">
    <h3 class="text-2xl font-black uppercase tracking-tight">CYBER ACID HOODIE</h3>
    <p class="text-xs font-bold text-neutral-800 mt-1">Heavyweight 480gsm organic fleece with reinforced double-stitched cuffs.</p>
    <div class="text-3xl font-black mt-3">$140.00</div>
  </div>
  <button type="button" class="w-full border-2 border-black bg-white hover:bg-black text-black hover:text-white font-black py-3 text-xs uppercase tracking-wider shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] transition-all">Claim Your Piece</button>
</div>"""
        },

        # 8. Organic Nordic
        "organic_nordic": {
            "prompt_en": "Minimalist Nordic acoustic speaker studio with unbleached cotton warmth and natural rhythm",
            "prompt_fa": "اسپیکر آکوستیک نوردیک با پارچه کتان ارگانیک، بافت چوب طبیعی و طراحی اسکاندیناوی",
            "domain": "lifestyle_home",
            "confidence": "94%",
            "style_en": "Organic Nordic (Scandinavian)",
            "style_fa": "ارگانیک نوردیک و آرام (Organic Nordic)",
            "material_en": "Unbleached Cotton + Earth Tint",
            "material_fa": "کتان خام + تم رنگی خاکی و طبیعی",
            "decision_en": "Scandinavian design philosophy prioritizes natural earth hues, airy breathing space, and subtle organic radii.",
            "decision_fa": "فلسفه اسکاندیناوی رنگ های خاکی آرامش بخش، فاصله تنفس زیاد و انحناهای نرم را در اولویت قرار می دهد.",
            "avoid_en": "Synthetic neon, cold sterile white, aggressive commercial countdowns.",
            "avoid_fa": "نئون های مصنوعی، سفیدی بی روح بیمارستانی، تایمرهای استرس زای فروشگاهی.",
            "contrast": "15.2 : 1 (AAA)",
            "quality": "96 / 100",
            "touch": "44px (Compliant)",
            "bidi": "Natural Flow",
            "title_en": "Klang Acoustic Soundbar",
            "title_fa": "ساندبار آکوستیک کلانگ",
            "subtitle_en": "Nordic Wool • Solid Smoked Oak Framing",
            "subtitle_fa": "پشم دست باف سوئدی • قاب بلوط دودی طبیعی",
            "badge_en": "SUSTAINABLE",
            "badge_fa": "پایدار و دوستدار طبیعت",
            "value": "$890 • Handcrafted",
            "subval_en": "10-Year Repairability Guarantee",
            "subval_fa": "۱۰ سال ضمانت قابلیت تعمیر و قطعات اصلی",
            "action_en": "Explore Craftsmanship",
            "action_fa": "بررسی جزئیات ساخت",
            "secondary_en": "Listen Sample",
            "secondary_fa": "شنیدن نمونه صدا",
            "codeTailwind": """<div class="rounded-xl border border-stone-200/80 bg-[#fbf9f5] p-6 text-stone-800 font-sans shadow-sm">
  <div class="flex items-center justify-between border-b border-stone-200/60 pb-3">
    <span class="text-xs tracking-wider uppercase text-stone-500 font-serif">København Studio</span>
    <span class="text-xs text-stone-600 bg-stone-100 px-2 py-0.5 rounded">Pure Oak</span>
  </div>
  <div class="my-4">
    <h3 class="text-xl font-serif text-stone-900">Klang Natural Soundbar</h3>
    <p class="text-xs text-stone-600 mt-1 leading-relaxed">Crafted from circular Danish wool and acoustic chamber wood.</p>
  </div>
  <button type="button" class="w-full rounded-lg bg-stone-800 hover:bg-stone-700 text-stone-50 py-3 text-xs font-medium transition-colors">Configure System</button>
</div>"""
        },

        # 9. Bauhaus Geometric
        "bauhaus_geometric": {
            "prompt_en": "Constructivist Bauhaus architecture exhibition catalogue with primary color blocks",
            "prompt_fa": "کاتالوگ نمایشگاه معماری باهاوس و آوانگارد با بلوک های رنگی اصلی و زوایای مهندسی",
            "domain": "culture_arts",
            "confidence": "95%",
            "style_en": "Bauhaus Geometric (Constructivist)",
            "style_fa": "باهاوس هندسی و آوانگارد (Bauhaus)",
            "material_en": "Flat Industrial Canvas + Primary Blocks",
            "material_fa": "بوم صنعتی تخت + بلوک های رنگی اصلی",
            "decision_en": "Art-and-technology synthesis mandates geometric alignment, zero curved pills, and uncompromising structural clarity.",
            "decision_fa": "پیوند هنر و تکنولوژی نیازمند خطوط منظم، زوایای قائم بدون انحنا و وضوح ساختاری کامل است.",
            "avoid_en": "Rounded corners, organic curved shapes, blurred gradients, pastel washes.",
            "avoid_fa": "گوشه های گرد، فرم های منحنی ارگانیک، گرادیان های مات، رنگ های پاستلی شلخته.",
            "contrast": "17.0 : 1 (AAA)",
            "quality": "97 / 100",
            "touch": "48px (Compliant)",
            "bidi": "Constructivist Geometric",
            "title_en": "Staatliches Bauhaus Weimar",
            "title_fa": "مکتب باهاوس وایمار",
            "subtitle_en": "Centennial Retrospective • Form Follows Function",
            "subtitle_fa": "نمایشگاه ۱۰۰ سالگی • فرم پیرو عملکرد",
            "badge_en": "WEIMAR 1919",
            "badge_fa": "وایمار ۱۹۱۹",
            "value": "Form Follows Function",
            "subval_en": "Curated by Gropius & Moholy-Nagy Foundation",
            "subval_fa": "با همکاری بنیاد والتر گروپیوس و موهولی-ناگی",
            "action_en": "View Exhibition Guide",
            "action_fa": "راهنمای آثار نمایشگاه",
            "secondary_en": "Floor Plan",
            "secondary_fa": "پلان گالری ها",
            "codeTailwind": """<div class="rounded-none border-2 border-zinc-950 bg-[#f7f5f0] p-6 text-zinc-950 font-sans relative">
  <div class="absolute top-0 right-0 w-12 h-12 bg-red-600"></div>
  <div class="flex items-center justify-between border-b-2 border-zinc-950 pb-3 pr-12">
    <span class="text-xs font-bold tracking-widest">DESSAU ARCHIVE</span>
    <span class="text-xs font-mono">1919-2026</span>
  </div>
  <div class="my-5">
    <h3 class="text-2xl font-black uppercase tracking-tight">Form Follows Function</h3>
    <p class="text-xs font-bold text-zinc-700 mt-1">Radical pedagogical architecture for modern mechanical civilization.</p>
  </div>
  <div class="flex gap-2">
    <button type="button" class="flex-1 rounded-none bg-blue-700 hover:bg-blue-800 text-white font-bold py-2.5 text-xs uppercase tracking-wider transition-colors">Exhibition Tour</button>
    <div class="w-10 bg-yellow-400 border-2 border-zinc-950"></div>
  </div>
</div>"""
        },

        # 10. Specular Glassmorphism 2.0
        "modern_glass_2": {
            "prompt_en": "Luminous Ambient Glassmorphism 2.0 AI assistant widget with specular Fresnel rim reflection",
            "prompt_fa": "ویجت هوش مصنوعی گلس مورفیسم ۲.۰ با بازتاب دو لایه لبه های فرنل و بلر کالیبره شده",
            "domain": "ai_agents_ambient",
            "confidence": "97%",
            "style_en": "Specular Glassmorphism 2.0",
            "style_fa": "شیشه ای مدرن و کالیبره (Glass 2.0)",
            "material_en": "Optic Glass + Chromatic Rim Glow",
            "material_fa": "شیشه اپتیکال شفاف + بازتاب نوری لبه ها",
            "decision_en": "Next-gen glassmorphism mandates maximum 2 blur surfaces, specular inset highlights, and pure AAA text contrast.",
            "decision_fa": "نسل جدید گلس مورفیسم حداکثر ۲ لایه بلر، هایلایت های ظریف اینست و کنتراست قطعی متن را تضمین می کند.",
            "avoid_en": "Excessive backdrop blurs (>2), low contrast text on glass, opaque flat fills.",
            "avoid_fa": "بلرهای متعدد تخریب کننده GPU، متن تاریک روی شیشه، لایه های مات بی روح.",
            "contrast": "16.8 : 1 (AAA)",
            "quality": "98 / 100",
            "touch": "44px (Compliant)",
            "bidi": "Luminous Centered",
            "title_en": "Antigravity Autonomous Core",
            "title_fa": "هسته پردازش خودکار Antigravity",
            "subtitle_en": "Multi-Agent Neural Thread Active • 120 FPS",
            "subtitle_fa": "ترد فعال عامل های چندگانه • ۱۲۰ فریم در ثانیه",
            "badge_en": "SYNAPSE READY",
            "badge_fa": "آماده استنتاج",
            "value": "1.24 TeraFLOPS",
            "subval_en": "Zero-Latency Local Context Synthesis",
            "subval_fa": "سنتز بلادرنگ کانتکست با تاخیر صفر",
            "action_en": "Authorize Agent Dispatch",
            "action_fa": "صدور مجوز اجرای ایجنت",
            "secondary_en": "Telemetry Trace",
            "secondary_fa": "ردپای تله متری",
            "codeTailwind": """<div class="rounded-2xl border border-white/20 bg-slate-900/60 backdrop-blur-md p-6 text-white font-sans shadow-[inset_0_1px_1px_rgba(255,255,255,0.4)]">
  <div class="flex items-center justify-between border-b border-white/10 pb-3">
    <div class="flex items-center gap-2">
      <span class="h-2 w-2 rounded-full bg-cyan-400 animate-ping"></span>
      <span class="text-xs font-medium text-cyan-200">Autonomous Neural Core</span>
    </div>
    <span class="text-[10px] uppercase font-mono tracking-wider bg-white/10 px-2 py-0.5 rounded-full">Active</span>
  </div>
  <div class="my-4">
    <div class="text-2xl font-bold tracking-tight text-white">1.24 TFLOPS</div>
    <p class="text-xs text-slate-300 mt-1">Multi-agent thread synthesis with 0ms server roundtrip.</p>
  </div>
  <button type="button" class="w-full rounded-xl bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-white font-semibold py-2.5 text-xs shadow-lg transition-all">Authorize Dispatch</button>
</div>"""
        },

        # 11. Retro Futurism / Cyber
        "retro_futurism": {
            "prompt_en": "Synthwave Retro-Futurism game tournament console with scanline edge and violet neon glow",
            "prompt_fa": "کنسول مسابقات بازی رترو-فیوچریسم با خطوط اسکن لاین و درخشش نئونی بنفش سایبرپانک",
            "domain": "gaming_entertainment",
            "confidence": "96%",
            "style_en": "Retro Futurism / Cyber",
            "style_fa": "سایبرپانک و رترو-فیوچریسم (Retro Cyber)",
            "material_en": "Deep Violet Space + Neon Halo",
            "material_fa": "فضای بنفش تیره + هاله نور نئونی",
            "decision_en": "Arcade gaming immersion requires scanline borders, high-impact neon contrasts, and monospace battle metrics.",
            "decision_fa": "بازی های سایبرپانک نیازمند لبه های اسکن لاین، کنتراست شدید نئونی و متریک های مونو اسپیس هستند.",
            "avoid_en": "Earth tone palettes, quiet serif typography, rustic wooden textures.",
            "avoid_fa": "پالت های خاکی آرامش بخش، فونت های سریف سنتی، بافت های چوبی روستایی.",
            "contrast": "16.2 : 1 (AAA)",
            "quality": "97 / 100",
            "touch": "48px (Compliant)",
            "bidi": "Arcade Matrix",
            "title_en": "Outrun 2088 Championship",
            "title_fa": "مسابقات جهانی اوت ران ۲۰۸۸",
            "subtitle_en": "Neon District Final • 64 Teams Competing",
            "subtitle_fa": "فینال نئون دیستریکت • رقابت ۶۴ تیم برتر",
            "badge_en": "LOBBY OPEN",
            "badge_fa": "لابی فعال",
            "value": "Pool: $250,000",
            "subval_en": "Live Holographic Broadcast • 4K 144Hz",
            "subval_fa": "پخش زنده هولوگرافیک با کیفیت 4K و ۱۴۴ هرتز",
            "action_en": "Enter Battle Arena",
            "action_fa": "ورود به آرنای مسابقه",
            "secondary_en": "Spectator Feed",
            "secondary_fa": "تماشای زنده بازی",
            "codeTailwind": """<div class="rounded-md border border-violet-500/50 bg-[#090514] p-5 text-violet-200 font-mono shadow-[0_0_20px_rgba(139,92,246,0.3)]">
  <div class="flex items-center justify-between border-b border-violet-900/60 pb-2 text-xs">
    <span class="text-fuchsia-400 font-bold">ARCADE SYSTEM // ONLINE</span>
    <span class="text-cyan-400 animate-pulse">60 FPS LOCKED</span>
  </div>
  <div class="my-4">
    <h3 class="text-xl font-bold tracking-wider text-white">NEON TOURNAMENT</h3>
    <p class="text-xs text-violet-400 mt-1">Prize Pool: $250,000 USD • Server Latency: 12ms</p>
  </div>
  <button type="button" class="w-full rounded bg-fuchsia-600 hover:bg-fuchsia-500 text-white font-bold py-2.5 text-xs uppercase tracking-widest shadow-[0_0_12px_rgba(217,70,239,0.5)] transition-all">Join Match Queue</button>
</div>"""
        },

        # 12. Swiss Editorial Magazine
        "editorial_magazine": {
            "prompt_en": "Swiss cultural review and long-form intellectual magazine essay with hairline dividers",
            "prompt_fa": "نشریه و مجله نقد فرهنگی مدرن با مقالات بلند، فونت سریف و خطوط جداکننده بسیار ظریف",
            "domain": "journalism_publishing",
            "confidence": "95%",
            "style_en": "Swiss Editorial Magazine",
            "style_fa": "نشریه و ادیتوریال مدرن (Swiss Editorial)",
            "material_en": "Newsprint Fine + Hairline Dividers",
            "material_fa": "کاغذ مرغوب نشریه + خطوط مویی جداکننده",
            "decision_en": "Long-form journalism mandates optimal reading line-length (65ch), classic serif body, and zero distracting popups.",
            "decision_fa": "روزنامه نگاری حرفه ای نیازمند طول سطر استاندارد (۶۵ کاراکتر)، فونت سریف خوانا و حذف هرگونه پاپ آپ است.",
            "avoid_en": "Floating glass cards, rounded pill buttons, saturated CTA bars, loud gradient text.",
            "avoid_fa": "کارت های شیشه ای شناور، دکمه های کپسولی گرد، گرادیان های جیغ، بنرهای چشمک زن.",
            "contrast": "18.5 : 1 (AAA)",
            "quality": "99 / 100",
            "touch": "44px (Compliant)",
            "bidi": "Literary Flow (Right/Left Aligned)",
            "title_en": "The Disappearance of Solitude",
            "title_fa": "زوال تنهایی در عصر هوش مصنوعی",
            "subtitle_en": "An Inquiry into Autonomous Agents & Human Cognition",
            "subtitle_fa": "جستاری پیرامون عاملیت های خودکار و ذهن انسان",
            "badge_en": "ESSAY • 18 MIN READ",
            "badge_fa": "مقاله بلند • ۱۸ دقیقه مطالعه",
            "value": "Critical Discourse",
            "subval_en": "Issue 88 • Spring Cultural Review",
            "subval_fa": "شماره ۸۸ • فصلنامه نقد فرهنگی بهار",
            "action_en": "Read Full Essay",
            "action_fa": "مطالعه متن کامل جستار",
            "secondary_en": "Download PDF",
            "secondary_fa": "دریافت نسخه چاپی PDF",
            "codeTailwind": """<div class="rounded-none border border-zinc-300 bg-[#faf8f5] p-6 text-zinc-900 font-serif shadow-none">
  <div class="flex items-center justify-between border-b border-zinc-300 pb-2 text-xs font-sans">
    <span class="uppercase tracking-widest text-zinc-500 font-medium">LITERARY QUARTERLY</span>
    <span class="text-zinc-600">ISSUE № 88</span>
  </div>
  <div class="my-5">
    <h3 class="text-2xl font-normal text-zinc-950 leading-tight">The Disappearance of Solitude</h3>
    <p class="text-xs text-zinc-600 font-sans mt-2 leading-relaxed max-w-md">An inquiry into the psychological consequences of constant synthetic companion intelligence.</p>
  </div>
  <button type="button" class="w-full border-b-2 border-zinc-950 bg-transparent text-zinc-950 font-sans font-bold py-2 text-xs uppercase tracking-wider hover:bg-zinc-100 transition-colors text-left">Continue Reading &rarr;</button>
</div>"""
        },

        # 13. Industrial Utility (Heavy Duty)
        "industrial_utility": {
            "prompt_en": "Heavy industrial power plant breaker control panel with yellow hazard stripes and fail-safe locks",
            "prompt_fa": "پنل کنترل نیروگاه صنعتی و تاسیسات برق با خطوط ایمنی زرد، بدنه فولادی و قفل های ایمن",
            "domain": "energy_industrial",
            "confidence": "96%",
            "style_en": "Industrial Utility (Heavy Industrial)",
            "style_fa": "صنعتی و ابزار مهندسی (Industrial Utility)",
            "material_en": "Galvanized Steel + Hazard Accents",
            "material_fa": "فولاد گالوانیزه تیره + خطوط ایمنی زرد",
            "decision_en": "Power utility operations require 0px radius, high-visibility amber alerts, and physical interlock confirmation.",
            "decision_fa": "عملیات نیروگاهی نیازمند گوشه های بدون انحنا، رنگ های هشدار فسفری/کهربایی و دکمه های بزرگ ایمن است.",
            "avoid_en": "Delicate rounded glass, pastel washes, tiny click targets, frivolous animations.",
            "avoid_fa": "شیشه های ظریف، رنگ های پاستلی دخترانه، تارگت های کلیک کوچک، انیمیشن های کند و نمایشی.",
            "contrast": "18.9 : 1 (AAA)",
            "quality": "98 / 100",
            "touch": "48px (Compliant)",
            "bidi": "Engineering HUD",
            "title_en": "Turbine Gen-4 Main Breaker",
            "title_fa": "کلید قدرت اصلی توربین ژنراتور شماره ۴",
            "subtitle_en": "Unit 42 • Substation South • 33kV Line",
            "subtitle_fa": "واحد ۴۲ • پست فشار قوی جنوب • خط ۳۳ کیلوولت",
            "badge_en": "HIGH VOLTAGE",
            "badge_fa": "ولتاژ خطرناک",
            "value": "Load: 84.2 MW",
            "subval_en": "Temperature: 68.4°C • SF6 Pressure: 0.62 MPa",
            "subval_fa": "دمای هسته: ۶۸.۴ درجه • فشار گاز: ۰.۶۲ مگاپاسکال",
            "action_en": "Arm Emergency Trip",
            "action_fa": "فعال سازی قطع اضطراری",
            "secondary_en": "Isolate Substation",
            "secondary_fa": "ایزولاسیون خط تغذیه",
            "codeTailwind": """<div class="rounded-none border-2 border-amber-500 bg-zinc-900 p-5 text-amber-400 font-mono">
  <div class="flex items-center justify-between border-b border-zinc-800 pb-2 text-xs font-bold">
    <span>TURBINE SUB-04 // 33KV</span>
    <span class="bg-amber-500 text-black px-2 py-0.5 font-black">ENERGIZED</span>
  </div>
  <div class="my-4">
    <div class="text-3xl font-black tracking-wider text-amber-300">84.2 MW</div>
    <p class="text-xs text-zinc-400 mt-1">Bus Frequency: 50.02 Hz • SF6 Pressure: 0.62 MPa</p>
  </div>
  <button type="button" class="w-full border-2 border-red-600 bg-red-950/60 hover:bg-red-600 text-red-100 font-bold py-2.5 text-xs uppercase tracking-widest transition-colors">ARM INTERLOCK TRIP</button>
</div>"""
        },

        # 14. Biophilic Wellness
        "biophilic_wellness": {
            "prompt_en": "Biophilic restorative sanctuary with living botanical moss textures and circadian breathing guide",
            "prompt_fa": "سامانه آرامش بخش زیست محور با بافت خزه طبیعی، گیاهان زنده و راهنمای تنفس ریتمیک",
            "domain": "wellness_meditation",
            "confidence": "97%",
            "style_en": "Biophilic Wellness (Organic Natural)",
            "style_fa": "زیست محور، طبیعت و آرامش (Biophilic)",
            "material_en": "Earthen Moss Light + Pebble Grain",
            "material_fa": "خزه خاکی روشن + بافت سنگریزه ای ملایم",
            "decision_en": "Therapeutic relaxation mandates organic curved envelopes, soft botanical greens, and slow breathing motion.",
            "decision_fa": "آرامش درمانی نیازمند انحناهای ارگانیک، رنگ های سبز گیاهی آرام و ریتم های تنفسی کند است.",
            "avoid_en": "Harsh right angles, fluorescent synthetic colors, high-stress numeric counters.",
            "avoid_fa": "زوایای تیز و خشک، رنگ های فلورسنت صنعتی، تایمرهای استرس زای دیجیتال.",
            "contrast": "16.0 : 1 (AAA)",
            "quality": "97 / 100",
            "touch": "48px (Compliant)",
            "bidi": "Calm Balanced",
            "title_en": "Circadian Breathwork Sanctuary",
            "title_fa": "آسایشگاه تمرینات تنفس بیوفیلیک",
            "subtitle_en": "Natural Forest Resonance • 4-7-8 Cadence",
            "subtitle_fa": "فرکانس طبیعی جنگل • ریتم تنفس ۴-۷-۸",
            "badge_en": "DEEP REST",
            "badge_fa": "آرامش عمیق",
            "value": "Coherence: 94%",
            "subval_en": "Heart Rate Variability: Optimal • 14 Min",
            "subval_fa": "تغییرپذیری ضربان قلب: بهینه • ۱۴ دقیقه باقیمانده",
            "action_en": "Begin Guided Breath",
            "action_fa": "شروع چرخه تنفس آرام",
            "secondary_en": "Select Soundscape",
            "secondary_fa": "انتخاب صدای طبیعت",
            "codeTailwind": """<div class="rounded-3xl border border-emerald-900/10 bg-[#f4f7f4] p-6 text-emerald-950 font-sans shadow-sm">
  <div class="flex items-center justify-between border-b border-emerald-900/10 pb-3">
    <span class="text-xs font-medium text-emerald-800 font-serif">Living Forest Cycle</span>
    <span class="rounded-full bg-emerald-100 px-2.5 py-0.5 text-xs text-emerald-800">Circadian Calm</span>
  </div>
  <div class="my-5 text-center">
    <div class="w-16 h-16 mx-auto rounded-full bg-emerald-200/60 flex items-center justify-center animate-pulse">
      <div class="w-8 h-8 rounded-full bg-emerald-600/40"></div>
    </div>
    <h3 class="text-xl font-serif text-emerald-900 mt-3">4-7-8 Restorative Breath</h3>
    <p class="text-xs text-emerald-700 mt-1">Slow parasympathetic nervous recovery through natural acoustic resonance.</p>
  </div>
  <button type="button" class="w-full rounded-2xl bg-emerald-800 hover:bg-emerald-700 text-white font-medium py-3 text-xs transition-colors">Start Inhale (4s)</button>
</div>"""
        },

        # 15. Futuristic Aerotech HUD
        "futuristic_tech": {
            "prompt_en": "Autonomous spacecraft orbital docking HUD with vector crosshair telemetry and trajectory matrix",
            "prompt_fa": "سیستم هاد الحاق خودکار فضاپیما در مدار زمین با تله متری وکتور و ماتریس مسیر پرواز",
            "domain": "aerospace_defense",
            "confidence": "98%",
            "style_en": "Futuristic Aerotech HUD",
            "style_fa": "فناوری آینده و هوانوردی (Aerotech HUD)",
            "material_en": "Carbon Slate + Crosshair Telemetry",
            "material_fa": "کربن مات تیره + تله متری خطوط وکتوری",
            "decision_en": "Orbital flight operations mandate high-precision vector crosshairs, cyan monochromatic lines, and sub-millimeter coordinates.",
            "decision_fa": "عملیات مانور مداری نیازمند خطوط وکتوری فیروزه ای بسیار دقیق، فاقد بلر و با ارقام مونو اسپیس است.",
            "avoid_en": "Serif typography, bright warm pastels, soft ambient shadows, playful emojis.",
            "avoid_fa": "فونت های سریف ادبی، رنگ های پاستلی گرم، سایه های ابری، اموجی های فانتزی.",
            "contrast": "17.6 : 1 (AAA)",
            "quality": "99 / 100",
            "touch": "44px (Compliant)",
            "bidi": "Fixed Aerotech Coordinates",
            "title_en": "Orbital Vector Docking Port",
            "title_fa": "سامانه اتصال مداری ایستگاه فضایی",
            "subtitle_en": "Approach Angle: 0.04° • Relative V: 0.12 m/s",
            "subtitle_fa": "زاویه تقرب: ۰.۰۴ درجه • سرعت نسبی: ۰.۱۲ متر بر ثانیه",
            "badge_en": "ALIGNMENT 99.8%",
            "badge_fa": "هم راستایی ۹۹.۸٪",
            "value": "Range: 42.6 m",
            "subval_en": "Thruster Pulse: Auto-Stabilized • Lock in T-34s",
            "subval_fa": "پالس تراستر: پایدار • قفل مکانیکی در ۳۴ ثانیه",
            "action_en": "Engage Final Clamp",
            "action_fa": "درگیر کردن قفل هیدرولیک نهایی",
            "secondary_en": "Abort to Safe Orbit",
            "secondary_fa": "انصراف و بازگشت به مدار امن",
            "codeTailwind": """<div class="rounded border border-cyan-500/40 bg-[#080d14] p-5 text-cyan-300 font-mono shadow-[0_0_15px_rgba(6,182,212,0.15)]">
  <div class="flex items-center justify-between border-b border-cyan-950 pb-2 text-xs">
    <span>APPROACH RADAR // DOCK-02</span>
    <span class="text-cyan-400 font-bold">DELTA-V: 0.12 M/S</span>
  </div>
  <div class="my-4">
    <div class="text-3xl font-bold tracking-widest text-cyan-200">42.6 METERS</div>
    <p class="text-xs text-cyan-500 mt-1">Relative Bearing: 004.2° • Gyro Rate: Nominal</p>
  </div>
  <button type="button" class="w-full border border-cyan-400 bg-cyan-950/60 hover:bg-cyan-500 hover:text-black text-cyan-100 font-bold py-2 text-xs uppercase tracking-widest transition-all">Lock Magnetic Clamps</button>
</div>"""
        },

        # 16. Retro Computing / CRT Phosphor
        "retro_computing_80s": {
            "prompt_en": "1982 Amber Phosphor CRT VT220 mainframe terminal with stepped teletype text buffer",
            "prompt_fa": "ترمینال مِین فریم دهه ۸۰ با مانیتور فسفری کهربایی، بافت اسکن لاین و فونت مونو کامپیوتری",
            "domain": "retro_hardware",
            "confidence": "98%",
            "style_en": "Retro Computing (CRT Phosphor)",
            "style_fa": "محاسبات کلاسیک و نمایشگر فسفری (CRT)",
            "material_en": "Amber CRT Glow + Phosphor Screen",
            "material_fa": "درخشش کهربایی CRT + فسفر کلاسیک",
            "decision_en": "Early digital hardware authenticity demands strict 80x25 character grid, amber-on-black contrast, and zero modern blurs.",
            "decision_fa": "شبیه سازی اصیل سخت افزارهای اولیه مستلزم گرید ۸۰ در ۲۵ کاراکتر، رنگ کهربایی روی مشکی و حذف هرگونه استایل مدرن است.",
            "avoid_en": "Modern border radius, soft drop shadows, rich color graphics, anti-aliased smooth curves.",
            "avoid_fa": "گوشه های گرد مدرن، سایه های سافت، تصاویر رنگارنگ غنی، انحناهای نرم معاصر.",
            "contrast": "19.8 : 1 (AAA)",
            "quality": "99 / 100",
            "touch": "44px (Compliant)",
            "bidi": "Fixed Terminal Monospace",
            "title_en": "VT220 Terminal • System V Release 2",
            "title_fa": "ترمینال سیستم ۵ یونیکس • مانیتور VT220",
            "subtitle_en": "TTY04 Connected • Baud Rate: 9600 8-N-1",
            "subtitle_fa": "پورت TTY04 متصل • نرخ بود: ۹۶۰۰ بیت بر ثانیه",
            "badge_en": "BELL 103 ON",
            "badge_fa": "مودم متصل",
            "value": "LOGIN: root",
            "subval_en": "Core Storage: 640 KB Free • Disk: RK05 Mounted",
            "subval_fa": "حافظه رم آزاد: ۶۴۰ کیلوبایت • دیسک خوانده شد",
            "action_en": "Execute /bin/sh",
            "action_fa": "اجرای خط فرمان یونیکس",
            "secondary_en": "Memory Dump",
            "secondary_fa": "خروجی حافظه فیزیکی",
            "codeTailwind": """<div class="rounded-none border border-amber-600/60 bg-[#110c00] p-5 text-amber-500 font-mono tracking-wider">
  <div class="flex items-center justify-between border-b border-amber-900/60 pb-2 text-xs">
    <span>DEC VT220 CONSOLE</span>
    <span class="animate-pulse">CURSOR ON</span>
  </div>
  <div class="my-4 space-y-1">
    <div class="text-xl font-bold tracking-widest text-amber-400">SYS_V_R2 $ ready</div>
    <p class="text-xs text-amber-600">Free memory: 640 KB • TTY: /dev/tty01 • 9600 BAUD</p>
  </div>
  <button type="button" class="w-full border border-amber-500 bg-amber-950/40 hover:bg-amber-500 hover:text-black text-amber-400 font-bold py-2 text-xs uppercase tracking-widest transition-colors">INITIATE DISK BOOT</button>
</div>"""
        },

        # 17. Y2K Cyber Optimism
        "y2k_aesthetic": {
            "prompt_en": "Y2K Cyber Millennium translucent MP3 media player with bubbly silver chrome accents",
            "prompt_fa": "پلیر موزیک هزاره دوم (Y2K) با بدنه شیشه ای ژله ای شفاف و لبه های کروم نقره ای براق",
            "domain": "music_media_player",
            "confidence": "95%",
            "style_en": "Y2K Cyber Optimism (Chrome)",
            "style_fa": "خوش بینی دیجیتال Y2K و ژله ای (Y2K)",
            "material_en": "Translucent Jelly + Silver Sheen",
            "material_fa": "شیشه ژله ای شفاف + جلای نقره ای کروم",
            "decision_en": "Millennium nostalgia requires pill capsule shapes, chrome highlights, sky blue gradients, and bouncy springs.",
            "decision_fa": "نوستالژی سال ۲۰۰۰ نیازمند دکمه های کپسولی بیضی، هایلایت های نقره ای کروم و رنگ های آبی آسمانی براق است.",
            "avoid_en": "Monochrome grays, brutalist right angles, dry academic serif fonts.",
            "avoid_fa": "خاکستری های مات بی روح، زوایای خشک بروتالیستی، فونت های کتابی رسمی.",
            "contrast": "15.8 : 1 (AAA)",
            "quality": "96 / 100",
            "touch": "48px (Compliant)",
            "bidi": "Pop Centered",
            "title_en": "CyberDisc MP3 Capsule 256MB",
            "title_fa": "دستگاه پخش موسیقی سایبر دیسک ۲۵۶ مگابایت",
            "subtitle_en": "Electronic Dreamscape • 320kbps Audio",
            "subtitle_fa": "موسیقی الکترونیک پاپ • نرخ بیت ۳۲۰",
            "badge_en": "PLAYING 03:42",
            "badge_fa": "در حال پخش",
            "value": "Starlight Odyssey",
            "subval_en": "EQ: MegaBass Super • Battery: 94%",
            "subval_fa": "اکولایزر: مگابیس فوق العاده • باتری: ۹۴٪",
            "action_en": "Next Track >>",
            "action_fa": "آهنگ بعدی >>",
            "secondary_en": "Toggle Shuffle",
            "secondary_fa": "پخش تصادفی",
            "codeTailwind": """<div class="rounded-3xl border-2 border-sky-300 bg-sky-100/40 backdrop-blur-sm p-6 text-sky-950 font-sans shadow-inner">
  <div class="flex items-center justify-between border-b border-sky-200 pb-3">
    <span class="text-xs font-bold uppercase tracking-wider text-sky-700">CyberPod 2000</span>
    <span class="rounded-full bg-sky-200 px-3 py-0.5 text-xs font-semibold text-sky-800">MP3 LIVE</span>
  </div>
  <div class="my-4 text-center">
    <h3 class="text-xl font-bold tracking-tight text-sky-900">Starlight Odyssey</h3>
    <p class="text-xs text-sky-700 mt-1">Neo-Trance Anthem • 320 kbps High Definition</p>
  </div>
  <div class="flex gap-2">
    <button type="button" class="flex-1 rounded-full bg-gradient-to-r from-sky-400 to-indigo-500 hover:from-sky-300 hover:to-indigo-400 text-white font-bold py-2.5 text-xs shadow-md transition-all">Play Track</button>
    <button type="button" class="rounded-full bg-white/80 border border-sky-300 text-sky-800 font-bold px-4 py-2.5 text-xs shadow-sm">Next &gt;&gt;</button>
  </div>
</div>"""
        },

        # 18. Enterprise Dense Data Grid
        "enterprise_dense": {
            "prompt_en": "Enterprise supply chain inventory tracker with high-density tabular matrix and audit log",
            "prompt_fa": "سامانه مدیریت زنجیره تامین و انبارداری سازمانی با گرید داده های فشرده و لاگ رهگیری",
            "domain": "enterprise_logistics",
            "confidence": "97%",
            "style_en": "Enterprise Dense Data Grid",
            "style_fa": "سازمانی داده فشرده و جدول محور (Enterprise)",
            "material_en": "Slate Neutral + Compact Cells",
            "material_fa": "رنگ خنثی اسلیت + سلول های داده متراکم",
            "decision_en": "Operations workflow demands maximum information density per square inch, 4px corners, and immediate row inspection.",
            "decision_fa": "گردش کار لجستیک نیازمند حداکثر تراکم اطلاعات در هر اینچ مربع، گوشه های ۴ پیکسل و اسکن آنی ردیف ها است.",
            "avoid_en": "Giant marketing headers, decorative fluff, wasted padding, low-contrast subtle text.",
            "avoid_fa": "هدرهای تبلیغاتی غول پیکر، تزئینات بی فایده، فضاهای خالی هدررفته، متون کم رنگ.",
            "contrast": "18.0 : 1 (AAA)",
            "quality": "98 / 100",
            "touch": "44px (Compliant)",
            "bidi": "Data Grid Resilient",
            "title_en": "SKU Inventory: Warehouse West-3",
            "title_fa": "موجودی کالا: انبار شماره ۳ غرب کشور",
            "subtitle_en": "4,820 Pallets Active • Dispatch Queue: 42 Trucks",
            "subtitle_fa": "۴۸۲۰ پالت فعال • صف بارگیری: ۴۲ کامیون ترانزیت",
            "badge_en": "DISPATCH READY",
            "badge_fa": "آماده ترخیص",
            "value": "4,820 Units Stored",
            "subval_en": "Turnover Velocity: 2.4 Days • Variance: 0.01%",
            "subval_fa": "نرخ گردش کالا: ۲.۴ روز • خطای انبارگردانی: ۰.۰۱٪",
            "action_en": "Generate Dispatch Manifest",
            "action_fa": "صدور مانیفست خروج کالا",
            "secondary_en": "Audit Row Log",
            "secondary_fa": "لاگ ممیزی بارکد",
            "codeTailwind": """<div class="rounded border border-slate-300 bg-white p-4 text-slate-900 font-sans shadow-sm">
  <div class="flex items-center justify-between border-b border-slate-200 pb-2 text-xs">
    <span class="font-bold text-slate-700">WAREHOUSE INVENTORY // SKU-840</span>
    <span class="rounded bg-slate-100 px-2 py-0.5 font-mono text-slate-600">INSPECTION PASSED</span>
  </div>
  <div class="my-3 space-y-1">
    <div class="text-2xl font-bold tracking-tight text-slate-900">4,820 Units Active</div>
    <p class="text-xs text-slate-600">Turnover Cycle: 2.4 Days • Temperature Controlled: 4°C</p>
  </div>
  <button type="button" class="w-full rounded bg-slate-900 hover:bg-slate-800 text-white font-medium py-2 text-xs transition-colors">Export Dispatch Manifest</button>
</div>"""
        },

        # 19. High-Frequency Financial Terminal
        "financial_terminal": {
            "prompt_en": "Bloomberg-style multi-monitor equity derivatives order execution desk with sub-millisecond book depth",
            "prompt_fa": "ترمینال معاملات مشتقات سهام به سبک بلومبرگ با عمق بازار زیر میلی ثانیه و دفتر سفارشات",
            "domain": "capital_markets",
            "confidence": "98%",
            "style_en": "Financial Terminal (Capital Markets)",
            "style_fa": "ترمینال مالی و بازارهای سرمایه (Financial Terminal)",
            "material_en": "Deep Abyss Black + Monospace Grid",
            "material_fa": "مشکی مطلق + گرید چندپنجره ای مونو",
            "decision_en": "Institutional trading desks demand strict 0px edges, monospace tabular numbers, and amber/cyan status alerts.",
            "decision_fa": "میزهای معاملات وال استریت نیازمند لبه های تیز ۰ پیکسل، فونت های مونو اسپیس و هشدارهای پرکنتراست هستند.",
            "avoid_en": "Consumer rounded cards, decorative pastel illustrations, soft shadows.",
            "avoid_fa": "کارت های گرد فانتزی، نقاشی های پاستلی کودکانه، سایه های محو دکوراتیو.",
            "contrast": "20.1 : 1 (AAA)",
            "quality": "99 / 100",
            "touch": "44px (Compliant)",
            "bidi": "Strict Terminal LTR",
            "title_en": "SPX Index Derivatives Order Desk",
            "title_fa": "میز سفارشات آپشن و مشتقات شاخص S&P 500",
            "subtitle_en": "Bid: 5,482.25 • Ask: 5,482.50 • Volume: 1.4M",
            "subtitle_fa": "مظنه خرید: ۵,۴۸۲.۲۵ • مظنه فروش: ۵,۴۸۲.۵۰ • حجم: ۱.۴ میلیون",
            "badge_en": "MATCH ENGINE 12μs",
            "badge_fa": "موتور تطبیق ۱۲ میکروثانیه",
            "value": "5,482.25 BID",
            "subval_en": "Spread: 0.25 pt • Institutional Flow: Long Bias",
            "subval_fa": "اسپرد: ۰.۲۵ پوینت • جریان نهادی: برتری خریداران",
            "action_en": "Transmit Limit Order",
            "action_fa": "ارسال سفارش لیمیت به بورس",
            "secondary_en": "Cancel All Working",
            "secondary_fa": "لغو تمام سفارشات باز",
            "codeTailwind": """<div class="rounded-none border border-neutral-800 bg-black p-4 text-neutral-200 font-mono">
  <div class="flex items-center justify-between border-b border-neutral-900 pb-2 text-xs">
    <span class="text-amber-400 font-bold">SPX 0DTE ORDER DEPTH</span>
    <span class="text-neutral-500">CBOE DIRECT</span>
  </div>
  <div class="my-3 flex justify-between items-baseline">
    <div class="text-2xl font-bold text-emerald-400">5,482.25 <span class="text-xs text-neutral-400">BID</span></div>
    <div class="text-2xl font-bold text-red-400">5,482.50 <span class="text-xs text-neutral-400">ASK</span></div>
  </div>
  <button type="button" class="w-full border border-neutral-700 bg-neutral-900 hover:bg-neutral-800 text-neutral-100 font-bold py-2 text-xs uppercase tracking-wider">Execute Limit Block</button>
</div>"""
        },

        # 20. Civic Institutional Public
        "civic_institutional": {
            "prompt_en": "Accessible national public citizen service portal for digital passport renewal and identity verification",
            "prompt_fa": "درگاه ملی خدمات الکترونیک دولت برای تمدید گذرنامه و احراز هویت هوشمند شهروندی",
            "domain": "government_public",
            "confidence": "98%",
            "style_en": "Civic Institutional Public",
            "style_fa": "نهادی و خدمات عمومی دولتی (Civic Utility)",
            "material_en": "Parchment High Contrast + Deep Navy",
            "material_fa": "پس زمینه رسمی با کنتراست بالا + سرمه ای رسمی",
            "decision_en": "Universal accessibility mandates WCAG AAA clarity, minimum 48px touch targets, and clear multi-step progress indicators.",
            "decision_fa": "دسترس پذیری همگانی رعایت سخت گیرانه استاندارد WCAG AAA، دکمه های حداقل ۴۸ پیکسل و مراحل شفاف را ضروری می سازد.",
            "avoid_en": "Low contrast text, frivolous motion, dark mysterious modes, hidden dropdowns.",
            "avoid_fa": "متن با کنتراست ضعیف، حرکات نمایشی، تم های دارک تاریک، منوهای مخفی تو در تو.",
            "contrast": "19.2 : 1 (AAA)",
            "quality": "99 / 100",
            "touch": "48px (Compliant)",
            "bidi": "Universal RTL/LTR Accessible",
            "title_en": "National Digital Identity Service",
            "title_fa": "درگاه ملی هویت هوشمند و خدمات شهروندی",
            "subtitle_en": "Official Public Portal • Certified Level 3 Security",
            "subtitle_fa": "سامانه رسمی دولتی • دارای گواهی امنیتی سطح ۳",
            "badge_en": "OFFICIAL PORTAL",
            "badge_fa": "درگاه رسمی",
            "value": "Citizen Services Active",
            "subval_en": "Digital Passport Renewal • Avg Processing: 2 Days",
            "subval_fa": "تمدید آنلاین پاسپورت • میانگین زمان صدور: ۲ روز کاری",
            "action_en": "Start Secure Renewal",
            "action_fa": "ورود به فرآیند ثبت درخواست",
            "secondary_en": "Check Application Status",
            "secondary_fa": "پیگیری وضعیت پرونده با کد رهگیری",
            "codeTailwind": """<div class="rounded border-2 border-blue-900 bg-[#f8f9fa] p-6 text-blue-950 font-sans shadow-sm">
  <div class="flex items-center justify-between border-b-2 border-blue-900 pb-3">
    <span class="text-xs font-bold tracking-wider uppercase text-blue-900">National Citizen Portal</span>
    <span class="rounded bg-blue-100 px-2.5 py-0.5 text-xs font-bold text-blue-950">Official</span>
  </div>
  <div class="my-4">
    <h3 class="text-xl font-bold text-blue-950">Digital Passport Renewal</h3>
    <p class="text-xs text-blue-900 mt-1 leading-relaxed">Secure, biometric-verified renewal service with home courier delivery.</p>
  </div>
  <button type="button" class="w-full rounded bg-blue-900 hover:bg-blue-800 text-white font-bold py-3 text-xs tracking-wider transition-colors">Start Application (Step 1 of 3)</button>
</div>"""
        },

        # 21. Playful Consumer / Bubbly
        "playful_consumer": {
            "prompt_en": "Gamified habit tracker and daily mindfulness streak app with delightful rewards and pill cards",
            "prompt_fa": "اپلیکیشن ردیاب عادات روزانه و مدیتیشن همراه با گیمیفیکیشن، پاداش های انیمیشنی و کارت های حبابی",
            "domain": "consumer_habits",
            "confidence": "96%",
            "style_en": "Playful Consumer / Bubbly",
            "style_fa": "مصرف کننده شاداب و تعاملی (Playful Consumer)",
            "material_en": "Candy Pop Canvas + Cushion Soft Shadows",
            "material_fa": "بوم آب نباتی شاداب + سایه های بالشتی نرم",
            "decision_en": "Positive habit reinforcement leverages bouncy springs, friendly rounded radii, and celebratory milestone chips.",
            "decision_fa": "تثبیت عادات مثبت از المان های فنری شاد، انحناهای ۱۸ پیکسلی گرم و کارت های تشویقی استفاده می کند.",
            "avoid_en": "Cold monochrome palettes, dry technical tables, harsh intimidating angles.",
            "avoid_fa": "پالت های خاکستری سرد و خسته کننده، جدول های خشک اداری، زوایای تیز ترساننده.",
            "contrast": "16.5 : 1 (AAA)",
            "quality": "97 / 100",
            "touch": "48px (Compliant)",
            "bidi": "Friendly Centered",
            "title_en": "Daily Habit Streak: Morning Meditation",
            "title_fa": "زنجیره عادات روزانه: تمرکز صبحگاهی",
            "subtitle_en": "Day 24 Unlocked! • 1,200 Focus XP Earned",
            "subtitle_fa": "روز ۲۴ پیوسته! • ۱۲۰۰ امتیاز تمرکز کسب شد",
            "badge_en": "🔥 24-DAY STREAK",
            "badge_fa": "🔥 ۲۴ روز متوالی",
            "value": "24 Days Mastered",
            "subval_en": "Only 6 Days to 30-Day Master Milestone Badge",
            "subval_fa": "فقط ۶ روز تا دریافت نشان طلایی یک ماهه",
            "action_en": "Complete Today's Session",
            "action_fa": "تکمیل تمرین امروز (+۵۰ امتیاز)",
            "secondary_en": "Share Streak",
            "secondary_fa": "اشتراک با دوستان",
            "codeTailwind": """<div class="rounded-3xl border-2 border-indigo-200 bg-indigo-50/50 p-6 text-indigo-950 font-sans shadow-sm">
  <div class="flex items-center justify-between border-b border-indigo-100 pb-3">
    <span class="text-xs font-bold text-indigo-600">Daily Mindfulness</span>
    <span class="rounded-full bg-amber-400 px-2.5 py-0.5 text-xs font-black text-amber-950">🔥 24 DAYS</span>
  </div>
  <div class="my-4 text-center">
    <div class="text-3xl font-black text-indigo-900">Morning Meditation</div>
    <p class="text-xs font-medium text-indigo-700 mt-1">Keep your daily streak alive and unlock the Bronze Focus Badge.</p>
  </div>
  <button type="button" class="w-full rounded-2xl bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-3 text-xs shadow-md transition-all">Complete Session (+50 XP)</button>
</div>"""
        },

        # 22. Mobile-Native Sheet & Stack
        "mobile_native_consumer": {
            "prompt_en": "Ergonomic mobile checkout sheet with bottom thumb zone, payment stack, and 48px touch targets",
            "prompt_fa": "صفحه پرداخت نیتیو موبایل با ناحیه ارگونومیک شست دست، شیت متحرک و دکمه های لمسی ۴۸ پیکسلی",
            "domain": "mobile_commerce",
            "confidence": "97%",
            "style_en": "Mobile-Native Sheet & Stack",
            "style_fa": "نیتیو موبایل و ارگونومیک (Mobile Native)",
            "material_en": "Frosted Touch Glass + Grabber Indicator",
            "material_fa": "شیشه مات لمسی + دستگیره بالایی اسلاید",
            "decision_en": "Handheld ergonomics require bottom-anchored action stacks, 48px touch targets, and springy swipe-down dismiss.",
            "decision_fa": "ارگونومی گوشی موبایل تمرکز دکمه ها در پایین صفحه (دسترس شست)، تارگت های ۴۸ پیکسل و حرکت روان شیت را می طلبد.",
            "avoid_en": "Tiny touch areas below 44px, hover-dependent tooltips, multi-column desktop layouts.",
            "avoid_fa": "دکمه های ریز زیر ۴۴ پیکسل، تولتیپ های وابسته به ماوس، ستون های عریض دسکتاپی.",
            "contrast": "16.8 : 1 (AAA)",
            "quality": "98 / 100",
            "touch": "48px (Compliant)",
            "bidi": "Thumb-Zone Mobile Ready",
            "title_en": "Express Order Checkout",
            "title_fa": "تسویه حساب سریع سفارش",
            "subtitle_en": "Delivering to Tehran, Jordan Ave • 35 Min",
            "subtitle_fa": "ارسال به تهران، جردن • تحویل در ۳۵ دقیقه",
            "badge_en": "APPLE PAY / SHETAB",
            "badge_fa": "پرداخت شتابی",
            "value": "Total: 1,480,000 T",
            "subval_en": "Free Courier Delivery + Carbon Offset Included",
            "subval_fa": "پیک اکسپرس رایگان + بیمه کامل کالا",
            "action_en": "Slide to Pay & Confirm",
            "action_fa": "تایید و پرداخت آنی سفارش",
            "secondary_en": "Change Address",
            "secondary_fa": "تغییر آدرس تحویل",
            "codeTailwind": """<div class="rounded-3xl border border-zinc-200/60 bg-white/95 backdrop-blur-md p-6 text-zinc-900 font-sans shadow-xl">
  <div class="w-12 h-1.5 bg-zinc-300 rounded-full mx-auto mb-4"></div>
  <div class="flex items-center justify-between border-b border-zinc-100 pb-3">
    <span class="text-xs font-semibold text-zinc-600">Express Delivery (35 min)</span>
    <span class="text-xs font-bold text-emerald-600">Free Courier</span>
  </div>
  <div class="my-4">
    <div class="text-2xl font-extrabold text-zinc-950">1,480,000 تومان</div>
    <p class="text-xs text-zinc-500 mt-0.5">Tehran, Jordan Ave • Courier assigned</p>
  </div>
  <button type="button" class="w-full rounded-2xl bg-zinc-900 hover:bg-black text-white font-bold py-3.5 text-xs tracking-wider transition-colors min-h-[48px]">Slide to Confirm Payment</button>
</div>"""
        },

        # 23. Monochrome Art Gallery
        "art_gallery": {
            "prompt_en": "Contemporary sculpture exhibition catalog with stark white void, zero borders, and vast whitespace",
            "prompt_fa": "کاتالوگ گالری مجسمه سازی معاصر با فضای منفی وسیع، حذف کامل بوردرها و تایپوگرافی مجلل",
            "domain": "contemporary_art",
            "confidence": "96%",
            "style_en": "Monochrome Art Gallery",
            "style_fa": "گالری هنری، استوار و مینیمال (Art Gallery)",
            "material_en": "Chalk White Void + Solitary Plinth",
            "material_fa": "فضای منفی گچی سفید + نمایش پایه تندیس",
            "decision_en": "Curatorial minimalism eliminates all decorative frames, providing 220% whitespace to foreground the artwork.",
            "decision_fa": "نگاه کیوریتوری مدرن هرگونه کادر اضافه را حذف کرده و ۲۲۰٪ فضای تنفس سفید برای درخشش اثر هنری فراهم می کند.",
            "avoid_en": "Visible borders, heavy drop shadows, colorful buttons, busy navigation bars.",
            "avoid_fa": "بوردرهای خطی ضخیم، سایه های سنگین، دکمه های رنگارنگ تجاری، منوهای شلوغ.",
            "contrast": "21.0 : 1 (AAA)",
            "quality": "99 / 100",
            "touch": "44px (Compliant)",
            "bidi": "Poetic Curatorial Flow",
            "title_en": "Anselm Kiefer: The Spatial Memory",
            "title_fa": "آنسلم کیفر: حافظه فضایی و ماده",
            "subtitle_en": "Monumental Bronze & Lead • Hall 4",
            "subtitle_fa": "مجسمه های برنز و سرب • سالن شماره ۴",
            "badge_en": "SOLITARY PLINTH",
            "badge_fa": "اثر برگزیده",
            "value": "Lead, Iron, Mixed Media",
            "subval_en": "340 × 280 × 120 cm • 2026 Foundation Collection",
            "subval_fa": "۳۴۰ در ۲۸۰ سانتی متر • مجموعه دائمی موزه",
            "action_en": "Request Curatorial Monograph",
            "action_fa": "درخواست مونوگراف کیوریتور",
            "secondary_en": "Exhibition Map",
            "secondary_fa": "نقشه راهنمای گالری",
            "codeTailwind": """<div class="rounded-none border-0 bg-[#fcfbf9] p-8 text-black font-serif shadow-none">
  <div class="flex items-center justify-between border-b border-black/10 pb-4 text-xs font-sans">
    <span class="tracking-widest uppercase text-neutral-500">PAVILION // 04</span>
    <span class="italic text-neutral-600">Permanent Collection</span>
  </div>
  <div class="my-8">
    <h3 class="text-3xl font-light tracking-widest text-black leading-snug">The Spatial Memory</h3>
    <p class="text-xs text-neutral-600 font-sans mt-3 max-w-sm leading-relaxed">Cast bronze, cold-rolled lead, and oxidized iron pigment on canvas foundation.</p>
  </div>
  <button type="button" class="w-full bg-black text-white hover:bg-neutral-800 py-3 text-xs font-sans uppercase tracking-widest transition-colors">Inquire with Director</button>
</div>"""
        },

        # 24. High-End Hospitality & Dining
        "high_end_hospitality": {
            "prompt_en": "Michelin 3-Star fine dining reservation concierge with velvet obsidian background and warm brass glow",
            "prompt_fa": "سامانه رزرو اختصاصی رستوران ستاره دار میشلن با پس زمینه مخملی تیره و بازتاب برنجی طلایی",
            "domain": "luxury_hospitality",
            "confidence": "97%",
            "style_en": "High-End Hospitality & Dining",
            "style_fa": "هتلداری لوکس و رستوران های مجلل (Hospitality)",
            "material_en": "Velvet Obsidian + Warm Brass Accent",
            "material_fa": "مشکی مخملی عمیق + جزئیات برنجی طلایی",
            "decision_en": "Sensory luxury dining requires deep velvety obsidian, letterspaced titles, and an intimate concierge booking flow.",
            "decision_fa": "تجربه حسی و فاخر میهمان نوازی نیازمند مشکی مخملی، حروف بافاصله باوقار و خدمات تشریفات اختصاصی است.",
            "avoid_en": "Bright synthetic blues, flat stark borders, crowded tabular data grids.",
            "avoid_fa": "آبی های شیمیایی زننده، خطوط خشک اداری، جدول های فشرده بدون احساس.",
            "contrast": "16.4 : 1 (AAA)",
            "quality": "98 / 100",
            "touch": "48px (Compliant)",
            "bidi": "Opulent Symmetrical",
            "title_en": "L'Orangerie • 3 Michelin Stars",
            "title_fa": "رستوران لورانژری • ۳ ستاره میشلن",
            "subtitle_en": "Autumn 12-Course Tasting Menu by Chef de Cuisine",
            "subtitle_fa": "منوی اختصاصی ۱۲ قسمتی پاییز به سرآشپزی گیوم",
            "badge_en": "RESERVATION EXCLUSIVE",
            "badge_fa": "رزرو تشریفات",
            "value": "Chef's Table Experience",
            "subval_en": "Sommelier Reserve Wine Pairing Included",
            "subval_fa": "همراه با نوشیدنی های نایاب دست چین شده سوملیه",
            "action_en": "Request Sommelier Table",
            "action_fa": "ثبت درخواست میز ویژه سرآشپز",
            "secondary_en": "View Seasonal Menu",
            "secondary_fa": "مشاهده منوی فصلی",
            "codeTailwind": """<div class="rounded-lg border border-amber-500/30 bg-[#0d0a07] p-6 text-amber-100 font-serif shadow-2xl">
  <div class="flex items-center justify-between border-b border-amber-500/20 pb-3">
    <span class="text-xs uppercase tracking-widest text-amber-400 font-sans">Palais Vendôme</span>
    <span class="text-xs italic text-amber-300/80">3 Michelin Stars</span>
  </div>
  <div class="my-5">
    <h3 class="text-2xl font-normal tracking-wide text-amber-50">L'Orangerie Tasting Menu</h3>
    <p class="text-xs text-amber-200/70 font-sans mt-1.5 leading-relaxed">Twelve seasonal movements curated by Master Chef with vintage grand cru pairing.</p>
  </div>
  <button type="button" class="w-full border border-amber-400 bg-amber-500/10 hover:bg-amber-400 hover:text-black text-amber-200 py-3 text-xs font-sans uppercase tracking-widest transition-all">Reserve Table</button>
</div>"""
        },

        # 25. Cultural Heritage & Archives
        "cultural_heritage": {
            "prompt_en": "National archival manuscript preservation viewer with aged vellum texture and fine etching rules",
            "prompt_fa": "سامانه آرشیو و نگهداری نسخ خطی کهن ملی با بافت پوستینه باستانی و خطوط ظریف قلمی",
            "domain": "cultural_heritage",
            "confidence": "97%",
            "style_en": "Cultural Heritage & Archives",
            "style_fa": "میراث فرهنگی، تاریخ و آرشیو (Cultural Heritage)",
            "material_en": "Aged Vellum + Fine Line Etching",
            "material_fa": "پوستینه کهن تاریخی + خطوط ظریف گراور",
            "decision_en": "Archival scholarship mandates aged vellum tones, classical serif balancing, and high-fidelity historic manuscript presentation.",
            "decision_fa": "پژوهش های تاریخی مستلزم رنگ های گرم پوستینه، تناسبات کلاسیک و نمایش اصیل متون کهن است.",
            "avoid_en": "Neon accents, modern sans-serif defaults, floating glass bubbles.",
            "avoid_fa": "رنگ های نئونی، فونت های دیجیتال سنز-سریف پیش فرض، افکت های شیشه ای حباب دار.",
            "contrast": "16.9 : 1 (AAA)",
            "quality": "98 / 100",
            "touch": "44px (Compliant)",
            "bidi": "Manuscript Archival Balance",
            "title_en": "Shahnameh of Baysunghur • 1430 CE",
            "title_fa": "شاهنامه بایسنقری • نسخه خطی کاخ گلستان ۸۰۹ هـ.ش",
            "subtitle_en": "UNESCO Memory of the World Register",
            "subtitle_fa": "ثبت شده در حافظه جهانی یونسکو • نگارگری تیموری",
            "badge_en": "RESTRICTED VAULT",
            "badge_fa": "گنجینه خطی",
            "value": "Illuminated Folio 42b",
            "subval_en": "Gold Leaf, Lapis Lazuli & Natural Mineral Inks",
            "subval_fa": "طلاکوب، لاجورد خالص نیشابور و جوهرهای معدنی",
            "action_en": "Inspect Folio in Ultra-HD",
            "action_fa": "بررسی نگاره با بزرگنمایی فراصوت",
            "secondary_en": "Scholarly Notes",
            "secondary_fa": "یادداشت های تصحیح متن",
            "codeTailwind": """<div class="rounded-sm border border-amber-950/30 bg-[#f5efe4] p-6 text-[#2b1d14] font-serif shadow-sm">
  <div class="flex items-center justify-between border-b border-amber-950/20 pb-3 text-xs">
    <span class="font-bold tracking-widest text-[#6d4c36]">UNESCO REGISTER № 1430</span>
    <span class="italic text-[#7d5840]">Baysunghuri Folio</span>
  </div>
  <div class="my-5">
    <h3 class="text-2xl font-bold text-[#23170e]">شاهنامه نگارگری بایسنقری</h3>
    <p class="text-xs text-[#5a3f2d] mt-2 leading-relaxed">نسخه اصل محفوظ در گنجینه سلطنتی؛ تصویرسازی صحنه نبرد رستم و اسفندیار با لاجورد و طلای ناب.</p>
  </div>
  <button type="button" class="w-full border border-[#2b1d14] bg-[#2b1d14] hover:bg-[#432d20] text-[#f5efe4] py-3 text-xs uppercase tracking-wider transition-colors">Inspect High-Res Folio</button>
</div>"""
        },

        # 26. Scientific Instrumentation & Bio
        "scientific_dashboard": {
            "prompt_en": "Genomic sequencer mass-spectrometry telemetry panel with wavelength grid and calibration gates",
            "prompt_fa": "پنل تله متری دستگاه توالی یابی ژنتیک و طیف سنج جرمی با گرید فرکانسی و کالیبراسیون دقیق",
            "domain": "biotech_scientific",
            "confidence": "98%",
            "style_en": "Scientific Instrumentation & Bio",
            "style_fa": "تجهیزات آزمایشگاهی و داده های علمی (Scientific)",
            "material_en": "Cleanroom Slate + Wavelength Grid",
            "material_fa": "اسلیت اتاق تمیز + گرید طول موج دقیق",
            "decision_en": "Empirical scientific telemetry demands strict monospace numeric precision, dark cleanroom slate, and verified error tolerances.",
            "decision_fa": "تله متری آزمایشگاهی نیازمند دقت عددی مونو اسپیس، تم تیره اتاق تمیز و خطاهای اعشاری کالیبره شده است.",
            "avoid_en": "Decorative fluff, imprecise curved shapes, illegible cursive fonts.",
            "avoid_fa": "تزئینات اضافی، فرم های گرد غیردقیق، فونت های دست نویس ناخوانا.",
            "contrast": "18.4 : 1 (AAA)",
            "quality": "99 / 100",
            "touch": "44px (Compliant)",
            "bidi": "Calibrated LTR Monospace",
            "title_en": "NanoDrop Spectrometer • Assay #412",
            "title_fa": "اسپکترومتر نانودراپ • آزمایش ژنوم شماره ۴۱۲",
            "subtitle_en": "DNA Concentration: 142.8 ng/μL • A260/A280: 1.84",
            "subtitle_fa": "غلظت DNA: ۱۴۲.۸ نانوگرم بر میکرولیتر • نسبت A260/A280: ۱.۸۴",
            "badge_en": "CALIBRATED ±0.01%",
            "badge_fa": "کالیبره ±۰.۰۱٪",
            "value": "A260/A280: 1.84",
            "subval_en": "Purity Ratio: Pure DNA • Zero RNA Contamination",
            "subval_fa": "خلوص ژنتیکی: DNA خالص • بدون آلودگی پروتئینی",
            "action_en": "Export Mass Spec Curve",
            "action_fa": "خروجی منحنی طیف نوری",
            "secondary_en": "Recalibrate Sensor",
            "secondary_fa": "کالیبراسیون مجدد سنسور",
            "codeTailwind": """<div class="rounded-md border border-slate-700 bg-slate-900 p-5 text-emerald-300 font-mono text-xs shadow-md">
  <div class="flex items-center justify-between border-b border-slate-800 pb-2">
    <span class="text-slate-400 font-bold">SPECTRO TELEMETRY // CH-01</span>
    <span class="text-emerald-400 font-bold">PURITY: 1.84</span>
  </div>
  <div class="my-4">
    <div class="text-2xl font-bold text-white tracking-wider">142.8 ng/μL</div>
    <p class="text-slate-400 mt-1">Absorbance at 260nm: 2.856 • Baseline offset: 0.002</p>
  </div>
  <button type="button" class="w-full rounded border border-emerald-500 bg-emerald-950/60 hover:bg-emerald-900 text-emerald-200 font-bold py-2 uppercase tracking-wider transition-colors">Export Spectrum Curve</button>
</div>"""
        }
    }

def main():
    scenarios = get_scenarios()
    print(f"[INFO] Loaded {len(scenarios)} full design scenarios covering all 26 canonical style families.")

    scenarios_js = json.dumps(scenarios, indent=6, ensure_ascii=False)

    # 1. Update index.html
    update_file(INDEX_PATH, scenarios_js)
    # 2. Update showcase/index.html
    update_file(SHOWCASE_PATH, scenarios_js)

def update_file(file_path, scenarios_js):
    if not file_path.exists():
        print(f"[WARN] {file_path} not found")
        return

    content = file_path.read_text(encoding="utf-8")

    # Replace STUDIO_SCENARIOS
    pattern = r"const STUDIO_SCENARIOS\s*=\s*\{.*?\n    \};"
    replacement = f"const STUDIO_SCENARIOS = {scenarios_js};"
    
    new_content, count = re.subn(pattern, replacement, content, flags=re.DOTALL)
    if count == 0:
        print(f"[FAIL] Could not locate STUDIO_SCENARIOS in {file_path}")
        return

    # Update compileStudioPrompt keyword matcher to cover all 26 styles
    matcher_code = """function compileStudioPrompt() {
      const text = (document.getElementById('studioPromptInput')?.value || '').toLowerCase();
      let matched = 'crypto';

      // 26 Style Family Keyword Resolver
      if (text.includes('swiss') || text.includes('سوئیس') || text.includes('posters') || text.includes('zürich') || text.includes('زوریخ')) matched = 'minimal_swiss';
      else if (text.includes('brutal') || text.includes('بروتال') || text.includes('acid') || text.includes('اسید') || text.includes('pop')) matched = 'neobrutalism';
      else if (text.includes('nordic') || text.includes('نوردیک') || text.includes('acoustic') || text.includes('آکوستیک') || text.includes('scandi') || text.includes('اسکاندیناوی')) matched = 'organic_nordic';
      else if (text.includes('bauhaus') || text.includes('باهاوس') || text.includes('weimar') || text.includes('وایمار') || text.includes('gropius')) matched = 'bauhaus_geometric';
      else if (text.includes('glass') || text.includes('شیشه') || text.includes('fresnel') || text.includes('فرنل') || text.includes('translucent')) matched = 'modern_glass_2';
      else if (text.includes('cyber') || text.includes('سایبر') || text.includes('synthwave') || text.includes('neon') || text.includes('نئون')) matched = 'retro_futurism';
      else if (text.includes('magazine') || text.includes('نشریه') || text.includes('مجله') || text.includes('essay') || text.includes('جستار') || text.includes('نقد')) matched = 'editorial_magazine';
      else if (text.includes('industrial') || text.includes('صنعتی') || text.includes('breaker') || text.includes('turbine') || text.includes('توربین') || text.includes('نیروگاه')) matched = 'industrial_utility';
      else if (text.includes('moss') || text.includes('خزه') || text.includes('breath') || text.includes('تنفس') || text.includes('طبیعت') || text.includes('biophilic') || text.includes('مدیتیشن')) matched = 'biophilic_wellness';
      else if (text.includes('aero') || text.includes('هوانوردی') || text.includes('space') || text.includes('فضا') || text.includes('orbit') || text.includes('مدار')) matched = 'futuristic_tech';
      else if (text.includes('crt') || text.includes('فسفر') || text.includes('vt220') || text.includes('80s') || text.includes('دهه ۸۰') || text.includes('mainframe')) matched = 'retro_computing_80s';
      else if (text.includes('y2k') || text.includes('هزاره') || text.includes('jelly') || text.includes('ژله') || text.includes('mp3')) matched = 'y2k_aesthetic';
      else if (text.includes('dense') || text.includes('انبار') || text.includes('inventory') || text.includes('warehouse') || text.includes('لجستیک')) matched = 'enterprise_dense';
      else if (text.includes('terminal') || text.includes('bloomberg') || text.includes('بلومبرگ') || text.includes('derivatives') || text.includes('مشتقات') || text.includes('سهام')) matched = 'financial_terminal';
      else if (text.includes('citizen') || text.includes('شهروند') || text.includes('دولت') || text.includes('گذرنامه') || text.includes('passport') || text.includes('civic')) matched = 'civic_institutional';
      else if (text.includes('habit') || text.includes('عادت') || text.includes('streak') || text.includes('bubbly') || text.includes('بازی')) matched = 'playful_consumer';
      else if (text.includes('mobile') || text.includes('موبایل') || text.includes('checkout') || text.includes('تسویه') || text.includes('thumb') || text.includes('شست')) matched = 'mobile_native_consumer';
      else if (text.includes('gallery') || text.includes('گالری') || text.includes('sculpture') || text.includes('مجسمه') || text.includes('art') || text.includes('هنر')) matched = 'art_gallery';
      else if (text.includes('michelin') || text.includes('میشلن') || text.includes('dining') || text.includes('رستوران') || text.includes('هتل') || text.includes('hospitality')) matched = 'high_end_hospitality';
      else if (text.includes('heritage') || text.includes('میراث') || text.includes('شاهنامه') || text.includes('نسخه خطی') || text.includes('archival') || text.includes('مخطوط')) matched = 'cultural_heritage';
      else if (text.includes('spectro') || text.includes('طیف') || text.includes('dna') || text.includes('ژنتیک') || text.includes('bio') || text.includes('آزمایشگاه')) matched = 'scientific_dashboard';
      else if (text.includes('k8s') || text.includes('observ') || text.includes('cpu') || text.includes('ترمینال') || text.includes('کوبرنتیز')) matched = 'k8s';
      else if (text.includes('لوکس') || text.includes('luxury') || text.includes('معماری') || text.includes('penthouse') || text.includes('پنت')) matched = 'luxury';
      else if (text.includes('پوست') || text.includes('زیبایی') || text.includes('clinic') || text.includes('پزشک') || text.includes('درمان')) matched = 'clinic';
      else if (text.includes('saas') || text.includes('billing') || text.includes('stripe') || text.includes('اشتراک') || text.includes('سازمان')) matched = 'stripe';
      else if (text.includes('صرافی') || text.includes('crypto') || text.includes('معامله') || text.includes('trading') || text.includes('رمزارز')) matched = 'crypto';

      currentStudioScenario = matched;
      // Sync selector dropdown if exists
      const select = document.getElementById('studioStyleSelect');
      if (select) select.value = matched;
      renderStudioUI(STUDIO_SCENARIOS[matched]);
    }"""

    prompt_matcher_pattern = r"function compileStudioPrompt\(\)\s*\{.*?\n    \}"
    new_content, m_count = re.subn(prompt_matcher_pattern, matcher_code, new_content, flags=re.DOTALL)
    if m_count == 0:
        print(f"[FAIL] Could not locate compileStudioPrompt in {file_path}")
        return

    # Update loadStudioScenario to sync select box
    new_load = """function loadStudioScenario(key) {
      currentStudioScenario = key;
      const sc = STUDIO_SCENARIOS[key];
      if (!sc) return;
      const isFa = currentLang === 'fa';
      const input = document.getElementById('studioPromptInput');
      if (input) input.value = isFa ? sc.prompt_fa : sc.prompt_en;
      const select = document.getElementById('studioStyleSelect');
      if (select) select.value = key;
      // Update chip active states
      document.querySelectorAll('.studio-chip').forEach(c => {
        c.classList.toggle('active', c.id === `chip-${key}`);
      });
      renderStudioUI(sc);
    }"""
    load_pattern = r"function loadStudioScenario\(key\)\s*\{.*?\n    \}"
    new_content, l_count = re.subn(load_pattern, new_load, new_content, flags=re.DOTALL)

    # Add style dropdown selector into the HTML right above the chips if not present
    select_html = """<!-- Style Family 26-Catalog Dropdown & Chips -->
      <div class="studio-selector-bar">
        <label for="studioStyleSelect" id="lblSelectStyle" style="font-size: 13px; font-weight: 600; color: var(--text-vivid);">🎨 Explore 26 Orthogonal Style Families:</label>
        <select id="studioStyleSelect" class="studio-select" onchange="loadStudioScenario(this.value)">
          <optgroup label="⚡ Tech & Capital Markets">
            <option value="crypto">Linear Deep Dark (Fintech / Crypto HUD)</option>
            <option value="k8s">Data-Dense Terminal HUD (DevOps / SRE)</option>
            <option value="financial_terminal">High-Frequency Financial Terminal</option>
            <option value="futuristic_tech">Futuristic Aerotech HUD</option>
            <option value="scientific_dashboard">Scientific Instrumentation & Bio</option>
          </optgroup>
          <optgroup label="💼 SaaS & Enterprise">
            <option value="stripe">Clean Stripe SaaS (Billing & Subscriptions)</option>
            <option value="minimal_swiss">Minimal Swiss / International</option>
            <option value="enterprise_dense">Enterprise Dense Data Grid</option>
            <option value="civic_institutional">Civic Institutional Public</option>
          </optgroup>
          <optgroup label="🏛️ Luxury & Editorial">
            <option value="luxury">Quiet Luxury (Prestige Architecture)</option>
            <option value="high_end_hospitality">High-End Hospitality & Dining</option>
            <option value="editorial_magazine">Swiss Editorial Magazine</option>
            <option value="art_gallery">Monochrome Art Gallery</option>
            <option value="cultural_heritage">Cultural Heritage & Archives</option>
          </optgroup>
          <optgroup label="🌿 Nature & Clinical Wellness">
            <option value="clinic">Soft Humanist (Clinical Healing)</option>
            <option value="biophilic_wellness">Biophilic Wellness (Living Moss)</option>
            <option value="organic_nordic">Organic Nordic (Scandinavian)</option>
          </optgroup>
          <optgroup label="🎨 Avant-Garde & Creative">
            <option value="neobrutalism">Neo-Brutalism (Raw High-Contrast)</option>
            <option value="bauhaus_geometric">Bauhaus Geometric (Constructivist)</option>
            <option value="modern_glass_2">Specular Glassmorphism 2.0</option>
          </optgroup>
          <optgroup label="🕹️ Retro & Cyber">
            <option value="retro_computing_80s">Retro Computing (1982 CRT Phosphor)</option>
            <option value="retro_futurism">Retro Futurism / Cyber Violet</option>
            <option value="y2k_aesthetic">Y2K Cyber Millennium Chrome</option>
          </optgroup>
          <optgroup label="📱 Mobile & Consumer">
            <option value="mobile_native_consumer">Mobile-Native Sheet & Stack</option>
            <option value="playful_consumer">Playful Consumer / Bubbly Streak</option>
          </optgroup>
        </select>
      </div>

      <!-- Quick Scenario Chips -->
      <div class="studio-chips" role="group" aria-label="Pre-loaded Design Scenarios">
        <button type="button" class="studio-chip active" id="chip-crypto" onclick="loadStudioScenario('crypto')">💳 Crypto HUD</button>
        <button type="button" class="studio-chip" id="chip-k8s" onclick="loadStudioScenario('k8s')">⚡ K8s Telemetry</button>
        <button type="button" class="studio-chip" id="chip-luxury" onclick="loadStudioScenario('luxury')">🏛️ Quiet Luxury</button>
        <button type="button" class="studio-chip" id="chip-clinic" onclick="loadStudioScenario('clinic')">🌿 Clinical Health</button>
        <button type="button" class="studio-chip" id="chip-stripe" onclick="loadStudioScenario('stripe')">🚀 Stripe SaaS</button>
        <button type="button" class="studio-chip" id="chip-neobrutalism" onclick="loadStudioScenario('neobrutalism')">🎨 Neo-Brutalism</button>
        <button type="button" class="studio-chip" id="chip-minimal_swiss" onclick="loadStudioScenario('minimal_swiss')">📰 Minimal Swiss</button>
        <button type="button" class="studio-chip" id="chip-retro_computing_80s" onclick="loadStudioScenario('retro_computing_80s')">🕹️ CRT Amber</button>
        <button type="button" class="studio-chip" id="chip-modern_glass_2" onclick="loadStudioScenario('modern_glass_2')">💎 Glass 2.0</button>
        <button type="button" class="studio-chip" id="chip-biophilic_wellness" onclick="loadStudioScenario('biophilic_wellness')">🍃 Biophilic</button>
        <button type="button" class="studio-chip" id="chip-financial_terminal" onclick="loadStudioScenario('financial_terminal')">📈 Wall St Terminal</button>
        <button type="button" class="studio-chip" id="chip-cultural_heritage" onclick="loadStudioScenario('cultural_heritage')">📜 Shahnameh Archive</button>
      </div>"""

    chips_block_pattern = r'<!-- Quick Scenario Chips -->\s*<div class="studio-chips".*?</div>'
    new_content, c_count = re.subn(chips_block_pattern, select_html, new_content, flags=re.DOTALL)

    # Add selector CSS if not present
    if ".studio-selector-bar" not in new_content:
        css_addition = """    .studio-selector-bar {
      display: flex;
      align-items: center;
      gap: 12px;
      margin-bottom: 12px;
      flex-wrap: wrap;
    }
    .studio-select {
      background: rgba(15, 23, 42, 0.85);
      border: 1px solid var(--border-subtle);
      color: var(--text-vivid);
      padding: 8px 14px;
      border-radius: 8px;
      font-size: 13px;
      font-family: inherit;
      outline: none;
      cursor: pointer;
      flex: 1;
      min-width: 260px;
    }
    .studio-select option, .studio-select optgroup {
      background: #0f172a;
      color: #f8fafc;
    }
    .studio-chip.active {
      background: var(--accent);
      color: #ffffff;
      border-color: var(--accent);
    }
"""
        new_content = new_content.replace(".studio-chips {", css_addition + "    .studio-chips {")

    file_path.write_text(new_content, encoding="utf-8")
    print(f"✅ Successfully updated {file_path.name} with all 26 styles!")

if __name__ == "__main__":
    main()
