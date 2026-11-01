================================================================================
  FILE 057: TYPESCRIPT ESSENTIALS
  Section: E - Frontend Development
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  TypeScript: Static Typing for Scalable JavaScript

  TypeScript (TS) is a superset of JavaScript that adds optional static typing. While JavaScript evaluates types at runtime, TypeScript evaluates types at compile time, catching entirely classes of errors (like "undefined is not a function") before the code ever runs. In modern frontend development (React, Angular, Node.js), TypeScript is the industry standard. In this file, you'll learn core TS concepts: Interfaces vs. Types, Generics, Utility Types, Type Guards, and structural typing. Mastering TS provides better IDE autocomplete, fearless refactoring, and self-documenting code.

  Prerequisites: Deep understanding of JavaScript ES6+.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  Static Typing vs Dynamic Typing
    JS is dynamic (variables can change type at runtime). TS is static (types are locked in during development/compilation).

  Type Annotations
    Explicitly defining the type of a variable, parameter, or return value (e.g., let count: number = 5;).

  Interfaces vs Type Aliases
    interface: Used to describe the shape of an object or class. Can be augmented (merged) later.
    type: Used for object shapes, but also for Unions, Intersections, and primitives. Cannot be augmented.

  Union Types (|)
    A variable can be one of several types (e.g., string | number).

  Literal Types
    Specific exact values as types (e.g., type Status = "success" | "error" | "loading";).

  Generics (<T>)
    Allows creating reusable components/functions that work with a variety of types rather than a single one (like function arguments, but for types).

  Enums
    A way of giving more friendly names to sets of numeric or string values. (Note: Const enums compile away, regular enums create IIFEs in JS).

  Utility Types
    Built-in TS transformations.
    Partial<T>: Makes all properties optional.
    Required<T>: Makes all properties required.
    Pick<T, Keys>: Extracts a subset of properties.
    Omit<T, Keys>: Removes a subset of properties.
    Record<Key, Value>: Constructs an object type with specific key/value types.
    ReturnType<T>: Extracts the return type of a function.

  Type Narrowing / Type Guards
    Refining a broad type into a narrower one using JS logic.
    typeof (for primitives), instanceof (for classes), in (checking object keys).
    Custom Type Predicate: A function returning arg is Type to tell the TS compiler the exact type.

  Discriminated (Tagged) Unions
    A pattern using a common literal property (like type: 'A') to distinguish between different object interfaces in a union.

  tsconfig.json
    The configuration file that dictates strictness (strict: true), compilation target, module resolution, and path aliases.

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  Structural Typing (Duck Typing)
  TypeScript cares about the shape of an object, not its explicit name.

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  Interface A {           Interface B {                                  │
  │    name: string;           name: string;                                │
  │    age: number;            age: number;                                 │
  │  }                       }                                              │
  │                                                                         │
  │         Object { name: "Bob", age: 30 }                                 │
  │                                                                         │
  │         (Valid as both Interface A and Interface B)                     │
  │         "If it walks like a duck and quacks like a duck..."             │
  └─────────────────────────────────────────────────────────────────────────┘

  TypeScript Compilation Process

  ┌─────────────────────────────────────────────────────────────────────────┐
  │   +---------------+       +--------------+       +-------------------+  │
  │   |   .ts file    | ----> | TS Compiler  | ----> |     .js file      |  │
  │   | (Type syntax) |       | (Type Check) |       | (Pure JavaScript) |  │
  │   +---------------+       +--------------+       +-------------------+  │
  │                                 |                                       │
  │                                 v                                       │
  │                       [Compilation Errors]                              │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  Interfaces, Types, and Utility Types

  [Language: Typescript]

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  // 1. Type alias for a Union of literals                               │
  │  type UserRole = 'admin' | 'editor' | 'viewer';                         │
  │                                                                         │
  │  // 2. Interface for object shape                                       │
  │  interface User {                                                       │
  │    id: string;                                                          │
  │    username: string;                                                    │
  │    email: string;                                                       │
  │    role: UserRole;                                                      │
  │    createdAt?: Date; // Optional property                               │
  │  }                                                                      │
  │                                                                         │
  │  // 3. Utility Types in action                                          │
  │  // Omit email and role for a public profile                            │
  │  type PublicProfile = Omit<User, 'email' | 'role'>;                     │
  │                                                                         │
  │  // Partial allows updating only specific fields                        │
  │  function updateUser(id: string, updates: Partial<User>): User {        │
  │    // Implementation...                                                 │
  │    return {} as User;                                                   │
  │  }                                                                      │
  │                                                                         │
  │  updateUser('123', { role: 'editor' }); // Valid                        │
  │  // updateUser('123', { unknownProp: true }); // Error                  │
  └─────────────────────────────────────────────────────────────────────────┘

  Discriminated Unions for State Management

  [Language: Typescript]

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  // Define separate interfaces with a common 'status' literal property  │
  │  interface StateLoading {                                               │
  │    status: 'loading';                                                   │
  │  }                                                                      │
  │                                                                         │
  │  interface StateSuccess {                                               │
  │    status: 'success';                                                   │
  │    data: string[];                                                      │
  │  }                                                                      │
  │                                                                         │
  │  interface StateError {                                                 │
  │    status: 'error';                                                     │
  │    errorMessage: string;                                                │
  │  }                                                                      │
  │                                                                         │
  │  // Create a union                                                      │
  │  type AppState = StateLoading | StateSuccess | StateError;              │
  │                                                                         │
  │  function renderUI(state: AppState) {                                   │
  │    // TypeScript narrows the type based on the 'status' check           │
  │    switch (state.status) {                                              │
  │      case 'loading':                                                    │
  │        // state is StateLoading                                         │
  │        return "Loading...";                                             │
  │      case 'success':                                                    │
  │        // state is StateSuccess, TS knows 'data' exists safely          │
  │        return `Loaded ${state.data.length} items`;                      │
  │      case 'error':                                                      │
  │        // state is StateError, TS knows 'errorMessage' exists           │
  │        return `Failed: ${state.errorMessage}`;                          │
  │    }                                                                    │
  │  }                                                                      │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

  Fully Typed Generic API Client
  This demonstrates advanced generics, fetch wrapping, custom error handling, and strict typing suitable for a production application.

  [Language: Typescript]

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  // 1. Define specific API Error class                                  │
  │  export class APIError extends Error {                                  │
  │    constructor(public status: number, public message: string) {         │
  │      super(message);                                                    │
  │      this.name = 'APIError';                                            │
  │    }                                                                    │
  │  }                                                                      │
  │                                                                         │
  │  // 2. Define HTTP Methods                                              │
  │  type HttpMethod = 'GET' | 'POST' | 'PUT' | 'DELETE';                   │
  │                                                                         │
  │  // 3. Generic API Client function                                      │
  │  // <T> represents the expected return type of the API call             │
  │  export async function fetchApi<T>(                                     │
  │    endpoint: string,                                                    │
  │    method: HttpMethod = 'GET',                                          │
  │    body?: unknown // Use unknown over any for safer body payload        │
  │  ): Promise<T> {                                                        │
  │    const headers: Record<string, string> = {                            │
  │      'Content-Type': 'application/json',                                │
  │      'Accept': 'application/json',                                      │
  │    };                                                                   │
  │                                                                         │
  │    const config: RequestInit = {                                        │
  │      method,                                                            │
  │      headers,                                                           │
  │      ...(body && { body: JSON.stringify(body) }),                       │
  │    };                                                                   │
  │                                                                         │
  │    try {                                                                │
  │      const response = await fetch(`/api/v1${endpoint}`, config);        │
  │                                                                         │
  │      if (!response.ok) {                                                │
  │        throw new APIError(response.status, `API request failed with status ${response.status}`); │
  │      }                                                                  │
  │                                                                         │
  │      // Return parsed JSON as type T                                      │
  │      const data: T = await response.json();                             │
  │      return data;                                                       │
  │    } catch (error) {                                                    │
  │      if (error instanceof APIError) {                                   │
  │        throw error; // Re-throw known API errors                        │
  │      }                                                                  │
  │      // Handle unexpected network errors                                  │
  │      throw new Error('Network failure or unexpected error occurred');   │
  │    }                                                                    │
  │  }                                                                      │
  │                                                                         │
  │  // === Usage Example ===                                               │
  │                                                                         │
  │  // Define domain models                                                │
  │  interface Product {                                                    │
  │    id: number;                                                          │
  │    name: string;                                                        │
  │    price: number;                                                       │
  │  }                                                                      │
  │                                                                         │
  │  // Define specific payload types                                       │
  │  type CreateProductPayload = Omit<Product, 'id'>;                       │
  │                                                                         │
  │  // Execute calls safely                                                │
  │  async function productApp() {                                          │
  │    // TS knows 'products' is an Array of Product objects                │
  │    const products = await fetchApi<Product[]>('/products');             │
  │                                                                         │
  │    // Enforces the correct payload shape                                │
  │    const newProduct = await fetchApi<Product>('/products', 'POST', {    │
  │      name: 'Keyboard',                                                  │
  │      price: 99.99                                                       │
  │    } satisfies CreateProductPayload);                                   │
  │  }                                                                      │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  7. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: What is the difference between interface and type?

  ANSWER:
    interface is best for object shapes and defining class contracts; it supports declaration merging (augmenting the same interface name later). type is more flexible, allowing Union types, Intersections, and mapping over keys, but it cannot be merged.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: What is the difference between any and unknown?

  ANSWER:
    any completely disables type checking (you can do anything with it). unknown is type-safe; it means "I don't know the type yet," and TS forces you to perform a type check (narrowing) before you can perform operations on it.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: What are Generics?

  ANSWER:
    Generics (<T>) allow you to write reusable code that can work across different types. They act as variables for types, capturing the type provided by the caller and applying it throughout a function, class, or interface.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: How does TypeScript structural typing (duck typing) work?

  ANSWER:
    TS compares the shapes (structure) of objects rather than their explicit names. If object A has all the properties required by interface B, TS considers A compatible with B, even if A has extra properties.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: What is a Discriminated Union?

  ANSWER:
    A pattern where a union of objects shares a common literal property (the discriminator, often type or status). By checking this property in a switch or if statement, TS narrows down the union to one specific object type safely.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: Explain Partial<T> and Omit<T, K>.

  ANSWER:
    Partial creates a type with all properties of T set to optional (great for updates/patches). Omit creates a type by picking all properties from T and then removing the keys specified in K.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q7: What is a Custom Type Predicate (Type Guard)?

  ANSWER:
    A function whose return type is written as arg is Type (e.g., function isString(val: any): val is string). If the function returns true, TS automatically narrows the type of val to string in the calling scope.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q8: What does keyof do?

  ANSWER:
    It takes an object type and produces a string or numeric literal union of its keys (e.g., keyof { a: 1, b: 2 } becomes "a" | "b").

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q9: Why avoid using Enums in TypeScript?

  ANSWER:
    Regular enums generate extra IIFE code in the final JavaScript. Sometimes string literal unions (type Role = "admin" | "user") are preferred because they compile away completely and are often easier to work with. (Note: const enum does compile away, but can cause issues with isolated modules).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q10: What does the strict flag in tsconfig.json do?

  ANSWER:
    It enables a suite of type-checking rules that provide stronger guarantees of program correctness. Most notably, it enables strictNullChecks (preventing null/undefined from being assigned to other types) and noImplicitAny (preventing variables from silently falling back to any).

