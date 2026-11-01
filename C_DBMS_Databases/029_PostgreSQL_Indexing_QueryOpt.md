================================================================================
  FILE 029: POSTGRESQL INDEXING & QUERY OPTIMIZATION: MAKING DATA FAST
  Section: C - DBMS & Databases
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  This document covers the crucial skill of retrieving data efficiently. A database without proper indexing is just an expensive, slow text file. You will learn the mechanics of different index types (B-Tree, GIN, GiST), advanced indexing strategies (Partial, Expression, Composite), and how to read and interpret EXPLAIN ANALYZE outputs to diagnose and fix slow queries.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  INDEX
    A distinct data structure that stores a subset of table columns in a highly organized way (usually a tree) to allow fast O(log N) lookups instead of O(N) sequential scans.

  B-TREE (BALANCED TREE)
    The default index type. Stores data sorted, allowing fast equality (=) and range (<, >, BETWEEN) queries.

  GIN (GENERALIZED INVERTED INDEX)
    Used for data types containing multiple values (Arrays, JSONB, Full-Text Search documents).

  GIST (GENERALIZED SEARCH TREE)
    Used for complex geometric and geospatial data (PostGIS), like "find all points within this polygon".

  BRIN (BLOCK RANGE INDEX)
    Very small index used for naturally ordered large tables (like time-series logs) by storing min/max values per disk block.

  SEQUENTIAL SCAN (SEQ SCAN)
    Scanning every row in a table. Bad for single row lookups, good for fetching 90% of the table.

  INDEX SCAN
    Traversing the index to find row pointers, then fetching the actual row from the heap (table).

  INDEX ONLY SCAN
    Fetching data entirely from the index without visiting the heap. Only possible if the index contains all queried columns and MVCC visibility checks pass.

  EXPLAIN
    A command that reveals the execution plan chosen by the PostgreSQL Query Planner.

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  B-TREE INDEX STRUCTURE                                                 │
  │                                                                         │
  │                            [ 50,  100 ]            <-- Root Node (Page) │
  │                          /      |       \                               │
  │             -------------       |        --------------                 │
  │            /                    |                      \                │
  │      [10, 30]                [60, 80]              [120, 150]  <-- Internal Nodes│
  │     /    |   \              /   |    \             /    |    \          │
  │   [5]  [15]  [35]        [55]  [70]  [90]      [110]  [130] [160] <-- Leaf Nodes (Sorted)│
  │    |     |     |          |     |      |         |      |     |         │
  │    v     v     v          v     v      v         v      v     v         │
  │   TIDs (Tuple IDs/Pointers to exact physical disk block and row in the Heap)│
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

  Leftmost Prefix Rule: In a composite index (A, B, C), you can use the index to search for A, or A AND B, or A AND B AND C. You cannot efficiently use the index if you only search for B or C.

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  READING AN EXPLAIN PLAN TREE                                           │
  │                                                                         │
  │  -> Limit  (cost=X..Y)                                                  │
  │     -> Sort  (cost=X..Y)                                                │
  │        -> Hash Join  (cost=X..Y)                                        │
  │           -> Seq Scan on Users                                          │
  │           -> Hash                                                       │
  │              -> Index Scan on Orders                                    │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

  Read from the bottom up, inside out. The deepest indentation happens first.

────────────────────────────────────────────────────────────────────────────────
  5. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: SQL]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Basic & Composite Indexes                                            │
  │                                                                          │
  │  -- Default B-Tree Index                                                 │
  │  CREATE INDEX idx_users_email ON users(email);                           │
  │                                                                          │
  │  -- Composite Index (Order matters! Filter column first, then secondary) │
  │  CREATE INDEX idx_orders_user_status ON orders(user_id, status);         │
  │                                                                          │
  │  -- This uses the index efficiently:                                     │
  │  SELECT * FROM orders WHERE user_id = 5 AND status = 'shipped';          │
  │                                                                          │
  │  -- This CANNOT use the composite index efficiently (violates leftmost prefix):│
  │  SELECT * FROM orders WHERE status = 'shipped';                          │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

  [Language: SQL]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Advanced Indexes                                                     │
  │                                                                          │
  │  -- Partial Index: Only index active users. Drastically reduces index size!│
  │  CREATE INDEX idx_users_active_email ON users(email)                     │
  │  WHERE status = 'ACTIVE';                                                │
  │                                                                          │
  │  -- Expression Index: Indexing a function applied to a column            │
  │  CREATE INDEX idx_users_lower_email ON users(LOWER(email));              │
  │  -- Query must exactly match the expression to use the index:            │
  │  SELECT * FROM users WHERE LOWER(email) = 'bob@example.com';             │
  │                                                                          │
  │  -- GIN Index for JSONB data                                             │
  │  CREATE INDEX idx_users_metadata ON users USING GIN (metadata);          │
  │  -- Query using JSONB containment operator                               │
  │  SELECT * FROM users WHERE metadata @> '{"role": "admin"}';              │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

  Always use EXPLAIN (ANALYZE, BUFFERS) to diagnose queries. ANALYZE actually runs the query (careful with UPDATE/DELETE!). BUFFERS shows memory vs disk usage.

  [Language: SQL]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Analyzing Queries                                                    │
  │                                                                          │
  │  EXPLAIN (ANALYZE, BUFFERS)                                              │
  │  SELECT u.name, o.total                                                  │
  │  FROM users u                                                            │
  │  JOIN orders o ON u.id = o.user_id                                       │
  │  WHERE u.status = 'ACTIVE'                                               │
  │  ORDER BY o.created_at DESC                                              │
  │  LIMIT 10;                                                               │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

  Example Output Interpretation:

  [Language: TEXT]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │                                                                          │
  │  Limit  (cost=100.50..100.60 rows=10 width=36) (actual time=12.4..12.5 rows=10 loops=1)│
  │    Buffers: shared hit=45 read=5                                         │
  │    -> Nested Loop  (cost=0.56..5050.20 rows=500 width=36) (...)          │
  │         -> Index Scan using idx_users_status on users u (...)            │
  │              Index Cond: (status = 'ACTIVE'::text)                       │
  │         -> Index Scan using idx_orders_user_id on orders o (...)         │
  │              Index Cond: (user_id = u.id)                                │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

  cost=X..Y: Planner's estimate. X is start-up cost, Y is total cost.
  actual time=A..B: Actual execution time in milliseconds.
  shared hit=45: Found 45 pages in memory (Shared Buffers). Excellent!
  read=5: Had to fetch 5 pages from disk.

