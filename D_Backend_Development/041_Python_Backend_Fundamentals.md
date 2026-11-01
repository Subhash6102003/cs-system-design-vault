================================================================================
  FILE 041: PYTHON BACKEND FUNDAMENTALS
  Section: D - Backend Development
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  Python Fundamentals for Backend Developers
  Python is a dynamically typed, interpreted language famous for its readability, vast ecosystem, and dominance in data science and modern backend development (especially AI-integrated backends). This guide serves as a bridge for developers coming from JavaScript or Java, highlighting Python's unique syntax, control flow, data structures, and ecosystem tooling required to build robust backend services.
  Prerequisites: Basic programming concepts (variables, loops, functions).
  What you'll learn: Python syntax, Type hints, Comprehensions, Exception handling, File I/O, Virtual Environments (venv), and Project Structure.
  
  ---

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  Indentation
    Python uses whitespace (indentation) to define code blocks instead of curly braces `{}`.

  Dynamic Typing
    Variable types are determined at runtime, though **Type Hints** (introduced in Python 3.5) allow static type checking via tools like `mypy`.

  List/Dict/Set Comprehensions
    A concise, "Pythonic" way to create collections based on existing sequences.

  `*args` and `
    Syntax used in function signatures to accept an arbitrary number of positional (`args`) and keyword (`kwargs`) arguments.

  Context Managers (`with` statement)
    Ensures that resources are properly acquired and released (e.g., automatically closing a file or database connection).

  f-strings
    Formatted string literals (prefixed with `f`), allowing embedded expressions inside curly braces `{}`.

  Virtual Environment (`venv`)
    An isolated environment that contains its own Python executable and installed packages. Prevents dependency conflicts between different projects.

  `requirements.txt`
    A file listing all the package dependencies for a project (analogous to `package.json` in Node.js).

  `__init__.py`
    A file (often empty) that tells Python a directory should be treated as a package/module.

  --

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  Python vs JavaScript vs Java Syntax Comparison

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  +----------------+--------------------------+---------------------------+-----------------------+│
  │  | Feature        | Python                   | JavaScript                | Java                  |│
  │  +----------------+--------------------------+---------------------------+-----------------------+│
  │  | Code Blocks    | Indentation              | Curly braces {}           | Curly braces {}       |│
  │  | Typing         | Dynamic (with hints)     | Dynamic (TypeScript = static)| Static             |│
  │  | Null Value     | None                     | null / undefined          | null                  |│
  │  | Booleans       | True, False              | true, false               | true, false           |│
  │  | Logical Ops    | and, or, not             | &&, ||, !                 | &&, ||, !             |│
  │  | Arrays         | Lists (brackets [])      | Arrays (brackets [])      | Arrays / ArrayList    |│
  │  | Objects/Maps   | Dictionaries (braces {}) | Objects (braces {})       | HashMap / Objects     |│
  │  +----------------+--------------------------+---------------------------+-----------------------+│
  └─────────────────────────────────────────────────────────────────────────┘

---

────────────────────────────────────────────────────────────────────────────────
  5. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  Comprehensions and Type Hints


  Language: python


  ┌──────────────────────────────────────────────────────────────────────────┐
  │  from typing import List, Dict, Optional                                 │
  │                                                                          │
  │  # Type hints make code self-documenting and IDE-friendly                │
  │  def process_users(users: List[Dict[str, str]], active_only: bool = True) -> List[str]:│
  │      # List comprehension: [expression for item in iterable if condition]│
  │      if active_only:                                                     │
  │          return [f"{u['first']} {u['last']}" for u in users if u.get('status') == 'active']│
  │                                                                          │
  │      return [f"{u['first']} {u['last']}" for u in users]                 │
  │                                                                          │
  │  # Usage                                                                 │
  │  db_users = [                                                            │
  │      {"first": "John", "last": "Doe", "status": "active"},               │
  │      {"first": "Jane", "last": "Smith", "status": "inactive"}            │
  │  ]                                                                       │
  │                                                                          │
  │  active_names = process_users(db_users)                                  │
  │  print(active_names) # Output: ['John Doe']                              │
  └──────────────────────────────────────────────────────────────────────────┘

  File I/O and Exception Handling


  Language: python


  ┌──────────────────────────────────────────────────────────────────────────┐
  │  import json                                                             │
  │                                                                          │
  │  def parse_config(filepath: str) -> Optional[dict]:                      │
  │      # Context manager 'with' ensures file is closed even if exceptions occur│
  │      try:                                                                │
  │          with open(filepath, 'r') as file:                               │
  │              data = json.load(file)                                      │
  │              return data                                                 │
  │      except FileNotFoundError:                                           │
  │          print(f"Error: {filepath} not found.")                          │
  │          return None                                                     │
  │      except json.JSONDecodeError as e:                                   │
  │          print(f"Error parsing JSON: {e}")                               │
  │          return None                                                     │
  │      finally:                                                            │
  │          # Executes no matter what (success or exception)                │
  │          print("File operation attempted.")                              │
  └──────────────────────────────────────────────────────────────────────────┘

  ---

────────────────────────────────────────────────────────────────────────────────
  6. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

  Basic HTTP Server with standard `http.server`
*(Note: In production, you'd use FastAPI, Django, or Flask. This illustrates core Python capabilities without frameworks.)*


  Language: python


  ┌──────────────────────────────────────────────────────────────────────────┐
  │  import json                                                             │
  │  from http.server import BaseHTTPRequestHandler, HTTPServer              │
  │  from urllib.parse import urlparse, parse_qs                             │
  │                                                                          │
  │  class SimpleAPIHandler(BaseHTTPRequestHandler):                         │
  │      def _send_response(self, payload: dict, status: int = 200):         │
  │          """Helper to send JSON responses"""                             │
  │          self.send_response(status)                                      │
  │          self.send_header('Content-type', 'application/json')            │
  │          self.end_headers()                                              │
  │          # Convert dict to JSON string, then encode to bytes             │
  │          self.wfile.write(json.dumps(payload).encode('utf-8'))           │
  │                                                                          │
  │      def do_GET(self):                                                   │
  │          """Handle GET requests"""                                       │
  │          parsed_path = urlparse(self.path)                               │
  │                                                                          │
  │          if parsed_path.path == '/api/health':                           │
  │              self._send_response({"status": "healthy", "service": "python-core"})│
  │                                                                          │
  │          elif parsed_path.path == '/api/echo':                           │
  │              # Extract query params                                      │
  │              query = parse_qs(parsed_path.query)                         │
  │              self._send_response({"you_sent": query})                    │
  │                                                                          │
  │          else:                                                           │
  │              self._send_response({"error": "Not Found"}, 404)            │
  │                                                                          │
  │      def do_POST(self):                                                  │
  │          """Handle POST requests"""                                      │
  │          if self.path == '/api/data':                                    │
  │              # 1. Get content length                                     │
  │              content_length = int(self.headers.get('Content-Length', 0)) │
  │                                                                          │
  │              # 2. Read body bytes and decode to string                   │
  │              post_data = self.rfile.read(content_length).decode('utf-8') │
  │                                                                          │
  │              try:                                                        │
  │                  # 3. Parse JSON                                         │
  │                  data = json.loads(post_data)                            │
  │                  self._send_response({"message": "Data received", "data": data}, 201)│
  │              except json.JSONDecodeError:                                │
  │                  self._send_response({"error": "Invalid JSON"}, 400)     │
  │          else:                                                           │
  │              self._send_response({"error": "Not Found"}, 404)            │
  │                                                                          │
  │  def run_server(port: int = 8000):                                       │
  │      server_address = ('', port)                                         │
  │      httpd = HTTPServer(server_address, SimpleAPIHandler)                │
  │      print(f"Starting native Python server on port {port}...")           │
  │      try:                                                                │
  │          httpd.serve_forever()                                           │
  │      except KeyboardInterrupt:                                           │
  │          pass                                                            │
  │      finally:                                                            │
  │          httpd.server_close()                                            │
  │          print("Server stopped.")                                        │
  │                                                                          │
  │  if __name__ == '__main__':                                              │
  │      run_server()                                                        │
  └──────────────────────────────────────────────────────────────────────────┘

  Python Backend Project Structure Convention


  Language: text


  ┌──────────────────────────────────────────────────────────────────────────┐
  │  /my_python_project                                                      │
  │  ├── venv/                   # Virtual environment (ignored in git)      │
  │  ├── requirements.txt        # Dependencies (pip freeze > requirements.txt)│
  │  ├── .env                    # Environment variables                     │
  │  ├── main.py                 # Application entry point                   │
  │  ├── README.md                                                           │
  │  ├── .gitignore                                                          │
  │  ├── app/                    # Main application package                  │
  │  │   ├── __init__.py                                                     │
  │  │   ├── config.py           # Configuration / env var loading           │
  │  │   ├── routes/             # API endpoints                             │
  │  │   ├── models/             # Database schemas                          │
  │  │   ├── services/           # Business logic                            │
  │  │   └── utils.py            # Helper functions                          │
  │  └── tests/                  # Pytest directory                          │
  │      ├── __init__.py                                                     │
  │      └── test_routes.py                                                  │
  └──────────────────────────────────────────────────────────────────────────┘

  ---

────────────────────────────────────────────────────────────────────────────────
  7. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: What is the difference between `is` and `==` in Python?

  ANSWER:
    `==` checks for **value equality** (do the objects hold the same data?). `is` checks for **identity** (do the variables point to the exact same object in memory?). E.g., `a = [1,2]; b = [1,2]; a == b` is True, `a is b` is False.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: Explain the Global Interpreter Lock (GIL).

  ANSWER:
    The GIL is a mutex in CPython that prevents multiple native threads from executing Python bytecodes at once. This means multithreading in Python is effectively single-core. For CPU-bound tasks, you must use multiprocessing (`multiprocessing` module). Threads are only useful for I/O bound tasks.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: What is a decorator in Python?

  ANSWER:
    A decorator is a function that takes another function and extends its behavior without explicitly modifying it. It's heavily used in backend frameworks (like `@app.get("/")` in FastAPI) for routing and authentication.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: Why are virtual environments necessary?

  ANSWER:
    Python installs packages globally by default. If Project A needs Django 3 and Project B needs Django 4, they will conflict. Virtual environments isolate project dependencies into specific folders.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: What are Python Type Hints? Do they enforce types at runtime?

  ANSWER:
    Type hints (e.g., `def add(a: int, b: int) -> int:`) are annotations that declare expected types. They do **not** enforce types at runtime (Python remains dynamically typed). However, static analyzers like `mypy` and frameworks like FastAPI use them for validation before runtime.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: What is a Context Manager?

  ANSWER:
    An object that defines the runtime context to be established when executing a `with` statement. It ensures resources are properly closed/released (via `__enter__` and `__exit__` methods) even if exceptions occur.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q7: Explain List Comprehensions vs Generators.

  ANSWER:
    `[x*2 for x in range(1000)]` creates a list in memory containing 1000 items. `(x*2 for x in range(1000))` creates a generator object that evaluates items lazily (one at a time), which is infinitely more memory efficient for large datasets.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q8: What does `if __name__ == '__main__':` do?

  ANSWER:
    It checks if the script is being run directly by Python (`python script.py`). If the file is being imported as a module into another file, this block is skipped, preventing executable code from running on import.

---

────────────────────────────────────────────────────────────────────────────────
  8. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: The Mutable Default Argument

  def add_item(item, basket=[]):
      basket.append(item)
      return basket
  
  print(add_item("Apple"))
  print(add_item("Banana"))

  SOLUTION:
    What's wrong? Default arguments are evaluated **once** when the function is defined, not every time it's called. The `basket` list is created once and reused. The second call outputs `['Apple', 'Banana']` instead of just `['Banana']`.
    Fix: Use `None` as the default. 
`def add_item(item, basket=None): basket = basket or []; basket.append(item); return basket;`

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─
  CHALLENGE 2: The Late Binding Closure

  functions = []
  for i in range(3):
      functions.append(lambda: i)
  
  for f in functions:
      print(f())

  SOLUTION:
    What's wrong? It prints `2 2 2` instead of `0 1 2`. Python's closures are late-binding. The lambda function looks up the value of `i` *when it is called*, at which point the loop has finished and `i` is 2.
    Fix: Bind `i` as a default argument in the lambda.
`functions.append(lambda x=i: x)`

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─
  CHALLENGE 3: Exception Swallowing

  try:
      user = db.get_user(user_id)
      print(user.name)
  except Exception:
      pass

  SOLUTION:
    What's wrong? Catching a broad `Exception` and `pass`ing (swallowing it) hides all errors. If `db.get_user` fails due to a network timeout, or if `user` is None and `user.name` causes an AttributeError, it will silently fail. This makes debugging impossible.
    Fix: Catch specific exceptions (e.g., `except AttributeError:`) and log them.

---


────────────────────────────────────────────────────────────────────────────────
  9. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  - Python's AI Dominance: If your backend needs to integrate with Machine Learning models (TensorFlow, PyTorch) or LLMs (LangChain, OpenAI), Python is mandatory. Understanding core Python ensures you don't write "JavaScript in Python syntax."
  - Memory Management: Not using Generators or Context Managers appropriately causes massive memory leaks and file descriptor limits to be reached, bringing down web servers.
  - Dependency Management: Failing to freeze dependencies (`requirements.txt`) guarantees the "it works on my machine" problem when deploying to a Docker container or AWS.
  ---

────────────────────────────────────────────────────────────────────────────────
  10. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

  -> File 42: Python FastAPI (See how Type Hints power modern Python frameworks.)
  -> File 43: Python SQLAlchemy (Learn to use Context Managers to handle database sessions securely.)

================================================================================
  END OF FILE 041
================================================================================
