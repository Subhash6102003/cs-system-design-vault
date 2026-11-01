================================================================================
  FILE 068: FULL-STACK CRUD APPLICATION
  Section: F - Full-Stack Integration
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  Building a Full CRUD App: React, Express, PostgreSQL
  This file details the creation of a complete Create, Read, Update, Delete (CRUD) application. You will learn RESTful API design, frontend state management for forms, optimistic UI updates, handling file uploads with Multer and S3, implementing pagination (offset vs. cursor), search and filtering, and real-time WebSockets. Prerequisite: Node.js basics, React fundamentals.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

CRUD
    Create, Read, Update, Delete. The four basic operations of persistent storage.
  RESTFUL API
    APIs designed around HTTP verbs (GET, POST, PUT/PATCH, DELETE) acting on resources (URLs).
  OPTIMISTIC UI
    Updating the UI immediately upon user action, assuming the server request will succeed, to provide a fast user experience.
  MULTER
    Node.js middleware for handling multipart/form-data, primarily used for uploading files.
  FORMDATA
    A browser API used to construct key/value pairs representing form fields and their values, specifically needed for file uploads.
  OFFSET PAGINATION
    Paging using LIMIT and OFFSET in SQL.
  CURSOR PAGINATION
    Paging using a unique identifier (like ID or timestamp) as a pointer to fetch the next set of results.
  DEBOUNCING
    A programming practice used to ensure that time-consuming tasks do not fire so often (e.g., search API calls as a user types).
  WEBSOCKET
    Full-duplex communication channel for real-time updates.

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

┌─────────────────────────────────────────────────────────────────────────┐
  │  PAGINATION TRADE-OFFS                                                  │
  │                                                                         │
  │  OFFSET PAGINATION                                                      │
  │  Query: SELECT * FROM items LIMIT 10 OFFSET 1000                        │
  │  Issues:                                                                │
  │  - Slow on large offsets (DB must scan & discard 1000 rows).            │
  │  - Inconsistent if items are added/deleted (shifting rows).             │
  │                                                                         │
  │  CURSOR PAGINATION                                                      │
  │  Query: SELECT * FROM items WHERE id > 1000 LIMIT 10                    │
  │  Benefits:                                                              │
  │  - O(1) performance using indexes.                                      │
  │  - Stable results even if data is mutating.                             │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  4. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

[Language: JavaScript]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // File Upload Handling (Backend)                                       │
  │                                                                          │
  │  const multer = require('multer');                                       │
  │  const upload = multer({ dest: 'uploads/' }); // Stores files in local 'uploads' dir│
  │                                                                          │
  │  app.post('/api/upload', upload.single('avatar'), (req, res) => {        │
  │      // req.file contains file metadata (original name, path, size)      │
  │      // req.body contains other text fields                              │
  │      if (!req.file) return res.status(400).send('No file uploaded.');    │
  │                                                                          │
  │      const fileUrl = `/uploads/${req.file.filename}`;                    │
  │      res.json({ url: fileUrl });                                         │
  │  });                                                                     │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

  [Language: TypeScript/React]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Debounced Search (Frontend React)                                    │
  │                                                                          │
  │  import React, { useState, useEffect } from 'react';                     │
  │                                                                          │
  │  function SearchComponent() {                                            │
  │      const [query, setQuery] = useState('');                             │
  │      const [results, setResults] = useState([]);                         │
  │                                                                          │
  │      useEffect(() => {                                                   │
  │          const timeoutId = setTimeout(async () => {                      │
  │              if (query) {                                                │
  │                  const res = await fetch(`/api/search?q=${query}`);      │
  │                  const data = await res.json();                          │
  │                  setResults(data);                                       │
  │              }                                                           │
  │          }, 500); // 500ms debounce                                      │
  │                                                                          │
  │          return () => clearTimeout(timeoutId); // Cleanup on re-render   │
  │      }, [query]);                                                        │
  │                                                                          │
  │      return <input value={query} onChange={(e) => setQuery(e.target.value)} />;│
  │  }                                                                       │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

