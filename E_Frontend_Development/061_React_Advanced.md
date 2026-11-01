================================================================================
  FILE 061: REACT ADVANCED CONCEPTS
  Section: E - Frontend Development
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  React Advanced: Routing, Performance, and Advanced Patterns

  Once you understand state and props, you must master the architecture of a full application. This guide delves into advanced React development, focusing on Client-Side Routing with React Router v6, advanced performance optimizations (using React.memo, Code Splitting with Suspense), creating Portals for escaping the DOM tree, and dealing with massive forms cleanly. Mastering these patterns allows you to build enterprise-level applications that load instantly and handle complex authentication flows seamlessly.

  Prerequisites: React Fundamentals, Hooks, State Management.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  React Router v6
    The standard library for client-side routing in React.
    <BrowserRouter>: Wraps the app to enable routing via HTML5 history API.
    <Routes> & <Route>: Defines mapping between URL paths and Components.
    useNavigate(): Programmatic navigation (e.g., redirecting after login).
    useParams(): Accessing dynamic URL parameters (e.g., /users/:id).
    <Outlet />: A placeholder for rendering child routes in nested layouts.

  Performance Optimization
    React.memo: A Higher Order Component that memorizes the rendered output of a functional component. It skips re-rendering if the props remain exactly the same.
    Code Splitting: Breaking a massive JavaScript bundle into smaller chunks that load on-demand.
    React.lazy & <Suspense>: APIs to dynamically load components only when they are needed.

  Portals (createPortal)
    Renders children into a DOM node that exists outside the DOM hierarchy of the parent component. Essential for Modals, Tooltips, and Dropdowns to avoid z-index and overflow: hidden CSS traps.

  Error Boundaries
    Components that catch JavaScript errors anywhere in their child component tree, log those errors, and display a fallback UI instead of a white screen of death. (Still requires Class Components or specific libraries like react-error-boundary).

  Forms (Controlled vs Uncontrolled)
    Controlled: React state drives the input value (value={state} onChange={...}).
    Uncontrolled: The DOM handles the state itself, accessed via useRef. Best handled via libraries like React Hook Form.

  Advanced Patterns (HOCs & Render Props)
    Legacy patterns heavily used before hooks. HOCs are functions that take a component and return a new enhanced component. Render props pass a function as a prop to determine what to render.

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  Client-Side Routing vs Server-Side Routing

  ┌─────────────────────────────────────────────────────────────────────────┐
  │    Traditional (Server-Side)        React SPA (Client-Side)             │
  │    +------------------+             +------------------+                │
  │    | Click /about     |             | Click /about     |                │
  │    | Sends HTTP Req   |             | JS Intercepts    |                │
  │    | Server renders HTML            | URL changes locally|              │
  │    | Page Refreshes   |             | React swaps UI   |                │
  │    +------------------+             +------------------+                │
  │    (Slow, blank screen)             (Instant, no reload)                │
  └─────────────────────────────────────────────────────────────────────────┘

  React Portals (Escaping CSS Flow)

  ┌─────────────────────────────────────────────────────────────────────────┐
  │    DOM Tree:                                                            │
  │    <div id="root">                                                      │
  │       <App>                                                             │
  │          <div style="overflow: hidden">                                 │
  │             <Button />                                                  │
  │             == Portal Magic ==  >  Renders Modal content outside 'root' │
  │          </div>                                                         │
  │       </App>                                                            │
  │    </div>                                                               │
  │                                                                         │
  │    <div id="modal-root">                                                │
  │        [ Modal renders here natively, escaping 'overflow: hidden' trap! ] │
  │    </div>                                                               │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  Code Splitting with Suspense & React.lazy

  [Language: Jsx]

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  import React, { Suspense, lazy } from 'react';                         │
  │                                                                         │
  │  // Dynamically import the heavy component.                             │
  │  // It won't be downloaded until it's actually rendered.                │
  │  const HeavyDashboard = lazy(() => import('./components/HeavyDashboard')); │
  │                                                                         │
  │  export const App = () => {                                             │
  │    return (                                                             │
  │      <div>                                                              │
  │        <h1>My Application</h1>                                          │
  │        {/* Suspense shows the fallback UI while the chunk downloads */} │
  │        <Suspense fallback={<div className="spinner">Loading Dashboard...</div>}> │
  │          <HeavyDashboard />                                             │
  │        </Suspense>                                                      │
  │      </div>                                                             │
  │    );                                                                   │
  │  };                                                                     │
  └─────────────────────────────────────────────────────────────────────────┘

  React Portals for a Modal

  [Language: Jsx]

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  import React from 'react';                                             │
  │  import ReactDOM from 'react-dom';                                      │
  │                                                                         │
  │  const Modal = ({ isOpen, onClose, children }) => {                     │
  │    if (!isOpen) return null;                                            │
  │                                                                         │
  │    // Render the modal into a specific DOM node outside the #root hierarchy │
  │    return ReactDOM.createPortal(                                        │
  │      <div className="modal-overlay" onClick={onClose}>                  │
  │        <div className="modal-content" onClick={e => e.stopPropagation()}> │
  │          <button className="close-btn" onClick={onClose}>X</button>     │
  │          {children}                                                     │
  │        </div>                                                           │
  │      </div>,                                                            │
  │      document.getElementById('modal-root') // Must exist in index.html  │
  │    );                                                                   │
  │  };                                                                     │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

  Protected Routes System with React Router v6
  A standard pattern to restrict parts of your application (like a dashboard) to authenticated users only.

  [Language: Jsx]

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  import React from 'react';                                             │
  │  import {                                                               │
  │    BrowserRouter, Routes, Route, Navigate, Outlet, useNavigate          │
  │  } from 'react-router-dom';                                             │
  │                                                                         │
  │  // 1. Mock Authentication Hook                                         │
  │  const useAuth = () => {                                                │
  │    // In reality, this checks Context or Redux/Zustand                  │
  │    return { isAuthenticated: true, user: { name: 'Admin' } };           │
  │  };                                                                     │
  │                                                                         │
  │  // 2. The Protected Route Wrapper                                      │
  │  const ProtectedRoute = () => {                                         │
  │    const { isAuthenticated } = useAuth();                               │
  │                                                                         │
  │    // If not authed, redirect to login page instantly                   │
  │    if (!isAuthenticated) {                                              │
  │      return <Navigate to="/login" replace />;                           │
  │    }                                                                    │
  │                                                                         │
  │    // If authed, render the child routes (the Outlet)                   │
  │    return <Outlet />;                                                   │
  │  };                                                                     │
  │                                                                         │
  │  // 3. Components                                                       │
  │  const Login = () => {                                                  │
  │    const navigate = useNavigate();                                      │
  │    return (                                                             │
  │      <div>                                                              │
  │        <h2>Login Page</h2>                                              │
  │        <button onClick={() => navigate('/dashboard')}>Sign In</button>  │
  │      </div>                                                             │
  │    );                                                                   │
  │  };                                                                     │
  │                                                                         │
  │  const DashboardLayout = () => (                                        │
  │    <div>                                                                │
  │      <nav>Dashboard Sidebar</nav>                                       │
  │      <main>                                                             │
  │         {/* Renders the nested route component (e.g. Settings or Profile) */} │
  │        <Outlet />                                                       │
  │      </main>                                                            │
  │    </div>                                                               │
  │  );                                                                     │
  │                                                                         │
  │  // 4. App Routing Configuration                                        │
  │  export const AppRouting = () => {                                      │
  │    return (                                                             │
  │      <BrowserRouter>                                                    │
  │        <Routes>                                                         │
  │          {/* Public Routes */}                                          │
  │          <Route path="/" element={<Home />} />                          │
  │          <Route path="/login" element={<Login />} />                    │
  │                                                                         │
  │          {/* Protected Routes Block */}                                 │
  │          <Route element={<ProtectedRoute />}>                           │
  │            {/* Nested Routing */}                                       │
  │            <Route path="/dashboard" element={<DashboardLayout />}>      │
  │              <Route index element={<DashboardOverview />} />            │
  │              <Route path="settings" element={<DashboardSettings />} />  │
  │            </Route>                                                     │
  │          </Route>                                                       │
  │                                                                         │
  │          {/* 404 Catch All */}                                          │
  │          <Route path="*" element={<h1>Page Not Found</h1>} />           │
  │        </Routes>                                                        │
  │      </BrowserRouter>                                                   │
  │    );                                                                   │
  │  };                                                                     │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  7. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: What is Client-Side Routing and how does it differ from Server-Side?

  ANSWER:
    Client-side routing intercepts URL changes in the browser using the HTML5 History API, allowing React to swap components instantly without refreshing the page. Server-side routing makes a full HTTP request for a new HTML document on every navigation.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: When should you use React.memo?

  ANSWER:
    Use it to wrap purely presentational child components that re-render often due to parent state changes, even though the child's specific props haven't changed. Overusing it can actually degrade performance due to the overhead of the prop comparison.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: What is a React Portal? Give a use case.

  ANSWER:
    createPortal allows you to render a component's DOM node completely outside its parent's DOM hierarchy (usually directly into document.body or a specific div). Use cases include Modals, Tooltips, and Dropdowns to avoid clipping issues with CSS overflow: hidden or z-index.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: Explain Code Splitting and <Suspense>.

  ANSWER:
    Code splitting divides the massive monolithic JS bundle into smaller chunks. Using React.lazy(() => import('...')), React downloads the chunk only when the component is needed. <Suspense> provides a fallback UI (like a spinner) while the download happens.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: What is the difference between Controlled and Uncontrolled inputs?

  ANSWER:
    Controlled components have their value dictated by React state (value={state}). Uncontrolled components maintain their own internal state in the DOM, which React reads using useRef.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: What is an Error Boundary?

  ANSWER:
    A React component that catches JavaScript errors in its child component tree, logs the errors, and displays a fallback UI instead of crashing the whole app. It requires implementing componentDidCatch or getDerivedStateFromError (currently only available in class components).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q7: What is prop drilling and how is it mitigated?

  ANSWER:
    Passing data through many layers of components just to reach a child. Mitigated by Context API, Global State managers (Redux/Zustand), or Component Composition (passing elements as children or props).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q8: How do you handle complex forms with hundreds of inputs without massive performance hits?

  ANSWER:
    Using uncontrolled component patterns (like the react-hook-form library) to avoid re-rendering the entire form component every time a single keystroke happens.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q9: What is the <Outlet /> component in React Router v6?

  ANSWER:
    It serves as a placeholder in a parent route layout. When a nested child route matches, the child component renders exactly where the <Outlet /> is placed.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q10: What is a Higher-Order Component (HOC)?

  ANSWER:
    An advanced, legacy pattern. It is a function that takes a component as an argument and returns a new component, adding extra data or functionality (e.g., withRouter or Redux's connect). Mostly replaced by custom hooks.

────────────────────────────────────────────────────────────────────────────────
  8. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: The Wasted Memo

  [Language: Jsx]

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  const Parent = () => {                                                 │
  │    const [count, setCount] = useState(0);                               │
  │                                                                         │
  │    // Passed to child                                                   │
  │    const onClick = () => console.log('Clicked');                        │
  │                                                                         │
  │    return <ChildButton onClick={onClick} />                             │
  │  };                                                                     │
  │                                                                         │
  │  const ChildButton = React.memo(({ onClick }) => {                      │
  │    console.log('Button rendered');                                      │
  │    return <button onClick={onClick}>Click</button>;                     │
  │  });                                                                    │
  └─────────────────────────────────────────────────────────────────────────┘

  SOLUTION:
    What's wrong? The ChildButton will still re-render every time Parent renders. Why? The onClick arrow function is re-created on every render, generating a new memory reference. React.memo sees oldProps.onClick !== newProps.onClick and triggers a render.
    Fix: Wrap the function in useCallback: const onClick = useCallback(() => console.log('Clicked'), []);

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 2: The Portal Trap

  [Language: Jsx]

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  const Modal = () => {                                                  │
  │    return ReactDOM.createPortal(                                        │
  │      <div className="modal">Content</div>,                              │
  │      document.getElementById('modal-root')                              │
  │    );                                                                   │
  │  };                                                                     │
  └─────────────────────────────────────────────────────────────────────────┘

  SOLUTION:
    What's wrong? If index.html does NOT have a <div id="modal-root"></div>, getElementById returns null. createPortal will throw a fatal runtime error and crash the app.
    Fix: Always verify the target node exists, or dynamically append it to document.body.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 3: React Router Link Nightmare

  [Language: Jsx]

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  import { Routes, Route } from 'react-router-dom';                      │
  │                                                                         │
  │  const App = () => (                                                    │
  │    <Routes>                                                             │
  │      <Route path="/home" element={<Home />} />                          │
  │    </Routes>                                                            │
  │  );                                                                     │
  │                                                                         │
  │  const Home = () => {                                                   │
  │    return <a href="/dashboard">Go to Dashboard</a>;                     │
  │  }                                                                      │
  └─────────────────────────────────────────────────────────────────────────┘

  SOLUTION:
    What's wrong? Using a standard HTML <a href="..."> anchor tag bypasses React Router. It will trigger a full browser refresh and HTTP request, losing all application state.
    Fix: Use React Router's <Link> component: <Link to="/dashboard">Go to Dashboard</Link>.

────────────────────────────────────────────────────────────────────────────────
  9. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  1. Bundle Size: A production app can easily reach 5MB of JavaScript. If you don't use React.lazy and Code Splitting, users on slow 3G networks will stare at a white screen for 10 seconds. Code splitting loads the login page instantly, then lazy-loads the heavy dashboard later.
  2. App Stability: Without Error Boundaries, a single null-pointer exception in a tiny user avatar component will unmount the entire React tree, leaving the user with a blank white screen.
  3. UI Integrity: Without Portals, building a tooltip in an intricate grid layout often ends with the tooltip being hidden behind other elements due to CSS overflow: hidden rules.

────────────────────────────────────────────────────────────────────────────────
  10. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

  -> File 058: React Fundamentals (For the base Virtual DOM concepts that React.memo interacts with.)
  -> File 059: React Hooks (Deep dive into useCallback which is required for React.memo to work properly.)
  -> File 062: NextJS (How Next.js replaces React Router with File-System Routing and automates code-splitting.)

================================================================================
  END OF FILE 061
================================================================================
