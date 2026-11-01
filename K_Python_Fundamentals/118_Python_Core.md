================================================================================
  FILE 118: Python Core Fundamentals
  Section: K - Python Fundamentals
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW

────────────────────────────────────────────────────────────────────────────────
  Python is a high-level, interpreted, dynamically typed programming language known for its readability and "batteries included" philosophy. This file covers the core syntax, data types, control structures, and standard library essentials that form the foundation of Python programming.
  Prerequisites: Basic understanding of programming concepts (variables, loops, logic).
  What you'll learn: Python philosophy, variables, data types, collections, control flow, functions, lambda functions, file I/O, exception handling, and module management.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY

────────────────────────────────────────────────────────────────────────────────
  INTERPRETED
    Python code is executed line-by-line by an interpreter (like CPython) rather than being compiled to machine code beforehand.

  DYNAMICALLY TYPED
    Variables in Python do not have fixed types. A variable can hold an integer, and later hold a string. Types are checked at runtime.

  INDENTATION-BASED
    Python uses whitespace (indentation) to define code blocks (like loops or functions) instead of curly braces `{}`.

  BATTERIES INCLUDED
    The Python Standard Library is vast, providing tools for everything from regular expressions to HTTP requests out of the box.

  REFERENCE SEMANTICS
    Variables are names bound to objects in memory.

  MUTABLE VS IMMUTABLE
    Immutable objects (like `int`, `str`, `tuple`) cannot be changed after creation. Mutable objects (like `list`, `dict`) can be modified in place.

  F-STRINGS
    Formatted string literals (prefixed with `f`) allow embedded expressions inside string literals.

────────────────────────────────────────────────────────────────────────────────
  3. DEMO CODE

────────────────────────────────────────────────────────────────────────────────
  [Language: Python]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Demo Code                                                            │
  │                                                                          │
  │  # Variables and Types                                                   │
  │  age = 25              # int                                             │
  │  price = 19.99         # float                                           │
  │  name = "Alice"        # str                                             │
  │  is_active = True      # bool                                            │
  │  result = None         # NoneType                                        │
  │                                                                          │
  │  # Type Conversions                                                      │
  │  age_str = str(age)                                                      │
  │  price_int = int(price)                                                  │
  │                                                                          │
  │  # Strings                                                               │
  │  raw_str = r"C:\new\folder"                                              │
  │  multi_line = """This is                                                 │
  │  a multiline string"""                                                   │
  │  greeting = f"Hello, {name}! You are {age} years old."                   │
  │                                                                          │
  │  # String Methods                                                        │
  │  csv = "apple, banana, cherry"                                           │
  │  fruits = csv.split(", ")    # ['apple', 'banana', 'cherry']             │
  │  joined = "-".join(fruits)   # 'apple-banana-cherry'                     │
  │  stripped = "  hello  ".strip() # 'hello'                                │
  │                                                                          │
  │  # Collections                                                           │
  │  my_list = [1, 2, 3, 4]      # list: mutable, ordered                    │
  │  my_tuple = (1, 2, 3, 4)     # tuple: immutable, ordered                 │
  │  my_dict = {"a": 1, "b": 2}  # dict: mutable, key-value pairs            │
  │  my_set = {1, 2, 3, 3}       # set: mutable, unique elements             │
  │  my_frozenset = frozenset([1, 2, 3]) # frozenset: immutable set          │
  │                                                                          │
  │  # List Comprehension                                                    │
  │  squares = [x**2 for x in range(5)] # [0, 1, 4, 9, 16]                   │
  │                                                                          │
  │  # Control Flow                                                          │
  │  if age > 18:                                                            │
  │      print("Adult")                                                      │
  │  elif age == 18:                                                         │
  │      print("Just became adult")                                          │
  │  else:                                                                   │
  │      print("Minor")                                                      │
  │                                                                          │
  │  for fruit in fruits:                                                    │
  │      if fruit == "banana":                                               │
  │          continue                                                        │
  │      print(fruit)                                                        │
  │                                                                          │
  │  # Functions & Lambda                                                    │
  │  def greet(user="Guest", *args, **kwargs):                               │
  │      """                                                                 │
  │      Docstring: Greets the user.                                         │
  │      """                                                                 │
  │      return f"Hello, {user}"                                             │
  │                                                                          │
  │  # Lambda                                                                │
  │  multiply = lambda x, y: x * y                                           │
  │  mapped = list(map(lambda x: x*2, [1, 2, 3])) # [2, 4, 6]                │
  │                                                                          │
  │  # File I/O                                                              │
  │  with open("test.txt", "w") as f:                                        │
  │      f.write("Hello World")                                              │
  │                                                                          │
  │  # Exception Handling                                                    │
  │  try:                                                                    │
  │      val = 10 / 0                                                        │
  │  except ZeroDivisionError as e:                                          │
  │      print(f"Error: {e}")                                                │
  │  else:                                                                   │
  │      print("Success")                                                    │
  │  finally:                                                                │
  │      print("Cleanup")                                                    │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  4. PRODUCTION CODE

