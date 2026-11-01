================================================================================
  FILE 035: TRANSACTIONS & CONCURRENCY: PREVENTING DATA CHAOS
  Section: C - DBMS & Databases
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  This document explores how databases handle multiple clients trying to read and write the exact same data at the exact same time. Without concurrency control, race conditions would cause incorrect bank balances and double-booked seats. You will learn about Isolation Levels, Locking mechanisms, Deadlocks, and Distributed Transactions (2PC, Saga).

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  TRANSACTION
    A logical unit of work encompassing one or more SQL statements (BEGIN to COMMIT/ROLLBACK).

  ISOLATION LEVEL
    Defines how strictly a transaction is isolated from the effects of concurrent transactions.

  LOCKING
    - Shared Lock (S): Allows concurrent readers, blocks writers.
    - Exclusive Lock (X): Blocks both readers and writers.

  PESSIMISTIC CONCURRENCY
    Locking rows preemptively because you assume conflicts will happen.

  OPTIMISTIC CONCURRENCY
    Proceeding without locks, checking for conflicts at commit time (via version numbers).

  DEADLOCK
    Two transactions wait for locks held by each other, causing an infinite standoff.

  DISTRIBUTED TRANSACTION
    A transaction spanning multiple microservices or database shards.

  TWO-PHASE COMMIT (2PC)
    A distributed algorithm to commit transactions across multiple nodes.

  SAGA PATTERN
    A distributed transaction pattern using compensating transactions (callbacks to undo work) instead of locking.

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  ISOLATION LEVEL PHENOMENA MATRIX                                       │
  │                                                                         │
  │  | Isolation Level | Dirty Read | Non-Repeatable Read | Phantom Read |  │
  │  | :--- | :--- | :--- | :--- |                                          │
  │  | Read Uncommitted| Possible | Possible | Possible |                   │
  │  | Read Committed | Prevented | Possible | Possible |                   │
  │  | Repeatable Read | Prevented | Prevented | Possible* |                │
  │  | Serializable | Prevented | Prevented | Prevented |                   │
  │  *(Note: PostgreSQL prevents Phantom Reads in Repeatable Read using MVCC)│
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘
  - Dirty Read: Reading uncommitted data from another transaction.
  - Non-Repeatable Read: Re-reading a row in the same transaction yields a different result because another transaction updated it.
  - Phantom Read: Re-running a query returning multiple rows yields new rows because another transaction inserted data matching the WHERE clause.

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  DEADLOCK SCENARIO                                                      │
  │                                                                         │
  │  Transaction A                 Transaction B                            │
  │  -------------                 -------------                            │
  │  1. UPDATE Account 1           1. UPDATE Account 2                      │
  │     (Acquires Lock on 1)          (Acquires Lock on 2)                  │
  │  2. UPDATE Account 2           2. UPDATE Account 1                      │
  │     (Waits for B's Lock)          (Waits for A's Lock)                  │
  │                                                                         │
  │            💥 DEADLOCK DETECTED (DB kills one Tx) 💥                    │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  4. EXPLANATION & THEORY
────────────────────────────────────────────────────────────────────────────────

  PRODUCTION CONCEPT: DISTRIBUTED TRANSACTIONS (SAGA)
  When an order spans an Order Service and a Payment Service, you cannot use standard SQL COMMIT.
  The Choreography Saga Flow:
  1. Order Service: Creates Order (Status: PENDING), emits OrderCreated event to Kafka.
  2. Payment Service: Listens to event, attempts charge.
     - If Success: Emits PaymentSucceeded. Order Service updates status to CONFIRMED.
     - If Failure: Emits PaymentFailed. Order Service executes Compensating Transaction (cancels order).

