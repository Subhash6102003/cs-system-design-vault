================================================================================
  FILE 066: FULL-STACK ARCHITECTURE
  Section: F - Full-Stack Integration
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  Full-Stack Architecture: Patterns, Protocols, and Project Structure
  This file explores the core architectural decisions required when building modern full-stack applications. You will learn the tradeoffs between Monoliths, Modular Monoliths, and Microservices, how to structure your frontend and backend (MVC, MVP, MVVM, 3-tier), the protocols used for communication (REST, GraphQL, WebSockets, SSE), and how to manage your code repository (Monorepo vs. Polyrepo). Prerequisite: Basic understanding of web development (HTTP, client-server model).

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

MONOLITH
    A software application designed without distinguishable modularity. All logic (UI, business, data access) resides in a single unified codebase and deployment unit.
  MICROSERVICES
    An architectural style that structures an application as a collection of small, autonomous, loosely coupled services, each running in its own process and communicating via lightweight mechanisms.
  MODULAR MONOLITH
    A monolithic application composed of loosely coupled, well-defined modules.
  MVC (MODEL-VIEW-CONTROLLER)
    A design pattern dividing an application into three interconnected parts: Model (data), View (UI), and Controller (logic).
  MVP (MODEL-VIEW-PRESENTER)
    A derivation of MVC where the Presenter acts as the middleman between the View and Model, making the View more passive.
  MVVM (MODEL-VIEW-VIEWMODEL)
    A design pattern heavily used in modern frameworks where the ViewModel exposes data objects from the Model in such a way that they are easily managed and presented.
  3-TIER ARCHITECTURE
    A client-server architecture organized into three tiers: Presentation, Business Logic, and Data Access.
  REST API (REPRESENTATIONAL STATE TRANSFER)
    An architectural style for networked applications using standard HTTP methods.
  GRAPHQL
    A query language for APIs and a runtime for fulfilling those queries, allowing clients to request exactly what they need.
  WEBSOCKET
    A computer communications protocol providing full-duplex communication channels over a single TCP connection.
  SSE (SERVER-SENT EVENTS)
    A technology where a browser receives automatic updates from a server via HTTP connection.
  OPENAPI
    A specification for machine-readable interface files for describing, producing, consuming, and visualizing RESTful web services.
  MONOREPO
    A software development strategy where code for many projects is stored in the same repository.
  POLYREPO
    The practice of splitting projects into separate repositories.

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

┌─────────────────────────────────────────────────────────────────────────┐
  │  3-TIER ARCHITECTURE                                                    │
  │                                                                         │
  │  +-----------------------+                                              │
  │  |   Presentation Tier   |                                              │
  │  |   (Frontend/Client)   |                                              │
  │  |  React, Vue, Android  |                                              │
  │  +-----------+-----------+                                              │
  │              | HTTP / WebSockets                                        │
  │              v                                                          │
  │  +-----------+-----------+                                              │
  │  | Business Logic Tier   |                                              │
  │  | (Backend Server)      |                                              │
  │  | Node.js, Spring Boot  |                                              │
  │  +-----------+-----------+                                              │
  │              | TCP / SQL                                                │
  │              v                                                          │
  │  +-----------+-----------+                                              │
  │  |   Data Access Tier    |                                              │
  │  |      (Database)       |                                              │
  │  |  PostgreSQL, MongoDB  |                                              │
  │  +-----------------------+                                              │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  MONOLITH VS MICROSERVICES                                              │
  │                                                                         │
  │  MONOLITHIC ARCHITECTURE                                                │
  │  +-----------------------------------+                                  │
  │  |         User Interface            |                                  │
  │  |-----------------------------------|                                  │
  │  |      Business Logic Module A      |                                  │
  │  |      Business Logic Module B      |                                  │
  │  |      Business Logic Module C      |                                  │
  │  |-----------------------------------|                                  │
  │  |          Data Access              |                                  │
  │  +-----------------------------------+                                  │
  │                    |                                                    │
  │               +----+----+                                               │
  │               |   DB    |                                               │
  │               +---------+                                               │
  │                                                                         │
  │  MICROSERVICES ARCHITECTURE                                             │
  │  +---------+       +---------+       +---------+                        │
  │  | Service |       | Service |       | Service |                        │
  │  |    A    |       |    B    |       |    C    |                        │
  │  +----+----+       +----+----+       +----+----+                        │
  │       |                 |                 |                             │
  │  +----+----+       +----+----+       +----+----+                        │
  │  |  DB A   |       |  DB B   |       |  DB C   |                        │
  │  +---------+       +---------+       +---------+                        │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  4. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

