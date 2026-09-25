# 🚀 Vibe UI Suite — Release & Publishing Runbook

راهنمای جامع و استاندارد انتشار و به روزرسانی نسخه های جدید اکوسیستم Vibe UI در رجیستری های جهانی.

---

## 🤖 ۱. فرآیند انتشار کاملاً خودکار (NPM & Open-VSX)

با ایجاد هر Release جدید در گیت هاب (یا اجرای دستی اکشن):
پایپ لاین `.github/workflows/publish.yml` به صورت خودکار موارد زیر را انجام می دهد:
1. **پکیج NPM (`@omid-io/tokens`):** کامپایل سورس های TypeScript، بیلد باندل های ESM و CJS، و انتشار خودکار در NPM با سکرت `NPM_TOKEN`.
2. **رجیستری Open-VSX (`omid-io.vibe-ui-vscode`):** ساخت افزونه، تولید باینری VSIX با آیکون رسمی، و انتشار خودکار با سکرت `OPENVSX_TOKEN`.
3. **فایل باینری در گیت هاب:** الصاق فایل `vibe-ui-vscode-X.Y.Z.vsix` به عنوان Asset رسمی در ریلیز گیت هاب.

---

## 🏢 ۲. فرآیند به روزرسانی در مارکت پلیس مایکروسافت (VS Code Marketplace)

به دلیل الزام مایکروسافت به اتصال کارت اعتباری برای صدور توکن خودکار در Azure DevOps، به روزرسانی در مارکت پلیس مایکروسافت از طریق پرتال رسمی وب انجام می شود (زمان اجرا: ۱۰ ثانیه):

1. به آدرس پرتال مدیریت ناشر بروید:  
   🔗 `https://marketplace.visualstudio.com/manage/publishers/omid-io`
2. روی سه نقطه (`...`) جلوی ردیف افزونه کلیک کرده و گزینه **Update** را انتخاب کنید.
3. فایل جدید باینری تولیدشده را که در مسیر زیر قرار دارد:
   ```text
   packages/vibe-ui-vscode/vibe-ui-vscode-X.Y.Z.vsix
   ```
   بکشید و در کادر آپلود رها کنید (یا از بخش Releases گیت هاب دانلود کنید).
4. دکمه **Upload** را بزنید. افزونه در کمتر از ۳ دقیقه در سراسر جهان به روزرسانی می شود.

---

## 🔒 ۳. محل نگهداری توکن ها و سکرت ها

* سکرت های مخزن گیت هاب:
  * `NPM_TOKEN`: توکن با دسترسی Read/Write و Bypass 2FA
  * `OPENVSX_TOKEN`: توکن دسترسی ناشر `omid-io` در Open-VSX
* نسخه پشتیبان محلی امن:
  * `C:\Users\Legion\.secrets\npm.env`
  * `C:\Users\Legion\.secrets\openvsx.env`
  * `C:\Users\Legion\.secrets\github.env`
