================================================================================
  FILE 032: REDIS: IN-MEMORY DATA STRUCTURE STORE
  Section: C - DBMS & Databases
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  This document covers Redis (Remote Dictionary Server), the industry standard for caching, session management, and real-time messaging. You will learn about its single-threaded architecture, versatile data structures, persistence mechanisms, and high-availability setups (Redis Sentinel and Cluster). Prerequisites include understanding basic key-value concepts and memory limitations.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  IN-MEMORY
    All data resides in RAM, providing sub-millisecond read/write latency.

  SINGLE-THREADED EVENT LOOP
    Redis executes commands sequentially on a single thread using I/O multiplexing. This guarantees atomicity for single commands without locks.

  DATA STRUCTURES
    Redis is not just a Key-Value store; it supports Strings, Lists, Sets, Sorted Sets (ZSet), Hashes, Bitmaps, and Streams.

  TTL (TIME TO LIVE)
    The lifespan of a key before it is automatically deleted.

  EVICTION POLICY
    Rules defining how Redis removes old data when RAM is full (e.g., LRU, LFU).

  RDB (REDIS DATABASE BACKUP)
    Point-in-time snapshot persistence.

  AOF (APPEND ONLY FILE)
    Transaction log persistence.

  PUB/SUB
    Publish/Subscribe messaging paradigm.

  LUA SCRIPTING
    Executing custom scripts atomically inside the Redis server.

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  CACHE-ASIDE (LAZY LOADING) PATTERN                                     │
  │                                                                         │
  │  [ Client/App ] ---> (1) Reads from Redis                               │
  │        |                                                                │
  │        +-----> [ Redis (Cache Miss) ]                                   │
  │        |                                                                │
  │        +---> (2) Reads from Primary DB (PostgreSQL)                     │
  │                    |                                                    │
  │                    v                                                    │
  │              (3) Writes data to Redis                                   │
  │              (4) Returns data to user                                   │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  REDIS CLUSTER HASH SLOTS                                               │
  │                                                                         │
  │  Key: "user:123" --> CRC16("user:123") % 16384 = Slot 4567              │
  │                                                                         │
  │  [ Node A ]          [ Node B ]          [ Node C ]                     │
  │  Slots 0 - 5460      Slots 5461 - 10922  Slots 10923 - 16383            │
  │  (Master + Replica)  (Master + Replica)  (Master + Replica)             │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: BASH]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Data Structures                                                      │
  │                                                                          │
  │  # Strings (Caching, Counters)                                           │
  │  SET user:100:name "Alice" EX 3600  # Expires in 1 hour                  │
  │  INCR page:views                    # Atomic increment                   │
  │                                                                          │
  │  # Hashes (Storing Objects)                                              │
  │  HSET user:101 name "Bob" age "30" role "admin"                          │
  │  HGETALL user:101                                                        │
  │                                                                          │
  │  # Lists (Queues, Recent Items)                                          │
  │  LPUSH queue:jobs "job1" "job2"                                          │
  │  RPOP queue:jobs                    # Returns "job1"                     │
  │                                                                          │
  │  # Sets (Unique Items, Intersections)                                    │
  │  SADD user:1:friends "Alice" "Bob"                                       │
  │  SADD user:2:friends "Bob" "Charlie"                                     │
  │  SINTER user:1:friends user:2:friends # Returns "Bob"                    │
  │                                                                          │
  │  # Sorted Sets (Leaderboards, Rate Limiters)                             │
  │  ZADD leaderboard 1500 "Alice" 2000 "Bob"                                │
  │  ZREVRANGE leaderboard 0 10 WITHSCORES # Top 10 descending               │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: JAVASCRIPT]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Redis with ioredis (Node.js)                                         │
  │                                                                          │
  │  const Redis = require('ioredis');                                       │
  │  const redis = new Redis({ host: 'localhost', port: 6379 });             │
  │                                                                          │
  │  async function getUserProfile(userId, db) {                             │
  │    const cacheKey = `user:${userId}:profile`;                            │
  │                                                                          │
  │    // 1. Check Cache                                                     │
  │    const cachedData = await redis.get(cacheKey);                         │
  │    if (cachedData) {                                                     │
  │      return JSON.parse(cachedData);                                      │
  │    }                                                                     │
  │                                                                          │
  │    // 2. Cache Miss -> Fetch from DB                                     │
  │    const dbData = await db.query('SELECT * FROM users WHERE id = ?', [userId]);│
  │                                                                          │
  │    if (dbData) {                                                         │
  │      // 3. Set Cache with TTL (e.g., 1 hour)                             │
  │      await redis.set(cacheKey, JSON.stringify(dbData), 'EX', 3600);      │
  │    }                                                                     │
  │                                                                          │
  │    return dbData;                                                        │
  │  }                                                                       │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

  [Language: JAVASCRIPT]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Distributed Lock (Redlock Pattern)                                   │
  │                                                                          │
  │  // Simplified lock via SET NX (Not eXists) PX (Milliseconds)            │
  │  async function acquireLock(lockName, timeout) {                         │
  │    const identifier = crypto.randomUUID();                               │
  │    const result = await redis.set(lockName, identifier, 'NX', 'PX', timeout);│
  │    return result === 'OK' ? identifier : false;                          │
  │  }                                                                       │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘
  Ensures only one process can execute a critical section (e.g., charging a credit card).

