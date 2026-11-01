================================================================================
  FILE 037: EXPRESSJS
  Section: D - Backend Development
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  Express.js: Fast, Unopinionated, Minimalist Web Framework for Node.js
  Express.js is the de facto standard web framework for Node.js. It provides a robust set of features for web and mobile applications, abstracting the complexity of Node's native `http` module.
  Prerequisites: Node.js fundamentals, JavaScript/ES6, basic HTTP knowledge (methods, status codes).
  What you'll learn: Routing, Middleware chains, Request/Response handling, Error handling, serving static files, template engines, and structuring a production Express app.
  
  ---

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  Routing
    Determining how an application responds to a client request to a particular endpoint, which is a URI (or path) and a specific HTTP request method (GET, POST, etc.).

  Route Parameters
    Named URL segments used to capture values at their position in the URL (e.g., `/users/:id`).

  Query Strings
    Key-value pairs attached to the end of a URL after a `?` (e.g., `/search?q=express&page=1`).

  Middleware
    Functions that have access to the request object (`req`), response object (`res`), and the next middleware function (`next()`). They can modify request/response, end the cycle, or call `next()`.

  Application-Level Middleware
    Bound to an instance of `express()` using `app.use()`.

  Router-Level Middleware
    Bound to an instance of `express.Router()`.

  Built-in Middleware
    e.g., `express.json()`, `express.urlencoded()`, `express.static()`.

  Error-Handling Middleware
    Middleware with specifically four arguments `(err, req, res, next)`.

  CORS (Cross-Origin Resource Sharing)
    Security mechanism that allows or restricts requested resources on a web server depending on where the HTTP request was initiated.

  dotenv
    Module that loads environment variables from a `.env` file into `process.env`.

  Template Engine
    Allows you to use static template files in your application. At runtime, it replaces variables in a template file with actual values (e.g., EJS, Pug).

  --

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  Middleware Chain Execution Flow

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  Client Request (GET /api/users)                                        │
  │         |                                                               │
  │         v                                                               │
  │  +-------------------------------+                                      │
  │  | App-Level Middleware          |  (e.g., CORS, Helmet)                │
  │  | app.use(cors())               |                                      │
  │  +-------------------------------+                                      │
  │         | next()                                                        │
  │         v                                                               │
  │  +-------------------------------+                                      │
  │  | Built-in Middleware           |  (e.g., Body Parser)                 │
  │  | app.use(express.json())       |                                      │
  │  +-------------------------------+                                      │
  │         | next()                                                        │
  │         v                                                               │
  │  +-------------------------------+                                      │
  │  | Custom Authentication Mid     |  (Check JWT token)                   │
  │  | req.user = user               |                                      │
  │  +-------------------------------+                                      │
  │         | next()                                                        │
  │         v                                                               │
  │  +-------------------------------+                                      │
  │  | Route Handler                 |  (e.g., Database Query)              │
  │  | app.get('/api/users', ...)    |                                      │
  │  | res.json(data)                |  <--- ENDS CYCLE                     │
  │  +-------------------------------+                                      │
  │         | (If error thrown or next(err) called)                         │
  │         v                                                               │
  │  +-------------------------------+                                      │
  │  | Error Handling Middleware     |                                      │
  │  | app.use((err, req, res, next))|                                      │
  │  +-------------------------------+                                      │
  │         |                                                               │
  │         v                                                               │
  │  Client Response (200 OK / 500 Error)                                   │
  └─────────────────────────────────────────────────────────────────────────┘

---

────────────────────────────────────────────────────────────────────────────────
  5. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  Routing & Middleware Basics


  Language: javascript


  ┌──────────────────────────────────────────────────────────────────────────┐
  │  const express = require('express');                                     │
  │  const app = express();                                                  │
  │                                                                          │
  │  // 1. Built-in Middleware                                               │
  │  app.use(express.json()); // parses application/json                     │
  │                                                                          │
  │  // 2. Custom Application-Level Middleware                               │
  │  app.use((req, res, next) => {                                           │
  │      console.log(`[${new Date().toISOString()}] ${req.method} ${req.url}`);│
  │      next(); // Pass control to next middleware                          │
  │  });                                                                     │
  │                                                                          │
  │  // 3. Routing: Query Strings and Route Params                           │
  │  // GET /api/users/123?includeProfile=true                               │
  │  app.get('/api/users/:userId', (req, res) => {                           │
  │      const userId = req.params.userId;        // "123"                   │
  │      const includeProfile = req.query.includeProfile; // "true"          │
  │                                                                          │
  │      res.status(200).json({                                              │
  │          id: userId,                                                     │
  │          profileIncluded: includeProfile === 'true',                     │
  │          name: "John Doe"                                                │
  │      });                                                                 │
  │  });                                                                     │
  │                                                                          │
  │  // 4. Fallback route (404)                                              │
  │  app.use((req, res) => {                                                 │
  │      res.status(404).send('Route not found');                            │
  │  });                                                                     │
  │                                                                          │
  │  app.listen(3000, () => console.log('Server running on port 3000'));     │
  └──────────────────────────────────────────────────────────────────────────┘

  ---

