================================================================================
  FILE 040: NODEJS ADVANCED
  Section: D - Backend Development
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  Node.js Advanced: Scaling, Concurrency, and Real-Time
  While Node.js is famous for its single-threaded event loop, scaling a production application requires leveraging multi-core processors, running CPU-intensive tasks without blocking the event loop, and managing background processes. This file covers Clustering, Worker Threads, Child Processes, WebSockets for real-time communication, and file uploads.
  Prerequisites: Node.js event loop understanding, Express.js basics, ES6 async/await.
  What you'll learn: Master-Worker clustering, Worker Threads for CPU tasks, PM2 process management, WebSockets vs. Socket.io, Multer for file uploads, and Cron jobs.
  
  ---

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  Clustering
    Running multiple instances of the Node.js process (workers) simultaneously, usually one per CPU core, sharing the same server port to distribute incoming HTTP requests.

  Worker Threads
    A module (`worker_threads`) that allows executing JavaScript in parallel on separate threads within the *same* Node process, sharing memory via `SharedArrayBuffer`. Used for CPU-heavy tasks.

  Child Processes
    Spawning entirely new OS processes (e.g., executing a Python script or shell command from Node) using `spawn`, `exec`, or `fork`.

  PM2
    An advanced, production process manager for Node.js. It handles auto-restarts, clustering, and log management without changing application code.

  WebSocket
    A communication protocol providing full-duplex (bidirectional) communication channels over a single, long-lived TCP connection.

  Socket.io
    A library built on top of WebSockets that adds auto-reconnection, broadcasting, rooms, and fallbacks to HTTP long-polling if WebSockets aren't supported.

  Multer
    Node.js middleware for handling `multipart/form-data`, primarily used for uploading files.

  node-cron
    A module that allows scheduling tasks using standard cron syntax.

  --

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  Cluster Mode Architecture

  ┌─────────────────────────────────────────────────────────────────────────┐
  │                       +-----------------------+                         │
  │                       |    Master Process     |                         │
  │                       |  (Listens on port 80) |                         │
  │                       +-----------------------+                         │
  │                      /            |            \                        │
  │         Round Robin /             |             \ Round Robin           │
  │                    v              v              v                      │
  │        +---------------+  +---------------+  +---------------+          │
  │        |   Worker 1    |  |   Worker 2    |  |   Worker 3    |          │
  │        | (CPU Core 1)  |  | (CPU Core 2)  |  | (CPU Core 3)  |          │
  │        +---------------+  +---------------+  +---------------+          │
  │                |                  |                  |                  │
  │                v                  v                  v                  │
  │         Handles HTTP       Handles HTTP       Handles HTTP              │
  │         Requests           Requests           Requests                  │
  └─────────────────────────────────────────────────────────────────────────┘

### WebSocket Handshake and Message Flow

  ┌─────────────────────────────────────────────────────────────────────────┐
  │    Client (Browser)                               Server (Node.js)      │
  │           |                                              |              │
  │           | 1. HTTP GET /chat (Upgrade: websocket)       |              │
  │           |--------------------------------------------->|              │
  │           | 2. HTTP 101 Switching Protocols              |              │
  │           |<---------------------------------------------|              │
  │           |                                              |              │
  │           | ====== PERSISTENT TCP CONNECTION OPEN ====== |              │
  │           |                                              |              │
  │           | 3. Data Frame (WebSocket Message: "Hello")   |              │
  │           |--------------------------------------------->|              │
  │           | 4. Data Frame (WebSocket Message: "Hi!")     |              │
  │           |<---------------------------------------------|              │
  └─────────────────────────────────────────────────────────────────────────┘

---

────────────────────────────────────────────────────────────────────────────────
  5. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  Worker Threads for CPU-Intensive Tasks


  Language: javascript


  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // main.js                                                              │
  │  const { Worker, isMainThread, parentPort, workerData } = require('worker_threads');│
  │                                                                          │
  │  if (isMainThread) {                                                     │
  │      // We are in the main Event Loop                                    │
  │      console.log("Main thread starting...");                             │
  │                                                                          │
  │      // Spawn a worker for a heavy task                                  │
  │      const worker = new Worker(__filename, {                             │
  │          workerData: { num: 40 } // Calculate Fibonacci 40               │
  │      });                                                                 │
  │                                                                          │
  │      worker.on('message', result => console.log(`Result from worker: ${result}`));│
  │      worker.on('error', err => console.error(err));                      │
  │      worker.on('exit', code => {                                         │
  │          if (code !== 0) console.error(`Worker stopped with exit code ${code}`);│
  │      });                                                                 │
  │                                                                          │
  │      console.log("Main thread is free to do other things!");             │
  │                                                                          │
  │  } else {                                                                │
  │      // We are in the Worker Thread (does not block the main event loop) │
  │      function fibonacci(n) {                                             │
  │          if (n <= 1) return n;                                           │
  │          return fibonacci(n - 1) + fibonacci(n - 2); // Very CPU intensive│
  │      }                                                                   │
  │                                                                          │
  │      const result = fibonacci(workerData.num);                           │
  │      parentPort.postMessage(result); // Send back to main thread         │
  │  }                                                                       │
  └──────────────────────────────────────────────────────────────────────────┘

  ---

