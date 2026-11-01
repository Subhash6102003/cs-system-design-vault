================================================================================
  FILE 092: DESIGN INSTAGRAM
  Section: H - System Design at Scale
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  Design Instagram walks through designing a massive-scale photo-sharing application. Prerequisites include understanding databases, object storage, and caching. You will learn how to handle read/write-heavy media workloads, generate news feeds efficiently using fan-out strategies, and architect a robust like-counter system.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  BLOB STORE
    Distributed object storage (e.g., Amazon S3) used to store immutable media files (photos, videos).

  FAN-OUT
    The process of pushing an update to all followers.
    - Fan-out on Write (Push): Pre-compute the feed during a write. Fast reads, slow writes.
    - Fan-out on Read (Pull): Compute the feed during a read. Fast writes, slow reads.

  EPHEMERAL CONTENT
    Data that expires after a set time (e.g., Instagram Stories, TTL 24h).

  SHARDING
    Horizontally partitioning the database (e.g., by User ID) to scale writes.

  EVENTUAL CONSISTENCY
    Acceptable delay in feed updates or like counts.

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  FULL ARCHITECTURE                                                      │
  │                                                                         │
  │  [ Client ] -> [ API Gateway / CDN ]                                    │
  │                       |                                                 │
  │              +--------+--------+                                        │
  │              |                 |                                        │
  │       [ Media Service ]  [ Timeline Service ] <--- [ Cache (Redis) ]    │
  │              |                 |                                        │
  │         [ S3 (Blobs) ]   [ PostgreSQL (Metadata) ]                      │
  │              |                                                          │
  │       [ CDN Edge Nodes]                                                 │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  FAN-OUT ON WRITE VS FAN-OUT ON READ                                    │
  │                                                                         │
  │  [ Fan-Out on Write (Normal User) ]                                     │
  │  User posts -> Gets 200 followers -> Pushes Post ID to 200 Redis Timelines.│
  │  Follower reads -> Fetches pre-computed Redis Timeline O(1).            │
  │                                                                         │
  │  [ Fan-Out on Read (Celebrity with 100M followers) ]                    │
  │  Celebrity posts -> Saved to DB only.                                   │
  │  Follower reads -> Pulls own Timeline + Pulls Celebrity's latest posts and merges O(N).│
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  4. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: python]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Hybrid Feed Generation (Conceptual)                                  │
  │                                                                          │
  │  def generate_feed(user_id):                                             │
  │      # 1. Fetch pre-computed feed (from Fan-out on Write)                │
  │      feed_cache = redis.get(f"feed:{user_id}")                           │
  │      feed = parse_cache(feed_cache)                                      │
  │                                                                          │
  │      # 2. Fetch active celebrities the user follows (Fan-out on Read)    │
  │      celebrities = db.query("SELECT celeb_id FROM follows WHERE follower=? AND is_celeb=true", user_id)│
  │                                                                          │
  │      for celeb in celebrities:                                           │
  │          celeb_posts = redis.get(f"user_posts:{celeb}")                  │
  │          feed.extend(celeb_posts)                                        │
  │                                                                          │
  │      # 3. Sort by timestamp and return                                   │
  │      feed.sort(key=lambda x: x.timestamp, reverse=True)                  │
  │      return feed[:50]                                                    │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: javascript]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │                                                                          │
  │  // High-Scale Like Counter (Write-Behind via Redis & Kafka)             │
  │  const redis = require('redis');                                         │
  │  const kafka = require('kafka-node');                                    │
  │                                                                          │
  │  const redisClient = redis.createClient();                               │
  │  const producer = new kafka.Producer(new kafka.KafkaClient());           │
  │                                                                          │
  │  // 1. Client hits API to like a photo                                   │
  │  async function handleLikePhoto(req, res) {                              │
  │      const { photoId, userId } = req.body;                               │
  │                                                                          │
  │      // Check if already liked (using Redis SET to avoid duplicate DB calls)│
  │      const isNewLike = await redisClient.sadd(`photo_likes_users:${photoId}`, userId);│
  │                                                                          │
  │      if (isNewLike) {                                                    │
  │          // Atomic increment in Redis (Extremely fast O(1))              │
  │          const count = await redisClient.incr(`photo_likes_count:${photoId}`);│
  │                                                                          │
  │          // Push event to Kafka for Async Database processing            │
  │          producer.send([{                                                │
  │              topic: 'photo-likes',                                       │
  │              messages: JSON.stringify({ photoId, userId, timestamp: Date.now() })│
  │          }], (err) => {                                                  │
  │              if (err) console.error("Kafka queue full", err);            │
  │          });                                                             │
  │                                                                          │
  │          res.status(200).json({ success: true, newCount: count });       │
  │      } else {                                                            │
  │          res.status(400).json({ error: "Already liked" });               │
  │      }                                                                   │
  │  }                                                                       │
  │                                                                          │
  │  // 2. Kafka Consumer (Background Worker) bathes writes to Postgres      │
  │  /*                                                                      │
  │  Kafka consumer reads 1000 messages from 'photo-likes' topic.            │
  │  Executes batch insert:                                                  │
  │  INSERT INTO likes (photo_id, user_id) VALUES (...), (...);              │
  │  UPDATE photos SET like_count = like_count + X WHERE id = Y;             │
  │  */                                                                      │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: How do you store user uploaded photos?

  ANSWER:
    Store the actual image binary in a Blob Store (S3), generate multiple resolutions asynchronously via a message queue (SQS + Lambda), and store the metadata (S3 URL, timestamp, user_id) in a relational DB (PostgreSQL).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: What is the problem with Fan-out on Write for celebrities (e.g., Cristiano Ronaldo)?

  ANSWER:
    Pushing an update to 500 million followers takes massive compute and time, causing the "Thundering Herd" problem. We use Fan-out on Read for celebrities instead.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: How do you generate primary keys for posts?

  ANSWER:
    Auto-increment in an RDBMS won't scale across sharded databases. Use a distributed ID generator like Twitter Snowflake (time + worker_id + sequence) to generate 64-bit sortable IDs.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: How would you shard the database?

  ANSWER:
    Shard by user_id. All metadata for a user (their posts, followers) lives on the same shard. Problem: celebrity shards become hot spots. Mitigation: caching and dedicated replica nodes.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: How are Instagram Stories designed differently from Posts?

  ANSWER:
    Stories are highly read-heavy but ephemeral. Store metadata in a NoSQL DB (e.g., Cassandra) or Redis with a strict 24-hour TTL, automatically garbage collecting expired data.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: How do you build the Instagram Explore page?

  ANSWER:
    Heavy use of Machine Learning pipeline. Offline jobs (Spark/Hadoop) analyze user interaction graphs, generating embeddings. Online serving fetches nearest-neighbor recommendations from a vector database (e.g., FAISS).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q7: How does the Like counter handle 100k likes per second?

  ANSWER:
    Never write directly to PostgreSQL. Buffer counts in Redis (atomic INCR), and asynchronously flush to the DB via a message queue (Write-Behind caching).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q8: Estimate the storage for photos (100M DAU, 1 photo/day, 2MB/photo).

  ANSWER:
    100M * 2MB = 200TB per day. Over a year: ~73 Petabytes. Requires highly scalable object storage.

────────────────────────────────────────────────────────────────────────────────
  7. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: Riddle 1

  "I'm perfectly fine for your mom's account, but if Justin Bieber uses me, the database servers burst into flames."

  SOLUTION:
    Problem: 
    Fix: Fan-out on Write architecture.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 2: Riddle 2

  -- What is the flaw for counting likes?
  SELECT COUNT(*) FROM likes WHERE photo_id = 12345;

  SOLUTION:
    Problem: 
    Fix: COUNT(*) in an RDBMS requires scanning rows (O(N)), which is incredibly slow for a photo with millions of likes. It should be a denormalized like_count integer on the photos table, updated incrementally.

────────────────────────────────────────────────────────────────────────────────
  8. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  Media-heavy social networks are the ultimate test of system design. Balancing read-heavy feeds with write-heavy media uploads requires decoupling systems, aggressive caching, and deep understanding of network vs storage tradeoffs.

────────────────────────────────────────────────────────────────────────────────
  9. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

  -> File 096: Distributed Systems (Snowflake ID generation)
  -> File 097: Data Pipeline Architecture (Explore page ML pipelines)

================================================================================
  END OF FILE 092
================================================================================