────────────────────────────────────────────────────────────────────────────────
  6. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

  Full Production Express Server Setup


  Language: javascript


  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // server.js                                                            │
  │  require('dotenv').config();                                             │
  │  const express = require('express');                                     │
  │  const cors = require('cors');                                           │
  │  const helmet = require('helmet');                                       │
  │  const morgan = require('morgan'); // HTTP request logger                │
  │                                                                          │
  │  const app = express();                                                  │
  │                                                                          │
  │  // --- GLOBAL MIDDLEWARE ---                                            │
  │  app.use(helmet()); // Security headers                                  │
  │  app.use(cors({                                                          │
  │      origin: process.env.CLIENT_URL || 'http://localhost:3000',          │
  │      credentials: true                                                   │
  │  }));                                                                    │
  │  app.use(express.json());                                                │
  │  app.use(express.urlencoded({ extended: true }));                        │
  │  app.use(morgan('combined')); // Logging                                 │
  │  app.use('/static', express.static('public')); // Static files           │
  │                                                                          │
  │  // --- ROUTES ---                                                       │
  │  // Mount routers                                                        │
  │  const userRoutes = require('./routes/userRoutes');                      │
  │  app.use('/api/v1/users', userRoutes);                                   │
  │                                                                          │
  │  // Health check endpoint                                                │
  │  app.get('/health', (req, res) => {                                      │
  │      res.status(200).json({ status: 'UP', timestamp: new Date() });      │
  │  });                                                                     │
  │                                                                          │
  │  // --- ERROR HANDLING ---                                               │
  │  // 404 handler                                                          │
  │  app.use((req, res, next) => {                                           │
  │      const error = new Error(`Not Found - ${req.originalUrl}`);          │
  │      res.status(404);                                                    │
  │      next(error); // Pass to global error handler                        │
  │  });                                                                     │
  │                                                                          │
  │  // Global Error Handler (MUST have 4 params)                            │
  │  app.use((err, req, res, next) => {                                      │
  │      const statusCode = res.statusCode === 200 ? 500 : res.statusCode;   │
  │                                                                          │
  │      console.error(err.stack); // Log for server operator                │
  │                                                                          │
  │      res.status(statusCode).json({                                       │
  │          success: false,                                                 │
  │          message: err.message,                                           │
  │          stack: process.env.NODE_ENV === 'production' ? '🥞' : err.stack │
  │      });                                                                 │
  │  });                                                                     │
  │                                                                          │
  │  // --- SERVER START ---                                                 │
  │  const PORT = process.env.PORT || 5000;                                  │
  │  const server = app.listen(PORT, () => {                                 │
  │      console.log(`Server running in ${process.env.NODE_ENV} mode on port ${PORT}`);│
  │  });                                                                     │
  │                                                                          │
  │  // Graceful shutdown                                                    │
  │  process.on('SIGTERM', () => {                                           │
  │      console.log('SIGTERM received. Shutting down gracefully.');         │
  │      server.close(() => {                                                │
  │          console.log('Process terminated.');                             │
  │          process.exit(0);                                                │
  │      });                                                                 │
  │  });                                                                     │
  └──────────────────────────────────────────────────────────────────────────┘

  Recommended Project Structure


  Language: text


  ┌──────────────────────────────────────────────────────────────────────────┐
  │  /my-express-app                                                         │
  │    /config         # DB connections, env variables validation            │
  │    /controllers    # Route logic (req, res handling)                     │
  │    /middlewares    # Custom middlewares (auth, validation)               │
  │    /models         # Database models/schemas                             │
  │    /routes         # Express Routers defining paths                      │
  │    /services       # Business logic layer                                │
  │    /utils          # Helper functions                                    │
  │    /public         # Static files (images, css)                          │
  │    .env            # Environment variables                               │
  │    server.js       # Entry point                                         │
  └──────────────────────────────────────────────────────────────────────────┘

  ---