[Language: JavaScript]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // REST vs GraphQL (Node.js/Express)                                    │
  │                                                                          │
  │  // --- REST API Example ---                                             │
  │  app.get('/api/users/:id', async (req, res) => {                         │
  │      try {                                                               │
  │          const user = await db.query('SELECT * FROM users WHERE id = ?', [req.params.id]);│
  │          const posts = await db.query('SELECT * FROM posts WHERE user_id = ?', [req.params.id]);│
  │          res.json({ ...user, posts }); // Overfetching or underfetching risks│
  │      } catch (err) {                                                     │
  │          res.status(500).json({ error: 'Server Error' });                │
  │      }                                                                   │
  │  });                                                                     │
  │                                                                          │
  │  // --- GraphQL Example ---                                              │
  │  // The client dictates the shape of the data:                           │
  │  /*                                                                      │
  │  query {                                                                 │
  │    user(id: 1) {                                                         │
  │      name                                                                │
  │      email                                                               │
  │      posts {                                                             │
  │        title                                                             │
  │      }                                                                   │
  │    }                                                                     │
  │  }                                                                       │
  │  */                                                                      │
  │  const resolvers = {                                                     │
  │      Query: {                                                            │
  │          user: async (_, { id }) => await db.query('SELECT * FROM users WHERE id = ?', [id]),│
  │      },                                                                  │
  │      User: {                                                             │
  │          posts: async (parent) => await db.query('SELECT * FROM posts WHERE user_id = ?', [parent.id]),│
  │      }                                                                   │
  │  };                                                                      │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

[Language: JavaScript]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // SSE Server and Client Setup                                          │
  │                                                                          │
  │  // --- Backend: Node.js/Express SSE ---                                 │
  │  const express = require('express');                                     │
  │  const app = express();                                                  │
  │                                                                          │
  │  app.get('/events', (req, res) => {                                      │
  │      // 1. Set headers for SSE                                           │
  │      res.setHeader('Content-Type', 'text/event-stream');                 │
  │      res.setHeader('Cache-Control', 'no-cache');                         │
  │      res.setHeader('Connection', 'keep-alive');                          │
  │                                                                          │
  │      // 2. Send initial message                                          │
  │      res.write('data: Connected to SSE stream\n\n');                     │
  │                                                                          │
  │      // 3. Keep sending data periodically                                │
  │      const intervalId = setInterval(() => {                              │
  │          const data = JSON.stringify({ time: new Date().toISOString() });│
  │          res.write(`data: ${data}\n\n`);                                 │
  │      }, 2000);                                                           │
  │                                                                          │
  │      // 4. Handle client disconnect                                      │
  │      req.on('close', () => {                                             │
  │          clearInterval(intervalId);                                      │
  │          res.end();                                                      │
  │      });                                                                 │
  │  });                                                                     │
  │                                                                          │
  │  app.listen(3000, () => console.log('SSE Server running on port 3000')); │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

  [Language: HTML]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │                                                                          │
  │  <!-- --- Frontend: HTML/JS SSE Client --- -->                           │
  │  <!DOCTYPE html>                                                         │
  │  <html>                                                                  │
  │  <body>                                                                  │
  │      <h1>Server-Sent Events</h1>                                         │
  │      <div id="messages"></div>                                           │
  │                                                                          │
  │      <script>                                                            │
  │          const evtSource = new EventSource('/events');                   │
  │                                                                          │
  │          evtSource.onmessage = function(event) {                         │
  │              const newElement = document.createElement("p");             │
  │              newElement.textContent = "Message: " + event.data;          │
  │              document.getElementById("messages").appendChild(newElement);│
  │          };                                                              │
  │                                                                          │
  │          evtSource.onerror = function(err) {                             │
  │              console.error("EventSource failed:", err);                  │
  │              evtSource.close();                                          │
  │          };                                                              │
  │      </script>                                                           │
  │  </body>                                                                 │
  │  </html>                                                                 │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

