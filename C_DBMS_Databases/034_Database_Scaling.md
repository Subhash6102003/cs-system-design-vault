================================================================================
  FILE 034: DATABASE SCALING: FROM ONE NODE TO A GLOBAL CLUSTER
  Section: C - DBMS & Databases
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  This document covers the strategies required to handle increased data volume and request throughput. Scaling the application tier is easy (stateless containers); scaling the stateful database tier is the hardest problem in backend engineering. You will learn about Vertical vs Horizontal scaling, Read Replicas, Sharding, Consistent Hashing, and Connection Pooling.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  VERTICAL SCALING (SCALING UP)
    Buying a bigger server (more CPU, RAM, faster SSDs). Limited by hardware constraints.

  HORIZONTAL SCALING (SCALING OUT)
    Adding more servers to a cluster. Theoretically infinite.

  READ REPLICA
    A read-only copy of the primary database. Scaled horizontally to handle high read traffic.

  REPLICATION LAG
    The delay between a write hitting the primary and becoming visible on the read replica.

  SHARDING
    Partitioning a database across multiple machines. Each machine holds a subset of the data.

  CONSISTENT HASHING
    An algorithm used in sharding/caching to minimize data movement when nodes are added or removed.

  CQRS (COMMAND QUERY RESPONSIBILITY SEGREGATION)
    An architectural pattern separating the write model (commands) from the read model (queries).

  DATABASE PROXY
    A middle layer (like ProxySQL or RDS Proxy) that routes queries, pools connections, and handles failovers transparently.

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  READ REPLICA TOPOLOGY (MASTER-SLAVE)                                   │
  │                                                                         │
  │             [ App Layer (Writes & Reads) ]                              │
  │                   |              \ (Reads Only)                         │
  │                (Writes)           \                                     │
  │                   v                v                                    │
  │            [ PRIMARY DB ]    [ Proxy/Load Balancer ]                    │
  │                   |              /         \                            │
  │            (WAL Streaming)      v           v                           │
  │                   |      [ Replica 1 ] [ Replica 2 ]                    │
  │                   v                                                     │
  │              [ Replica 3 ]                                              │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  CONSISTENT HASHING RING                                                │
  │                                                                         │
  │  When standard hashing (Key % N) is used, adding a node changes the hash for ALL keys.│
  │  Consistent hashing maps Nodes and Keys to a circular ring (0 to 2^32-1).│
  │                                                                         │
  │          [Node A] 0                                                     │
  │         /          \                                                    │
  │    (Key 1)       (Key 2)                                                │
  │       /              \                                                  │
  │  [Node D]          [Node B]                                             │
  │       \              /                                                  │
  │    (Key 4)       (Key 3)                                                │
  │         \          /                                                    │
  │          [Node C]                                                       │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘
  Keys are assigned to the first Node encountered moving clockwise. Adding Node E only redistributes keys between D and E.