[Language: TypeScript/React]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Optimistic UI Update with React & Fetch                              │
  │                                                                          │
  │  function TodoList({ todos, setTodos }) {                                │
  │      const toggleTodo = async (id, currentStatus) => {                   │
  │          // 1. Optimistic Update (Immediate UI change)                   │
  │          const previousTodos = [...todos];                               │
  │          setTodos(todos.map(t => t.id === id ? { ...t, completed: !t.completed } : t));│
  │                                                                          │
  │          try {                                                           │
  │              // 2. Network Request                                       │
  │              const response = await fetch(`/api/todos/${id}`, {          │
  │                  method: 'PATCH',                                        │
  │                  headers: { 'Content-Type': 'application/json' },        │
  │                  body: JSON.stringify({ completed: !currentStatus })     │
  │              });                                                         │
  │                                                                          │
  │              if (!response.ok) throw new Error('Server update failed');  │
  │          } catch (error) {                                               │
  │              // 3. Revert on failure                                     │
  │              console.error(error);                                       │
  │              setTodos(previousTodos);                                    │
  │              alert("Failed to update status. Reverting.");               │
  │          }                                                               │
  │      };                                                                  │
  │                                                                          │
  │      return (                                                            │
  │          <ul>                                                            │
  │              {todos.map(todo => (                                        │
  │                  <li key={todo.id} onClick={() => toggleTodo(todo.id, todo.completed)}>│
  │                      {todo.completed ? '✅' : '❌'} {todo.title}           │
  │                  </li>                                                   │
  │              ))}                                                         │
  │          </ul>                                                           │
  │      );                                                                  │
  │  }                                                                       │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

Q1: Explain the difference between PUT and PATCH.

  ANSWER:
    PUT replaces the entire resource. PATCH partially updates the resource.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: Why is cursor-based pagination preferred over offset-based for infinite scroll?

  ANSWER:
    Offset requires the database to scan all rows up to the offset, causing O(N) performance degradation as pages increase. Cursor uses an indexed column (like ID) for O(1) performance. Also, offset suffers from duplicate/missing items if data is added/deleted during pagination.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: What is Optimistic UI?

  ANSWER:
    A frontend pattern where the UI is updated immediately assuming the network request will succeed. If it fails, the UI is rolled back. It makes the app feel extremely fast.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: How do you upload a file using React and fetch?

  ANSWER:
    Use the FormData API, append the file to it, and pass it as the body of the fetch request. Do *not* set the Content-Type header manually; let the browser set it to multipart/form-data with the correct boundary.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: What is debouncing and why is it used in search?

  ANSWER:
    Debouncing delays the execution of a function until a certain amount of idle time has passed. In search, it prevents firing an API call on every keystroke, reducing server load.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: How do you handle syncing search state with the URL?

  ANSWER:
    Use React Router's useSearchParams to store the search query in the URL. This allows users to share the link or refresh the page without losing search context.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q7: What is Multer?

  ANSWER:
    A node.js middleware for handling multipart/form-data, which is primarily used for uploading files.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q8: How do WebSockets fit into a standard CRUD app?

  ANSWER:
    After a standard HTTP POST/PUT/DELETE, the server broadcasts an event via WebSockets to all connected clients, allowing their UI to update in real-time without polling.

────────────────────────────────────────────────────────────────────────────────
  7. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

CHALLENGE 1: Riddle

  I pretend the server is fast, lying to the user's eyes, but if the network fails, I must confess and undo my lies. What am I?

  SOLUTION:
    Optimistic UI.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─


  CHALLENGE 2: Riddle

  I slice through massive tables in O(1) time, refusing to scan from the start. Give me an ID, and I'll give you the next page. What am I?

  SOLUTION:
    Cursor Pagination.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─


  CHALLENGE 3: 

  // React frontend file upload
  const formData = new FormData();
  formData.append('file', fileInput);
  fetch('/upload', {
      method: 'POST',
      headers: { 'Content-Type': 'multipart/form-data' }, // What's wrong?
      body: formData
  });

  SOLUTION:
    Manually setting Content-Type for FormData breaks the upload because the browser needs to automatically append a unique boundary string to separate the file parts. Remove the headers property completely.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─


  CHALLENGE 4: 

  -- Database query for infinite scroll
  SELECT * FROM posts ORDER BY created_at DESC LIMIT 10 OFFSET 50;

  SOLUTION:
    If 5 new posts are added while the user is reading page 5, requesting OFFSET 50 for page 6 will return 5 duplicated posts that were shifted down. Fix: Use cursor pagination (WHERE created_at < ?).

────────────────────────────────────────────────────────────────────────────────
  8. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  CRUD apps are the foundation of most software. Understanding pagination ensures your app doesn't crash the database when users reach 1 million records. Implementing optimistic UI and debouncing separates a clunky, slow application from a professional, highly responsive product.

────────────────────────────────────────────────────────────────────────────────
  9. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

-> File 066: 066 FullStack Architecture (related topic)
  -> File 071: 071 FullStack Security (Validating input data in CRUD.)

================================================================================
  END OF FILE 068
================================================================================