────────────────────────────────────────────────────────────────────────────────
  7. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: When is a Sequential Scan faster than an Index Scan?

  ANSWER:
    When retrieving a large percentage of the table (e.g., > 20%). Sequential I/O reading the raw table is faster than reading the index and performing random I/O hops to fetch every row from the heap.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: What is a Covering Index?

  ANSWER:
    An index that contains all the columns needed for a query, allowing an "Index Only Scan". In Postgres, you can use the INCLUDE clause: CREATE INDEX idx ON tbl(a) INCLUDE (b, c); to store non-searchable payload data in the index leaf nodes.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: Explain the Leftmost Prefix rule in composite indexes.

  ANSWER:
    An index on (A, B, C) is sorted by A, then B within A, then C within B. If you search WHERE B=1, the index is useless because B is scattered across the tree under various values of A.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: Why did my query not use the index I just created?

  ANSWER:
    Several reasons: Statistics are outdated (needs ANALYZE), the planner estimated a Seq Scan is faster, you wrapped the column in a function without using an expression index, or data types mismatched (e.g., comparing a string to an integer).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: What is a Hash Join vs a Nested Loop Join?

  ANSWER:
    Nested Loop scans the outer table row by row, doing an index lookup in the inner table for each (good for small datasets). Hash Join builds an in-memory hash table of the smaller table, then scans the larger table against it (good for large, unindexed bulk joins).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: How do you find unused indexes in PostgreSQL?

  ANSWER:
    Query the pg_stat_user_indexes view. Look for indexes where idx_scan is 0 or very low, but idx_tup_read / idx_tup_fetch are high (meaning writes are slowing down but reads aren't happening).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q7: What is a BRIN index and when is it useful?

  ANSWER:
    Block Range Index. It stores min/max values for sequential blocks of data. Extremely useful for IoT/Time-series data where created_at correlates directly with physical insertion order. It's 99% smaller than a B-Tree.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q8: How does the LIMIT clause affect the query planner?

  ANSWER:
    It often encourages the planner to use an Index Scan to find the first N rows quickly, rather than a Seq Scan/Hash Join that requires processing the whole set before returning the top N.

────────────────────────────────────────────────────────────────────────────────
  8. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: The Function Trap

  CREATE INDEX idx_user_created ON users(created_at);
  -- Query:
  SELECT * FROM users WHERE DATE(created_at) = '2023-01-01';

  SOLUTION:
    Problem: Wrapping created_at in the DATE() function hides it from the index. The DB must evaluate the function for every row (Seq Scan).
    Answer: Rewrite the query to use range bounds against the raw column: WHERE created_at >= '2023-01-01' AND created_at < '2023-01-02', or create an expression index on DATE(created_at).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 2: The Like "%Wildcard%"

  CREATE INDEX idx_user_name ON users(name);
  SELECT * FROM users WHERE name LIKE '%John%';

  SOLUTION:
    Problem: B-Trees cannot evaluate leading wildcards. This will result in a Seq Scan.
    Answer: For substring search, use a trigram index (pg_trgm extension) with a GiST or GIN index.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 3: OR conditions

  CREATE INDEX idx_status ON users(status);
  CREATE INDEX idx_type ON users(type);
  SELECT * FROM users WHERE status = 'ACTIVE' OR type = 'ADMIN';

  SOLUTION:
    Problem: While Postgres can do a "BitmapOr" using both indexes, complex OR queries are notoriously hard to optimize.
    Answer: Often, writing this as a UNION ALL of two queries (one for status, one for type) can drastically improve the execution plan.

────────────────────────────────────────────────────────────────────────────────
  9. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  WRITE PENALTY: Every index you add slows down INSERT, UPDATE, and DELETE operations, taking up memory and disk. Over-indexing is a common production killer.
  N+1 QUERIES VS JOINS: Understanding EXPLAIN plans helps developers realize why letting an ORM execute 1000 individual queries (N+1 problem) is fundamentally worse than one optimized JOIN with an Index Scan.

────────────────────────────────────────────────────────────────────────────────
  10. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

  -> File 028: PostgreSQL_MVCC_WAL (How MVCC affects Index-Only scans (requires visibility map).)
  -> File 031: MongoDB (Compare B-Tree with MongoDB's B-Tree indexing.)

================================================================================
  END OF FILE 029
================================================================================
