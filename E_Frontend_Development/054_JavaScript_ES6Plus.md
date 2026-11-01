================================================================================
  FILE 054: JAVASCRIPT ES6PLUS FEATURES
  Section: E - Frontend Development
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  JavaScript ES6+: Modern Syntax and Capabilities

  ECMAScript 2015 (ES6) and subsequent updates fundamentally changed JavaScript, introducing syntax and features that make the language more powerful, readable, and less error-prone. In this file, you'll explore the critical ES6+ features you use daily in modern web development: variable scoping, arrow functions, destructuring, spread/rest operators, modules, iterators, and the new data structures like Maps and Sets. Understanding these features is non-negotiable for reading and writing modern frontend code, especially in frameworks like React or Vue.

  Prerequisites: Basic understanding of JavaScript syntax, functions, and arrays.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  let & const vs var
    var: Function-scoped, hoisted (initialized as undefined).
    let: Block-scoped, hoisted but kept in a Temporal Dead Zone (TDZ) (cannot be accessed before declaration).
    const: Block-scoped, must be initialized at declaration, and the binding cannot be reassigned (though objects/arrays assigned to it can still be mutated).

  Arrow Functions
    Shorter syntax for anonymous functions. Crucially, they do not have their own this binding; they inherit this from the enclosing lexical context.

  Template Literals
    Strings enclosed in backticks (`) allowing embedded expressions (${expression}) and multi-line strings.

  Destructuring
    Extracting values from arrays or properties from objects into distinct variables.
    Supports default values, nested destructuring, and renaming variables on the fly.

  Spread (...) and Rest (...) Operators
    Spread: Expands an iterable (like an array or object) into individual elements.
    Rest: Condenses multiple elements into a single array (used in function parameters).

  ES Modules (ESM)
    Native module system for JavaScript using import and export.
    Named exports: Export multiple variables/functions. Imported with curly braces.
    Default exports: One per file. Imported without curly braces.
    Dynamic import: import('path') returns a promise, useful for code-splitting.

  Iterators and for...of loops
    Iterating over iterable objects (Arrays, Strings, Maps, Sets). Does not work directly on plain Objects without Object.entries().

  New Data Structures
    Map: Key-value pairs where keys can be any type (even objects). Maintains insertion order.
    Set: A collection of unique values.
    WeakMap / WeakSet: Keys must be objects. Do not prevent garbage collection of the keys.

  Generators
    Functions declared with function* that can be paused (yield) and resumed (next()), producing a sequence of results.

  Optional Chaining (?.)
    Safely access deeply nested object properties without throwing an error if a reference is null or undefined.

  Nullish Coalescing (??)
    Returns the right-hand operand only when the left-hand operand is null or undefined (unlike || which checks for any falsy value like 0 or "").

  Class Syntax
    Syntactical sugar over JavaScript's existing prototype-based inheritance, including static methods, getters/setters, and private fields (#).

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  Let vs Var & Temporal Dead Zone (TDZ)

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  Block Scope {                                                          │
  │    |  <--- TDZ starts for 'let x'                                       │
  │    |                                                                    │
  │    |  console.log(x); // ReferenceError!                                │
  │    |                                                                    │
  │    |  let x = 10; <--- TDZ ends, x is initialized                       │
  │    |                                                                    │
  │    |  console.log(x); // 10                                             │
  │  }                                                                      │
  └─────────────────────────────────────────────────────────────────────────┘

  Arrow Function Lexical this

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  const obj = {                                                          │
  │    name: 'Alice',                                                       │
  │    regularFunc: function() {                                            │
  │      // 'this' is bound to 'obj' because obj called it                  │
  │      setTimeout(function() {                                            │
  │        // 'this' is bound to Window/Global (or undefined in strict mode)│
  │      }, 100);                                                           │
  │                                                                         │
  │      setTimeout(() => {                                                 │
  │        // 'this' is inherited from regularFunc's scope ('obj')          │
  │      }, 100);                                                           │
  │    }                                                                    │
  │  }                                                                      │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  Destructuring, Spread, and Rest

  [Language: Javascript]

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  // 1. Array Destructuring with Rest                                    │
  │  const scores = [98, 85, 91, 78, 100];                                  │
  │  const [topScore, secondScore, ...remainingScores] = scores;            │
  │  console.log(topScore); // 98                                           │
  │  console.log(remainingScores); // [91, 78, 100]                         │
  │                                                                         │
  │  // 2. Object Destructuring with Default Values and Renaming            │
  │  const user = { id: 1, profile: { name: 'Bob', age: 30 } };             │
  │  const {                                                                │
  │    id,                                                                  │
  │    profile: { name, age, bio = 'No bio provided' }, // nested & default │
  │    role: userRole = 'User' // renaming and default                      │
  │  } = user;                                                              │
  │                                                                         │
  │  // 3. Object Spread (Merging)                                          │
  │  const updates = { age: 31, location: 'NY' };                           │
  │  const updatedUser = { ...user, profile: { ...user.profile, ...updates } }; │
  └─────────────────────────────────────────────────────────────────────────┘

  Optional Chaining & Nullish Coalescing

  [Language: Javascript]

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  const response = {                                                     │
  │    data: {                                                              │
  │      user: {                                                            │
  │        settings: {                                                      │
  │          theme: null,                                                   │
  │          notifications: true                                            │
  │        }                                                                │
  │      }                                                                  │
  │    }                                                                    │
  │  };                                                                     │
  │                                                                         │
  │  // Safe access without TypeError: Cannot read property of undefined    │
  │  const theme = response?.data?.user?.settings?.theme;                   │
  │                                                                         │
  │  // ?? only falls back if left side is null or undefined                │
  │  // || would fall back if left side was 0 or "" or false                │
  │  const selectedTheme = theme ?? 'dark'; // 'dark' (theme was null)      │
  │  const hasNotifications = response?.data?.user?.settings?.notifications ?? true; // true │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

  Data Fetcher with Classes, Map, and Private Fields
  This snippet demonstrates a production-style Cache manager utilizing ES6 classes, private fields (#), Map for performant key-value lookups, and modern async handling.

  [Language: Javascript]

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  export class APIManager {                                              │
  │    // Private field (ES2022) - accessible only within this class        │
  │    #cache;                                                              │
  │    #baseURL;                                                            │
  │                                                                         │
  │    constructor(baseURL) {                                               │
  │      this.#baseURL = baseURL;                                           │
  │      // Map is preferred over {} for caching because it doesn't have prototype keys │
  │      // and handles arbitrary key types safely.                         │
  │      this.#cache = new Map();                                           │
  │    }                                                                    │
  │                                                                         │
  │    // Getter method                                                     │
  │    get cacheSize() {                                                    │
  │      return this.#cache.size;                                           │
  │    }                                                                    │
  │                                                                         │
  │    /**                                                                  │
  │     * Fetches data with built-in memory caching                         │
  │     */                                                                  │
  │    async fetchData(endpoint) {                                          │
  │      if (this.#cache.has(endpoint)) {                                   │
  │        console.log(`[Cache Hit] ${endpoint}`);                          │
  │        return this.#cache.get(endpoint);                                │
  │      }                                                                  │
  │                                                                         │
  │      try {                                                              │
  │        console.log(`[Network Request] ${endpoint}`);                    │
  │        const response = await fetch(`${this.#baseURL}${endpoint}`);     │
  │                                                                         │
  │        if (!response.ok) {                                              │
  │          throw new Error(`HTTP error! status: ${response.status}`);     │
  │        }                                                                │
  │                                                                         │
  │        const data = await response.json();                              │
  │        this.#cache.set(endpoint, data);                                 │
  │                                                                         │
  │        return data;                                                     │
  │      } catch (error) {                                                  │
  │        console.error('Fetch failed:', error);                           │
  │        throw error;                                                     │
  │      }                                                                  │
  │    }                                                                    │
  │                                                                         │
  │    clearCache() {                                                       │
  │      this.#cache.clear();                                               │
  │    }                                                                    │
  │  }                                                                      │
  │                                                                         │
  │  // Usage with generator for sequential processing                      │
  │  export function* createEndpointGenerator(endpoints) {                  │
  │    for (const endpoint of endpoints) {                                  │
  │      yield endpoint;                                                    │
  │    }                                                                    │
  │  }                                                                      │
  │                                                                         │
  │  // Executing                                                           │
  │  async function runDemo() {                                             │
  │    const api = new APIManager('https://jsonplaceholder.typicode.com');  │
  │    const generator = createEndpointGenerator(['/users/1', '/users/2', '/users/1']); │
  │                                                                         │
  │    for (const endpoint of generator) {                                  │
  │      const data = await api.fetchData(endpoint); // 3rd request will hit cache │
  │      console.log(`Fetched user: ${data?.name ?? 'Unknown'}`);           │
  │    }                                                                    │
  │  }                                                                      │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  7. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: What is hoisting, and how does it affect var, let, and const?

  ANSWER:
    Hoisting is JS's behavior of moving declarations to the top of the current scope. var is hoisted and initialized with undefined. let and const are hoisted but NOT initialized; accessing them before the declaration throws a ReferenceError (due to the Temporal Dead Zone).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: How is an Arrow Function different from a regular function?

  ANSWER:
    1) Syntactically shorter. 2) No implicit arguments object. 3) Cannot be used as constructors (no new). 4) Crucially, no own this binding—they lexically capture this from their surrounding scope.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: Explain the difference between Rest and Spread operators.

  ANSWER:
    They use the same syntax (...). Spread unpacks elements from an iterable (like merging arrays). Rest packs remaining elements into a single array (used in function parameters or destructuring).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: When should you use a Map instead of a plain Object?

  ANSWER:
    Use Map when keys are not strings/symbols (Maps allow object keys), when you frequently add/remove keys (Maps are optimized for this), when you need to maintain insertion order, or when you need an exact size property.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: What is a WeakMap, and what is its primary use case?

  ANSWER:
    A WeakMap is a Map where keys must be objects, and the references to those objects are "weak." If no other references to the key object exist, the garbage collector will remove the entry from the WeakMap. Used to prevent memory leaks (e.g., attaching metadata to DOM nodes).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: Explain the difference between || (Logical OR) and ?? (Nullish Coalescing).

  ANSWER:
    || returns the right side if the left side is falsy (false, 0, "", null, undefined, NaN). ?? returns the right side ONLY if the left side is null or undefined.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q7: What are ES Modules (ESM)?

  ANSWER:
    The official standard format to package JavaScript code for reuse. Code is isolated by default. Uses export to expose functions/variables and import to bring them in. Browsers support it natively via <script type="module">.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q8: What is a Generator function?

  ANSWER:
    A function declared with function* that can pause its execution using the yield keyword and resume later when next() is called on it. It returns an Iterator object.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q9: How do you clone an object in modern JavaScript?

  ANSWER:
    Shallow clone: const clone = { ...original }; or Object.assign({}, original). Deep clone: const deep = structuredClone(original); (modern native API) or JSON.parse(JSON.stringify(original)) (with data loss caveats).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q10: What is Destructuring, and can you set default values?

  ANSWER:
    It's a syntax to unpack values from arrays or properties from objects into distinct variables. Yes, default values can be set using =: const { name = 'Anonymous' } = user;.

