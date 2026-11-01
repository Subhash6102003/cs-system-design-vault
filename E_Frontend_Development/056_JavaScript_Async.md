================================================================================
  FILE 056: JAVASCRIPT ASYNCHRONOUS PROGRAMMING
  Section: E - Frontend Development
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  JavaScript Async: Promises, Async/Await, and Network Requests

  In modern web applications, the UI must remain responsive while waiting for slow operations like network requests, file reading, or timers. JavaScript handles this natively through asynchronous programming. This guide covers the evolution from "Callback Hell" to the elegant async/await syntax, mastering the Fetch API, and managing complex asynchronous flows with Promise combinators like Promise.all and Promise.allSettled. Mastering async JavaScript is essential for preventing frozen UIs and gracefully handling network failures in production.

  Prerequisites: Understanding of the JavaScript Event Loop, Callbacks, and basic HTTP concepts.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  Callback Pattern
    Passing a function as an argument to be executed later. Leads to "Callback Hell" (Pyramid of Doom) when nesting multiple async operations.

  Promises
    An object representing the eventual completion (or failure) of an asynchronous operation and its resulting value.
    States:
    1. Pending: Initial state, neither fulfilled nor rejected.
    2. Fulfilled (Resolved): The operation completed successfully.
    3. Rejected: The operation failed.
    Methods: .then(onFulfilled), .catch(onRejected), .finally(onSettled).

  Promise Combinators
    Promise.all(iterable): Fails fast if any promise rejects. Resolves when all resolve.
    Promise.allSettled(iterable): Waits for all to finish, regardless of success/failure.
    Promise.race(iterable): Resolves/rejects as soon as the first promise settles.
    Promise.any(iterable): Resolves as soon as the first promise fulfills (ignores rejections unless all reject).

  async / await
    Syntactic sugar introduced in ES2017. Makes asynchronous code look and behave a bit more like synchronous code. Uses try/catch for error handling.

  Fetch API
    The modern native browser API for making HTTP requests, replacing XMLHttpRequest (XHR).
    Requires a two-step resolution (first for the headers/metadata, second for the body parsing via .json()).

  AbortController
    An interface that allows you to abort one or more Web requests as and when desired.

  Top-level await
    (ES2022) Allows using await at the top level of ES modules without wrapping in an async function.

  Async Iterators
    for await...of loop allows iterating over async iterables (like reading a file stream chunk by chunk).

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  The Promise State Machine

  ┌─────────────────────────────────────────────────────────────────────────┐
  │                       +-------------------+                             │
  │                       |                   |                             │
  │                       |     PENDING       |                             │
  │                       |                   |                             │
  │                       +--------+----------+                             │
  │                                |                                        │
  │                  +-------------+-------------+                          │
  │                  |                           |                          │
  │            [resolve()]                  [reject()]                      │
  │                  |                           |                          │
  │                  v                           v                          │
  │        +-------------------+       +-------------------+                │
  │        |                   |       |                   |                │
  │        |    FULFILLED      |       |     REJECTED      |                │
  │        |                   |       |                   |                │
  │        +--------+----------+       +---------+---------+                │
  │                 |                            |                          │
  │            [.then()]                    [.catch()]                      │
  │                 |                            |                          │
  │                 +-------------+--------------+                          │
  │                               |                                         │
  │                               v                                         │
  │                      +-------------------+                              │
  │                      |     FINALLY       |                              │
  │                      | (Always executes) |                              │
  │                      +-------------------+                              │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  Implementing Promise.all from Scratch
  A classic interview question to test deep Promise knowledge.

  [Language: Javascript]

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  function myPromiseAll(promises) {                                      │
  │    return new Promise((resolve, reject) => {                            │
  │      const results = [];                                                │
  │      let completedCount = 0;                                            │
  │                                                                         │
  │      // Edge case: Empty array                                          │
  │      if (promises.length === 0) return resolve(results);                │
  │                                                                         │
  │      promises.forEach((promise, index) => {                             │
  │        // Wrap in Promise.resolve to handle non-promise values passed in│
  │        Promise.resolve(promise)                                         │
  │          .then(value => {                                               │
  │            results[index] = value; // Maintain order                    │
  │            completedCount += 1;                                         │
  │            if (completedCount === promises.length) {                    │
  │              resolve(results);                                          │
  │            }                                                            │
  │          })                                                             │
  │          .catch(error => {                                              │
  │            // Reject immediately on first failure                       │
  │            reject(error);                                               │
  │          });                                                            │
  │      });                                                                │
  │    });                                                                  │
  │  }                                                                      │
  └─────────────────────────────────────────────────────────────────────────┘

  AbortController for Fetch Timeout

  [Language: Javascript]

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  async function fetchWithTimeout(url, timeoutMs = 5000) {               │
  │    const controller = new AbortController();                            │
  │    const id = setTimeout(() => controller.abort(), timeoutMs);          │
  │                                                                         │
  │    try {                                                                │
  │      const response = await fetch(url, { signal: controller.signal });  │
  │      clearTimeout(id); // Clear timeout if successful                   │
  │                                                                         │
  │      if (!response.ok) throw new Error('Network response was not ok');  │
  │      return await response.json();                                      │
  │    } catch (error) {                                                    │
  │      if (error.name === 'AbortError') {                                 │
  │        throw new Error(`Request to ${url} timed out after ${timeoutMs}ms`); │
  │      }                                                                  │
  │      throw error;                                                       │
  │    }                                                                    │
  │  }                                                                      │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

  API Fetcher with Exponential Backoff Retry
  In production, mobile networks fail frequently. Silent retries with exponential backoff prevent hammering a struggling server while ensuring user actions eventually succeed.

  [Language: Javascript]

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  /**                                                                    │
  │   * Executes an async function with exponential backoff retries.        │
  │   *                                                                     │
  │   * @param {Function} asyncFn - The async function to execute.          │
  │   * @param {number} maxRetries - Maximum number of retry attempts.      │
  │   * @param {number} baseDelayMs - Initial delay in milliseconds.        │
  │   * @returns {Promise<any>}                                             │
  │   */                                                                    │
  │  async function withRetry(asyncFn, maxRetries = 3, baseDelayMs = 500) { │
  │    let attempt = 0;                                                     │
  │                                                                         │
  │    while (attempt < maxRetries) {                                       │
  │      try {                                                              │
  │        // Attempt the operation                                         │
  │        return await asyncFn();                                          │
  │      } catch (error) {                                                  │
  │        attempt++;                                                       │
  │        console.warn(`[Retry ${attempt}/${maxRetries}] Failed:`, error.message); │
  │                                                                         │
  │        if (attempt >= maxRetries) {                                     │
  │          console.error('Max retries reached. Failing permanently.');    │
  │          throw error;                                                   │
  │        }                                                                │
  │                                                                         │
  │        // Calculate delay: baseDelay * 2^attempt (e.g., 500ms, 1000ms, 2000ms) │
  │        // Add jitter (randomness) to prevent thundering herd problem    │
  │        const delay = (baseDelayMs * Math.pow(2, attempt - 1)) + (Math.random() * 100); │
  │                                                                         │
  │        console.log(`Waiting ${Math.round(delay)}ms before next attempt...`); │
  │        await new Promise(resolve => setTimeout(resolve, delay));        │
  │      }                                                                  │
  │    }                                                                    │
  │  }                                                                      │
  │                                                                         │
  │  // Usage in an application                                             │
  │  async function syncUserData(userData) {                                │
  │    const submitData = async () => {                                     │
  │      const response = await fetch('/api/v1/sync', {                     │
  │        method: 'POST',                                                  │
  │        headers: { 'Content-Type': 'application/json' },                 │
  │        body: JSON.stringify(userData)                                   │
  │      });                                                                │
  │                                                                         │
  │      if (!response.ok) {                                                │
  │        // 5xx errors should be retried, 4xx shouldn't usually, but simplified here │
  │        throw new Error(`HTTP ${response.status}`);                      │
  │      }                                                                  │
  │      return response.json();                                            │
  │    };                                                                   │
  │                                                                         │
  │    try {                                                                │
  │      const result = await withRetry(submitData, 3, 1000);               │
  │      console.log('Sync successful:', result);                           │
  │    } catch (e) {                                                        │
  │      // Show UI error banner to user                                    │
  │      console.error('Final sync failure. Please check connection.');     │
  │    }                                                                    │
  │  }                                                                      │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  7. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: What is the difference between Promise.all and Promise.allSettled?

  ANSWER:
    Promise.all fails immediately if any promise rejects ("fail-fast"). Promise.allSettled waits for all promises to finish (either resolve or reject) and returns an array of objects detailing the status and value/reason of each promise.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: Why does fetch require two .then() calls (or two awaits) to get JSON data?

  ANSWER:
    The first await fetch() resolves as soon as the server sends the HTTP headers, allowing you to check status codes before downloading a massive body. The second await response.json() actually reads the body stream to completion and parses it.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: Does a Promise execute synchronously or asynchronously?

  ANSWER:
    The executor function passed into new Promise((resolve) => { ... }) runs synchronously. However, the callbacks attached via .then() or .catch() are executed asynchronously via the Microtask Queue.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: How do you run asynchronous tasks in parallel vs sequentially using async/await?

  ANSWER:
    Sequentially: await task1(); await task2();. Parallel: const p1 = task1(); const p2 = task2(); await Promise.all([p1, p2]);.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: What is "Callback Hell" and how do Promises solve it?

  ANSWER:
    Deeply nested callbacks (Pyramid of Doom) that make code hard to read and errors hard to track. Promises flatten this structure via .then() chaining, allowing a single .catch() at the end for unified error handling.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: Can you cancel a Promise?

  ANSWER:
    Promises themselves are natively uncancellable once created. However, Web APIs like fetch can be cancelled using an AbortController.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q7: What happens if you forget to await an async function call?

  ANSWER:
    It returns a pending Promise object immediately. If you try to use its value, it will evaluate to [object Promise] instead of the actual data, and unhandled rejections won't be caught by your surrounding try/catch.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q8: Explain Promise.race vs Promise.any.

  ANSWER:
    race resolves/rejects on the first promise to settle (regardless of success or failure). any waits for the first promise to fulfill (ignoring rejections, unless all of them reject).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q9: Can async functions return a primitive value?

  ANSWER:
    Yes, but the JavaScript engine will automatically wrap that return value in a resolved Promise. (async () => 5 returns Promise.resolve(5)).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q10: How do you handle errors in async/await?

  ANSWER:
    By wrapping the await calls inside a standard try { ... } catch (error) { ... } block.

