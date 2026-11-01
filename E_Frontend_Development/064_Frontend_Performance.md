================================================================================
  FILE 064: FRONTEND PERFORMANCE OPTIMIZATION
  Section: E - Frontend Development
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  Frontend Performance: Core Web Vitals, Bundling, and Caching

  A slow website destroys conversion rates, harms SEO, and ruins user experience. In modern frontend development, just making things "work" is not enough; they must work fast, even on low-end mobile devices over 3G networks. This module focuses on measuring and improving Google's Core Web Vitals (LCP, INP/FID, CLS). You will learn how to optimize JavaScript bundles through code-splitting, optimize assets (images/fonts), and implement advanced caching strategies (Service Workers) to build lightning-fast web applications.

  Prerequisites: Understanding of the HTML Rendering Pipeline, React, and basic Network/HTTP mechanics.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  Core Web Vitals (CWV)
    Google's standardized metrics for user experience.
    LCP (Largest Contentful Paint): Measures Loading performance. (Goal: < 2.5s). The time it takes for the largest text block or image to render on screen.
    INP (Interaction to Next Paint): Measures Responsiveness. (Goal: < 200ms). Replaced FID. Measures the delay between a user click/tap and the UI updating.
    CLS (Cumulative Layout Shift): Measures Visual Stability. (Goal: < 0.1). Occurs when elements jump around while loading (e.g., an image loads and pushes text down).

  Bundle Optimization
    Tree Shaking: Removing unused/dead code from the final JS bundle (relies on ES6 import/export).
    Code Splitting: Splitting the main JS bundle into smaller chunks loaded on-demand.
    Dynamic Imports: import('module') loads code asynchronously only when executed.

  Asset Optimization
    Images: Use WebP or AVIF formats. Use srcset and sizes for responsive images. Always set explicit width and height to prevent CLS. Lazy load non-critical images (loading="lazy").
    Fonts: Use font-display: swap to ensure text is visible while the custom font downloads. Preload critical fonts.

  JavaScript Execution
    Main Thread Blocking: JS executes on the browser's single main thread. Long-running tasks freeze the UI (hurting INP).
    Web Workers: Offload heavy computational tasks (parsing large CSVs, cryptography) to background threads.

  Caching & CDNs
    Cache-Control: HTTP headers telling the browser how long to keep files in memory.
    CDN (Content Delivery Network): Distributed servers that cache static assets physically close to the user, drastically reducing latency.

  Service Workers & PWAs
    A JavaScript script that runs in the background, acting as a network proxy. It can intercept HTTP requests and serve files from a local cache, enabling offline functionality.

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  Browser Critical Rendering Path & Main Thread Blocking

  ┌─────────────────────────────────────────────────────────────────────────┐
  │    Network Request -> HTML arrives                                      │
  │                           |                                             │
  │    Parse HTML             |--> Encounters <script src="bundle.js">      │
  │                           |    (Synchronous script blocks parsing!)     │
  │                           v                                             │
  │                      Download JS                                        │
  │                           |                                             │
  │                      Execute JS  <--- [ MAIN THREAD BLOCKED HERE ]      │
  │                           |           (User clicks button -> Nothing happens!)│
  │                           v                                             │
  │                    Resume HTML Parsing                                  │
  │                           |                                             │
  │                  DOM + CSSOM = Render Tree                              │
  │                           |                                             │
  │                     Layout & Paint                                      │
  └─────────────────────────────────────────────────────────────────────────┘

  Fixing CLS (Cumulative Layout Shift)

  ┌─────────────────────────────────────────────────────────────────────────┐
  │    BAD (Causes Shift)                   GOOD (Space Reserved)           │
  │    <img src="hero.jpg" />               <img src="hero.jpg" width="800" height="400" />│
  │                                                                         │
  │    [ Header ]                           [ Header ]                      │
  │    [ Text.. ]                           [   Empty Space Reserved  ]     │
  │    (Image loads, pushes                 [   for image             ]     │
  │     text down violently)                [ Text.. ]                      │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  Image Optimization & CLS Prevention

  [Language: Html]

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  <!--                                                                   │
  │    1. width/height prevents CLS.                                        │
  │    2. loading="lazy" defers loading until user scrolls near it.         │
  │    3. srcset serves smaller files to mobile devices.                    │
  │  -->                                                                    │
  │  <picture>                                                              │
  │    <!-- Serve next-gen AVIF format if supported -->                     │
  │    <source type="image/avif" srcset="hero-small.avif 400w, hero-large.avif 800w" sizes="(max-width: 600px) 400px, 800px">│
  │                                                                         │
  │    <!-- Fallback to optimized WebP -->                                  │
  │    <source type="image/webp" srcset="hero-small.webp 400w, hero-large.webp 800w" sizes="(max-width: 600px) 400px, 800px">│
  │                                                                         │
  │    <!-- Standard fallback for old browsers -->                          │
  │    <img                                                                 │
  │      src="hero-large.jpg"                                               │
  │      alt="Hero presentation"                                            │
  │      width="800"                                                        │
  │      height="400"                                                       │
  │      loading="lazy"                                                     │
  │      decoding="async"                                                   │
  │      style="width: 100%; height: auto;"                                 │
  │    >                                                                    │
  │  </picture>                                                             │
  └─────────────────────────────────────────────────────────────────────────┘

  Font Optimization in CSS

  [Language: Css]

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  /* Using font-display: swap ensures text remains visible (using a system font) │
  │     while the custom web font is downloading, preventing Flash of Invisible Text (FOIT) */│
  │  @font-face {                                                           │
  │    font-family: 'MyCustomFont';                                         │
  │    src: url('/fonts/my-font.woff2') format('woff2');                    │
  │    font-weight: 400;                                                    │
  │    font-display: swap;                                                  │
  │  }                                                                      │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

  Service Worker for Offline Caching (PWA Basics)
  This script sits between the browser and the network. It caches core assets on install, and intercepts fetches to serve them from the cache if the network fails.

  [Language: Javascript]

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  // sw.js (Registered via navigator.serviceWorker.register('/sw.js'))   │
  │                                                                         │
  │  const CACHE_NAME = 'app-cache-v1';                                     │
  │  const ASSETS_TO_CACHE = [                                              │
  │    '/',                                                                 │
  │    '/index.html',                                                       │
  │    '/styles.css',                                                       │
  │    '/app.bundle.js',                                                    │
  │    '/fallback.json' // Offline fallback data                            │
  │  ];                                                                     │
  │                                                                         │
  │  // 1. Install Event: Cache essential files                             │
  │  self.addEventListener('install', (event) => {                          │
  │    event.waitUntil(                                                     │
  │      caches.open(CACHE_NAME).then((cache) => {                          │
  │        console.log('Opened cache and caching assets');                  │
  │        return cache.addAll(ASSETS_TO_CACHE);                            │
  │      })                                                                 │
  │    );                                                                   │
  │    // Force the waiting service worker to become the active service worker│
  │    self.skipWaiting();                                                  │
  │  });                                                                    │
  │                                                                         │
  │  // 2. Activate Event: Clean up old caches (e.g., when updating to v2)  │
  │  self.addEventListener('activate', (event) => {                         │
  │    event.waitUntil(                                                     │
  │      caches.keys().then((cacheNames) => {                               │
  │        return Promise.all(                                              │
  │          cacheNames.map((cacheName) => {                                │
  │            if (cacheName !== CACHE_NAME) {                              │
  │              console.log('Deleting old cache:', cacheName);             │
  │              return caches.delete(cacheName);                           │
  │            }                                                            │
  │          })                                                             │
  │        );                                                               │
  │      })                                                                 │
  │    );                                                                   │
  │    self.clients.claim();                                                │
  │  });                                                                    │
  │                                                                         │
  │  // 3. Fetch Event: Intercept network requests                          │
  │  self.addEventListener('fetch', (event) => {                            │
  │    // Stale-While-Revalidate pattern for API calls                      │
  │    if (event.request.url.includes('/api/')) {                           │
  │      event.respondWith(                                                 │
  │        caches.open('api-cache').then((cache) => {                       │
  │          return fetch(event.request)                                    │
  │            .then((response) => {                                        │
  │               // Put successful fetch in cache                          │
  │               cache.put(event.request, response.clone());               │
  │               return response;                                          │
  │            })                                                           │
  │            .catch(() => {                                               │
  │               // If network fails, try to serve from cache              │
  │               return cache.match(event.request).then((res) => {         │
  │                 if (res) return res;                                    │
  │                 // Absolute fallback                                    │
  │                 return caches.match('/fallback.json');                  │
  │               });                                                       │
  │            });                                                          │
  │        })                                                               │
  │      );                                                                 │
  │    } else {                                                             │
  │      // Cache-First strategy for static assets                          │
  │      event.respondWith(                                                 │
  │        caches.match(event.request).then((cachedResponse) => {           │
  │          // Return cached version if found, otherwise hit network       │
  │          return cachedResponse || fetch(event.request);                 │
  │        })                                                               │
  │      );                                                                 │
  │    }                                                                    │
  │  });                                                                    │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  7. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: What are the Core Web Vitals?

  ANSWER:
    Google's 3 primary performance metrics: LCP (Largest Contentful Paint) for loading speed, INP (Interaction to Next Paint) for visual responsiveness to clicks, and CLS (Cumulative Layout Shift) for visual stability.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: How do you prevent Cumulative Layout Shift (CLS)?

  ANSWER:
    Always provide explicit width and height attributes to images and videos. Ensure ad slots or dynamic UI elements (like banners) have a reserved min-height. Avoid injecting dynamic content above existing content without user interaction.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: What is Tree Shaking?

  ANSWER:
    A build-step optimization (usually done by Webpack/Vite) that analyzes your code and removes unused exports. If you import one function from a 100-function library (like Lodash-es), tree shaking ensures the other 99 functions aren't included in the final JS bundle.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: How can you improve LCP (Largest Contentful Paint)?

  ANSWER:
    Optimize the hero image (WebP/AVIF), preload the hero image (<link rel="preload">), use a CDN to reduce time-to-first-byte (TTFB), and remove render-blocking JavaScript/CSS in the document <head>.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: What does font-display: swap do?

  ANSWER:
    It instructs the browser to immediately render text using a fallback system font (like Arial) while the custom web font is downloading, then "swaps" the font in once downloaded. This prevents the "Flash of Invisible Text" (FOIT).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: What is a Service Worker?

  ANSWER:
    A script that runs in the background, separate from the webpage. It enables features that don't need a web page or user interaction, specifically proxying network requests, enabling offline caching, and receiving background push notifications.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q7: Explain the difference between defer and async in script tags.

  ANSWER:
    Both download the script in the background without blocking HTML parsing. async executes the script immediately when downloaded, which can interrupt HTML parsing. defer waits and executes the script only after the HTML is fully parsed, preserving execution order.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q8: What causes poor INP (Interaction to Next Paint) and how do you fix it?

  ANSWER:
    Long, heavy JavaScript tasks that monopolize the main thread. When a user clicks, the browser can't update the UI until the JS task finishes. Fixed by yielding to the main thread, code splitting, or moving heavy math to Web Workers.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q9: What is cache invalidation and how is it typically handled for JS/CSS files?

  ANSWER:
    Forcing the browser to fetch a new version of a file instead of using a stale cached version. Solved by appending content hashes to filenames during the build process (e.g., app.7b9c.js). When code changes, the hash changes, the browser sees a "new" file, and downloads it while caching it infinitely.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q10: Why shouldn't you lazy load the hero image?

  ANSWER:
    The hero image is usually the LCP element (first thing the user sees). Lazy loading defers the download until the browser calculates layout, unnecessarily delaying the LCP metric. It should be eagerly loaded and preloaded.

