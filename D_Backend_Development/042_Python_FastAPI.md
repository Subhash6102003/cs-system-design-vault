================================================================================
  FILE 042: PYTHON FASTAPI
  Section: D - Backend Development
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  FastAPI: Modern, Fast Web Framework for Python
  FastAPI is a modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints. It is built on top of Starlette for the web parts (ASGI) and Pydantic for the data parts. It provides automatic interactive API documentation, data validation, and asynchronous support out of the box.
  Prerequisites: Python fundamentals, Type Hints, basic HTTP and REST API concepts.
  What you'll learn: Request parsing, Pydantic data validation, Async endpoints, Dependency Injection, Middleware, Background Tasks, and Error Handling.
  
  ---

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  ASGI (Asynchronous Server Gateway Interface)
    The spiritual successor to WSGI. It allows Python web frameworks and servers to communicate asynchronously. Starlette is the ASGI toolkit FastAPI uses.

  Pydantic
    A data validation and settings management library using Python type annotations. FastAPI uses it to validate incoming JSON bodies and serialize outgoing responses.

  Path Parameters
    Variables embedded directly in the URL path (e.g., `/users/{user_id}`).

  Query Parameters
    Key-value pairs in the URL after a `?` (e.g., `/users?skip=0&limit=10`).

  Dependency Injection (`Depends`)
    A pattern used heavily in FastAPI to provide components (like database sessions or authentication tokens) to route handlers efficiently and cleanly.

  Background Tasks
    A FastAPI feature allowing you to run a function in the background after returning the HTTP response (e.g., sending an email).

  OpenAPI
    A specification for machine-readable interface files for describing APIs. FastAPI automatically generates this, providing interactive UI docs at `/docs` (Swagger UI) and `/redoc` (ReDoc).

  Uvicorn
    A lightning-fast ASGI server implementation. It's the standard server used to run FastAPI applications.

  --

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  FastAPI Request Lifecycle Architecture

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  Client Request                                                         │
  │        |                                                                │
  │        v                                                                │
  │  +---------------------------------------------------+                  │
  │  |  Uvicorn / Gunicorn (ASGI Server)                 |                  │
  │  +---------------------------------------------------+                  │
  │        | (Async HTTP Request)                                           │
  │        v                                                                │
  │  +---------------------------------------------------+                  │
  │  |  Middleware Chain (CORS, Logging, Timing, Auth)   |                  │
  │  +---------------------------------------------------+                  │
  │        |                                                                │
  │        v                                                                │
  │  +---------------------------------------------------+                  │
  │  |  FastAPI Router (Matches path / method)           |                  │
  │  +---------------------------------------------------+                  │
  │        |                                                                │
  │        v                                                                │
  │  +---------------------------------------------------+                  │
  │  |  Dependencies (Depends)                           |                  │
  │  |  - e.g., Get DB Session, Verify JWT               |                  │
  │  +---------------------------------------------------+                  │
  │        |                                                                │
  │        v                                                                │
  │  +---------------------------------------------------+                  │
  │  |  Pydantic Validation (Incoming Request Body)      |                  │
  │  |  - Converts JSON to Python objects                |                  │
  │  |  - Throws 422 Unprocessable Entity if invalid     |                  │
  │  +---------------------------------------------------+                  │
  │        |                                                                │
  │        v                                                                │
  │  +---------------------------------------------------+                  │
  │  |  Endpoint Handler (async def / def)               |                  │
  │  |  - Executes business logic                        |                  │
  │  +---------------------------------------------------+                  │
  │        |                                                                │
  │        v                                                                │
  │  +---------------------------------------------------+                  │
  │  |  Pydantic Serialization (Outgoing Response)       |                  │
  │  |  - Converts Python objects back to JSON           |                  │
  │  +---------------------------------------------------+                  │
  │        |                                                                │
  │        v                                                                │
  │  Response returned to Client (while BackgroundTasks run)                │
  └─────────────────────────────────────────────────────────────────────────┘