────────────────────────────────────────────────────────────────────────────────
  8. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: The ReferenceError

  [Language: Javascript]

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  console.log(message);                                                  │
  │  let message = "Hello World";                                           │
  └─────────────────────────────────────────────────────────────────────────┘

  SOLUTION:
    What's wrong? Unlike var which would log undefined, let and const throw a ReferenceError because the variable is accessed while in the Temporal Dead Zone (TDZ).
    Fix: Move the console.log below the declaration.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 2: Arrow Function this Trap

  [Language: Javascript]

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  const user = {                                                         │
  │    name: "Alice",                                                       │
  │    greet: () => {                                                       │
  │      console.log(`Hello, my name is ${this.name}`);                     │
  │    }                                                                    │
  │  };                                                                     │
  │  user.greet();                                                          │
  └─────────────────────────────────────────────────────────────────────────┘

  SOLUTION:
    What's wrong? The arrow function inherits this from the outer lexical scope (usually window or undefined in strict mode), NOT the user object. It logs "Hello, my name is undefined".
    Fix: Use a regular function for object methods: greet() { console.log(...) }.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 3: Object Reference Mutation

  [Language: Javascript]

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  const defaultConfig = { port: 8080, db: { name: 'test' } };            │
  │  const customConfig = { ...defaultConfig };                             │
  │  customConfig.port = 3000;                                              │
  │  customConfig.db.name = 'prod';                                         │
  │                                                                         │
  │  console.log(defaultConfig.db.name);                                    │
  └─────────────────────────────────────────────────────────────────────────┘

  SOLUTION:
    What's wrong? The spread operator (...) creates a shallow copy. customConfig.db points to the exact same nested object in memory as defaultConfig.db. Mutating it changes both.
    Fix: Perform a deep copy using structuredClone(defaultConfig) or deep spread: const customConfig = { ...defaultConfig, db: { ...defaultConfig.db } }.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 4: The Un-iterable Object

  [Language: Javascript]

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  const data = { a: 1, b: 2 };                                           │
  │  for (const item of data) {                                             │
  │    console.log(item);                                                   │
  │  }                                                                      │
  └─────────────────────────────────────────────────────────────────────────┘

  SOLUTION:
    What's wrong? Plain objects are not iterable, so for...of throws a TypeError.
    Fix: Use Object.entries(data), Object.keys(data), or Object.values(data) to get an iterable array: for (const [key, val] of Object.entries(data)). Alternatively, use for...in (but be careful of prototype keys).

────────────────────────────────────────────────────────────────────────────────
  9. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  1. Code Predictability: Using const by default and let only when reassignment is needed clearly communicates intent and prevents accidental overwriting of variables.
  2. React and Frameworks: React relies heavily on destructuring for props (const MyComponent = ({ title, data }) => ...) and spread operators for updating state immutably (setState(prev => ({ ...prev, newKey: val }))).
  3. Safety: Optional chaining (?.) replaces massive, ugly && blocks preventing dreaded "Cannot read properties of undefined" errors that crash whole applications in production.

────────────────────────────────────────────────────────────────────────────────
  10. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

  -> File 055: JavaScript DeepDive (Deep dive into prototypes, closures, and the event loop.)
  -> File 056: JavaScript Async (Deep dive into Promises and Async/Await.)
  -> File 058: React Fundamentals (How ES6+ features are utilized heavily in modern React.)

================================================================================
  END OF FILE 054
================================================================================
