================================================================================
  FILE 089: SYSTEM DESIGN FUNDAMENTALS
  Section: H - System Design at Scale
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  System Design Fundamentals covers the foundational concepts required to architect scalable, highly available, and reliable distributed systems. Prerequisites include basic understanding of client-server architecture and databases. You will learn about scalability, availability, the CAP theorem, consistency models, and how to perform back-of-the-envelope estimations for large-scale systems.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  SCALABILITY
    The capability of a system to handle a growing amount of work.
    - Horizontal Scaling (Scale Out): Adding more machines to a system's resource pool.
    - Vertical Scaling (Scale Up): Adding more power (CPU, RAM) to an existing machine.

  AVAILABILITY
    The percentage of time a system is operational. Often measured in "nines" (e.g., 99.9% = 8.76 hrs downtime/year). Defined in SLAs (Service Level Agreements).

  RELIABILITY
    The probability a system will perform its intended function without failure.

  LATENCY VS THROUGHPUT
    Latency is the time to perform an action (e.g., 50ms). Throughput is the number of actions executed per unit of time (e.g., 1000 QPS).

  CAP THEOREM
    A distributed data store can only guarantee two of three: Consistency (every read receives the most recent write), Availability (every request receives a non-error response), Partition Tolerance (system continues to operate despite network partitions).

  CONSISTENCY MODELS
    - Strong: After a write completes, any subsequent read will return the updated value.
    - Eventual: Given enough time, all updates will propagate through the system.
    - Causal: Operations that are causally related are seen by every node in the same order.
    - Read-Your-Writes: A user will always see their own updates immediately.

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  CAP THEOREM REAL-WORLD DATABASES                                       │
  │                                                                         │
  │                  +-------------------------+                            │
  │                  |       CONSISTENCY       |                            │
  │                  |                         |                            │
  │                  |       (RDBMS, Spanner)  |                            │
  │                  +-----------+-------------+                            │
  │                             / \                                         │
  │                            /   \                                        │
  │                           /     \                                       │
  │                          /       \                                      │
  │    +--------------------+         +--------------------+                │
  │    |                    |         |                    |                │
  │    |    AVAILABILITY    |---------| PARTITION TOLERANCE|                │
  │    |                    | (Cassandra,                  |                │
  │    |  (DynamoDB)        |  Riak)                       |                │
  │    +--------------------+         +--------------------+                │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  SYSTEM DESIGN INTERVIEW FRAMEWORK                                      │
  │                                                                         │
  │  [1. Requirements Clarification] -> [2. Back-of-the-Envelope] -> [3. High-Level Design] -> [4. Deep Dive] -> [5. Wrap Up]│
  │  (Features, Scale, Constraints)     (QPS, Storage, Bandwidth)    (Components, APIs)        (Bottlenecks,   (Trade-offs)│
  │                                                                                            DB Schema)      │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  4. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: python]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Simple QPS and Storage Estimator                                     │
  │                                                                          │
  │  def estimate_system(daily_active_users, requests_per_user, bytes_per_request):│
  │      """                                                                 │
  │      Demonstrates basic back-of-the-envelope calculations.               │
  │      """                                                                 │
  │      total_requests_per_day = daily_active_users * requests_per_user     │
  │      # 1 day = 86400 seconds                                             │
  │      qps = total_requests_per_day // 86400                               │
  │                                                                          │
  │      daily_storage_bytes = total_requests_per_day * bytes_per_request    │
  │      daily_storage_gb = daily_storage_bytes / (1024**3)                  │
  │      yearly_storage_tb = (daily_storage_gb * 365) / 1024                 │
  │                                                                          │
  │      return qps, yearly_storage_tb                                       │
  │                                                                          │
  │  # Example: 10M DAU, 5 requests/day, 100KB per request                   │
  │  qps, storage = estimate_system(10_000_000, 5, 100_000)                  │
  │  print(f"QPS: {qps}") # ~578 QPS                                         │
  │  print(f"Storage/Year: {storage:.2f} TB") # ~1.70 TB                     │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: python]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │                                                                          │
  │  import time                                                             │
  │  from typing import Optional, Dict                                       │
  │                                                                          │
  │  class EventualConsistencyCache:                                         │
  │      """                                                                 │
  │      Production simulation of an eventually consistent local cache         │
  │      that syncs with a primary datastore asynchronously.                 │
  │      """                                                                 │
  │      def __init__(self, sync_interval_seconds: int = 5):                 │
  │          self.local_cache: Dict[str, str] = {}                           │
  │          self.primary_store: Dict[str, str] = {}                         │
  │          self.last_sync_time: float = time.time()                        │
  │          self.sync_interval = sync_interval_seconds                      │
  │                                                                          │
  │      def write(self, key: str, value: str) -> None:                      │
  │          # Write directly to primary store (simulating network write)    │
  │          self.primary_store[key] = value                                 │
  │                                                                          │
  │      def read(self, key: str) -> Optional[str]:                          │
  │          # Check if we need to sync based on eventual consistency SLA    │
  │          current_time = time.time()                                      │
  │          if current_time - self.last_sync_time > self.sync_interval:     │
  │              self._sync_cache()                                          │
  │                                                                          │
  │          return self.local_cache.get(key)                                │
  │                                                                          │
  │      def _sync_cache(self) -> None:                                      │
  │          """Background job to pull updates."""                           │
  │          print("[Sync] Pulling updates from primary datastore...")       │
  │          self.local_cache.update(self.primary_store)                     │
  │          self.last_sync_time = time.time()                               │
  │                                                                          │
  │  # Usage                                                                 │
  │  db = EventualConsistencyCache(sync_interval_seconds=2)                  │
  │  db.write("user:1", "Alice")                                             │
  │  print("Immediate Read (Stale):", db.read("user:1")) # None              │
  │  time.sleep(2.1)                                                         │
  │  print("Eventual Read (Fresh):", db.read("user:1")) # Alice              │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: Explain the difference between horizontal and vertical scaling.

  ANSWER:
    Vertical is adding CPU/RAM to one machine (limited ceiling, single point of failure). Horizontal is adding more machines (infinite ceiling, requires load balancing/distributed logic).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: How do you calculate QPS for a system with 50M DAU making 10 requests per day?

  ANSWER:
    50M * 10 = 500M req/day. 500M / 86400 seconds ≈ 5800 QPS.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: What is the CAP theorem and why can't we have all three?

  ANSWER:
    In a distributed system, network partitions (P) are unavoidable. When P happens, you must choose between C (cancel the request to maintain consistency) or A (serve the stale request to maintain availability).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: What is Read-Your-Writes consistency?

  ANSWER:
    A guarantee that once a client updates a record, they will immediately see the updated value on subsequent reads, even if other clients see eventual consistency.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: How does 99.99% availability translate to downtime?

  ANSWER:
    99.99% = 4 nines. Total minutes in year = 525,600. 0.01% of that is ~52.5 minutes of downtime per year.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: What is the difference between latency and throughput?

  ANSWER:
    Latency is the time taken for a single request. Throughput is the volume of requests processed over time.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q7: When would you choose CP over AP in a database?

  ANSWER:
    Financial transactions, billing systems, or any domain where reading stale data has catastrophic consequences.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q8: What is an SLA versus an SLO?

  ANSWER:
    SLA is the external agreement with clients (e.g., penalties if missed). SLO is the internal objective (often stricter than the SLA) used by engineering teams.

