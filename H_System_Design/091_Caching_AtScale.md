================================================================================
  FILE 091: CACHING AT SCALE
  Section: H - System Design at Scale
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  Caching At Scale explores techniques to minimize latency and reduce backend load by storing copies of frequently accessed data in memory. Prerequisites include an understanding of memory hierarchies and basic database read/write operations. You will learn caching strategies (Cache-Aside, Write-Through), eviction policies, and how to solve critical production caching issues like Stampedes, Avalanches, and Penetration.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  THE 80/20 RULE (PARETO PRINCIPLE)
    80% of traffic accesses 20% of the data. Caching that 20% yields massive performance gains.

  CACHE EVICTION
    Removing items when the cache is full (LRU, LFU, FIFO).

  CACHE INVALIDATION
    Removing items when the underlying data changes, keeping cache and DB consistent.

  CACHE STAMPEDE / THUNDERING HERD
    When a popular cache key expires, thousands of concurrent requests miss the cache and hit the database simultaneously, potentially crashing it.

  CACHE PENETRATION
    Malicious/frequent queries for data that doesn't exist in the DB. The cache always misses, routing all traffic to the DB.

  CACHE AVALANCHE
    When many cache keys expire at the exact same time, causing a sudden spike in database load.

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  CACHING STRATEGIES                                                     │
  │                                                                         │
  │  [ Cache-Aside (Lazy Loading) ]                                         │
  │  App -> Checks Cache -> (Miss) -> App reads DB -> App writes to Cache -> App returns data│
  │    * Used for read-heavy workloads.                                     │
  │                                                                         │
  │  [ Read-Through ]                                                       │
  │  App -> Reads from Cache Provider -> (Miss) -> Cache Provider reads DB -> Returns to App│
  │    * App code is cleaner, cache provider handles DB sync.               │
  │                                                                         │
  │  [ Write-Through ]                                                      │
  │  App -> Writes to Cache -> Cache writes synchronously to DB -> Returns Success│
  │    * High write latency, but strict consistency.                        │
  │                                                                         │
  │  [ Write-Behind (Write-Back) ]                                          │
  │  App -> Writes to Cache -> Returns Success immediately -> Cache asynchronously writes to DB│
  │    * Extremely fast writes, but risk of data loss if cache crashes before DB sync.│
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  4. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: python]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // LRU Cache Implementation (Conceptual)                                │
  │                                                                          │
  │  from collections import OrderedDict                                     │
  │                                                                          │
  │  class LRUCache:                                                         │
  │      def __init__(self, capacity: int):                                  │
  │          self.cache = OrderedDict()                                      │
  │          self.capacity = capacity                                        │
  │                                                                          │
  │      def get(self, key: int) -> int:                                     │
  │          if key not in self.cache:                                       │
  │              return -1                                                   │
  │          # Move to end to show it was recently used                      │
  │          self.cache.move_to_end(key)                                     │
  │          return self.cache[key]                                          │
  │                                                                          │
  │      def put(self, key: int, value: int) -> None:                        │
  │          if key in self.cache:                                           │
  │              self.cache.move_to_end(key)                                 │
  │          self.cache[key] = value                                         │
  │          if len(self.cache) > self.capacity:                             │
  │              # Pop the first item (least recently used)                  │
  │              self.cache.popitem(last=False)                              │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: python]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │                                                                          │
  │  import redis                                                            │
  │  import sqlite3                                                          │
  │  import json                                                             │
  │  import time                                                             │
  │  import random                                                           │
  │                                                                          │
  │  # Cache-Aside pattern with Cache Stampede prevention (Probabilistic Early Expiration)│
  │  cache = redis.Redis(host='localhost', port=6379, db=0)                  │
  │  db = sqlite3.connect('app.db', check_same_thread=False)                 │
  │                                                                          │
  │  def get_user_profile(user_id: str):                                     │
  │      cache_key = f"user_profile:{user_id}"                               │
  │                                                                          │
  │      # 1. Check cache                                                    │
  │      cached_data = cache.get(cache_key)                                  │
  │      if cached_data:                                                     │
  │          data = json.loads(cached_data)                                  │
  │                                                                          │
  │          # XFetch: Probabilistic early expiration to prevent Stampede    │
  │          # If we are close to the TTL, randomly decide to re-compute early│
  │          ttl = cache.ttl(cache_key)                                      │
  │          if ttl > 0 and ttl < 10 and random.random() < 0.2:              │
  │              print("[Early Refresh] Refreshing in background to prevent stampede...")│
  │              _refresh_cache(cache_key, user_id)                          │
  │                                                                          │
  │          return data['payload']                                          │
  │                                                                          │
  │      # 2. Cache Miss - Fetch from DB                                     │
  │      return _refresh_cache(cache_key, user_id)                           │
  │                                                                          │
  │  def _refresh_cache(cache_key: str, user_id: str):                       │
  │      cursor = db.cursor()                                                │
  │      cursor.execute("SELECT name, email FROM users WHERE id=?", (user_id,))│
  │      row = cursor.fetchone()                                             │
  │                                                                          │
  │      # Handle Cache Penetration: Cache null values for a short time      │
  │      if not row:                                                         │
  │          cache.setex(cache_key, 60, json.dumps({'payload': None})) # 1 min TTL│
  │          return None                                                     │
  │                                                                          │
  │      user_data = {"name": row[0], "email": row[1]}                       │
  │                                                                          │
  │      # Handle Cache Avalanche: Add random jitter to TTL                  │
  │      base_ttl = 3600 # 1 hour                                            │
  │      jitter = random.randint(0, 300) # 0-5 mins jitter                   │
  │      cache.setex(cache_key, base_ttl + jitter, json.dumps({'payload': user_data}))│
  │                                                                          │
  │      return user_data                                                    │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: Explain the Cache-Aside pattern.

  ANSWER:
    The application first queries the cache. On a hit, return data. On a miss, query the DB, store the result in the cache, and return.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: What is a Cache Stampede and how do you fix it?

  ANSWER:
    Concurrent misses for a popular key. Fix using Mutex locks (only one thread fetches DB, others wait) or Probabilistic Early Expiration (refresh cache before it strictly expires).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: What is Cache Penetration and how do you prevent it?

  ANSWER:
    Queries for non-existent keys. Prevent by caching null values with short TTLs or using a Bloom Filter before querying the DB.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: How do you prevent a Cache Avalanche?

  ANSWER:
    Add random jitter to TTLs so keys don't expire simultaneously. Warm up the cache before putting it live.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: Redis vs Memcached?

  ANSWER:
    Memcached is purely in-memory, multithreaded, simple strings. Redis supports data structures (Lists, Sets, Hashes), persistence (AOF/RDB), replication, and Lua scripting (single-threaded).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: Write-Through vs Write-Behind?

  ANSWER:
    Write-Through writes to cache and DB synchronously (slower, safer). Write-Behind writes to cache and a background job syncs to DB (faster, risk of data loss).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q7: What happens when Redis runs out of memory?

  ANSWER:
    It executes the configured maxmemory-policy (e.g., allkeys-lru evicts least recently used keys, noeviction returns errors on write).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q8: How do you handle the Hot Key problem?

  ANSWER:
    When a single key (e.g., celebrity profile) receives millions of reads, overwhelming one Redis node, use a local in-memory cache on the application servers (Guava, Caffeine) to short-circuit the network call.