────────────────────────────────────────────────────────────────────────────────
  5. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: SQL]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // SQL: Testing Read Committed vs Repeatable Read                       │
  │                                                                          │
  │  -- Transaction 1 (T1)                                                   │
  │  BEGIN ISOLATION LEVEL READ COMMITTED;                                   │
  │  SELECT balance FROM accounts WHERE id = 1; -- Returns 100               │
  │                                                                          │
  │  -- Transaction 2 (T2) (Runs concurrently)                               │
  │  BEGIN;                                                                  │
  │  UPDATE accounts SET balance = 50 WHERE id = 1;                          │
  │  COMMIT;                                                                 │
  │                                                                          │
  │  -- Transaction 1 (T1) continues                                         │
  │  SELECT balance FROM accounts WHERE id = 1; -- Returns 50! (Non-repeatable read)│
  │  COMMIT;                                                                 │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

  [Language: SQL]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // SQL: Pessimistic Locking (SELECT FOR UPDATE)                         │
  │                                                                          │
  │  BEGIN;                                                                  │
  │  -- Acquires an Exclusive Lock on the row. Other transactions attempting │
  │  -- to SELECT FOR UPDATE this row will block until we COMMIT.            │
  │  SELECT balance FROM accounts WHERE id = 1 FOR UPDATE;                   │
  │                                                                          │
  │  -- Application checks balance >= 50, then issues update                 │
  │  UPDATE accounts SET balance = balance - 50 WHERE id = 1;                │
  │  COMMIT;                                                                 │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘
  Used to prevent race conditions during "Read-Modify-Write" cycles.

  [Language: JAVASCRIPT]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Application Code: Optimistic Locking                                 │
  │                                                                          │
  │  // Adding a `version` column to the table. No DB locks required.        │
  │  async function updateProductPrice(id, newPrice) {                       │
  │    // 1. Read data and current version                                   │
  │    const product = await db.query('SELECT price, version FROM products WHERE id = $1', [id]);│
  │                                                                          │
  │    // 2. Attempt update, but ONLY if version hasn't changed              │
  │    const result = await db.query(                                        │
  │      'UPDATE products SET price = $1, version = version + 1 WHERE id = $2 AND version = $3',│
  │      [newPrice, id, product.version]                                     │
  │    );                                                                    │
  │                                                                          │
  │    if (result.rowCount === 0) {                                          │
  │      throw new Error("Concurrency conflict! Someone else updated this product.");│
  │    }                                                                     │
  │  }                                                                       │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  7. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: How do you prevent a Double-Spending problem?

  ANSWER:
    Using pessimistic locking (SELECT FOR UPDATE), or optimistic concurrency control (versioning), or atomic DB operations (UPDATE ... SET balance = balance - 10 WHERE balance >= 10).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: What is a Deadlock and how does the Database handle it?

  ANSWER:
    When two transactions are mutually waiting on each other's locks. The database periodically runs a deadlock detector graph. When a cycle is found, it aborts (rolls back) one of the transactions and throws an error, unblocking the other.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: Explain Two-Phase Commit (2PC).

  ANSWER:
    A distributed transaction protocol. Phase 1 (Prepare): The Coordinator asks all nodes if they are ready to commit. Phase 2 (Commit): If ALL nodes vote yes, the Coordinator tells them to Commit. If ANY vote no, it tells them to Rollback. It is highly consistent but slow and prone to blocking if the Coordinator crashes.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: What is the difference between Repeatable Read and Serializable?

  ANSWER:
    Serializable strictly guarantees that the outcome of concurrent transactions is exactly the same as if they were executed serially (one after the other). Repeatable Read allows Phantom Reads (though Postgres protects against this, it still allows "Serialization Anomalies" like Write Skew).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: How do you avoid Deadlocks in application code?

  ANSWER:
    By ensuring all transactions acquire locks in the exact same order. If Tx A and Tx B always lock Account 1 before Account 2, a deadlock cannot occur.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: What is Write Skew?

  ANSWER:
    A concurrency anomaly under Repeatable Read. Example: Two on-call doctors check if anyone is on call (SELECT COUNT(*)). Both see the count is 2. Both decide to take time off and update their own status (UPDATE ...). Result: 0 doctors on call. Serializable prevents this.

────────────────────────────────────────────────────────────────────────────────
  8. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: The Race Condition

  // Node.js Checkout Logic
  const seat = await db.query('SELECT status FROM seats WHERE id = 42');
  if (seat.status === 'AVAILABLE') {
      // What happens if two users execute the above line at the exact same millisecond?
      await db.query("UPDATE seats SET status = 'SOLD', user = 'Alice' WHERE id = 42");
  }

  SOLUTION:
    Problem: Classic race condition. Both read 'AVAILABLE', both write 'SOLD'. The last write wins, overwriting the first.
    Answer: Use SELECT status FROM seats ... FOR UPDATE (Pessimistic), OR include the status check in the update: UPDATE seats ... WHERE id = 42 AND status = 'AVAILABLE'.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 2: The Long Transaction

  await db.query('BEGIN');
  await db.query('SELECT * FROM users FOR UPDATE');
  // Application makes a 10-second external API call to Stripe
  await stripe.charge(user.stripe_id); 
  await db.query('COMMIT');

  SOLUTION:
    Problem: Holding an Exclusive Lock while waiting for external I/O (Stripe API) will halt all other database traffic attempting to read/write the users table.
    Answer: Never hold DB locks during external API calls. Move the API call outside the transaction, or use a Saga pattern (mark status as processing_payment, then update later).

────────────────────────────────────────────────────────────────────────────────
  9. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  FINANCIAL INTEGRITY: If you build a Fintech app without understanding Isolation Levels, money will be created or destroyed via race conditions.
  PERFORMANCE VS SAFETY TRADEOFF: Setting everything to Serializable ensures data safety but destroys throughput via locking and retries. Engineers must choose the lowest acceptable isolation level (usually Read Committed) and explicitly handle critical sections with row locks.

────────────────────────────────────────────────────────────────────────────────
  10. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

  -> File 028: PostgreSQL_MVCC_WAL (How Postgres achieves Isolation without heavy locking.)
  -> File 034: Database_Scaling (Why distributed transactions are required when scaling out.)

================================================================================
  END OF FILE 035
================================================================================
