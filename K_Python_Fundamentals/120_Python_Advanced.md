================================================================================
  FILE 120: Python Advanced Concepts
  Section: K - Python Fundamentals
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW

────────────────────────────────────────────────────────────────────────────────
  This file covers advanced Python paradigms that enable writing elegant, efficient, and Pythonic code. We dive deep into iteration protocols, memory efficiency with generators, context management, and type hinting for robust applications.
  Prerequisites: Python Core Fundamentals, Python OOP.
  What you'll learn: Generators, iterators, context managers, comprehensions, advanced type hints, `functools`, `itertools`, `collections`, structural pattern matching, and the walrus operator.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY

────────────────────────────────────────────────────────────────────────────────
  GENERATORS
    Functions that use `yield` instead of `return`. They return an iterator that yields one item at a time, lazily, preserving state between yields.

  ITERATORS & ITERABLES
    An iterable is anything that can be looped over (implements `__iter__`). An iterator is the object doing the iterating (implements `__next__`).

  CONTEXT MANAGERS
    Objects that set up a context for a block of code and guarantee cleanup using `__enter__` and `__exit__`.

  TYPE HINTS
    Annotations indicating expected types. Python remains dynamically typed; tools like `mypy` statically analyze these hints to catch bugs.

  WALRUS OPERATOR (`=`):
    Assignment expressions (introduced in 3.8) assign and return a value in the same expression.

  STRUCTURAL PATTERN MATCHING (`MATCH`/`CASE`)
    Introduced in 3.10, similar to switch statements but allows unpacking complex data structures.

────────────────────────────────────────────────────────────────────────────────
  3. DEMO CODE

────────────────────────────────────────────────────────────────────────────────
  [Language: Python]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Demo Code                                                            │
  │                                                                          │
  │  import time                                                             │
  │  from typing import Generator, List, Optional, TypeVar, Generic          │
  │                                                                          │
  │  # 1. Generators (Lazy Evaluation)                                       │
  │  def fibonacci(limit: int) -> Generator[int, None, None]:                │
  │      a, b = 0, 1                                                         │
  │      while a < limit:                                                    │
  │          yield a                                                         │
  │          a, b = b, a + b                                                 │
  │                                                                          │
  │  # 2. Context Managers (with contextlib)                                 │
  │  from contextlib import contextmanager                                   │
  │                                                                          │
  │  @contextmanager                                                         │
  │  def timer(label: str):                                                  │
  │      start = time.perf_counter()                                         │
  │      try:                                                                │
  │          yield                                                           │
  │      finally:                                                            │
  │          end = time.perf_counter()                                       │
  │          print(f"{label}: {end - start:.4f} seconds")                    │
  │                                                                          │
  │  # 3. Type Hints & Generics                                              │
  │  T = TypeVar('T')                                                        │
  │  class Stack(Generic[T]):                                                │
  │      def __init__(self) -> None:                                         │
  │          self._items: List[T] = []                                       │
  │      def push(self, item: T) -> None:                                    │
  │          self._items.append(item)                                        │
  │      def pop(self) -> Optional[T]:                                       │
  │          return self._items.pop() if self._items else None               │
  │                                                                          │
  │  # 4. Walrus Operator & Pattern Matching                                 │
  │  def process_data(data: dict):                                           │
  │      if (user_id := data.get("id")) is not None:                         │
  │          match data:                                                     │
  │              case {"role": "admin", "actions": actions}:                 │
  │                  print(f"Admin {user_id} can {actions}")                 │
  │              case {"role": "user"}:                                      │
  │                  print(f"Standard user {user_id}")                       │
  │              case _:                                                     │
  │                  print(f"Unknown role for {user_id}")                    │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  4. PRODUCTION CODE