Q1: Explain the difference between a Monolith and Microservices. When would you choose which?

  ANSWER:
    Monolith is a single deployable unit; microservices are loosely coupled independent services. Choose a monolith for small teams/projects to reduce operational complexity. Choose microservices when scaling teams, needing independent deployment, or polyglot persistence.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: What is a Modular Monolith and why is it gaining popularity?

  ANSWER:
    It maintains a single deployment unit but enforces strict boundaries between domain modules internally. It offers the simplicity of deployment of a monolith while preventing the "big ball of mud" architecture, making future extraction to microservices easier.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: Compare MVC, MVP, and MVVM.

  ANSWER:
    MVC: Controller updates View and Model. MVP: Presenter handles all logic, View is passive. MVVM: View binds to ViewModel automatically (e.g., via observables), reducing boilerplate UI code.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: How does GraphQL solve REST's over-fetching problem?

  ANSWER:
    GraphQL uses a single endpoint and a query language where the client specifies exactly which fields to return, avoiding the retrieval of unnecessary data common in fixed REST endpoints.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: When would you use WebSockets over Server-Sent Events (SSE)?

  ANSWER:
    Use WebSockets for true bidirectional, real-time communication (e.g., chat apps, multiplayer games). Use SSE for unidirectional server-to-client streaming (e.g., live stock tickers, news feeds).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: What is an API contract-first approach?

  ANSWER:
    Designing and agreeing upon the API specification (like OpenAPI/Swagger) before writing any code. It allows frontend and backend teams to work in parallel.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q7: What are the tiers in a 3-tier architecture?

  ANSWER:
    Presentation Tier (UI), Business Logic Tier (processing/rules), and Data Access Tier (database).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q8: What are the pros and cons of a Monorepo?

  ANSWER:
    Pros: Unified versioning, easy code sharing, single CI/CD pipeline, atomic commits across projects. Cons: Can grow massively (scaling issues), tight coupling if not careful, requires advanced tooling (Lerna, Nx, Turborepo).

────────────────────────────────────────────────────────────────────────────────
  7. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

CHALLENGE 1: Riddle

  I am a single file, yet I hold the blueprint for all endpoints, schemas, and responses. Frontends use me to mock, backends use me to validate. What am I?

  SOLUTION:
    An OpenAPI (Swagger) Specification file.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─


  CHALLENGE 2: Riddle

  I push, but I never pull. I stream, but I never pause. HTTP keeps me alive. What am I?

  SOLUTION:
    Server-Sent Events (SSE).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─


  CHALLENGE 3: 

  // What's wrong here?
  const UserType = new GraphQLObjectType({
    name: 'User',
    fields: () => ({
      friends: { type: new GraphQLList(UserType) }
    })
  });

  SOLUTION:
    While this schema allows querying friends of friends, a malicious or poorly designed client query could nest infinitely (e.g., user -> friends -> friends -> friends), crashing the server. Fix: Implement query depth limiting.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─


  CHALLENGE 4: 

  // What's wrong in this monolith controller?
  app.get('/heavy-task', (req, res) => {
      let result = 0;
      for(let i=0; i<10000000000; i++) { result += i; } // Huge synchronous loop
      res.json({ result });
  });

  SOLUTION:
    Node.js is single-threaded. This massive synchronous loop blocks the event loop, preventing the server from handling any other requests. Fix: Offload to a worker thread or use asynchronous batching.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─


  CHALLENGE 5: 

  app.get('/stream', (req, res) => {
      res.setHeader('Content-Type', 'text/event-stream');
      res.write('data: hello\n\n');
      res.end(); // What's wrong?
  });

  SOLUTION:
    Calling res.end() immediately closes the connection. SSE requires keeping the connection open indefinitely to push future events.

────────────────────────────────────────────────────────────────────────────────
  8. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  Architectural decisions are the hardest to change later. A poorly structured monolith becomes unmaintainable (the "big ball of mud"), while premature microservices introduce extreme network, deployment, and debugging complexity (distributed monolith). Choosing the right communication protocol (REST vs GraphQL, SSE vs WebSockets) directly impacts application performance, scalability, and cloud hosting costs.

────────────────────────────────────────────────────────────────────────────────
  9. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

-> File 067: 067 FullStack Project Auth (Integrating authentication in this architecture.)
  -> File 069: 069 FullStack Deployment (Deploying monoliths vs microservices.)
  -> File 071: 071 FullStack Security (Securing APIs.)

================================================================================
  END OF FILE 066
================================================================================