────────────────────────────────────────────────────────────────────────────────
  6. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

  WebSocket Chat Server with Rooms (Socket.io)


  Language: javascript


  ┌──────────────────────────────────────────────────────────────────────────┐
  │  const express = require('express');                                     │
  │  const http = require('http');                                           │
  │  const { Server } = require('socket.io');                                │
  │                                                                          │
  │  const app = express();                                                  │
  │  const server = http.createServer(app);                                  │
  │  const io = new Server(server, {                                         │
  │      cors: { origin: '*' }                                               │
  │  });                                                                     │
  │                                                                          │
  │  // Middleware for authentication                                        │
  │  io.use((socket, next) => {                                              │
  │      const token = socket.handshake.auth.token;                          │
  │      if (token === "secret_token") {                                     │
  │          next();                                                         │
  │      } else {                                                            │
  │          next(new Error("Authentication error"));                        │
  │      }                                                                   │
  │  });                                                                     │
  │                                                                          │
  │  io.on('connection', (socket) => {                                       │
  │      console.log(`User connected: ${socket.id}`);                        │
  │                                                                          │
  │      // Join a specific room                                             │
  │      socket.on('join_room', (roomName) => {                              │
  │          socket.join(roomName);                                          │
  │          console.log(`User ${socket.id} joined room ${roomName}`);       │
  │                                                                          │
  │          // Broadcast to everyone ELSE in the room                       │
  │          socket.to(roomName).emit('user_joined', `User ${socket.id} joined.`);│
  │      });                                                                 │
  │                                                                          │
  │      // Handle messages within a room                                    │
  │      socket.on('send_message', (data) => {                               │
  │          // data: { room: 'tech', message: 'Hello!' }                    │
  │          // Emits to everyone in the room, including sender              │
  │          io.to(data.room).emit('receive_message', {                      │
  │              sender: socket.id,                                          │
  │              message: data.message,                                      │
  │              timestamp: new Date()                                       │
  │          });                                                             │
  │      });                                                                 │
  │                                                                          │
  │      socket.on('disconnect', () => {                                     │
  │          console.log(`User disconnected: ${socket.id}`);                 │
  │      });                                                                 │
  │  });                                                                     │
  │                                                                          │
  │  server.listen(3000, () => {                                             │
  │      console.log('WebSocket server listening on port 3000');             │
  │  });                                                                     │
  └──────────────────────────────────────────────────────────────────────────┘

  File Uploads with Multer


  Language: javascript


  ┌──────────────────────────────────────────────────────────────────────────┐
  │  const express = require('express');                                     │
  │  const multer = require('multer');                                       │
  │  const path = require('path');                                           │
  │  const app = express();                                                  │
  │                                                                          │
  │  // Configure storage                                                    │
  │  const storage = multer.diskStorage({                                    │
  │      destination: (req, file, cb) => {                                   │
  │          cb(null, 'uploads/'); // Directory must exist                   │
  │      },                                                                  │
  │      filename: (req, file, cb) => {                                      │
  │          const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1E9);│
  │          cb(null, file.fieldname + '-' + uniqueSuffix + path.extname(file.originalname));│
  │      }                                                                   │
  │  });                                                                     │
  │                                                                          │
  │  // Configure file filter (e.g., images only)                            │
  │  const fileFilter = (req, file, cb) => {                                 │
  │      if (file.mimetype.startsWith('image/')) {                           │
  │          cb(null, true);                                                 │
  │      } else {                                                            │
  │          cb(new Error('Not an image! Please upload an image.'), false);  │
  │      }                                                                   │
  │  };                                                                      │
  │                                                                          │
  │  const upload = multer({                                                 │
  │      storage: storage,                                                   │
  │      limits: { fileSize: 5 * 1024 * 1024 }, // 5 MB limit                │
  │      fileFilter: fileFilter                                              │
  │  });                                                                     │
  │                                                                          │
  │  // Route handling the upload                                            │
  │  app.post('/api/upload', upload.single('profilePic'), (req, res) => {    │
  │      try {                                                               │
  │          res.status(200).json({                                          │
  │              message: 'File uploaded successfully',                      │
  │              file: req.file.filename                                     │
  │          });                                                             │
  │      } catch (error) {                                                   │
  │          res.status(400).json({ error: error.message });                 │
  │      }                                                                   │
  │  });                                                                     │
  │                                                                          │
  │  // Error handling middleware for Multer errors                          │
  │  app.use((err, req, res, next) => {                                      │
  │      if (err instanceof multer.MulterError) {                            │
  │          res.status(400).json({ error: err.message });                   │
  │      } else if (err) {                                                   │
  │          res.status(400).json({ error: err.message });                   │
  │      }                                                                   │
  │  });                                                                     │
  └──────────────────────────────────────────────────────────────────────────┘

  ---