────────────────────────────────────────────────────────────────────────────────
  6. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: JAVASCRIPT]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Read/Write Split Logic (Node.js)                                     │
  │                                                                          │
  │  // Simplistic implementation of connection routing                      │
  │  const { Pool } = require('pg');                                         │
  │                                                                          │
  │  const writePool = new Pool({ host: 'primary.db.internal' });            │
  │  const readPool = new Pool({ host: 'ro-replica.db.internal' });          │
  │                                                                          │
  │  async function executeQuery(query, params, isWrite = false) {           │
  │    const pool = isWrite ? writePool : readPool;                          │
  │                                                                          │
  │    try {                                                                 │
  │      return await pool.query(query, params);                             │
  │    } catch (error) {                                                     │
  │      // Fallback logic could go here                                     │
  │      throw error;                                                        │
  │    }                                                                     │
  │  }                                                                       │
  │                                                                          │
  │  // Usage                                                                │
  │  await executeQuery('INSERT INTO users(name) VALUES ($1)', ['Alice'], true);│
  │  await executeQuery('SELECT * FROM users WHERE name = $1', ['Alice'], false);│
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

  [Language: JAVASCRIPT]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Consistent Hashing Implementation Snippet                            │
  │                                                                          │
  │  const crypto = require('crypto');                                       │
  │                                                                          │
  │  class ConsistentHash {                                                  │
  │    constructor() {                                                       │
  │      this.ring = new Map(); // Hash -> Node                              │
  │      this.sortedHashes = [];                                             │
  │    }                                                                     │
  │                                                                          │
  │    hash(key) {                                                           │
  │      return parseInt(crypto.createHash('md5').update(key).digest('hex').slice(0,8), 16);│
  │    }                                                                     │
  │                                                                          │
  │    addNode(node) {                                                       │
  │      // Add multiple virtual nodes for better distribution               │
  │      for (let i = 0; i < 3; i++) {                                       │
  │        const h = this.hash(node + i);                                    │
  │        this.ring.set(h, node);                                           │
  │        this.sortedHashes.push(h);                                        │
  │      }                                                                   │
  │      this.sortedHashes.sort((a, b) => a - b);                            │
  │    }                                                                     │
  │                                                                          │
  │    getNode(key) {                                                        │
  │      const h = this.hash(key);                                           │
  │      for (const nodeHash of this.sortedHashes) {                         │
  │        if (h <= nodeHash) return this.ring.get(nodeHash);                │
  │      }                                                                   │
  │      return this.ring.get(this.sortedHashes[0]); // Wrap around          │
  │    }                                                                     │
  │  }                                                                       │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  7. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: What is the difference between Vertical and Horizontal scaling?

  ANSWER:
    Vertical is adding resources (RAM/CPU) to a single machine; it's easy, requires no code changes, but has a hard physical limit. Horizontal is adding more machines; it provides infinite scale but introduces distributed system complexities (sharding, distributed transactions, lag).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: How do you handle Replication Lag in a Read Replica setup?

  ANSWER:
    If a user updates their profile and instantly refreshes, the read might hit a lagging replica and show old data. Solutions: 1) App logic forces reads from the Primary for X seconds after a write. 2) "Read-Your-Writes" consistency mechanisms. 3) Use synchronous replication (hurts write performance).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: Explain the Sharding strategies.

  ANSWER:
    1) Hash-based: Hash the shard key to pick a node (even distribution, but range queries are impossible). 2) Range-based: Shard by ranges (e.g., A-M on Node 1, N-Z on Node 2). Good for ranges, but can cause hotspots. 3) Directory-based: A lookup table points to the exact shard.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: What is the "Celebrity Problem" in Sharding?

  ANSWER:
    A hotspot issue. If data is sharded by UserID, and Justin Bieber (massive traffic) is on Shard 3, Shard 3 will be overwhelmed while others are idle. Mitigated by splitting heavily accessed entities, or adding random suffix hashing.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: Why do microservices require their own databases?

  ANSWER:
    To ensure loose coupling. If multiple services share a DB, a schema change by Team A will break Team B. It also prevents one high-traffic service from starving the DB resources of other services.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: What is CQRS?

  ANSWER:
    Command Query Responsibility Segregation. Using fundamentally different data models (and often entirely different databases) for reading and writing data. e.g., Writing to PostgreSQL, which emits events to Kafka, which populates Elasticsearch for fast querying.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q7: What is Connection Pooling and why is it mandatory at scale?

  ANSWER:
    Opening a TCP connection to a DB is slow and memory-intensive. A pooler maintains a set of long-lived connections. When an app needs to query, it borrows a connection and returns it. Prevents the DB from being crushed by thousands of concurrent connections.

────────────────────────────────────────────────────────────────────────────────
  8. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: Cross-Shard Joins

  Scenario: You sharded your database by user_id. Shard A holds Users 1-500. Shard B holds Users 501-1000. You need to write a query: "Get the most active users across the platform."

  SOLUTION:
    Problem: You cannot perform a SQL ORDER BY LIMIT across physical databases.
    Answer: Scatter-Gather query. An application-level router queries both shards for their top users, aggregates the results in memory, sorts them, and returns the top subset. (Alternatively, maintain a global leaderboard in Redis).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 2: The Load Balancer Trap

  Scenario: You put a standard AWS ALB (Application Load Balancer) in front of 3 PostgreSQL read replicas.

  SOLUTION:
    Problem: Database connections (TCP/TCP-Keepalive) are long-lived. ALBs are Layer 7 HTTP load balancers. You need a Layer 4 (Network) load balancer, or better, a database-aware proxy (like ProxySQL or PgBouncer) that understands SQL protocols.

────────────────────────────────────────────────────────────────────────────────
  9. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  LIMITS OF THE CLOUD: Even the largest AWS RDS instance tops out at a certain IOPS (Input/Output Operations Per Second) limit. Sharding is the only way companies like Discord and Instagram survive.
  DISASTER RECOVERY: Replication isn't just for scaling reads; it's the foundation of High Availability (HA). If the primary data center catches fire, traffic is rerouted to replicas in another region.

────────────────────────────────────────────────────────────────────────────────
  10. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

  -> File 035: Transactions_Concurrency (How Distributed Transactions (2PC) work across shards.)
  -> File 030: PostgreSQL_Advanced (Postgres Partitioning (Sharding within a single node).)

================================================================================
  END OF FILE 034
================================================================================