---

────────────────────────────────────────────────────────────────────────────────
  5. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  Path Params, Query Params, and Pydantic Models


  Language: python


  ┌──────────────────────────────────────────────────────────────────────────┐
  │  from fastapi import FastAPI, Query, Path, HTTPException                 │
  │  from pydantic import BaseModel, Field                                   │
  │                                                                          │
  │  app = FastAPI(title="Demo API")                                         │
  │                                                                          │
  │  # 1. Pydantic Model for Request Body                                    │
  │  class Item(BaseModel):                                                  │
  │      name: str = Field(..., example="Laptop")                            │
  │      description: str | None = Field(default=None, max_length=50)        │
  │      price: float = Field(..., gt=0, description="Price must be greater than zero")│
  │      tax: float | None = None                                            │
  │                                                                          │
  │  # Mock database                                                         │
  │  items_db = {"1": {"name": "Phone", "price": 500.0}}                     │
  │                                                                          │
  │  # 2. Endpoint utilizing Path, Query, and Body parameters                │
  │  @app.post("/items/{item_id}", response_model=Item, status_code=201)     │
  │  async def create_item(                                                  │
  │      item_id: str = Path(..., title="The ID of the item to create"),     │
  │      q: str | None = Query(default=None, max_length=10),                 │
  │      item: Item = None  # Body payload parsed and validated by Pydantic  │
  │  ):                                                                      │
  │      if item_id in items_db:                                             │
  │          # FastAPI Error Handling                                        │
  │          raise HTTPException(status_code=400, detail="Item already exists")│
  │                                                                          │
  │      items_db[item_id] = item.model_dump()                               │
  │      return item                                                         │
  └──────────────────────────────────────────────────────────────────────────┘

  ---

────────────────────────────────────────────────────────────────────────────────
  6. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

  Full API Setup: Middleware, Dependency Injection, and Background Tasks


  Language: python


  ┌──────────────────────────────────────────────────────────────────────────┐
  │  import time                                                             │
  │  from typing import List, Optional                                       │
  │  from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks, Request│
  │  from fastapi.middleware.cors import CORSMiddleware                      │
  │  from pydantic import BaseModel                                          │
  │  import uvicorn                                                          │
  │                                                                          │
  │  # --- MODELS ---                                                        │
  │  class UserCreate(BaseModel):                                            │
  │      username: str                                                       │
  │      email: str                                                          │
  │                                                                          │
  │  class UserResponse(UserCreate):                                         │
  │      id: int                                                             │
  │                                                                          │
  │  # --- FAKE DATABASE & EMAIL SERVICE ---                                 │
  │  fake_db = []                                                            │
  │                                                                          │
  │  async def get_db():                                                     │
  │      # Dependency that simulates yielding a database session             │
  │      db_session = fake_db                                                │
  │      try:                                                                │
  │          yield db_session                                                │
  │      finally:                                                            │
  │          # Teardown logic (e.g., closing the DB session) happens here    │
  │          pass                                                            │
  │                                                                          │
  │  def write_notification(email: str, message=""):                         │
  │      """Function to be run in the background"""                          │
  │      with open("log.txt", mode="a") as email_file:                       │
  │          content = f"notification for {email}: {message}\n"              │
  │          email_file.write(content)                                       │
  │          # Simulate slow operation                                       │
  │          time.sleep(2)                                                   │
  │                                                                          │
  │  # --- APP SETUP ---                                                     │
  │  app = FastAPI(                                                          │
  │      title="Production-Ready API",                                       │
  │      description="API demonstrating dependencies, middleware, and background tasks",│
  │      version="1.0.0"                                                     │
  │  )                                                                       │
  │                                                                          │
  │  # --- MIDDLEWARE ---                                                    │
  │  app.add_middleware(                                                     │
  │      CORSMiddleware,                                                     │
  │      allow_origins=["*"], # In prod, use specific domains                │
  │      allow_credentials=True,                                             │
  │      allow_methods=["*"],                                                │
  │      allow_headers=["*"],                                                │
  │  )                                                                       │
  │                                                                          │
  │  @app.middleware("http")                                                 │
  │  async def add_process_time_header(request: Request, call_next):         │
  │      start_time = time.time()                                            │
  │      response = await call_next(request) # Pass request down the chain   │
  │      process_time = time.time() - start_time                             │
  │      # Add custom header to outgoing response                            │
  │      response.headers["X-Process-Time"] = str(process_time)              │
  │      return response                                                     │
  │                                                                          │
  │  # --- ROUTES ---                                                        │
  │  @app.post("/users/", response_model=UserResponse, status_code=201)      │
  │  async def create_user(                                                  │
  │      user: UserCreate,                                                   │
  │      background_tasks: BackgroundTasks, # Injected by FastAPI            │
  │      db: list = Depends(get_db)         # Injected dependency            │
  │  ):                                                                      │
  │      # Validate unique email                                             │
  │      if any(u.get("email") == user.email for u in db):                   │
  │          raise HTTPException(status_code=400, detail="Email already registered")│
  │                                                                          │
  │      # Save to "database"                                                │
  │      new_user = {"id": len(db) + 1, "username": user.username, "email": user.email}│
  │      db.append(new_user)                                                 │
  │                                                                          │
  │      # Schedule background task (Response returns immediately, email sends in background)│
  │      background_tasks.add_task(write_notification, user.email, message="Welcome to our platform!")│
  │                                                                          │
  │      return new_user                                                     │
  │                                                                          │
  │  @app.get("/users/", response_model=List[UserResponse])                  │
  │  async def read_users(                                                   │
  │      skip: int = 0,                                                      │
  │      limit: int = 10,                                                    │
  │      db: list = Depends(get_db)                                          │
  │  ):                                                                      │
  │      return db[skip : skip + limit]                                      │
  │                                                                          │
  │  # --- RUN THE APP ---                                                   │
  │  if __name__ == "__main__":                                              │
  │      uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)     │
  └──────────────────────────────────────────────────────────────────────────┘

  ---

