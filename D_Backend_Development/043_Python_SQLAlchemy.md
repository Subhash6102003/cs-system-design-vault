================================================================================
  FILE 043: PYTHON SQLALCHEMY
  Section: D - Backend Development
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  SQLAlchemy: The Python SQL Toolkit and ORM
  SQLAlchemy is the premier Object-Relational Mapper (ORM) and SQL toolkit for Python. It provides a full suite of well-known enterprise-level persistence patterns, designed for efficient and high-performing database access. This guide covers both the traditional (synchronous) ORM and the modern Async ORM integration, along with handling complex relationships and database migrations using Alembic.
  Prerequisites: Python fundamentals, SQL basics, Relational Database concepts.
  What you'll learn: Engines, Connection Pools, Session Lifecycle, Declarative Models, Relationships, Querying, Eager vs. Lazy Loading, the N+1 problem, Async SQLAlchemy, and Alembic migrations.
  
  ---

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  Core vs. ORM
    SQLAlchemy consists of two parts. **Core** provides a SQL expression language for writing raw-ish SQL using Python objects. **ORM** builds on Core, mapping database tables to Python classes and rows to objects.

  Engine
    The starting point for any SQLAlchemy application. It acts as a registry for the database dialect (e.g., PostgreSQL, MySQL) and maintains the **Connection Pool**.

  Session
    The "workspace" or "transaction" for your objects. It tracks changes to objects and flushes them to the database via SQL statements when necessary.

  Declarative Base
    A factory function that creates a base class. All ORM models inherit from this base class, mapping Python classes to database tables.

  Lazy Loading
    Related objects (e.g., a User's Posts) are not loaded from the database until you explicitly access the attribute (e.g., `user.posts`). Causes the N+1 problem.

  Eager Loading
    Related objects are loaded at the same time as the parent object using JOINs (`joinedload`) or secondary queries (`selectinload`).

  N+1 Problem
    A performance killer where querying $N$ rows results in 1 initial query + $N$ additional queries to fetch related data.

  Alembic
    The standard database migration tool written for SQLAlchemy. It tracks changes to your models and generates upgrade/downgrade scripts.

  --

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  SQLAlchemy Architecture Layers

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  +-------------------------------------------------------------+        │
  │  |                     FastAPI / Application                   |        │
  │  +-------------------------------------------------------------+        │
  │                                |                                        │
  │  +-------------------------------------------------------------+        │
  │  |                     SQLAlchemy ORM                          |        │
  │  |  (Sessions, Declarative Models, Relationships, Unit of Work)|        │
  │  +-------------------------------------------------------------+        │
  │                                |                                        │
  │  +-------------------------------------------------------------+        │
  │  |                     SQLAlchemy CORE                         |        │
  │  |  (SQL Expression Language, Schema Definition, Types)        |        │
  │  +-------------------------------------------------------------+        │
  │                                |                                        │
  │  +-------------------------------------------------------------+        │
  │  |                         Engine                              |        │
  │  |  (Connection Pool, Dialect Specific Execution)              |        │
  │  +-------------------------------------------------------------+        │
  │                                |                                        │
  │  +-------------------------------------------------------------+        │
  │  |                  DBAPI (e.g., psycopg2, asyncpg)            |        │
  │  +-------------------------------------------------------------+        │
  │                                |                                        │
  │  +-------------------------------------------------------------+        │
  │  |                   Relational Database                       |        │
  │  |                 (PostgreSQL, MySQL, SQLite)                 |        │
  │  +-------------------------------------------------------------+        │
  └─────────────────────────────────────────────────────────────────────────┘

---

────────────────────────────────────────────────────────────────────────────────
  5. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  The N+1 Problem and its Fix


  Language: python


  ┌──────────────────────────────────────────────────────────────────────────┐
  │  from sqlalchemy.orm import Session, joinedload                          │
  │  from models import User # Assume User has a one-to-many relationship with 'posts'│
  │                                                                          │
  │  def get_users_bad_performance(db: Session):                             │
  │      # 1. THE N+1 PROBLEM                                                │
  │      # This fires 1 query to get all 100 users: SELECT * FROM users;     │
  │      users = db.query(User).all()                                        │
  │                                                                          │
  │      for user in users:                                                  │
  │          # As we iterate, accessing user.posts fires an ADDITIONAL query for EVERY user.│
  │          # SELECT * FROM posts WHERE user_id = X;                        │
  │          # If there are 100 users, this executes 101 queries total!      │
  │          print(f"User {user.name} has {len(user.posts)} posts.")         │
  │                                                                          │
  │  def get_users_good_performance(db: Session):                            │
  │      # 2. THE FIX: Eager Loading                                         │
  │      # Use joinedload to fetch users AND their posts in a single LEFT OUTER JOIN query.│
  │      # Total queries: 1.                                                 │
  │      users = db.query(User).options(joinedload(User.posts)).all()        │
  │                                                                          │
  │      for user in users:                                                  │
  │          # No extra queries fired here; posts are already in memory.     │
  │          print(f"User {user.name} has {len(user.posts)} posts.")         │
  └──────────────────────────────────────────────────────────────────────────┘

  ---

────────────────────────────────────────────────────────────────────────────────
  6. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

  Async FastAPI + SQLAlchemy ORM Setup


  Language: python


  ┌──────────────────────────────────────────────────────────────────────────┐
  │  # --- database.py ---                                                   │
  │  import os                                                               │
  │  from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession    │
  │  from sqlalchemy.orm import declarative_base, sessionmaker               │
  │                                                                          │
  │  # Uses asyncpg driver for PostgreSQL                                    │
  │  DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:pass@localhost/dbname")│
  │                                                                          │
  │  # Create Async Engine (manages the connection pool)                     │
  │  engine = create_async_engine(DATABASE_URL, echo=False, pool_size=10, max_overflow=20)│
  │                                                                          │
  │  # Create Async Session Factory                                          │
  │  AsyncSessionLocal = sessionmaker(                                       │
  │      bind=engine,                                                        │
  │      class_=AsyncSession,                                                │
  │      expire_on_commit=False,                                             │
  │      autocommit=False,                                                   │
  │      autoflush=False,                                                    │
  │  )                                                                       │
  │                                                                          │
  │  Base = declarative_base()                                               │
  │                                                                          │
  │  # Dependency for FastAPI                                                │
  │  async def get_db():                                                     │
  │      async with AsyncSessionLocal() as session:                          │
  │          try:                                                            │
  │              yield session                                               │
  │              await session.commit()                                      │
  │          except Exception:                                               │
  │              await session.rollback()                                    │
  │              raise                                                       │
  │          finally:                                                        │
  │              await session.close()                                       │
  │                                                                          │
  │                                                                          │
  │  # --- models.py ---                                                     │
  │  from sqlalchemy import Column, Integer, String, ForeignKey              │
  │  from sqlalchemy.orm import relationship                                 │
  │  from database import Base                                               │
  │                                                                          │
  │  class User(Base):                                                       │
  │      __tablename__ = "users"                                             │
  │      id = Column(Integer, primary_key=True, index=True)                  │
  │      username = Column(String(50), unique=True, nullable=False)          │
  │                                                                          │
  │      # One-to-Many Relationship                                          │
  │      items = relationship("Item", back_populates="owner", cascade="all, delete-orphan")│
  │                                                                          │
  │  class Item(Base):                                                       │
  │      __tablename__ = "items"                                             │
  │      id = Column(Integer, primary_key=True, index=True)                  │
  │      title = Column(String(100), nullable=False)                         │
  │      owner_id = Column(Integer, ForeignKey("users.id"))                  │
  │                                                                          │
  │      # Back-reference                                                    │
  │      owner = relationship("User", back_populates="items")                │
  │                                                                          │
  │                                                                          │
  │  # --- main.py (FastAPI Routes) ---                                      │
  │  from fastapi import FastAPI, Depends, HTTPException                     │
  │  from sqlalchemy.ext.asyncio import AsyncSession                         │
  │  from sqlalchemy.future import select                                    │
  │  from sqlalchemy.orm import selectinload                                 │
  │  from database import get_db                                             │
  │  import models                                                           │
  │                                                                          │
  │  app = FastAPI()                                                         │
  │                                                                          │
  │  @app.get("/users/{user_id}/items")                                      │
  │  async def get_user_with_items(user_id: int, db: AsyncSession = Depends(get_db)):│
  │      # Async 2.0 Query Style                                             │
  │      # Use selectinload for 1-to-many eager loading (avoids cartesian product issues)│
  │      stmt = select(models.User).where(models.User.id == user_id).options(selectinload(models.User.items))│
  │      result = await db.execute(stmt)                                     │
  │      user = result.scalar_one_or_none()                                  │
  │                                                                          │
  │      if not user:                                                        │
  │          raise HTTPException(status_code=404, detail="User not found")   │
  │                                                                          │
  │      return {"user": user.username, "items": [{"id": i.id, "title": i.title} for i in user.items]}│
  │                                                                          │
  │  @app.post("/users/")                                                    │
  │  async def create_user(username: str, db: AsyncSession = Depends(get_db)):│
  │      new_user = models.User(username=username)                           │
  │      db.add(new_user)                                                    │
  │      # The session is committed automatically by the get_db dependency if no exception occurs│
  │      return {"msg": "User created"}                                      │
  └──────────────────────────────────────────────────────────────────────────┘

  Alembic Workflow (Terminal Commands)


  Language: bash


  ┌──────────────────────────────────────────────────────────────────────────┐
  │  # 1. Initialize Alembic (creates alembic.ini and /alembic folder)       │
  │  alembic init -t async alembic                                           │
  │                                                                          │
  │  # 2. Edit alembic/env.py to point to your Base.metadata and Database URL│
  │                                                                          │
  │  # 3. Generate a migration script automatically based on models.py changes│
  │  alembic revision --autogenerate -m "create users and items tables"      │
  │                                                                          │
  │  # 4. Apply the migration to the database (Run 'up' scripts)             │
  │  alembic upgrade head                                                    │
  │                                                                          │
  │  # 5. Rollback if something breaks (Run 'down' scripts)                  │
  │  alembic downgrade -1                                                    │
  └──────────────────────────────────────────────────────────────────────────┘

  ---

────────────────────────────────────────────────────────────────────────────────
  7. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: What is the purpose of the SQLAlchemy `Session`?

  ANSWER:
    The Session acts as a "holding zone" or "Unit of Work" for objects loaded from or destined for the database. It tracks changes to objects (Identity Map), manages the transaction lifecycle (begin, commit, rollback), and translates operations into SQL via the Engine.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: What is the N+1 problem and how do you solve it in SQLAlchemy?

  ANSWER:
    It occurs when querying a list of parent objects (1 query) and lazily loading a related collection for each parent as you iterate ($N$ queries). Solve it using eager loading strategies: `joinedload` (generates an INNER/OUTER JOIN, best for many-to-one) or `selectinload` (emits a second SELECT statement with an IN clause, best for one-to-many collections).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: What is the difference between `expire_on_commit=True` and `False`?

  ANSWER:
    By default, when a Session commits, it "expires" all instances, meaning their attributes are marked as stale. If you try to access them again, SQLAlchemy will emit a fresh database query. In Async environments (like FastAPI), this causes errors because implicit IO is not allowed. Setting it to `False` keeps the object data in memory after commit.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: Why do we need Alembic? Why not just use `Base.metadata.create_all(engine)`?

  ANSWER:
    `create_all()` can only create *new* tables. It cannot modify existing tables (e.g., adding a new column, changing a data type, dropping a table). Alembic provides full schema migrations, version control for the database, and rollback capabilities.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: Explain the difference between SQLAlchemy 1.4 (Query syntax) and 2.0 (Select syntax).

  ANSWER:
    In older syntax, you used `session.query(User).filter(User.id == 1)`. In the modern 2.0 (and async) syntax, you construct a SQL expression using Core: `stmt = select(User).where(User.id == 1)`, and then execute it via the session: `session.execute(stmt)`. This unifies Core and ORM paradigms.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: How does SQLAlchemy handle Connection Pooling?

  ANSWER:
    The `Engine` maintains a `QueuePool` by default. Instead of closing a TCP connection to the database when a request finishes, it returns the connection to the pool. When a new request comes in, it reuses an idle connection, dramatically reducing database connection latency.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q7: What does `flush()` do compared to `commit()`?

  ANSWER:
    `flush()` pushes all pending object changes (INSERTs, UPDATEs) to the database, allowing you to get newly generated primary keys, but the transaction remains *open* (uncommitted). `commit()` permanently saves those changes to the database and ends the transaction.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q8: How does the Identity Map pattern work in SQLAlchemy?

  ANSWER:
    The Session maintains a dictionary of all objects it has loaded, keyed by their primary key. If you query for a user with ID 1, and then query for user ID 1 again in the same session, SQLAlchemy returns the exact same Python object from memory without hitting the database again.

---

────────────────────────────────────────────────────────────────────────────────
  8. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: The Detached Object

  def update_user_status(user_id: int):
      session = SessionLocal()
      user = session.query(User).get(user_id)
      session.close() # Connection returned to pool
      
      # Later in the code...
      print(user.items) # Accessing a relationship

  SOLUTION:
    What's wrong? The session is closed. Accessing `user.items` triggers a Lazy Load (an implicit database query). Because the session is closed, the object is "detached", and SQLAlchemy will throw an `Instance(s) is detached` or `DetachedInstanceError`.
    Fix: Eager load the relationship before closing the session (`joinedload`), or keep the session open via a context manager until all operations are finished.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─
  CHALLENGE 2: The Silent Rollback Fail

  def process_payment(db: Session, order):
      try:
          order.status = "PAID"
          db.commit()
      except Exception as e:
          print("Payment failed!")
          # BUG: What's missing here?

  SOLUTION:
    What's wrong? If `db.commit()` raises an IntegrityError (e.g., unique constraint violation), the exception is caught, but the session remains in a failed, invalid state. Any subsequent queries using this session will crash.
    Fix: Always call `db.rollback()` in the `except` block to clean up the transaction state before reusing or closing the session.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─
  CHALLENGE 3: Async Implicit I/O

  @app.get("/users/{id}")
  async def get_user(id: int, db: AsyncSession = Depends(get_db)):
      result = await db.execute(select(User).where(User.id == id))
      user = result.scalar_one()
      # User.items is a lazily loaded relationship
      items = user.items 
      return {"user": user.name, "items": items}

  SOLUTION:
    What's wrong? `user.items` attempts to lazy load the items by firing a SQL query synchronously under the hood. In `asyncio`, doing synchronous blocking I/O raises a `MissingGreenlet` error because you cannot perform an `await` implicitly inside a property accessor.
    Fix: You must eagerly load the relationship in the initial query using `.options(selectinload(User.items))`.

---


────────────────────────────────────────────────────────────────────────────────
  9. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  - Database Scalability: Poorly managed sessions (connection leaks) or N+1 query problems will throttle your database CPU to 100% and bring down production under moderate traffic.
  - Data Integrity: Leveraging the Unit of Work pattern ensures that complex operations (e.g., deducting inventory and charging a user) are atomic. If one fails, the rollback guarantees no partial data corruption.
  - Migration Safety: Using Alembic ensures that database schema changes are reviewed as code (PRs), run deterministically in CI/CD pipelines, and can be reversed if a deployment fails.
  ---

────────────────────────────────────────────────────────────────────────────────
  10. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

  -> File 42: Python FastAPI (Learn how FastAPI uses Dependency Injection to securely provide the Database Session.)
  -> File 38: NodeJS PostgreSQL (Compare Python's ORM approach with Node.js raw parameterized queries and connection pooling.)

================================================================================
  END OF FILE 043
================================================================================
