================================================================================
  FILE 062: NEXT.JS ARCHITECTURE
  Section: E - Frontend Development
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  Next.js: The React Framework for Production

  React is a UI library, but building a full production application requires routing, data fetching, server-side rendering, SEO management, and API endpoints. Next.js wraps React to provide all of this out of the box. With the introduction of the App Router (Next.js 13+), the architecture shifted dramatically toward React Server Components (RSC), blending server-side performance with client-side interactivity. In this file, you'll master Server vs Client components, data fetching strategies (SSR, SSG, ISR), file-based routing, and built-in optimization APIs for images and fonts.

  Prerequisites: Strong React fundamentals, understanding of Async JavaScript and basic backend HTTP concepts.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  App Router (app/ directory)
    The modern routing paradigm in Next.js using file-system based routing.
    page.tsx: Defines the unique UI for a route.
    layout.tsx: Defines shared UI (like navbars) that wraps pages and preserves state across navigations.
    loading.tsx: Automatically creates a React Suspense boundary.
    error.tsx: Creates a React Error Boundary.

  React Server Components (RSC)
    By default, all components in the app/ router are Server Components. They render entirely on the server, send zero JavaScript to the client, and can securely access databases directly.

  Client Components
    Components that render on the client (browser) and require JavaScript. Defined by adding the "use client" directive at the top of the file. Required for interactivity (onClick, useState, useEffect).

  Rendering Strategies
    SSR (Server-Side Rendering): Generating HTML on the server for every request. Best for highly dynamic data.
    SSG (Static Site Generation): Generating HTML at build time. Extremely fast, cached on CDNs. Best for blogs/docs.
    ISR (Incremental Static Regeneration): SSG, but updates static pages in the background at set intervals (e.g., revalidate: 60).

  Data Fetching
    Fetching data using native async/await in Server Components. fetch() is extended by Next.js to handle caching and revalidation automatically.

  Server Actions
    A way to mutate data (like submitting a form) securely on the server without creating a dedicated API route.

  Route Handlers
    (Equivalent to old API routes). Files named route.ts that export standard HTTP methods (GET, POST) to build REST APIs directly in Next.js.

  Middleware
    Code that executes before a request completes. Used for authentication checks, redirects, and localization.

  Image Optimization (next/image)
    Prevents layout shift, lazy-loads, and serves WebP/AVIF formats automatically.

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  Server vs Client Components (The Next.js Tree)

  ┌─────────────────────────────────────────────────────────────────────────┐
  │    [ Server Component (Page) ] --- Runs on Server, sends plain HTML     │
  │          |                                                              │
  │          +-- [ Server Component (DB Fetch) ] --- Secure, no JS bundle   │
  │          |                                                              │
  │          +-- [ Client Component (Button) ] <--- "use client"            │
  │                 |                           --- Sends JS to browser     │
  │                 +-- [ Server Component ] <--- Passed as children to Client│
  │                                               (Allowed and performant!) │
  └─────────────────────────────────────────────────────────────────────────┘

  Next.js Request Flow (SSR)

  ┌─────────────────────────────────────────────────────────────────────────┐
  │    Browser                  Next.js Edge/Server                   Database │
  │       |                              |                                | │
  │    1. GET /dashboard  -------------> |                                | │
  │       |                              | 2. Server Component runs       | │
  │       |                              |    (awaits data) ------------> | │
  │       |                              | <----------------------------- | │
  │       |                              | 3. Generates HTML tree         | │
  │       | <--------------------------- | 4. Sends HTML & limited JS     | │
  │       |                              |                                | │
  │    5. Renders UI instantly           |                                | │
  │    6. Hydrates Client Components (attaches Event Listeners)           | │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  File-Based Routing & Route Handlers

  [Language: Text]

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  app/                                                                   │
  │   ┣ layout.tsx                                                          │
  │   ┣ page.tsx                  (-> /)                                    │
  │   ┣ blog/                                                               │
  │   ┃ ┣ page.tsx                (-> /blog)                                │
  │   ┃ ┗ [slug]/                                                           │
  │   ┃   ┗ page.tsx              (-> /blog/my-post)                        │
  │   ┗ api/                                                                │
  │     ┗ users/                                                            │
  │       ┗ route.ts              (-> /api/users)                           │
  └─────────────────────────────────────────────────────────────────────────┘

  Route Handler (app/api/users/route.ts)

  [Language: Typescript]

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  import { NextResponse } from 'next/server';                            │
  │                                                                         │
  │  export async function GET(request: Request) {                          │
  │    // Extract query params (e.g. /api/users?id=1)                       │
  │    const { searchParams } = new URL(request.url);                       │
  │    const id = searchParams.get('id');                                   │
  │                                                                         │
  │    // Secure DB operation here                                          │
  │    return NextResponse.json({ users: [{ id: 1, name: 'Alice' }] });     │
  │  }                                                                      │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

  Server Component + Client Component Interleave
  This is the optimal Next.js pattern: Fetching data securely on the server and passing it to an interactive client component.

  1. app/dashboard/page.tsx (Server Component)

  [Language: Tsx]

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  // This file runs entirely on the server. No JS sent to client.        │
  │  import { Suspense } from 'react';                                      │
  │  import db from '@/lib/db';                                             │
  │  import InteractiveTable from './InteractiveTable';                     │
  │                                                                         │
  │  // 1. Next.js extended fetch (ISR pattern - cache for 60 seconds)      │
  │  async function getDashboardData() {                                    │
  │    const res = await fetch('https://api.internal.com/stats', {        │
  │      next: { revalidate: 60 }                                           │
  │    });                                                                  │
  │    return res.json();                                                   │
  │  }                                                                      │
  │                                                                         │
  │  export default async function DashboardPage() {                        │
  │    // 2. Await data on the server                                       │
  │    const stats = await getDashboardData();                              │
  │                                                                         │
  │    // 3. Direct DB access is secure here!                               │
  │    const users = await db.query('SELECT * FROM users LIMIT 10');        │
  │                                                                         │
  │    return (                                                             │
  │      <main className="p-8">                                             │
  │        <h1>Enterprise Dashboard</h1>                                      │
  │        <p>Server-rendered stats: {stats.totalRevenue}</p>               │
  │                                                                         │
  │        {/* 4. Pass server data to interactive client component */}       │
  │        <Suspense fallback={<p>Loading table...</p>}>                    │
  │          <InteractiveTable initialUsers={users} />                      │
  │        </Suspense>                                                      │
  │      </main>                                                            │
  │    );                                                                   │
  │  }                                                                      │
  └─────────────────────────────────────────────────────────────────────────┘

  2. app/dashboard/InteractiveTable.tsx (Client Component)

  [Language: Tsx]

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  'use client'; // This directive makes it a Client Component            │
  │                                                                         │
  │  import { useState } from 'react';                                      │
  │                                                                         │
  │  // Receives the data fetched on the server as a prop                   │
  │  export default function InteractiveTable({ initialUsers }) {           │
  │    const [users, setUsers] = useState(initialUsers);                    │
  │    const [search, setSearch] = useState('');                            │
  │                                                                         │
  │    // Client-side interactivity                                         │
  │    const filteredUsers = users.filter(u => u.name.includes(search));    │
  │                                                                         │
  │    return (                                                             │
  │      <div>                                                              │
  │        <input                                                           │
  │          type="text"                                                    │
  │          value={search}                                                 │
  │          onChange={(e) => setSearch(e.target.value)}                    │
  │          placeholder="Filter users..."                                  │
  │        />                                                               │
  │        <ul>                                                             │
  │          {filteredUsers.map(user => (                                   │
  │            <li key={user.id}>{user.name}</li>                           │
  │          ))}                                                            │
  │        </ul>                                                            │
  │      </div>                                                             │
  │    );                                                                   │
  │  }                                                                      │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  7. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: What is the difference between a Server Component and a Client Component?

  ANSWER:
    Server components render exclusively on the server, resulting in zero JS added to the browser bundle, and they can directly securely access databases. Client components ("use client") render on the server to HTML, but their JS is sent to the client to be "hydrated" so they can handle interactivity (useState, onClick).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: When should you use the "use client" directive?

  ANSWER:
    Only when you need interactivity (event listeners like onClick), React state/lifecycle hooks (useState, useEffect), or browser-only APIs (like window.localStorage). Leaf nodes of the component tree should be client components; layout and data fetching should be server components.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: Explain the difference between SSG, SSR, and ISR.

  ANSWER:
    SSG (Static) generates HTML at build time. SSR (Server-Rendered) generates HTML dynamically on every request. ISR (Incremental) is hybrid: it serves cached SSG pages, but regenerates them in the background after a specific time interval when traffic hits.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: How do you do Dynamic Routing in Next.js?

  ANSWER:
    By wrapping folder names in brackets. E.g., app/blog/[slug]/page.tsx will match /blog/hello-world where hello-world is the slug parameter passed to the page.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: What is the purpose of next/image?

  ANSWER:
    It automatically optimizes images by converting them to WebP/AVIF, resizing them for different devices, preventing Cumulative Layout Shift (CLS) by reserving space, and lazy-loading them out of the box.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: How do you handle SEO metadata in Next.js App Router?

  ANSWER:
    By exporting a metadata object or a generateMetadata async function from a page.tsx or layout.tsx file. Next.js automatically injects these into the <head>.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q7: What are Server Actions?

  ANSWER:
    Asynchronous functions executed on the server that can be called directly from Client or Server components. They eliminate the need to manually build API endpoints for form submissions or simple database mutations.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q8: What happens in a Next.js App Router layout.tsx file?

  ANSWER:
    It defines shared UI (like a sidebar) that wraps its children pages. Crucially, layouts do not unmount during route transitions between their children, meaning their state and DOM remain intact and performant.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q9: Can you import a Server Component into a Client Component?

  ANSWER:
    No, that defeats the purpose as it forces the Server Component into the client bundle. However, you can pass a Server Component as a children prop to a Client Component.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q10: What is Next.js Middleware?

  ANSWER:
    Code that runs at the Edge before a request is completed. It is typically used to inspect the incoming request (cookies/headers) to perform authentication, rewrites, or redirects before the route even begins rendering.

