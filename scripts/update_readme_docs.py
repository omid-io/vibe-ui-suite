# -*- coding: utf-8 -*-
"""
Synchronize README.md and README.fa.md to v6.5.0 Sovereign Multi-Agent Swarm architecture.
"""

def update_readme_en():
    with open("README.md", "r", encoding="utf-8") as f:
        text = f.read()

    # 1. Update version mentions
    text = text.replace("Vanilla AI Slop vs. Vibe UI v6.4.5 Masterpiece", "Vanilla AI Slop vs. Vibe UI v6.5.0 Masterpiece")
    text = text.replace("✨ VIBE UI v6.4.5 MASTERPIECE", "✨ VIBE UI v6.5.0 MASTERPIECE")
    text = text.replace("Vibe UI Suite is at `v6.4.5`", "Vibe UI Suite is at `v6.5.0`")

    # 2. Update Swarm Architecture
    old_swarm_head = "## 👑 Sovereign Multi-Agent Swarm Architecture (v6.4.5)"
    if old_swarm_head in text:
        idx_start = text.find(old_swarm_head)
        idx_end = text.find("### Workflow 1: Build from Scratch", idx_start)
        if idx_start != -1 and idx_end != -1:
            new_swarm_section = """## 👑 Sovereign Multi-Agent Swarm Architecture (v6.5.0)

> **Eliminating the "Solo Shortcut":** Single AI models attempting to design, curate, code, and test simultaneously suffer from confirmation bias and hallucinated shortcuts.  
> Vibe UI v6.5.0 introduces the **Sovereign Multi-Agent Swarm** led by `vibe-ui-agent` (`agents/vibe-ui-agent.md`): a 5-phase autonomous pipeline where a non-coding supervisor orchestrates specialized agents with zero human micromanagement and universal multi-harness portability.

```mermaid
flowchart TD
    User(["👤 User: 'Make my web UI look incredible'"]) --> Orchestrator["👑 vibe-ui-agent<br/>(Sovereign Orchestrator • Zero Code Writing)"]
    
    subgraph SwarmPipeline ["The 5-Phase Autonomous Swarm (agents/)"]
        Orchestrator --> P1["💡 Phase 1: vibe-concept-architect<br/>Expands 1-line lazy prompts into psychographics & layout archetypes"]
        P1 --> P2["🔍 Phase 2: vibe-trend-hunter<br/>Mines GitHub Stars (>10k shadcn/aceternity) & Uiverse Likes"]
        P2 --> P3["🎨 Phase 3: vibe-art-director<br/>Synthesizes OKLCH color tokens, typography & Design Blueprint"]
        P3 --> P4["🛠️ Phase 4: vibe-master-builder<br/>Single-author HTML / React 19 TSX synthesis with spring physics"]
        P4 --> P5["📸 Isolated Headless Chromium<br/>Captures Desktop (1440px) & Mobile (390px) screenshots"]
        P5 --> P6["👁️ Phase 5: vibe-visual-auditor & 🛡️ vibe-tech-auditor<br/>Adversarial Inspection: WCAG AA, 0px overflow, visual harmony"]
    end
    
    P6 -- "Defects Detected (Max 3 Loops)" --> PunchList["Atomic 3-Item Punch List"]
    PunchList --> P4
    P6 -- "PASS" --> Delivery(["✨ Verified Production Artifact + Dual-Viewport Screenshots"])
```

### ⚡ One-Liner Swarm Quickstart
Run the complete swarm from your terminal, Cursor, Claude Code, or Antigravity:

```bash
# Direct execution via npx (Zero Setup)
npx vibe-ui-suite swarm "Modern Dark Luxury Real Estate Showcase"

# Or via Python CLI
python vibe_cli.py swarm "High-velocity AI developer platform" -o landing.html
```

### 🏛️ The Specialized Swarm Roles (`agents/`)
Every agent is defined as an independent, portable specification in `agents/` ready to drop into any AI IDE:
- **`vibe-ui-agent`**: Sovereign Swarm Orchestrator. Coordinates execution state, enforces phase progression, and strictly obeys the **Zero Direct Code Writing Invariant**.
- **`vibe-concept-architect`** (Phase 1): Solves lazy prompts by determining product domain, audience psychographics, and spatial layout archetypes.
- **`vibe-trend-hunter`** (Phase 2): Discovers top-starred benchmarks (>10k stars like shadcn/aceternity) and 3,800+ offline Galaxy components.
- **`vibe-art-director`** (Phase 3): Compiles the binding `Design Style Blueprint` with calibrated OKLCH palettes and typography scales.
- **`vibe-master-builder`** (Phase 4): The sole code author, producing pristine HTML / React 19 TSX with spring physics and zero seams.
- **`vibe-visual-auditor` & `vibe-tech-auditor`** (Phase 5): Dual adversarial inspectors enforcing WCAG AA contrast (>=4.5:1), 0px mobile overflow, and visual hierarchy.

### 🌐 Universal Multi-Harness Portability
Vibe UI v6.5.0 ships with zero host-path dependencies across all major AI harnesses:
- **Antigravity**: Local project plugin at `.agents/plugins/vibe-ui/` with dynamic runtime `define_subagent` registration.
- **Claude Code**: Native subagent discovery from `.claude/agents/`.
- **Cursor & Windsurf**: Direct workspace orchestration from root `AGENTS.md`.
- **NPM Package**: Distributed with all agent specifications packaged under `agents/`.

---

"""
            text = text[:idx_start] + new_swarm_section + text[idx_end:]

    # 3. Update Visual Chemistries
    old_chem_head = "## 🎨 Five Visual Chemistries"
    if old_chem_head in text:
        idx_chem = text.find(old_chem_head)
        idx_chem_end = text.find("## ⚡ The Lightswind Kinetic Living Standard", idx_chem)
        if idx_chem != -1 and idx_chem_end != -1:
            new_chem_section = """## 🎨 The Eight Canonical Visual Chemistries

Vibe UI defines eight visual systems for consistent design decisions:

1. **Minimalist SaaS**: Monochrome restraint, precision borders, high information density, Geist/Inter functional typography (`oklch(0.12 0.01 260)`).
2. **Luxury Glassmorphism 2.0**: Dark substrates, specular Fresnel highlights, subtle gold accents, up to 8 controlled GPU backdrop blur layers (`oklch(0.08 0.02 270)`).
3. **Neobrutalism**: High-contrast saturated cards, hard 3-4px black offset geometric drop-shadows, zero blur, explicit physical boundaries (`oklch(0.98 0.02 95)`).
4. **Swiss Editorial**: Asymmetric typographic grid, generous negative space, International Typographic Style with serif/sans harmony (`oklch(0.97 0.005 80)`).
5. **Stripe Crisp Light**: Developer-first documentation aesthetic, micro-borders, clean typography, subtle shadows (`oklch(0.99 0.002 250)`).
6. **Apple Cupertino Fluid**: Continuous corner curvature (`squircle`), tactile spring physics, translucent materials, dynamic responsive states.
7. **Cinematic Motion & Depth**: Nocturnal void (`#050508`), ambient looping media from `cinematic_media_shelf.json`, high-contrast text scrims.
8. **Monochrome Graphite & Laser Mint**: Deep obsidian/graphite (`#09090b`), laser mint (`#00f5a0`) / cyan (`#22d3ee`) telemetry, geometric sans paired with editorial italic serifs.

---

"""
            text = text[:idx_chem] + new_chem_section + text[idx_chem_end:]

    with open("README.md", "w", encoding="utf-8", newline="") as f:
        f.write(text)
    print("README.md updated.")