────────────────────────────────────────────────────────────────────────────────
  8. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: The Swallow

  [Language: Javascript]

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  async function getData() {                                             │
  │    try {                                                                │
  │      const data = fetch('/api/data');                                   │
  │      return data.json();                                                │
  │    } catch (e) {                                                        │
  │      console.error('Error!', e);                                        │
  │    }                                                                    │
  │  }                                                                      │
  └─────────────────────────────────────────────────────────────────────────┘

  SOLUTION:
    What's wrong? 1. Forgot await on fetch, so data is a Promise, not a Response. Calling .json() on a Promise throws an error. 2. Returning a Promise from inside a try block without awaiting it means the function returns immediately; if the .json() promise rejects later, the catch block will NOT catch it.
    Fix: const response = await fetch(); return await response.json();

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 2: The Sequential Trap

  [Language: Javascript]

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  async function getUserAndPosts(userId) {                               │
  │    const user = await fetch(`/users/${userId}`).then(r => r.json());    │
  │    const posts = await fetch(`/posts?userId=${userId}`).then(r => r.json()); │
  │    return { user, posts };                                              │
  │  }                                                                      │
  └─────────────────────────────────────────────────────────────────────────┘

  SOLUTION:
    What's wrong? Performance bottleneck. Fetching posts doesn't strictly depend on the user data returning first, but the second request won't start until the first finishes.
    Fix: Run in parallel using Promise.all:

  [Language: Javascript]

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  const [user, posts] = await Promise.all([ fetchUser(), fetchPosts() ]);│
  └─────────────────────────────────────────────────────────────────────────┘

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 3: Unhandled Array Iteration

  [Language: Javascript]

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  async function deleteFiles(files) {                                    │
  │    files.forEach(async (file) => {                                      │
  │      await deleteFileFromServer(file);                                  │
  │    });                                                                  │
  │    console.log('All files deleted!');                                   │
  │  }                                                                      │
  └─────────────────────────────────────────────────────────────────────────┘

  SOLUTION:
    What's wrong? Array.prototype.forEach does not wait for Promises. It will fire off all deletions and immediately print "All files deleted!" before any network request actually finishes.
    Fix: Use for...of for sequential, or Promise.all(files.map(...)) for parallel execution.

────────────────────────────────────────────────────────────────────────────────
  9. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  1. UX / Perceived Performance: Using Promise.all properly turns a 5-second loading spinner (5 sequential 1s requests) into a 1-second loading spinner.
  2. Resilience: The network is unreliable. Implementing timeouts (AbortController) and retry logic prevents infinite loading states and ghost failures.
  3. Error Tracking: Proper try/catch chaining ensures that when an API fails, the error is gracefully caught, sent to logging services (like Sentry), and the user is shown a fallback UI rather than a blank white screen.

────────────────────────────────────────────────────────────────────────────────
  10. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

  -> File 055: JavaScript DeepDive (Event Loop and Microtasks (how Promises actually execute).)
  -> File 060: React StateManagement (How Redux Thunk and RTK Query utilize async patterns for state.)
  -> File 062: NextJS (Server Components and async data fetching at the edge.)

================================================================================
  END OF FILE 056
================================================================================