────────────────────────────────────────────────────────────────────────────────
  7. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: When should you use Clustering vs. Worker Threads?

  ANSWER:
    Use **Clustering** to scale web servers (I/O heavy). It spawns multiple instances of your entire app to handle more HTTP requests across CPU cores. Use **Worker Threads** for CPU-intensive tasks (e.g., image processing, heavy math) within a single request, so the main event loop isn't blocked.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: How does PM2 improve upon the native `cluster` module?

  ANSWER:
    The native cluster module requires writing manual code to fork workers and restart them if they die. PM2 handles clustering transparently (`pm2 start app.js -i max`), provides zero-downtime reloads, log aggregation, and restarts crashed processes automatically.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: What is the difference between WebSockets and HTTP?

  ANSWER:
    HTTP is unidirectional and stateless (Client requests, Server responds, connection closes). WebSockets are bidirectional and stateful (Connection stays open, Server can push data to the Client unprompted, low latency).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: Why use Socket.io instead of native WebSockets (`ws`)?

  ANSWER:
    Native `ws` provides barebones WebSockets. Socket.io provides automatic reconnections, fallbacks to HTTP polling (for older firewalls/browsers), channels/rooms, and automatic JSON serialization.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: What is `multipart/form-data` and why is it used for file uploads?

  ANSWER:
    It is an encoding type that allows sending binary data (files) alongside standard text fields in a single HTTP POST request. Standard JSON/URL-encoded bodies cannot handle raw binary files efficiently.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: How do you handle memory management when uploading large files?

  ANSWER:
    Never use memory storage for large files, as it will crash the V8 heap (Out of Memory). Always stream the file directly to disk (using `multer.diskStorage`) or directly to a cloud provider like AWS S3.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q7: What is the difference between `spawn` and `exec` in child processes?

  ANSWER:
    `exec` buffers the command's entire output in memory and returns it to a callback. It's fine for small outputs but will crash on large outputs. `spawn` returns a stream, allowing you to process massive amounts of data chunk-by-chunk.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q8: How do WebSockets scale across multiple servers (Clustering)?

  ANSWER:
    WebSockets require sticky sessions (a user must always hit the same server) or a pub/sub mechanism like Redis Adapter. If User A is connected to Worker 1, and User B to Worker 2, Worker 1 cannot directly emit a message to User B without a Redis backplane bridging the workers.

---

────────────────────────────────────────────────────────────────────────────────
  8. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: The Accidental DoS

  app.get('/hash', (req, res) => {
      // Requires millions of iterations
      const hash = crypto.pbkdf2Sync(req.query.pwd, 'salt', 10000000, 64, 'sha512');
      res.send(hash);
  });

  SOLUTION:
    What's wrong? `pbkdf2Sync` is a synchronous, CPU-intensive operation. It completely blocks the main event loop. While this request is processing (which could take seconds), no other users can access the server.
    Fix: Use the asynchronous version `crypto.pbkdf2(...)` which utilizes the libuv thread pool, or offload it to a Worker Thread.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─
  CHALLENGE 2: The Memory Bloat

  const upload = multer({ storage: multer.memoryStorage() });
  
  app.post('/upload-video', upload.single('video'), (req, res) => {
      fs.writeFileSync('output.mp4', req.file.buffer);
      res.send("Uploaded!");
  });

  SOLUTION:
    What's wrong? `memoryStorage()` holds the entire uploaded file in RAM as a Buffer. If 5 users upload a 500MB video simultaneously, the Node process will consume 2.5GB of RAM and likely crash with an OOM (Out Of Memory) error.
    Fix: Use `multer.diskStorage()` to stream the upload directly to the filesystem.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─
  CHALLENGE 3: Socket Ghosting

  io.on('connection', (socket) => {
      setInterval(() => {
          socket.emit('ping', 'Alive');
      }, 1000);
  });

  SOLUTION:
    What's wrong? When the user disconnects, the `setInterval` is never cleared. This creates a memory leak. The server keeps trying to send data to a dead socket, consuming CPU and memory.
    Fix: Clear the interval on disconnect:
`const timer = setInterval(...); socket.on('disconnect', () => clearInterval(timer));`

---


────────────────────────────────────────────────────────────────────────────────
  9. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  - Scaling out vs Scaling up: Node.js apps must use clustering or PM2 to utilize multi-core VMs. A 16-core server running a single Node process wastes 15 cores.
  - Real-time UX: WebSockets power chat apps, live sports scores, trading dashboards, and collaborative tools (like Google Docs). Polling via HTTP is too slow and resource-heavy for these.
  - Handling untrusted input: File uploads are a massive security risk. Without file size limits and MIME type filtering (Multer configurations), attackers can upload malware or fill up server hard drives.
  ---

────────────────────────────────────────────────────────────────────────────────
  10. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

  -> File 36: NodeJS Fundamentals (Review the Event Loop to understand *why* worker threads are necessary.)
  -> File 37: ExpressJS (Review how Express middleware works before implementing Multer.)

================================================================================
  END OF FILE 040
================================================================================