────────────────────────────────────────────────────────────────────────────────
  8. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: The Render Block

  [Language: Html]

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  <head>                                                                 │
  │    <link rel="stylesheet" href="styles.css">                            │
  │    <script src="heavy-analytics.js"></script>                           │
  │    <script src="ui-library.js"></script>                                │
  │  </head>                                                                │
  └─────────────────────────────────────────────────────────────────────────┘

  SOLUTION:
    What's wrong? Both scripts are synchronous. The browser will stop parsing the HTML entirely until heavy-analytics.js is downloaded, parsed, and executed. This creates a massive blank white screen delay (terrible First Contentful Paint).
    Fix: Add defer to the <script> tags.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 2: The Import Bloat

  [Language: Javascript]

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  import { isArray, isObject, cloneDeep } from 'lodash';                 │
  │                                                                         │
  │  const myClone = cloneDeep(data);                                       │
  └─────────────────────────────────────────────────────────────────────────┘

  SOLUTION:
    What's wrong? Importing from the main lodash package like this often pulls the entire 70kb Lodash library into your bundle, bypassing tree-shaking because lodash uses old CommonJS modules.
    Fix: Use lodash-es (the ES Module version) which supports tree-shaking, or import specifically: import cloneDeep from 'lodash/cloneDeep'.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 3: The Shifting Ad

  [Language: Jsx]

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  const Page = () => {                                                   │
  │    const [ad, setAd] = useState(null);                                  │
  │                                                                         │
  │    useEffect(() => {                                                    │
  │      fetchAd().then(res => setAd(res)); // Takes 2 seconds              │
  │    }, []);                                                              │
  │                                                                         │
  │    return (                                                             │
  │      <div>                                                              │
  │        <header>My Website</header>                                      │
  │        {ad && <div className="ad-banner">{ad.content}</div>}            │
  │        <main>Lots of text content here...</main>                        │
  │      </div>                                                             │
  │    );                                                                   │
  │  }                                                                      │
  └─────────────────────────────────────────────────────────────────────────┘

  SOLUTION:
    What's wrong? Huge CLS violation. For 2 seconds, the user reads the main text. Then the ad loads and suddenly pushes all the text down, causing the user to lose their place or mis-click.
    Fix: Give the ad container a fixed minimum height so the space is reserved before the ad loads. <div style={{ minHeight: '100px' }}>{ad && ...}</div>.

────────────────────────────────────────────────────────────────────────────────
  9. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  1. Revenue & Conversions: Amazon famously found that every 100ms of latency cost them 1% in sales. Fast sites retain users; slow sites cause them to bounce to competitors.
  2. SEO Rankings: Google directly penalizes websites with poor Core Web Vitals. If your CLS is high or your LCP is over 4 seconds, you will rank lower in search results, reducing organic traffic.
  3. Global Accessibility: Not everyone is on an iPhone 15 Pro with 5G. Testing and optimizing for low-end Android devices on 3G networks is mandatory for global products. Shipping a 5MB JS bundle ruins the experience for these users.

────────────────────────────────────────────────────────────────────────────────
  10. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

  -> File 052: HTML5 Essentials (The base HTML rendering pipeline that JS/CSS blocks.)
  -> File 061: React Advanced (React code-splitting and Suspense logic.)
  -> File 062: NextJS (How Next.js automates image optimization and code-splitting out of the box.)

================================================================================
  END OF FILE 064
================================================================================
