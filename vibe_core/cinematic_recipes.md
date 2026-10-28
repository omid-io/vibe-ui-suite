# Cinematic Motion & Depth Recipes (Vibe UI Core)

> **Architectural Standard:** Production-grade motion, WebGL, video canvas, and kinetic typography recipes.
> **Language Policy:** Universal & language-agnostic core. When RTL is active, respect logical layout properties (`margin-inline`, `padding-inline`), mirror directional transforms (`translateX` inversion), and apply Vazirmatn typography without altering 3D coordinates or video aspect ratios.
> **Zero-Slop Rule:** All recipes are clean, zero-upsell, GPU-composited (`will-change: transform`, `transform: translate3d(0,0,0)`), and respect `prefers-reduced-motion`.

---


## Video & Cinematic Media Recipes

# Video & media

Background footage, loops, scrubbing and the overlays that keep text legible on top of it.

**Conventions.** Every snippet runs in a single `index.html` with no build step. Code assumes `*,*::before,*::after{box-sizing:border-box}`, a dark page, and these shared tokens (paste once):
```css
:root{
  --ease-out-expo:cubic-bezier(.16,1,.3,1);   /* premium settle: entrances, panels */
  --ease-out-quint:cubic-bezier(.22,1,.36,1); /* carousels, fills, menus */
  --ease-material:cubic-bezier(.4,0,.2,1);    /* UI state changes */
}
.sr-only{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}
```
`VIDEO_URL.mp4`, `poster.jpg` etc. are placeholders. Encode backgrounds as H.264 MP4 with `-movflags +faststart` (add WebM as a second `<source>` if you have it). Keep background clips 6–12 s and ≤ 5–8 MB.

---

## 1. Cinematic background video layer (autoplay, HLS, off-screen pause, settle-in)

**What / when:** The default premium hero foundation: a muted looping clip fills the viewport and all UI floats over it. The video provides all the depth, so no decorative blobs are needed. Use it for any hero where footage carries the mood.