────────────────────────────────────────────────────────────────────────────────
  7. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: Riddle 1

  def process_data(data_stream):
      # Process synchronously
      for item in data_stream:
          db.save(item) # takes 100ms

  SOLUTION:
    Problem: 
    Fix: This system scales poorly. A stream of 1000 items takes 100 seconds (low throughput). It needs batching or asynchronous processing.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 2: Riddle 2

  "I promise to always be there when you call, but I might occasionally lie to you about the past. What am I?"

  SOLUTION:
    Problem: 
    Fix: An AP (Available & Partition Tolerant) system utilizing Eventual Consistency.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 3: Riddle 3

  def get_user_balance(user_id):
      cache_val = redis.get(user_id)
      if cache_val: return cache_val
      val = sql.query("SELECT balance FROM users WHERE id=?", user_id)
      redis.set(user_id, val)
      return val

  SOLUTION:
    Problem: 
    Fix: This is subject to stale reads if the SQL DB updates but Redis isn't invalidated. Financial balances should generally avoid caching or use strict write-through/invalidation mechanisms.

────────────────────────────────────────────────────────────────────────────────
  8. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  Understanding CAP theorem and consistency prevents catastrophic data loss or corruption during network partitions. Back-of-the-envelope estimation dictates whether you should provision a single PostgreSQL instance or a 100-node Cassandra cluster, saving millions of dollars in infrastructure costs and preventing scaling bottlenecks.

────────────────────────────────────────────────────────────────────────────────
  9. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

  -> File 090: Load Balancing, CDN, & API Gateway (How to scale horizontally)
  -> File 091: Caching at Scale (Techniques for reducing latency)
  -> File 096: Distributed Systems (Deep dive into Paxos, Raft, and Vector Clocks)

================================================================================
  END OF FILE 089
================================================================================
