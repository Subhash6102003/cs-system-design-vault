================================================================================
  FILE 059: REACT HOOKS DEEP DIVE
  Section: E - Frontend Development
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  React Hooks: State, Side Effects, and Refs in Functional Components

  Introduced in React 16.8, Hooks revolutionized React by allowing functional components to manage state and side effects, entirely replacing class components. Hooks make it possible to extract and reuse stateful logic cleanly. In this guide, we dive deep into the essential hooks: useState, useEffect, useContext, useRef, and performance hooks like useMemo and useCallback. Mastering hooks—especially understanding dependency arrays and avoiding stale closures—is the single most important skill for a modern React developer.

  Prerequisites: Solid understanding of React Fundamentals (Components, Props, JSX) and JavaScript Closures.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  Rules of Hooks
    1. Only call hooks at the top level (never inside loops, conditions, or nested functions). This ensures hooks are called in the exact same order every render.
    2. Only call hooks from React Function Components or Custom Hooks.

  useState(initialValue)
    Returns a stateful value and a function to update it. Triggers a re-render when the setter is called.

  useEffect(setup, dependencies?)
    Lets you perform side effects (data fetching, DOM manipulation, timers).
    No dependency array: Runs after every render.
    Empty array []: Runs only once (on mount).
    With dependencies [prop, state]: Runs on mount and whenever a dependency changes.
    Cleanup function: The return value of the setup function, runs before the component unmounts and before the effect runs again.

  useContext(Context)
    Accepts a context object (created by React.createContext) and returns the current context value. Solves "prop drilling".

  useRef(initialValue)
    Returns a mutable ref object whose .current property is initialized to the passed argument.
    Unlike state, mutating .current does not cause a re-render. Perfect for storing DOM references or mutable values across renders (like interval IDs).

  useMemo(calculateValue, dependencies)
    Caches the result of an expensive calculation between renders.

  useCallback(fn, dependencies)
    Caches a function definition between renders. Usually used to prevent unnecessary re-renders of child components wrapped in React.memo.

  useReducer(reducer, initialArg)
    An alternative to useState for complex state logic (similar to Redux).

  Custom Hooks
    JavaScript functions whose names start with use and call other hooks. They encapsulate reusable stateful logic.

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  The useEffect Lifecycle

  ┌─────────────────────────────────────────────────────────────────────────┐
  │    Component Renders (Mount)                                            │
  │             |                                                           │
  │             v                                                           │
  │    DOM is updated visually                                              │
  │             |                                                           │
  │             v                                                           │
  │    Run useEffect(setup)  <--------------------+                         │
  │             |                                 |                         │
  │    (Time passes, state/props change)          |                         │
  │             |                                 |                         │
  │    Component Re-renders                       |                         │
  │             |                                 |                         │
  │    DOM is updated visually                    |                         │
  │             |                                 |                         │
  │    Run useEffect(cleanup) from PREVIOUS run   |                         │
  │             |                                 |                         │
  │             +---------------------------------+                         │
  │                                                                         │
  │    (When Component Unmounts)                                            │
  │             |                                                           │
  │    Run final useEffect(cleanup)                                         │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  The Core Hooks (State, Ref, Effect)

  [Language: Jsx]

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  import React, { useState, useEffect, useRef } from 'react';            │
  │                                                                         │
  │  const Timer = () => {                                                  │
  │    const [seconds, setSeconds] = useState(0);                           │
  │                                                                         │
  │    // useRef to persist the interval ID across renders without causing re-renders │
  │    const intervalRef = useRef(null);                                    │
  │                                                                         │
  │    // useRef to access a DOM element directly                           │
  │    const headerRef = useRef(null);                                      │
  │                                                                         │
  │    useEffect(() => {                                                    │
  │      // 1. Setup: Start the timer on mount                              │
  │      intervalRef.current = setInterval(() => {                          │
  │        // Use the functional state update to prevent Stale Closures     │
  │        setSeconds(prev => prev + 1);                                    │
  │      }, 1000);                                                          │
  │                                                                         │
  │      // Focus the header programmatically                               │
  │      if (headerRef.current) headerRef.current.style.color = 'blue';     │
  │                                                                         │
  │      // 2. Cleanup: Clear timer on unmount                              │
  │      return () => {                                                     │
  │        clearInterval(intervalRef.current);                              │
  │      };                                                                 │
  │    }, []); // Empty array = run only on mount                           │
  │                                                                         │
  │    return (                                                             │
  │      <div>                                                              │
  │        <h2 ref={headerRef}>Timer: {seconds}s</h2>                       │
  │        <button onClick={() => clearInterval(intervalRef.current)}>      │
  │          Stop Timer                                                     │
  │        </button>                                                        │
  │      </div>                                                             │
  │    );                                                                   │
  │  };                                                                     │
  └─────────────────────────────────────────────────────────────────────────┘

  useMemo and useCallback for Performance

  [Language: Jsx]

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  import React, { useState, useMemo, useCallback } from 'react';         │
  │                                                                         │
  │  // Child wrapped in React.memo (only re-renders if props change)       │
  │  const ExpensiveList = React.memo(({ items, onAction }) => {            │
  │    console.log("ExpensiveList rendered");                               │
  │    return (                                                             │
  │      <ul>                                                               │
  │        {items.map(i => <li key={i} onClick={onAction}>{i}</li>)}        │
  │      </ul>                                                              │
  │    );                                                                   │
  │  });                                                                    │
  │                                                                         │
  │  export const ParentComponent = () => {                                 │
  │    const [count, setCount] = useState(0);                               │
  │    const [darkMode, setDarkMode] = useState(false);                     │
  │                                                                         │
  │    // 1. useMemo caches the array so it's not recreated every render    │
  │    // Otherwise, [] !== [] in memory, causing Child to re-render        │
  │    const items = useMemo(() => ['A', 'B', 'C'], []);                    │
  │                                                                         │
  │    // 2. useCallback caches the function definition                     │
  │    // Without this, a new function is created every time count changes, │
  │    // breaking React.memo on the child.                                 │
  │    const handleAction = useCallback(() => {                             │
  │      console.log("Action triggered");                                   │
  │    }, []); // empty deps = function never changes                       │
  │                                                                         │
  │    return (                                                             │
  │      <div style={{ background: darkMode ? '#333' : '#FFF' }}>           │
  │        <button onClick={() => setCount(c => c + 1)}>Count: {count}</button> │
  │        <button onClick={() => setDarkMode(d => !d)}>Toggle Theme</button>│
  │                                                                         │
  │        <ExpensiveList items={items} onAction={handleAction} />          │
  │      </div>                                                             │
  │    );                                                                   │
  │  };                                                                     │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

  Custom Hook: useFetch
  A robust custom hook for fetching data, managing loading/error states, and handling component unmounting/cancellations to prevent memory leaks.

  [Language: Jsx]

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  import { useState, useEffect } from 'react';                           │
  │                                                                         │
  │  export function useFetch(url) {                                        │
  │    const [data, setData] = useState(null);                              │
  │    const [loading, setLoading] = useState(true);                        │
  │    const [error, setError] = useState(null);                            │
  │                                                                         │
  │    useEffect(() => {                                                    │
  │      // 1. Create AbortController to cancel requests if component unmounts │
  │      const abortController = new AbortController();                     │
  │                                                                         │
  │      // Reset states on URL change                                      │
  │      setLoading(true);                                                  │
  │      setError(null);                                                    │
  │                                                                         │
  │      const fetchData = async () => {                                    │
  │        try {                                                            │
  │          const response = await fetch(url, { signal: abortController.signal }); │
  │                                                                         │
  │          if (!response.ok) {                                            │
  │            throw new Error(`HTTP error: ${response.status}`);           │
  │          }                                                              │
  │                                                                         │
  │          const json = await response.json();                            │
  │          setData(json);                                                 │
  │        } catch (err) {                                                  │
  │          // Ignore errors caused by intentional aborts                  │
  │          if (err.name !== 'AbortError') {                               │
  │            setError(err.message);                                       │
  │          }                                                              │
  │        } finally {                                                      │
  │          setLoading(false);                                             │
  │        }                                                                │
  │      };                                                                 │
  │                                                                         │
  │      fetchData();                                                       │
  │                                                                         │
  │      // 2. Cleanup function                                             │
  │      return () => {                                                     │
  │        abortController.abort(); // Cancel the fetch on unmount or url change │
  │      };                                                                 │
  │    }, [url]); // Re-run effect if the URL changes                       │
  │                                                                         │
  │    return { data, loading, error };                                     │
  │  }                                                                      │
  │                                                                         │
  │  // === Usage ===                                                       │
  │  // const { data: users, loading, error } = useFetch('/api/users');     │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  7. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: What are the rules of Hooks?

  ANSWER:
    Only call hooks at the top level of a component (not in loops or conditionals). Only call hooks from React function components or custom hooks.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: Why can't you put hooks inside conditional statements?

  ANSWER:
    React relies on the exact order in which hooks are called to associate internal state with the correct hook. If a condition skips a hook, the order shifts, causing catastrophic bugs in state mapping.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: Explain the difference between useEffect and useLayoutEffect.

  ANSWER:
    useEffect is asynchronous and runs after the browser has painted the DOM. useLayoutEffect runs synchronously before the browser paints. It is used exclusively to read DOM measurements and synchronously re-render to prevent UI flickering.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: What is a Stale Closure in React?

  ANSWER:
    It happens when a closure (like inside useEffect or setTimeout) captures a state variable at a specific point in time, but the state later updates. Because the closure is "stuck" with the old value, it behaves incorrectly. Solved by updating dependency arrays or using functional state updates (setCount(prev => prev + 1)).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: When should you use useRef instead of useState?

  ANSWER:
    Use useState when you want the UI to update when the data changes. Use useRef for mutable values you want to track across renders without triggering a re-render (e.g., keeping track of a setTimeout ID, previous state, or directly accessing DOM elements).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: What does useMemo do and when should you use it?

  ANSWER:
    It memoizes (caches) the result of a calculation. Use it only for computationally expensive operations (like filtering a massive array) or when generating an object/array that is passed as a prop to a React.memo child, to prevent unnecessary re-renders.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q7: What is the purpose of the Cleanup function in useEffect?

  ANSWER:
    To clean up side effects (like clearing intervals, removing event listeners, or aborting fetch requests) to prevent memory leaks and unexpected behavior when a component unmounts or before the effect runs again.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q8: How does useCallback differ from useMemo?

  ANSWER:
    useMemo caches a value returned by a function. useCallback caches the function definition itself.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q9: Can you force a functional component to re-render?

  ANSWER:
    Yes, by updating a state variable. A common hack is const [_, forceUpdate] = useState(0); forceUpdate(n => n + 1);, though it usually indicates bad architecture.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q10: How do you build a custom hook?

  ANSWER:
    Create a standard JavaScript function that starts with "use" (e.g., useWindowSize). Inside it, call native hooks like useState and useEffect, and return whatever data/functions the consuming component needs.