────────────────────────────────────────────────────────────────────────────────
  8. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: The Secure Leak

  [Language: Tsx]

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  'use client';                                                          │
  │  import { useState, useEffect } from 'react';                           │
  │  import { db } from '@/lib/db'; // Postgres client                      │
  │                                                                         │
  │  export default function UserList() {                                   │
  │    const [users, setUsers] = useState([]);                              │
  │                                                                         │
  │    useEffect(() => {                                                    │
  │      // Let's fetch from DB directly                                    │
  │      db.query('SELECT * FROM users').then(data => setUsers(data));      │
  │    }, []);                                                              │
  │                                                                         │
  │    return <div>...</div>;                                               │
  │  }                                                                      │
  └─────────────────────────────────────────────────────────────────────────┘

  SOLUTION:
    What's wrong? Massive security and architecture failure. Because of "use client", this code attempts to run in the browser. The browser cannot connect directly to Postgres, and if it could, you'd be exposing database credentials to the public internet.
    Fix: Remove "use client", turn it into an async Server Component, and do the DB fetch there directly.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 2: Client Component Import Error

  [Language: Tsx]

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  // app/page.tsx (Server Component)                                     │
  │  import InteractiveButton from './InteractiveButton';                   │
  │                                                                         │
  │  // app/InteractiveButton.tsx                                           │
  │  import { useState } from 'react';                                      │
  │  export default function InteractiveButton() {                          │
  │    const [click, setClick] = useState(0);                               │
  │    return <button onClick={() => setClick(c=>c+1)}>Click</button>;      │
  │  }                                                                      │
  └─────────────────────────────────────────────────────────────────────────┘

  SOLUTION:
    What's wrong? InteractiveButton uses useState but is missing the "use client" directive at the top. Next.js will throw a build error stating you cannot use hooks in Server Components.
    Fix: Add 'use client'; as the very first line of InteractiveButton.tsx.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 3: The Slow Page

  [Language: Tsx]

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  // app/dashboard/page.tsx                                              │
  │  export default async function Dashboard() {                            │
  │    const users = await fetchUsers(); // Takes 2 seconds                 │
  │    const posts = await fetchPosts(); // Takes 2 seconds                 │
  │    return <UI users={users} posts={posts} />;                           │
  │  }                                                                      │
  └─────────────────────────────────────────────────────────────────────────┘

  SOLUTION:
    What's wrong? The requests are sequential. The page will take 4 seconds to render.
    Fix: Run them in parallel using Promise.all:

  [Language: Tsx]

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  const [users, posts] = await Promise.all([fetchUsers(), fetchPosts()]);│
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  9. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  1. SEO & Indexing: Traditional React SPAs send empty HTML (<div id="root"></div>). Web crawlers struggle to index this. Next.js SSR/SSG sends fully populated HTML, guaranteeing perfect SEO out of the box.
  2. Performance (LCP & TTI): Moving heavy libraries (like Markdown parsers or complex formatting tools) to Server Components removes them from the JS bundle sent to the client. This drastically reduces the amount of JS the browser has to download, parse, and execute, speeding up Time to Interactive (TTI).
  3. Backend Simplification: Small-to-medium teams no longer need a separate Node.js/Express server and a React frontend. Next.js handles both securely in a single monorepo.

────────────────────────────────────────────────────────────────────────────────
  10. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

  -> File 058: React Fundamentals (Base React principles extended by Next.js.)
  -> File 061: React Advanced (Contrast Client-side routing with Next.js File-based routing.)
  -> File 064: Frontend Performance (Core Web Vitals (LCP, CLS) that Next.js automatically optimizes.)

================================================================================
  END OF FILE 062
================================================================================
