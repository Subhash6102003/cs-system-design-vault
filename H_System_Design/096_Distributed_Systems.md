================================================================================
  FILE 096: DISTRIBUTED SYSTEMS
  Section: H - System Design at Scale
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  Distributed Systems dives into the theoretical and practical challenges of coordinating multiple independent computers to act as a single system. Prerequisites include network programming and database internals. You will learn about consensus algorithms (Raft, Paxos), clock synchronization (Vector Clocks), distributed locks, and CRDTs.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  CONSENSUS
    The process of agreeing on a single data value among distributed processes. Hard due to network drops, crashes, and latency.

  BYZANTINE GENERALS PROBLEM
    A condition where nodes may fail arbitrarily (including malicious behavior).

  FLP IMPOSSIBILITY
    States that in an asynchronous network where even one node can crash, no deterministic consensus algorithm can guarantee completion.

  RAFT CONSENSUS
    An understandable algorithm for managing a replicated log. Uses Leader Election, Log Replication, and Safety.

  PAXOS
    The mathematically proven, but notoriously complex, predecessor to Raft.

  VECTOR CLOCKS
    A data structure for determining the partial ordering of events and detecting causality violations (concurrent writes).

  CRDTS (CONFLICT-FREE REPLICATED DATA TYPES)
    Data structures that can be replicated across a network and updated independently, merging without conflicts (e.g., G-Counter, OR-Set).

  IDEMPOTENCY
    A property where an operation applied multiple times yields the same result as applied once.

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  RAFT LEADER ELECTION                                                   │
  │                                                                         │
  │  [ Node A (Follower) ]  --Timeout-->  Becomes [ Candidate ]  --> Requests Votes│
  │                                                                |        │
  │      (Votes Yes) <---------------------------------------------+        │
  │   [ Node B (Follower) ]                                        |        │
  │                                                                v        │
  │   [ Node C (Follower) ] <--------------------------------- (Votes Yes)  │
  │                                                                         │
  │  Node A receives majority (2/3) -> Becomes [ LEADER ] -> Sends Heartbeats (AppendEntries)│
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  VECTOR CLOCK CONFLICT DETECTION                                        │
  │                                                                         │
  │  Node 1 updates -> V1: [A:1, B:0]                                       │
  │  Node 2 updates -> V2: [A:1, B:1] -> Causally later than V1 (No conflict)│
  │                                                                         │
  │  Node 1 offline updates -> V3: [A:2, B:0]                               │
  │  Node 2 offline updates -> V4: [A:1, B:1]                               │
  │  Merge Attempt! V3 and V4 are CONCURRENT (neither is strictly > the other). Conflict detected!│
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  4. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: python]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Simple Idempotency Key Middleware Concept                            │
  │                                                                          │
  │  redis_cache = {}                                                        │
  │                                                                          │
  │  def process_payment(idempotency_key: str, amount: int):                 │
  │      # 1. Check if we already processed this request                     │
  │      if idempotency_key in redis_cache:                                  │
  │          return redis_cache[idempotency_key] # Return cached successful response│
  │                                                                          │
  │      # 2. Process payment (simulated)                                    │
  │      result = {"status": "SUCCESS", "amount": amount, "tx_id": "12345"}  │
  │                                                                          │
  │      # 3. Store result to ensure idempotency                             │
  │      redis_cache[idempotency_key] = result                               │
  │                                                                          │
  │      return result                                                       │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: java]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │                                                                          │
  │  // Twitter Snowflake ID Generator                                       │
  │  // 64-bit ID: 1 bit sign, 41 bits timestamp, 10 bits machine id, 12 bits sequence│
  │  public class SnowflakeIdGenerator {                                     │
  │      private final long twepoch = 1288834974657L; // Custom Epoch        │
  │      private final long workerIdBits = 10L;                              │
  │      private final long maxWorkerId = -1L ^ (-1L << workerIdBits);       │
  │      private final long sequenceBits = 12L;                              │
  │                                                                          │
  │      private final long workerIdShift = sequenceBits;                    │
  │      private final long timestampLeftShift = sequenceBits + workerIdBits;│
  │      private final long sequenceMask = -1L ^ (-1L << sequenceBits);      │
  │                                                                          │
  │      private long workerId;                                              │
  │      private long sequence = 0L;                                         │
  │      private long lastTimestamp = -1L;                                   │
  │                                                                          │
  │      public SnowflakeIdGenerator(long workerId) {                        │
  │          if (workerId > maxWorkerId || workerId < 0) {                   │
  │              throw new IllegalArgumentException("Invalid worker ID");    │
  │          }                                                               │
  │          this.workerId = workerId;                                       │
  │      }                                                                   │
  │                                                                          │
  │      public synchronized long nextId() {                                 │
  │          long timestamp = System.currentTimeMillis();                    │
  │                                                                          │
  │          if (timestamp < lastTimestamp) {                                │
  │              throw new RuntimeException("Clock moved backwards");        │
  │          }                                                               │
  │                                                                          │
  │          if (lastTimestamp == timestamp) {                               │
  │              sequence = (sequence + 1) & sequenceMask;                   │
  │              if (sequence == 0) {                                        │
  │                  timestamp = waitNextMillis(lastTimestamp); // Wait for next ms│
  │              }                                                           │
  │          } else {                                                        │
  │              sequence = 0L;                                              │
  │          }                                                               │
  │                                                                          │
  │          lastTimestamp = timestamp;                                      │
  │                                                                          │
  │          return ((timestamp - twepoch) << timestampLeftShift) |          │
  │                 (workerId << workerIdShift) |                            │
  │                 sequence;                                                │
  │      }                                                                   │
  │                                                                          │
  │      private long waitNextMillis(long lastTimestamp) {                   │
  │          long timestamp = System.currentTimeMillis();                    │
  │          while (timestamp <= lastTimestamp) {                            │
  │              timestamp = System.currentTimeMillis();                     │
  │          }                                                               │
  │          return timestamp;                                               │
  │      }                                                                   │
  │  }                                                                       │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: Explain the Raft consensus algorithm.

  ANSWER:
    Nodes are Leaders, Followers, or Candidates. The Leader takes client writes and replicates logs to followers. If the Leader dies (heartbeat timeout), Followers become Candidates and request votes. Majority wins and becomes the new Leader.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: What is the Split-Brain problem?

  ANSWER:
    A network partition causes a cluster to split into two, and both halves elect a leader, leading to conflicting writes. Solved by requiring a strict quorum (N/2 + 1) for leader election.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: What is a Vector Clock?

  ANSWER:
    An array of counters (one per node). It detects concurrent modifications (conflicts) in distributed databases like DynamoDB, allowing the client to resolve the conflict via siblings.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: How does distributed locking work (e.g., Redlock)?

  ANSWER:
    Client acquires a lock on a majority of independent Redis nodes with a TTL. If acquired on majority within a small time window, lock is valid. Otherwise, it unlocks everything and retries.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: What is the difference between At-Least-Once, At-Most-Once, and Exactly-Once delivery?

  ANSWER:
    At-Least-Once: Retries until ACK (can duplicate). At-Most-Once: Fire and forget (can lose). Exactly-Once: Requires idempotency keys and two-phase commits (very hard/expensive).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: Why can't we just rely on NTP (Network Time Protocol) for ordering events?

  ANSWER:
    Physical clocks drift. A node's clock can skew backwards or leap forwards. NTP synchronization is not precise enough to guarantee the absolute ordering of two writes separated by milliseconds across the globe.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q7: What is a CRDT?

  ANSWER:
    A data structure (like a counter or set) mathematically designed so that concurrent updates can be merged in any order without conflicts. Used in collaborative editors (Figma, Google Docs) and Redis Enterprise.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q8: Explain the Twitter Snowflake format.

  ANSWER:
    A 64-bit integer: 41 bits for timestamp (gives ~69 years), 10 bits for worker ID (up to 1024 machines), and 12 bits for a sequence number (4096 IDs per ms per machine).

────────────────────────────────────────────────────────────────────────────────
  7. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: Riddle 1

  "I try to tell the exact time, but Einstein proved I can never be universally agreed upon. What am I?"

  SOLUTION:
    Problem: 
    Fix: The Physical Clock (Wall-clock time) in a distributed system.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 2: Riddle 2

  # Payment API
  def refund_user(user_id, amount):
      db.execute("UPDATE balances SET amount = amount + ?", amount)
      return "Refunded"

  SOLUTION:
    Problem: 
    Fix: Not idempotent. If the network drops the HTTP 200 OK, the client retries, and the user gets double refunded. It needs an idempotency key.

────────────────────────────────────────────────────────────────────────────────
  8. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  Without consensus (Raft/Zookeeper), a Kafka cluster doesn't know who the controller is. Without Snowflake IDs, distributed databases clash on primary keys. Without idempotency, payments process twice, causing massive financial loss and legal trouble.

────────────────────────────────────────────────────────────────────────────────
  9. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

  -> File 089: SystemDesign Fundamentals (CAP Theorem)
  -> File 092: Design Instagram (Usage of Snowflake IDs)

================================================================================
  END OF FILE 096
================================================================================