**Premium parameters**
- Full-bleed absolute video, `object-fit:cover`. The section background is `#000` (or the page bg, matching the clip's edge colour) so nothing flashes before the first frame.
- Always `muted autoplay loop playsinline` (all four are required for iOS autoplay), and set `video.muted = true` as a property too.
- `object-position: 70% center` (or wherever the subject is) so portrait crops keep the subject.
- Entrance: fade in from `opacity 0, scale(1.05)` to `1, scale(1)` over **1.8 s** `--ease-out-expo`. Or a **delayed reveal**: keep a still/blank hero during the type intro and fade the video in at ~**2.8 s**.
- Pause when off-screen (IntersectionObserver): a big battery and CPU win on long pages with several videos.
- HLS (`.m3u8`): Safari plays it natively; every other browser needs hls.js with `capLevelToPlayerSize: true` so phones never stream 4K.
- Text protection: pick one scrim from technique 4, or none when the footage has calm negative space behind the copy.

**Implementation**
```html
<section class="vhero">
  <video class="vhero__media vhero__media--settle" data-src="VIDEO_URL.mp4" poster="poster.jpg"
         autoplay muted loop playsinline preload="auto" aria-hidden="true"></video>
  <div class="vhero__content">…nav, headline, CTAs…</div>
</section>
<!-- Only needed when a source is .m3u8 -->
<script src="https://cdn.jsdelivr.net/npm/hls.js@1.5.20/dist/hls.min.js"></script>
```
```css
.vhero{position:relative;min-height:100vh;min-height:100svh;overflow:hidden;background:#000;isolation:isolate;color:#fff}
.vhero__media{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:-2;pointer-events:none}
.vhero__media--settle{opacity:0;transform:scale(1.05);transition:opacity 1.8s var(--ease-out-expo),transform 1.8s var(--ease-out-expo)}
.vhero__media--settle.is-ready{opacity:1;transform:none}
.vhero__content{position:relative;min-height:inherit;display:flex;flex-direction:column}
@media (prefers-reduced-motion:reduce){.vhero__media--settle{opacity:1;transform:none;transition:none}}
```
```js
function mountVideo(video, src, { revealDelay = 0 } = {}) {
  video.muted = true;               // some browsers ignore the attribute for autoplay
  video.playsInline = true;
  const isHls = /\.m3u8($|\?)/i.test(src);
  if (isHls && !video.canPlayType('application/vnd.apple.mpegurl') && window.Hls && Hls.isSupported()) {
    const hls = new Hls({ capLevelToPlayerSize: true });
    hls.loadSource(src); hls.attachMedia(video);
  } else {
    video.src = src;                // MP4 everywhere, or native HLS in Safari/iOS
  }
  const reveal = () => setTimeout(() => video.classList.add('is-ready'), revealDelay);
  video.readyState >= 2 ? reveal() : video.addEventListener('loadeddata', reveal, { once: true });
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) {
    video.removeAttribute('autoplay'); video.pause();   // poster / first frame stays as a still
    return;
  }
  video.play().catch(() => {});     // autoplay can be refused (low-power mode): the poster remains
  new IntersectionObserver(([e]) => (e.isIntersecting ? video.play().catch(() => {}) : video.pause()))
    .observe(video);
}
document.querySelectorAll('video[data-src]').forEach((v) => mountVideo(v, v.dataset.src));
// Delayed reveal, letting the headline intro own the first ~3 s:
// mountVideo(el, el.dataset.src, { revealDelay: 2800 });
```

**React variant** (hls.js needs explicit cleanup):
```tsx
useEffect(() => {
  const v = ref.current!; let hls: Hls | undefined;
  if (v.canPlayType('application/vnd.apple.mpegurl')) v.src = SRC;
  else if (Hls.isSupported()) { hls = new Hls({ capLevelToPlayerSize: true }); hls.loadSource(SRC); hls.attachMedia(v); }
  return () => hls?.destroy();
}, []);
```

**Mobile / a11y:** use `100svh`/`100dvh` with a `100vh` fallback so browser chrome doesn't crop. Serve a lighter ≤720p encode to phones by picking `src` with `matchMedia('(max-width: 768px)')`. Reduced motion shows the poster or first frame as a still.

---

## 2. Seamless video loop with rAF opacity fades (manual loop, optional playlist)

**What / when:** A background video that fades in from black on load, fades out just before its last frame, and restarts after a short black beat. This hides the hard cut of a native `loop` (and any mismatch between first and last frame), so every loop reads as a cinematic "cut to black". The same mechanism cycles a playlist of clips.

**Premium parameters**
- Fade-in 500 ms; fade-out 500–550 ms, triggered when `duration − currentTime ≤ 0.55 s`.
- 100 ms of pure black between plays (`ended` → opacity 0 → wait 100 ms → `currentTime = 0` → play → fade in).
- Fades run on `requestAnimationFrame`, never a CSS `transition` on the video. Each new fade cancels the previous rAF and starts from the current opacity, so fades never snap or fight.
- A guard flag stops the fade-out from re-triggering on every `timeupdate`.
- Native `loop` is OFF. The video is `muted playsinline autoplay preload="auto"`. The section behind is pure `#000`, so the dip reads as intentional.

**Implementation**
```html
<section class="hero">
  <video class="hero-video" data-fade-loop muted playsinline autoplay preload="auto" src="VIDEO_URL.mp4" aria-hidden="true"></video>
  <div class="hero-content">…</div>
</section>
```
```css
.hero{position:relative;min-height:100vh;min-height:100dvh;overflow:hidden;background:#000}
.hero-video{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;
  opacity:0;            /* JS owns opacity: no CSS transition here */
  pointer-events:none;z-index:0}
.hero-content{position:relative;z-index:10}
```
```js
/** Manual loop with rAF fades. Returns a cleanup function. */
function fadeLoopVideo(video, { fadeMs = 500, fadeOutLead = 0.55, gapMs = 100, playlist = null } = {}) {
  let raf = 0, timer = 0, fadingOut = false, idx = 0;
  const fadeTo = (target, ms = fadeMs) => {
    cancelAnimationFrame(raf);
    const from = parseFloat(video.style.opacity) || 0;   // resume from wherever we are
    const t0 = performance.now();
    const tick = (now) => {
      const p = Math.min((now - t0) / ms, 1);
      video.style.opacity = String(from + (target - from) * p);
      if (p < 1) raf = requestAnimationFrame(tick);
    };
    raf = requestAnimationFrame(tick);
  };
  const startPlayback = () => { fadingOut = false; video.play().catch(() => {}); fadeTo(1); };
  const onTimeUpdate = () => {
    const left = video.duration - video.currentTime;
    if (!fadingOut && left > 0 && left <= fadeOutLead) { fadingOut = true; fadeTo(0); }
  };
  const onEnded = () => {
    cancelAnimationFrame(raf);
    video.style.opacity = '0';
    timer = setTimeout(() => {
      if (playlist && playlist.length > 1) {
        idx = (idx + 1) % playlist.length;
        video.src = playlist[idx];             // 'loadeddata' fires again -> startPlayback
      } else { video.currentTime = 0; startPlayback(); }
    }, gapMs);
  };
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) {   // still frame instead of motion
    video.removeAttribute('autoplay'); video.pause(); video.style.opacity = '1';
    return () => {};
  }
  video.loop = false; video.muted = true; video.playsInline = true;
  video.style.opacity = '0';
  if (playlist && playlist.length) video.src = playlist[0];
  video.addEventListener('loadeddata', startPlayback);
  video.addEventListener('timeupdate', onTimeUpdate);
  video.addEventListener('ended', onEnded);
  if (video.readyState >= 2) startPlayback();   // already loaded from cache
  return () => {
    cancelAnimationFrame(raf); clearTimeout(timer);
    video.removeEventListener('loadeddata', startPlayback);
    video.removeEventListener('timeupdate', onTimeUpdate);
    video.removeEventListener('ended', onEnded);
  };
}
document.querySelectorAll('video[data-fade-loop]').forEach((v) => fadeLoopVideo(v));
// Playlist: fadeLoopVideo(el, { playlist: ['a.mp4', 'b.mp4', 'c.mp4'] });
```
For `.m3u8` sources, attach them with the HLS branch of technique 1 instead of setting `video.src`.

**React variant** (only the lifecycle differs):
```tsx
function FadingVideo({ src, className }: { src: string | string[]; className?: string }) {
  const ref = useRef<HTMLVideoElement>(null);
  useEffect(() => fadeLoopVideo(ref.current!, { playlist: Array.isArray(src) ? src : null }), [src]);
  // put opacity:0 in the CSS class, not style={{}}, so a re-render never resets it
  return <video ref={ref} className={className} src={Array.isArray(src) ? undefined : src} muted playsInline autoPlay preload="auto" />;
}
```

**Mobile / perf:** iOS needs `muted` + `playsinline`. With several of these on one page, pause off-screen ones with an IntersectionObserver.

---

## 3. Background-video framing & art direction

**What / when:** Small geometry tricks that put the clip's subject exactly where the layout needs it, without re-editing the video. Use them whenever the focal point would collide with the copy, sit too low or high, or crop badly on portrait screens.

**Premium parameters / variants**
- **Oversize + top anchor:** `width:120%; height:120%`, centred horizontally, `top:0`, `object-position:top`. Keeps the top of the frame (sky, horizon, a planet) in view, trims edges and bottom, and reads slightly zoomed-in.
- **Vertical offset:** `translateY(15–20%)` on an `inset:0` cover video pushes the subject below the headline. Only works when the exposed band blends into the section bg (black clip edge, or a scrim from technique 4).
- **Lower band:** the video occupies only the area below the headline (from ~300 px / 30vh down). A `bg → transparent → bg` vertical gradient dissolves it into a light page.
- **Focal crop for portrait:** `object-position: 70% center` (or `right bottom` from ≥1024 px) keeps a right-side subject visible when a phone crops the sides.
- **Bleed scale:** `scale(1.05)` hides encoder edge lines and 1 px letterbox slivers.
- **Mobile in-flow:** on phones the video becomes a square block below the copy (`aspect-ratio:1/1`, `16/9` on tablet, absolute background again from ≥1024 px). Avoids text over busy video on small screens.
- **Light pages on mobile:** inset the video to `80% × 80%`, centred; it reads as a floating screen instead of a cropped mess.
- **Reuse trick:** the same clip flipped with `transform: scaleY(-1)` behind the footer or contact band, dimmed 60 %, reads as a new shot.

**Implementation**
```css
/* A. Oversize, top-anchored */
.video--oversize{position:absolute;left:50%;top:0;width:120%;height:120%;transform:translateX(-50%);object-fit:cover;object-position:top center}
/* B. Vertical offset */
.video--shift{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transform:translateY(17%)}
/* C. Lower band dissolving into a light page */
.video-band{position:absolute;left:0;right:0;bottom:0;top:clamp(180px,30vh,300px);z-index:0}
.video-band video{width:100%;height:100%;object-fit:cover}
.video-band::after{content:"";position:absolute;inset:0;pointer-events:none;
  background:linear-gradient(to bottom,var(--bg,#fff) 0%,transparent 50%,var(--bg,#fff) 100%)}
/* D. Focal crop */
.video--focal{object-position:70% center}
@media (min-width:1024px){.video--focal{object-position:right bottom}}
/* E. Bleed */
.video--bleed{transform:scale(1.05)}
/* F. In-flow block on mobile, background on desktop */
.split{display:flex;flex-direction:column;background:#fff}
.split__copy{order:1;position:relative;z-index:10;padding:48px 24px}
.split__media{order:2;position:relative;aspect-ratio:1/1;overflow:hidden}
.split__media video{width:100%;height:100%;object-fit:cover;object-position:right}
@media (min-width:768px){.split__media{aspect-ratio:16/9}}
@media (min-width:1024px){
  .split{display:block;position:relative;min-height:100vh}
  .split__copy{background:transparent;min-height:100vh;display:flex;flex-direction:column;justify-content:center}
  .split__media{position:absolute;inset:0;aspect-ratio:auto;z-index:0}
  .split__media video{object-position:right bottom}
}
/* G. Footer reuse */
.video--flipped{transform:scaleY(-1);filter:brightness(.4)}
```
```html
<section class="split">
  <div class="split__copy">…headline / form…</div>
  <div class="split__media"><video muted playsinline autoplay loop preload="auto" src="VIDEO_URL.mp4"></video></div>
</section>
```

**Mobile:** retest the focal point at 375×812. Usually you change `object-position` per breakpoint rather than the transform.

---

## 4. Edge-blend scrims & text protection over video

**What / when:** Gradient overlays that melt a video into the page colour and keep text legible without a flat dark tint that kills the footage. Eased bottom fade where the hero hands off to the next section; side letterboxing when the video has a capped width on ultra-wide screens; a directional scrim on portrait where text sits over the busiest part of the frame.

**Premium parameters**
- Eased bottom fade that starts late (~79 %) with many stops (a 2-stop gradient bands and looks cheap): 0 @78.8 % → .23 @79.6 → .45 @81.4 → .75 @83.3 → .84 @85.2 → .888 @88 → .905 @91 → .96 @95 → 1 @100.
- Simple menu of scrims (pick one, keep it subtle):
  - bottom fade into the page: `height 12–16rem`, `linear-gradient(to top, var(--bg), transparent)`;
  - top fade under a transparent nav: `height 180px`, `linear-gradient(#010103, transparent)`;
  - full vertical: `rgba(0,0,0,.30) → transparent 45 % → rgba(0,0,0,.60)`;
  - flat dim: `.20` hero, `.45` CTA band, `.60` when a clip is reused behind a footer;
  - light theme: `linear-gradient(to top, #fff 0%, rgba(255,255,255,.8) 50%, transparent 100%)` behind bottom copy.
- Side letterbox: solid page colour beyond the video's edges, feathered over ~70 px.
- Portrait text scrim, left→right `.86 → .66 @42 % → .20 @78 % → .10`; top→bottom `.72 → .34 @24 % → .34 @56 % → .80 @82 % → .97 @94 % → 1`.
- Media cards: `to top`, black 60 % → transparent at 50 %.
- Use the exact page colour (e.g. `#050505`), never a different black, or the seam shows.
- **No scrim at all** is often the strongest choice: the video at 100 %, contrast from glass chrome and from placing copy where the frame is naturally dark. Choose footage with a dark negative-space zone.

**Implementation**
```css
:root{--bg:#050505;--video-half:746px}  /* half the rendered video width, if capped */
.plate{position:absolute;inset:0;overflow:hidden;background:var(--bg)}
.plate video{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.plate::after{content:"";position:absolute;inset:0;pointer-events:none;background:
  linear-gradient(to bottom,
    rgb(5 5 5/0) 78.8%, rgb(5 5 5/.23) 79.6%, rgb(5 5 5/.45) 81.4%, rgb(5 5 5/.75) 83.3%,
    rgb(5 5 5/.84) 85.2%, rgb(5 5 5/.888) 88%, rgb(5 5 5/.905) 91%, rgb(5 5 5/.96) 95%, var(--bg) 100%),
  linear-gradient(to right,
    var(--bg) calc(50% - var(--video-half)), transparent calc(50% - var(--video-half) + 70px),
    transparent calc(50% + var(--video-half) - 70px), var(--bg) calc(50% + var(--video-half)))}
/* Portrait: copy over the frame -> directional legibility scrim */
@media (max-aspect-ratio:11/10){
  .plate video{object-position:43% center}
  .plate::after{background:
    linear-gradient(to right,rgb(5 5 5/.86),rgb(5 5 5/.66) 42%,rgb(5 5 5/.20) 78%,rgb(5 5 5/.10)),
    linear-gradient(to bottom,rgb(5 5 5/.72),rgb(5 5 5/.34) 24%,rgb(5 5 5/.34) 56%,rgb(5 5 5/.80) 82%,rgb(5 5 5/.97) 94%,var(--bg))}
}
/* Simple scrims */
.scrim-vertical{position:absolute;inset:0;pointer-events:none;background:linear-gradient(to bottom,rgba(0,0,0,.3),transparent 45%,rgba(0,0,0,.6))}
.fade-bottom{position:absolute;left:0;right:0;bottom:0;height:16rem;pointer-events:none;background:linear-gradient(to top,var(--bg),transparent)}
.fade-top{position:absolute;left:0;right:0;top:0;height:180px;pointer-events:none;background:linear-gradient(#010103,transparent)}
/* Media card scrim */
.media-card{position:relative;overflow:hidden;border-radius:24px}
.media-card::after{content:"";position:absolute;inset:0;pointer-events:none;background:linear-gradient(to top,rgb(0 0 0/.6),transparent 50%)}
```

---

## 5. Progressive bottom blur (masked backdrop-filter)

**What / when:** Instead of darkening the footage, the bottom of the video goes out of focus and sharpens toward the middle: a camera-like depth-of-field band that protects bottom-aligned titles while keeping colours intact. Use it for bottom-anchored cinematic heroes.

**Premium parameters:** blur **24px**, mask `linear-gradient(to top, #000 0%, transparent 45%)`, no colour overlay. The stepped version stacks 2 / 4 / 8 / 16 px layers with shrinking masks so the blur compounds toward the bottom.

**Implementation**
```html
<div class="bottom-blur" aria-hidden="true"></div>
<!-- or: <div class="pblur" aria-hidden="true"><i></i><i></i><i></i><i></i></div> -->
```
```css
.bottom-blur{position:absolute;inset:0;z-index:1;pointer-events:none;
  -webkit-backdrop-filter:blur(24px);backdrop-filter:blur(24px);
  -webkit-mask-image:linear-gradient(to top,#000 0%,transparent 45%);mask-image:linear-gradient(to top,#000 0%,transparent 45%)}
/* Smoother stepped version */
.pblur{position:absolute;left:0;right:0;bottom:0;height:55%;z-index:1;pointer-events:none}
.pblur>i{position:absolute;inset:0}
.pblur>i:nth-child(1){-webkit-backdrop-filter:blur(2px);backdrop-filter:blur(2px);-webkit-mask-image:linear-gradient(to top,#000,transparent 100%);mask-image:linear-gradient(to top,#000,transparent 100%)}
.pblur>i:nth-child(2){-webkit-backdrop-filter:blur(4px);backdrop-filter:blur(4px);-webkit-mask-image:linear-gradient(to top,#000,transparent 75%);mask-image:linear-gradient(to top,#000,transparent 75%)}
.pblur>i:nth-child(3){-webkit-backdrop-filter:blur(8px);backdrop-filter:blur(8px);-webkit-mask-image:linear-gradient(to top,#000,transparent 50%);mask-image:linear-gradient(to top,#000,transparent 50%)}
.pblur>i:nth-child(4){-webkit-backdrop-filter:blur(16px);backdrop-filter:blur(16px);-webkit-mask-image:linear-gradient(to top,#000,transparent 25%);mask-image:linear-gradient(to top,#000,transparent 25%)}
```

**Mobile:** `backdrop-filter` over full-screen video is GPU-heavy on low-end phones; prefer the single-layer version there.

---

## 6. Cursor-scrubbed video (delta scrub · split dual-video)

**What / when:** A paused clip whose timeline follows horizontal mouse movement: a character turns its head, a product spins on a turntable, an object opens. It feels like a live 3D object without WebGL. Desktop only; touch falls back to autoplay.
- **Delta scrub:** relative horizontal movement moves the playhead forward or back.
- **Split dual-video:** two clips; left of centre scrubs clip A, right of centre scrubs clip B; a dead zone at the centre holds frame 0.

**Premium parameters**
- Sensitivity **0.8**: crossing the full viewport width scrubs 80 % of the clip. `Δt = (Δx / innerWidth) × 0.8 × duration`, clamped to `[0, duration]`. Relative mapping, so the first mouse move never jumps.
- **Seek queue:** never assign `currentTime` while a seek is in flight. Store the target; on `seeked`, seek again only if the target moved. Without this the decoder floods and the image freezes.
- Split: dead zone `max(30px, width × 0.05)` either side of centre; progress = distance beyond the dead-zone edge ÷ remaining half-width; keep showing the last active side inside the dead zone.
- Disabled below 1024 px and on non-hover devices (autoplay loop there; the split version alternates the two clips on `ended`).
- `muted playsinline preload="auto"`, no autoplay on desktop, `object-position: 70% center`.
- Encode for scrubbing with tiny GOPs so seeks land instantly (the difference between silky and steppy):
  `ffmpeg -i in.mp4 -an -c:v libx264 -crf 20 -g 6 -keyint_min 6 -pix_fmt yuv420p -movflags +faststart scrub.mp4` (`-g 1` = all-intra, silkiest).
- For clips under ~15 MB, load the file fully before scrubbing so every seek is local: `fetch(url).then(r => r.blob()).then(b => { video.src = URL.createObjectURL(b); })`.

**Implementation (A: delta scrub)**
```html
<video class="scrub-video" muted playsinline preload="auto" src="TURNTABLE.mp4" aria-hidden="true"></video>
```
```css
.scrub-video{position:fixed;inset:0;width:100%;height:100%;object-fit:cover;object-position:70% center;z-index:0}
```
```js
function mouseScrubVideo(video, { sensitivity = 0.8, query = '(min-width: 1024px) and (hover: hover)' } = {}) {
  const mq = matchMedia(query);
  const reduce = matchMedia('(prefers-reduced-motion: reduce)');
  let prevX = null, target = 0, busy = false;
  video.muted = true; video.playsInline = true;
  const flush = () => {
    if (!mq.matches || reduce.matches) { busy = false; return; }   // ignore seeks caused by normal looping
    if (Math.abs(video.currentTime - target) < 1 / 60) { busy = false; return; }
    busy = true;
    video.currentTime = target;                 // 'seeked' fires when the frame is decoded
  };
  video.addEventListener('seeked', flush);
  addEventListener('mousemove', (e) => {
    if (!mq.matches || reduce.matches || !video.duration) return;
    if (prevX === null) { prevX = e.clientX; return; }
    const dx = e.clientX - prevX; prevX = e.clientX;
    target = Math.max(0, Math.min(video.duration, target + (dx / innerWidth) * sensitivity * video.duration));
    if (!busy) flush();
  }, { passive: true });
  const applyMode = () => {
    if (reduce.matches) { video.pause(); return; }                         // still frame
    if (mq.matches) { video.loop = false; video.pause(); target = video.currentTime; }
    else { video.loop = true; video.play().catch(() => {}); }             // touch / small screens
  };
  mq.addEventListener('change', applyMode);
  reduce.addEventListener('change', applyMode);
  applyMode();
}
mouseScrubVideo(document.querySelector('.scrub-video'));
```

**Implementation (B: split dual-video with dead zone)**
```html
<div class="dual" aria-hidden="true">
  <video class="dual__v" id="vidA" src="a.mp4" muted playsinline preload="auto"></video>
  <video class="dual__v" id="vidB" src="b.mp4" muted playsinline preload="auto"></video>
</div>
```
```css
.dual{position:fixed;inset:0;z-index:0;opacity:0;transition:opacity .3s ease;pointer-events:none;overflow:hidden}
.dual.is-ready{opacity:1}
.dual__v{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
@media (max-width:640px){.dual{top:220px;height:calc(100vh - 220px)}}  /* room for stacked copy */
```
```js
(() => {
  const wrap = document.querySelector('.dual');
  const A = document.getElementById('vidA'), B = document.getElementById('vidB');
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const show = (v) => { A.style.visibility = v === A ? 'visible' : 'hidden'; B.style.visibility = v === B ? 'visible' : 'hidden'; };
  Promise.all([A, B].map((v) => (v.readyState >= 2 ? 0 : new Promise((r) => v.addEventListener('loadeddata', r, { once: true })))))
    .then(() => wrap.classList.add('is-ready'));
  if (matchMedia('(hover: none)').matches) {              // touch: alternate autoplay
    [A, B].forEach((v) => v.addEventListener('ended', () => {
      const next = v === A ? B : A; next.currentTime = 0; show(next); next.play().catch(() => {});
    }));
    show(A); if (!reduce) A.play().catch(() => {});
    return;
  }
  let mouseX = innerWidth / 2, active = B;
  show(active);
  addEventListener('mousemove', (e) => { mouseX = e.clientX; }, { passive: true });
  (function frame() {
    const w = innerWidth, c = w / 2, dz = Math.max(30, w * 0.05);
    let p = -1;
    if (mouseX < c - dz)      { active = A; p = (c - dz - mouseX) / (c - dz); }
    else if (mouseX > c + dz) { active = B; p = (mouseX - c - dz) / (w - c - dz); }
    show(active);
    if (active.duration && !active.seeking) {           // never seek while seeking
      const t = p < 0 ? 0 : Math.min(1, p) * (active.duration - 0.05);
      if (Math.abs(active.currentTime - t) > 0.02) active.currentTime = t;
    }
    requestAnimationFrame(frame);
  })();
})();
```

**Reduced motion:** variant A shows a still frame; B holds frame 0 on touch. The scrub itself is user-driven, so it may stay on for fine pointers.

---

## 7. Scroll-scrubbed video with canvas frame cache

**What / when:** The page scroll *is* the video timeline: a fixed full-bleed clip advances only as the user scrolls, smoothed with a lerp. Use it for abstract or 3D "transformation" footage behind a sparse editorial page (2–3 screens of text over it). Never also autoplay it.

**Premium parameters**
- Layers bottom→top: poster `<img>` → `<video>` (seek fallback) → `<canvas>` (cached frames). Crossfades `opacity 500ms`.
- `progress = scrollY / (scrollHeight − innerHeight)`, clamped; smoothing `smooth += (target − smooth) × 0.12` per rAF.
- Frame cache: `count = clamp(round(duration × 12), 24, 90)` frames, max width **960 px** (640 px on phones). Start extracting only after the visible video has `loadeddata` + **300 ms**, so the first paint isn't starved.
- Fallback before the cache is ready: seek the `<video>` to `smooth × (duration − 0.05)` only when `|Δ| > 0.04 s` and not already seeking. Encode with short GOPs (`-g 5`, or all-intra `-g 1`).
- Canvas DPR `min(devicePixelRatio, 2)`; draw with object-cover math.
- Give the scrub room: an `~80vh` spacer between content screens so the footage visibly transforms.
- Memory: 90 frames × 960×540 RGBA ≈ 190 MB; halve the width on mobile (≈ 47 MB).

**Implementation**
```html
<div class="scrubbg" aria-hidden="true">
  <img class="scrubbg__poster" src="poster.jpg" alt="">
  <video class="scrubbg__video" src="VIDEO_URL.mp4" muted playsinline preload="auto"></video>
  <canvas class="scrubbg__canvas"></canvas>
</div>
<div class="page">
  <section class="screen">…hero copy…</section>
  <div style="height:80vh" aria-hidden="true"></div>   <!-- scrub runway -->
  <section class="screen">…second scene…</section>
</div>
```
```css
.scrubbg{position:fixed;inset:0;z-index:0;pointer-events:none;overflow:hidden;background:#0a0a0a}
.scrubbg>*{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transition:opacity .5s ease}
.scrubbg__video,.scrubbg__canvas{opacity:0}
.scrubbg.has-video .scrubbg__video{opacity:1}
.scrubbg.has-video .scrubbg__poster{opacity:0}
.scrubbg.has-frames .scrubbg__canvas{opacity:1}
.scrubbg.has-frames .scrubbg__video{opacity:0}
.page{position:relative;z-index:1}
.screen{min-height:100vh;min-height:100svh;display:flex;flex-direction:column;justify-content:space-between}
```
```js
(() => {
  const root = document.querySelector('.scrubbg');
  const video = root.querySelector('video');
  const canvas = root.querySelector('canvas');
  const ctx = canvas.getContext('2d');
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const MAX_W = matchMedia('(max-width: 768px)').matches ? 640 : 960;
  let frames = [], target = 0, smooth = 0, lastIndex = -1;

  const resize = () => {
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    canvas.width = Math.round(innerWidth * dpr);
    canvas.height = Math.round(innerHeight * dpr);
    lastIndex = -1;                                     // force a redraw
  };
  const drawCover = (img) => {
    const cw = canvas.width, ch = canvas.height;
    const s = Math.max(cw / img.width, ch / img.height);
    const w = img.width * s, h = img.height * s;
    ctx.drawImage(img, (cw - w) / 2, (ch - h) / 2, w, h);
  };
  const progress = () => {
    const max = document.documentElement.scrollHeight - innerHeight;
    return max > 0 ? Math.min(1, Math.max(0, scrollY / max)) : 0;
  };
  const once = (el, ev) => new Promise((r) => el.addEventListener(ev, r, { once: true }));
  const seekTo = (v, t) => new Promise((r) => {
    const done = () => { clearTimeout(timer); r(); };
    const timer = setTimeout(done, 1000);               // safety net
    v.addEventListener('seeked', done, { once: true });
    v.currentTime = t;
  });
  async function buildFrameCache() {
    const v = document.createElement('video');
    v.muted = true; v.playsInline = true; v.preload = 'auto';
    v.src = video.currentSrc || video.src;
    v.play().then(() => v.pause()).catch(() => {});     // iOS ignores preload until play()
    if (v.readyState < 2) await once(v, 'loadeddata');
    const count = Math.max(24, Math.min(90, Math.round(v.duration * 12)));
    const scale = Math.min(1, MAX_W / v.videoWidth);
    const w = Math.round(v.videoWidth * scale), h = Math.round(v.videoHeight * scale);
    const out = [];
    for (let i = 0; i < count; i++) {
      await seekTo(v, (i / (count - 1)) * (v.duration - 0.05));
      const c = document.createElement('canvas');      // small canvases: no CORS/ImageBitmap quirks
      c.width = w; c.height = h;
      c.getContext('2d').drawImage(v, 0, 0, w, h);
      out.push(c);
    }
    return out;
  }
  function tick() {
    target = progress();
    smooth = reduce ? target : smooth + (target - smooth) * 0.12;
    if (frames.length) {
      const i = Math.round(smooth * (frames.length - 1));
      if (i !== lastIndex) { drawCover(frames[i]); lastIndex = i; }
    } else if (video.readyState >= 1 && video.duration) {
      const t = smooth * (video.duration - 0.05);
      if (!video.seeking && Math.abs(video.currentTime - t) > 0.04) video.currentTime = t;
    }
    requestAnimationFrame(tick);
  }
  resize();
  addEventListener('resize', resize);
  video.play().then(() => video.pause()).catch(() => {}); // prime decoding on iOS
  video.addEventListener('loadeddata', async () => {
    root.classList.add('has-video');
    await new Promise((r) => setTimeout(r, 300));
    try { frames = await buildFrameCache(); lastIndex = -1; root.classList.add('has-frames'); }
    catch (e) { /* keep the seek fallback */ }
  }, { once: true });
  requestAnimationFrame(tick);
})();
```

**Notes:** drawing a cross-origin video into a canvas only "taints" it (you can't read pixels back); drawing still works, so don't set `crossOrigin` unless the host sends CORS headers (otherwise the video fails to load). Reduced motion bypasses smoothing; the scrub is user-driven, so it stays.

---

## 8. Boomerang (ping-pong) video loop

**What / when:** The clip plays forward, then backward, then forward again, with no seam. Use it for any non-looping clip: a camera push-in, a flower opening, smoke rising. It reads like slow breathing.

**Premium parameters**
- **Preferred for production:** pre-render the boomerang as a file and loop it natively:
  `ffmpeg -i in.mp4 -filter_complex "[0:v]split[a][b];[b]reverse[r];[a][r]concat=n=2:v=1:a=0[out]" -map "[out]" -an -c:v libx264 -crf 20 -movflags +faststart boomerang.mp4`
- Runtime capture (when you can't pre-render): play at 30 fps; capture frames at most 960 px wide with `requestVideoFrameCallback` (exact per-frame, rAF fallback), skipping duplicate `currentTime` values. Show the live `<video>` during the first pass, then swap to a `<canvas>` with `object-fit:cover`.
- **Memory:** each 960×540 RGBA frame ≈ 2 MB, so 150 frames ≈ 300 MB. Keep clips 3–5 s, or capture at 640 px.
- Only add `crossorigin="anonymous"` if the video host sends CORS headers.

**Implementation (runtime capture)**
```html
<div class="boomerang">
  <video muted playsinline preload="auto" src="CLIP.mp4"></video>
  <canvas hidden></canvas>
</div>
```
```css
.boomerang{position:absolute;inset:0}
.boomerang video,.boomerang canvas{width:100%;height:100%;object-fit:cover;display:block}
```
```js
function boomerangVideo(root, { maxWidth = 960, fps = 30 } = {}) {
  const video = root.querySelector('video');
  const out = root.querySelector('canvas');
  const octx = out.getContext('2d');
  const frames = [];
  let capturing = true, lastT = -1;
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) return;   // keep the first frame
  const grab = () => {
    if (!capturing || video.readyState < 2 || video.currentTime === lastT || !video.videoWidth) return;
    lastT = video.currentTime;
    const s = Math.min(1, maxWidth / video.videoWidth);
    const c = document.createElement('canvas');
    c.width = Math.round(video.videoWidth * s);
    c.height = Math.round(video.videoHeight * s);
    c.getContext('2d').drawImage(video, 0, 0, c.width, c.height);
    frames.push(c);
  };
  const hasVFC = 'requestVideoFrameCallback' in HTMLVideoElement.prototype;
  const loop = () => { grab(); if (!capturing) return; hasVFC ? video.requestVideoFrameCallback(loop) : requestAnimationFrame(loop); };
  video.addEventListener('ended', () => {
    capturing = false;
    if (!frames.length) return;
    out.width = frames[0].width; out.height = frames[0].height;
    video.hidden = true; out.hidden = false;
    let i = frames.length - 1, dir = -1, last = 0;
    const step = 1000 / fps;
    const render = (now) => {
      if (now - last >= step) {
        last = now;
        octx.drawImage(frames[i], 0, 0);
        i += dir;
        if (i >= frames.length - 1) { i = frames.length - 1; dir = -1; }
        else if (i <= 0) { i = 0; dir = 1; }
      }
      requestAnimationFrame(render);
    };
    requestAnimationFrame(render);
  }, { once: true });
  video.muted = true; video.loop = false;
  const start = () => { video.play().catch(() => {}); loop(); };
  video.readyState >= 1 ? start() : video.addEventListener('loadedmetadata', start, { once: true });
}
document.querySelectorAll('.boomerang').forEach((el) => boomerangVideo(el));
```

---

## 9. Crossfading multi-video scene switcher with adaptive text tone

**What / when:** 3–5 stacked looping clips (moods or locations) with a small text tab row to switch scenes; the active clip crossfades in. A transparent foreground cut-out (window frame, cockpit, interior) sits on top with a gentle bob, as if looking out of a moving vehicle. Use it for "choose your atmosphere" heroes (wellness, travel, focus apps).

**Premium parameters**
- Crossfade `opacity 1000ms ease-in-out`; lock input for the same 1000 ms so clicks can't stack. Pause the outgoing clip after the fade.
- Foreground bob: `translateY(0 → -6px)` **3 s ease-in-out infinite**, constant `scale(1.03)` so edges never show.
- Adaptive tone: when a bright clip is active, the hero copy switches to a deep ink (e.g. `#182C41`) over **700 ms**; nav and footer stats stay white.
- Tabs: active = full colour + 1 px bottom border; inactive `opacity .5`, hover `.8`.

**Implementation**
```html
<section class="vswitch" data-tone="light">
  <div class="vswitch__media">
    <video class="is-active" src="scene-1.mp4" autoplay muted loop playsinline></video>
    <video src="scene-2.mp4" muted loop playsinline preload="auto"></video>
    <video src="scene-3.mp4" muted loop playsinline preload="auto"></video>
  </div>
  <img class="vswitch__overlay" src="foreground-frame.png" alt="" aria-hidden="true">
  <div class="vswitch__content">
    <h1>…</h1>
    <div class="vswitch__tabs" role="tablist" aria-label="Scene">
      <button role="tab" aria-selected="true"  data-tone="light">Scene one</button>
      <button role="tab" aria-selected="false" data-tone="light">Scene two</button>
      <button role="tab" aria-selected="false" data-tone="dark">Scene three</button>
    </div>
  </div>
</section>
```
```css
.vswitch{position:relative;height:100vh;height:100svh;overflow:hidden;background:#000}
.vswitch__media video{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0;transition:opacity 1s ease-in-out}
.vswitch__media video.is-active{opacity:1}
.vswitch__overlay{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:1;pointer-events:none;animation:bob 3s ease-in-out infinite}
@keyframes bob{0%,100%{transform:translateY(0) scale(1.03)}50%{transform:translateY(-6px) scale(1.03)}}
.vswitch__content{position:relative;z-index:2;height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center;color:#fff;transition:color .7s ease}
.vswitch[data-tone="dark"] .vswitch__content{color:#182C41}
.vswitch__tabs button{background:none;border:0;border-bottom:1px solid transparent;color:inherit;opacity:.5;padding:6px 2px;cursor:pointer;transition:opacity .3s,border-color .3s}
.vswitch__tabs button:hover{opacity:.8}
.vswitch__tabs button[aria-selected="true"]{opacity:1;border-bottom-color:currentColor}
@media (prefers-reduced-motion:reduce){.vswitch__overlay{animation:none;transform:scale(1.03)}.vswitch__media video{transition:none}}
```
```js
(() => {
  const root = document.querySelector('.vswitch');
  const vids = [...root.querySelectorAll('.vswitch__media video')];
  const tabs = [...root.querySelectorAll('[role="tab"]')];
  let active = 0, locked = false;
  tabs.forEach((tab, i) => tab.addEventListener('click', () => {
    if (i === active || locked) return;
    locked = true;
    const prev = vids[active], next = vids[i];
    next.play().catch(() => {});
    next.classList.add('is-active'); prev.classList.remove('is-active');
    tabs[active].setAttribute('aria-selected', 'false'); tab.setAttribute('aria-selected', 'true');
    root.dataset.tone = tab.dataset.tone || 'light';
    active = i;
    setTimeout(() => { prev.pause(); locked = false; }, 1000);   // matches the CSS crossfade
  }));
})();
```

**Mobile:** preload only the active clip (`preload="metadata"` on the rest) to save data; the others load on first tap.

---

## Kinetic Typography & Text Motion

# Type & text motion

Entrance choreography, headline effects, display type as image, and animated numbers.

**Conventions.** Single-file, no build step, dark page unless stated. Shared tokens and helpers (paste once):
```css
:root{
  --ease-out-expo:cubic-bezier(.16,1,.3,1);
  --ease-out-quint:cubic-bezier(.22,1,.36,1);
  --ease-out-cubic:cubic-bezier(.215,.61,.355,1);
}
.sr-only{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}
```
Golden rule for every entrance: the **rest state is visible**. Hide only through `animation-fill-mode: both` or a `.js` class, so a failed script never leaves a blank page.

---

## 1. Staggered blur-rise load choreography (+ settle-zoom media)

**What / when:** The hero's first second. Each element rises a few px out of a blur into focus in a deliberate reading order (nav → eyebrow → headline lines → body → CTAs → proof strip) while the background media settles from a slight zoom. The blur is what separates premium from a plain fade-up. The default entrance for any hero.

**Premium parameters**
- Blur-rise: `opacity 0, translateY(20–28px), blur(6–12px)` (optionally `scale(.98)`) → rest, **0.85–1.1 s**, `--ease-out-expo` or `cubic-bezier(.22,1,.36,1)`. Heavier variant: `blur(20px), y 40px`, 1 s ease-out.
- The nav comes **down** from `-10…-20px` (0.5–0.8 s); content comes **up**; secondary items may slide in sideways.
- Plain rise (no blur) for paragraphs: `y 20–24px`, 0.8–1 s. `filter: blur()` on huge text is costly, so keep blur for headline lines and a few chips.
- Media settle: `scale(1.12 → 1)` 1.8 s expo (images); `scale(1.05 → 1)` + fade 1.8 s (video).
- Proven timelines (start delays):
  - Cinematic glass hero: badge .4 → headline words (stagger .1) → sub .8 → CTAs 1.1 → stat cards 1.3 → partner strip 1.4.
  - Minimal centred: headline 0 → sub .2 → CTA .4 (0.8 s, y 24).
  - Bold left-aligned: tagline 0 → heading .2 → sub .4 → CTA row .6 → stats .8 (y 30).
  - Editorial light page: nav down (0.8 s) · video settle 1.8 s · badge/eyebrow .2–.6 → heading .4–.8 → paragraph .7 → buttons .9–1.0.
  - Tight technical: brand/nav/CTA 0 → headline .06 → sub .14 → CTAs .22 → logo strip .34 (fade only, 1.1 s); y 14.
  - Nav-first: logo 0 · links .10/.15/.20/.25/.30 · nav actions .35/.40 · title .4 · description .5 · primary .6 · secondary .7.
  - Two-line headline: line 1 .25, line 2 .42, bottom-left copy .70, bottom-right copy .85.
  - Split hero: header fade-down −20 px · left copy rise 40 px 1 s · right visual `scale(.85 → 1)` 1.2 s at .3 · logo strip .6.
- Rules of thumb: 80–200 ms between siblings, everything lands by ~1.5 s, the headline gets the longest duration, logos and fine print only fade.

**Implementation**
```css
@keyframes blurRise{from{opacity:0;transform:translateY(var(--rise,28px));filter:blur(var(--blur,12px))}to{opacity:1;transform:none;filter:blur(0)}}
@keyframes fadeRise{from{opacity:0;transform:translateY(var(--rise,20px))}to{opacity:1;transform:none}}
@keyframes fadeDown{from{opacity:0;transform:translateY(-16px)}to{opacity:1;transform:none}}
@keyframes settleZoom{from{transform:scale(var(--zoom-from,1.12))}to{transform:scale(1)}}
.in-blur{animation:blurRise var(--dur,1.1s) var(--ease-out-expo) var(--d,0ms) both}
.in-fade{animation:fadeRise var(--dur,1s) var(--ease-out-expo) var(--d,0ms) both}
.in-down{animation:fadeDown .8s var(--ease-out-expo) var(--d,0ms) both}
.in-zoom{animation:settleZoom 1.8s var(--ease-out-expo) both}
@media (prefers-reduced-motion:reduce){.in-blur,.in-fade,.in-down,.in-zoom{animation:none}}
```
```html
<header class="in-down">…</header>
<div class="hero__bg in-zoom" style="background-image:url(hero.jpg)"></div>
<h1>
  <span class="in-blur" style="display:block;--d:250ms">First line</span>
  <span class="in-blur" style="display:block;--d:420ms">second line</span>
</h1>
<p class="in-fade" style="--d:700ms">Supporting copy…</p>
<a class="btn in-fade" style="--d:850ms" href="#">Primary action</a>
```
`both` keeps elements hidden only during their delay; if animations never run, everything stays visible. Gate the sequence on fonts to avoid a re-layout mid-animation:
```css
.in-blur,.in-fade{animation-play-state:paused}
.fonts-ready .in-blur,.fonts-ready .in-fade{animation-play-state:running}
```
```js
document.fonts.ready.then(() => document.documentElement.classList.add('fonts-ready'));
setTimeout(() => document.documentElement.classList.add('fonts-ready'), 1500);   // never wait forever
```

**Framer Motion variant**
```tsx
const rise = (delay = 0) => ({
  initial: { opacity: 0, y: 28, filter: 'blur(12px)' },
  animate: { opacity: 1, y: 0, filter: 'blur(0px)' },
  transition: { duration: 1.1, delay, ease: [0.16, 1, 0.3, 1] },
});
<motion.h1 {...rise(0.25)}>…</motion.h1>
// lists: variants with custom index -> delay: i * 0.12
```
**GSAP variant:** `gsap.timeline({defaults:{ease:'power3.out'}}).from('.name',{opacity:0,y:50,duration:1.2,delay:.1}).from('.blur-in',{opacity:0,y:20,filter:'blur(10px)',duration:1,stagger:.1},.3)`.

---

## 2. Fail-safe entrance system with a motion vocabulary

**What / when:** A production-grade version of technique 1. Each element picks a *verb* (scale, soft-rise, mask, pop, button, side-slide, stat) and a delay. The page can never be stuck blank, and once an animation ends its `transform` is released so hover effects work. Use it on single-file pages that want rich choreography with zero framework.

**Premium parameters**
- Resting state visible (`opacity:1`); hiding comes only from `animation-fill-mode: both`.
- Duration 1.05 s, `cubic-bezier(.16,1,.3,1)`, delay from `--d` (default .08 s). The lede gets 1.25 s.
- Vocabulary: `in-scale` `opacity 0, scale(.84)` (logo, alternating nav items) · `in-soft` `translateY(14px)` · `in-mask` `translateY(40%)` inside an overflow-hidden line · `in-pop` `scale(.9) → 1.03 @70 % → 1` (badges) · `in-btn` `translateY(18px) scale(.94)` · `in-side` `translateX(22px)` (secondary CTAs) · `in-stat` `translateY(20px)` · `in-star` `scale(.2) rotate(-50deg) → scale(1.2) rotate(8deg) @65 % → rest`, 0.9 s (sparkle icon) · `in-em` `opacity .35, blur(4px)` → sharp, 1.2 s @ .72 s (italic accent words).
- Example timeline: logo .08; nav items .16/.28/.40/.52 (alternating scale/soft); header CTA .34; badge .22; H1 line 1 .42, line 2 .62; lede .82; primary CTA .96; ghost CTA 1.10; stats 1.12/1.28/1.44.
- After `animationend` the element gets `.is-in` (`animation:none` + final values); otherwise the held `transform` from fill-mode overrides `:hover{transform}`.
- JS fallback: after two rAFs, if no animation is running or finished, force `.is-in` on everything.

**Implementation**
```css
.appear{animation-duration:1.05s;animation-fill-mode:both;animation-timing-function:cubic-bezier(.16,1,.3,1);animation-delay:var(--d,.08s)}
.appear--scale{animation-name:in-scale}
.appear--soft {animation-name:in-soft}
.appear--mask {animation-name:in-mask}
.appear--pop  {animation-name:in-pop}
.appear--btn  {animation-name:in-btn}
.appear--side {animation-name:in-side}
.appear--stat {animation-name:in-stat}
.appear.is-in{animation:none;opacity:1;transform:none;clip-path:none;filter:none}
@keyframes in-scale{from{opacity:0;transform:scale(.84)}}
@keyframes in-soft {from{opacity:0;transform:translateY(14px)}}
@keyframes in-mask {from{opacity:0;transform:translateY(40%)}}
@keyframes in-pop  {0%{opacity:0;transform:scale(.9)}70%{opacity:1;transform:scale(1.03)}100%{opacity:1;transform:scale(1)}}
@keyframes in-btn  {from{opacity:0;transform:translateY(18px) scale(.94)}}
@keyframes in-side {from{opacity:0;transform:translateX(22px)}}
@keyframes in-stat {from{opacity:0;transform:translateY(20px)}}
@keyframes in-star {0%{transform:scale(.2) rotate(-50deg)}65%{transform:scale(1.2) rotate(8deg)}100%{transform:none}}
@keyframes in-em   {from{opacity:.35;filter:blur(4px)}}
.headline-line{display:block;overflow:hidden;padding:.06em .15em .14em}  /* room for descenders/italics */
.badge-star{animation:in-star .9s cubic-bezier(.16,1,.3,1) .28s both}
h1 em{animation:in-em 1.2s cubic-bezier(.16,1,.3,1) .72s both}
@media (prefers-reduced-motion:reduce){
  .appear,.badge-star,h1 em{animation:none!important;opacity:1;transform:none;clip-path:none;filter:none}
}
```
```html
<a class="logo appear appear--scale" style="--d:.08s">…</a>
<span class="badge appear appear--pop" style="--d:.22s"><svg class="badge-star">…</svg>Label</span>
<h1>
  <span class="headline-line appear appear--mask" style="--d:.42s">First line with <em>accent</em></span>
  <span class="headline-line appear appear--mask" style="--d:.62s">second line.</span>
</h1>
<p class="lede appear appear--soft" style="--d:.82s;animation-duration:1.25s">…</p>
<a class="btn appear appear--btn" style="--d:.96s">Primary</a>
<a class="btn appear appear--side" style="--d:1.10s">Secondary</a>
```
```js
const appearEls = document.querySelectorAll('.appear');
appearEls.forEach((el) => el.addEventListener('animationend', (e) => {
  if (e.target === el) el.classList.add('is-in');     // ignore bubbling from children (e.g. <em>)
}));
requestAnimationFrame(() => requestAnimationFrame(() => {
  const running = [...appearEls].some((el) =>
    (el.getAnimations ? el.getAnimations() : []).some((a) => a.playState === 'running' || a.playState === 'finished'));
  if (!running) appearEls.forEach((el) => el.classList.add('is-in'));
}));
```

---

## 3. Word-by-word blur-in headline

**What / when:** Headline words arrive one after another, each rising from below, overshooting slightly upward and coming into focus. It feels like an exhale. Best with large italic serif display type over video. Trigger on load for heroes and on scroll-into-view for section headings.

**Premium parameters**
- Per word: `blur(10px), opacity 0, y 50px` → at 50 %: `blur(5px), opacity .5, y -5px` → `blur(0), opacity 1, y 0`. 0.7 s per word, ease-out, stagger 100 ms.
- Words are `inline-block` with `margin-right: .28em` (non-breaking spaces get eaten by tight negative tracking).
- Container `display:flex; flex-wrap:wrap; justify-content:center; row-gap:.1em`. IntersectionObserver threshold 0.1, once.
- Pairs with italic serif display ~`clamp(56px,7vw,88px)`, `line-height:.8`, `letter-spacing:-.045em`.

**Implementation**
```html
<h1 class="blur-text">Words that arrive one breath at a time</h1>
```
```css
.blur-text{display:flex;flex-wrap:wrap;justify-content:center;row-gap:.1em;
  font:italic 400 clamp(56px,7vw,88px)/.8 'Instrument Serif',serif;letter-spacing:-.045em;color:#fff}
.bt-word{display:inline-block;margin-right:.28em;opacity:0;filter:blur(10px);transform:translateY(50px);will-change:transform,filter,opacity}
.bt-word:last-child{margin-right:0}
.blur-text.is-in .bt-word{animation:bt-in .7s ease-out both;animation-delay:calc(var(--i) * var(--stagger,100ms) + var(--base,0ms))}
@keyframes bt-in{
  0%  {filter:blur(10px);opacity:0;transform:translateY(50px)}
  50% {filter:blur(5px); opacity:.5;transform:translateY(-5px)}
  100%{filter:blur(0);   opacity:1;transform:translateY(0)}
}
@media (prefers-reduced-motion:reduce){.bt-word{opacity:1;filter:none;transform:none}.blur-text.is-in .bt-word{animation:none}}
```
```js
function blurText(el, { stagger = 100, base = 0, threshold = 0.1 } = {}) {
  const words = el.textContent.trim().split(/\s+/);
  el.textContent = '';
  words.forEach((w, i) => {
    const s = document.createElement('span');
    s.className = 'bt-word'; s.textContent = w; s.style.setProperty('--i', i);
    el.append(s);
    if (i < words.length - 1) el.append(' ');   // real spaces keep copy/paste and screen readers right
  });
  el.style.setProperty('--stagger', `${stagger}ms`);
  el.style.setProperty('--base', `${base}ms`);
  const io = new IntersectionObserver(([entry]) => {
    if (entry.isIntersecting) { el.classList.add('is-in'); io.disconnect(); }
  }, { threshold });
  io.observe(el);
}
document.querySelectorAll('.blur-text').forEach((el) => blurText(el));
```
The word spans are created by the script, so without JS the headline simply shows as plain text. For headlines with an `<em>` word, wrap the words by hand in `.bt-word` spans with `--i` inline and call only the observer part.

**Framer Motion variant**
```tsx
{words.map((w, i) => (
  <motion.span key={i} style={{ display: 'inline-block', marginRight: '0.28em' }}
    initial={{ filter: 'blur(10px)', opacity: 0, y: 50 }}
    animate={inView ? { filter: ['blur(10px)', 'blur(5px)', 'blur(0px)'], opacity: [0, 0.5, 1], y: [50, -5, 0] } : undefined}
    transition={{ duration: 0.7, times: [0, 0.5, 1], ease: 'easeOut', delay: i * 0.1 }}>{w}</motion.span>
))}
```

---

## 4. Split-text headline entrances (masked line/word pull-up · soft word rise · per-character cascade)

**What / when:** Headlines that assemble line by line, word by word or letter by letter. The masked pull-up (type rising out of a slot) is the classic editorial move for giant display words and stacked uppercase statements; the per-character lateral cascade feels like a sentence being written across the screen. `splitText()` below is also the splitter used by technique 10.

**Premium parameters**
- Masked lines (hand-written): `translateY(110%) → 0` inside `overflow:hidden`, 0.7 s `cubic-bezier(.22,1,.36,1)`, delays `0.4 + i × 0.14 s`. Stacked display words at line-height .88–.92, e.g. right-aligned uppercase 600 at `clamp(2rem, 9vw, 9rem)`.
- Masked words: inner word `translateY(110%) → 0`, **1.2 s** `--ease-out-expo`, stagger **60 ms** (letter blocks) to **80 ms** (words); optional parent `scale(1.03 → 1)` over the same time.
- Soft rise (no mask): `y 20px + opacity`, stagger 80 ms, ~0.8 s.
- Character cascade: `translateX(-18px) + opacity 0` → rest, 500 ms per char, **30 ms** step, starts at 200 ms; subhead at 800 ms, CTAs 1200 ms.
- The mask needs breathing room: pad the clip box `.06em .15em .14em` with an equal negative margin, or descenders and italic overhangs get cut.
- Words stay unbreakable (`white-space:nowrap` on the word wrapper); italic serif words inside `<em>` keep their styling after splitting.

**Implementation (hand-written masked lines, CSS only)**
```html
<h1 class="mask-lines">
  <span class="ml"><span style="--i:0">Make</span></span>
  <span class="ml"><span style="--i:1">Things</span></span>
  <span class="ml"><span style="--i:2">Last</span></span>
</h1>
```
```css
.mask-lines{margin:0;font:600 clamp(2rem,9vw,9rem)/.88 Inter,sans-serif;text-transform:uppercase;text-align:right;letter-spacing:-.02em}
.ml{display:block;overflow:hidden;padding:.06em .15em .14em;margin:-.06em -.15em -.14em}
.ml>span{display:block;animation:ml-up .7s cubic-bezier(.22,1,.36,1) both;animation-delay:calc(.4s + var(--i) * .14s)}
@keyframes ml-up{from{transform:translateY(110%)}}
@media (prefers-reduced-motion:reduce){.ml>span{animation:none}}
```

**Implementation (automatic splitter)**
```js
// modes: 'words' (masked pull-up) | 'chars' (lateral cascade) | 'plain' (bare word spans) | 'plain-chars'
function splitText(root, mode = 'words') {
  if (root.dataset.splitDone) return;
  root.dataset.splitDone = '1';
  // Word spans read fine in screen readers. Letter spans can be spelled out, so in char modes
  // the split copy is aria-hidden and one clean visually-hidden copy is added.
  const charMode = mode === 'chars' || mode === 'plain-chars';
  const plain = (root.innerText || root.textContent).replace(/\s+/g, ' ').trim();
  let i = 0;
  const span = (cls, text) => { const s = document.createElement('span'); s.className = cls; if (text != null) s.textContent = text; return s; };
  const walk = (node) => [...node.childNodes].forEach((n) => {
    if (n.nodeType === Node.ELEMENT_NODE) return walk(n);       // keeps <em>, <strong>, <br>
    if (n.nodeType !== Node.TEXT_NODE) return;
    const frag = document.createDocumentFragment();
    n.textContent.split(/(\s+)/).forEach((part) => {
      if (!part) return;
      if (/^\s+$/.test(part)) { frag.append(' '); return; }
      if (charMode) {
        const w = span(mode === 'chars' ? 'sc-w' : 'sp-w');
        w.setAttribute('aria-hidden', 'true');
        for (const ch of part) { const c = span(mode === 'chars' ? 'sc-c' : 'sp', ch); c.style.setProperty('--i', i++); w.append(c); }
        frag.append(w);
      } else if (mode === 'plain') {
        const w = span('sp', part); w.style.setProperty('--i', i++); frag.append(w);
      } else {
        const o = span('sw-o'), inner = span('sw-i', part);
        inner.style.setProperty('--i', i++); o.append(inner); frag.append(o);
      }
    });
    n.replaceWith(frag);
  });
  walk(root);
  if (charMode) root.prepend(span('sr-only', plain));
  return i;   // number of pieces
}
// Hero (on load): split, then add .is-in after the first paint.
document.querySelectorAll('[data-split-text]').forEach((el) => {
  splitText(el, el.dataset.splitText);
  requestAnimationFrame(() => requestAnimationFrame(() => el.classList.add('is-in')));
});
// Below the fold: add .is-in from an IntersectionObserver instead (scroll.md, technique 1).
```
```css
/* masked word pull-up */
.sw-o{display:inline-block;overflow:hidden;vertical-align:top;padding:0 .06em .14em;margin:0 -.06em -.14em}
.sw-i{display:inline-block;transform:translateY(110%);transition:transform var(--dur,1.2s) var(--ease-out-expo);
  transition-delay:calc(var(--start,0ms) + var(--i) * var(--step,60ms))}
.is-in .sw-i{transform:none}
/* soft word rise (no mask) */
.split-soft .sw-o{overflow:visible}
.split-soft .sw-i{transform:translateY(20px);opacity:0;transition-property:transform,opacity;--dur:.8s;--step:80ms}
.split-soft.is-in .sw-i{transform:none;opacity:1}
/* per-character lateral cascade */
.sc-w{display:inline-block;white-space:nowrap}
.sc-c{display:inline-block;opacity:0;transform:translateX(-18px);transition:opacity .5s ease-out,transform .5s ease-out;
  transition-delay:calc(var(--start,200ms) + var(--i) * 30ms)}
.is-in .sc-c{opacity:1;transform:none}
.sp-w{display:inline-block;white-space:nowrap}
@media (prefers-reduced-motion:reduce){.sw-i,.sc-c{transition:none!important;transform:none!important;opacity:1!important}}
```
```html
<h1 data-split-text="words" style="font-size:clamp(4rem,20vw,18rem);line-height:.85;letter-spacing:-.07em">Wordmark</h1>
<h2 data-split-text="words" class="split-soft">I make <em>quiet, cinematic</em> work.</h2>
<h1 data-split-text="chars">Shaping tomorrow<br>with vision and action.</h1>
```

**Framer Motion variant:** `<span className="block overflow-hidden"><motion.span className="block" initial={{ y: '110%' }} animate={{ y: 0 }} transition={{ delay: 0.4 + i * 0.14, duration: 0.7, ease: [0.22, 1, 0.36, 1] }} /></span>`; for soft words use `initial={{y:20,opacity:0}}` with `useInView(ref,{once:true})` and `delay: i*0.08`.

---

## 5. Serif-italic accent words inside a headline

**What / when:** One to three words of a headline switch to an italic display serif, a touch larger and in a muted tone. The headline gains a spoken emphasis and an editorial voice. One of the most reliable premium signals; use it whenever a headline has a natural key phrase.

**Premium parameters**
- Sans base: Inter 500, `letter-spacing:-.045em`, `line-height:1.12`. Accent: Instrument Serif italic 400 at `1.08em` (serif x-height is smaller), `letter-spacing:-.03em`.
- Accent colour is **muted, not brighter**: `#9a9a9a` on black, `#6F6F6F` on white, or `rgba(255,255,255,.6–.8)`. A contrasting hue also works (deep green `#336443` with sage `#85AB8B`).
- Inverse version: an all-serif headline (`line-height:.95`, `letter-spacing ≈ -.025em`) with the italic words greyed out.
- Tone-only variant: no italics, just `<em class="not-italic">` in the muted foreground.
- Optional sharpen-in: the accent starts at `opacity .35, blur(4px)` and focuses over 1.2 s after its line lands (.72 s).
- Pairings: Inter + Instrument Serif; Poppins + Source Serif 4 italic; Barlow body with an all-italic Instrument Serif display; Playfair Display italic as the accent.

**Implementation**
```html
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Instrument+Serif:ital@0;1&display=swap" rel="stylesheet">
<h1 class="mixed">Ship <em>calmer software</em><br>in half the time.</h1>
```
```css
.mixed{font:500 clamp(36px,4.4vw,76px)/1.12 Inter,system-ui,sans-serif;letter-spacing:-.045em;color:#fff;text-align:center}
.mixed em{font-family:'Instrument Serif',Georgia,serif;font-style:italic;font-weight:400;font-size:1.08em;
  letter-spacing:-.03em;color:#9a9a9a;animation:em-sharpen 1.2s cubic-bezier(.16,1,.3,1) .72s both}
@keyframes em-sharpen{from{opacity:.35;filter:blur(4px)}}
@media (prefers-reduced-motion:reduce){.mixed em{animation:none}}
```

---

## 6. Gradient-clipped text: static metallic and animated shine sweep

**What / when:** **Metallic:** a vertical two-stop gradient clipped to giant type, reading as brushed steel lit from below; use it for name-as-hero portfolios and section titles. **Shine sweep:** a multi-stop gradient whose highlight travels endlessly through one key word; use it for the single "magic" word of a SaaS headline. Gradient text is rare by design: one element per page.

**Premium parameters**
- Metallic: `linear-gradient(180deg, #646973 0%, #BBCCD7 100%)` (dark top → cool light bottom) on weight 900, uppercase, `line-height:1`, tight tracking.
- Sweep stops `dark 0 % → brand-dark 12.5 % → highlight 32.5 % → brand 50 % → brand-dark 67.5 % → dark 87.5–100 %`. First and last stops must match so the tile repeats seamlessly. `background-size:200% auto`, position `-200% → 200%`, 6 s linear infinite.
- Choose base stops for contrast with what's behind: on black use mid-greys or blues, not near-black.
- Optional grain inside the glyphs (surfaces-and-buttons.md, technique 8) makes the gradient feel printed; drop it ≤1024 px.

**Implementation**
```css
.text-metal{background:linear-gradient(180deg,#646973 0%,#BBCCD7 100%);
  -webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;color:transparent}
.text-shine{background-image:linear-gradient(to right,#091020 0%,#0B2551 12.5%,#A4F4FD 32.5%,#00d2ff 50%,#0B2551 67.5%,#091020 87.5%,#091020 100%);
  background-size:200% auto;-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;color:transparent;
  animation:shine 6s linear infinite}
@keyframes shine{from{background-position:-200% center}to{background-position:200% center}}
@media (prefers-reduced-motion:reduce){.text-shine{animation:none;background-position:30% center}}
```
```html
<h1 style="font:600 clamp(40px,7vw,72px)/.9 Inter,sans-serif;letter-spacing:-.025em">Your workflow.<br><span class="text-shine">Reimagined</span></h1>
```
Keep `color:transparent` together with `-webkit-text-fill-color` (engines differ). Theme `::selection` so selected gradient text stays readable.

---

## 7. Scramble / decode text (entrance + hover)

**What / when:** Characters resolve from random glyphs left to right, like a terminal decoding: on entrance for headline lines, on hover for nav links and buttons. Made for AI, tech and sci-fi brands, especially in a monospace.

**Premium parameters**
- Glyph set `A–Z a–z 0–9 !@#$%^&*()_+~|}{[]:;?><`.
- Entrance: tick **25 ms**, reveal cursor advances **0.5 chars/tick**; up to **3** random glyphs run ahead of it and nothing beyond (the text "grows"). Spaces stay spaces. Line delays e.g. 200 / 500 / 700 / 1000 ms for four corner lines.
- Hover: everything scrambles, then resolves at **4 ticks per char**; unhover snaps back instantly.
- Use a **monospace** face: constant glyph widths mean zero jitter.
- Pair with a body paragraph that simply fades up (y 25 → 0, 0.9 s, `--ease-out-cubic`, 0.2 s delay).

**Implementation**
```js
const GLYPHS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()_+~|}{[]:;?><';
const randGlyph = () => GLYPHS[(Math.random() * GLYPHS.length) | 0];

function scrambleIn(el, { delay = 0, speed = 0.5, lookahead = 3, tick = 25 } = {}) {
  const text = el.textContent;
  const sr = document.createElement('span'); sr.className = 'sr-only'; sr.textContent = text;
  el.after(sr); el.setAttribute('aria-hidden', 'true');
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  el.textContent = ' ';
  setTimeout(() => {
    let pos = 0;
    const id = setInterval(() => {
      pos += speed;
      const shown = Math.floor(pos);
      let out = '';
      for (let i = 0; i < text.length; i++) {
        if (i >= shown + lookahead) break;
        out += text[i] === ' ' ? ' ' : i < shown ? text[i] : randGlyph();
      }
      el.textContent = out || ' ';
      if (shown >= text.length) { clearInterval(id); el.textContent = text; }
    }, tick);
  }, delay);
}
function scrambleOnHover(el, { framesPerChar = 4, tick = 25 } = {}) {
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  const text = el.textContent; let id = 0;
  el.addEventListener('mouseenter', () => {
    let frame = 0; clearInterval(id);
    id = setInterval(() => {
      const revealed = Math.floor(frame / framesPerChar);
      el.textContent = [...text].map((c, i) => (c === ' ' ? ' ' : i < revealed ? c : randGlyph())).join('');
      if (revealed >= text.length) { clearInterval(id); el.textContent = text; }
      frame++;
    }, tick);
  });
  el.addEventListener('mouseleave', () => { clearInterval(id); el.textContent = text; });
}
document.querySelectorAll('[data-scramble]').forEach((el) => scrambleIn(el, { delay: +(el.dataset.delay || 0) }));
document.querySelectorAll('[data-scramble-hover]').forEach((el) => scrambleOnHover(el));
```
```html
<h1 class="mono"><span data-scramble data-delay="200">Line one</span><br><span data-scramble data-delay="500">Line two</span></h1>
<a href="#about"><span data-scramble-hover>About</span></a>
```
**Layout:** reserve each line's width (`display:inline-block; min-width: Nch` in a mono face) so the growing entrance never reflows neighbours.

---

## 8. Typewriter with zero-reflow caret, two-tone text and a depth-of-field lead-in

**What / when:** An "assistant is speaking" hero or a typed headline: a soft, out-of-focus intro line sits above a sharp line that types itself out with a blinking caret, optionally switching colour mid-sentence, followed by quick-reply pills or a CTA. For AI products, agencies with a persona, and contact pages.

**Premium parameters**
- **35–38 ms/char**, start delay **400–600 ms**. The caret disappears when typing ends.
- Caret: `2px × 1.1em`, `currentColor` or the accent, `blink 1s step-end infinite`; `margin-right:-2px` cancels its own width so it never pushes a word to the next line.
- **Zero reflow:** the untyped remainder is rendered `color: transparent`, so the block holds its final size and line breaks from frame one (no `min-height` hacks). `white-space: pre-wrap` supports `\n`.
- Two-tone: split at a character index (e.g. first ~60 % dark, the rest light), great over a split-tone background.
- **Depth-of-field lead-in:** the line above is the same size (`clamp(18px,4vw,26px)`, lh 1.33) with `filter: blur(4px)`, non-selectable: the eye racks focus onto the sharp line.
- Follow-ups: a CTA at typing end + ~200 ms; or quick-reply pills independently at 400 ms (`opacity + translateY(8px)`, 0.4 s). Pills: white, black text, `1px solid rgba(0,0,0,.1)`, 13–15 px, `padding:.3em 1.25em`; hover inverts over 200 ms; an outline pill copies an email to the clipboard.
- Large contact-headline variant: 48 → 76 px, `line-height 1.08`, tight tracking.

**Implementation**
```html
<div class="persona">
  <p class="voice" aria-hidden="true">Hi, I'm the studio's assistant,<br>here to point you the right way</p>
  <p class="tw" data-text="Good to see you. What are we making today?" data-split="17"></p>
  <div class="replies">
    <button class="reply">Start a project</button>
    <button class="reply">See open roles</button>
    <button class="reply reply--outline" data-copy="hello@example.com">Reach us: <u>hello@example.com</u></button>
  </div>
</div>
```
```css
.persona{max-width:36rem;color:#fff}
.voice,.tw{font-size:clamp(18px,4vw,26px);line-height:1.33;font-weight:400;margin:0 0 24px}
.voice{filter:blur(4px);user-select:none;pointer-events:none}
.tw{white-space:pre-wrap}
.tw__a{color:inherit}
.tw__b{color:var(--tw-b,rgb(255 255 255/.55))}     /* second tone */
.tw__rest{color:transparent}
.tw__caret{display:inline-block;width:2px;height:1.1em;margin-right:-2px;vertical-align:-.15em;
  background:var(--accent,currentColor);animation:tw-blink 1s step-end infinite}
.tw.is-done .tw__caret{display:none}
@keyframes tw-blink{0%,100%{opacity:1}50%{opacity:0}}
.replies{display:flex;flex-wrap:wrap;row-gap:4px;opacity:0;transform:translateY(8px);transition:opacity .4s ease,transform .4s ease}
.replies.is-in{opacity:1;transform:none}
.reply{display:inline-flex;align-items:center;gap:10px;white-space:nowrap;border-radius:999px;cursor:pointer;
  background:#fff;color:#000;border:1px solid rgba(0,0,0,.1);font-size:clamp(13px,1.2vw,15px);
  padding:.3em 1.25em;margin:0 .2em .4em;transition:background-color .2s,color .2s}
.reply:hover{background:#000;color:#fff}
.reply--outline{background:transparent;color:#fff;border-color:#fff}
.reply--outline:hover{background:#fff;color:#000}
@media (prefers-reduced-motion:reduce){.tw__caret{animation:none}}
```
```js
function typewriter(el, { speed = 36, startDelay = 500, onDone } = {}) {
  const text = el.dataset.text.replace(/\\n/g, '\n');
  const split = el.dataset.split ? +el.dataset.split : text.length;   // chars before split use tone A
  const sr = document.createElement('span'); sr.className = 'sr-only'; sr.textContent = text;
  const vis = document.createElement('span'); vis.setAttribute('aria-hidden', 'true');
  vis.innerHTML = '<span class="tw__a"></span><span class="tw__b"></span><span class="tw__caret"></span><span class="tw__rest"></span>';
  el.replaceChildren(sr, vis);
  const [a, b, , rest] = vis.children;
  const paint = (n) => {
    const k = Math.min(n, split);
    a.textContent = text.slice(0, k);
    b.textContent = text.slice(k, n);
    rest.textContent = text.slice(n);
  };
  const finish = () => { el.classList.add('is-done'); onDone && onDone(); };
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) { paint(text.length); return finish(); }
  paint(0);
  setTimeout(() => {
    let n = 0;
    const id = setInterval(() => { paint(++n); if (n >= text.length) { clearInterval(id); finish(); } }, speed);
  }, startDelay);
}
typewriter(document.querySelector('.tw'));
setTimeout(() => document.querySelector('.replies').classList.add('is-in'), 400);
// or: typewriter(el, { onDone: () => setTimeout(() => cta.classList.add('is-in'), 200) });
document.querySelectorAll('[data-copy]').forEach((b) => b.addEventListener('click', async () => {
  try { await navigator.clipboard.writeText(b.dataset.copy); b.dataset.state = 'copied'; } catch {}   // https or localhost only
}));
```

**React variant:** a `useTypewriter(text, speed = 36, startDelay = 500)` hook returning `{ count, done }` (a `setTimeout` that starts a `setInterval`, both cleared on unmount), rendered with the same three spans: `text.slice(0,count)`, caret, and `text.slice(count)` in transparent.

---

## 9. Rotating word slot (zero-reflow)

**What / when:** One word inside a sentence cycles through alternatives ("A ___ based in …"), set in an italic serif accent. Also used for the cycling word in a preloader. Adds personality without extra copy.

**Premium parameters:** interval **2 s** (sentence) / **900 ms** (preloader); enter `opacity 0, translateY(8px)` → rest in **0.4 s ease-out**, exit upward (preloader travels ±20 px). All words are stacked in one grid cell, so the slot is as wide as the longest word and the sentence never reflows.

**Implementation**
```html
<p class="role-line">A <span class="rotator" data-interval="2000" aria-hidden="true">
  <span class="is-active">designer</span><span>developer</span><span>founder</span><span>writer</span>
</span><span class="sr-only">designer, developer, founder and writer</span> based somewhere nice.</p>
```
```css
.rotator{display:inline-grid;vertical-align:bottom;font-family:'Instrument Serif',serif;font-style:italic}
.rotator>span{grid-area:1/1;justify-self:center;opacity:0;transform:translateY(8px);transition:opacity .4s ease-out,transform .4s ease-out}
.rotator>span.is-active{opacity:1;transform:none}
.rotator>span.is-leaving{opacity:0;transform:translateY(-8px)}
```
```js
document.querySelectorAll('.rotator').forEach((r) => {
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  const items = [...r.children];
  let i = Math.max(0, items.findIndex((s) => s.classList.contains('is-active')));
  setInterval(() => {
    const prev = items[i];
    prev.classList.replace('is-active', 'is-leaving');
    setTimeout(() => prev.classList.remove('is-leaving'), 400);
    i = (i + 1) % items.length;
    items[i].classList.add('is-active');
  }, +r.dataset.interval || 2000);
});
```
Single-element variant (used by the preloader in technique 13): `swapWord()` animates the old text out with WAAPI and the new one in.

---

## 10. Scroll-linked word-by-word (or char-by-char) opacity reveal

**What / when:** A manifesto or About paragraph in large type starts at 15–20 % opacity and "lights up" piece by piece as the reader scrolls through it, so reading pace is tied to the scrollbar. Highlight 2–3 key words in full foreground while the rest end on a softer tone. One or two per page.

**Premium parameters**
- Start opacity **0.15** (words) / **0.2** (chars); end 1.
- Progress window `['start 0.8', 'end 0.2']`: 0 when the block's top hits 80 % of the viewport, 1 when its bottom reaches 20 %.
- Per-piece window `[i/N − 0.1, i/N + 0.05]` (soft overlap), or strict `[i/N, (i+1)/N]` for a crisper sweep (`before:0, after:1/N`).
- Type: words `clamp(1.5rem, 4vw, 3rem)`, 500, `letter-spacing:-1px`, lh 1.2; chars version centred, `max-width:560px`, `clamp(1rem,2vw,1.35rem)`, lh 1.625, a cool light tone (e.g. `#D7E2EA`) on near-black.
- Opacity-only, so no layout shift; pieces are inline spans, so line breaking stays natural.

**Implementation** (needs `splitText()` from technique 4: `'plain'` for words, `'plain-chars'` for characters)
```html
<p class="scroll-reveal">We're building a place where <span class="hl">depth</span> meets
<span class="hl">clarity</span>, and every word arrives as you get to it.</p>
```
```css
.scroll-reveal{font-size:clamp(1.5rem,4vw,3rem);font-weight:500;letter-spacing:-1px;line-height:1.2;color:hsl(210 17% 82%)}
.scroll-reveal .hl{color:#fff}
.scroll-reveal .sp{opacity:.15}
```
```js
function scrollReveal(el, { mode = 'plain', from = 0.15, start = 0.8, end = 0.2, before = 0.1, after = 0.05 } = {}) {
  splitText(el, mode);
  const pieces = [...el.querySelectorAll('.sp')], N = pieces.length;
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  let last = -1, ticking = false;
  const update = () => {
    ticking = false;
    const r = el.getBoundingClientRect(), vh = innerHeight;
    const p = reduce ? 1 : Math.min(1, Math.max(0, (start * vh - r.top) / ((start - end) * vh + r.height)));
    if (Math.abs(p - last) < 0.0005) return;
    last = p;
    pieces.forEach((s, i) => {
      const a = i / N - before, b = i / N + after;
      const t = Math.min(1, Math.max(0, (p - a) / (b - a)));
      s.style.opacity = (from + (1 - from) * t).toFixed(3);
    });
  };
  addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(update); } }, { passive: true });
  addEventListener('resize', update);
  update();
}
document.querySelectorAll('.scroll-reveal').forEach((el) => scrollReveal(el));
// characters: scrollReveal(el, { mode: 'plain-chars', from: 0.2, before: 0, after: 1 / el.textContent.length })
```

**Framer Motion variant:** `const {scrollYProgress} = useScroll({target: ref, offset: ['start 0.8','end 0.2']})`; per piece `const o = useTransform(scrollYProgress, [i/N - 0.1, i/N + 0.05], [0.15, 1])` on a `motion.span`.

---

## 11. Giant display type as image (ghost word behind subject · edge-to-edge wordmark · watermark · scattered words)

**What / when:** Type set so large it becomes architecture. Patterns:
- **Ghost word behind a cut-out subject:** a viewport-wide word sits *between* the background and a transparent product/character/portrait, so the subject stands in front of the letters. Instant depth and a poster composition.
- **Edge-to-edge name / wordmark:** anchored at the bottom or top of the hero, almost touching both edges, often metallic (technique 6), with a tiny superscript mark.
- **Echo / ghost watermark:** the hero line repeated as an enormous low-opacity backdrop title for a later section (pricing, CTA), with cards sitting over it.
- **Scattered words:** a 3-word headline broken across the viewport (left / right / indented), with tiny stats tucked into the gaps.

**Premium parameters**
- Ghost word: condensed heavy face (Anton-style), uppercase, `clamp(90px, 28vw, 380px)`, lh 1, `letter-spacing:-.02em`, nowrap, solid white on a saturated background, `top:18%`. The subject PNG is anchored at the bottom (`object-fit:contain; object-position:bottom center`) and scaled up (×1.68 desktop, ×1.25 mobile) so it covers the lower half of the letters. Z-order: background → word (2) → subject (3) → grain (50) → UI (60).
- Photographic variant: serif title `clamp(4.5rem,14vw,14rem)` / lh .78, width `min(94vw,1780px)`, `top: clamp(122px,19vh,205px)`, cream `#fdf1e1` over a landscape, with the subject cut-out at `bottom:5vh`.
- Wordmark: `19–26vw` (stepping 26 → 24 → 22 → 20 → 19vw by breakpoint), lh .85, `letter-spacing:-.07em`, weight 500; superscript mark `position:absolute; top:.65em; right:-.3em; font-size:.31em`. Name-as-hero: `14vw → 17.5vw`, weight 900, uppercase, with a portrait (280 → 520 px) centred at the bottom overlapping the name.
- Ghost watermark: `clamp(120px, 30vw, 521px)`, uppercase condensed, `letter-spacing:-4px`, `opacity .10`, fill `radial-gradient(circle, rgba(c,0) 0%, c 70%)` via `background-clip:text`, centred +50 px below middle. Echo title alternative: ~9rem / 800 / `-.05em` / lh .9, dropping to 3.5rem solid colour ≤1024 px.
- Scattered: words `14vw` (mobile) / `13vw`, lh .95, `-.04em`, all lowercase; at `top 18 % left` · `top 38 % right` · `top 58 % left 18–28 %`; a note `max-width 240px; 15px` at `top 46 %`; stats 36–48 px with rotated hairlines (`96×1 px`, `rgba(255,255,255,.4)`, `rotate(±20deg)`) and 12–14 px labels at 70 %; a bottom gradient to black.
- For an **exact** full-width fit, measure and scale after `document.fonts.ready` (vw sizes drift with font metrics). Pair the wordmark with a 12-column bottom grid (8 for the word, 4 for a short paragraph + CTA) and animate it with the masked pull-up (technique 4).

**Implementation**
```html
<!-- Ghost word behind a cut-out -->
<section class="ghost-stage">
  <div class="ghost-word" aria-hidden="true">FORM</div>
  <img class="ghost-subject" src="subject.png" alt="Product figure">
  <div class="ghost-ui"><!-- labels, arrows, CTA --></div>
</section>
<!-- Edge-to-edge wordmark -->
<div class="mega-wrap"><h1 class="mega" data-fit>Wordmark<sup class="mega__mark">*</sup></h1></div>
<!-- Ghost gradient watermark (inside a position:relative section) -->
<div class="ghost-mark" aria-hidden="true">Studio</div>
```
```css
.ghost-stage{position:relative;height:100vh;height:100dvh;overflow:hidden;background:var(--stage-bg,#F4845F)}
.ghost-word{position:absolute;left:0;right:0;top:18%;z-index:2;display:flex;justify-content:center;
  font:400 clamp(90px,28vw,380px)/1 Anton,Impact,'Arial Narrow',sans-serif;letter-spacing:-.02em;
  text-transform:uppercase;white-space:nowrap;color:#fff;pointer-events:none;user-select:none}
.ghost-subject{position:absolute;left:50%;bottom:0;height:92%;z-index:3;
  transform:translateX(-50%) scale(1.68);transform-origin:bottom center;object-fit:contain;object-position:bottom center}
.ghost-ui{position:relative;z-index:60}
@media (max-width:639px){.ghost-subject{height:60%;bottom:22%;transform:translateX(-50%) scale(1.25)}}

.mega-wrap{width:100%;overflow:hidden}
.mega{position:relative;display:inline-block;margin:0;white-space:nowrap;font-size:19vw;font-weight:500;line-height:.85;letter-spacing:-.07em;color:#E1E0CC}
.mega__mark{position:absolute;top:.65em;right:-.3em;font-size:.31em;line-height:1}

.ghost-mark{position:absolute;left:50%;top:calc(50% + 50px);translate:-50% -50%;z-index:0;margin:0;pointer-events:none;user-select:none;
  white-space:nowrap;text-transform:uppercase;letter-spacing:-4px;opacity:.1;
  font:400 clamp(120px,30vw,521px)/1 'Anton',Impact,sans-serif;
  background:radial-gradient(circle,rgba(142,127,148,0) 0%,#8E7F94 70%);
  -webkit-background-clip:text;background-clip:text;color:transparent;-webkit-text-fill-color:transparent}
```
```js
// Exact fit-to-width: the element must be display:inline-block; white-space:nowrap
function fitToWidth(el) {
  let lastW = 0;
  const fit = () => {
    const w = el.parentElement.clientWidth;
    if (!w || w === lastW) return;
    lastW = w;
    el.style.fontSize = '100px';
    el.style.fontSize = (100 * w / el.getBoundingClientRect().width).toFixed(2) + 'px';
  };
  new ResizeObserver(fit).observe(el.parentElement);
  if (document.fonts) document.fonts.ready.then(() => { lastW = 0; fit(); });
}
document.querySelectorAll('[data-fit]').forEach(fitToWidth);
```
Scattered words:
```html
<section class="scatter">
  <video class="scatter__bg" src="VIDEO_URL.mp4" autoplay muted loop playsinline aria-hidden="true"></video>
  <h1><span class="scatter__w scatter__w--1">first</span> <span class="scatter__w scatter__w--2">second</span> <span class="scatter__w scatter__w--3">third</span></h1>
  <p class="scatter__note">A two-line supporting sentence tucked into the gap.</p>
  <div class="scatter__stat" style="right:96px;top:14%;text-align:right">
    <div class="scatter__stat-row" style="justify-content:flex-end"><span class="scatter__rule" style="rotate:20deg"></span><span class="scatter__stat-num">+65k</span></div>
    <div class="scatter__label">customers</div>
  </div>
</section>
```
```css
.scatter{position:relative;height:100vh;height:100dvh;overflow:hidden;background:#000;color:#fff}
.scatter__bg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.scatter h1{margin:0;font:inherit}
.scatter__w{position:absolute;margin:0;font-size:14vw;font-weight:500;line-height:.95;letter-spacing:-.04em}
.scatter__w--1{left:16px;top:18%}.scatter__w--2{right:16px;top:38%}.scatter__w--3{left:18%;top:58%}
.scatter__note{position:absolute;left:24px;top:46%;max-width:240px;font-size:15px;line-height:1.375;color:rgba(255,255,255,.9)}
.scatter__stat{position:absolute}
.scatter__stat-row{display:flex;align-items:center;gap:12px}
.scatter__stat-num{font-size:clamp(36px,4vw,48px);font-weight:500;letter-spacing:-.025em}
.scatter__rule{display:none;width:96px;height:1px;background:rgba(255,255,255,.4)}
.scatter__label{margin-top:4px;font-size:14px;color:rgba(255,255,255,.7)}
@media (min-width:768px){.scatter__w{font-size:13vw}.scatter__w--1{left:40px}.scatter__w--2{right:40px}.scatter__w--3{left:28%}.scatter__rule{display:block}}
```

**Mobile:** retest the subject/word overlap at 375 px; clip the root with `overflow-x:clip` so vw type never causes horizontal scroll.

---

## 12. Geometric SVG wordmark assembly

**What / when:** A full-width wordmark drawn from flat polygons (verticals, diagonals, crossbars). On load each polygon slides up from below the SVG's edge in a quick cascade while the whole mark settles from a 3 % zoom, like type being set in metal. Ideal for museum, institution or studio headers.

**Premium parameters:** each block `translateY(120 user units) → 0` + fade, **1.2 s** `--ease-out-expo`, stagger **60 ms** after 100 ms; parent `scale(1.03 → 1)` 1.4 s; stroke weight 14 units on a 100-unit cap height; letter gap ~66 units; fill `#111` on `#fcfcfc`.

**Implementation**
```html
<h1 class="wm" aria-label="NH"><!-- set aria-label to the real word -->
  <svg viewBox="0 0 494 100" aria-hidden="true" focusable="false">
    <g>                                     <!-- N -->
      <polygon style="--i:0" points="0,0 14,0 14,100 0,100"/>
      <polygon style="--i:1" points="200,0 214,0 214,100 200,100"/>
      <polygon style="--i:2" points="0,0 33,0 214,100 181,100"/>
    </g>
    <g transform="translate(280,0)">        <!-- H -->
      <polygon style="--i:3" points="0,0 14,0 14,100 0,100"/>
      <polygon style="--i:4" points="200,0 214,0 214,100 200,100"/>
      <polygon style="--i:5" points="14,43 200,43 200,57 14,57"/>
    </g>
  </svg>
</h1>
```
```css
.wm{margin:0}
.wm svg{display:block;width:100%;height:auto;fill:#111;overflow:hidden;animation:wm-settle 1.4s var(--ease-out-expo) both}
.wm polygon{animation:wm-block 1.2s var(--ease-out-expo) both;animation-delay:calc(100ms + var(--i) * 60ms)}
@keyframes wm-block{from{transform:translateY(120px);opacity:0}}
@keyframes wm-settle{from{transform:scale(1.03)}to{transform:scale(1)}}
@media (prefers-reduced-motion:reduce){.wm svg,.wm polygon{animation:none}}
```
CSS `px` on SVG children equals user units, so 120 px is more than the 100-unit cap height and each block starts fully below the viewBox (the SVG clips it). Letter recipes: **M** = two verticals + two diagonals meeting at the bottom centre; **A/V** = two diagonals + optional bar.

---

## 13. Count-up statistics & counter preloader

**What / when:** Stat values roll up from zero when the row becomes visible, each slightly later and longer than the previous one (hero footers, proof bars, orbit centres). And a full-screen intro loader: a 000 → 100 counter in huge display numerals, a cycling word in italic serif and a hairline gradient progress bar, after which the hero entrance plays.

**Premium parameters**
- easeOutCubic `1 − (1 − t)³`. In a row: duration `1500 + i × 80` ms, delay `480 + i × 90` ms, so counting starts as the row's entrance lands. Single big metric: 2 s.
- IntersectionObserver threshold 0.25, once. `font-variant-numeric: tabular-nums`; fixed decimals (`99.99`); prefix/suffix (`+`, `k+`, `%`, `ms`, `/7`, `M`) outside the animated digits.
- The **final value is in the HTML**, so no-JS users, crawlers and reduced-motion users see real numbers; JS resets to 0 just before animating.
- Compact proof bar: icon glyph → value `clamp(18px, 2.2vw, 26px)` `-.025em` → muted label `clamp(11px, 1.2vw, 12.5px)` `#8e8e8e`; 4 columns → 2×2 at ≤720 px.
- Big metric: `clamp(48px, 10vw, 96px)`, weight 300, `-.04em`, lh 1; label 13–15 px at 40 % white, `margin-top:16px`; columns stagger 0.15 s.
- Loader: **2.7 s** rAF counter, `padStart(3,'0')`; numerals 60 → 128 px display serif bottom-right; words cycle every **900 ms** (y 20 → 0 → −20); eyebrow 12 px uppercase `.3em` top-left; bar **3 px**, gradient `scaleX(p)`, glow `0 0 8px rgba(accent,.35)`; hold **400 ms** at 100, fade out 0.6 s, then start the hero timeline. Skip it on repeat visits in the same session.

**Implementation**
```html
<div class="stats-grid" data-count-group>
  <div class="stat"><span class="stat-val" data-count="120" data-suffix="ms">120ms</span><span class="stat-label">Response time</span></div>
  <div class="stat"><span class="stat-val" data-count="99.99" data-decimals="2" data-suffix="%">99.99%</span><span class="stat-label">Uptime</span></div>
  <div class="stat"><span class="stat-val" data-count="2.4" data-decimals="1" data-suffix="M">2.4M</span><span class="stat-label">Active users</span></div>
</div>
```
```css
.stats-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:24px;max-width:920px;margin:0 auto;text-align:center}
.stat{display:flex;flex-direction:column;align-items:center;gap:6px}
.stat-val{font-size:clamp(18px,2.2vw,26px);letter-spacing:-.025em;color:#fff;font-variant-numeric:tabular-nums}
.stat-label{font-size:clamp(11px,1.2vw,12.5px);color:#8e8e8e}
.stat-big{font-size:clamp(48px,10vw,96px);font-weight:300;letter-spacing:-.04em;line-height:1;font-variant-numeric:tabular-nums}
@media (max-width:720px){.stats-grid{grid-template-columns:repeat(2,1fr)}}
```
```js
function countUp(el, { duration = 2000, delay = 0 } = {}) {
  const to = parseFloat(el.dataset.count), dec = +(el.dataset.decimals || 0);
  const nf = new Intl.NumberFormat('en-US', { minimumFractionDigits: dec, maximumFractionDigits: dec });
  const fmt = (v) => (el.dataset.prefix || '') + nf.format(v) + (el.dataset.suffix || '');
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) { el.textContent = fmt(to); return; }
  el.textContent = fmt(0);
  setTimeout(() => {
    const t0 = performance.now();
    requestAnimationFrame(function f(now) {
      const t = Math.min(1, (now - t0) / duration);
      el.textContent = fmt(to * (1 - Math.pow(1 - t, 3)));
      if (t < 1) requestAnimationFrame(f);
    });
  }, delay);
}
const countIO = new IntersectionObserver((entries) => entries.forEach((e) => {
  if (!e.isIntersecting) return;
  countIO.unobserve(e.target);
  if (e.target.hasAttribute('data-count-group')) {
    e.target.querySelectorAll('[data-count]').forEach((el, i) => countUp(el, { duration: 1500 + i * 80, delay: 480 + i * 90 }));
  } else countUp(e.target);
}), { threshold: 0.25 });
document.querySelectorAll('[data-count-group], [data-count]:not([data-count-group] [data-count])').forEach((el) => countIO.observe(el));
```
Counter preloader:
```html
<div class="loader" role="status" aria-label="Loading">
  <span class="loader__eyebrow">Portfolio</span>
  <span class="loader__word">Design</span>
  <span class="loader__count">000</span>
  <div class="loader__bar"><i></i></div>
</div>
```
```css
.loader{position:fixed;inset:0;z-index:9999;background:#0a0a0a;color:#f5f5f5;transition:opacity .6s ease,visibility .6s}
.loader.is-done{opacity:0;visibility:hidden}
.loader__eyebrow{position:absolute;top:32px;left:32px;font-size:12px;letter-spacing:.3em;text-transform:uppercase;color:#888}
.loader__word{position:absolute;inset:0;display:grid;place-items:center;opacity:.8;font:italic 400 clamp(2.25rem,6vw,4.5rem)/1 'Instrument Serif',serif}
.loader__count{position:absolute;right:32px;bottom:40px;font:400 clamp(3.75rem,10vw,8rem)/1 'Instrument Serif',serif;font-variant-numeric:tabular-nums}
.loader__bar{position:absolute;left:0;right:0;bottom:0;height:3px;background:rgba(31,31,31,.5)}
.loader__bar i{display:block;height:100%;transform-origin:left;transform:scaleX(0);
  background:linear-gradient(90deg,#89AACC,#4E85BF);box-shadow:0 0 8px rgba(137,170,204,.35)}
```
```js
function swapWord(el, text) {                         // exit up, enter from below
  const out = el.animate([{ opacity: 1, transform: 'translateY(0)' }, { opacity: 0, transform: 'translateY(-20px)' }],
    { duration: 250, easing: 'ease-in', fill: 'forwards' });
  out.onfinish = () => {
    el.textContent = text; out.cancel();
    el.animate([{ opacity: 0, transform: 'translateY(20px)' }, { opacity: 1, transform: 'translateY(0)' }],
      { duration: 350, easing: 'cubic-bezier(.16,1,.3,1)' });
  };
}
function runLoader(onDone, { duration = 2700, words = ['Design', 'Create', 'Inspire'], every = 900 } = {}) {
  const el = document.querySelector('.loader');
  const count = el.querySelector('.loader__count'), bar = el.querySelector('.loader__bar i'), word = el.querySelector('.loader__word');
  const finish = () => { el.classList.add('is-done'); onDone && onDone(); setTimeout(() => el.remove(), 700); };
  let seen = false;
  try { seen = sessionStorage.getItem('intro-seen') === '1'; sessionStorage.setItem('intro-seen', '1'); } catch {}
  if (seen || matchMedia('(prefers-reduced-motion: reduce)').matches) return finish();
  let w = 0;
  const wid = setInterval(() => { w = (w + 1) % words.length; swapWord(word, words[w]); }, every);
  const t0 = performance.now();
  requestAnimationFrame(function f(now) {
    const p = Math.min(1, (now - t0) / duration);
    count.textContent = String(Math.round(p * 100)).padStart(3, '0');
    bar.style.transform = `scaleX(${p})`;
    if (p < 1) requestAnimationFrame(f);
    else { clearInterval(wid); setTimeout(finish, 400); }
  });
}
runLoader(() => document.documentElement.classList.add('hero-go'));   // start the hero entrance from here
```
Gate hero entrances on `.hero-go` (e.g. `.hero-go .in-blur{animation-play-state:running}`) so they play after the loader, not behind it.

---

## Surfaces, Liquid Glass & Button Physics

# Surfaces & buttons

Materials (glass, frost, grain) and the button and card finishes built on them.

**Conventions.** Single-file, no build step, `*,*::before,*::after{box-sizing:border-box}`, dark page unless stated. Shared tokens (paste once):
```css
:root{
  --ease-out-expo:cubic-bezier(.16,1,.3,1);
  --ease-out-quint:cubic-bezier(.22,1,.36,1);
  --ease-standard:cubic-bezier(.25,.1,.25,1);
}
```
Always keep the `-webkit-` prefixes shown (`backdrop-filter`, `mask`, `mask-composite`, `background-clip`).

---

## 1. Liquid-glass surface (gradient hairline rim)

**What / when:** An almost-invisible frosted surface whose "edge" is a gradient hairline: bright at the top and bottom, fading to nothing at the sides, like light catching the rim of a lens. The signature chrome for UI floating over cinematic video: nav pills, logo discs, badges, secondary CTAs, email inputs, stat and feature cards. It replaces borders completely. Pair it with **one** solid white primary button.

**Premium parameters**
- Fill `rgba(255,255,255,.01)` + `background-blend-mode: luminosity`. The look comes from the blur and the rim, not the fill.
- **Subtle tier** (nav, chips, cards): `blur(4px)` (heavier blur kills the glass read on small chips), `inset 0 1px 1px rgba(255,255,255,.1)`, rim stops `.45 / .15 / 0 / 0 / .15 / .45` at `0 / 20 / 40 / 60 / 80 / 100 %`.
- **Strong tier** (primary glass CTA, big panels): `blur(50px)`, `4px 4px 4px rgba(0,0,0,.05), inset 0 1px 1px rgba(255,255,255,.15)`, rim `.5 / .2 / 0 / 0 / .2 / .5`. For menus and sheets you can drop the rim.
- **Dark tier** (bright footage): fill `rgba(0,0,0,.4)`, rim `.3 / .1 / 0 / 0 / .1 / .3`.
- Rim 1.4 px, drawn on `::before` with padding plus mask compositing (content-box XOR border-box). No `border` anywhere; `border-radius: inherit` on the pseudo-element.
- Sizes: 48×48 logo disc; nav pill `padding 6px` with `8px 12px` 14 px links; pills `10px 24px`; 40×40 icon circles; stat cards `p 20px, w 220px, radius 1.25rem`; feature cards `p 24px, min-h 360px, radius 1.25rem` with a nested 44×44 icon tile (radius .75rem); tags `4px 12px`, 11 px. Hover `scale(1.03)`.
- On a flat black background glass reads only as a hairline outline: it needs moving footage behind it.

**Implementation**
```css
.liquid-glass{position:relative;overflow:hidden;border:none;
  background:rgba(255,255,255,.01);background-blend-mode:luminosity;
  -webkit-backdrop-filter:blur(4px);backdrop-filter:blur(4px);
  box-shadow:inset 0 1px 1px rgba(255,255,255,.1)}
.liquid-glass::before{content:"";position:absolute;inset:0;border-radius:inherit;padding:1.4px;pointer-events:none;
  background:linear-gradient(180deg,
    rgba(255,255,255,var(--rim-a,.45)) 0%,rgba(255,255,255,var(--rim-b,.15)) 20%,
    rgba(255,255,255,0) 40%,rgba(255,255,255,0) 60%,
    rgba(255,255,255,var(--rim-b,.15)) 80%,rgba(255,255,255,var(--rim-a,.45)) 100%);
  -webkit-mask:linear-gradient(#fff 0 0) content-box,linear-gradient(#fff 0 0);
  -webkit-mask-composite:xor;          /* Chrome/Safari legacy keyword */
          mask:linear-gradient(#fff 0 0) content-box,linear-gradient(#fff 0 0);
          mask-composite:exclude}      /* standard */
.liquid-glass--strong{-webkit-backdrop-filter:blur(50px);backdrop-filter:blur(50px);
  box-shadow:4px 4px 4px rgba(0,0,0,.05),inset 0 1px 1px rgba(255,255,255,.15)}
.liquid-glass--strong::before{--rim-a:.5;--rim-b:.2}
.liquid-glass--dark{background:rgba(0,0,0,.4)}
.liquid-glass--dark::before{--rim-a:.3;--rim-b:.1}
.liquid-glass--norim::before{content:none}
@supports not ((backdrop-filter:blur(1px)) or (-webkit-backdrop-filter:blur(1px))){
  .liquid-glass{background:rgba(255,255,255,.08)}}
```
Keep the exact three-line mask form: it is the cross-browser-safe one. The rim covers the element, but the mask removes its content box, so only the 1.4 px ring paints and clicks pass through.

Applications:
```html
<!-- Announcement badge with an inner chip -->
<div class="liquid-glass" style="display:inline-flex;align-items:center;gap:8px;border-radius:999px;padding:4px 12px 4px 4px">
  <span style="background:#fff;color:#000;border-radius:999px;padding:4px 12px;font:600 12px/1 system-ui">New</span>
  <span style="font-size:14px;color:rgb(255 255 255/.9)">Announcing something worth reading</span>
</div>

<!-- Email capture pill, submit inside -->
<form class="liquid-glass" style="display:flex;align-items:center;gap:12px;border-radius:999px;padding:8px 8px 8px 24px;max-width:36rem">
  <input type="email" placeholder="Enter your email" aria-label="Email" style="flex:1;min-width:0;background:transparent;border:0;outline:0;color:#fff;font-size:16px">
  <button style="background:#fff;color:#000;border:0;border-radius:999px;padding:12px 28px;font-weight:500">Join</button>
</form>

<!-- Capability card: nested icon tile, right-aligned tags, flex spacer, serif-italic title -->
<article class="liquid-glass" style="border-radius:1.25rem;padding:24px;min-height:360px;display:flex;flex-direction:column">
  <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:16px">
    <span class="liquid-glass" style="width:44px;height:44px;border-radius:.75rem;display:grid;place-items:center"><!-- svg --></span>
    <div style="display:flex;flex-wrap:wrap;justify-content:flex-end;gap:6px;max-width:70%">
      <span class="liquid-glass" style="border-radius:999px;padding:4px 12px;font-size:11px;white-space:nowrap">Tag one</span>
    </div>
  </div>
  <div style="flex:1"></div>
  <h3 style="font:italic 400 clamp(30px,3vw,36px)/1 'Instrument Serif',serif;letter-spacing:-1px">Card title</h3>
  <p style="margin-top:12px;font-size:14px;font-weight:300;line-height:1.35;max-width:32ch;color:rgb(255 255 255/.9)">Short supporting sentence.</p>
</article>
```

**Light-surface sibling ("frosted white"):** on bright footage use `background: rgb(255 255 255/.7); backdrop-filter: blur(12px); border: 1px solid rgb(255 255 255/.6); box-shadow: 0 1px 2px rgb(0 0 0/.05)`. A floating dock uses `.9` alpha, `blur(40px)` and `0 12px 40px rgba(0,0,0,.08)`.

**Perf:** `backdrop-filter` re-samples the moving video every frame. Use at most a few large `blur(50px)` surfaces; use the 4 px tier for repeated chips.

---

## 2. Frosted glass UI kit over video (chips, accent badge, numbered panel, contact card)

**What / when:** A consistent token set for an editorial page over moving footage: frosted chips, a left-accent label badge, a frosted list panel with numbered rows, and a "talk to a human" contact card. Heavier frost than liquid glass: use it where text *on* the glass must be legible.

**Premium parameters**
- Frost `rgba(255,255,255,.15)` (small chips) / `.10` (large panels), `blur(12px)`, border `1px rgba(255,255,255,.15–.25)`.
- Dark frosted pill (bright footage): `rgba(23,23,23,.9)` + `blur(8px)`; bright frosted pill: `rgba(255,255,255,.2)` + `blur(12px)` + border `rgba(255,255,255,.3)`.
- Left-accent badge: `border-left: 2px solid #fff`, `padding 6px 12px`, mono 11 px uppercase, tracking `.15em`.
- Text over video: white + layered `drop-shadow` (no box); mono labels 10–12 px, `.15em`, 55–60 % white.
- Numbered rows: mono index 11 px at 55 %; title 16–18 px medium; body 14 px at 70 %; dividers `rgba(255,255,255,.15)`; row padding 20 px; chevron nudges 2 px right on hover.
- Contact card: radius 12 px, padding 12 px, portrait **80×96** radius 8 px, name 14 px medium, role mono 10 px, mini white pill CTA 12 px with chevron.

**Implementation**
```css
.frost{background:rgba(255,255,255,.15);-webkit-backdrop-filter:blur(12px);backdrop-filter:blur(12px)}
.frost--panel{background:rgba(255,255,255,.10);border:1px solid rgba(255,255,255,.15);border-radius:16px}
.frost--dark{background:rgba(23,23,23,.9);-webkit-backdrop-filter:blur(8px);backdrop-filter:blur(8px)}
.on-video{color:#fff;filter:drop-shadow(0 4px 3px rgba(0,0,0,.07)) drop-shadow(0 2px 2px rgba(0,0,0,.06))}
.on-video--lg{filter:drop-shadow(0 10px 8px rgba(0,0,0,.04)) drop-shadow(0 4px 3px rgba(0,0,0,.1))}
.mono-label{font:500 11px/1.2 ui-monospace,'JetBrains Mono',monospace;text-transform:uppercase;letter-spacing:.15em}
.accent-badge{display:inline-block;border-left:2px solid #fff;padding:6px 12px;
  background:rgba(255,255,255,.15);-webkit-backdrop-filter:blur(12px);backdrop-filter:blur(12px)}
.rows{max-width:28rem;padding:0 24px}
.row{display:flex;gap:20px;padding:20px 0;border-bottom:1px solid rgba(255,255,255,.15)}
.row:last-child{border-bottom:0}
.row__idx{font:11px/1.6 ui-monospace,monospace;letter-spacing:.15em;color:rgba(255,255,255,.55)}
.row__title{display:flex;align-items:center;gap:6px;font-size:18px;font-weight:500}
.row__title svg{color:rgba(255,255,255,.4);transition:transform .3s,color .3s}
.row:hover .row__title svg{transform:translateX(2px);color:#fff}
.row__body{margin-top:6px;font-size:14px;line-height:1.6;color:rgba(255,255,255,.7)}
.contact-card{display:flex;align-items:center;gap:16px;padding:12px;border-radius:12px}
.contact-card img{width:80px;height:96px;border-radius:8px;object-fit:cover}
.contact-card .cta{margin-top:6px;display:inline-flex;align-items:center;gap:4px;border-radius:999px;background:#fff;color:#000;
  padding:8px 16px;font-size:12px;font-weight:500;transition:background .3s}
.contact-card .cta:hover{background:rgba(255,255,255,.85)}
```
```html
<span class="accent-badge mono-label">Short proof statement</span>
<div class="frost frost--panel rows">
  <div class="row"><span class="row__idx">01</span><div>
    <div class="row__title">Capability <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m9 18 6-6-6-6"/></svg></div>
    <p class="row__body">One-line explanation.</p></div></div>
  <!-- 02, 03 … -->
</div>
<div class="frost contact-card">
  <img src="portrait.jpg" alt="Team member">
  <div><div style="font-size:14px;font-weight:500">Name Surname</div><div class="mono-label" style="font-size:10px;opacity:.6">Role</div>
    <a class="cta" href="#contact">Book a call ›</a></div>
</div>
```

---

## 3. Premium button finishes (liquid-metal + sweep shine, halo pill, jewel pill)

**What / when:** Finishes that make a CTA feel machined rather than flat. **(a) Liquid-metal** brushed gradients with a light sweep on hover, for monochrome or tech brands. **(b) Halo-glow white pill**, the single bright object on a dark video. **(c) Jewel-gradient pill**, saturated multi-stop gradient with inner shadow and an inset white ring, for creator or portfolio pages.

**Premium parameters**
- **Sweep shine:** a 115° band `transparent 20–30 % → rgba(255,255,255,.16–.45) ~50 % → transparent 70–76 %`, from `translateX(-120…-130%)` to `+120…130%` over 0.6–0.65 s ease on hover. `isolation:isolate` + `z-index:-1` makes it pass between the fill and the label.
- **Chrome solid:** `linear-gradient(180deg,#fff 0%,#e7e7e7 48%,#cfcfcf 100%)`, text `#111`, `1px solid #fff`, `inset 0 1px 0 rgba(255,255,255,.95)`. Hover `#fff → #f3f6ff 42% → #d5def2` with glow `0 0 22px rgba(186,208,255,.35), 0 8px 18px rgba(255,255,255,.12)`.
- **Frosted ghost:** `linear-gradient(135deg, rgba(255,255,255,.12), rgba(0,0,0,.5) 46%, rgba(150,170,200,.1))`, `1px solid rgba(198,198,198,.55)`, `blur(16px)`. Hover border `rgba(220,230,255,.8)`, glow `0 0 24px rgba(170,200,255,.28)`.
- **Metal nav tab:** `linear-gradient(105deg,#050505 0%,#2a2a2a 48%,#4a4a4a 100%)`, `1px solid rgba(198,198,198,.55)`, radius 7 px, height 40 px, padding 0 18 px. Hover `#111 → #3a3a3a 45% → #6a6a6a`, border `rgba(235,235,235,.9)`, glow `0 0 18px rgba(200,210,230,.18)`.
- **Metal badge:** `linear-gradient(90deg,#7d7d7d 0%,#2a2a2a 52%,#0a0a0a 100%)`, radius 5 px, padding 9×15 px, a 4-point sparkle icon with `drop-shadow(0 0 3px rgba(255,255,255,.45))`.
- Geometry: height 40–42 px, radius 6 px (crisp) or 999 px (pill), weight 500, `letter-spacing:-.02em`, `line-height:1`, 0.35 s transitions on background, border, shadow, colour, filter.
- **Halo pill:** white, black text, weight 600, `0 0 0 1px rgba(255,255,255,.15), 0 0 22px rgba(255,255,255,.32), 0 0 44px rgba(255,255,255,.12)`; hover `translateY(-2px) scale(1.02)` with a stronger glow.
- **Jewel pill:** `linear-gradient(123deg,#18011F 7%,#B600A8 37%,#7621B0 72%,#BE4C00 100%)` (near-black → magenta → violet → burnt orange), `0 4px 4px rgba(181,1,167,.25), inset 4px 4px 12px #7721B1`, `outline: 2px solid #fff; outline-offset: -3px`, uppercase, wide tracking.
- Icon nudge: arrow-up-right `translate(2px,-2px)`, chevron `+1px` x. Press `scale(.98)`.

**Implementation**
```css
.btn{position:relative;isolation:isolate;overflow:hidden;display:inline-flex;align-items:center;justify-content:center;gap:8px;
  height:42px;padding:0 18px;border-radius:6px;font:500 14px/1 Inter,system-ui,sans-serif;letter-spacing:-.02em;white-space:nowrap;
  cursor:pointer;text-decoration:none;
  transition:background .35s ease,border-color .35s ease,box-shadow .35s ease,color .35s ease,transform .2s ease}
.btn::after{content:"";position:absolute;inset:0;z-index:-1;pointer-events:none;
  background:linear-gradient(115deg,transparent 20%,rgba(255,255,255,.45) 48%,transparent 76%);
  transform:translateX(-130%);transition:transform .65s ease}
.btn:hover::after{transform:translateX(130%)}
.btn:active{transform:scale(.98)}
.btn--chrome{color:#111;border:1px solid #fff;background:linear-gradient(180deg,#fff 0%,#e7e7e7 48%,#cfcfcf 100%);
  box-shadow:inset 0 1px 0 rgba(255,255,255,.95)}
.btn--chrome:hover{border-color:#f2f6ff;background:linear-gradient(180deg,#fff 0%,#f3f6ff 42%,#d5def2 100%);
  box-shadow:inset 0 1px 0 #fff,0 0 22px rgba(186,208,255,.35),0 8px 18px rgba(255,255,255,.12)}
.btn--ghost{color:#fff;border:1px solid rgba(198,198,198,.55);
  background:linear-gradient(135deg,rgba(255,255,255,.12),rgba(0,0,0,.5) 46%,rgba(150,170,200,.1));
  -webkit-backdrop-filter:blur(16px);backdrop-filter:blur(16px);box-shadow:inset 0 1px 0 rgba(255,255,255,.12)}
.btn--ghost:hover{border-color:rgba(220,230,255,.8);box-shadow:inset 0 1px 0 rgba(255,255,255,.22),0 0 24px rgba(170,200,255,.28)}
.btn .icon{transition:transform .25s ease}
.btn:hover .icon{transform:translate(2px,-2px)}

.tab-metal{position:relative;overflow:hidden;display:inline-flex;align-items:center;height:40px;padding:0 18px;border-radius:7px;
  color:#f3f3f3;font-size:14px;letter-spacing:-.01em;border:1px solid rgba(198,198,198,.55);
  background:linear-gradient(105deg,#050505 0%,#2a2a2a 48%,#4a4a4a 100%);
  transition:background .35s ease,border-color .35s ease,box-shadow .35s ease}
.tab-metal::before{content:"";position:absolute;inset:0;pointer-events:none;
  background:linear-gradient(115deg,transparent 30%,rgba(255,255,255,.16) 50%,transparent 70%);
  transform:translateX(-120%);transition:transform .6s ease}
.tab-metal:hover{border-color:rgba(235,235,235,.9);background:linear-gradient(105deg,#111 0%,#3a3a3a 45%,#6a6a6a 100%);box-shadow:0 0 18px rgba(200,210,230,.18)}
.tab-metal:hover::before{transform:translateX(120%)}

.btn-halo{display:inline-flex;align-items:center;border-radius:999px;background:#fff;color:#000;font:600 14.5px/1 Inter,sans-serif;
  padding:13px 28px;border:0;cursor:pointer;
  box-shadow:0 0 0 1px rgba(255,255,255,.15),0 0 22px rgba(255,255,255,.32),0 0 44px rgba(255,255,255,.12);
  transition:transform .3s cubic-bezier(.22,1,.36,1),box-shadow .3s ease}
.btn-halo:hover{transform:translateY(-2px) scale(1.02);
  box-shadow:0 0 0 1px rgba(255,255,255,.25),0 0 30px rgba(255,255,255,.45),0 0 64px rgba(255,255,255,.18)}

.btn-jewel{display:inline-flex;align-items:center;border-radius:999px;border:0;color:#fff;cursor:pointer;
  padding:16px 48px;font:500 16px/1 system-ui,sans-serif;text-transform:uppercase;letter-spacing:.1em;
  background:linear-gradient(123deg,#18011F 7%,#B600A8 37%,#7621B0 72%,#BE4C00 100%);
  box-shadow:0 4px 4px rgba(181,1,167,.25),inset 4px 4px 12px #7721B1;
  outline:2px solid #fff;outline-offset:-3px;transition:transform .2s ease,filter .2s ease}
.btn-jewel:hover{transform:translateY(-1px);filter:brightness(1.08)}
.btn-jewel:focus-visible{outline-width:3px}
@media (prefers-reduced-motion:reduce){.btn::after,.tab-metal::before{transition:none}}
```

---

## 4. Text-roll button with rotating arrow chip

**What / when:** The label is stacked twice in a 20 px-tall window; on hover the stack slides up so a fresh copy rolls in from below, while an arrow in a circular chip at the right edge rotates. Tiny, tactile, unmistakably "studio". Use it for primary and nav CTAs.

**Premium parameters**
- Window height = line-height = **20 px**; roll `translateY(-50%)` **500 ms** `--ease-standard`.
- Asymmetric padding `8px 8px 8px 20–24px` so the chip hugs the right edge; chip 24 px (nav) / 28–32 px (hero), white with the button colour as the arrow colour.
- Arrow `rotate(-45deg)` on hover (→ becomes ↗), same duration and easing.
- Colours: one accent (e.g. orange `#F26522`, hover `#e05a1a`) or near-black `#111` with a white chip. Cream-pill variant: black chip 36–40 px, hover gap `8 → 12px`, chip `scale(1.1)`.
- Text arrows (`→`) in links nudge `translateX(2px)` over 200 ms.

**Implementation**
```html
<a class="btn-roll" href="#">
  <span class="btn-roll__label"><span class="btn-roll__inner">
    <span>Start a project</span><span aria-hidden="true">Start a project</span>
  </span></span>
  <span class="btn-roll__chip" aria-hidden="true">
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
  </span>
</a>
```
```css
.btn-roll{display:inline-flex;align-items:center;gap:12px;padding:8px 8px 8px 24px;border-radius:999px;background:#F26522;color:#fff;
  font:500 14px/20px system-ui,-apple-system,sans-serif;text-decoration:none;transition:background-color .3s}
.btn-roll:hover{background:#e05a1a}
.btn-roll__label{display:block;height:20px;overflow:hidden}
.btn-roll__inner{display:flex;flex-direction:column;transition:transform .5s var(--ease-standard)}
.btn-roll__inner>span{display:block;height:20px;white-space:nowrap}
.btn-roll:hover .btn-roll__inner,.btn-roll:focus-visible .btn-roll__inner{transform:translateY(-50%)}
.btn-roll__chip{width:32px;height:32px;border-radius:999px;background:#fff;color:#F26522;display:grid;place-items:center;flex:none}
.btn-roll__chip svg{transition:transform .5s var(--ease-standard)}
.btn-roll:hover .btn-roll__chip svg,.btn-roll:focus-visible .btn-roll__chip svg{transform:rotate(-45deg)}
.btn-roll--dark{background:#111;font-size:13px;padding-left:20px}
.btn-roll--dark .btn-roll__chip{width:24px;height:24px;color:#111}
@media (prefers-reduced-motion:reduce){.btn-roll__inner,.btn-roll__chip svg{transition:none}}
```

---

## 5. Sliding-fill buttons (+ hard offset shadow)

**What / when:** On hover a colour panel wipes across the button from one side and the label inverts above it. Two flavours: a fast accent wipe on a dark pill, and a slow paper-white wipe on a near-black button with a playful icon tilt and a hard offset shadow (editorial / museum feel).

**Premium parameters**
- Accent wipe: `::after` `translateX(-100%) → 0`, **0.4 s** `--ease-out-quint`; paired buttons wipe from opposite sides. Pill `border-radius 50px`, `padding 12px 26px`, 15 px / 500.
- Paper wipe: panel `translateX(-101%) → 0`, **700 ms** `--ease-out-expo`; label colour flips; icon `scale(1.1) rotate(-12deg) translateY(-4px)`; the button lifts `translateY(-2px)` and gains `box-shadow: 3px 3px 0 rgba(17,17,17,.5)`; `:active` resets lift and shadow. A 1 px border in the dark colour keeps the edge crisp under the light panel.
- `isolation:isolate` + `z-index:-1` paints the panel above the button background and below the label, with no extra wrappers.

**Implementation**
```html
<a class="btn-fill" href="#"><span>Join now</span></a>
<a class="btn-fill btn-fill--from-right" href="#"><span>Start project</span></a>
<a class="btn-paper" href="#"><svg class="btn-paper__icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M7 17 17 7M8 7h9v9"/></svg><span>Explore now</span></a>
```
```css
.btn-fill{position:relative;display:inline-flex;align-items:center;gap:8px;overflow:hidden;isolation:isolate;
  border-radius:50px;padding:12px 26px;background:#000;color:#fff;font:500 15px/1 Inter,sans-serif;text-decoration:none}
.btn-fill::after{content:"";position:absolute;inset:0;z-index:-1;background:var(--fill,#A068FF);
  transform:translateX(-100%);transition:transform .4s var(--ease-out-quint)}
.btn-fill--from-right::after{transform:translateX(100%)}
.btn-fill:hover::after,.btn-fill:focus-visible::after{transform:translateX(0)}

.btn-paper{position:relative;display:inline-flex;align-items:center;gap:10px;overflow:hidden;isolation:isolate;
  padding:14px 24px;border:1px solid #1a1a1a;border-radius:6px;background:#1a1a1a;color:#fff;font:500 15px/1 Inter,sans-serif;
  text-decoration:none;box-shadow:0 1px 2px rgba(0,0,0,.05);
  transition:transform .3s var(--ease-out-expo),box-shadow .3s var(--ease-out-expo),color .7s var(--ease-out-expo)}
.btn-paper::before{content:"";position:absolute;inset:0;z-index:-1;background:#fcfcfc;transform:translateX(-101%);
  transition:transform .7s var(--ease-out-expo)}
.btn-paper:hover{color:#111;transform:translateY(-2px);box-shadow:3px 3px 0 rgba(17,17,17,.5)}
.btn-paper:hover::before{transform:translateX(0)}
.btn-paper:active{transform:none;box-shadow:none}
.btn-paper__icon{width:18px;height:18px;transition:transform .7s var(--ease-out-expo)}
.btn-paper:hover .btn-paper__icon{transform:scale(1.1) rotate(-12deg) translateY(-4px)}
@media (prefers-reduced-motion:reduce){.btn-fill::after,.btn-paper,.btn-paper::before,.btn-paper__icon{transition-duration:.01s}}
```

---

## 6. Animated gradient border ring (@property conic spin · hover ring)

**What / when:** A thin conic-gradient border that endlessly travels around a pill (draws the eye to the one CTA that matters), and a calmer variant where a gradient ring appears only on hover.

**Premium parameters**
- Spinning ring: `inset:-3px; padding:3px`, `conic-gradient(from var(--border-angle), accent, deep, accent, deep, accent)` (e.g. `#A068FF / #070319`), **3 s linear infinite** via a registered `@property`.
- Hover ring: `inset:-2px`, `linear-gradient(90deg, #89AACC, #4E85BF)` fading in over 0.3 s, background-position drifting over **6 s**; the inner surface keeps the page colour; the button scales 1.05 on hover.
- Logo variant: 36 px circle with a 2 px gradient ring, `scale(1.1)` on hover with the gradient direction reversed.
- `@property` works in Chrome/Edge 85+, Safari 16.4+, Firefox 128+; elsewhere the ring renders static, an acceptable fallback.

**Implementation**
```html
<span class="ring-spin"><a class="btn-fill" href="#"><span>Join now</span></a></span>
<a class="ring-hover" href="#"><span>See works</span></a>
```
```css
@property --border-angle{syntax:'<angle>';inherits:false;initial-value:0deg}
.ring-spin{position:relative;display:inline-block;border-radius:50px}
.ring-spin::before{content:"";position:absolute;inset:-3px;padding:3px;border-radius:inherit;pointer-events:none;
  background:conic-gradient(from var(--border-angle),#A068FF,#070319,#A068FF,#070319,#A068FF);
  -webkit-mask:linear-gradient(#fff 0 0) content-box,linear-gradient(#fff 0 0);
  -webkit-mask-composite:xor;mask:linear-gradient(#fff 0 0) content-box,linear-gradient(#fff 0 0);mask-composite:exclude;
  animation:border-spin 3s linear infinite}
@keyframes border-spin{to{--border-angle:360deg}}

.ring-hover{position:relative;display:inline-block;border-radius:999px;isolation:isolate;text-decoration:none;transition:transform .3s var(--ease-out-expo)}
.ring-hover::before{content:"";position:absolute;inset:-2px;border-radius:inherit;z-index:-1;opacity:0;
  background:linear-gradient(90deg,#89AACC,#4E85BF,#89AACC);background-size:200% 100%;
  transition:opacity .3s;animation:gradient-shift 6s ease infinite}
.ring-hover>span{display:block;border-radius:inherit;padding:14px 28px;background:#141414;color:#f5f5f5;font-size:14px}
.ring-hover:hover{transform:scale(1.05)}
.ring-hover:hover::before,.ring-hover:focus-visible::before{opacity:1}
@keyframes gradient-shift{0%,100%{background-position:0% 50%}50%{background-position:100% 50%}}
@media (prefers-reduced-motion:reduce){.ring-spin::before,.ring-hover::before{animation:none}}
```

---

## 7. Media card hover: icon-to-label pill, zoom, frosted veil

**What / when:** Case-study cards with muted autoplay video or images. On hover a small circular icon in the corner stretches into a labelled pill ("View case study"), the media zooms 5 %, and (bento variant) a frosted veil fades over the image with a centred label. Clean at rest, expressive on hover.

**Premium parameters**
- Pill: 36×36 circle → width **148–168 px**, `width .3s ease-in-out`; label fades in with a **100 ms** delay; icon `rotate(-45deg) → 0`. Light pill on dark media, dark (`#111`) on light media.
- Media: `aspect-ratio` per card (e.g. `329/246`, `1/1`), radius 16 px, a placeholder background close to the media's average colour; zoom `scale(1.05)` over 0.7 s expo.
- Below the card: description 13–14 px grey, title 14–15 px semibold, `margin-top 16px / 4px`.
- Bento variant: 12-column grid, spans **7/5/5/7**, cards radius 24 px with a 1 px stroke; a halftone overlay (technique 8) at 20 %; hover veil `rgba(10,10,10,.7)` + `blur(16px)`; white label pill with a gradient ring, "View — *Title*" (title in italic serif).

**Implementation**
```html
<a class="mcard" href="#">
  <div class="mcard__media" style="aspect-ratio:329/246;background:#1a1d2e">
    <video src="case.mp4" autoplay muted loop playsinline></video>
    <span class="mcard__pill"><span class="mcard__label">View case study</span>
      <svg class="mcard__icon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
    </span>
  </div>
  <p class="mcard__desc">One-line outcome of the project.</p>
  <h3 class="mcard__title">Project name</h3>
</a>
```
```css
.mcard{display:block;color:inherit;text-decoration:none}
.mcard__media{position:relative;border-radius:16px;overflow:hidden}
.mcard__media video,.mcard__media img{display:block;width:100%;height:100%;object-fit:cover;transition:transform .7s var(--ease-out-expo)}
.mcard:hover .mcard__media video,.mcard:hover .mcard__media img{transform:scale(1.05)}
.mcard__pill{position:absolute;left:16px;bottom:16px;height:36px;width:36px;border-radius:999px;background:#fff;color:#111;
  display:flex;align-items:center;justify-content:flex-end;overflow:hidden;white-space:nowrap;transition:width .3s ease-in-out}
.mcard:hover .mcard__pill,.mcard:focus-visible .mcard__pill{width:148px}
.mcard__label{position:absolute;left:16px;top:50%;translate:0 -50%;font:500 13px/1 Inter,sans-serif;opacity:0;transition:opacity .2s ease}
.mcard:hover .mcard__label,.mcard:focus-visible .mcard__label{opacity:1;transition-delay:.1s}
.mcard__icon{flex:none;width:36px;transform:rotate(-45deg);transition:transform .3s ease-in-out}
.mcard:hover .mcard__icon,.mcard:focus-visible .mcard__icon{transform:none}
.mcard__desc{margin:16px 0 0;font-size:14px;line-height:1.6;color:#4b5563}
.mcard__title{margin:4px 0 0;font-size:15px;font-weight:600;color:#111}
/* bento variant */
.bento{display:grid;grid-template-columns:repeat(12,1fr);gap:24px}
.bento>*:nth-child(4n+1),.bento>*:nth-child(4n+4){grid-column:span 7}
.bento>*:nth-child(4n+2),.bento>*:nth-child(4n+3){grid-column:span 5}
@media (max-width:767px){.bento>*{grid-column:1 / -1}}
.bcard{position:relative;border:1px solid #1f1f1f;border-radius:24px;overflow:hidden;background:#141414}
.bcard__veil{position:absolute;inset:0;display:grid;place-items:center;background:rgba(10,10,10,.7);
  -webkit-backdrop-filter:blur(16px);backdrop-filter:blur(16px);opacity:0;transition:opacity .4s ease}
.bcard:hover .bcard__veil,.bcard:focus-within .bcard__veil{opacity:1}
@media (hover:none){.mcard__pill{width:148px}.mcard__label{opacity:1}}   /* touch: show the affordance */
```

**Perf:** many autoplaying card videos add up; pause off-screen ones with an IntersectionObserver.

---

## 8. Texture overlays: film grain, noise inside type, halftone, dot grid

**What / when:** A barely-there texture that kills the "flat digital" look of video, solid colour fields and gradients, and removes compression banding: a fixed page-wide grain, fractal noise blended over a hero video, an animated grain, noise *inside* glyphs for poster type, a halftone screen over project images, a faint dot grid behind tech heroes.

**Premium parameters**
- Page grain: `feTurbulence fractalNoise baseFrequency .9 numOctaves 4 stitchTiles stitch`, rect opacity `.08` inside the SVG × layer opacity `.4` (≈ 3 % effective), 200 px tile, fixed, `z-index` 50–100 above content, `pointer-events:none`. UI that must stay crisp (nav) may sit above it.
- Video grain: `baseFrequency .85 numOctaves 3`, `opacity .7`, `mix-blend-mode: overlay` (shows in mid-tones, vanishes on pure black/white, exactly where banding lives). Section noise: `.9 / 4 octaves`, `opacity .15`.
- Animated grain: oversized noise tile jittered with `steps(6)` over 1 s at ~`.08`. Shader-grade grain strength ≈ 0.05.
- Text noise (multiply): `baseFrequency .9, numOctaves 2`, alpha `.35`, composite `in` SourceGraphic. Watermark noise (overlay): `baseFrequency .5`, `feFuncA slope .075`.
- Halftone: `radial-gradient(circle, #000 1px, transparent 1px)` at **4×4 px**, `opacity .2`, `multiply`. Dot grid: `radial-gradient(#fff 1px, transparent 1px)` at **24×24 px**, `opacity .05`.

**Implementation**
```html
<div class="page-grain" aria-hidden="true"></div>
```
```css
:root{
  --noise-a:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='240' height='240'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
  --noise-b:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='240' height='240'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
}
/* fixed page-wide grain */
.page-grain{position:fixed;inset:0;z-index:100;pointer-events:none;opacity:.4;background-size:200px 200px;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='200'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.08'/%3E%3C/svg%3E")}
/* over a video, as the last child of a position:relative; overflow:hidden media box */
.noise-overlay{position:absolute;inset:0;pointer-events:none;opacity:.7;mix-blend-mode:overlay;background-image:var(--noise-a)}
.bg-noise{position:absolute;inset:0;pointer-events:none;opacity:.15;background-image:var(--noise-b)}
/* animated film grain (parent needs overflow:hidden) */
.grain-anim{position:absolute;inset:-50%;pointer-events:none;opacity:.08;mix-blend-mode:overlay;
  background-image:var(--noise-a);animation:grain 1s steps(6) infinite}
@keyframes grain{0%,100%{transform:translate(0,0)}20%{transform:translate(-5%,3%)}40%{transform:translate(4%,-6%)}
  60%{transform:translate(-3%,5%)}80%{transform:translate(6%,2%)}}
.halftone{position:absolute;inset:0;pointer-events:none;opacity:.2;mix-blend-mode:multiply;
  background-image:radial-gradient(circle,#000 1px,transparent 1px);background-size:4px 4px}
.dot-grid{position:absolute;inset:0;pointer-events:none;opacity:.05;
  background-image:radial-gradient(#fff 1px,transparent 1px);background-size:24px 24px}
@media (prefers-reduced-motion:reduce){.grain-anim{animation:none}}
```
Noise *inside* text (define once per page, then `filter:url(#text-grain)`):
```html
<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false">
  <filter id="text-grain">
    <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" stitchTiles="stitch"/>
    <feColorMatrix type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 0.35 0"/>
    <feComposite in2="SourceGraphic" operator="in" result="noise"/>
    <feBlend in="SourceGraphic" in2="noise" mode="multiply"/>
  </filter>
  <filter id="watermark-grain">
    <feTurbulence type="fractalNoise" baseFrequency="0.5" numOctaves="2" stitchTiles="stitch"/>
    <feComponentTransfer><feFuncA type="linear" slope="0.075"/></feComponentTransfer>
    <feComposite in2="SourceGraphic" operator="in" result="noise"/>
    <feBlend in="SourceGraphic" in2="noise" mode="overlay"/>
  </filter>
</svg>
<h2 style="filter:url(#text-grain)">Poster type</h2>
```

**Perf / mobile:** SVG filters on large text are expensive: use them on one or two elements and drop them ≤1024 px. Overlay grain is cheap (a static tile).

---

## Scroll-Linked Choreography & Frame Scrubbing

# Scroll

Reveals, pinned stages, parallax and scroll-linked motion. (Scroll-scrubbed video lives in video-and-media.md; the scroll-linked word reveal in type-and-text-motion.md.)

**Conventions.** Single-file, no build step. Shared tokens (paste once):
```css
:root{
  --ease-out-expo:cubic-bezier(.16,1,.3,1);
  --ease-out-quint:cubic-bezier(.22,1,.36,1);
  --ease-reveal:cubic-bezier(.25,.1,.25,1);
}
```
Scroll handlers are passive and rAF-throttled (`if (!ticking) { ticking = true; requestAnimationFrame(update); }`). **Never** put `overflow:hidden` on an ancestor of a sticky element: it kills `position:sticky`. Use `overflow-x:clip` on wrappers. Scroll-driven motion is user-driven, so under reduced motion keep the mapping but drop smoothing and autonomous movement.

---

## 1. Viewport-triggered staggered reveal (+ directional corner decor)

**What / when:** Below-the-fold blocks fade and rise once as they enter the viewport, with per-element delays so a group cascades. The workhorse for every section after the hero. The corner-decor version frames a centred heading with four objects (3D renders, icons) that slide in from the left and right toward the corners: good for an About or Intro section.

**Premium parameters**
- Default `opacity 0, y 30px` → rest, **0.7 s** `cubic-bezier(.25,.1,.25,1)`, once. Large headings y 40 px; media blocks y 60 px, 0.9 s; two-column splits from `x −40px` / `x +40px`; card grids `scale(.95)` + fade with `--ease-out-quint`.
- Trigger: IntersectionObserver `threshold .15`, `rootMargin: 0px 0px -10% 0px` (lets the reader see it happen). Eager alternative: `threshold 0`, `rootMargin 50px`.
- Stagger formulas `base + i × step`: list `150 + i·120 ms`, panel rows `300 + i·110 ms`, nav links `100 + i·100 ms`, stat columns `i·150 ms` (y 30, 0.8 s), grid cards `i·100 ms` (y 20, 0.7 s).
- Corner decor: `x ±80px`, 0.9 s, delays .10 / .15 / .25 / .30 s; sizes 120 → 160 → 210 px by breakpoint; top pair at `top 4 %`, `left/right 1 % → 4 %`; bottom pair at `bottom 8 %`, `3 % → 10 %`.
- Hide targets only when JS is running (`.js` class on `<html>`), so content never disappears if a script fails.
- Gotcha: `threshold` is a fraction of the *element*; a block taller than ~6.6 viewports can never reach 0.15, so use `threshold: 0` plus `rootMargin` for very tall blocks.

**Implementation**
```html
<script>document.documentElement.classList.add('js')</script> <!-- in <head> -->
<ul data-stagger="120" data-stagger-base="150">
  <li data-reveal>…</li><li data-reveal>…</li><li data-reveal>…</li>
</ul>
<section class="about">
  <img class="decor decor--tl" data-reveal style="--x:-80px;--y:0px;--dur:.9s;--d:.10s" src="obj1.png" alt="">
  <img class="decor decor--tr" data-reveal style="--x:80px;--y:0px;--dur:.9s;--d:.15s" src="obj2.png" alt="">
  <img class="decor decor--bl" data-reveal style="--x:-80px;--y:0px;--dur:.9s;--d:.25s" src="obj3.png" alt="">
  <img class="decor decor--br" data-reveal style="--x:80px;--y:0px;--dur:.9s;--d:.30s" src="obj4.png" alt="">
  <h2 data-reveal style="--y:40px">About</h2>
</section>
```
```css
.js [data-reveal]{opacity:0;transform:translate3d(var(--x,0px),var(--y,30px),0);
  transition:opacity var(--dur,.7s) var(--ease,var(--ease-reveal)) var(--d,0s),
             transform var(--dur,.7s) var(--ease,var(--ease-reveal)) var(--d,0s)}
.js [data-reveal="scale"]{transform:scale(.95);--ease:var(--ease-out-quint)}
.js [data-reveal].is-in{opacity:1;transform:none}
.about{position:relative;min-height:100vh;display:grid;place-items:center;padding:80px 20px;overflow-x:clip}
.decor{position:absolute;width:clamp(120px,14vw,210px);height:auto;pointer-events:none}
.decor--tl{top:4%;left:clamp(1%,2vw,4%)} .decor--tr{top:4%;right:clamp(1%,2vw,4%)}
.decor--bl{bottom:8%;left:clamp(3%,5vw,10%);width:clamp(100px,12vw,180px)}
.decor--br{bottom:8%;right:clamp(3%,5vw,10%);width:clamp(130px,15vw,220px)}
@media (prefers-reduced-motion:reduce){.js [data-reveal]{opacity:1;transform:none;transition:none}}
```
```js
document.querySelectorAll('[data-stagger]').forEach((group) => {
  const step = +group.dataset.stagger, base = +(group.dataset.staggerBase || 0);
  group.querySelectorAll('[data-reveal]').forEach((el, i) => el.style.setProperty('--d', `${base + i * step}ms`));
});
const revealIO = new IntersectionObserver((entries) => entries.forEach((e) => {
  if (e.isIntersecting) { e.target.classList.add('is-in'); revealIO.unobserve(e.target); }
}), { threshold: 0.15, rootMargin: '0px 0px -10% 0px' });
document.querySelectorAll('[data-reveal]').forEach((el) => revealIO.observe(el));
```

**Framer Motion variant:** `<motion.div initial={{ opacity: 0, x, y }} whileInView={{ opacity: 1, x: 0, y: 0 }} viewport={{ once: true, margin: '-100px' }} transition={{ delay, duration: 0.7, ease: [0.25, 0.1, 0.25, 1] }} />`

---

## 2. Sticky cinematic stage with CSS-variable choreography (scroll windows, split-frame parting, depth-of-field, tint)

**What / when:** A whole "film" told in one pinned viewport. Layered transparent cut-outs (sky → midground → giant title → subject → foreground halves) move independently as the user scrolls a long runway. The title sits *between* background and subject; the foreground splits apart like curtains to reveal a close-up; the background racks out of focus and takes on a tint; story panels slide through. For destination, product-launch or brand-story pages with layered photography.

**Architecture**
- Runway section `height: calc(100vh + N px)` (~3000–3700 px) with a `position:sticky; top:0; height:100vh; min-height:620px` stage.
- JS computes `scroll = clamp(-section.top, 0, section.height − innerHeight)` in **pixels**, smooths it (`lerp 0.14`, snap when `|Δ| < 0.08px`), then writes ~25 CSS custom properties per frame; CSS owns all transforms. rAF runs only while something is still settling.
- Two helpers build the timeline: `smoothstep(e0, e1, s)` and `segment(s, a, b, c, d)` → `{enter, exit, active = enter × (1 − exit)}`, a "scroll window" that fades in over `[a,b]` and out over `[c,d]`.
- Write the story as a table of pixel windows first, e.g.:

| Scroll px | What happens |
|---|---|
| 90 → 650 | Title rises `−210px`, scales to `.92`, fades; intro copy + pills sink `+90px`, fade |
| 560 → 900 (enter) | Foreground halves part to `∓46vw` (eased `enter^1.5`), rise `−180px`, scale `+0.74`; subject widens `67.2 → 105vw`, lifts; close-up fades in; background blurs to **14px**, brightness `−25.5 %`, tint rises to alphas **.465 / .42 / .51** |
| 1300 → 1620 (exit) | Subject launches `−760px`, scales `+0.46`; chapter panel slides `+58 → −86px` and fades |
| next windows | Repeat with new layers (saturation boosts, a card row flying in from `420vw`, …) |

- Constant drift across the runway: `progress = scroll / 2700` adds `−74px` Y and `+0.23` scale to the hero layers and grows the back stack `0.76 → 0.96`.
- Pointer parallax mixed in (depth-and-interaction.md, technique 3): background `x·−12 / y·−4`, subject `x·18 / y·8`, foreground halves `x·22 / y·10`, close-up `x·10 / y·8`.

**Implementation**
```html
<section class="cine" style="--runway:3000px" aria-label="Story">
  <div class="cine__stage">
    <img class="cine__layer cine__sky" src="sky.jpg" alt="">
    <img class="cine__layer cine__mid" src="midground-cutout.png" alt="">
    <div class="cine__shade" aria-hidden="true"></div>
    <h1 class="cine__title">Title</h1>
    <img class="cine__layer cine__subject" src="subject-cutout.png" alt="">
    <img class="cine__layer cine__closeup" src="closeup.png" alt="">
    <img class="cine__layer cine__split cine__split--l" src="foreground-left-half.png" alt="">
    <img class="cine__layer cine__split cine__split--r" src="foreground-right-half.png" alt="">
    <div class="cine__intro">
      <p>One-sentence promise of the place or product.</p>
      <div class="cine__tags"><span>Tag one</span><span>Tag two</span><span>Tag three</span></div>
    </div>
    <div class="cine__panel"><h2>Chapter headline.</h2><p>Two short lines of supporting copy.</p></div>
  </div>
</section>
```
```css
.cine{position:relative;height:calc(100vh + var(--runway,3000px))}
.cine__stage{position:sticky;top:0;height:100vh;min-height:620px;overflow:hidden;isolation:isolate;background:#7fb4d4;
  --tint:74,181,224;
  --mx:0;--my:0;--blur:0px;--bright:1;--shade:0;--mid-s:.76;
  --title-y:0px;--title-s:1;--title-o:1;
  --subj-y:0px;--subj-w:67.2vw;--subj-b:5vh;--subj-s:1.02;
  --split-x:0vw;--split-y:0px;--split-s:1;
  --close-o:0;--close-y:0px;--close-s:1.06;
  --intro-y:0px;--intro-o:1;--panel-o:0;--panel-y:58px}
.cine__layer{position:absolute;display:block;max-width:none;pointer-events:none;user-select:none;-webkit-user-drag:none;will-change:transform,opacity,filter}
.cine__sky{inset:0;width:100%;height:100%;object-fit:cover;z-index:0;filter:blur(var(--blur)) brightness(var(--bright))}
.cine__mid{left:50%;bottom:0;width:112%;height:auto;z-index:1;transform-origin:50% 100%;
  transform:translate3d(calc(-50% + var(--mx) * -12px),calc(var(--my) * -4px),0) scale(var(--mid-s));
  filter:blur(var(--blur)) brightness(var(--bright))}
.cine__shade{position:absolute;inset:0;z-index:2;pointer-events:none;
  background:linear-gradient(180deg,rgba(var(--tint),calc(var(--shade) * .465)) 0%,rgba(var(--tint),calc(var(--shade) * .42)) 48%,rgba(var(--tint),calc(var(--shade) * .51)) 100%)}
.cine__title{position:absolute;left:50%;top:clamp(122px,19vh,205px);z-index:3;width:min(94vw,1780px);margin:0;text-align:center;
  font:500 14rem/.78 Georgia,serif;color:#fdf1e1;
  transform:translate3d(-50%,var(--title-y),0) scale(var(--title-s));opacity:var(--title-o);will-change:transform,opacity}
.cine__subject{left:50%;bottom:var(--subj-b);width:min(var(--subj-w),2140px);height:auto;z-index:4;transform-origin:50% 48%;
  transform:translate3d(calc(-50% + var(--mx) * 18px),var(--subj-y),0) scale(var(--subj-s))}
.cine__closeup{left:50%;top:50%;width:min(122vw,2160px);height:auto;z-index:5;opacity:var(--close-o);transform-origin:50% 48%;
  transform:translate3d(calc(-50% + var(--mx) * 10px),calc(-50% + var(--close-y)),0) scale(var(--close-s))}
.cine__split{left:50%;bottom:-2vh;width:min(118vw,2240px);height:auto;z-index:6}
.cine__split--l{transform-origin:21% 52%;
  transform:translate3d(calc(-50% - var(--split-x) + var(--mx) * 22px),calc(var(--split-y) + var(--my) * 10px),0) scale(var(--split-s))}
.cine__split--r{transform-origin:79% 52%;
  transform:translate3d(calc(-50% + var(--split-x) + var(--mx) * 22px),calc(var(--split-y) + var(--my) * 10px),0) scale(var(--split-s))}
.cine__intro{position:absolute;left:50%;bottom:clamp(56px,28vh,400px);z-index:9;width:min(560px,calc(100vw - 40px));text-align:center;
  transform:translate3d(-50%,var(--intro-y),0);opacity:var(--intro-o)}
.cine__intro p{margin:0;color:#fdf1e1;font-size:1.18rem;font-weight:500;line-height:1.18;text-shadow:0 2px 18px rgba(0,0,0,.42)}
.cine__tags{display:flex;flex-wrap:wrap;justify-content:center;gap:10px;margin-top:26px}
.cine__tags span{min-height:42px;display:inline-flex;align-items:center;padding:0 25px;border-radius:999px;background:#fdf1e1;
  color:#111411;font-size:.98rem;font-weight:500;box-shadow:0 12px 30px rgba(0,0,0,.18)}
.cine__panel{position:absolute;left:50%;top:60%;z-index:10;width:min(760px,calc(100vw - 42px));text-align:center;pointer-events:none;
  opacity:var(--panel-o);transform:translate3d(-50%,calc(-50% + var(--panel-y)),0)}
.cine__panel h2{margin:0;color:#fdf1e1;font:500 4.75rem/.95 Georgia,serif;text-shadow:0 16px 38px rgba(0,0,0,.32)}
.cine__panel p{width:min(520px,100%);margin:26px auto 0;color:#fdf1e1;font-size:1.14rem;font-weight:500;line-height:1.18;text-shadow:0 2px 18px rgba(0,0,0,.42)}
@media (max-width:1500px){.cine__title{font-size:11rem}.cine__panel h2{font-size:4.1rem}}
@media (max-width:1100px){.cine__title{top:15vh;font-size:7.5rem}.cine__subject{width:138vw}.cine__closeup{width:132vw}.cine__panel h2{font-size:3.2rem}}
@media (max-width:640px){.cine__stage{min-height:640px}.cine__title{top:16vh;font-size:4.5rem}
  .cine__subject{bottom:2vh;width:190vw}.cine__closeup{width:176vw}.cine__intro{bottom:42px}
  .cine__intro p,.cine__panel p{font-size:1rem}.cine__panel{top:42%}.cine__panel h2{font-size:2.45rem}}
```
```js
(() => {
  const section = document.querySelector('.cine');
  const stage = section.querySelector('.cine__stage');
  const reduce = matchMedia('(prefers-reduced-motion: reduce)');
  const clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v));
  const smoothstep = (e0, e1, v) => { const x = clamp((v - e0) / (e1 - e0)); return x * x * (3 - 2 * x); };
  const lerp = (a, b, t) => a + (b - a) * t;
  const segment = (s, a, b, c, d) => { const enter = smoothstep(a, b, s), exit = smoothstep(c, d, s); return { enter, exit, active: enter * (1 - exit) }; };
  const set = (k, v) => stage.style.setProperty(k, v);
  let target = 0, smooth = 0, mx = 0, my = 0, tmx = 0, tmy = 0, init = false, pending = false;

  function update() {
    pending = false;
    const rm = reduce.matches;
    target = clamp(-section.getBoundingClientRect().top, 0, section.offsetHeight - innerHeight);
    smooth = (!init || rm) ? target : lerp(smooth, target, 0.14);
    init = true;
    if (Math.abs(smooth - target) < 0.08) smooth = target;
    mx = rm ? 0 : lerp(mx, tmx, 0.12);
    my = rm ? 0 : lerp(my, tmy, 0.12);

    const s = smooth;
    const intro = smoothstep(90, 650, s);                 // hero exit
    const ch = segment(s, 560, 900, 1300, 1620);          // chapter 1 window
    const progress = clamp(s / 2700);
    const split = Math.pow(ch.enter, 1.5);                // eased parting
    const drift = progress * -74, grow = progress * 0.23;

    set('--mx', mx.toFixed(4)); set('--my', my.toFixed(4));
    set('--title-y', `${intro * -210}px`); set('--title-s', (1 - intro * 0.08).toFixed(4)); set('--title-o', (1 - intro).toFixed(4));
    set('--intro-y', `${intro * 90}px`);   set('--intro-o', (1 - intro).toFixed(4));
    set('--mid-s', (0.76 + progress * 0.2 + ch.enter * 0.18).toFixed(4));
    set('--blur', `${(ch.active * 14).toFixed(2)}px`);
    set('--bright', (1 - ch.active * 0.255).toFixed(4));
    set('--shade', ch.active.toFixed(4));
    set('--subj-y', `${(my * 8 + drift - ch.exit * 760).toFixed(1)}px`);
    set('--subj-b', `${(5 - ch.enter * 13).toFixed(2)}vh`);
    set('--subj-w', `${(67.2 + ch.enter * 37.8).toFixed(2)}vw`);
    set('--subj-s', (1.02 + grow + ch.exit * 0.46).toFixed(4));
    set('--split-x', `${(split * 46).toFixed(2)}vw`);
    set('--split-y', `${(drift - split * 180).toFixed(1)}px`);
    set('--split-s', (1 + grow + ch.enter * 0.74).toFixed(4));
    set('--close-o', ch.active.toFixed(4));
    set('--close-y', `${(my * 8 - ch.exit * 150).toFixed(1)}px`);
    set('--close-s', (1.06 + ch.enter * 0.08 + ch.exit * 0.08).toFixed(4));
    set('--panel-o', (ch.active * (1 - ch.exit)).toFixed(4));
    set('--panel-y', `${(-ch.exit * 86 + (1 - ch.enter) * 58).toFixed(1)}px`);

    const settling = Math.abs(smooth - target) > 0.08 || (!rm && (Math.abs(mx - tmx) > 0.001 || Math.abs(my - tmy) > 0.001));
    if (settling) requestTick();
  }
  function requestTick() { if (!pending) { pending = true; requestAnimationFrame(update); } }
  addEventListener('scroll', requestTick, { passive: true });
  addEventListener('resize', requestTick);
  if (matchMedia('(hover: hover) and (pointer: fine)').matches) {
    addEventListener('pointermove', (e) => { tmx = e.clientX / innerWidth - 0.5; tmy = e.clientY / innerHeight - 0.5; requestTick(); }, { passive: true });
  }
  requestTick();
})();
```

**Extra tricks**
- *Screen-true UI inside a zooming layer:* a card row inside the scaling back stack gets `scale(1 / backScale)` with `transform-origin:0 0`, and its top solves `parentTop = vh − (vh − screenTop) / backScale` (back stack origin `50% 100%`), so cards stay pixel-stable while the world zooms.
- *Hide, don't just fade:* off-stage interactive elements use `visibility:hidden` + an off-screen X (`420vw`); controls get `pointer-events:auto` only once their enter value passes **0.98**.
- *Glow layer:* a duplicate background at `opacity .72; mix-blend-mode: screen` adds atmospheric light.
- Asset prep: export each depth plane as transparent PNG/WebP at ~2× viewport width; cut the foreground into a left and a right file (each keeps one half, the other half transparent).

**Reduced motion / mobile:** smoothing and pointer parallax are bypassed (values snap, `--mx/--my = 0`); the composition still scrubs because it's user-driven. Mobile widens subject and close-up (`138vw → 190vw`) so planes still cover, and shrinks the title `14rem → 11 → 7.5 → 4.5rem`.

---

## 3. Panel slide-over hero + viewport-scaled scattered gallery + blend outro

**What / when:** A fashion / archive pattern: a full-bleed video hero, then a black panel slides up over it carrying a sparse, asymmetric grid of tall images that *grow* as they enter the viewport and *shrink away* as they exit, each growing toward the page centre. At the end a white veil fades over everything and a giant pill CTA scales in from the corner. Fixed UI stays legible throughout via exclusion blending (depth-and-interaction.md, technique 6).

**Premium parameters**
- Panel black, top padding `min(400px, 40vh)`; it slides over the sticky hero for the first 100vh.
- Columns 2 / 3 / 4 at `<640 / <1024 / ≥1024 px`; cells `aspect-ratio: 2/3`.
- Scatter rule per row `r`: primary column `a = (2r + r mod 2) mod cols`; every 3rd row adds a second image at `(a + 2) mod cols` (or `a + 1` if equal); other cells stay empty.
- Scale per frame: enter `min(1, (vh − top) / (0.6·vh))`, exit `min(1, bottom / (0.4·vh))`, `scale = min(enter, exit)`, 0 off-screen. Left-half cards `transform-origin: right bottom`, right-half `left bottom`.
- Outro over one screen: white veil `opacity 0 → 1`; CTA `scale(0 → 1)` from `right bottom`; pill `border-radius 1335px`, desktop `330 × 174px`, text **110 px** (72 px mobile), `-.04em`. The double exclusion makes it white-with-black-text over black and the inverse over the veil.
- Measure the *cell*, scale the *image* (`getBoundingClientRect()` includes transforms).

**Implementation**
```html
<section class="pg-hero"><video src="VIDEO_URL.mp4" autoplay muted loop playsinline aria-hidden="true"></video></section>
<section class="pg-panel"><div class="pg-grid" id="pgGrid"></div></section>
<section class="pg-outro" aria-label="End"></section>
<div class="pg-veil" aria-hidden="true"></div>
<a class="pg-cta" href="#"><span>view</span></a>
```
```css
.pg-hero{position:sticky;top:0;height:100vh;height:100svh;z-index:0;overflow:hidden}
.pg-hero video{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.pg-panel{position:relative;z-index:10;background:#000;padding-top:min(400px,40vh);min-height:100vh}
.pg-grid{display:grid;grid-template-columns:repeat(var(--cols,4),1fr)}
.pg-cell{aspect-ratio:2/3}
.pg-card{display:block;width:100%;height:100%;object-fit:cover;transform:scale(0);will-change:transform}
.pg-outro{position:relative;z-index:10;height:100vh;background:#000}
.pg-veil{position:fixed;inset:0;z-index:12;background:#fff;opacity:0;pointer-events:none}
.pg-cta{position:fixed;right:32px;bottom:32px;z-index:20;width:330px;height:174px;border-radius:1335px;background:#fff;
  display:flex;align-items:center;justify-content:center;transform:scale(0);transform-origin:right bottom;
  mix-blend-mode:exclusion;text-decoration:none;pointer-events:none}
.pg-cta span{color:#fff;mix-blend-mode:exclusion;font:500 110px/1 'Inter Tight',Inter,sans-serif;letter-spacing:-.04em}
@media (max-width:640px){.pg-cta{left:16px;right:16px;bottom:60px;width:auto;height:100px}.pg-cta span{font-size:72px}}
```
```js
(() => {
  const IMAGES = ['p1.jpg', 'p2.jpg', 'p3.jpg' /* … ~10 */];
  const grid = document.getElementById('pgGrid');
  const veil = document.querySelector('.pg-veil'), cta = document.querySelector('.pg-cta');
  const outro = document.querySelector('.pg-outro');
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  let cells = [], cols = 0, ticking = false;
  function buildLayout(count, c) {
    const out = []; let placed = 0, r = 0;
    while (placed < count) {
      const row = new Array(c).fill(-1);
      const a = (r * 2 + (r % 2)) % c;
      row[a] = placed++;
      if (r % 3 === 0 && placed < count) { let b = (a + 2) % c; if (b === a) b = (a + 1) % c; row[b] = placed++; }
      out.push(...row); r++;
    }
    return out;
  }
  function render() {
    const c = innerWidth < 640 ? 2 : innerWidth < 1024 ? 3 : 4;
    if (c === cols) return;
    cols = c;
    grid.style.setProperty('--cols', c);
    grid.replaceChildren(...buildLayout(IMAGES.length, c).map((idx, k) => {
      const cell = document.createElement('div'); cell.className = 'pg-cell';
      if (idx >= 0) {
        const img = new Image(); img.src = IMAGES[idx]; img.alt = ''; img.decoding = 'async'; img.className = 'pg-card';
        img.style.transformOrigin = (k % c) < c / 2 ? 'right bottom' : 'left bottom';   // grow toward the centre
        cell.append(img);
      }
      return cell;
    }));
    cells = [...grid.querySelectorAll('.pg-card')].map((img) => [img.parentElement, img]);
  }
  function frame() {
    ticking = false;
    const vh = innerHeight;
    const rects = cells.map(([cell]) => cell.getBoundingClientRect());   // read all…
    cells.forEach(([, img], i) => {                                      // …then write (no layout thrash)
      const r = rects[i];
      let s = reduce ? 1 : 0;
      if (!reduce && r.bottom > 0 && r.top < vh) s = Math.min(1, (vh - r.top) / (vh * 0.6), r.bottom / (vh * 0.4));
      img.style.transform = `scale(${s.toFixed(4)})`;
    });
    const p = Math.min(1, Math.max(0, 1 - outro.getBoundingClientRect().top / vh));
    veil.style.opacity = p.toFixed(3);
    cta.style.transform = `scale(${p.toFixed(4)})`;
    cta.style.pointerEvents = p > 0.9 ? 'auto' : 'none';
  }
  const tick = () => { if (!ticking) { ticking = true; requestAnimationFrame(frame); } };
  render(); frame();
  addEventListener('scroll', tick, { passive: true });
  addEventListener('resize', () => { render(); tick(); });
})();
```
**Perf:** pause or `visibility:hidden` the hero video once the panel covers it (past 100vh).

---

## 4. Pinned heading with counter-drifting parallax columns (+ single-element parallax)

**What / when:** A "visual playground" section: a heading stays pinned in the centre while two columns of tilted square images scroll past over it at different speeds, one faster than the page and one slower. Also: a lone portrait drifting against the scroll beside a testimonial.

**Premium parameters**
- Section `min-height: 300vh`; pinned layer `sticky; top:0; height:100vh` underneath (z 1); columns absolutely over it (z 2), `grid-template-columns: 1fr 1fr`, gap `48 → 160px`, `max-width 1400px`.
- Cards `aspect-ratio 1`, `max-width 320px`, rotations `−4° / +3°`, big soft shadow `0 30px 60px rgba(0,0,0,.35)`, radius 20 px.
- Column speeds `-0.6` (rises faster) and `0.3` (lags), applied as `(progress − 0.5) × speed × innerHeight`.
- Single-element parallax: `offset = clamp(−(elementCentre − viewportCentre) × 0.2, −200px, 200px)`, measured on the untransformed parent.

**Implementation**
```html
<section class="pp">
  <div class="pp__pin"><div><p class="eyebrow">Explorations</p><h2>Visual <em>playground</em></h2></div></div>
  <div class="pp__cols">
    <div class="pp__col" data-speed="-0.6"><figure class="pp__card">…</figure><figure class="pp__card">…</figure><figure class="pp__card">…</figure></div>
    <div class="pp__col" data-speed="0.3"><figure class="pp__card">…</figure><figure class="pp__card">…</figure><figure class="pp__card">…</figure></div>
  </div>
</section>
```
```css
.pp{position:relative;min-height:300vh}
.pp__pin{position:sticky;top:0;height:100vh;display:grid;place-items:center;text-align:center;z-index:1}
.pp__cols{position:absolute;inset:0;z-index:2;display:grid;grid-template-columns:1fr 1fr;gap:clamp(48px,10vw,160px);
  max-width:1400px;margin:0 auto;padding:30vh 24px;pointer-events:none}
.pp__col{display:flex;flex-direction:column;gap:30vh;will-change:transform}
.pp__col:nth-child(2){padding-top:40vh}
.pp__col:nth-child(1) .pp__card{margin-left:auto}
.pp__card{pointer-events:auto;aspect-ratio:1;width:100%;max-width:320px;margin:0;border-radius:20px;overflow:hidden;box-shadow:0 30px 60px rgba(0,0,0,.35)}
.pp__card:nth-child(odd){rotate:-4deg}
.pp__card:nth-child(even){rotate:3deg}
.pp__card img{width:100%;height:100%;object-fit:cover}
```
```js
(() => {
  const sec = document.querySelector('.pp');
  const cols = [...sec.querySelectorAll('.pp__col')];
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  let ticking = false;
  const update = () => {
    ticking = false;
    const r = sec.getBoundingClientRect();
    const p = Math.min(1, Math.max(0, -r.top / (r.height - innerHeight)));
    cols.forEach((c) => {
      const y = reduce ? 0 : (p - 0.5) * parseFloat(c.dataset.speed) * innerHeight;
      c.style.transform = `translate3d(0, ${y.toFixed(1)}px, 0)`;
    });
  };
  addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(update); } }, { passive: true });
  addEventListener('resize', update);
  update();
})();
// Single-element parallax: <div class="parallax-frame"><img data-parallax="0.2" …></div>
(() => {
  const items = [...document.querySelectorAll('[data-parallax]')];
  if (!items.length || matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  let ticking = false;
  const update = () => {
    ticking = false;
    items.forEach((el) => {
      const r = el.parentElement.getBoundingClientRect();
      const delta = r.top + r.height / 2 - innerHeight / 2;
      const y = Math.max(-200, Math.min(200, -delta * parseFloat(el.dataset.parallax)));
      el.style.transform = `translate3d(0, ${y.toFixed(1)}px, 0)`;
    });
  };
  addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(update); } }, { passive: true });
  update();
})();
```
**GSAP variant:** `ScrollTrigger.create({ trigger: '.pp', start: 'top top', end: 'bottom bottom', pin: '.pp__pin', pinSpacing: false })` and `gsap.to('.pp__col:first-child', { yPercent: -30, ease: 'none', scrollTrigger: { trigger: '.pp', scrub: true } })` (load `https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js` + `ScrollTrigger.min.js`, then `gsap.registerPlugin(ScrollTrigger)`).

**Mobile:** on one column (<640 px) reduce speeds by half and the gap to 48 px, or show the cards as a plain stack.

---

## 5. Sticky stacking cards that scale down

**What / when:** Project cards pin near the top of the viewport one after another. Each new card slides over the previous one, and the cards underneath shrink slightly with a sliver of their top edge still visible, like a deck being dealt. For case studies, project lists and process steps (3–5 cards).

**Premium parameters**
- Each card sits in its own sticky slot (`sticky; top:0; height:85vh`), offset `top: i × 28px` so earlier cards peek out above later ones. Slot padding-top 6 rem (8 rem desktop).
- Target scale per card `1 − (n − 1 − i) × 0.03` (3 cards: .94, .97, 1), interpolated from 1 at section progress `i/n` to the target at progress 1 (section top at viewport top → section bottom at viewport bottom). `transform-origin: top center`.
- Cards: very large radii (40 → 60 px), a 2 px light border (`#D7E2EA`) on near-black (`#0C0C0C`), an inner image grid (40 % column with two stacked images, 60 % column with one tall image) at 40–60 px radii.

**Implementation**
```html
<section class="stack">
  <div class="stack-slot"><article class="stack-card" style="--i:0">…</article></div>
  <div class="stack-slot"><article class="stack-card" style="--i:1">…</article></div>
  <div class="stack-slot"><article class="stack-card" style="--i:2">…</article></div>
</section>
```
```css
.stack{position:relative;padding-bottom:10vh}
.stack-slot{position:sticky;top:0;height:85vh;display:flex;justify-content:center;align-items:flex-start;padding-top:clamp(6rem,10vh,8rem)}
.stack-card{position:relative;top:calc(var(--i) * 28px);width:min(1200px,100%);transform-origin:top center;will-change:transform;
  border-radius:clamp(40px,5vw,60px);border:2px solid #D7E2EA;background:#0C0C0C;padding:clamp(16px,2vw,32px)}
```
```js
(function stackCards(section) {
  const cards = [...section.querySelectorAll('.stack-card')];
  const n = cards.length;
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) return;   // keep sticky, skip scaling
  let ticking = false;
  const update = () => {
    ticking = false;
    const r = section.getBoundingClientRect();
    const p = Math.min(1, Math.max(0, -r.top / Math.max(1, r.height - innerHeight)));
    cards.forEach((card, i) => {
      const target = 1 - (n - 1 - i) * 0.03;
      const t = Math.min(1, Math.max(0, (p - i / n) / (1 - i / n)));
      card.style.transform = `scale(${1 + (target - 1) * t})`;
    });
  };
  addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(update); } }, { passive: true });
  addEventListener('resize', update);
  update();
})(document.querySelector('.stack'));
```
**Framer Motion variant**
```tsx
const { scrollYProgress } = useScroll({ target: ref, offset: ['start start', 'end end'] });
const scale = useTransform(scrollYProgress, [i / n, 1], [1, 1 - (n - 1 - i) * 0.03]);   // per card
<div className="h-[85vh] sticky top-0 flex items-start justify-center pt-24 md:pt-32">
  <motion.article style={{ scale, top: i * 28 }} className="relative origin-top …" />
</div>
```

---

## 6. Scroll-linked opposing marquee rows

**What / when:** Two rows of work thumbnails slide horizontally *as you scroll vertically*: the top row to the right, the bottom row to the left. Scrolling becomes a showreel. Use it right after a hero on portfolio or studio pages, or as a "wall of work".

**Premium parameters**
- `offset = (innerHeight − sectionRect.top) × 0.3` (0 when the section's top enters). Row A `translateX(base + offset)`, row B `translateX(base − offset)`.
- Each row's content is **tripled** and starts at `base = −33.333%` (one set to the left), so neither direction ever shows an empty edge. Mark duplicate sets `aria-hidden="true"`.
- Tiles 420 × 270 px (260 × 168 on phones), radius 16 px, `object-fit:cover`, 12 px gaps between tiles and rows; section padding-top 6–10 rem.
- Muted looping MP4/WebM or animated WebP rather than GIF.

**Implementation**
```html
<section class="scroll-rows">
  <div class="sr-row" data-dir="1"><!-- 3 × [tile tile tile …] --></div>
  <div class="sr-row" data-dir="-1"><!-- 3 × [tile tile tile …] --></div>
</section>
```
```css
.scroll-rows{overflow:hidden;padding:clamp(96px,12vw,160px) 0 40px;display:grid;gap:12px}
.sr-row{display:flex;gap:12px;width:max-content;will-change:transform;transform:translate3d(-33.333%,0,0)}
.sr-row img,.sr-row video{width:420px;height:270px;flex:none;border-radius:16px;object-fit:cover;display:block}
@media (max-width:640px){.sr-row img,.sr-row video{width:260px;height:168px}}
```
```js
(function scrollRows(section, factor = 0.3) {
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  const rows = [...section.querySelectorAll('.sr-row')];
  let ticking = false;
  const update = () => {
    ticking = false;
    const offset = (innerHeight - section.getBoundingClientRect().top) * factor;
    rows.forEach((row) => { row.style.transform = `translate3d(calc(-33.333% + ${offset * +row.dataset.dir}px),0,0)`; });
  };
  addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(update); } }, { passive: true });
  addEventListener('resize', update);
  update();
})(document.querySelector('.scroll-rows'));
```
(`.scroll-rows` clips its own content; it is not an ancestor of anything sticky, so `overflow:hidden` is fine here.)

---

## 7. 3D tilted text crawl on scroll (spring-smoothed)

**What / when:** A large centred paragraph tilted back in perspective (like an opening crawl) drifts upward as the section scrolls past, lagging on a heavy spring and fading in mid-way. Turns a plain manifesto paragraph into a cinematic moment over background video.

**Premium parameters**
- Container `perspective: 400px`; text `rotateX(24deg) translateY(y) translateZ(15px)`.
- `y` maps progress `0 → 1` to `60px → −120px`; opacity `0 → 1` between progress **0.3 and 0.5**.
- Progress = section from entering at the bottom to leaving at the top, smoothed by a spring **stiffness 15, damping 32, mass 1.8** (heavy, overdamped: the floaty feel).
- Type `clamp(22px, 3.2vw, 42px)`, lh 1.35, `-.02em`, `user-select:none`; a 180 px top gradient from near-black blends the section edge.

**Implementation**
```html
<section class="crawl">
  <video class="crawl__bg" src="VIDEO_URL.mp4" autoplay muted loop playsinline aria-hidden="true"></video>
  <div class="crawl__fade" aria-hidden="true"></div>
  <div class="crawl__stage"><p class="crawl__text">Your manifesto paragraph…</p></div>
</section>
```
```css
.crawl{position:relative;height:100vh;height:100dvh;overflow:hidden;display:grid;place-items:center;background:#000}
.crawl__bg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.crawl__fade{position:absolute;left:0;right:0;top:0;height:180px;z-index:1;background:linear-gradient(#010103,transparent)}
.crawl__stage{position:relative;z-index:2;max-width:64rem;perspective:400px}
.crawl__text{margin:0;padding:0 1.5rem;text-align:center;color:#fff;font-size:clamp(22px,3.2vw,42px);line-height:1.35;
  letter-spacing:-.02em;user-select:none;opacity:var(--o,0);transform:rotateX(24deg) translateY(var(--y,60px)) translateZ(15px)}
```
```js
(() => {
  const sec = document.querySelector('.crawl'), txt = sec.querySelector('.crawl__text');
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const K = 15, C = 32, M = 1.8;                         // spring constants
  let x = 0, v = 0, last = performance.now();
  function frame(now) {
    const dt = Math.min(0.032, (now - last) / 1000); last = now;
    const r = sec.getBoundingClientRect();
    if (r.bottom > -200 && r.top < innerHeight + 200) {   // only work near the viewport
      const target = Math.min(1, Math.max(0, (innerHeight - r.top) / (innerHeight + r.height)));
      if (reduce) { x = target; v = 0; }
      else { const a = (-K * (x - target) - C * v) / M; v += a * dt; x += v * dt; }   // semi-implicit Euler
      txt.style.setProperty('--y', (60 - 180 * x).toFixed(2) + 'px');
      txt.style.setProperty('--o', Math.min(1, Math.max(0, (x - 0.3) / 0.2)).toFixed(3));
    }
    requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);
})();
```
**Framer Motion variant**
```tsx
const { scrollYProgress } = useScroll({ target: ref, offset: ['start end', 'end start'] });
const smooth = useSpring(scrollYProgress, { stiffness: 15, damping: 32, mass: 1.8 });
const y = useTransform(smooth, [0, 1], [60, -120]);
const opacity = useTransform(smooth, [0.3, 0.5], [0, 1]);
const transform = useMotionTemplate`rotateX(24deg) translateY(${y}px) translateZ(15px)`;
// <div style={{ perspective: 400 }}><motion.p style={{ transform, opacity }}>…</motion.p></div>
```
**A11y:** the text is real DOM text, so it stays readable to screen readers; under reduced motion it tracks scroll without the spring lag.

---

## Spatial Depth, Tilt & Interactive Motion

# Depth & interaction

Pointer-driven depth, cursor effects and interactive showcases.

**Conventions.** Single-file, no build step, dark page unless stated. Shared tokens (paste once):
```css
:root{
  --ease-out-expo:cubic-bezier(.16,1,.3,1);
  --ease-out-quint:cubic-bezier(.22,1,.36,1);
  --ease-standard:cubic-bezier(.25,.1,.25,1);
  --ease-material:cubic-bezier(.4,0,.2,1);
}
```
Pointer effects run only on `(hover: hover) and (pointer: fine)` with motion allowed; give touch screens an autonomous or static alternative. Measure an **untransformed** wrapper and move an inner element, or the moving box feeds back into its own measurement.

---

## 1. Depth carousel with role slots and background-colour crossfade

**What / when:** A product or character carousel built from depth rather than sliding. One item is huge and sharp in the centre; two are small and slightly blurred to the sides; the rest are tiny and more blurred at the back. Navigating rotates items through these *roles*, and the page background crossfades to the active item's colour. For collectibles, colourways and character line-ups (3–6 items). Pairs with a ghost word behind the subject (type-and-text-motion.md, technique 11) and grain.

**Premium parameters**
- One shared transition on every animated property: **650 ms** `cubic-bezier(.4,0,.2,1)`, which also drives the background colour.
- Desktop roles: center `left 50%, height 92%, bottom 0, scale 1.68`, no blur, z 20 · left `left 30%, height 28%, bottom 12%, blur(2px), opacity .85`, z 10 · right the same at `left 70%` · back `left 50%, height 22%, bottom 12%, blur(4px)`, z 5.
- Mobile (<640 px): center `height 60%, bottom 22%, scale 1.25`; sides at 20 % / 80 %, `height 16%, bottom 32%`; back `height 13%, bottom 32%`.
- Items `aspect-ratio: .6/1`, `object-fit:contain; object-position:bottom center`, `will-change: transform, filter, opacity`. Preload all images.
- An animation lock (650 ms) ignores clicks mid-transition.
- Controls: 48 → 64 px circular outline buttons (2 px white border, 26 px arrow at stroke 2.25); hover `scale(1.08)` + `rgba(255,255,255,.12)` fill over 150 ms.
- Palette idea: each item gets a saturated bg and a lighter panel tint (`#F4845F/#F79B7F`, `#6BBF7A/#85CC92`, `#E882B4/#ED9DC4`, `#6EB5FF/#8DC4FF`).

**Implementation**
```html
<section class="dc" tabindex="0" aria-roledescription="carousel" aria-label="Collection">
  <div class="dc-stage">
    <img class="dc-item" src="a.png" alt="Item A" draggable="false">
    <img class="dc-item" src="b.png" alt="Item B" draggable="false">
    <img class="dc-item" src="c.png" alt="Item C" draggable="false">
    <img class="dc-item" src="d.png" alt="Item D" draggable="false">
  </div>
  <button class="dc-btn" data-dir="-1" aria-label="Previous">←</button>
  <button class="dc-btn" data-dir="1" aria-label="Next">→</button>
</section>
```
```css
.dc{--e:cubic-bezier(.4,0,.2,1);position:relative;height:100vh;height:100dvh;overflow:hidden;
  background:var(--bg,#F4845F);transition:background-color 650ms var(--e)}
.dc-stage{position:absolute;inset:0;z-index:3}
.dc-item{position:absolute;aspect-ratio:.6/1;object-fit:contain;object-position:bottom center;
  transform:translateX(-50%) scale(1);transform-origin:bottom center;will-change:transform,filter,opacity;
  transition:transform 650ms var(--e),filter 650ms var(--e),opacity 650ms var(--e),left 650ms var(--e),height 650ms var(--e),bottom 650ms var(--e)}
.dc-item[data-role=center]{left:50%;height:92%;bottom:0;transform:translateX(-50%) scale(1.68);filter:none;opacity:1;z-index:20}
.dc-item[data-role=left]  {left:30%;height:28%;bottom:12%;filter:blur(2px);opacity:.85;z-index:10}
.dc-item[data-role=right] {left:70%;height:28%;bottom:12%;filter:blur(2px);opacity:.85;z-index:10}
.dc-item[data-role=back]  {left:50%;height:22%;bottom:12%;filter:blur(4px);opacity:1;z-index:5}
@media (max-width:639px){
  .dc-item[data-role=center]{height:60%;bottom:22%;transform:translateX(-50%) scale(1.25)}
  .dc-item[data-role=left]{left:20%;height:16%;bottom:32%}
  .dc-item[data-role=right]{left:80%;height:16%;bottom:32%}
  .dc-item[data-role=back]{height:13%;bottom:32%}
}
.dc-btn{position:relative;z-index:60;width:64px;height:64px;border-radius:50%;border:2px solid #fff;background:transparent;color:#fff;
  cursor:pointer;transition:transform 150ms,background-color 150ms}
.dc-btn:hover{transform:scale(1.08);background:rgba(255,255,255,.12)}
@media (max-width:639px){.dc-btn{width:48px;height:48px}}
@media (prefers-reduced-motion:reduce){.dc,.dc-item{transition:none}}
```
```js
(function depthCarousel(root, colors) {
  const items = [...root.querySelectorAll('.dc-item')];
  const N = items.length;
  const roleFor = (off) => (off === 0 ? 'center' : off === 1 ? 'right' : off === N - 1 ? 'left' : 'back');
  let active = 0, locked = false;
  items.forEach((img) => { const p = new Image(); p.src = img.src; });   // preload
  const render = () => {
    items.forEach((el, i) => {
      const role = roleFor((i - active + N) % N);
      el.dataset.role = role;
      el.setAttribute('aria-hidden', String(role !== 'center'));
    });
    root.style.setProperty('--bg', colors[active % colors.length]);
  };
  const go = (dir) => {
    if (locked) return;
    locked = true;
    active = (active + (dir > 0 ? 1 : N - 1)) % N;
    render();
    setTimeout(() => { locked = false; }, 650);
  };
  root.querySelectorAll('.dc-btn').forEach((b) => b.addEventListener('click', () => go(+b.dataset.dir)));
  root.addEventListener('keydown', (e) => { if (e.key === 'ArrowRight') go(1); if (e.key === 'ArrowLeft') go(-1); });
  let x0 = null;                                  // swipe
  root.addEventListener('pointerdown', (e) => { x0 = e.clientX; });
  root.addEventListener('pointerup', (e) => { if (x0 !== null && Math.abs(e.clientX - x0) > 40) go(e.clientX < x0 ? 1 : -1); x0 = null; });
  render();
})(document.querySelector('.dc'), ['#F4845F', '#6BBF7A', '#E882B4', '#6EB5FF']);
```

---

## 2. Magnetic hover (element drifts toward the cursor)

**What / when:** When the cursor comes within a generous radius, an element (portrait, CTA, logo) eases toward it by a fraction of the distance, then floats back slowly when the cursor leaves. It adds weight and life. Use it on hero subjects and primary buttons.

**Premium parameters**
- Activation zone: the element's box plus 150 px (40–80 px for buttons).
- Strength 3: the element moves 1/3 of the cursor offset from its centre (2–4 is the sweet spot).
- Asymmetric easing: `transform .3s ease-out` while tracking, `.6s ease-in-out` on release. The return is slower than the pull.
- Measure the untransformed wrapper, move an inner element. Positioning transforms (like centring with `translateX(-50%)`) belong on the wrapper.
- `translate3d` + `will-change: transform`; fine pointers with motion allowed only.

**Implementation**
```html
<div class="magnet" data-padding="150" data-strength="3"><img class="magnet-inner" src="portrait.png" alt=""></div>
```
```js
function magnet(wrap, { padding = 150, strength = 3 } = {}) {
  if (!matchMedia('(hover: hover) and (pointer: fine) and (prefers-reduced-motion: no-preference)').matches) return;
  const inner = wrap.firstElementChild;
  inner.style.willChange = 'transform';
  let active = false, raf = 0, mx = 0, my = 0;
  const update = () => {
    raf = 0;
    const r = wrap.getBoundingClientRect();          // wrapper is never transformed
    const dx = mx - (r.left + r.width / 2), dy = my - (r.top + r.height / 2);
    const inside = Math.abs(dx) < r.width / 2 + padding && Math.abs(dy) < r.height / 2 + padding;
    if (inside) {
      if (!active) { active = true; inner.style.transition = 'transform .3s ease-out'; }
      inner.style.transform = `translate3d(${dx / strength}px, ${dy / strength}px, 0)`;
    } else if (active) {
      active = false;
      inner.style.transition = 'transform .6s ease-in-out';
      inner.style.transform = 'translate3d(0,0,0)';
    }
  };
  addEventListener('mousemove', (e) => { mx = e.clientX; my = e.clientY; if (!raf) raf = requestAnimationFrame(update); }, { passive: true });
}
document.querySelectorAll('.magnet').forEach((el) => magnet(el, { padding: +el.dataset.padding || 150, strength: +el.dataset.strength || 3 }));
```

---

## 3. Pointer parallax depth layers

**What / when:** Stacked transparent layers drift with or against the pointer by different amounts, giving a still photo real depth. Cheap, subtle, and works on any layered hero (combines with the sticky cinematic stage in scroll.md).

**Premium parameters**
- Normalised pointer `[-0.5, 0.5]`, eased with **lerp 0.12** per rAF; the loop stops once settled.
- Depths (px per unit of pointer): far background **−12 x / −4 y** (moves against the cursor), subject **+18 / +8**, foreground **+22 / +10**. Vertical ≈ 0.35–0.45 × horizontal: horizontal parallax reads stronger and vertical motion feels seasick.
- Overscan every layer (`inset:-4%` or `scale(1.03+)`) so edges never show.

**Implementation**
```html
<div class="px-scene">
  <img class="px-layer" style="--dx:-12;--dy:-4" src="far.jpg" alt="">
  <img class="px-layer" style="--dx:18;--dy:8"   src="subject.png" alt="">
  <img class="px-layer" style="--dx:22;--dy:10"  src="foreground.png" alt="">
</div>
```
```css
.px-scene{position:relative;height:100vh;height:100dvh;overflow:hidden;--mx:0;--my:0}
.px-layer{position:absolute;inset:-4%;width:108%;height:108%;object-fit:cover;pointer-events:none;will-change:transform;
  transform:translate3d(calc(var(--mx) * var(--dx) * 1px),calc(var(--my) * var(--dy) * 1px),0)}
```
```js
(() => {
  const scene = document.querySelector('.px-scene');
  if (!matchMedia('(hover: hover) and (pointer: fine)').matches || matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  let tx = 0, ty = 0, x = 0, y = 0, raf = 0;
  const loop = () => {
    x += (tx - x) * 0.12; y += (ty - y) * 0.12;
    scene.style.setProperty('--mx', x.toFixed(4)); scene.style.setProperty('--my', y.toFixed(4));
    raf = (Math.abs(tx - x) > 0.0005 || Math.abs(ty - y) > 0.0005) ? requestAnimationFrame(loop) : 0;
  };
  addEventListener('pointermove', (e) => {
    tx = e.clientX / innerWidth - 0.5; ty = e.clientY / innerHeight - 0.5;
    if (!raf) raf = requestAnimationFrame(loop);
  }, { passive: true });
})();
```

---

## 4. Cursor-following spotlight reveal mask

**What / when:** Two aligned full-bleed images (surface vs cross-section, day vs night, sketch vs render); a soft glowing circle trailing the cursor reveals the second one. A signature "discovery" interaction for explanatory heroes.

**Premium parameters**
- Radius **260 px**; cursor smoothing **lerp 0.1** per rAF (the trailing lag is what makes it feel physical).
- Feathered mask stops: `0 → 1`, `.4 → 1`, `.6 → .75`, `.75 → .4`, `.88 → .12`, `1 → 0`.
- Start off-screen (`-999px`) so nothing shows until the first move; snap to the first pointer position (no fly-in). The radius eases to 0 on pointer leave via an animatable `@property`.
- Base image settles `scale(1.12 → 1)` over 1.8 s `--ease-out-expo`. The heading uses `pointer-events:none` so it never blocks the reveal.
- Touch screens: the spotlight drifts on its own along a slow Lissajous path.
- A CSS `radial-gradient` mask driven by custom properties is far cheaper than drawing a canvas mask every frame.

**Implementation**
```html
<section class="spot">
  <div class="spot__base"   style="background-image:url(base.jpg)"></div>
  <div class="spot__reveal" style="background-image:url(reveal.jpg)"></div>
  <div class="spot__content">…</div>
</section>
```
```css
@property --spot-r{syntax:'<length>';inherits:true;initial-value:0px}
.spot{position:relative;height:100vh;height:100dvh;overflow:hidden;background:#000;
  --x:-999px;--y:-999px;--spot-r:0px;transition:--spot-r .45s var(--ease-out-expo)}
.spot.is-lit{--spot-r:260px}
.spot__base,.spot__reveal{position:absolute;inset:0;background-position:center;background-size:cover;background-repeat:no-repeat}
.spot__base{z-index:1;animation:spot-settle 1.8s var(--ease-out-expo) both}
.spot__reveal{z-index:3;pointer-events:none;
  -webkit-mask-image:radial-gradient(circle var(--spot-r) at var(--x) var(--y),#000 0%,#000 40%,rgba(0,0,0,.75) 60%,rgba(0,0,0,.4) 75%,rgba(0,0,0,.12) 88%,transparent 100%);
          mask-image:radial-gradient(circle var(--spot-r) at var(--x) var(--y),#000 0%,#000 40%,rgba(0,0,0,.75) 60%,rgba(0,0,0,.4) 75%,rgba(0,0,0,.12) 88%,transparent 100%);
  -webkit-mask-repeat:no-repeat;mask-repeat:no-repeat}
.spot__content{position:relative;z-index:5;height:100%;pointer-events:none}
.spot__content a,.spot__content button{pointer-events:auto}
@keyframes spot-settle{from{transform:scale(1.12)}to{transform:scale(1)}}
@media (prefers-reduced-motion:reduce){.spot__base{animation:none}}
```
```js
(() => {
  const spot = document.querySelector('.spot');
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  let tx = 0, ty = 0, sx = 0, sy = 0, seeded = false, raf = 0;
  const loop = () => {
    const k = reduce ? 1 : 0.1;
    sx += (tx - sx) * k; sy += (ty - sy) * k;
    spot.style.setProperty('--x', sx.toFixed(1) + 'px');
    spot.style.setProperty('--y', sy.toFixed(1) + 'px');
    raf = (Math.abs(tx - sx) > 0.1 || Math.abs(ty - sy) > 0.1) ? requestAnimationFrame(loop) : 0;
  };
  const setTarget = (x, y) => {
    tx = x; ty = y;
    if (!seeded) { sx = x; sy = y; seeded = true; }    // no fly-in from off-screen
    spot.classList.add('is-lit');
    if (!raf) raf = requestAnimationFrame(loop);
  };
  spot.addEventListener('pointermove', (e) => { const r = spot.getBoundingClientRect(); setTarget(e.clientX - r.left, e.clientY - r.top); });
  spot.addEventListener('pointerleave', () => spot.classList.remove('is-lit'));
  if (matchMedia('(hover: none)').matches) {          // touch: slow autonomous drift (parked in the centre for reduced motion)
    const t0 = performance.now();
    (function drift(now) {
      const r = spot.getBoundingClientRect(), p = (now - t0) / 1000, k = reduce ? 0 : 1;
      setTarget(r.width * (0.5 + 0.28 * Math.sin(p * 0.45) * k), r.height * (0.55 + 0.18 * Math.sin(p * 0.8) * k));
      if (!reduce) requestAnimationFrame(drift);
    })(t0);
  }
})();
```
`@property` makes the radius animatable (Chrome/Edge, Safari 16.4+, Firefox 128+); elsewhere it simply snaps.

---

## 5. Cursor image trail

**What / when:** Moving the mouse over a big CTA block spawns thumbnails of your work at the cursor, each slightly rotated, fading and shrinking away: a playful "portfolio spray" behind a "Let's work together" heading.

**Premium parameters:** spawn at most every **80 ms**; random rotation **−10°…+10°**; life **1000 ms**, fading to `opacity 0, scale(.6)`; thumbs ~200–240 px, radius 12 px, soft shadow; a huge calm container (`padding 12rem 0`, radius 40 px, subtle shadow), heading 48 → 80 px. Off on touch and for reduced motion.

**Implementation**
```html
<section class="trail-area">
  <h2 class="trail-area__title">Let's build together</h2>
  <a class="btn" href="#">Start a chat</a>
</section>
```
```css
.trail-area{position:relative;overflow:hidden;padding:12rem 1.5rem;border-radius:40px;background:#fff;text-align:center;box-shadow:0 4px 16px rgba(0,0,0,.08)}
.trail-area>*:not(.trail-img){position:relative;z-index:2}
.trail-area__title{font-size:clamp(48px,6vw,80px);letter-spacing:-.02em;margin:0 0 3rem}
.trail-img{position:absolute;z-index:1;pointer-events:none;border-radius:12px;box-shadow:0 10px 30px rgba(0,0,0,.15);object-fit:cover}
```
```js
function imageTrail(area, srcs, { every = 80, life = 1000, size = 220 } = {}) {
  if (matchMedia('(prefers-reduced-motion: reduce), (hover: none)').matches) return;
  srcs.forEach((s) => { const i = new Image(); i.src = s; });           // preload
  let last = 0, n = 0;
  area.addEventListener('pointermove', (e) => {
    const now = performance.now();
    if (now - last < every) return;
    last = now;
    const r = area.getBoundingClientRect();
    const img = document.createElement('img');
    img.src = srcs[n++ % srcs.length]; img.alt = ''; img.className = 'trail-img';
    img.style.width = `${size}px`; img.style.aspectRatio = '4 / 3';
    img.style.left = `${e.clientX - r.left}px`; img.style.top = `${e.clientY - r.top}px`;
    const rot = (Math.random() * 20 - 10).toFixed(1);
    area.append(img);
    img.animate([
      { opacity: 1, transform: `translate(-50%,-50%) rotate(${rot}deg) scale(1)` },
      { opacity: 0, transform: `translate(-50%,-50%) rotate(${rot}deg) scale(.6)` },
    ], { duration: life, easing: 'cubic-bezier(.4,0,.2,1)', fill: 'forwards' }).onfinish = () => img.remove();
  });
}
imageTrail(document.querySelector('.trail-area'), ['w1.webp', 'w2.webp', 'w3.webp', 'w4.webp']);
```

---

## 6. Exclusion-blend overlay UI & custom cursor

**What / when:** All fixed UI (wordmark, nav, captions, price, footer, cursor) is white with `mix-blend-mode: exclusion`, so it inverts automatically: white over dark footage, black over the white sections that later slide beneath it. One fixed layer survives a page that goes video → black → white. Add a custom circular glyph cursor with the same blend.

**Premium parameters**
- Overlay elements: `position:fixed; color:#fff; mix-blend-mode:exclusion; pointer-events:none` (re-enabled on real links), `z-index:20`; corners at 32 px desktop / 16 px mobile.
- One family at weight 500, `letter-spacing:-.04em`; uppercase 13–15 px nav, 30 px collection label, 80 px price-size numbers.
- Cursor: 48 px SVG (circle `r=22.75`, stroke 2.5) with a glyph inside, centred on the pointer, hidden below 1024 px and on touch; the native cursor is hidden only for fine pointers.
- Micro-detail: a glyph inside a small circle randomises on scroll (`8 $ ^^ % /`), throttled to 80 ms.
- Entrance stagger: logo 0 · nav .15 · caption .3 · product info .45 s (`opacity 0, y 12 → 0`, 0.6 s `--ease-standard`).
- **Stacking gotcha:** blending happens against what is painted inside the same stacking context. Keep blended elements as direct children of `body` (or of the media's wrapper). A parent with `transform`, `filter`, `opacity < 1`, `isolation` or `will-change` traps the blend, so animate the blended element itself, not a wrapper.

**Implementation**
```html
<div class="ui-blend ui-blend--logo">WORDMARK</div>
<nav class="ui-blend ui-blend--nav"><a href="#">About</a><a href="#">[ Cart ]</a></nav>
<div class="ui-blend ui-blend--info"><span class="glyph-ring"><span class="glyph">8</span></span>…</div>
<div class="cursor" aria-hidden="true">
  <svg width="48" height="48" viewBox="0 0 48 48" fill="none"><circle cx="24" cy="24" r="22.75" stroke="#fff" stroke-width="2.5"/>
    <path d="M17 24h14M24 17v14" stroke="#fff" stroke-width="2.5"/></svg>
</div>
```
```css
.ui-blend{position:fixed;z-index:20;color:#fff;mix-blend-mode:exclusion;pointer-events:none;
  font:500 15px/1 'Inter Tight',Inter,sans-serif;letter-spacing:-.04em;text-transform:uppercase}
.ui-blend a{pointer-events:auto;color:inherit;text-decoration:none}
.ui-blend--logo{top:32px;left:32px}
.ui-blend--nav{top:32px;right:32px;width:330px;display:flex;justify-content:space-between}
.ui-blend--info{right:32px;bottom:80px;width:330px;text-align:center}
.glyph-ring{display:inline-grid;place-items:center;width:30px;height:30px;border:2.5px solid currentColor;border-radius:50%;font-size:15px}
@media (max-width:640px){.ui-blend--logo{top:16px;left:16px}.ui-blend--nav{top:16px;right:16px;width:auto;gap:20px}
  .ui-blend--info{left:0;right:0;bottom:48px;width:auto}}
.cursor{position:fixed;left:0;top:0;z-index:50;pointer-events:none;mix-blend-mode:exclusion;will-change:transform}
@media (hover:none),(pointer:coarse),(max-width:1023px){.cursor{display:none}}
@media (hover:hover) and (pointer:fine) and (min-width:1024px){html.has-cursor,html.has-cursor a,html.has-cursor button{cursor:none}}
```
```js
(() => {
  const cur = document.querySelector('.cursor');
  if (matchMedia('(hover: hover) and (pointer: fine) and (min-width: 1024px)').matches) {
    document.documentElement.classList.add('has-cursor');
    addEventListener('pointermove', (e) => { cur.style.transform = `translate3d(${e.clientX - 24}px, ${e.clientY - 24}px, 0)`; }, { passive: true });
  }
  const glyph = document.querySelector('.glyph'), set = ['8', '$', '^^', '%', '/'];
  let lastG = 0;
  addEventListener('scroll', () => {
    const now = performance.now();
    if (now - lastG < 80) return;
    lastG = now;
    glyph.textContent = set[(Math.random() * set.length) | 0];
  }, { passive: true });
})();
```
Keep a visible focus style for keyboard users even when the native cursor is hidden.

---

## 7. Orbit rings with counter-rotating avatars

**What / when:** A "network" visual for talent marketplaces, communities and integrations: concentric hairline rings slowly rotate in alternating directions, avatars ride on them but stay upright, and a big count-up number sits in the centre. Replaces a boring logo grid or stock illustration.

**Premium parameters**
- Container **720×720**; ring diameters **353 / 501 / 649 / 797 px** (148 px spacing; the outer ring deliberately overflows); periods **30 / 40 / 50 / 60 s**, directions **ccw / cw / cw / ccw**.
- Ring stroke: 1 px gradient `accent 0 → 1 @43 % → 0` via the mask-composite ring, so a bright arc travels as the ring spins.
- Avatars 58 px (feature ones 78–88 px; squircles radius 20–24 px mixed with circles) with a coloured glow `0 0 24px <colour>`, placed by `rotate(a) translate(r) rotate(−a)`, `r = diameter/2`.
- Fly-in per avatar: `scale(.3) rotate(−180deg) blur(8px)` → rest, staggered **0.6 → 2.3 s**, `--ease-out-quint`; container `scale(.85 → 1)` 1.2 s at 0.3 s.
- Centre: count-up 0 → 20 over 2 s starting at 1.2 s (type-and-text-motion.md, technique 13), display font 64 px + 16 px label.
- Responsive scale `.85` ≤1280 px, `.7` ≤1024, `.5` ≤768, `.4` ≤480.

**Implementation**
```html
<div class="orbits-wrap">
  <div class="orbits">
    <div class="orbit" data-dir="ccw" style="--d:353px;--t:30s">
      <div class="orbit__item" style="--a:270deg;--r:177px"><div class="orbit__upright">
        <img class="orbit__pop" src="a1.jpg" alt="" style="--delay:.6s;--glow:#a068ff;border-radius:20px"></div></div>
    </div>
    <div class="orbit" style="--d:501px;--t:40s">
      <div class="orbit__item" style="--a:60deg;--r:251px"><div class="orbit__upright">
        <img class="orbit__pop" src="a2.jpg" alt="" style="--delay:.8s;--glow:#ffd166"></div></div>
      <div class="orbit__item" style="--a:180deg;--r:251px"><div class="orbit__upright">
        <img class="orbit__pop orbit__pop--lg" src="a3.jpg" alt="" style="--delay:1s;--glow:#ff5fa2"></div></div>
    </div>
    <div class="orbit" style="--d:649px;--t:50s"></div>
    <div class="orbit" data-dir="ccw" style="--d:797px;--t:60s"></div>
    <div class="orbits__center"><strong data-count="20" data-suffix="k+">20k+</strong><span>Specialists</span></div>
  </div>
</div>
```
```css
.orbits-wrap{--s:1;display:flex;justify-content:center;height:calc(720px * var(--s));overflow:visible}
.orbits{position:relative;flex:none;width:720px;height:720px;transform:scale(var(--s));transform-origin:top center;
  animation:orbits-in 1.2s var(--ease-out-quint) .3s both}
.orbit{position:absolute;left:50%;top:50%;width:var(--d);height:var(--d);translate:-50% -50%;border-radius:50%;
  animation:orbit-spin var(--t) linear infinite}
.orbit[data-dir="ccw"]{animation-direction:reverse}
.orbit::before{content:"";position:absolute;inset:0;border-radius:50%;padding:1px;pointer-events:none;
  background:linear-gradient(180deg,rgba(217,161,255,0) 0%,rgba(217,161,255,1) 43%,rgba(217,161,255,0) 100%);
  -webkit-mask:linear-gradient(#fff 0 0) content-box,linear-gradient(#fff 0 0);
  -webkit-mask-composite:xor;mask:linear-gradient(#fff 0 0) content-box,linear-gradient(#fff 0 0);mask-composite:exclude}
.orbit__item{position:absolute;left:50%;top:50%;width:0;height:0;transform:rotate(var(--a)) translate(var(--r)) rotate(calc(-1 * var(--a)))}
.orbit__upright{position:absolute;translate:-50% -50%;animation:orbit-spin var(--t) linear infinite reverse}
.orbit[data-dir="ccw"] .orbit__upright{animation-direction:normal}
.orbit__pop{display:block;width:58px;height:58px;border-radius:50%;object-fit:cover;box-shadow:0 0 24px var(--glow);
  animation:orbit-pop 1s var(--ease-out-quint) var(--delay,0s) both}
.orbit__pop--lg{width:88px;height:88px}
.orbits__center{position:absolute;inset:0;display:grid;place-content:center;text-align:center;pointer-events:none}
.orbits__center strong{font:500 64px/1 Urbanist,Inter,sans-serif;font-variant-numeric:tabular-nums}
.orbits__center span{font:600 16px/1.4 Urbanist,Inter,sans-serif}
@keyframes orbit-spin{to{rotate:360deg}}
@keyframes orbit-pop{from{opacity:0;transform:scale(.3) rotate(-180deg);filter:blur(8px)}to{opacity:1;transform:none;filter:none}}
@keyframes orbits-in{from{opacity:0;scale:.85}to{opacity:1;scale:1}}
@media (max-width:1280px){.orbits-wrap{--s:.85}}
@media (max-width:1024px){.orbits-wrap{--s:.7}}
@media (max-width:768px){.orbits-wrap{--s:.5}}
@media (max-width:480px){.orbits-wrap{--s:.4}}
@media (prefers-reduced-motion:reduce){.orbit,.orbit__upright,.orbit__pop,.orbits{animation:none}}
```
How it stays upright: each ring spins via the individual `rotate` property; each avatar wrapper runs the *same* animation reversed, cancelling the ring's rotation; the static `rotate(−a)` in the placement cancels the placement angle. Individual `translate/rotate/scale` properties keep them from fighting the `transform` used by the pop-in. The flex wrapper centres the 720 px box even when the viewport is narrower; clip the section with `overflow-x: clip`.

---

## 8. Sand-dissolve image transition (SVG turbulence) + auto-cycling index list

**What / when:** A specimen or product image that disintegrates into drifting grains and re-forms as the next one, driven by an auto-advancing chapter list with a rolling counter. Archival and physical: great for collections, chapters and product variants.

**Premium parameters**
- Filter chain: `feTurbulence fractalNoise baseFrequency 1.8 numOctaves 4` → `feDisplacementMap` scale **0 → 150** → `feOffset` (exit `dx +30, dy +120`, grains fall; enter from `dx −30, dy −80`) → `feGaussianBlur` **0 → 6** → alpha `1 − p × 1.2`.
- **900 ms** per phase; exit eases in `t³`, enter eases out `1 − (1 − t)⁴`. The filter is removed at rest (no cost).
- Image `object-fit:contain` at 80 % of the panel, `mix-blend-mode: lighten` on a black panel (cut-outs float).
- List: auto-advance every **3500 ms**, pause on hover; active item white, idle `#444`, hover `#999`; 32 px rows divided by `rgba(31,41,55,.8)`; the active item shows a thin `↗`; counter `01 / 05` in mono 10 px with the number rolling vertically.

**Implementation**
```html
<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false">
  <filter id="sand" x="-30%" y="-40%" width="160%" height="180%" color-interpolation-filters="sRGB">
    <feTurbulence type="fractalNoise" baseFrequency="1.8" numOctaves="4" seed="3" result="noise"/>
    <feDisplacementMap in="SourceGraphic" in2="noise" scale="0" xChannelSelector="R" yChannelSelector="G" result="disp"/>
    <feOffset in="disp" dx="0" dy="0" result="off"/>
    <feGaussianBlur in="off" stdDeviation="0" result="blur"/>
    <feColorMatrix in="blur" type="matrix" values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 1 0"/>
  </filter>
</svg>
<div class="chapters">
  <figure class="chapters__media"><img id="chapterImg" src="item-3.png" alt=""></figure>
  <div class="chapters__counter"><span class="roll"><span id="chapterNum">03</span></span> / 05</div>
  <ol class="chapters__list">
    <li><button data-img="item-1.png">Chapter one</button></li>
    <li><button data-img="item-2.png">Chapter two</button></li>
    <li><button data-img="item-3.png">Chapter three</button></li>
    <li><button data-img="item-4.png">Chapter four</button></li>
    <li><button data-img="item-5.png">Chapter five</button></li>
  </ol>
</div>
```
```css
.chapters{background:#0a0a0a;color:#fff}
.chapters__media{position:relative;aspect-ratio:1;margin:0;display:grid;place-items:center}
.chapters__media img{width:80%;height:80%;object-fit:contain;mix-blend-mode:lighten}
.chapters__counter{font:10px/1 ui-monospace,monospace;letter-spacing:.1em;color:#888;text-transform:uppercase}
.roll{display:inline-block;overflow:hidden;vertical-align:bottom}
.roll>span{display:inline-block}
.chapters__list{list-style:none;margin:0;padding:0}
.chapters__list button{all:unset;box-sizing:border-box;display:flex;justify-content:space-between;align-items:center;width:100%;
  padding:32px 0;border-bottom:1px solid rgba(31,41,55,.8);cursor:pointer;color:#444;transition:color .3s;
  font-size:clamp(1.5rem,2.4vw,2rem);font-weight:500;letter-spacing:-.025em}
.chapters__list button:hover{color:#999}
.chapters__list button:focus-visible{outline:1px solid #fff;outline-offset:4px}
.chapters__list button[aria-current="true"]{color:#fff}
.chapters__list button::after{content:"\2197";font-weight:200;color:#9ca3af;opacity:0;transform:translate(-6px,6px);transition:opacity .3s,transform .3s}
.chapters__list button[aria-current="true"]::after{opacity:1;transform:none}
```
```js
const sandState = { busy: false, next: null };
async function sandSwap(img, src, { duration = 900 } = {}) {
  if (sandState.busy) { sandState.next = src; return; }
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) { img.src = src; return; }
  sandState.busy = true;
  const f = document.getElementById('sand');
  const disp = f.querySelector('feDisplacementMap'), off = f.querySelector('feOffset');
  const blur = f.querySelector('feGaussianBlur'), cm = f.querySelector('feColorMatrix');
  const apply = (p, dir) => {                 // p: 0 intact → 1 dissolved; dir: +1 exit, -1 enter
    disp.setAttribute('scale', (p * 150).toFixed(1));
    off.setAttribute('dx', (p * 30 * dir).toFixed(1));
    off.setAttribute('dy', (p * (dir > 0 ? 120 : -80)).toFixed(1));
    blur.setAttribute('stdDeviation', (p * 6).toFixed(2));
    cm.setAttribute('values', `1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 ${Math.max(0, 1 - p * 1.2).toFixed(3)} 0`);
  };
  const run = (from, to, ease, dir) => new Promise((res) => {
    const t0 = performance.now();
    const step = (now) => {
      const t = Math.min(1, (now - t0) / duration);
      apply(from + (to - from) * ease(t), dir);
      if (t < 1) requestAnimationFrame(step); else res();
    };
    requestAnimationFrame(step);
  });
  img.style.filter = 'url(#sand)';
  await run(0, 1, (t) => t * t * t, 1);                       // dissolve out (ease-in)
  img.src = src;
  try { await img.decode(); } catch (e) { /* show anyway */ }
  await run(1, 0, (t) => 1 - Math.pow(1 - t, 4), -1);         // re-form (ease-out)
  img.style.filter = '';
  sandState.busy = false;
  if (sandState.next && sandState.next !== src) { const n = sandState.next; sandState.next = null; sandSwap(img, n, { duration }); }
  else sandState.next = null;
}
function rollTo(el, text) {
  const out = el.animate([{ transform: 'translateY(0)', opacity: 1 }, { transform: 'translateY(-100%)', opacity: 0 }],
    { duration: 250, easing: 'ease-in', fill: 'forwards' });
  out.onfinish = () => {
    el.textContent = text; out.cancel();
    el.animate([{ transform: 'translateY(100%)', opacity: 0 }, { transform: 'translateY(0)', opacity: 1 }], { duration: 350, easing: 'cubic-bezier(.16,1,.3,1)' });
  };
}
(() => {
  const root = document.querySelector('.chapters');
  const img = document.getElementById('chapterImg'), num = document.getElementById('chapterNum');
  const btns = [...root.querySelectorAll('.chapters__list button')];
  let active = 2, timer = 0;
  const mark = () => btns.forEach((b, k) => b.setAttribute('aria-current', String(k === active)));
  const setActive = (i) => {
    if (i === active) return;
    active = i; mark();
    rollTo(num, String(i + 1).padStart(2, '0'));
    sandSwap(img, btns[i].dataset.img);
  };
  const start = () => { clearInterval(timer); timer = setInterval(() => setActive((active + 1) % btns.length), 3500); };
  btns.forEach((b, i) => b.addEventListener('click', () => { setActive(i); start(); }));
  root.addEventListener('mouseenter', () => clearInterval(timer));
  root.addEventListener('mouseleave', start);
  mark();
  if (!matchMedia('(prefers-reduced-motion: reduce)').matches) start();
})();
```
**Perf:** 4-octave high-frequency turbulence is expensive on big bitmaps. Keep the image ≤ ~600 px rendered; with several instances, clone the `<filter>` with unique ids.

---

## WebGL Shaders & Three.js 3D Primitives

# 3D & WebGL

Real-time 3D models and shader backdrops. Both are **heavy**: use one per page, as the signature, and always ship a static fallback.

**Conventions.** Single-file, no build step. Pin library versions (`three@0.170.0`). Clamp the device pixel ratio, pause rendering off-screen, and render a still frame for `prefers-reduced-motion`. Opening the page over `file://` blocks model fetches, so serve it (`npx serve .` or `python3 -m http.server`) when testing; the fallback image appears otherwise.

---

## 1. Real 3D model hero (Three.js + GLB)

**What / when:** A real product, character or object model that the visitor can grab and turn, framed exactly inside a chosen area of the layout (usually the right half), with the copy beside it. It settles in with a short turn, sways gently when left alone, and drops to a PNG render if anything fails. Use it when you have (or can generate) a GLB and the object itself is the story: hardware, collectibles, sneakers, packaging, characters.

**Premium parameters**
- Lens **fov 30°** (product-shot look, little distortion). The model is re-centred on its bounding sphere and scaled to **unit radius**, so any GLB frames the same way; the camera distance is solved so the sphere fills **90 %** of the stage's shorter side.
- **Framing with `camera.setViewOffset`:** the camera still looks straight at the model (no perspective skew), but the projection is shifted so the model's centre lands on the centre of a stage element (`[data-stage]`). Layout decides where the model sits; resize keeps it there.
- Rig `pivot > spin > holder > model`: **holder** = centring + unit scale + authored-orientation fix; **spin** = user rotation + inertia; **pivot** = intro turn + idle sway. Each concern owns one group, so they never fight.
- Drag: **0.006 rad/px**, vertical at 0.6× of horizontal; rotations are **premultiplied** onto the spin quaternion around the screen axes, so dragging right always turns the visible face right whatever the current orientation (no gimbal lock). Release keeps the smoothed velocity and decays it (`friction 3.5/s`, max 12 rad/s); a pause of >90 ms before lifting kills the throw.
- Zoom: wheel / trackpad pinch / two-finger pinch, clamped **1 → 1.8**, smoothed (lerp ~10/s). The start zoom *is* the minimum, so a downward wheel over the hero scrolls the page instead of being trapped; trackpad pinch (`ctrlKey`) is always captured.
- Idle: after **1.8 s** without input the sway fades in (yaw ±0.22 rad, pitch ±0.06, lift 0.03 units, ~11 s period) and the model levels itself back upright, keeping its yaw.
- Intro: canvas fades in over 0.9 s while the pivot turns from −0.9 rad and scales 0.9 → 1 over 1.6 s (expo out). Shaders are compiled before the reveal so the first frame doesn't hitch.
- Light: `RoomEnvironment` baked through PMREM (sigma 0.04) as the environment + one key `DirectionalLight` (1.5) for definition; `NeutralToneMapping` keeps product colours honest (use `ACESFilmicToneMapping` for a filmic look).
- Loader: a 140 × 2 px bar driven by real download progress (indeterminate shimmer when the size is unknown). Fallback: a PNG render of the model at its default angle, loaded only when needed (GLB error, no WebGL, context loss, Save-Data).
- Performance: DPR clamped to **2**, rendering paused off-screen (IntersectionObserver), `ResizeObserver` on canvas and stage. Model budget ≤ 3–5 MB, textures 1–2K: `npx gltf-transform optimize in.glb model.glb --compress draco --texture-compress webp --texture-size 2048`.

**Implementation**
```html
<!-- in <head>, before any module script -->
<script type="importmap">
{ "imports": {
    "three": "https://cdn.jsdelivr.net/npm/three@0.170.0/build/three.module.js",
    "three/addons/": "https://cdn.jsdelivr.net/npm/three@0.170.0/examples/jsm/"
} }
</script>

<section class="hero3d" data-model="model.glb">
  <canvas class="hero3d__canvas" aria-hidden="true"></canvas>
  <div class="hero3d__copy">
    <h1>Built to be held.</h1>
    <p>Drag it, turn it, look underneath. Every edge is exactly where you'd want it.</p>
    <a class="btn" href="#buy">Pre-order</a>
  </div>
  <div class="hero3d__stage" data-stage tabindex="0" role="group" aria-label="3D view of the product. Drag or use the arrow keys to rotate.">
    <div class="hero3d__loader is-indeterminate" role="status"><span class="hero3d__bar"><i></i></span><span>Loading model</span></div>
    <img class="hero3d__fallback" data-src="model-fallback.png" alt="The product, front three-quarter view" hidden>
  </div>
</section>
```
```css
.hero3d{position:relative;isolation:isolate;min-height:100vh;min-height:100dvh;display:grid;
  grid-template-columns:minmax(0,1fr) minmax(0,1.15fr);align-items:center;gap:clamp(24px,4vw,64px);
  padding:clamp(96px,12vh,140px) clamp(20px,5vw,72px) clamp(40px,6vh,80px);overflow:hidden;background:#0b0b0c;color:#f4f4f2}
.hero3d__canvas{position:absolute;inset:0;width:100%;height:100%;display:block;z-index:0;pointer-events:none;
  opacity:0;transition:opacity .9s cubic-bezier(.22,1,.36,1)}
.hero3d.is-ready .hero3d__canvas{opacity:1}
.hero3d.is-fallback .hero3d__canvas{display:none}
.hero3d__copy{position:relative;z-index:2;max-width:34rem}
.hero3d__copy h1{margin:0 0 20px;font:500 clamp(40px,5.2vw,76px)/.98 Inter,system-ui,sans-serif;letter-spacing:-.035em}
.hero3d__copy p{margin:0 0 32px;max-width:28rem;font-size:17px;line-height:1.55;color:rgb(244 244 242/.6)}
/* The stage is an empty box in the layout: the model is framed on its centre and it receives the drag */
.hero3d__stage{position:relative;z-index:1;align-self:stretch;min-height:clamp(320px,62vh,760px);display:grid;place-items:center;
  cursor:grab;touch-action:pan-y;-webkit-user-select:none;user-select:none;-webkit-tap-highlight-color:transparent;border-radius:24px;outline:none}
.hero3d__stage:active{cursor:grabbing}
.hero3d__stage:focus-visible{box-shadow:inset 0 0 0 1px rgb(255 255 255/.3)}
.hero3d__stage>*{grid-area:1/1}
.hero3d__loader{display:grid;justify-items:center;gap:12px;font:500 11px/1 ui-monospace,monospace;letter-spacing:.2em;
  text-transform:uppercase;color:rgb(255 255 255/.5);transition:opacity .4s}
.hero3d__bar{width:140px;height:2px;border-radius:2px;background:rgb(255 255 255/.12);overflow:hidden}
.hero3d__bar i{display:block;width:100%;height:100%;background:#fff;transform-origin:left;transform:scaleX(var(--p,0));transition:transform .2s linear}
.hero3d__loader.is-indeterminate .hero3d__bar i{width:40%;transform:none;animation:hero3d-bar 1.1s ease-in-out infinite}
@keyframes hero3d-bar{from{translate:-100% 0}to{translate:250% 0}}
.hero3d.is-ready .hero3d__loader,.hero3d.is-fallback .hero3d__loader{opacity:0;pointer-events:none}
.hero3d__fallback{width:min(88%,560px);height:auto;object-fit:contain}
.hero3d.is-fallback .hero3d__stage{cursor:default}
@media (max-width:860px){
  .hero3d{grid-template-columns:1fr;align-content:start}
  .hero3d__stage{min-height:56vh;min-height:56svh}
}
@media (prefers-reduced-motion:reduce){
  .hero3d__canvas{transition:none}
  .hero3d__loader.is-indeterminate .hero3d__bar i{animation:none;width:100%;opacity:.4}
}
```
```html
<script type="module">
import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { DRACOLoader } from 'three/addons/loaders/DRACOLoader.js';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';

const DRACO_PATH = 'https://www.gstatic.com/draco/versioned/decoders/1.5.7/';
const clamp = (v, a, b) => Math.min(b, Math.max(a, v));
const easeOutExpo = (t) => (t >= 1 ? 1 : 1 - Math.pow(2, -10 * t));

function modelHero(root, opts = {}) {
  const o = {
    src: root.dataset.model,
    fov: 30,                    // narrow lens: product-shot look
    fill: 0.9,                  // share of the stage's shorter side the bounding sphere fills
    zoomMin: 1, zoomMax: 1.8,   // start = min, so a downward wheel scrolls the page
    dragSpeed: 0.006,           // rad per px
    friction: 3.5,              // inertia decay per second
    idleAfter: 1800,            // ms without input before the idle sway
    sway: { yaw: 0.22, pitch: 0.06, lift: 0.03, speed: 0.55 },
    rightOnIdle: true,          // level the model again when idle (keeps its yaw)
    baseRotation: [0, 0, 0],    // fix the model's authored orientation (radians)
    exposure: 1,
    ...opts,
  };
  const canvas = root.querySelector('.hero3d__canvas');
  const stage = root.querySelector('[data-stage]');
  const loaderEl = root.querySelector('.hero3d__loader');
  const reduce = matchMedia('(prefers-reduced-motion: reduce)');
  let renderer, raf = 0, ready = false, visible = true, dead = false;

  const dropLoader = () => setTimeout(() => loaderEl?.remove(), 500);
  const showFallback = () => {
    if (dead) return;
    dead = true; ready = false; cancelAnimationFrame(raf); raf = 0;
    root.classList.remove('is-ready'); root.classList.add('is-fallback');
    const img = root.querySelector('.hero3d__fallback');
    if (img) { if (!img.getAttribute('src')) img.src = img.dataset.src; img.hidden = false; }
    dropLoader();
  };
  if (!o.src || navigator.connection?.saveData) { showFallback(); return () => {}; }
  try {
    renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true, powerPreference: 'high-performance' });
  } catch (e) { showFallback(); return () => {}; }
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
  renderer.setClearColor(0x000000, 0);
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.NeutralToneMapping;
  renderer.toneMappingExposure = o.exposure;
  canvas.addEventListener('webglcontextlost', (e) => { e.preventDefault(); showFallback(); });

  const scene = new THREE.Scene();
  const pmrem = new THREE.PMREMGenerator(renderer);
  const room = new RoomEnvironment();
  scene.environment = pmrem.fromScene(room, 0.04).texture;
  room.dispose?.(); pmrem.dispose();
  const key = new THREE.DirectionalLight(0xffffff, 1.5);
  key.position.set(2.5, 3.5, 4);
  scene.add(key);
  const camera = new THREE.PerspectiveCamera(o.fov, 1, 0.05, 200);

  // Rig: pivot (intro + idle sway) > spin (user rotation + inertia) > holder (centre + unit scale) > model
  const pivot = new THREE.Group(), spin = new THREE.Group(), holder = new THREE.Group();
  holder.rotation.set(...o.baseRotation);
  spin.add(holder); pivot.add(spin); scene.add(pivot);

  // State
  let baseDist = 10, zoomT = clamp(1, o.zoomMin, o.zoomMax), zoom = zoomT;
  let vx = 0, vy = 0, dragging = false, swayW = 0, last = 0, introStart = 0, lastInput = performance.now();
  const AX_X = new THREE.Vector3(1, 0, 0), AX_Y = new THREE.Vector3(0, 1, 0);
  const dq = new THREE.Quaternion(), upright = new THREE.Quaternion(), eul = new THREE.Euler(0, 0, 0, 'YXZ');
  const rotateBy = (ax, ay) => {                       // premultiply = rotate about screen axes
    spin.quaternion.premultiply(dq.setFromAxisAngle(AX_Y, ax));
    spin.quaternion.premultiply(dq.setFromAxisAngle(AX_X, ay));
  };

  // Framing: project the model's centre onto the stage element's centre
  function layout() {
    const W = canvas.clientWidth, H = canvas.clientHeight;
    if (!W || !H) return;
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
    renderer.setSize(W, H, false);
    const c = canvas.getBoundingClientRect();
    let s = stage.getBoundingClientRect();
    if (!s.width || !s.height) s = c;
    const sx = s.left - c.left + s.width / 2, sy = s.top - c.top + s.height / 2;
    camera.aspect = W / H;
    camera.setViewOffset(W, H, W / 2 - sx, H / 2 - sy, W, H);
    const fitPx = o.fill * Math.min(s.width, s.height);                 // on-screen diameter of the unit sphere
    baseDist = H / (fitPx * Math.tan(THREE.MathUtils.degToRad(camera.fov / 2)));
    camera.updateProjectionMatrix();
    wake();
  }

  function tick(now) {
    raf = 0;
    const dt = Math.min(0.05, Math.max(0, (now - last) / 1000)); last = now;
    const rm = reduce.matches;
    let busy = false;
    if (!dragging && (vx || vy)) {                                      // inertia
      if (rm) { vx = vy = 0; }
      else {
        rotateBy(vx * dt, vy * dt);
        const k = Math.exp(-o.friction * dt); vx *= k; vy *= k;
        if (Math.hypot(vx, vy) < 0.02) vx = vy = 0; else busy = true;
      }
    }
    zoom = rm ? zoomT : zoom + (zoomT - zoom) * (1 - Math.exp(-dt * 10));
    if (Math.abs(zoomT - zoom) > 1e-4) busy = true; else zoom = zoomT;
    camera.position.set(0, 0, Math.max(1.6, baseDist / zoom));

    const intro = rm ? 1 : easeOutExpo(Math.min(1, (now - introStart) / 1600));
    if (intro < 1) busy = true;

    const idle = !rm && !dragging && !vx && !vy && now - lastInput > o.idleAfter;
    swayW += ((idle ? 1 : 0) - swayW) * (1 - Math.exp(-dt * (idle ? 1.2 : 6)));
    if (o.rightOnIdle && swayW > 0.001) {                               // level out, keep the yaw
      eul.setFromQuaternion(spin.quaternion); eul.x = 0; eul.z = 0;
      spin.quaternion.slerp(upright.setFromEuler(eul), (1 - Math.exp(-dt * 1.5)) * swayW);
    }
    const t = (now / 1000) * o.sway.speed;
    pivot.rotation.set(swayW * o.sway.pitch * Math.sin(t * 1.3 + 1), (1 - intro) * -0.9 + swayW * o.sway.yaw * Math.sin(t), 0);
    pivot.position.y = swayW * o.sway.lift * Math.sin(t * 1.7);
    pivot.scale.setScalar(0.9 + 0.1 * intro);

    renderer.render(scene, camera);
    if (visible && !dead && (busy || dragging || !rm)) raf = requestAnimationFrame(tick);   // reduced motion: render on demand
  }
  function wake() { if (!raf && visible && ready) { last = performance.now(); raf = requestAnimationFrame(tick); } }
  const poke = () => { lastInput = performance.now(); wake(); };

  // Drag to rotate (one pointer) and pinch to zoom (two pointers)
  const pointers = new Map();
  let lastX = 0, lastY = 0, lastT = 0, pinch = 0;
  stage.addEventListener('pointerdown', (e) => {
    if (!ready || (e.pointerType === 'mouse' && e.button !== 0)) return;
    stage.setPointerCapture(e.pointerId);
    pointers.set(e.pointerId, { x: e.clientX, y: e.clientY });
    if (pointers.size === 1) { dragging = true; vx = vy = 0; lastX = e.clientX; lastY = e.clientY; lastT = e.timeStamp; }
    else if (pointers.size === 2) { const [a, b] = [...pointers.values()]; pinch = Math.hypot(a.x - b.x, a.y - b.y); }
    poke();
  });
  stage.addEventListener('pointermove', (e) => {
    if (!pointers.has(e.pointerId)) return;
    pointers.set(e.pointerId, { x: e.clientX, y: e.clientY });
    if (pointers.size >= 2) {
      const [a, b] = [...pointers.values()];
      const d = Math.hypot(a.x - b.x, a.y - b.y);
      if (pinch > 0) zoomT = clamp(zoomT * (d / pinch), o.zoomMin, o.zoomMax);
      pinch = d;
    } else {
      const dx = e.clientX - lastX, dy = e.clientY - lastY, dms = Math.max(1, e.timeStamp - lastT);
      lastX = e.clientX; lastY = e.clientY; lastT = e.timeStamp;
      const ax = dx * o.dragSpeed;
      const ay = e.pointerType === 'touch' ? 0 : dy * o.dragSpeed * 0.6;   // touch: vertical swipes scroll the page
      rotateBy(ax, ay);
      vx = 0.75 * vx + 0.25 * (ax / dms) * 1000;                          // rad/s, smoothed
      vy = 0.75 * vy + 0.25 * (ay / dms) * 1000;
    }
    poke();
  });
  const release = (e) => {
    if (!pointers.delete(e.pointerId)) return;
    if (pointers.size === 1) {                                            // pinch -> drag: re-seed
      const [p] = [...pointers.values()];
      lastX = p.x; lastY = p.y; lastT = e.timeStamp; pinch = 0; vx = vy = 0;
    } else if (pointers.size === 0) {
      dragging = false;
      if (e.type === 'pointercancel' || e.timeStamp - lastT > 90 || reduce.matches) vx = vy = 0;
      vx = clamp(vx, -12, 12); vy = clamp(vy, -12, 12);
    }
    poke();
  };
  stage.addEventListener('pointerup', release);
  stage.addEventListener('pointercancel', release);

  // Wheel / trackpad pinch zoom; at the limits the page scrolls normally
  stage.addEventListener('wheel', (e) => {
    if (!ready) return;
    const dy = e.deltaY * (e.deltaMode === 1 ? 16 : 1);
    const atLimit = dy > 0 ? zoomT <= o.zoomMin + 1e-3 : zoomT >= o.zoomMax - 1e-3;
    if (atLimit && !e.ctrlKey) return;
    e.preventDefault();
    zoomT = clamp(zoomT * Math.exp(-dy * (e.ctrlKey ? 0.01 : 0.0015)), o.zoomMin, o.zoomMax);
    poke();
  }, { passive: false });

  // Keyboard: arrows rotate 15°, +/- zoom
  stage.addEventListener('keydown', (e) => {
    if (!ready) return;
    const step = 0.26;
    const turns = { ArrowLeft: [-step, 0], ArrowRight: [step, 0], ArrowUp: [0, -step], ArrowDown: [0, step] };
    if (turns[e.key]) rotateBy(...turns[e.key]);
    else if (e.key === '+' || e.key === '=') zoomT = clamp(zoomT * 1.15, o.zoomMin, o.zoomMax);
    else if (e.key === '-') zoomT = clamp(zoomT / 1.15, o.zoomMin, o.zoomMax);
    else return;
    e.preventDefault();
    poke();
  });

  // Load: re-centre on the bounding sphere, scale to unit radius, compile, reveal
  const draco = new DRACOLoader().setDecoderPath(DRACO_PATH);
  const loader = new GLTFLoader().setDRACOLoader(draco);
  loader.load(o.src, (gltf) => {
    draco.dispose();
    if (dead) return;
    const model = gltf.scene;
    model.updateMatrixWorld(true);
    const sphere = new THREE.Box3().setFromObject(model).getBoundingSphere(new THREE.Sphere());
    if (!(sphere.radius > 0) || !Number.isFinite(sphere.radius)) { showFallback(); return; }
    model.position.sub(sphere.center);
    holder.scale.setScalar(1 / sphere.radius);
    holder.add(model);
    layout();
    const reveal = () => {
      if (dead) return;
      ready = true;
      introStart = lastInput = performance.now();
      root.classList.add('is-ready');
      dropLoader();
      wake();
    };
    renderer.compileAsync(scene, camera).then(reveal, reveal);           // no shader hitch on the first frame
  }, (e) => {
    if (!loaderEl || !e.lengthComputable || !e.total) return;
    loaderEl.classList.remove('is-indeterminate');
    loaderEl.style.setProperty('--p', Math.min(1, e.loaded / e.total).toFixed(3));
  }, () => { draco.dispose(); showFallback(); });

  const ro = new ResizeObserver(() => layout());
  ro.observe(canvas); ro.observe(stage);
  const io = new IntersectionObserver(([en]) => { visible = en.isIntersecting; if (visible) wake(); });
  io.observe(root);
  reduce.addEventListener('change', wake);
  document.fonts?.ready.then(() => layout());

  return () => { dead = true; cancelAnimationFrame(raf); ro.disconnect(); io.disconnect(); renderer.dispose(); };
}

modelHero(document.querySelector('.hero3d'));
// Options: modelHero(el, { baseRotation: [0, Math.PI / 4, 0], fill: 0.8, zoomMax: 2.2, rightOnIdle: false });
</script>
```

**Notes**
- **Placing the model:** move or resize `[data-stage]` with ordinary CSS (a grid column, an absolutely positioned box, a card) and the model follows; nothing in the script knows about the layout. The canvas stays full-bleed so the model can overhang the stage edges slightly without clipping.
- **Orientation:** most GLBs face +Z. If yours faces sideways or lies down, fix it once with `baseRotation` rather than rotating in the rig.
- **Look:** a dark page with the model lit by the room environment reads as a studio shot. For a light page set the section background light and `exposure` ~0.9. Add a soft CSS ground shadow under the stage (`radial-gradient(closest-side, rgb(0 0 0/.35), transparent)` in a squashed ellipse) if the object needs to sit on something.
- **Hosting:** the GLB and fallback PNG must come from the same origin or a host that sends CORS headers. The Draco decoder is fetched from gstatic only when the file is Draco-compressed.
- **Reduced motion:** no intro turn, no sway or self-levelling, no inertia, zoom snaps, and frames render only on input. Drag still works because it is user-driven.
- **Mobile:** on touch, horizontal drags rotate and vertical swipes scroll the page (`touch-action: pan-y`); two-finger pinch zooms. The layout stacks the stage under the copy at ≤860 px.
- **React:** call `modelHero(ref.current)` inside `useEffect` and return its cleanup function; keep the markup identical. (React Three Fiber with drei's `useGLTF`/`Bounds` is the idiomatic alternative when the project already uses it.)

---

## 2. Animated shader backdrop (swirl + pointer chroma blob + fluted glass + grain)

**What / when:** A light, almost-white hero whose background is alive: a slow marble swirl between two near-whites, a saturated accent blob that lazily follows the cursor, all seen through vertical **fluted (reeded) glass** with slight chromatic aberration and ridge highlights, plus film grain. For agency and studio heroes on light themes; dark text sits on top with no scrim.

**Premium parameters**
- Swirl `colorA #ffffff`, `colorB #f0f0f0`, twist ("detail") **1.7**.
- Chroma blob in one accent (e.g. `#ff5f03`), heavy momentum (follow lerp **0.04** per frame), soft radius.
- Fluted glass: **8** flutes, angle **31°**, refraction ~0.04 of the frame, aberration ~0.004, ridge highlight **.12**, rounded flute shading.
- Film grain strength **.05**. Page background `#EFEFEF` behind it (the CSS fallback when WebGL is unavailable).
- Full-screen fragment shaders are fill-rate bound: cap DPR at **1.5**, stop the loop off-screen, render one still frame for reduced motion.

**Implementation**
```html
<section class="shader-hero">
  <canvas class="shader-hero__canvas" aria-hidden="true"></canvas>
  <div class="shader-hero__content">…</div>
</section>
```
```css
.shader-hero{position:relative;min-height:100vh;min-height:100svh;background:#EFEFEF;overflow:hidden}
.shader-hero__canvas{position:absolute;inset:0;width:100%;height:100%;display:block;z-index:0;pointer-events:none}
.shader-hero__content{position:relative;z-index:1}
```
```js
const SHADER_VERT = `
attribute vec2 aPos;
void main(){ gl_Position = vec4(aPos, 0.0, 1.0); }`;

const SHADER_FRAG = `
#ifdef GL_FRAGMENT_PRECISION_HIGH
precision highp float;
#else
precision mediump float;
#endif
uniform vec2  uRes;
uniform float uTime;
uniform vec2  uPointer;
uniform vec3  uColA, uColB, uAccent;
uniform float uFlutes, uAngle, uRefract, uAberr, uHighlight, uGrain;

float hash(vec2 p){ return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453); }
float noise(vec2 p){
  vec2 i = floor(p), f = fract(p);
  vec2 u = f * f * (3.0 - 2.0 * f);
  return mix(mix(hash(i), hash(i + vec2(1.0, 0.0)), u.x),
             mix(hash(i + vec2(0.0, 1.0)), hash(i + vec2(1.0, 1.0)), u.x), u.y);
}
float fbm(vec2 p){
  float v = 0.0, a = 0.5;
  for (int i = 0; i < 4; i++){ v += a * noise(p); p *= 2.0; a *= 0.5; }
  return v;
}
vec3 scene(vec2 uv){
  float aspect = uRes.x / uRes.y;
  vec2 p = vec2(uv.x * aspect, uv.y);
  float t = uTime * 0.06;
  vec2 c = p - vec2(0.5 * aspect, 0.5);
  float r = length(c);
  float ang = atan(c.y, c.x) + r * 1.7 - t;                 // swirl twist ("detail")
  vec2 q = vec2(cos(ang), sin(ang)) * r;
  float s = fbm(q * 2.5 + vec2(t, -t));
  vec3 col = mix(uColA, uColB, smoothstep(0.3, 0.7, s));
  vec2 m = vec2(uPointer.x * aspect, uPointer.y);
  float d = length(p - m) + 0.12 * (fbm(p * 3.0 + t * 3.0) - 0.5);
  float blob = 1.0 - smoothstep(0.0, 0.45, d);              // chroma blob
  return mix(col, uAccent, blob);
}
void main(){
  vec2 uv = gl_FragCoord.xy / uRes;
  float aspect = uRes.x / uRes.y;
  vec2 p = vec2((uv.x - 0.5) * aspect, uv.y - 0.5);
  float ca = cos(uAngle), sa = sin(uAngle);
  float across = ca * p.x - sa * p.y;                       // coordinate across the flutes
  float bend = fract(across * uFlutes) * 2.0 - 1.0;         // -1..1 inside one flute
  vec2 dir = vec2(ca, -sa);
  vec2 off = dir * bend * uRefract; off.x /= aspect;        // refraction
  vec2 ab  = dir * uAberr;          ab.x  /= aspect;        // chromatic aberration
  vec3 col;
  col.r = scene(uv + off + ab).r;
  col.g = scene(uv + off).g;
  col.b = scene(uv + off - ab).b;
  col *= 1.0 - 0.06 * bend * bend;                          // rounded flute shading
  col += uHighlight * pow(max(0.0, 1.0 - abs(bend)), 6.0);  // ridge highlight
  col += (hash(gl_FragCoord.xy + fract(uTime) * 61.0) - 0.5) * uGrain;   // film grain
  gl_FragColor = vec4(col, 1.0);
}`;

function shaderBackdrop(canvas, opts = {}) {
  const o = Object.assign({ colA: '#ffffff', colB: '#f0f0f0', accent: '#ff5f03', flutes: 8, angle: 31,
    refract: 0.04, aberr: 0.004, highlight: 0.12, grain: 0.05, momentum: 0.04, speed: 1 }, opts);
  const gl = canvas.getContext('webgl', { antialias: false, alpha: false, powerPreference: 'low-power' });
  if (!gl) return false;                                      // the CSS background is the fallback
  const compile = (type, src) => {
    const s = gl.createShader(type); gl.shaderSource(s, src); gl.compileShader(s);
    if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) throw new Error(gl.getShaderInfoLog(s));
    return s;
  };
  const prog = gl.createProgram();
  gl.attachShader(prog, compile(gl.VERTEX_SHADER, SHADER_VERT));
  gl.attachShader(prog, compile(gl.FRAGMENT_SHADER, SHADER_FRAG));
  gl.linkProgram(prog);
  if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) throw new Error(gl.getProgramInfoLog(prog));
  gl.useProgram(prog);
  gl.bindBuffer(gl.ARRAY_BUFFER, gl.createBuffer());
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 3, -1, -1, 3]), gl.STATIC_DRAW);  // one covering triangle
  const aPos = gl.getAttribLocation(prog, 'aPos');
  gl.enableVertexAttribArray(aPos);
  gl.vertexAttribPointer(aPos, 2, gl.FLOAT, false, 0, 0);
  const U = (n) => gl.getUniformLocation(prog, n);
  const rgb = (h) => { const n = parseInt(h.slice(1), 16); return [(n >> 16 & 255) / 255, (n >> 8 & 255) / 255, (n & 255) / 255]; };
  gl.uniform3fv(U('uColA'), rgb(o.colA)); gl.uniform3fv(U('uColB'), rgb(o.colB)); gl.uniform3fv(U('uAccent'), rgb(o.accent));
  gl.uniform1f(U('uFlutes'), o.flutes); gl.uniform1f(U('uAngle'), o.angle * Math.PI / 180);
  gl.uniform1f(U('uRefract'), o.refract); gl.uniform1f(U('uAberr'), o.aberr);
  gl.uniform1f(U('uHighlight'), o.highlight); gl.uniform1f(U('uGrain'), o.grain);
  const uRes = U('uRes'), uTime = U('uTime'), uPointer = U('uPointer');

  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  let px = 0.72, py = 0.35, tx = px, ty = py, visible = true, raf = 0;
  const resize = () => {
    const dpr = Math.min(window.devicePixelRatio || 1, 1.5);   // full-screen fragment shader: cap DPR
    canvas.width = Math.round(canvas.clientWidth * dpr);
    canvas.height = Math.round(canvas.clientHeight * dpr);
    gl.viewport(0, 0, canvas.width, canvas.height);
    gl.uniform2f(uRes, canvas.width, canvas.height);
  };
  const draw = (t) => {
    px += (tx - px) * o.momentum; py += (ty - py) * o.momentum;  // heavy "momentum" follow
    gl.uniform1f(uTime, (t / 1000) * o.speed);
    gl.uniform2f(uPointer, px, py);
    gl.drawArrays(gl.TRIANGLES, 0, 3);
  };
  const loop = (t) => { draw(t); raf = visible && !reduce ? requestAnimationFrame(loop) : 0; };
  resize();
  addEventListener('resize', () => { resize(); if (!raf) draw(performance.now()); });
  addEventListener('pointermove', (e) => {
    const r = canvas.getBoundingClientRect();
    tx = (e.clientX - r.left) / r.width; ty = 1 - (e.clientY - r.top) / r.height;   // GL y points up
  }, { passive: true });
  new IntersectionObserver(([e]) => {
    visible = e.isIntersecting;
    if (visible && !raf && !reduce) raf = requestAnimationFrame(loop);
  }).observe(canvas);
  if (reduce) draw(12000); else raf = requestAnimationFrame(loop);
  return true;
}
shaderBackdrop(document.querySelector('.shader-hero__canvas'));
```

**Mobile:** with no pointer the blob rests at its start position (72 % / 35 %); for touch you can drift it slowly with a `sin`/`cos` target instead. On low-end phones consider `flutes` 6 and DPR 1.

---
