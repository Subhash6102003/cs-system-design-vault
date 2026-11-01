================================================================================
  FILE 094: DESIGN URLSHORTENER RATELIMITER
  Section: H - System Design at Scale
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  URL Shortener & Rate Limiter covers two classic system design problems that share a focus on high-throughput, low-latency, and distributed coordination. Prerequisites include hashing algorithms and caching. You will learn how to encode URLs, resolve collisions, and enforce API usage quotas across distributed systems.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  BASE62 ENCODING
    Uses [0-9, a-z, A-Z] (62 characters) to convert a base-10 number (counter) into a short string (e.g., 100 -> bM). 7 characters can represent 3.5 trillion URLs.

  301 VS 302 REDIRECT
    - 301 Permanent: Browsers cache the redirect. Good for server load, bad for analytics.
    - 302 Temporary: Browsers hit the shortener every time. Good for analytics, higher server load.

  RATE LIMITING ALGORITHMS
    - Token Bucket: Tokens are added to a bucket at a fixed rate. Requests consume tokens. Allows bursts.
    - Leaky Bucket: Requests enter a queue, processed at a constant rate. Smooths out traffic.
    - Fixed Window: Counters per time window (e.g., 00:00 - 00:01). Can double-allow at boundaries.
    - Sliding Window Log: Stores timestamps of all requests. Perfectly accurate, high memory.

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  TOKEN BUCKET RATE LIMITER                                              │
  │                                                                         │
  │    [ Refill 10 tokens / sec ]                                           │
  │              |                                                          │
  │              v                                                          │
  │        +-----------+                                                    │
  │        | o o o o   | <-- Capacity: 100 tokens                           │
  │        +-----------+                                                    │
  │              |                                                          │
  │     (Request consumes 1 token) -> [ Processed ]                         │
  │     (If bucket empty)          -> [ 429 Too Many Requests ]             │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  URL SHORTENER WRITE FLOW                                               │
  │                                                                         │
  │  [ Client ] -> [ API Gateway ] -> [ Application Server ] -> Gets Counter (e.g., 1000001)│
  │                                        |                    from Zookeeper/DB│
  │                                 (Base62 Encode)                         │
  │                                        |                                │
  │                                [ Returns: bit.ly/Xyz ] -> Saves {short: Xyz, long: URL} in DB│
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  4. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: python]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Base62 Encoding for URL Shortener                                    │
  │                                                                          │
  │  BASE62 = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"│
  │                                                                          │
  │  def encode_base62(num: int) -> str:                                     │
  │      """Converts a database auto-increment ID to a short URL string."""  │
  │      if num == 0:                                                        │
  │          return BASE62[0]                                                │
  │                                                                          │
  │      encoded = []                                                        │
  │      while num > 0:                                                      │
  │          num, rem = divmod(num, 62)                                      │
  │          encoded.append(BASE62[rem])                                     │
  │                                                                          │
  │      return ''.join(reversed(encoded))                                   │
  │                                                                          │
  │  # Example: DB ID 100,000,000 becomes short string                       │
  │  print(encode_base62(100000000)) # '6LAze'                               │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: python]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │                                                                          │
  │  # Distributed Fixed Window Rate Limiter using Redis (Lua Script)        │
  │  import redis                                                            │
  │  import time                                                             │
  │                                                                          │
  │  r = redis.Redis(host='localhost', port=6379, db=0)                      │
  │                                                                          │
  │  def is_rate_limited(user_id: str, limit: int, window_sec: int) -> bool: │
  │      """                                                                 │
  │      Uses Redis INCR and EXPIRE to enforce limits.                       │
  │      Returns True if limited (429), False otherwise.                     │
  │      """                                                                 │
  │      # Current window epoch (e.g., minute boundary)                      │
  │      current_window = int(time.time() // window_sec)                     │
  │      redis_key = f"rate_limit:{user_id}:{current_window}"                │
  │                                                                          │
  │      # Atomic increment                                                  │
  │      current_count = r.incr(redis_key)                                   │
  │                                                                          │
  │      # Set expiry on first request in window to avoid memory leak        │
  │      if current_count == 1:                                              │
  │          r.expire(redis_key, window_sec * 2)                             │
  │                                                                          │
  │      return current_count > limit                                        │
  │                                                                          │
  │  # Usage: 5 requests per 10-second window                                │
  │  user = "alice123"                                                       │
  │  for i in range(7):                                                      │
  │      if is_rate_limited(user, limit=5, window_sec=10):                   │
  │          print(f"Request {i+1}: 429 TOO MANY REQUESTS")                  │
  │      else:                                                               │
  │          print(f"Request {i+1}: 200 OK")                                 │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: How do you prevent URL collisions if you use hashing (MD5)?

  ANSWER:
    MD5 generates a 128-bit hash. Taking the first 7 chars of base62 causes collisions. On collision, append a unique string (or sequence) to the original URL and rehash, or just use the Base62 Counter method which guarantees uniqueness.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: How do you generate distributed unique IDs for the counter approach?

  ANSWER:
    Using Zookeeper to manage counter ranges (e.g., Server A gets 1-1,000,000, Server B gets 1,000,001-2,000,000), or using Twitter Snowflake, or a dedicated auto-incrementing database table.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: What database would you use for a URL shortener?

  ANSWER:
    A NoSQL key-value store (e.g., DynamoDB, Cassandra) is perfect since we only need simple GET (short->long) and PUT. It scales horizontally easily for billions of records.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: How do you rate limit distributed across 50 API servers?

  ANSWER:
    Local memory isn't synchronized. Use a centralized Redis cluster to track counts. To reduce latency, use a Redis Lua script or the Token Bucket algorithm with local bucket caches synced asynchronously.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: What is the flaw of the Fixed Window algorithm?

  ANSWER:
    The boundary problem. If limit is 10/min, a user can send 10 requests at 12:00:59, and 10 more at 12:01:01. They essentially did 20 requests in 2 seconds.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: How do you track analytics for short URLs?

  ANSWER:
    Push click events to a Kafka queue asynchronously during the redirect. Use stream processing (Flink/Spark) to aggregate clicks by geography/time, storing results in a Data Warehouse.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q7: How would you rate limit by IP if users are behind a shared NAT?

  ANSWER:
    IP rate limiting will unfairly punish all users on that NAT. Better to rate limit by authenticated API Key, User-ID, or a combination of IP and device fingerprint.

────────────────────────────────────────────────────────────────────────────────
  7. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: Riddle 1

  "I'm a bucket with holes, but I'm designed to calm the storm, not spill the water."

  SOLUTION:
    Problem: 
    Fix: The Leaky Bucket Rate Limiting Algorithm.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 2: Riddle 2

  # Token bucket refill logic running on every request
  bucket.tokens += (current_time - last_request_time) * refill_rate
  bucket.tokens = min(bucket.tokens, MAX_CAPACITY)

  SOLUTION:
    Problem: 
    Fix: This logic is correct conceptually, but if executed concurrently by multiple requests hitting the same bucket in DB/Redis, race conditions will overwrite the token count. It MUST be executed atomically via Redis Lua scripts.

────────────────────────────────────────────────────────────────────────────────
  8. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  URL Shorteners teach the critical pattern of ID generation and O(1) key-value retrieval at scale. Rate limiting is non-negotiable in production; without it, DDoS attacks, rogue scrapers, or a bug in a client's while(true) loop will take down your entire microservice ecosystem.

────────────────────────────────────────────────────────────────────────────────
  9. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

  -> File 091: Caching at Scale (Caching hot URLs)
  -> File 096: Distributed Systems (Distributed ID Generators (Snowflake))

================================================================================
  END OF FILE 094
================================================================================