────────────────────────────────────────────────────────────────────────────────
  [Language: Python]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │                                                                          │
  │  import os                                                               │
  │  import sys                                                              │
  │  import logging                                                          │
  │  from typing import List, Dict, Optional                                 │
  │                                                                          │
  │  # Setup basic logging                                                   │
  │  logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')│
  │                                                                          │
  │  class ConfigurationError(Exception):                                    │
  │      """Custom exception for configuration errors."""                    │
  │      pass                                                                │
  │                                                                          │
  │  def load_config(filepath: str) -> Dict[str, str]:                       │
  │      """                                                                 │
  │      Reads a simple key=value configuration file.                        │
  │                                                                          │
  │      Args:                                                               │
  │          filepath: Path to the config file.                              │
  │                                                                          │
  │      Returns:                                                            │
  │          A dictionary containing the configuration variables.            │
  │                                                                          │
  │      Raises:                                                             │
  │          ConfigurationError: If the file cannot be read or parsed properly.│
  │      """                                                                 │
  │      config = {}                                                         │
  │                                                                          │
  │      if not os.path.exists(filepath):                                    │
  │          logging.error(f"Configuration file {filepath} not found.")      │
  │          raise ConfigurationError(f"File not found: {filepath}")         │
  │                                                                          │
  │      try:                                                                │
  │          with open(filepath, 'r', encoding='utf-8') as f:                │
  │              for line_num, line in enumerate(f, start=1):                │
  │                  line = line.strip()                                     │
  │                  # Skip comments and empty lines                         │
  │                  if not line or line.startswith('#'):                    │
  │                      continue                                            │
  │                                                                          │
  │                  if '=' not in line:                                     │
  │                      raise ConfigurationError(f"Invalid format at line {line_num}: {line}")│
  │                                                                          │
  │                  key, value = line.split('=', 1)                         │
  │                  config[key.strip()] = value.strip()                     │
  │                                                                          │
  │      except IOError as e:                                                │
  │          logging.error(f"Failed to read {filepath}: {e}")                │
  │          raise ConfigurationError(f"IOError: {e}")                       │
  │                                                                          │
  │      return config                                                       │
  │                                                                          │
  │  if __name__ == "__main__":                                              │
  │      # Virtual Environment & Pip Note:                                   │
  │      # Always use `python -m venv venv` to create an isolated environment.│
  │      # Use `pip install -r requirements.txt` to install dependencies.    │
  │      pass                                                                │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. INTERVIEW QUESTIONS

────────────────────────────────────────────────────────────────────────────────
  Q1: What is the difference between a list and a tuple?

  ANSWER:
    Lists are mutable (can be changed after creation), whereas tuples are immutable. Lists use `[]` and tuples use `()`. Tuples can be used as dictionary keys if they contain only immutable elements.


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: Explain how Python handles memory management.

  ANSWER:
    Python uses an automatic memory manager with reference counting and a cyclic garbage collector to detect reference cycles.


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: What are `*args` and `

  ANSWER:
    `*args` allows a function to accept any number of positional arguments (as a tuple). `**kwargs` allows any number of keyword arguments (as a dictionary).


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: What is the difference between `is` and `==`?

  ANSWER:
    `==` checks for value equality, while `is` checks for object identity (if they point to the exact same object in memory).


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: How do decorators work in Python?

  ANSWER:
    A decorator is a function that takes another function and extends its behavior without explicitly modifying it. (Covered more in advanced topics).


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: What is the `with` statement used for?

  ANSWER:
    It simplifies exception handling by encapsulating common preparation and cleanup tasks (Context Managers). It ensures resources are properly released, like closing a file.


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q7: Explain dictionary comprehensions.

  ANSWER:
    A concise way to create dictionaries from iterables, e.g., `{k: v for k, v in iterable}`.


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q8: What is a lambda function?

  ANSWER:
    An anonymous function declared with the `lambda` keyword, mostly used for short, throwaway functions.

────────────────────────────────────────────────────────────────────────────────
  6. RIDDLES & DEBUGGING CHALLENGES

────────────────────────────────────────────────────────────────────────────────
  CHALLENGE 1: The Default Mutable Argument



  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  def append_to(num, target=[]):


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

      target.append(num)


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

      return target


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  print(append_to(1))


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  print(append_to(2))


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─




  SOLUTION:
    The default argument `target=[]` is evaluated only once when the function is defined. Successive calls mutate the same list. Output will be `[1]` then `[1, 2]`. Fix: Use `target=None` and initialize it inside.


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 2: Late Binding Closures



  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  funcs = []


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  for i in range(3):


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

      funcs.append(lambda: i)


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  for f in funcs:


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

      print(f())


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─




  SOLUTION:
    The lambda uses late binding for `i`, meaning it looks up `i` when called. By the time it's called, the loop finished and `i` is 2. Prints `2, 2, 2`. Fix: `lambda i=i: i`.


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 3: Modifying a list while iterating



  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  nums = [1, 2, 3, 4]


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  for num in nums:


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

      if num % 2 == 0:


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

          nums.remove(num)


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─




  SOLUTION:
    Modifying a collection while iterating over it leads to skipped elements or exceptions. Fix: iterate over a copy `for num in nums[:]` or use a list comprehension.

────────────────────────────────────────────────────────────────────────────────
  7. WHY THIS MATTERS IN PRODUCTION

────────────────────────────────────────────────────────────────────────────────
  Understanding core syntax and Python's memory model (like mutable defaults and variable references) prevents insidious bugs that cause data corruption across requests in web servers (like Django or FastAPI). Efficient use of built-in collections directly correlates to application latency.

────────────────────────────────────────────────────────────────────────────────
  8. CROSS-REFERENCES

────────────────────────────────────────────────────────────────────────────────
  -> File 119: Python OOP
  -> File 120: Python Advanced
================================================================================
  END OF FILE 118
================================================================================
