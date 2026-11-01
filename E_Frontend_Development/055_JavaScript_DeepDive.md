================================================================================
  FILE 055: JAVASCRIPT DEEP DIVE
  Section: E - Frontend Development
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  JavaScript Deep Dive: Closures, Prototypes, this, and the Event Loop

  Underneath JavaScript's friendly syntax lie some of the most misunderstood mechanisms in programming. Understanding how JavaScript actually works behind the scenes separates junior developers from senior engineers. In this deep dive, you will learn the core pillars of the language: Closures (lexical scoping), Prototypal Inheritance (the prototype chain), the exact rules governing the this keyword, and the Event Loop (how a single-threaded language handles asynchronous tasks). Mastering these concepts allows you to write highly optimized code, prevent memory leaks, and debug complex asynchronous bugs.

  Prerequisites: Solid grasp of ES6+ syntax, functions, and objects.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  Closures
    A closure is formed when a function retains access to its lexical scope (the variables defined outside of it) even after the outer function has returned. It is the backbone of data privacy and functional programming patterns in JS.

  Prototypal Inheritance
    JavaScript objects inherit properties and methods from a prototype.
    __proto__ (or Object.getPrototypeOf(obj)): The hidden property on instances pointing to the constructor's prototype.
    prototype: The object on a constructor function that becomes the __proto__ of all instances created with new.
    Object.create(): Creates a new object with a specified prototype.

  The this Keyword Binding Rules
    1. Default Binding: In strict mode, this is undefined. Otherwise, it's the global object (window).
    2. Implicit Binding: When a function is called as a method of an object (obj.foo()), this is obj.
    3. Explicit Binding: Using .call(), .apply(), or .bind() to force this to be a specific object.
    4. New Binding: When calling a function with new, this binds to the newly constructed object.
    5. Lexical Binding: Arrow functions do not have their own this; they adopt it from the enclosing scope.

  The Event Loop & Concurrency Model
    Call Stack: Where synchronous code executes (LIFO).
    Web APIs: Browser features (DOM, setTimeout, fetch) that handle async work in the background.
    Macrotask Queue (Callback Queue): Holds callbacks from setTimeout, DOM events, etc. Processed when the call stack is empty.
    Microtask Queue: Holds callbacks from Promises (.then()), queueMicrotask, and MutationObserver. Has higher priority than the Macrotask queue.

  Event Delegation
    A pattern where a single event listener is placed on a parent element to handle events originating from its children, exploiting event bubbling (events firing from target element upwards to document).

  Debouncing vs Throttling
    Debounce: Groups a sudden burst of events into a single execution (waits until X ms of inactivity).
    Throttle: Guarantees execution of a function at a regular interval (at most once every X ms).

  Garbage Collection
    Browsers use a "Mark-and-Sweep" algorithm to clear memory. Unreachable objects are swept away.

  Memory Leaks
    Common sources include detached DOM elements referenced in JS, Uncleared setIntervals, and massive closure scopes kept alive unnecessarily.

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  The JavaScript Event Loop

  ┌─────────────────────────────────────────────────────────────────────────┐
  │    +-----------------------+                                            │
  │    |      CALL STACK       |  (Synchronous Execution)                   │
  │    |                       |                                            │
  │    |  console.log('hi')    |  -----> Executes, pops off                 │
  │    |  main()               |                                            │
  │    +-----------|-----------+                                            │
  │                |                                                        │
  │                V (If async task, passed to Web API)                     │
  │    +-----------------------+                                            │
  │    |      WEB APIs         |  (Browser background threads)              │
  │    |                       |                                            │
  │    |  setTimeout(), fetch, |  -----> When done, callback pushed to Queue│
  │    |  DOM Events           |                                            │
  │    +-----------|-----------+                                            │
  │                |                                                        │
  │                V                                                        │
  │    +-----------------------+     Priority!                              │
  │    | MICROTASK QUEUE       |  <-----------------+                       │
  │    | (Promises.then)       |                    |                       │
  │    +-----------------------+    Event Loop checks Microtasks first!     │
  │                                                 |                       │
  │    +-----------------------+                    |                       │
  │    | MACROTASK QUEUE       |  <-----------------+                       │
  │    | (setTimeout cb)       |    Event Loop moves cb to Stack when Stack empty │
  │    +-----------------------+                                            │
  └─────────────────────────────────────────────────────────────────────────┘

  Prototypal Chain

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  [ instance: arr ]                                                      │
  │        | __proto__                                                      │
  │        V                                                                │
  │  [ Array.prototype ] (methods like .map, .filter)                       │
  │        | __proto__                                                      │
  │        V                                                                │
  │  [ Object.prototype ] (methods like .hasOwnProperty)                    │
  │        | __proto__                                                      │
  │        V                                                                │
  │      null                                                               │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  Closure for Data Privacy and Currying

  [Language: Javascript]

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  // 1. Data Privacy (Module Pattern)                                    │
  │  function createCounter() {                                             │
  │    let count = 0; // Private variable                                   │
  │    return {                                                             │
  │      increment: () => ++count,                                          │
  │      decrement: () => --count,                                          │
  │      getCount: () => count                                              │
  │    };                                                                   │
  │  }                                                                      │
  │  const counter = createCounter();                                       │
  │  console.log(counter.increment()); // 1                                 │
  │  console.log(counter.count);       // undefined (cannot access directly)│
  │                                                                         │
  │  // 2. Currying                                                         │
  │  const multiply = (a) => (b) => a * b;                                  │
  │  const double = multiply(2); // Retains lexical scope where 'a' is 2    │
  │  console.log(double(5)); // 10                                          │
  └─────────────────────────────────────────────────────────────────────────┘

  Debounce Implementation

  [Language: Javascript]

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  // Waits until 'delay' ms have passed since the LAST time the function was invoked │
  │  function debounce(func, delay) {                                       │
  │    let timeoutId;                                                       │
  │    return function(...args) {                                           │
  │      const context = this;                                              │
  │      // Clear previous timer if called again                            │
  │      clearTimeout(timeoutId);                                           │
  │      // Set new timer                                                   │
  │      timeoutId = setTimeout(() => {                                     │
  │        func.apply(context, args);                                       │
  │      }, delay);                                                         │
  │    };                                                                   │
  │  }                                                                      │
  │                                                                         │
  │  // Usage: attaching to window resize                                   │
  │  const handleResize = debounce(() => console.log('Resized!'), 300);     │
  │  window.addEventListener('resize', handleResize);                       │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

  Advanced Event Delegation & Memory Management
  In production, especially in vanilla JS or large React apps, attaching 1000 event listeners to a list of 1000 items crashes performance. Event delegation is required.

  [Language: Html]

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  <ul id="todo-list">                                                    │
  │    <!-- Imagine 10,000 li elements here -->                             │
  │    <li data-id="1">                                                     │
  │      <span>Buy Milk</span>                                              │
  │      <button class="delete-btn">Delete</button>                         │
  │    </li>                                                                │
  │    <li data-id="2">                                                     │
  │      <span>Walk Dog</span>                                              │
  │      <button class="delete-btn">Delete</button>                         │
  │    </li>                                                                │
  │  </ul>                                                                  │
  │                                                                         │
  │  <script>                                                               │
  │  class TodoManager {                                                    │
  │    constructor(listElementId) {                                         │
  │      this.listElement = document.getElementById(listElementId);         │
  │      this.items = new Map(); // Store data separately from DOM          │
  │                                                                         │
  │      // Bind 'this' explicitly to ensure it points to the class instance│
  │      this.handleListClick = this.handleListClick.bind(this);            │
  │                                                                         │
  │      // Attach ONE listener to the parent (Event Delegation)            │
  │      this.listElement.addEventListener('click', this.handleListClick);  │
  │    }                                                                    │
  │                                                                         │
  │    handleListClick(event) {                                             │
  │      // Check if the clicked target (or its parent) matches our delete button │
  │      const target = event.target;                                       │
  │                                                                         │
  │      if (target.classList.contains('delete-btn')) {                     │
  │        // Find the closest parent <li> to get the ID                    │
  │        const listItem = target.closest('li');                           │
  │        const id = listItem.dataset.id;                                  │
  │                                                                         │
  │        this.deleteTodo(id, listItem);                                   │
  │      }                                                                  │
  │    }                                                                    │
  │                                                                         │
  │    deleteTodo(id, domNode) {                                            │
  │      console.log(`Deleting todo ${id}`);                                │
  │      // 1. Remove from data structure                                   │
  │      this.items.delete(id);                                             │
  │                                                                         │
  │      // 2. Remove DOM node                                              │
  │      // Removing the node removes all child nodes. Because we used event delegation, │
  │      // we don't have to worry about cleaning up event listeners on the button itself. │
  │      domNode.remove();                                                  │
  │    }                                                                    │
  │                                                                         │
  │    destroy() {                                                          │
  │      // Memory leak prevention: clean up the parent listener when component unmounts │
  │      this.listElement.removeEventListener('click', this.handleListClick); │
  │      this.items.clear();                                                │
  │    }                                                                    │
  │  }                                                                      │
  │                                                                         │
  │  const manager = new TodoManager('todo-list');                          │
  │  </script>                                                              │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  7. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: What is a Closure? Can you give a practical use case?

  ANSWER:
    A closure is a function bundled together with references to its surrounding lexical environment. A practical use case is data privacy (creating private variables that can't be modified directly from the outside) or function currying.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: Explain the difference between call, apply, and bind.

  ANSWER:
    All three explicitly bind this to a function. .call(context, arg1, arg2) invokes the function immediately with comma-separated arguments. .apply(context, [arg1, arg2]) invokes it immediately with an array of arguments. .bind(context) returns a new function with this bound, to be invoked later.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: What is the output order and why? setTimeout(cb, 0), Promise.resolve().then(cb), console.log()

  ANSWER:
    1) console.log() (Synchronous code executes first on the call stack). 2) Promise.then (Microtasks execute immediately after the call stack clears). 3) setTimeout (Macrotasks execute only after all microtasks are clear).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: How does Prototypal Inheritance differ from Classical Inheritance?

  ANSWER:
    Classical inheritance defines rigid blueprints (classes) that create instances. Prototypal inheritance creates objects directly from other objects (prototypes). An object simply links to another object via __proto__ to delegate method lookups.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: What is Event Delegation and why is it useful?

  ANSWER:
    Event delegation involves placing a single event listener on a parent element instead of multiple listeners on children. It utilizes event bubbling. It improves memory and performance significantly and automatically handles dynamically added child elements.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: Explain Debouncing vs Throttling.

  ANSWER:
    Debounce ensures a function is only executed after a specified "quiet" period (e.g., waiting for the user to stop typing before fetching search results). Throttle forces a function to execute at a steady rate, at most once per X ms (e.g., updating a scroll progress bar).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q7: What causes memory leaks in JavaScript?

  ANSWER:
    1) Unintentional global variables. 2) Forgotten timers (setInterval). 3) Closures holding large scopes that are no longer needed. 4) Detached DOM elements (DOM node removed from document, but a JS variable still references it).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q8: What does new keyword actually do under the hood?

  ANSWER:
    1) Creates a new empty object. 2) Sets the prototype of that object to the constructor function's prototype. 3) Binds this to the new object and executes the constructor. 4) Returns the new object.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q9: What is strict mode ('use strict')?

  ANSWER:
    It enforces stricter parsing and error handling. It prevents accidental global variables (throws an error if you assign to undeclared variable), makes this default to undefined instead of window, and prevents duplicate parameter names.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q10: Explain Phase Capturing vs Phase Bubbling.

  ANSWER:
    When a DOM event triggers, it travels down from the window to the target element (Capture Phase), hits the target (Target Phase), and then travels back up to the window (Bubble Phase). addEventListener('click', cb, true) listens on the capture phase; default is bubbling phase.