def update_readme_fa():
    with open("README.fa.md", "r", encoding="utf-8") as f:
        text = f.read()

    # 1. Update version mentions
    text = text.replace("Vibe UI v6.4.5 شاهکار", "Vibe UI v6.5.0 شاهکار")
    text = text.replace("✨ خروجی شاهکار Vibe UI v6.4.5", "✨ خروجی شاهکار Vibe UI v6.5.0")
    text = text.replace("نسخه `v6.4.1`", "نسخه `v6.5.0`")
    text = text.replace("(نسخه 6.4.1)", "(نسخه 6.5.0)")
    text = text.replace("نسخه 6.4.1 این پروژه", "نسخه 6.5.0 این پروژه")

    # 2. Update agent architecture to Swarm
    old_agent_head = "## 👑 ایجنت ارشد معماری فرانت اند: `vibe-ui-agent`"
    if old_agent_head in text:
        idx_start = text.find(old_agent_head)
        idx_end = text.find("### جریان اول: ساخت از صفر", idx_start)
        if idx_start != -1 and idx_end != -1:
            new_fa_swarm = """## 👑 معماری خودمختار سوارم چند ایجنتی (v6.5.0)

> **حذف میانبر تک‌مدلی (Solo Shortcut):** وقتی یک مدل هوش مصنوعی به تنهایی تلاش می‌کند همزمان ایده‌پردازی کند، بنچ‌مارک ببیند، کد بنویسد و تست کند، گرفتار سوگیری تأیید و کدهای بی‌کیفیت و کلیشه‌ای می‌شود.  
> نسخه **v6.5.0** معماری **سوارم چند ایجنتی یکپارچه** به رهبری `vibe-ui-agent` ([AGENT.md](vibe-ui-agent/AGENT.md)) را معرفی می‌کند: خط تولید ۵ فازی کاملاً مستقل که در آن ارکستراتور کل بدون نوشتن مستقیم کد، وظایف را بین ۵ ایجنت متخصص توزیع و تضمین کیفیت خصمانه را مدیریت می‌کند.

```mermaid
flowchart TD
    User(["👤 کاربر: 'یک رابط کاربری خیره‌کننده بساز'"]) --> Orchestrator["👑 vibe-ui-agent<br/>(ارکستراتور سوارم • عدم نوشتن مستقیم کد)"]
    
    subgraph SwarmPipeline ["پایپ‌لاین ۵ فازی سوارم خودمختار (agents/)"]
        Orchestrator --> P1["💡 فاز ۱: vibe-concept-architect<br/>بسط پرامپت‌های کوتاه به پرسونای کاربر و آرکی‌تایپ چیدمان"]
        P1 --> P2["🔍 فاز ۲: vibe-trend-hunter<br/>استخراج مخازن برتر گیت‌هاب (>10k ستاره) و لایک‌های Uiverse"]
        P2 --> P3["🎨 فاز ۳: vibe-art-director<br/>تدوین توکن‌های OKLCH، مقیاس تایپوگرافی و Design Blueprint"]
        P3 --> P4["🛠️ فاز ۴: vibe-master-builder<br/>تک‌نویسنده کد تمیز HTML / React 19 TSX با فیزیک فنر"]
        P4 --> P5["📸 کرومیوم هدلس مجزا<br/>ثبت اسکرین‌شات دسکتاپ (۱۴۴۰px) و موبایل (۳۹۰px)"]
        P5 --> P6["👁️ فاز ۵: vibe-visual-auditor و 🛡️ vibe-tech-auditor<br/>بازرسی خصمانه: کنتراست ریاضی WCAG AA، عدم سرریز و تعادل بصری"]
    end
    
    P6 -- "نقص فنی یا بصری (حداکثر ۳ چرخه)" --> PunchList["لیست ۳ موردی اصلاحات اتمیک"]
    PunchList --> P4
    P6 -- "تأیید نهایی (PASS)" --> Delivery(["✨ تحویل کد آماده پروداکشن + اسکرین‌شات ویوپورت‌های دوگانه"])
```

### ⚡ اجرای تک‌خطی سوارم (Swarm Quickstart)
اجرای بی‌درنگ کل سوارم از طریق ترمینال، Cursor، Claude Code یا Antigravity:

```bash
# اجرای مستقیم با npx بدون نیاز به نصب
npx vibe-ui-suite swarm "Modern Dark Luxury Real Estate Showcase"

# یا از طریق پایتون CLI
python vibe_cli.py swarm "High-velocity AI developer platform" -o landing.html
```

### 🏛️ نقش‌های تخصصی درون سوارم (`agents/`)
تمام ایجنت‌ها به عنوان مشخصات مستقل و پرتابل در پوشه `agents/` تعریف شده‌اند:
- **`vibe-ui-agent`**: ارکستراتور کل سوارم. وظیفه هدایت و پیشبرد فازها را بر عهده دارد و طبق قانون قطعی **Zero Direct Code Writing** هرگز مستقیماً در چت کد نمی‌نویسد.
- **`vibe-concept-architect`** (فاز ۱): حلال پرامپت‌های تنبل با تشخیص دقیق دامنه محصول، روانشناسی مخاطب و کهن‌الگوی چیدمان.
- **`vibe-trend-hunter`** (فاز ۲): کاوشگر ترندهای مطرح گیت‌هاب (بیش از ۱۰ هزار ستاره) و ۳,۸۰۰ المان تعاملی گالکسی به همراه کش آفلاین.
- **`vibe-art-director`** (فاز ۳): تدوینگر سند الزام‌آور `Design Style Blueprint` بر پایه پالت‌های مدرن OKLCH و سلسله‌مراتب فونت.
- **`vibe-master-builder`** (فاز ۴): تنها نویسنده کد، مجری کامپوننت‌های بدون درز HTML / React 19 TSX با فیزیک فنر.
- **`vibe-visual-auditor` و `vibe-tech-auditor`** (فاز ۵): بازرسان سخت‌گیر کیفیت با بررسی کنتراست ریاضی، سرریز ۰ پیکسل موبایل و هماهنگی فضایی.

### 🌐 قابلیت حمل همه‌جانبه (Multi-Harness Portability)
نسخه v6.5.0 برای تمامی محیط‌های اصلی هوش مصنوعی با قابلیت شناسایی بومی بازطراحی شده است:
- **Antigravity**: به عنوان پلاگین محلی پروژه در `.agents/plugins/vibe-ui/` با رجیستری داینامیک `define_subagent`.
- **Claude Code**: شناسایی بومی ساب‌ایجنت‌ها از مسیر `.claude/agents/`.
- **Cursor و Windsurf**: راهبری مستقیم محیط توسعه از طریق ریشه `AGENTS.md`.
- **پکیج NPM**: عرضه همگانی همراه با تمام ایجنت‌ها در بسته دانلودی `agents/`.

---

"""
            text = text[:idx_start] + new_fa_swarm + text[idx_end:]

    # 3. Update Visual Chemistries
    old_fa_chem_head = "## 🎨 ۵ استایل بصری و شیمی دیزاین"
    if old_fa_chem_head in text:
        idx_chem = text.find(old_fa_chem_head)
        idx_chem_end = text.find("## ⚡ استانداردهای حرکتی کینتیک وایب یو آی", idx_chem)
        if idx_chem != -1 and idx_chem_end != -1:
            new_fa_chem = """## 🎨 هشت کهن‌الگوی بصری رسمی (The Eight Visual Chemistries)

سیستم طراحی Vibe UI بر پایه ۸ سبک بصری استاندارد و تثبیت‌شده عمل می‌کند:

1. **مینیمال نرم‌افزاری (Minimalist SaaS):** انضباط مونوکروم، خطوط مرزی دقیق، تراکم بالای اطلاعات و تایپوگرافی خوانا (`oklch(0.12 0.01 260)`).
2. **شیشه‌ای لوکس (Luxury Glassmorphism 2.0):** لایه‌های بلور مات چندگانه، رفلکس‌های براق فرنل، خطوط طلایی ظریف و تاریکی مخملی (`oklch(0.08 0.02 270)`).
3. **نئوبروتالیسم (Neobrutalism):** کارت‌های اشباع با کنتراست بالا، سایه‌های سخت ۳-۴ پیکسلی مشکی بدون بلور و مرزبندی‌های فیزیکی مشخص.
4. **تحریریه سوئیسی (Swiss Editorial):** شبکه نامتقارن تایپوگرافی، فضای منفی فراخ، هماهنگی فونت‌های سریف/سنس برگرفته از سبک بین‌المللی سوئیس.
5. **روشن و شفاف استرایپ (Stripe Crisp Light):** استایل توسعه‌دهنده‌محور با پس‌زمینه‌های عاجی درخشان، گرادیان‌های لطیف و سایه‌های کنترل‌شده.
6. **روان اپل کوپرتینو (Apple Cupertino Fluid):** گوشه‌های کاملاً منحنی اسکویرکل (Squircle)، فیزیک نرم فنر و متریال‌های نیمه‌شفاف.
7. **عمق و حرکت سینمایی (Cinematic Motion & Depth):** پس‌زمینه شبانه عمیق (`#050508`)، ویدیوهای امبینت سبک و کنتراست بالای لایه‌های متنی.
8. **گرافیت مونوکروم و نعنایی لیزری (Monochrome Laser Mint):** بوم گرافیتی بسیار تاریک (`#09090b`)، رنگ‌های تلمتری نعنایی (`#00f5a0`) و سایان، ترکیب سنس هندسی و سریف ایتالیک.

---

"""
            text = text[:idx_chem] + new_fa_chem + text[idx_chem_end:]

    with open("README.fa.md", "w", encoding="utf-8", newline="") as f:
        f.write(text)
    print("README.fa.md updated.")

if __name__ == "__main__":
    update_readme_en()
    update_readme_fa()