────────────────────────────────────────────────────────────────────────────────
  8. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: The Infinite Loop

  [Language: Jsx]

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  const UserProfile = ({ userId }) => {                                  │
  │    const [user, setUser] = useState(null);                              │
  │                                                                         │
  │    useEffect(() => {                                                    │
  │      fetch(`/api/users/${userId}`)                                      │
  │        .then(res => res.json())                                         │
  │        .then(data => setUser(data));                                    │
  │    });                                                                  │
  │                                                                         │
  │    return <div>{user?.name}</div>;                                      │
  │  }                                                                      │
  └─────────────────────────────────────────────────────────────────────────┘

  SOLUTION:
    What's wrong? The useEffect has NO dependency array. It runs after every render. Fetching data updates state -> state update triggers a re-render -> re-render triggers useEffect -> fetches data -> updates state... Infinite loop crashing the browser!
    Fix: Add a dependency array: useEffect(() => { ... }, [userId]);

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 2: The Stale Interval

  [Language: Jsx]

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  const Counter = () => {                                                │
  │    const [count, setCount] = useState(0);                               │
  │                                                                         │
  │    useEffect(() => {                                                    │
  │      const id = setInterval(() => {                                     │
  │        setCount(count + 1);                                             │
  │      }, 1000);                                                          │
  │      return () => clearInterval(id);                                    │
  │    }, []);                                                              │
  │                                                                         │
  │    return <h1>{count}</h1>;                                             │
  │  }                                                                      │
  └─────────────────────────────────────────────────────────────────────────┘

  SOLUTION:
    What's wrong? Stale closure. Because the dependency array is [], the effect only runs once. Inside the interval closure, count is captured at its initial value of 0. It will repeatedly do setCount(0 + 1), so the timer will permanently show 1.
    Fix: Use functional state update: setCount(prevCount => prevCount + 1).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 3: The Object Dependency Trap

  [Language: Jsx]

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  const Configurator = () => {                                           │
  │    const [data, setData] = useState('');                                │
  │                                                                         │
  │    // Object created fresh on every render                              │
  │    const config = { theme: 'dark', retries: 3 };                        │
  │                                                                         │
  │    useEffect(() => {                                                    │
  │      console.log("Config changed!");                                    │
  │    }, [config]);                                                        │
  │  }                                                                      │
  └─────────────────────────────────────────────────────────────────────────┘

  SOLUTION:
    What's wrong? config is a new object reference in memory on every render. Because {} !== {}, React thinks the dependency has changed, causing the effect to run on every render unnecessarily.
    Fix: Move config outside the component if it's static, OR wrap it in useMemo(() => ({ theme: 'dark' }), []).

────────────────────────────────────────────────────────────────────────────────
  9. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  1. Memory Leaks: In a large Single Page Application (SPA), navigating between pages without cleaning up intervals or fetch requests in useEffect will quickly degrade browser performance and crash the tab.
  2. Performance Optimization: Unnecessary re-renders are the #1 cause of slow React apps. Proper use of useMemo, useCallback, and understanding object references in dependency arrays are mandatory for rendering lists of complex data at 60fps.
  3. Code Reusability: Custom hooks (like useAuth, useForm, useFetch) allow teams to abstract complex business logic out of components, resulting in drastically cleaner and more testable codebases.

────────────────────────────────────────────────────────────────────────────────
  10. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

  -> File 058: React Fundamentals (The foundational knowledge of State and Props.)
  -> File 060: React StateManagement (When useState isn't enough, moving to Context, Redux, or Zustand.)
  -> File 055: JavaScript DeepDive (Understanding the Closures that govern how Hooks work internally.)

================================================================================
  END OF FILE 059
================================================================================