────────────────────────────────────────────────────────────────────────────────
  8. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: The Loop Closure Problem

  [Language: Javascript]

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  for (var i = 0; i < 3; i++) {                                          │
  │    setTimeout(function() {                                              │
  │      console.log(i);                                                    │
  │    }, 100);                                                             │
  │  }                                                                      │
  └─────────────────────────────────────────────────────────────────────────┘

  SOLUTION:
    What's the output? It prints 3, 3, 3. By the time the setTimeout callbacks run, the loop has finished and the single var i variable (which is function-scoped to the global/outer scope) has the value of 3.
    Fix: Change var to let (creates a new block scope for each iteration), or wrap in an IIFE.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 2: The Lost Context

  [Language: Javascript]

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  const obj = {                                                          │
  │    name: 'Batman',                                                      │
  │    printName: function() {                                              │
  │      console.log(this.name);                                            │
  │    }                                                                    │
  │  };                                                                     │
  │  setTimeout(obj.printName, 1000);                                       │
  └─────────────────────────────────────────────────────────────────────────┘

  SOLUTION:
    What's wrong? Passing obj.printName as a callback strips it of its context. Inside setTimeout, the function is executed in the global context, so this.name is undefined.
    Fix: setTimeout(() => obj.printName(), 1000) or setTimeout(obj.printName.bind(obj), 1000).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 3: Event Loop Tricky Question

  [Language: Javascript]

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  console.log('1');                                                      │
  │  setTimeout(() => console.log('2'), 0);                                 │
  │  Promise.resolve().then(() => console.log('3'));                        │
  │  console.log('4');                                                      │
  └─────────────────────────────────────────────────────────────────────────┘

  SOLUTION:
    What is the exact output sequence?
    Answer: 1, 4, 3, 2. Synchronous first (1, 4), then Microtasks (3), then Macrotasks (2).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 4: The Detached DOM Leak

  [Language: Javascript]

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  let detachedNodes = [];                                                │
  │  function removeElement() {                                             │
  │    const el = document.getElementById('heavy-image');                   │
  │    document.body.removeChild(el);                                       │
  │    detachedNodes.push(el); // Uh oh                                     │
  │  }                                                                      │
  └─────────────────────────────────────────────────────────────────────────┘

  SOLUTION:
    What's wrong? The element is removed from the DOM, but a reference is saved in detachedNodes array. The garbage collector cannot clean up the DOM node memory because JS still holds a reference to it.
    Fix: Do not push it to a long-lived array, or set the array reference to null when done.

────────────────────────────────────────────────────────────────────────────────
  9. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  1. Memory Management: Single Page Applications (React/Angular) don't undergo full page refreshes. If you attach event listeners inside components and don't clean them up on unmount, or leave detached DOM nodes in closures, the browser tab will consume gigabytes of RAM and crash.
  2. React Specifics: React's useEffect closures capture state at the time they are created ("stale closures"). Understanding closures is strictly required to fix bugs where an effect uses an old state value.
  3. Performance: Debouncing API calls prevents a user typing in a search box from triggering 50 requests per second to your backend, saving server costs and preventing rate limits.

────────────────────────────────────────────────────────────────────────────────
  10. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

  -> File 054: JavaScript ES6Plus (ES6 class syntax (which is sugar over prototypes) and Arrow functions (which solve lexical this).)
  -> File 056: JavaScript Async (Deep dive into Promises (Microtasks) and async/await syntax.)
  -> File 059: React Hooks (How closures cause "stale state" bugs in useEffect and useState.)

================================================================================
  END OF FILE 055
================================================================================
