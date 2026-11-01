================================================================================
  FILE 036: NODEJS FUNDAMENTALS
  Section: D - Backend Development
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  Node.js is a runtime environment that allows executing JavaScript code outside of a web browser, typically on the server side. It is built on Google Chrome's V8 JavaScript engine and uses an event-driven, non-blocking I/O model that makes it lightweight and highly efficient. 
  Prerequisites: Basic understanding of JavaScript syntax, ES6 features, and fundamental programming concepts.
  What you'll learn: V8 engine internals, the Node.js event loop, Libuv, streams, buffers, modules, and how asynchronous JavaScript truly works under the hood.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  V8 Engine
    Google's open-source high-performance JavaScript and WebAssembly engine. It parses, compiles, and executes JavaScript.

  AST (Abstract Syntax Tree)
    A tree representation of the abstract syntactic structure of source code. V8 generates this from parsed JavaScript.

  Ignition
    V8's interpreter, which compiles the AST into bytecode.

  TurboFan
    V8's optimizing JIT (Just-In-Time) compiler, which takes hot bytecode and compiles it into highly optimized machine code.

  Event Loop
    The mechanism that allows Node.js to perform non-blocking I/O operations despite JavaScript being single-threaded. It offloads operations to the system kernel whenever possible.

  Libuv
    A multi-platform support library with a focus on asynchronous I/O. It implements the Node.js event loop and provides the Thread Pool (default 4 threads) for heavy tasks (e.g., file system, DNS, crypto).

  Streams
    Collections of data that might not be available all at once and don't have to fit in memory.

  Buffers
    Fixed-length sequences of bytes. Used to handle binary data in Node.js.

  Event Emitter
    A design pattern in Node.js where objects emit named events that cause function modules ("listeners") to be called.

  CommonJS
    The original Node.js module system (require / module.exports).

  ES Modules (ESM)
    The ECMAScript standard module system (import / export).

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  V8 Compilation Pipeline                                                │
  │                                                                         │
  │  JavaScript Code                                                        │
  │         |                                                               │
  │      [Parser] -----> AST (Abstract Syntax Tree)                         │
  │         |                                                               │
  │     [Ignition] (Interpreter)                                            │
  │         |----> Generates Bytecode (Executed quickly)                    │
  │         |                                                               │
  │  (Profiling Data: Hot functions?)                                       │
  │         |                                                               │
  │     [TurboFan] (JIT Compiler)                                           │
  │         |----> Generates Optimized Machine Code (Blazing fast)          │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  Node.js Event Loop Phases                                              │
  │                                                                         │
  │         +-----------------------------------+                           │
  │         |           timers phase            | <--- setTimeout(), setInterval()│
  │         +-----------------------------------+                           │
  │                           |                                             │
  │         +-----------------------------------+                           │
  │         |     pending callbacks phase       | <--- I/O callbacks deferred to the next loop iteration│
  │         +-----------------------------------+                           │
  │                           |                                             │
  │         +-----------------------------------+                           │
  │         |       idle, prepare phase         | <--- internal usage only  │
  │         +-----------------------------------+                           │
  │                           |                                             │
  │         +-----------------------------------+                           │
  │         |           poll phase              | <--- Retrieve new I/O events; execute I/O callbacks│
  │         +-----------------------------------+                           │
  │                           |                                             │
  │         +-----------------------------------+                           │
  │         |           check phase             | <--- setImmediate() callbacks│
  │         +-----------------------------------+                           │
  │                           |                                             │
  │         +-----------------------------------+                           │
  │         |      close callbacks phase        | <--- e.g., socket.on('close', ...)│
  │         +-----------------------------------+                           │
  │                                                                         │
  │  *Note: Microtasks (process.nextTick and Promise callbacks) run         │
  │   immediately after the current operation completes, before the         │
  │   event loop continues to the next phase.*                              │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  Language: JavaScript

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Execution Order: nextTick vs setImmediate vs setTimeout              │
  │                                                                          │
  │  const fs = require('fs');                                               │
  │                                                                          │
  │  console.log('1. Script start');                                         │
  │                                                                          │
  │  setTimeout(() => {                                                      │
  │      console.log('5. setTimeout 0ms');                                   │
  │  }, 0);                                                                  │
  │                                                                          │
  │  setImmediate(() => {                                                    │
  │      console.log('6. setImmediate');                                     │
  │  });                                                                     │
  │                                                                          │
  │  process.nextTick(() => {                                                │
  │      console.log('3. process.nextTick');                                 │
  │  });                                                                     │
  │                                                                          │
  │  Promise.resolve().then(() => {                                          │
  │      console.log('4. Promise.then');                                     │
  │  });                                                                     │
  │                                                                          │
  │  console.log('2. Script end');                                           │
  │                                                                          │
  │  // Output order:                                                        │
  │  // 1. Script start                                                      │
  │  // 2. Script end                                                        │
  │  // 3. process.nextTick (Microtask queue processed first)                │
  │  // 4. Promise.then (Microtask queue processed next)                     │
  │  // 5. setTimeout 0ms (Timers phase)                                     │
  │  // 6. setImmediate (Check phase)                                        │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

  Language: JavaScript

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Stream Processing Large Files                                        │
  │  // When handling large files (e.g., Gigabytes of data), reading the     │
  │  // entire file into memory using fs.readFile will crash the Node        │
  │  // application (Out of Memory). We use Streams to read and process      │
  │  // chunks sequentially.                                                 │
  │                                                                          │
  │  // fileProcessor.js                                                     │
  │  const fs = require('fs');                                               │
  │  const zlib = require('zlib');                                           │
  │  const path = require('path');                                           │
  │  const { pipeline } = require('stream');                                 │
  │  const { promisify } = require('util');                                  │
  │                                                                          │
  │  const pipelineAsync = promisify(pipeline);                              │
  │                                                                          │
  │  /**                                                                     │
  │   * Compresses a large file using streams to avoid memory exhaustion.    │
  │   * @param {string} inputFilePath                                        │
  │   * @param {string} outputFilePath                                       │
  │   */                                                                     │
  │  async function compressLargeFile(inputFilePath, outputFilePath) {       │
  │      try {                                                               │
  │          console.log(`Starting compression for ${inputFilePath}...`);    │
  │                                                                          │
  │          // 1. Readable Stream                                           │
  │          const readStream = fs.createReadStream(inputFilePath);          │
  │                                                                          │
  │          // 2. Transform Stream (Compress)                               │
  │          const gzipStream = zlib.createGzip();                           │
  │                                                                          │
  │          // 3. Writable Stream                                           │
  │          const writeStream = fs.createWriteStream(outputFilePath);       │
  │                                                                          │
  │          // pipeline handles backpressure automatically and cleans up streams on error│
  │          await pipelineAsync(readStream, gzipStream, writeStream);       │
  │                                                                          │
  │          console.log(`File compressed successfully to ${outputFilePath}`);│
  │      } catch (err) {                                                     │
  │          console.error('Compression failed:', err);                      │
  │          throw err;                                                      │
  │      }                                                                   │
  │  }                                                                       │
  │                                                                          │
  │  // Usage                                                                │
  │  const input = path.join(__dirname, 'huge_dataset.csv');                 │
  │  const output = path.join(__dirname, 'huge_dataset.csv.gz');             │
  │                                                                          │
  │  // Execute only if file exists                                          │
  │  if (fs.existsSync(input)) {                                             │
  │      compressLargeFile(input, output);                                   │
  │  } else {                                                                │
  │      console.log("Create a 'huge_dataset.csv' to test the stream.");     │
  │  }                                                                       │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  7. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: What is the difference between process.nextTick() and setImmediate()?

  ANSWER:
    process.nextTick() fires immediately on the same phase, resolving before the event loop continues. It's evaluated in the microtask queue. setImmediate() fires in the Check phase of the event loop, typically executing after I/O events in the current poll phase.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: Explain Node.js event loop phases.

  ANSWER:
    Timers (executes callbacks scheduled by setTimeout/setInterval), Pending (executes I/O callbacks deferred to the next loop iteration), Idle/Prepare (internal), Poll (retrieves new I/O events), Check (executes setImmediate), Close (executes close event callbacks).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: What is libuv and what is its role in Node.js?

  ANSWER:
    Libuv is a multi-platform C library that provides asynchronous I/O based on event loops. In Node.js, it abstracts non-blocking I/O operations and provides a thread pool for tasks that cannot be non-blocking at the OS level (like dns lookups, fs operations, crypto).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: Is Node.js completely single-threaded?

  ANSWER:
    No. JavaScript execution is single-threaded, but I/O operations and certain heavy CPU tasks (like hashing) are offloaded to Libuv's thread pool (default 4 threads), meaning under the hood Node.js uses multiple threads.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: What is backpressure in Node.js Streams?

  ANSWER:
    Backpressure occurs when data is read from a Readable stream faster than a Writable stream can consume it. This causes the internal buffer to fill up and consume memory. pipe() or pipeline() automatically manages backpressure by pausing the readable stream until the writable stream drains.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: How does V8 compile JavaScript?

  ANSWER:
    V8 parses JS to an AST, then Ignition (interpreter) turns AST to bytecode. If functions run frequently ("hot"), TurboFan (JIT compiler) optimizes the bytecode into raw machine code.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q7: What is the difference between Buffers and Streams?

  ANSWER:
    A Buffer is a temporary memory spot holding a fixed amount of raw binary data. A Stream is a continuous flow of data that is processed chunk by chunk (often using Buffers under the hood) without needing to load the entire data into memory at once.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q8: CommonJS vs ES Modules?

  ANSWER:
    CommonJS uses require() and module.exports, loads synchronously, and is Node's traditional module format. ESM uses import and export, loads asynchronously, is statically analyzable, and is the standard JS module format.