────────────────────────────────────────────────────────────────────────────────
  7. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: What is middleware in Express.js?

  ANSWER:
    Middleware are functions that execute during the lifecycle of a request to the Express server. They have access to `req`, `res`, and `next`. They can run code, modify the request/response, and end the cycle or call `next()` to pass control to the next middleware.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: How does Express handle errors?

  ANSWER:
    Express relies on an Error Handling Middleware function, distinguished by having exactly 4 parameters: `(err, req, res, next)`. When you pass an argument to `next(err)`, Express skips all remaining non-error middleware and sends the request directly to the error-handling middleware.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: What is the difference between `app.use()` and `app.get()`?

  ANSWER:
    `app.use()` mounts middleware for all HTTP methods on a specified path (default `/`). `app.get()` is an HTTP method-specific routing function that only fires for GET requests on exact paths.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: Why do we need `express.json()`?

  ANSWER:
    Raw HTTP requests send the body as a stream of bytes. `express.json()` is a body-parsing middleware that collects these bytes, parses the JSON string, and populates `req.body` with the resulting JavaScript object.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: What is CORS and how do you configure it in Express?

  ANSWER:
    Cross-Origin Resource Sharing is a browser security feature preventing a frontend from domain A making requests to an API on domain B. We configure it in Express using the `cors` middleware package to explicitly allow specific origins via HTTP headers.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: How do you structure a large Express application?

  ANSWER:
    Following MVC or layered architecture: isolate routes in `/routes`, business logic in `/services` or `/controllers`, database interaction in `/models`, and generic logic in `/middlewares` and `/utils`.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q7: How do you handle async errors in route handlers?

  ANSWER:
    Because Express 4 doesn't catch unhandled promise rejections automatically, you must wrap async code in `try/catch` and call `next(err)`, or use a wrapper library like `express-async-handler` to automatically forward async errors to `next()`. (Note: Express 5 natively handles this).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q8: What are template engines and why use them?

  ANSWER:
    Template engines like EJS or Pug allow servers to generate dynamic HTML by injecting server-side variables into static templates before sending the final HTML string to the client. Useful for Server-Side Rendered (SSR) applications.

---

────────────────────────────────────────────────────────────────────────────────
  8. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: The Hanging Request

  app.post('/api/data', (req, res, next) => {
      const data = req.body;
      if (!data.name) {
          console.log("Validation failed");
          // BUG HERE
      } else {
          res.status(200).send("Success");
      }
  });

  SOLUTION:
    What's wrong? If validation fails, the server logs the error but never responds to the client (`res.send`) or calls `next()`. The client request will hang indefinitely until it times out.
    Fix: Add `res.status(400).send("Bad Request")` or `return next(new Error("Validation failed"))`.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─
  CHALLENGE 2: Middleware Order Matters

  app.use((err, req, res, next) => {
      res.status(500).send("Something broke!");
  });
  
  app.get('/error', (req, res, next) => {
      next(new Error("Manual error"));
  });

  SOLUTION:
    What's wrong? Error handling middleware is defined *before* the routes. Express executes middleware in the order they are defined. The `/error` route throws an error, but there is no error handler *after* it to catch it.
    Fix: Always place error handling middleware at the very end of your middleware stack, after all routes.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─
  CHALLENGE 3: Unhandled Async Crash

  app.get('/users', async (req, res, next) => {
      const users = await db.query("SELECT * FROM users");
      res.json(users);
  });

  SOLUTION:
    What's wrong? If the database query throws an error (e.g., connection lost), the promise rejects. Since there's no `try/catch`, the error is unhandled, potentially crashing the Node process or returning a blank error to the client (depending on Node version).
    Fix: Wrap in `try/catch` and call `next(error)` in the catch block.

---


────────────────────────────────────────────────────────────────────────────────
  9. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  - Security: Forgetting `helmet` or `cors` exposes APIs to XSS attacks, clickjacking, and unauthorized cross-origin requests.
  - Graceful Shutdowns: Without trapping `SIGTERM`, server restarts (common in Kubernetes/Docker) will abruptly kill ongoing requests, resulting in dropped database transactions and bad user experiences.
  - Centralized Error Handling: Without a global error handler, bugs leak stack traces to users, exposing backend architecture, and APIs return inconsistent error formats to frontends.
  ---

────────────────────────────────────────────────────────────────────────────────
  10. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

  -> File 36: NodeJS Fundamentals (Understand how Express relies on Node's http module and event loop.)
  -> File 38: NodeJS PostgreSQL (Connect your Express app to a PostgreSQL database.)
  -> File 39: NodeJS Auth Security (Add JWT authentication to your Express routes.)

================================================================================
  END OF FILE 037
================================================================================
