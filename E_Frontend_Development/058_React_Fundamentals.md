================================================================================
  FILE 058: REACT FUNDAMENTALS
  Section: E - Frontend Development
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  React Fundamentals: JSX, Components, and the Virtual DOM

  React is a declarative, component-based JavaScript library for building user interfaces. Instead of manually manipulating the DOM (imperative programming), React allows you to define what the UI should look like for any given state, and it efficiently updates the DOM to match. This file covers the core philosophy of React: JSX syntax, functional components vs. legacy class components, Props for data passing, local State, and the mechanics of the Virtual DOM and Reconciliation algorithm. Mastering these fundamentals is critical before moving on to complex state management and Hooks.

  Prerequisites: JavaScript ES6+ (Arrow functions, Destructuring, Modules), HTML/CSS basics.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  Declarative vs Imperative
    React is declarative (you declare what you want: <h1>{title}</h1>). Vanilla JS is imperative (you write how to do it: el = document.createElement('h1'); el.innerText = title; body.appendChild(el)).

  Component-Based Architecture
    UIs are broken down into small, reusable, independent pieces called Components.

  JSX (JavaScript XML)
    A syntax extension for JS that looks like HTML. It is compiled by Babel into React.createElement() calls.
    Rules: Must return a single root element (or Fragment <>), use className instead of class, and camelCase for inline styles and event handlers.

  Functional Components
    Modern React components are just JS functions that accept props and return JSX. (Legacy React used ES6 Classes).

  Props (Properties)
    Read-only data passed from a parent component to a child component. This enforces a unidirectional (top-down) data flow.

  State
    Data managed within a component that changes over time. When state changes, React re-renders the component.

  Virtual DOM (VDOM)
    An in-memory, lightweight javascript object representation of the actual DOM.

  Reconciliation & Diffing Algorithm
    When state changes, React creates a new VDOM. It compares (diffs) the new VDOM with the old VDOM. It then calculates the minimum number of actual DOM updates required and applies them efficiently.

  Keys
    A special string attribute you must include when creating arrays of elements. Keys help React identify which items have changed, been added, or been removed, optimizing the diffing process.

  Synthetic Events
    React's cross-browser wrapper around native browser events (e.g., onClick, onChange).

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  Component Tree & Unidirectional Data Flow

  ┌─────────────────────────────────────────────────────────────────────────┐
  │                    [App] (State: user)                                  │
  │                   /     \                                               │
  │      props: user /       \ props: theme                                 │
  │                 v         v                                             │
  │        [Navbar]          [MainContent]                                  │
  │                            /      \                                     │
  │                           /        \                                    │
  │                [Sidebar]          [ArticleList] (State: articles)       │
  │                                         |                               │
  │                                         v props: articleData            │
  │                                    [ArticleItem]                        │
  └─────────────────────────────────────────────────────────────────────────┘

  Virtual DOM Diffing Process

  ┌─────────────────────────────────────────────────────────────────────────┐
  │    State Change Occurs!                                                 │
  │             |                                                           │
  │             v                                                           │
  │    1. Generate New VDOM  -->  [div (color: red)]                        │
  │                                  |                                      │
  │    2. Diff against Old VDOM -> [div (color: blue)]                      │
  │                                  |                                      │
  │    3. Calculate Delta    -->  "Change color from blue to red"           │
  │                                  |                                      │
  │    4. Update Actual DOM  -->  DOM.element.style.color = 'red';          │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  JSX, Props, and List Rendering

  [Language: Jsx]

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  import React from 'react';                                             │
  │                                                                         │
  │  // 1. Child Component receiving props                                  │
  │  const UserCard = ({ name, role, isActive }) => {                       │
  │    return (                                                             │
  │      // className instead of class                                      │
  │      <div className={`card ${isActive ? 'active' : 'inactive'}`}>       │
  │        <h3>{name}</h3>                                                  │
  │        <p>Role: {role}</p>                                              │
  │        {/* Conditional Rendering */}                                    │
  │        {isActive && <span className="badge">Online</span>}              │
  │      </div>                                                             │
  │    );                                                                   │
  │  };                                                                     │
  │                                                                         │
  │  // 2. Parent Component rendering a list                                │
  │  const UserList = () => {                                               │
  │    const users = [                                                      │
  │      { id: 'u1', name: 'Alice', role: 'Admin', active: true },          │
  │      { id: 'u2', name: 'Bob', role: 'User', active: false }             │
  │    ];                                                                   │
  │                                                                         │
  │    return (                                                             │
  │      <section>                                                          │
  │        <h2>User Directory</h2>                                          │
  │        <div className="grid">                                           │
  │          {users.map((user) => (                                         │
  │            // The 'key' prop is mandatory for arrays!                   │
  │            <UserCard                                                    │
  │              key={user.id}                                              │
  │              name={user.name}                                           │
  │              role={user.role}                                           │
  │              isActive={user.active}                                     │
  │            />                                                           │
  │          ))}                                                            │
  │        </div>                                                           │
  │      </section>                                                         │
  │    );                                                                   │
  │  };                                                                     │
  │                                                                         │
  │  export default UserList;                                               │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

  Interactive Todo Component (State + Event Handling)
  This component demonstrates state management (via useState, previewing next chapter), synthetic event handling, form submission, and proper state immutability.

  [Language: Jsx]

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  import React, { useState } from 'react';                               │
  │  import './TodoApp.css'; // Assume CSS exists                           │
  │                                                                         │
  │  export const TodoApp = () => {                                         │
  │    // Local state for the input field                                   │
  │    const [inputValue, setInputValue] = useState('');                    │
  │                                                                         │
  │    // Local state for the list of todos                                 │
  │    const [todos, setTodos] = useState([                                 │
  │      { id: 1, text: 'Learn React VDOM', completed: true },              │
  │      { id: 2, text: 'Master Hooks', completed: false }                  │
  │    ]);                                                                  │
  │                                                                         │
  │    // Handle Input Change                                               │
  │    const handleInputChange = (e) => {                                   │
  │      setInputValue(e.target.value);                                     │
  │    };                                                                   │
  │                                                                         │
  │    // Handle Form Submit                                                │
  │    const handleAddTodo = (e) => {                                       │
  │      e.preventDefault(); // Prevent page reload                         │
  │                                                                         │
  │      if (inputValue.trim() === '') return;                              │
  │                                                                         │
  │      const newTodo = {                                                  │
  │        id: Date.now(), // Simple unique ID generator                    │
  │        text: inputValue,                                                │
  │        completed: false                                                 │
  │      };                                                                 │
  │                                                                         │
  │      // ALWAYS update arrays/objects immutably using the spread operator│
  │      setTodos((prevTodos) => [...prevTodos, newTodo]);                  │
  │      setInputValue(''); // Clear input                                  │
  │    };                                                                   │
  │                                                                         │
  │    // Handle Delete (Immutable removal)                                 │
  │    const handleDelete = (idToRemove) => {                               │
  │      setTodos((prevTodos) => prevTodos.filter(todo => todo.id !== idToRemove)); │
  │    };                                                                   │
  │                                                                         │
  │    // Handle Toggle (Immutable update)                                  │
  │    const handleToggle = (idToToggle) => {                               │
  │      setTodos((prevTodos) =>                                            │
  │        prevTodos.map(todo =>                                            │
  │          todo.id === idToToggle                                         │
  │            ? { ...todo, completed: !todo.completed }                    │
  │            : todo                                                       │
  │        )                                                                │
  │      );                                                                 │
  │    };                                                                   │
  │                                                                         │
  │    return (                                                             │
  │      <div className="todo-container">                                   │
  │        <h2>My Tasks</h2>                                                │
  │                                                                         │
  │        <form onSubmit={handleAddTodo} className="todo-form">            │
  │          <input                                                         │
  │            type="text"                                                  │
  │            value={inputValue}                                           │
  │            onChange={handleInputChange}                                 │
  │            placeholder="What needs to be done?"                         │
  │            aria-label="New Todo Input"                                  │
  │          />                                                             │
  │          <button type="submit">Add</button>                             │
  │        </form>                                                          │
  │                                                                         │
  │        <ul className="todo-list">                                       │
  │          {/* Conditional rendering if array is empty */}                 │
  │          {todos.length === 0 && <p>No tasks left! 🎉</p>}               │
  │                                                                         │
  │          {todos.map((todo) => (                                         │
  │            <li key={todo.id} className={todo.completed ? 'completed' : ''}> │
  │              <input                                                     │
  │                type="checkbox"                                          │
  │                checked={todo.completed}                                 │
  │                onChange={() => handleToggle(todo.id)}                   │
  │              />                                                         │
  │              <span>{todo.text}</span>                                   │
  │              <button                                                    │
  │                onClick={() => handleDelete(todo.id)}                    │
  │                aria-label={`Delete ${todo.text}`}                       │
  │              >                                                          │
  │                ❌                                                       │
  │              </button>                                                  │
  │            </li>                                                        │
  │          ))}                                                            │
  │        </ul>                                                            │
  │      </div>                                                             │
  │    );                                                                   │
  │  };                                                                     │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  7. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: What is the Virtual DOM, and why is it fast?

  ANSWER:
    The Virtual DOM is a lightweight JavaScript representation of the actual DOM. It's fast because manipulating JS objects is inherently much faster than repainting the actual browser DOM. React batches updates and applies only the calculated differences (reconciliation) to the real DOM, minimizing expensive layout/paint operations.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: What is the difference between Element and Component?

  ANSWER:
    An Element is a plain object describing what you want to see on the screen (e.g., <div /> which Babel turns into React.createElement('div')). A Component is a function (or class) that accepts props and returns React Elements.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: Why do we need the key prop when mapping over arrays in React?

  ANSWER:
    Keys help React's reconciliation algorithm uniquely identify elements. If an item is added or removed from the middle of an array, keys prevent React from destroying and recreating every subsequent element, drastically improving performance and preventing bugs with component state.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: Can you mutate State directly (e.g., this.state.name = 'Bob')? Why or why not?

  ANSWER:
    No. You must use the state setter function (setState or setSomething). Mutating state directly bypasses React's lifecycle and will NOT trigger a re-render, leaving your UI out of sync with your data.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: Explain the difference between Props and State.

  ANSWER:
    Props are arguments passed from a parent to a child; they are read-only (immutable) from the child's perspective. State is local, private data managed entirely within the component that can change over time.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: What is JSX? Is it required to use React?

  ANSWER:
    JSX is syntax sugar for React.createElement(). It looks like HTML but lives in JS. It is not strictly required—you can write React using pure JS functions—but nobody does this because JSX is infinitely more readable.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q7: What are Synthetic Events?

  ANSWER:
    A cross-browser wrapper around the browser's native event system. It normalizes events so they behave identically across Chrome, Firefox, Safari, etc., and implements Event Pooling (though pooling was removed in React 17 for better async behavior).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q8: What is Lifting State Up?

  ANSWER:
    When two sibling components need to share or communicate data, you move (lift) their shared state to their closest common parent component and pass the state down via props.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q9: Why should you avoid using array indexes as key props?

  ANSWER:
    If the array can be reordered, filtered, or prepended to, using indexes causes React to confuse elements. A deleted item's index shifts to the next item, which might cause React to render the wrong state for the wrong element.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q10: What is a React Fragment?

  ANSWER:
    <React.Fragment> or <> is a feature that allows you to group a list of children without adding an extra DOM node (like a wrapper <div>) to the HTML output.