────────────────────────────────────────────────────────────────────────────────
  8. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: The Implicit Any

  [Language: Typescript]

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  function parseData(data) {                                             │
  │    return data.map(item => item.id);                                    │
  │  }                                                                      │
  └─────────────────────────────────────────────────────────────────────────┘

  SOLUTION:
    What's wrong? Under strict mode, data has an implicit any type, defeating the purpose of TypeScript.
    Fix: Provide a type: function parseData(data: { id: number }[]) { ... } or use generics.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 2: The Constriction

  [Language: Typescript]

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  const roles = ['admin', 'user'];                                       │
  │  const myRole: 'admin' | 'user' = roles[0];                             │
  └─────────────────────────────────────────────────────────────────────────┘

  SOLUTION:
    What's wrong? roles is inferred as string[]. Accessing roles[0] yields a string, which cannot be assigned to the highly specific union type 'admin' | 'user'.
    Fix: Use as const to freeze the array: const roles = ['admin', 'user'] as const;.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 3: Object Spread Type Loss

  [Language: Typescript]

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  interface Car { make: string; model: string; }                         │
  │  const myCar = { make: "Ford", model: "Mustang", year: 2020 };          │
  │  const typedCar: Car = myCar; // No error due to structural typing      │
  │                                                                         │
  │  function updateCar(car: Car) {                                         │
  │    const newCar = { ...car, year: 2024 };                               │
  │  }                                                                      │
  └─────────────────────────────────────────────────────────────────────────┘

  SOLUTION:
    What's wrong? When TS analyzes ...car inside updateCar, it only knows about make and model from the Car interface. The year property from the original object is structurally ignored in the type system, causing unexpected behavior or typing conflicts downstream.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 4: The Risky Assert

  [Language: Typescript]

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  const input = document.getElementById('user-email') as HTMLInputElement;│
  │  console.log(input.value);                                              │
  └─────────────────────────────────────────────────────────────────────────┘

  SOLUTION:
    What's wrong? getElementById can return null if the element doesn't exist. Using as HTMLInputElement forcibly overrides TS's null check, leading to a runtime crash (Cannot read properties of null) if the ID is wrong.
    Fix: Do a runtime check instead of a type assertion.

  [Language: Typescript]

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  const input = document.getElementById('user-email');                   │
  │  if (input instanceof HTMLInputElement) {                               │
  │    console.log(input.value); // TS knows it's an input and not null     │
  │  }                                                                      │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  9. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  1. Refactoring Confidence: In a massive codebase, renaming a property or changing an API response shape in plain JS is terrifying (you rely purely on search-and-replace). TS instantly flags every file and line where the broken property is used.
  2. Self-Documenting Code: Instead of writing JSDoc comments explaining that a function takes an object with specific keys, the TS Interface forces the shape. You hover over a function in VSCode, and you instantly know what it expects and what it returns.
  3. Catching Edge Cases: strictNullChecks forces developers to handle the "what if it's undefined" scenario, which prevents 90% of the Uncaught TypeError crashes in production frontend apps.

────────────────────────────────────────────────────────────────────────────────
  10. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

  -> File 058: React Fundamentals (Integrating TS with React props and state.)
  -> File 062: NextJS (How Next.js uses TypeScript for API routes and Server Components.)

================================================================================
  END OF FILE 057
================================================================================
