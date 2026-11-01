================================================================================
  FILE 033: DATABASE COMPARISON: CHOOSING THE RIGHT TOOL FOR THE JOB
  Section: C - DBMS & Databases
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  This document synthesizes knowledge across relational and NoSQL paradigms. System design interviews frequently require you to justify why you chose a specific database. You will learn the tradeoffs between PostgreSQL, MongoDB, Redis, and Cassandra, focusing on ACID compliance, scaling models, and data structures.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  RELATIONAL (RDBMS)
    Data organized in tables, strict schema, powerful JOINs, ACID guarantees (PostgreSQL, MySQL).

  DOCUMENT STORE
    Data in JSON-like documents, flexible schema, embeds related data (MongoDB, Couchbase).

  KEY-VALUE STORE
    Simplest model, O(1) lookups by key, purely in-memory or persisted (Redis, Memcached).

  WIDE-COLUMN STORE
    Optimized for fast writes and massive datasets, column-family structure (Cassandra, ScyllaDB).

  GRAPH DATABASE
    Optimized for highly connected data and relationship traversal (Neo4j).

  CAP THEOREM
    Consistency, Availability, Partition Tolerance. Distributed databases can only guarantee 2 of the 3 (usually CP or AP).

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  DECISION FLOWCHART                                                     │
  │                                                                         │
  │  [ What is the primary access pattern? ]                                │
  │     |                                                                   │
  │     |-- Highly structured, complex queries, strict consistency?         │
  │     |    `-- [ RDBMS (PostgreSQL / MySQL) ]                             │
  │     |                                                                   │
  │     |-- Sub-millisecond latency, caching, transient data?               │
  │     |    `-- [ Key-Value (Redis) ]                                      │
  │     |                                                                   │
  │     |-- Rapidly changing schema, JSON inputs, hierarchical data?        │
  │     |    `-- [ Document (MongoDB) ]                                     │
  │     |                                                                   │
  │     |-- Heavy write throughput, time-series, immense scale, no JOINs?   │
  │     |    `-- [ Wide-Column (Cassandra) ]                                │
  │     |                                                                   │
  │     `-- Highly interconnected data (recommendations, social networks)?  │
  │          `-- [ Graph (Neo4j) ]                                          │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  4. EXPLANATION & THEORY
────────────────────────────────────────────────────────────────────────────────

  FEATURE COMPARISON MATRIX
  Feature | PostgreSQL | MongoDB | Redis | Cassandra
  Data Model | Relational / Object-Relational | Document (BSON) | Key-Value / Data Structures | Wide-Column
  Primary Use Case | General purpose, ACID transactions | Flexible schema, CMS, Catalogs | Caching, Leaderboards, Pub/Sub | Time-series, IoT, Heavy Writes
  ACID Compliance | Full ACID | Multi-document (since 4.0) | Single command atomicity | Tunable (BASE)
  Scaling | Vertical (Easy), Read Replicas | Horizontal (Sharding built-in) | Sharding (Redis Cluster) | Horizontal (Masterless ring)
  Joins | Excellent | $lookup (Expensive) | N/A | Not supported
  Indexes | B-Tree, GIN, GiST, BRIN | B-Tree, Text, Geospatial | N/A (Has native structures) | Secondary indexes (limited)

  DEEP DIVE: WHY POSTGRESQL USUALLY WINS
  In modern software development, PostgreSQL is often the default choice until proven otherwise.
  1. JSONB: Postgres can store, index (GIN), and query JSON almost as efficiently as MongoDB. It bridges the RDBMS and NoSQL worlds.
  2. Extensibility: PostGIS makes it the best geospatial database in the world. pgvector makes it a vector database for AI embeddings.
  3. Strict Data Integrity: When dealing with money or critical user state, constraints, foreign keys, and strict types prevent application bugs from corrupting data.

────────────────────────────────────────────────────────────────────────────────
  7. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: Explain the CAP Theorem and where MongoDB and Cassandra sit.

  ANSWER:
    Consistency (every read receives the most recent write), Availability (every request receives a non-error response), Partition Tolerance (system operates despite network drops). Network partitions (P) are a physical reality, so you choose C or A. MongoDB is CP (Primary node election causes brief unavailability, but guarantees consistency). Cassandra is AP (Tunable consistency, always available for writes).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: When would you choose MySQL over PostgreSQL?

  ANSWER:
    Historically, MySQL was easier to set up and had better Master-Master replication. Uber notoriously moved from Postgres to MySQL due to write amplification caused by Postgres's MVCC architecture (which requires updating indexes when rows update, though HOT updates mitigate this).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: What is a Graph Database and when is it necessary?

  ANSWER:
    Databases like Neo4j use nodes and edges to store data. In SQL, finding "friends of friends of friends" requires 3 expensive JOINs. In a Graph DB, it is a fast O(1) pointer traversal.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: Why not use Redis for everything?

  ANSWER:
    It is constrained by RAM size, making it far too expensive to store terabytes of historical data. Also, its persistence mechanisms (AOF/RDB) are not as robust against corruption/loss as an RDBMS WAL.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: What does "BASE" mean in NoSQL?

  ANSWER:
    Basically Available, Soft state, Eventual consistency. It is the antithesis of ACID, prioritizing availability and scale over immediate consistency.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: How does DynamoDB differ from MongoDB?

  ANSWER:
    DynamoDB is a managed AWS Key-Value/Document store optimized for single-digit millisecond latency at any scale. It lacks complex aggregation and JOINs, forcing you to heavily denormalize data and rely on Single-Table Design.

────────────────────────────────────────────────────────────────────────────────
  8. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: The Relational Analytics Dashboard

  Scenario: A team is using PostgreSQL to power an internal analytics dashboard calculating sums over 500 million rows. The dashboard takes 30 seconds to load.

  SOLUTION:
    Problem: PostgreSQL is an OLTP (Online Transaction Processing) database. It reads data row-by-row.
    Answer: For massive analytics, data should be ETL'd into an OLAP (Online Analytical Processing) columnar database like Snowflake, ClickHouse, or Amazon Redshift.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 2: The E-Commerce Shopping Cart in SQL

  Scenario: Every time a user adds an item to their cart, an INSERT is made to a Cart SQL table. On Black Friday, the DB locks up due to write contention.

  SOLUTION:
    Problem: Carts are transient, highly volatile data that rarely needs strict ACID guarantees until checkout.
    Answer: Store active shopping carts in Redis. When the user hits "Checkout", persist the final state to PostgreSQL.

────────────────────────────────────────────────────────────────────────────────
  9. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  POLYGLOT PERSISTENCE: Modern architectures rarely use one database. A standard e-commerce stack uses: Postgres (Users, Orders), MongoDB (Product Catalog), Redis (Caching, Sessions), and Elasticsearch (Full-Text Product Search).
  MIGRATION PAIN: Choosing a NoSQL database early on because "we don't know the schema yet," only to realize later you need complex reporting and ACID transactions, is a classic engineering mistake that takes months to untangle.

────────────────────────────────────────────────────────────────────────────────
  10. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

  -> File 031: MongoDB (Deep dive into MongoDB.)
  -> File 034: Database_Scaling (How to scale these DBs.)

================================================================================
  END OF FILE 033
================================================================================