────────────────────────────────────────────────────────────────────────────────
  7. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: How does FastAPI compare to Flask and Django?

  ANSWER:
    Django is a "batteries-included" full-stack framework with an integrated ORM, admin panel, and templating engine (sync by default, heavily opinionated). Flask is a microframework, highly unopinionated, using WSGI (historically sync). FastAPI is a modern microframework built on ASGI (async by design), highly focused on building APIs, with automatic OpenAPI docs, Pydantic validation, and unmatched performance.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: What happens if you define a FastAPI endpoint using `def` instead of `async def`?

  ANSWER:
    FastAPI is smart. If you use standard `def`, FastAPI will run the endpoint in an external threadpool (using Starlette's `run_in_threadpool`). This prevents a synchronous, blocking operation (like a traditional database query or `time.sleep()`) from freezing the entire asynchronous event loop.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: When should you use `async def` vs `def` in FastAPI?

  ANSWER:
    Use `async def` if you are awaiting asynchronous code inside the endpoint (e.g., async HTTP clients like `httpx`, async ORMs like SQLAlchemy Async, or Motor for MongoDB). Use standard `def` if you are using blocking, synchronous libraries (e.g., standard SQLAlchemy, `requests`, or heavy CPU-bound tasks).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: Explain Dependency Injection (`Depends`) in FastAPI.

  ANSWER:
    It is a system that allows you to declare dependencies (functions) that an endpoint needs to execute. FastAPI executes these dependencies before the endpoint, passing the results as parameters. It's heavily used for database sessions, authentication (extracting/verifying tokens), and sharing common query parameters.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: What is Pydantic and why does FastAPI use it?

  ANSWER:
    Pydantic is a data validation library. FastAPI uses it to define the shape of JSON request bodies and response models using Python type hints. Pydantic automatically parses JSON into Python objects, validates data types, handles coercion (e.g., casting the string `"1"` to int `1`), and generates helpful error messages for invalid data.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: How does FastAPI automatically generate documentation?

  ANSWER:
    FastAPI translates your route paths, type hints, Pydantic models, and docstrings into an OpenAPI schema (a standard JSON definition of your API). It then serves web interfaces (Swagger UI and ReDoc) that read this schema to provide interactive documentation.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q7: How do Background Tasks work in FastAPI?

  ANSWER:
    The `BackgroundTasks` class is injected into the endpoint. You add functions to it using `.add_task()`. Once FastAPI finishes generating the HTTP response and sends it to the client, it executes the queued background tasks in the same process without blocking the response.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q8: What is the difference between a Path Parameter and a Query Parameter?

  ANSWER:
    Path parameters are variables defined directly in the URL structure (`/users/{id}`) and are required to route the request properly. Query parameters are appended to the URL after a question mark (`/users?role=admin`) and are typically optional, used for filtering, pagination, or sorting.

---

────────────────────────────────────────────────────────────────────────────────
  8. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: The Event Loop Blocker

  import time
  from fastapi import FastAPI
  
  app = FastAPI()
  
  @app.get("/heavy-processing")
  async def process_data():
      time.sleep(10) # Simulating heavy synchronous work
      return {"status": "done"}

  SOLUTION:
    What's wrong? Because the endpoint is defined with `async def`, FastAPI runs it directly on the main asynchronous event loop. Calling `time.sleep(10)` (a blocking, synchronous operation) will freeze the entire server. No other requests can be processed for 10 seconds.
    Fix: Remove `async` from `async def`. FastAPI will automatically push the `def` function to a background threadpool, keeping the main event loop unblocked. Or, use `await asyncio.sleep(10)`.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─
  CHALLENGE 2: The List Default Danger

  from fastapi import FastAPI, Depends
  
  def get_list(my_list=[]):
      my_list.append("item")
      return my_list
  
  app = FastAPI()
  
  @app.get("/items")
  def read_items(items: list = Depends(get_list)):
      return {"items": items}

  SOLUTION:
    What's wrong? Standard Python gotcha. Default arguments in functions are evaluated once at module load time. The `my_list` is shared across all requests. First request gets `["item"]`, second gets `["item", "item"]`, and memory leaks endlessly.
    Fix: `def get_list(my_list=None): if my_list is None: my_list = [] ...`

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─
  CHALLENGE 3: Pydantic Secret Leak

  class User(BaseModel):
      id: int
      username: str
      password_hash: str
  
  @app.post("/users", response_model=User)
  def create_user(user: UserCreate):
      new_user = db.create(user)
      return new_user

  SOLUTION:
    What's wrong? The `response_model` is set to `User`, which includes the `password_hash`. FastAPI will serialize this and send the password hash back to the client, creating a massive security vulnerability.
    Fix: Create a separate response model `class UserResponse(BaseModel): id: int; username: str` and use that for `response_model`, or exclude the field in Pydantic.

---


────────────────────────────────────────────────────────────────────────────────
  9. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  - Performance: Combining FastAPI with Uvicorn results in Node.js/Go-like performance in Python, saving significant cloud compute costs.
  - Data Integrity: In dynamically typed Python, APIs often crash deep in the codebase because a client sent an integer instead of a string. Pydantic stops bad data at the front door (raising a 422 error automatically) before it ever touches your business logic.
  - Developer Velocity: Auto-generated Swagger docs mean frontend and backend teams stay in sync effortlessly without manually maintaining Postman collections or Wiki pages.
  ---

────────────────────────────────────────────────────────────────────────────────
  10. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

  -> File 41: Python Backend Fundamentals (Review Python Type Hints, which are the engine behind FastAPI.)
  -> File 43: Python SQLAlchemy (Learn how to inject an Async SQLAlchemy database session into a FastAPI route using Dependencies.)

================================================================================
  END OF FILE 042
================================================================================
