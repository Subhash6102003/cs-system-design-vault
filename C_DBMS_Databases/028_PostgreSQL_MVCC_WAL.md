================================================================================
  FILE 028: POSTGRESQL INTERNAL ARCHITECTURE: MVCC, WAL, AND CHECKPOINTS
  Section: C - DBMS & Databases
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  This document dives deep into the engine of PostgreSQL. To operate databases at scale, you must understand how they handle concurrent transactions and guarantee data durability without locking the entire database. You will learn the process architecture of Postgres, how Multi-Version Concurrency Control (MVCC) enables high concurrency, the lifecycle of a row (tuple), how Write-Ahead Logging (WAL) guarantees the 'D' in ACID, and how Autovacuum prevents database bloat.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  POSTMASTER
    The main supervisor process in PostgreSQL that listens for connections and forks worker processes.

  SHARED BUFFERS
    PostgreSQL's in-memory cache of 8KB disk pages. Reads and writes happen here first.

  MVCC (MULTI-VERSION CONCURRENCY CONTROL)
    The mechanism allowing multiple transactions to read and write simultaneously by creating multiple versions of rows. "Readers don't block writers, writers don't block readers."

  TUPLE
    A physical row version in a PostgreSQL data page.

  XMIN
    The transaction ID (XID) that inserted the tuple.

  XMAX
    The transaction ID (XID) that deleted or updated the tuple (0 if not deleted).

  TRANSACTION SNAPSHOT
    The state of all active transactions at a specific point in time, used to determine visibility.

  DEAD TUPLE
    A tuple version that is no longer visible to any active transaction.

  BLOAT
    Wasted disk space and degraded performance caused by an accumulation of dead tuples.

  VACUUM
    A maintenance process that scans tables to mark dead tuples' space as available for future inserts.

  WAL (WRITE-AHEAD LOG)
    An append-only log of all changes. Changes are written to WAL (and flushed to disk) before they are applied to the actual data files.

  CHECKPOINT
    The process of flushing all modified ("dirty") pages from Shared Buffers to actual disk data files.

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  POSTGRESQL PROCESS ARCHITECTURE                                        │
  │                                                                         │
  │  Client Connection ---> [ Postmaster (Supervisor) ] ---> Forks Backend Process│
  │                                 |                                       │
  │                     +-----------+-----------+                           │
  │                     |                       |                           │
  │            [ Backend Process 1 ]   [ Backend Process 2 ] ... (One per connection)│
  │                     |                       |                           │
  │  ===================|=======================|===========================│
  │  SHARED MEMORY      v                       v                           │
  │               [ Shared Buffers (8KB Pages cache) ] <---> [ WAL Buffers ]│
  │  ===================|=======================|================|==========│
  │  BACKGROUND W.      |                       |                |          │
  │               [ Background Writer ]   [ Checkpointer ]  [ WAL Writer ]  │
  │                     |                       |                |          │
  │                     v                       v                v          │
  │  DISK         [ Data Files (.heap) ]  [ Data Files ]    [ WAL Segments ]│
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  MVCC TUPLE VERSIONING FLOW                                             │
  │                                                                         │
  │  Page 1 (Table Data):                                                   │
  │  Tuple 1: (id=1, name='Alice') | xmin=100 | xmax=102 (Marked deleted by 102)│
  │  Tuple 2: (id=1, name='Bob')   | xmin=102 | xmax=0   (Inserted by 102, active)│
  │                                                                         │
  │  Active Snapshot for Tx 101: Can see Tuple 1 (Tx 102 is in the future for 101)│
  │  Active Snapshot for Tx 103: Can see Tuple 2 (Tx 102 is committed in the past for 103)│
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘
  Scenario: UPDATE users SET name = 'Bob' WHERE id = 1 (Transaction 102)

────────────────────────────────────────────────────────────────────────────────
  4. EXPLANATION & THEORY
────────────────────────────────────────────────────────────────────────────────

  PRODUCTION CONCEPT: WAL AND CHECKPOINTS
  Why not write directly to data files?
  Writing 8KB pages randomly across the disk is extremely slow (random I/O). Instead, Postgres writes changes sequentially to the WAL (fast sequential I/O).

  The Flow of a COMMIT:
  1. Backend process alters data in Shared Buffers (memory). Page is now "dirty".
  2. Backend creates a WAL record of the change and writes it to WAL Buffers.
  3. On COMMIT, the WAL Writer synchronously flushes WAL Buffers to disk (fsync). The commit is acknowledged to the user. At this point, the database could crash, and data is safe.
  4. Later, the Checkpointer process periodically writes the "dirty" 8KB pages from Shared Buffers to the actual table data files.

  Crash Recovery:
  If the server crashes between step 3 and 4, the data files are outdated. On restart, Postgres reads the WAL from the last Checkpoint and replays the changes into the data files.