────────────────────────────────────────────────────────────────────────────────
  [Language: Python]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │                                                                          │
  │  import functools                                                        │
  │  import itertools                                                        │
  │  from collections import defaultdict, deque                              │
  │  import logging                                                          │
  │                                                                          │
  │  logging.basicConfig(level=logging.INFO)                                 │
  │                                                                          │
  │  # Advanced Data Pipeline using Generators and functools                 │
  │  def read_log_lines(filepath: str):                                      │
  │      """Generator to read a file lazily."""                              │
  │      try:                                                                │
  │          with open(filepath, 'r') as f:                                  │
  │              for line in f:                                              │
  │                  yield line.strip()                                      │
  │      except FileNotFoundError:                                           │
  │          logging.error("Log file not found.")                            │
  │                                                                          │
  │  def filter_errors(lines):                                               │
  │      """Generator to filter error lines."""                              │
  │      return (line for line in lines if "ERROR" in line)                  │
  │                                                                          │
  │  def extract_error_codes(lines):                                         │
  │      """Generator to extract the error code from log lines."""           │
  │      for line in lines:                                                  │
  │          parts = line.split(":")                                         │
  │          if len(parts) >= 2:                                             │
  │              yield parts[1].strip()                                      │
  │                                                                          │
  │  # Decorator with arguments using functools.wraps                        │
  │  def retry(max_retries: int = 3):                                        │
  │      def decorator(func):                                                │
  │          @functools.wraps(func) # Preserves function metadata            │
  │          def wrapper(*args, **kwargs):                                   │
  │              for attempt in range(1, max_retries + 1):                   │
  │                  try:                                                    │
  │                      return func(*args, **kwargs)                        │
  │                  except Exception as e:                                  │
  │                      logging.warning(f"Attempt {attempt} failed: {e}")   │
  │              raise RuntimeError(f"Failed after {max_retries} retries")   │
  │          return wrapper                                                  │
  │      return decorator                                                    │
  │                                                                          │
  │  @retry(max_retries=2)                                                   │
  │  def unstable_api_call():                                                │
  │      import random                                                       │
  │      if random.random() < 0.7:                                           │
  │          raise ValueError("Network Timeout")                             │
  │      return {"status": "success"}                                        │
  │                                                                          │
  │  if __name__ == "__main__":                                              │
  │      # Pipeline execution is memory efficient!                           │
  │      # No matter how large the log file, only 1 line is processed in memory at a time.│
  │      # pipeline = extract_error_codes(filter_errors(read_log_lines("app.log")))│
  │      # error_counts = collections.Counter(pipeline)                      │
  │      pass                                                                │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. INTERVIEW QUESTIONS

────────────────────────────────────────────────────────────────────────────────
  Q1: How do generators improve performance?

  ANSWER:
    Generators calculate values lazily. This significantly reduces memory usage since you don't load huge datasets into RAM all at once.


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: What is the difference between `yield` and `return`?

  ANSWER:
    `return` exits the function completely, destroying local state. `yield` pauses the function, returning a value, and preserves the local state for the next time `next()` is called.


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: What is `functools.wraps` and why use it?

  ANSWER:
    When writing decorators, the wrapper function replaces the original function, hiding its name and docstring. `@wraps` copies metadata (like `__name__`, `__doc__`) from the original function to the wrapper.


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: Explain how to create a custom context manager.

  ANSWER:
    Either implement a class with `__enter__` and `__exit__` methods, or use the `@contextlib.contextmanager` decorator on a generator function yielding once.


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: What does the walrus operator (`:=`) do?

  ANSWER:
    It assigns a value to a variable and returns that value simultaneously, useful for reducing redundant function calls inside `if` or `while` conditions.


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: How does structural pattern matching differ from `if/elif`?

  ANSWER:
    Pattern matching (`match/case`) can unpack and destructure data types (like dictionaries, objects, sequences) declaratively, checking structure and types rather than just boolean conditions.


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q7: What is `itertools.chain`?

  ANSWER:
    It treats multiple iterables as a single continuous iterable without concatenating them into a new list.


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q8: What is `lru_cache`?

  ANSWER:
    A decorator in `functools` that caches the return values of a function based on its arguments. Using an LRU (Least Recently Used) policy to save computation time for repetitive calls.

────────────────────────────────────────────────────────────────────────────────
  6. RIDDLES & DEBUGGING CHALLENGES

────────────────────────────────────────────────────────────────────────────────
  CHALLENGE 1: Exhausting an Iterator



  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  gen = (x**2 for x in range(3))


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  list1 = list(gen)


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  list2 = list(gen)


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  print(list1, list2)


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─




  SOLUTION:
    Generators are one-time use iterators. Once exhausted, they are empty. Output is `[0, 1, 4], []`. Fix: Recreate the generator or convert to a list upfront.


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 2: Bad Type Hinting



  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  def append_item(item: int, lst: list = []) -> list:


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

      lst.append(item)


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

      return lst


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─




  SOLUTION:
    Standard `list` doesn't specify what's inside (use `List[int]` from typing). More importantly, the mutable default argument bug remains despite the type hint. Type hints don't fix runtime semantics.


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 3: Context Manager Exception Swallowing



  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  class MyContext:


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

      def __enter__(self): pass


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

      def __exit__(self, exc_type, exc_val, traceback):


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

          return True


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  with MyContext():


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

      raise ValueError("Crash!")


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─




  SOLUTION:
    Returning `True` from `__exit__` explicitly suppresses the exception. The `ValueError` is swallowed silently, hiding potential bugs.

────────────────────────────────────────────────────────────────────────────────
  7. WHY THIS MATTERS IN PRODUCTION

────────────────────────────────────────────────────────────────────────────────
  Generators are mandatory when processing files larger than the available RAM (e.g., 50GB CSVs). Context managers ensure network connections and file descriptors are always closed, preventing connection leaks. Type hints drastically reduce runtime `AttributeError`s and improve IDE autocompletion in large codebases.

────────────────────────────────────────────────────────────────────────────────
  8. CROSS-REFERENCES

────────────────────────────────────────────────────────────────────────────────
  -> File 119: Python OOP
  -> File 122: Python Concurrency
================================================================================
  END OF FILE 120
================================================================================
