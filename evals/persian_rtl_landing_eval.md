# 🧪 Eval 02: Persian Semantic RTL Landing Page

**Test ID:** `EVAL-PERSIAN-RTL-02`  
**Domain:** `HIGH_TICKET_SERVICE`  
**Archetype:** Luxury Obsidian / Clinical Minimalist  

---

## 📝 Input Prompt
```text
vibe-ui-agent یک لندینگ پیج فارسی برای کلینیک زیبایی و کاشت مو با بنتو گرید ۳ ستونه و اسلایدر قبل و بعد طراحی کن.
```

---

## ✅ Expected Properties (Pass Criteria)
1. **Font Stack & Language:**
   - HTML document has `lang="fa" dir="rtl"`.
   - Font family specifies `Vazirmatn, sans-serif` as primary webfont.
2. **Semantic RTL Architecture:**
   - Macro layout invariant: Bento grid columns remain physically positioned without reversing the entire screen structure.
   - Text alignment: Headings and descriptions use `text-right` or `text-center`.
   - Directional affordance mirroring: Navigation chevrons (back/forward) mirror semantically to follow Persian reading order.
3. **BiDi Resilience:**
   - English brand names or tech metrics inside Persian text are wrapped in `<bdi>` or styled with `unicode-bidi: plaintext` so closing parentheses and punctuation don't jump to the wrong side.
   - Numbers and phone numbers stay in LTR formatting (`dir="ltr"`).
4. **Copywriting Ethics:**
   - Adheres to Anti-Dark-Pattern policy: no fake countdown timers or fabricated user testimonials.

---

## ❌ Forbidden Patterns (Fail Triggers)
- ❌ Flipping the entire macro layout (e.g. putting the main visual on the left just because it's RTL).
- ❌ Unisolated English terms that flip Persian question marks or periods (`؟` or `.`).
- ❌ Code blocks or technical metrics displayed in RTL.
- ❌ Using system Tahoma font instead of modern Vazirmatn.