────────────────────────────────────────────────────────────────────────────────
  8. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: The Adjacent Elements

  [Language: Jsx]

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  const Header = () => {                                                 │
  │    return (                                                             │
  │      <h1>Title</h1>                                                     │
  │      <h2>Subtitle</h2>                                                  │
  │    );                                                                   │
  │  }                                                                      │
  └─────────────────────────────────────────────────────────────────────────┘

  SOLUTION:
    What's wrong? A React component must return a single root element. Babel cannot compile two adjacent elements because it translates to two adjacent return values in JS, which is invalid.
    Fix: Wrap them in a fragment <> ... </> or a <div>.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 2: The Direct Mutation

  [Language: Jsx]

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  const [items, setItems] = useState(['Apple', 'Banana']);               │
  │  const addItem = () => {                                                │
  │    items.push('Orange');                                                │
  │    setItems(items);                                                     │
  │  };                                                                     │
  └─────────────────────────────────────────────────────────────────────────┘

  SOLUTION:
    What's wrong? push mutates the original array in memory. When setItems(items) is called, React checks if the new reference is the same as the old reference (using Object.is). Since it is the exact same array in memory, React thinks nothing changed and will NOT re-render.
    Fix: Use spread syntax to create a new array reference: setItems([...items, 'Orange']);

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 3: The Missing Return

  [Language: Jsx]

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  const NameList = ({ names }) => {                                      │
  │    return (                                                             │
  │      <ul>                                                               │
  │        {names.map(name => {                                             │
  │          <li key={name}>{name}</li>                                     │
  │        })}                                                              │
  │      </ul>                                                              │
  │    );                                                                   │
  │  }                                                                      │
  └─────────────────────────────────────────────────────────────────────────┘

  SOLUTION:
    What's wrong? The arrow function inside map uses curly braces {} but lacks a return keyword. It returns undefined, rendering nothing.
    Fix: Use implicit return names.map(name => <li...>) or add the return keyword inside the curly braces.

────────────────────────────────────────────────────────────────────────────────
  9. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  1. Component Reusability: Breaking UI into small components (Buttons, Inputs, Cards) means you write code once and reuse it across your whole app, ensuring visual consistency and drastically reducing bug surface area.
  2. Performance Check: Understanding the Virtual DOM and Reconciliation is key to diagnosing a slow React app. If you don't understand how React diffs trees, you will inadvertently cause massive, unnecessary re-renders in production.
  3. Predictability: Unidirectional data flow (props down, events up) makes debugging state bugs significantly easier compared to two-way data binding (like Angular 1.x), where state can mutate from anywhere.

────────────────────────────────────────────────────────────────────────────────
  10. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

  -> File 054: JavaScript ES6Plus (Destructuring and Spread operators (heavily used in React state).)
  -> File 059: React Hooks (Deep dive into useState, useEffect, and component lifecycle.)
  -> File 061: React Advanced (Advanced performance optimization (React.memo) to bypass unnecessary Reconciliation.)

================================================================================
  END OF FILE 058
================================================================================