────────────────────────────────────────────────────────────────────────────────
  5. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: SQL]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Inspecting MVCC                                                      │
  │                                                                          │
  │  -- Setup                                                                │
  │  CREATE EXTENSION IF NOT EXISTS pageinspect;                             │
  │  CREATE TABLE mvcc_demo (id INT, val TEXT);                              │
  │                                                                          │
  │  -- Insert a row (Assume this runs in Transaction ID 500)                │
  │  INSERT INTO mvcc_demo VALUES (1, 'Initial');                            │
  │                                                                          │
  │  -- Check hidden system columns                                          │
  │  SELECT xmin, xmax, * FROM mvcc_demo;                                    │
  │  -- Output: xmin=500, xmax=0, id=1, val='Initial'                        │
  │                                                                          │
  │  -- Update the row (Assume Transaction ID 501)                           │
  │  UPDATE mvcc_demo SET val = 'Updated' WHERE id = 1;                      │
  │                                                                          │
  │  -- Check system columns again                                           │
  │  SELECT xmin, xmax, * FROM mvcc_demo;                                    │
  │  -- Output: xmin=501, xmax=0, id=1, val='Updated'                        │
  │                                                                          │
  │  -- The old row is hidden, but still physically on disk!                 │
  │  -- We can inspect the raw heap page:                                    │
  │  SELECT t_xmin, t_xmax, t_data                                           │
  │  FROM heap_page_items(get_raw_page('mvcc_demo', 0));                     │
  │  -- Output shows TWO items:                                              │
  │  -- 1. t_xmin=500, t_xmax=501 (The dead tuple)                           │
  │  -- 2. t_xmin=501, t_xmax=0   (The live tuple)                           │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘
  You can actually see MVCC in action using the pageinspect extension.

────────────────────────────────────────────────────────────────────────────────
  7. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: Why does PostgreSQL require VACUUM while MySQL (InnoDB) mostly does not?

  ANSWER:
    Postgres implements MVCC by storing all row versions in the main table data (heap). Updates create new rows and leave dead ones behind. InnoDB stores the current row in the table and old versions in an Undo Log, which is purged differently. Postgres needs VACUUM to reclaim space in the heap.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: What is the difference between VACUUM and VACUUM FULL?

  ANSWER:
    Standard VACUUM marks dead space as reusable without locking the table for reads/writes. VACUUM FULL aggressively rewrites the entire table to a new file, reclaiming disk space to the OS, but takes an exclusive lock, blocking all access.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: Explain xmin and xmax.

  ANSWER:
    System columns on every row. xmin is the Transaction ID that created the row. xmax is the ID of the transaction that updated/deleted the row.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: How does PostgreSQL ensure Durability (ACID)?

  ANSWER:
    Through Write-Ahead Logging (WAL). A transaction isn't reported as committed until its WAL records are flushed (fsync) to stable storage.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: What causes "Transaction ID Wraparound"?

  ANSWER:
    Transaction IDs (XIDs) are 32-bit integers (~4 billion limit). When it wraps around to 0, past transactions would appear to be in the future (invisible). Postgres uses a "frozen" XID concept and aggressive vacuuming to prevent this. If a DB approaches wraparound, it will shut down to prevent data loss.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: What is the purpose of the Checkpointer process?

  ANSWER:
    To write dirty pages from memory to disk. This bounds the amount of time crash recovery takes. Without checkpoints, a crash would require replaying the WAL from the beginning of time.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q7: If work_mem is exceeded during a sort, what happens?

  ANSWER:
    Postgres spills the sort operation to disk (temporary files), which drastically slows down query execution.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q8: Can a transaction see a row inserted by an uncommitted transaction?

  ANSWER:
    No, due to the Isolation property. Postgres checks the active snapshot; if the xmin belongs to an uncommitted transaction (unless it's the current transaction), the row is invisible.

────────────────────────────────────────────────────────────────────────────────
  8. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: The Bloating Table

  Scenario: A table receives 1000 UPDATE queries a second. autovacuum is turned on, but the table size on disk keeps growing indefinitely.

  SOLUTION:
    Problem: There might be a long-running transaction (e.g., an analyst ran a SELECT query that's taking 5 hours) or an abandoned replication slot. Because that old transaction might need to see the old data, VACUUM cannot remove any dead tuples created after that transaction started.
    Answer: Monitor pg_stat_activity for long-running transactions and terminate them. Configure idle_in_transaction_session_timeout.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 2: Slow Commits

  Scenario: An application inserts 1,000,000 rows in a loop: for i in 1..1M: execute("INSERT...")

  SOLUTION:
    Problem: Each individual insert runs in its own implicit transaction. This causes 1,000,000 synchronous fsync calls to the WAL file on disk, crushing I/O performance.
    Answer: Batch inserts using a single explicit transaction (BEGIN; ... COMMIT;), or use COPY, or multi-row INSERT VALUES (...), (...), (...).

────────────────────────────────────────────────────────────────────────────────
  9. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  AUTOVACUUM TUNING: The default autovacuum settings are too passive for massive, high-write tables. Production DBAs frequently tune autovacuum_vacuum_scale_factor to ensure tables are vacuumed frequently, preventing catastrophic bloat and table locks.
  DISK I/O SEPARATION: In high-throughput architectures, the WAL directory (pg_wal) is often placed on a completely separate physical SSD from the main data files to prevent sequential WAL writes from competing with random data file I/O.

────────────────────────────────────────────────────────────────────────────────
  10. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

  -> File 029: PostgreSQL_Indexing_QueryOpt (How MVCC impacts indexes (e.g., Index-Only Scans requiring the Visibility Map).)
  -> File 035: Transactions_Concurrency (Isolation levels and how Postgres implements Repeatable Read using MVCC snapshots.)

================================================================================
  END OF FILE 028
================================================================================