────────────────────────────────────────────────────────────────────────────────
  8. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: The Event Loop Block

  const fs = require('fs');
  console.log('Start');
  setTimeout(() => console.log('Timer'), 0);
  while(true) { /* heavy computation */ }
  console.log('End');

  SOLUTION:
    What's wrong? The while(true) is an infinite synchronous loop. Because Node is single-threaded for JS execution, the event loop is entirely blocked. End and Timer will never be printed.
    Fix: Break computation into chunks, use worker threads, or use setImmediate to yield to the event loop.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 2: Memory Leak with Arrays

  const fs = require('fs');
  const http = require('http');
  
  http.createServer((req, res) => {
      fs.readFile(__dirname + '/large-video.mp4', (err, data) => {
          if (err) res.end('Error');
          else res.end(data);
      });
  }).listen(3000);

  SOLUTION:
    What's wrong? fs.readFile loads the entire file (e.g., 1GB video) into RAM for every single request. 10 concurrent requests = 10GB RAM = Server Crash.
    Fix: Use streams! fs.createReadStream(__dirname + '/large-video.mp4').pipe(res);

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 3: NextTick Recursion

  function recursiveTick() {
      process.nextTick(recursiveTick);
  }
  recursiveTick();
  setTimeout(() => console.log('Timeout fired!'), 100);

  SOLUTION:
    What's wrong? process.nextTick enqueues callbacks to the microtask queue, which must be fully drained before the event loop advances. This creates an infinite microtask loop, starving the event loop. The setTimeout will never execute.
    Fix: Use setImmediate if you need recursive asynchronous execution without starving the event loop.

────────────────────────────────────────────────────────────────────────────────
  9. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  - Understanding Event Loop blocking: In production, accidentally writing blocking code (e.g., heavy Regex, massive JSON parsing) will bring down a Node server, affecting all connected users simultaneously.
  - Streams are essential: Production apps must handle high throughput with low memory overhead. Streaming large payloads to AWS S3, reading huge logs, or proxying requests requires streams.
  - Microtasks vs Macrotasks: Understanding execution order ensures race conditions don't happen and responses are sent predictably.

────────────────────────────────────────────────────────────────────────────────
  10. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

  -> File 037: ExpressJS.md (Learn how to build web servers using Node.js event loop efficiently.)
  -> File 040: NodeJS_Advanced.md (Explore Worker Threads (to fix blocking loop issues) and Clustering.)

================================================================================
  END OF FILE 036
================================================================================