────────────────────────────────────────────────────────────────────────────────
  7. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: If Redis is single-threaded, how is it so fast?

  ANSWER:
    It is heavily optimized C code executing entirely in RAM. Network I/O is handled via epoll/kqueue (I/O multiplexing). Because it's single-threaded, it avoids context switching and locking overhead. (Note: Modern Redis uses threads for background I/O tasks, but command execution remains single-threaded).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: What happens when Redis runs out of memory?

  ANSWER:
    It depends on the maxmemory-policy. Defaults to noeviction (errors on new writes). Common production policy is allkeys-lru (evicts least recently used keys) or volatile-lru (evicts only keys with an expiration set).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: Explain the difference between RDB and AOF.

  ANSWER:
    RDB creates a compressed binary snapshot of memory at intervals (fast recovery, but data since last snapshot is lost). AOF logs every write command to disk (slower, larger file, but highly durable). Production often uses both.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: How do you prevent a Cache Stampede (Thundering Herd)?

  ANSWER:
    When a heavily requested cache key expires, thousands of requests hit the DB simultaneously. Prevent by: 1) Using a distributed lock (only one thread fetches from DB, others wait), 2) "Probabilistic early expiration" (refresh cache before it fully expires).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: What is a Redis transaction?

  ANSWER:
    Using MULTI, commands are queued. On EXEC, all commands run sequentially. If you need conditional logic, you use WATCH (optimistic locking) or execute a Lua script for strict atomicity.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: What is the maximum size of a Redis value?

  ANSWER:
    512 MB.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q7: What are Sorted Sets often used for?

  ANSWER:
    Leaderboards (sorting players by score), priority queues, and sliding-window rate limiters (using timestamp as score).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q8: How does Redis Cluster achieve high availability?

  ANSWER:
    By dividing the keyspace into 16,384 hash slots distributed across multiple master nodes. Each master has replicas. If a master fails, the cluster gossips and promotes its replica automatically.

────────────────────────────────────────────────────────────────────────────────
  8. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: The Blocking Command

  Scenario: Users complain the entire application hangs for 2 seconds randomly.
  # Admin runs this to find user keys
  KEYS user:* 

  SOLUTION:
    Problem: KEYS is a blocking command that iterates over the entire O(N) keyspace. On a single-threaded server with 10 million keys, this freezes the server, blocking all other application commands.
    Answer: Never use KEYS in production. Use the SCAN command, which returns an iterator cursor and processes a small batch of keys at a time.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 2: The Multi-Key Cluster Error

  MGET user:100:profile user:200:profile

  SOLUTION:
    Problem: In a Redis Cluster, MGET (Multi-Get) will fail if the keys hash to different slots on different nodes.
    Answer: Use Hash Tags. If you name keys {user}:100:profile and {user}:200:profile, the cluster hashes only the substring inside {} ensuring they land on the same node.

────────────────────────────────────────────────────────────────────────────────
  9. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  DATABASE SHIELDING: Almost every massive scale application (Twitter, Netflix, Discord) uses Redis to protect primary databases. Without Redis, the primary DB would melt under read loads.
  SESSION STATE: In a stateless microservice architecture, HTTP requests can hit any backend server. Storing session tokens in Redis allows any server to instantly validate a session.

────────────────────────────────────────────────────────────────────────────────
  10. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

  -> File 034: Database_Scaling (Caching as a scaling strategy.)
  -> File 033: Database_Comparison (Redis vs Memcached.)

================================================================================
  END OF FILE 032
================================================================================
