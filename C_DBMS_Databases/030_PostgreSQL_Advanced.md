================================================================================
  FILE 030: POSTGRESQL ADVANCED FEATURES: PARTITIONING, REPLICATION, AND BEYOND
  Section: C - DBMS & Databases
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  This document explores the advanced capabilities that make PostgreSQL an enterprise-grade database. Once a database grows beyond a few hundred gigabytes, standard indexing is no longer enough. You will learn about Table Partitioning for massive data management, Streaming and Logical Replication for High Availability (HA), JSONB capabilities that make Postgres a viable NoSQL alternative, TOAST for large data storage, and connection pooling.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  TABLE PARTITIONING
    Splitting a massive logical table into smaller physical tables (partitions) based on a key (e.g., date ranges).

  REPLICATION
    Copying data from a Primary node to one or more Replica nodes.
    - Physical (Streaming) Replication: Byte-for-byte block copy using the WAL.
    - Logical Replication: Row-based replication of specific tables using a Publisher/Subscriber model.

  TOAST (THE OVERSIZED-ATTRIBUTE STORAGE TECHNIQUE)
    Postgres page size is 8KB. If a row exceeds this (e.g., a massive text or JSON field), Postgres transparently compresses and moves the large field into a hidden TOAST table.

  JSONB
    Binary JSON. Unlike standard JSON (which stores raw text), JSONB parses the data into a binary tree, enabling indexing, fast lookups, and manipulation.

  CONNECTION POOLING
    Managing a cache of open database connections (e.g., PgBouncer). Postgres processes are heavy; pooling maps thousands of lightweight client connections to a few heavyweight database processes.

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  TABLE PARTITIONING (RANGE)                                             │
  │                                                                         │
  │                            [ Logical Table: "orders" ]                  │
  │                           /             |             \                 │
  │            (Jan 2023 - Mar 2023)  (Apr 2023 - Jun 2023)  (Jul 2023 - Sep 2023)│
  │                   /                     |                     \         │
  │  [ orders_2023_q1 ]           [ orders_2023_q2 ]           [ orders_2023_q3 ]│
  │     (Physical)                   (Physical)                   (Physical)│
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘
  Querying the parent table routes the query only to the relevant partition(s) via "Partition Pruning".

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  STREAMING REPLICATION TOPOLOGY                                         │
  │                                                                         │
  │        [ Primary Node ]  ===( WAL Stream )===> [ Standby / Replica Node ]│
  │        - Read / Write                          - Read Only              │
  │        - Generates WAL                         - Replays WAL immediately│
  │        - Handles active traffic                - Hot standby for Failover│
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: SQL]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Range Partitioning Setup                                             │
  │                                                                          │
  │  -- 1. Create parent partitioned table                                   │
  │  CREATE TABLE event_logs (                                               │
  │      id SERIAL,                                                          │
  │      event_name VARCHAR(100),                                            │
  │      created_at TIMESTAMP NOT NULL                                       │
  │  ) PARTITION BY RANGE (created_at);                                      │
  │                                                                          │
  │  -- 2. Create physical partitions                                        │
  │  CREATE TABLE event_logs_2023_q1 PARTITION OF event_logs                 │
  │      FOR VALUES FROM ('2023-01-01') TO ('2023-04-01');                   │
  │                                                                          │
  │  CREATE TABLE event_logs_2023_q2 PARTITION OF event_logs                 │
  │      FOR VALUES FROM ('2023-04-01') TO ('2023-07-01');                   │
  │                                                                          │
  │  -- 3. Insert data (automatically routed)                                │
  │  INSERT INTO event_logs (event_name, created_at)                         │
  │  VALUES ('login', '2023-02-15 10:00:00'); -- Goes to q1 partition        │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

  [Language: SQL]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // JSONB Power Queries                                                  │
  │                                                                          │
  │  CREATE TABLE users_docs (                                               │
  │      id SERIAL PRIMARY KEY,                                              │
  │      profile JSONB                                                       │
  │  );                                                                      │
  │                                                                          │
  │  INSERT INTO users_docs (profile) VALUES                                 │
  │  ('{"name": "Alice", "tags": ["admin", "dev"], "address": {"city": "NY"}}');│
  │                                                                          │
  │  -- Extract text value using ->> (Returns text)                          │
  │  SELECT profile->>'name' FROM users_docs; -- 'Alice'                     │
  │                                                                          │
  │  -- Extract JSON object using -> (Returns JSONB)                         │
  │  SELECT profile->'address' FROM users_docs; -- '{"city": "NY"}'          │
  │                                                                          │
  │  -- Containment operator @> (Does the left contain the right?)           │
  │  SELECT * FROM users_docs WHERE profile @> '{"tags": ["admin"]}';        │
  │                                                                          │
  │  -- Create a GIN index on the JSONB column for rapid queries             │
  │  CREATE INDEX idx_users_profile ON users_docs USING GIN (profile);       │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

  Connection Pooling (PgBouncer)
  Postgres forks a whole OS process for every connection. If your Node.js microservices open 5,000 connections, Postgres will run out of memory and crash.
  - Session Pooling: Connection tied to client for the whole session.
  - Transaction Pooling (Recommended): Client gets a real connection only during a transaction (BEGIN to COMMIT). Enables 5,000 microservice connections to be served by 100 actual Postgres backend processes.

  [Language: INI]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Critical postgresql.conf Parameters                                  │
  │                                                                          │
  │  # Memory used by shared buffers (recommendation: 25% of system RAM)     │
  │  shared_buffers = 4GB                                                    │
  │                                                                          │
  │  # Memory used per operation (e.g., sorting). High values prevent disk spilling, but are per-connection!│
  │  work_mem = 32MB                                                         │
  │                                                                          │
  │  # Helps planner estimate if data fits in OS cache (recommendation: 50-75% of RAM)│
  │  effective_cache_size = 12GB                                             │
  │                                                                          │
  │  # Max connections (keep low, use PgBouncer in front)                    │
  │  max_connections = 200                                                   │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  7. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: What is the difference between JSON and JSONB in PostgreSQL?

  ANSWER:
    JSON stores an exact text copy, preserving whitespace and duplicate keys; it requires parsing on every execution. JSONB stores a parsed binary format, removing whitespace and duplicates; it is faster to process, supports GIN indexing, and enables advanced query operators.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: How does Table Partitioning improve performance?

  ANSWER:
    1. Partition Pruning: Queries filtering by the partition key only scan relevant partitions, skipping massive amounts of data. 2. Maintenance: You can easily drop old data by running DROP TABLE old_partition (O(1) operation), instead of a massive DELETE that causes MVCC bloat.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: Explain Physical vs Logical Replication.

  ANSWER:
    Physical (Streaming) replication copies block-level changes via WAL; the replica is an exact byte-for-byte clone of the entire server. Logical replication decodes WAL into row-level changes (INSERT/UPDATE), allowing replication of specific tables, replicating to different Postgres versions, or transforming data.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: What is TOAST and why does it exist?

  ANSWER:
    The Oversized-Attribute Storage Technique. Postgres pages are 8KB. Rows cannot span pages. If a row exceeds 8KB, large columns are chunked, compressed, and moved to a separate TOAST table, leaving a pointer in the main table.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: What happens in synchronous vs asynchronous replication?

  ANSWER:
    In Async (default), the Primary commits the transaction and responds to the client immediately, then sends WAL to the replica. Risk: If Primary dies, recent commits might be lost. In Sync, the Primary waits for the Replica to confirm it wrote the WAL before responding to the client. Risk: Slower writes, and if Replica dies, Primary write operations block.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: Why do we need a connection pooler like PgBouncer?

  ANSWER:
    Because PostgreSQL uses a process-per-connection model. Spawning processes is heavy, and too many active processes cause memory starvation and context-switching overhead.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q7: What is Full-Text Search in Postgres?

  ANSWER:
    Utilizing tsvector (parsed text data) and tsquery (search terms). It provides stemming, ranking, and stop-word removal, far exceeding the capabilities of LIKE.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q8: How do you identify the slowest queries in a production database?

  ANSWER:
    Enable the pg_stat_statements extension. It tracks execution statistics of all SQL statements, allowing you to query by highest total_time or mean_time.