────────────────────────────────────────────────────────────────────────────────
  7. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: Riddle 1

  "I'm meant to save the database, but when a celebrity posts and I expire, I accidentally execute the database." What am I?

  SOLUTION:
    Problem: 
    Fix: A cache experiencing a Thundering Herd (Stampede).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 2: Riddle 2

  // What is the flaw?
  async function getUser(id) {
      let user = await redis.get(`user:${id}`);
      if (!user) {
          user = await db.query(`SELECT * FROM users WHERE id = ${id}`);
          if (user) await redis.set(`user:${id}`, user, 'EX', 3600);
      }
      return user;
  }

  SOLUTION:
    Problem: 
    Fix: Cache Penetration vulnerability. If an attacker requests id=999999 repeatedly, user is null, so it never gets cached, slamming the database on every request.

────────────────────────────────────────────────────────────────────────────────
  8. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  Databases are fundamentally limited by disk I/O and connection counts. In-memory caching provides microsecond latency (vs millisecond DB latency) and handles millions of QPS. Without proper caching strategies, social media feeds, e-commerce product pages, and heavy dashboards would crumble under production loads.

────────────────────────────────────────────────────────────────────────────────
  9. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

  -> File 092: Design Instagram (How caching is used for feeds)
  -> File 089: SystemDesign Fundamentals (Back-of-the-envelope calculation for cache sizing)

================================================================================
  END OF FILE 091
================================================================================
