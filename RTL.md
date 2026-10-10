# 🌐 Vibe UI Suite — RTL & Bilingual Specification (RTL.md)

> **Document Type:** Modular On-Demand Protocol  
> **Status:** Active & Authoritative Single Source of Truth for RTL  
> **Applies To:** Projects with explicit Persian / RTL requirements, or bilingual UI with RTL toggle.

---

## 🏛️ 1. Activation Trigger Matrix (On-Demand Activation)

RTL is **NOT** a base global intrusive constraint that applies to all projects. It is an **on-demand specialized capability**:

1. **English Prompt -> English Site:**
   - When a user prompt or requirement is in English (e.g., *"Design a modern SaaS pricing table"*), the resulting interface is **100% English LTR**.
   - Standard English typography (Inter, Geist, Satoshi, Cabinet Grotesk) is used.
   - Zero RTL overhead, no forced Persian fonts, no unnecessary `<bdi>` tags on pure English content.

2. **Persian / RTL Prompt -> Persian / RTL Site:**
   - When the user prompt is in Persian (e.g., *"یک صفحه فرود برای کلینیک زیبایی بساز"*), the interface is built in Persian following this document's non-mirrored rules.

3. **Explicit Directive Precedence:**
   - If the user explicitly requests a specific language or a bilingual UI (e.g., *"Make it bilingual in English and Persian"* or *"Build an English site with Persian localization toggle"*), follow the explicit instruction.

---

## 📐 2. The Non-Mirrored Layout Law (Fixed-Structure Semantic RTL)

**Absolute Prohibition of Layout Inversion / Mirroring:**
- Switching to Persian / RTL **MUST NEVER** mirror or flip the physical UI structure.
- **Window Chrome:** macOS traffic lights (red, yellow, green dots) remain fixed on the top-left.
- **Header & Navigation:** The brand logo remains on the left; navigation links and actions remain in their logical positions.
- **Bento Grids & Layout Columns:** 1-2-3 column grids, asymmetrical bento cards, and dashboard panels maintain their exact physical coordinate ordering (left remains left, right remains right).
- **Interactive Controls:** Faders, sliders, knobs, step indicators, and buttons do not reverse their spatial mechanics.
- **Root Document Anchor:** The root document container remains `dir="ltr"`.
- **Scoped Directionality:** Only Persian text blocks (headings, paragraphs, labels) receive `dir="rtl"` (or Persian text alignment). English text and code blocks strictly remain `dir="ltr"`.

---

## 🔤 3. Font Independence & Scoped Persian Typography

**English Text Must Never Be Overwritten by Vazirmatn:**
- English words, phrases, numbers, and Latin glyphs **MUST** retain the default English font (Inter, Geist, Plus Jakarta Sans, SF Pro, sans-serif).
- Only Persian glyphs and Persian text blocks render in **Vazirmatn**.

### Technical Implementation Methods:

#### Method A: Font Fallback Ordering (Preferred for Unified CSS)
By declaring the English font *first* in the CSS `font-family` stack:
```css
:root {
  --font-sans: 'Inter', 'Geist', 'Vazirmatn', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  --font-mono: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace;
}
```
*Why this works:* Latin fonts (like Inter or Geist) do not contain Persian/Arabic glyphs. The browser uses Inter for all English letters and numbers, and automatically falls back to Vazirmatn exclusively for Persian glyphs. English typography is preserved with 100% fidelity.

#### Method B: Scoped Language Selectors
```css
/* Persian typography scoped exclusively to Persian elements */
[lang="fa"], .font-fa, .persian-text {
  font-family: 'Vazirmatn', 'Inter', sans-serif;
  direction: rtl;
}

/* English / Monospace elements strictly isolated */
[lang="en"], .ltr-code, .font-mono, pre, code {
  font-family: 'JetBrains Mono', 'Inter', monospace;
  direction: ltr !important;
  text-align: left !important;
}
```

#### Method C: Unicode-Range Precision
```css
@font-face {
  font-family: 'VazirmatnSubset';
  src: url('/fonts/Vazirmatn.woff2') format('woff2');
  unicode-range: U+0600-06FF, U+FB50-FDFF, U+FE70-FEFF;
}
```

---

## 🛡️ 4. BiDi Punctuation & Token Isolation (`<bdi>`)

When English terms, metrics, numbers, or technical acronyms appear inside Persian sentences:
- The bidirectional (BiDi) algorithm can pull trailing punctuation (like `.`, `،`, `:`, `%`) to the wrong side.
- Every mixed English token, acronym, or metric inside Persian text **MUST** be wrapped in `<bdi>`:
```html
<!-- Correct -->
<p>پشتیبانی کامل از معماری <bdi>Next.js 15</bdi> و استاندارد <bdi>WCAG AAA</bdi> در موتور طراحی.</p>
<div>قیمت: <bdi>$49.99</bdi> ماهیانه</div>

<!-- Incorrect (causes punctuation jumps) -->
<p>پشتیبانی کامل از معماری Next.js 15 و استاندارد WCAG AAA در موتور طراحی.</p>
```

---

## 💻 5. Strict LTR for Technical & Telemetry Blocks

The following elements **MUST ALWAYS** have `direction: ltr !important` and `text-align: left !important`, regardless of page language:
1. Terminal outputs, bash / CLI commands (`vibe_cli.py`, `npm run dev`, `kubectl`).
2. Code blocks (`pre`, `code`, syntax-highlighted containers).
3. System telemetry readouts, JSON data views, and URL strings.
4. Latency benchmarks and math formulas (`O(1)`, `<1ms`, `ζ = 1.0`).

---

## 🚫 6. Absolute Zero ZWNJ Rule (نیم فاصله مطلقا ممنوع)

In all Persian text (UI copy, comments, documentation, and chat output):
- The zero-width non-joiner (ZWNJ / `\u200c` / نیم فاصله) is **strictly forbidden**.
- Standard ASCII space (`\u0020`) must be used exclusively.
- Example: Write `می شود` (never `می شود`), `طراحی شده` (never `طراحی شده`).

---

## 📋 7. Summary Checklist for Code Reviews

| Criterion | Rule | Status |
|:---|:---|:---:|
| **Activation** | Only active when prompt is Persian or bilingual requested | Mandatory |
| **Structure** | Macro layout, traffic lights, and bento grids NOT mirrored | Mandatory |
| **English Typography** | English words keep Inter / Geist (never forced to Vazirmatn) | Mandatory |
| **Persian Typography** | Persian text renders in Vazirmatn via font fallback or scoped class | Mandatory |
| **Token Isolation** | Mixed Latin tokens inside Persian wrapped in `<bdi>` | Mandatory |
| **Monospace / Code** | Code blocks & terminals strictly locked in LTR | Mandatory |
| **ZWNJ** | 0 ZWNJ characters (standard space only) | Mandatory |