────────────────────────────────────────────────────────────────────────────────
  8. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: The Partitioning Missing Key

  CREATE TABLE users ( id SERIAL, created_at TIMESTAMP ) PARTITION BY RANGE (created_at);
  -- Later...
  ALTER TABLE users ADD PRIMARY KEY (id);

  SOLUTION:
    Problem: In PostgreSQL, the Primary Key or Unique Constraint on a partitioned table must include the partition key.
    Answer: ALTER TABLE users ADD PRIMARY KEY (id, created_at);

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 2: Synchronous Standby Freeze

  Scenario: You set synchronous_commit = on and synchronous_standby_names = 'replica1'. Suddenly, your application cannot write anything to the database. Reads work fine.

  SOLUTION:
    Problem: The standby node (replica1) went offline. The primary is indefinitely waiting for the standby to acknowledge the WAL write.
    Answer: Fix the replica, or temporarily turn off synchronous commit/remove the standby name from the config, reload, and accept async replication.

────────────────────────────────────────────────────────────────────────────────
  9. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  DATA LIFECYCLE: Time-series data (logs, telemetry) grows infinitely. Without partitioning, deleting a billion rows of 1-year-old data will destroy database performance via transaction logs and bloat. With partitioning, dropping a partition takes milliseconds.
  MICROSERVICE DBS: Logical replication is the premier way to stream change-data-capture (CDC) events out of a monolith DB into microservices, or into analytical warehouses (e.g., using Debezium).

────────────────────────────────────────────────────────────────────────────────
  10. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

  -> File 034: Database_Scaling (How to scale out using read replicas and sharding.)
  -> File 031: MongoDB (Compare Postgres JSONB capabilities against a native document store.)

================================================================================
  END OF FILE 030
================================================================================
