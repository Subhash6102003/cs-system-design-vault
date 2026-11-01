================================================================================
  FILE 098B: SYSTEM DESIGN & BACKEND ARCHITECTURE — COMPLETE 55-PHASE INTERVIEW ROADMAP
  Section: H - System Design at Scale
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW & ROADMAP BLUEPRINT
────────────────────────────────────────────────────────────────────────────────

  This master reference is the comprehensive system design and distributed backend
  engineering curriculum, spanning all 55 phases from low-level networking prerequisites
  to high-scale microservices design across Java (Spring Boot), Python (FastAPI/Celery),
  and Node.js/Express.js.

  Every concept, mathematical estimation, database trade-off, failure scenario, and
  architectural design is addressed with production-tested mechanics and concrete code.

  ROADMAP ARCHITECTURE AT A GLANCE:
  - MODULE 1 (Phases 0-2): Networking, Complete Request Flow & Client-Server Mechanics
  - MODULE 2 (Phases 3, 16, 17): REST APIs, Rate Limiting & API Gateways
  - MODULE 3 (Phases 4, 31): Authentication, Authorization & Distributed Security
  - MODULE 4 (Phases 5, 6, 26, 28): Databases, Storage Engines, Sharding & Search
  - MODULE 5 (Phases 7, 8, 27): In-Memory Caching (Redis), Load Balancing & CDNs
  - MODULE 6 (Phases 9-15): Queues, Workers, Background Jobs, Notifications & SMTP
  - MODULE 7 (Phases 18-25, 29-30): Microservices, Distributed Systems & Observability
  - MODULE 8 (Phases 32, 33, 50): Cloud Infrastructure, CI/CD & Back-of-the-Envelope Math
  - MODULE 9 (Phases 34-44): 17-Step Interview Framework & 20 Priority System Designs
  - MODULE 10 (Phases 45-55): Failure Modes, Trade-Off Matrices, Schemas & Interview Checklist

────────────────────────────────────────────────────────────────────────────────
  2. MODULE 1: NETWORKING, REQUEST LIFECYCLE & CLIENT-SERVER ARCHITECTURE (PHASES 0 - 2)
────────────────────────────────────────────────────────────────────────────────

  PHASE 0: PREREQUISITES & NETWORKING MECHANICS

  What Happens When You Enter a URL in a Browser?
    1. URL Parsing: Browser extracts protocol (https), domain (api.company.com), port (443), path.
    2. DNS Resolution:
       - Checks browser cache -> OS cache -> hosts file -> local router -> ISP recursive resolver.
       - Recursive resolver queries Root DNS ('.') -> TLD DNS ('.com') -> Authoritative Name Server.
       - Returns A record (IPv4: 198.51.100.1) or AAAA record (IPv6).
    3. TCP 3-Way Handshake:
       - Client sends SYN (Synchronize sequence number X).
       - Server responds with SYN-ACK (Ack X+1, Sequence Y).
       - Client sends ACK (Ack Y+1). Connection ESTABLISHED.
    4. TLS 1.3 Handshake:
       - Client sends ClientHello (supported cipher suites, client key share).
       - Server replies with ServerHello, X.509 digital certificate, server key share.
       - Both compute shared symmetric session key via ECDHE math. Encrypted channel ready.
    5. HTTP Request & Processing:
       - Client sends GET /index.html HTTP/2 with headers.
       - Traffic hits CDN -> Anycast DNS -> Load Balancer (ALB) -> Nginx -> Application Server.
    6. Browser Rendering:
       - Browser receives HTML bytes -> Tokenization -> DOM Tree.
       - Parses CSS -> CSSOM Tree.
       - Combines into Render Tree -> Layout (Reflow) -> Paint -> Composite.

  Networking Fundamentals & Differences:
    - DNS (Domain Name System): Distributed, hierarchical key-value directory mapping human-readable
      hostnames to IP addresses. Operates primarily over UDP port 53 for speed (sub-50ms).
    - IPv4 vs. IPv6: IPv4 uses 32-bit addresses (4.3 billion limit, exhausted); IPv6 uses 128-bit
      hexadecimal addresses (3.4 x 10^38 unique addresses, eliminates NAT complexity).
    - Public vs. Private IP: Public IPs are globally routable across the public internet. Private IPs
      (RFC 1918: 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16) operate inside private local networks / VPCs.
    - Port: 16-bit integer (0-65535) identifying a specific application or process endpoint on a host.
    - TCP vs. UDP:
      * TCP: Connection-oriented, reliable, guaranteed ordered delivery, flow control (sliding window),
        congestion control. Used for HTTP, WebSockets, gRPC, database connections.
      * UDP: Connectionless, unreliable, unordered, lightweight (8-byte header vs 20-byte TCP).
        Used for DNS, live streaming, WebRTC audio/video, multiplayer gaming.
    - HTTP Protocol Evolution:
      * HTTP/1.1: Persistent connections (Keep-Alive), but suffers from Head-of-Line (HoL) blocking.
      * HTTP/2: Binary framing layer, multiplexed streams over 1 TCP connection, header compression (HPACK).
      * HTTP/3: Replaces TCP with QUIC over UDP. Eliminates TCP HoL blocking, supports 0-RTT handshakes
        and connection migration (switching Wi-Fi to 5G seamlessly).
    - Proxy Types:
      * Forward Proxy: Sits in front of clients; hides client identity, bypasses firewalls (e.g. corporate VPN).
      * Reverse Proxy: Sits in front of servers; hides server infrastructure, terminates SSL, balances load.
    - Real-Time Communication Strategies:
      * Polling: Client sends HTTP GET every 3 seconds. Wasteful, high server CPU overhead.
      * Long Polling: Server holds connection open until data is available, then closes. High reconnections.
      * SSE (Server-Sent Events): Unidirectional (Server -> Client) text stream over HTTP/2. Auto-reconnects.
      * WebSockets: Full-duplex bidirectional TCP communication after HTTP upgrade handshake. Low latency.
      * gRPC: Google RPC framework using HTTP/2 transport and Protocol Buffers binary serialization.

  PHASE 1: THE COMPLETE REQUEST FLOW BLUEPRINT

  ┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
  │  COMPLETE REQUEST LIFECYCLE (END-TO-END SYSTEM BLUEPRINT)                                       │
  │                                                                                                 │
  │  [ User Device ]                                                                                │
  │        │                                                                                        │
  │        ├─(1. Resolve Domain)──> [ DNS Server (Route 53) ]                                       │
  │        │                                                                                        │
  │        ├─(2. Static Asset Hit?)──> [ CDN Edge Cache (CloudFront) ]                             │
  │        │                                                                                        │
  │        v (3. Dynamic API Request over HTTPS)                                                    │
  │  +──────────────────────────────────────────────────────────+                                   │
  │  |  Load Balancer (AWS ALB / Nginx L7)                      | <── Health Checks, SSL Termination│
  │  +─────────────────────────────┬────────────────────────────+                                   │
  │                                │ 4. Routes to VPC                                               │
  │                                v                                                                │
  │  +──────────────────────────────────────────────────────────+                                   │
  │  |  API Gateway (Kong / Spring Cloud Gateway)               | <── JWT Validation, Rate Limiting │
  │  +─────────────────────────────┬────────────────────────────+                                   │
  │                                │ 5. Forward Authenticated Request                               │
  │                                v                                                                │
  │  +──────────────────────────────────────────────────────────+                                   │
  │  |  Backend Microservice (Spring Boot / Node / FastAPI)     |                                   │
  │  +───────┬─────────────────────┬────────────────────┬───────+                                   │
  │          │ 6. Check Cache      │ 7. Cache Miss Query│ 8. Async Work                             │
  │          v                     v                    v                                           │
  │    [ Redis Cache ]     [ PostgreSQL / Mongo ]  [ Kafka / RabbitMQ / SQS ]                       │
  │                                                     │                                           │
  │                                                     v 9. Consume Event                          │
  │                                            [ Background Workers ]                               │
  │                                                     │                                           │
  │                                                     v 10. External API                          │
  │                                            [ SES / FCM / Twilio Push ]                          │
  └─────────────────────────────────────────────────────────────────────────────────────────────────┘

  Component Responsibility Rules:
    - Synchronous vs. Asynchronous:
      * Synchronous (User Waits): Authentication, querying product catalog, placing initial order, reading feed.
      * Asynchronous (Decoupled): Sending confirmation email, generating PDF invoice, video transcoding,
        updating search index, awarding loyalty points.
    - When to check cache? Immediately before touching the database.
    - Why workers? Offloads slow, unpredictable I/O from blocking user-facing HTTP threads.

  PHASE 2: CLIENT-SERVER ARCHITECTURE

    - What Happens When an Android App Calls an API?
      Retrofit generates dynamic proxy -> OkHttp builds HTTP request -> Android OS executes network
      syscall over cell/Wi-Fi modem -> Traverses gateways -> Receives JSON -> Moshi parses to Kotlin objects.
    - Why Business Logic Must Never Live in Frontend:
      1. Security: Client code can be decompiled, inspected, and manipulated in browser DevTools or APK patches.
      2. Data Integrity: Client-side validation is trivial to bypass using curl or Postman.
      3. Centralized Auditing & Rules: Business rules change instantly on servers without requiring app store updates.
    - Can Frontend Connect Directly to Supabase/Firebase?
      Yes, via Row Level Security (RLS) policies where Postgres verifies JWT claims directly. However,
      for complex multi-table domain logic, third-party payment APIs, and audit trails, a backend service is mandatory.

────────────────────────────────────────────────────────────────────────────────
  3. MODULE 2: REST APIS, RATE LIMITING & GATEWAYS (PHASES 3, 16, 17)
────────────────────────────────────────────────────────────────────────────────

  REST API MASTERY:
    - Richardson Maturity Model: Level 0 (The Swamp of POX), Level 1 (Resources), Level 2 (HTTP Verbs),
      Level 3 (HATEOAS hypermedia links).
    - HTTP Methods & Idempotency:
      * GET: Idempotent & Safe. Retrieves representation without modifying state.
      * POST: Non-idempotent & Unsafe. Appends new resource (e.g. /orders).
      * PUT: Idempotent. Complete replacement of resource at specific URI.
      * PATCH: Non-idempotent (by spec) / Idempotent (if key-value). Partial update.
      * DELETE: Idempotent. Removes resource; subsequent calls return 404/204, server state remains deleted.
    - Status Codes:
      * 200 OK, 201 Created, 204 No Content.
      * 400 Bad Request, 401 Unauthorized (unauthenticated), 403 Forbidden (authenticated but unauthorized).
      * 404 Not Found, 409 Conflict (duplicate record), 429 Too Many Requests.
      * 500 Internal Error, 502 Bad Gateway (upstream dead), 503 Service Unavailable (overloaded).
    - Pagination Strategies:
      * Offset Pagination (OFFSET 50000 LIMIT 20): O(N) database cost. Suffers from phantom duplicates on inserts.
      * Cursor-Based Pagination (WHERE id > last_seen_id ORDER BY id LIMIT 20): O(1) B+Tree index seek. Perfect for infinite scroll.

  RATE LIMITING ALGORITHMS (PHASE 16):
    1. Fixed Window: Counts requests in fixed 1-minute blocks. Vulnerable to 2x burst traffic at boundary transitions.
    2. Sliding Window Log: Stores timestamp of every request in Redis Sorted Set (ZSET). Precise, but high memory footprint.
    3. Sliding Window Counter: Blends current window count and previous window count proportionally. Low memory, highly accurate.
    4. Token Bucket: Bucket fills with tokens at rate R up to capacity C. Requests consume tokens. Handles bursts gracefully.
    5. Leaky Bucket: Requests enter FIFO queue and leak out at smooth constant rate. Ideal for traffic shaping.

  API GATEWAY RESPONSIBILITIES (PHASE 17):
    - Reverse proxy routing to private internal microservices.
    - Edge authentication: Verifies JWT signatures once; injects sanitized 'X-User-Id' header for downstream services.
    - Rate limiting per API Key / IP using shared Redis cluster.
    - Request transformation (protocol translation: public REST JSON to internal gRPC Protobuf).

────────────────────────────────────────────────────────────────────────────────
  4. MODULE 3: AUTHENTICATION, AUTHORIZATION & SECURITY (PHASES 4, 31)
────────────────────────────────────────────────────────────────────────────────

  AUTH MECHANICS:
    - Authentication (AuthN): Proves WHO you are (username/password, biometric, OTP).
    - Authorization (AuthZ): Proves WHAT you can do (Admin vs Recruiter vs Candidate permissions).
    - Session-Based Auth: Server stores session in Redis/DB; client holds opaque session ID in httpOnly cookie.
      * Pros: Instant revocation. Cons: Stateful, memory overhead at scale.
    - JWT (JSON Web Token): Stateless token consisting of Header.Payload.Signature.
      * Signature = HMAC-SHA256(Base64(Header) + "." + Base64(Payload), SecretKey).
      * Pros: Decoupled, verified on any server without database lookups.
      * Cons: Cannot be invalidated instantly without a token blacklist.
    - Refresh Token Rotation: Short-lived Access Token (15 mins) + Long-lived Refresh Token (7 days).
      When refreshed, the old refresh token is invalidated and a new pair is issued. Detects token theft.
    - RBAC (Role-Based Access Control) vs ABAC (Attribute-Based Access Control):
      * RBAC: Permissions tied to fixed roles (ROLE_ADMIN, ROLE_RECRUITER).
      * ABAC: Dynamic policy evaluation (e.g. Can view document IF user.department == doc.department AND time == work_hours).

  SECURITY VULNERABILITIES & MITIGATION:
    - Password Hashing: NEVER encrypt passwords (encryption is reversible). Use bcrypt / Argon2 with adaptive
      work factor (salt + 12 rounds) to prevent rainbow table attacks and GPU brute-forcing.
    - SQL Injection: Attacker injects SQL fragments (' OR 1=1 --). Prevention: Parameterized prepared statements.
    - Cross-Site Scripting (XSS): Attacker executes malicious JavaScript in victim's browser.
      Prevention: Sanitize output, set Content Security Policy (CSP), store JWTs in httpOnly, Secure, SameSite cookies.
    - Cross-Site Request Forgery (CSRF): Malicious site tricks authenticated browser into sending unauthorized commands.
      Prevention: SameSite=Strict cookies, anti-CSRF challenge tokens.

────────────────────────────────────────────────────────────────────────────────
  5. MODULE 4: DATABASES, SCALING & STORAGE ENGINES (PHASES 5, 6, 26, 28)
────────────────────────────────────────────────────────────────────────────────

  SQL VS. NOSQL TRADEOFF MATRIX:
  ┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
  │  Feature          PostgreSQL (Relational SQL)         MongoDB (Document NoSQL)                  │
  │  ─────────────────────────────────────────────────────────────────────────────────────────────  │
  │  Data Model       Normalized Tables & Foreign Keys    Denormalized BSON Documents               │
  │  Schema           Strict, typed, schema migrations     Dynamic, flexible, polymorphic            │
  │  ACID Guarantee   Full multi-row ACID transactions     Per-document ACID (multi-doc has overhead)│
  │  Scaling          Vertical + Read Replicas (Sharding hard) Built-in horizontal sharding clusters│
  │  Best For         Financial ledgers, relational orders Catalogs, fast iteration, unjoined trees │
  └─────────────────────────────────────────────────────────────────────────────────────────────────┘

  DATABASE INDEXING INTERNALS:
    - B+Tree Indexes: Balanced multi-way trees optimized for disk blocks.
      * Leaf nodes store actual table row pointers (or clustered row data) and are linked as a doubly-linked list.
      * Range queries (BETWEEN 10 AND 50) perform 1 root-to-leaf binary search, then scan sequential leaves.
    - Why Indexes Slow Writes: Every INSERT, UPDATE, or DELETE must recalculate tree balances, split pages,
      and write to multiple index segments on disk.

  DATABASE SCALING & SHARDING (PHASE 6):
    - Read Replicas: Asynchronous WAL streaming replication from Primary (Write) to Replicas (Reads).
      * Challenge: Replication Lag (user writes profile, refreshes immediately, replica hasn't synced yet).
      * Solution: Read-your-own-writes (route user queries to Primary for 5 seconds after a write).
    - Sharding: Partitioning database horizontally across independent servers by Shard Key.
      * Range-Based: Shard 1 (A-M), Shard 2 (N-Z). Vulnerable to uneven distribution.
      * Hash-Based: Shard = Hash(user_id) % num_shards. Distributes data evenly.
      * Hot Partitions: Celebrities (e.g. Cristiano Ronaldo with 600M followers) saturate a single shard.
      * Cross-Shard Queries: Avoid joining across shards; aggregate via application logic or event-driven read models.

  OBJECT STORAGE & S3 (PHASE 26):
    - Never store binary blobs (images, videos, PDFs) inside database columns (bloats buffers, ruins cache locality).
    - Pre-Signed URLs: Client requests upload ticket -> Backend generates AWS S3 pre-signed PUT URL with 5-minute expiry ->
      Client uploads file directly to S3. Bypasses backend server bandwidth entirely.

  SEARCH ENGINES & ELASTICSEARCH (PHASE 28):
    - Why SQL 'LIKE %developer%' Fails: Cannot use B+Tree indexes; forces a full table scan over millions of rows.
    - Inverted Index: Maps distinct words (tokens) to posting lists of Document IDs (e.g. "developer" -> [Doc1, Doc4, Doc99]).
    - Supports TF-IDF, BM25 ranking, fuzziness (Levenshtein distance), and real-time autocomplete prefix trees.

────────────────────────────────────────────────────────────────────────────────
  6. MODULE 5: CACHING, LOAD BALANCING & CDNS (PHASES 7, 8, 27)
────────────────────────────────────────────────────────────────────────────────

  CACHING PATTERNS & FAILURE MODES (PHASE 7):
    - Patterns:
      * Cache-Aside (Lazy Loading): App reads Cache -> Miss -> Reads DB -> Writes Cache.
      * Read-Through: App queries Cache provider; Cache provider loads from DB transparently.
      * Write-Through: App writes to Cache; Cache synchronously updates DB before returning.
      * Write-Behind (Write-Back): App writes to Cache; Cache batches asynchronous writes to DB (Fast writes; risk of data loss).
    - Cache Failure Phenomena:
      * Cache Stampede (Thundering Herd): Hot key expires -> 50,000 concurrent requests miss cache -> All hit DB at once.
        Fix: Distributed mutex lock (Redlock) or probabilistic early expiration (XFetch).
      * Cache Penetration: Queries for non-existent IDs bypass cache and hit DB continuously.
        Fix: Cache empty result with 2-minute TTL, or evaluate a Bloom Filter at gateway.
      * Cache Avalanche: Thousands of keys expire at the exact same second.
        Fix: Add random jitter to TTL (e.g. TTL = 3600 + rand(0, 300) seconds).

  LOAD BALANCING MECHANICS (PHASE 8):
    - L4 Load Balancer: Operates at TCP layer; routes based on IP & Port. Blazingly fast, zero payload inspection.
    - L7 Load Balancer: Operates at HTTP application layer; routes based on URL path, headers, cookies, HTTP verbs.
    - Algorithms: Round Robin, Weighted Round Robin, Least Connections (best for long transactions), IP Hash.
    - Sticky Sessions: Pinning a user to a specific backend server via cookie. Anti-pattern for microservices;
      stateless servers using centralized Redis sessions are preferred.

  CDN (CONTENT DELIVERY NETWORK) (PHASE 27):
    - Geographically distributed edge servers caching static assets (images, CSS, JS, videos) close to end users.
    - Latency reduction: Reduces round-trip time (RTT) from 200ms across oceans to 10ms at local edge point of presence (PoP).

────────────────────────────────────────────────────────────────────────────────
  7. MODULE 6: QUEUES, WORKERS, NOTIFICATIONS & EMAIL SYSTEMS (PHASES 9 - 15)
────────────────────────────────────────────────────────────────────────────────

  MESSAGE BROKERS: KAFKA VS. RABBITMQ VS. SQS (PHASE 9)
  ┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
  │  Feature          RabbitMQ                           Apache Kafka                 AWS SQS       │
  │  ─────────────────────────────────────────────────────────────────────────────────────────────  │
  │  Paradigm         Smart broker, dumb consumer        Dumb broker, smart consumer  Managed Queue │
  │  Storage          Deletes message upon Ack           Persists log to disk (Days)  Managed (14d) │
  │  Routing          Complex Exchange bindings (Topic)  Topic & Partition Key        Queue URL     │
  │  Ordering         Guaranteed within queue            Guaranteed PER PARTITION     FIFO queues   │
  │  Throughput       ~50K msgs/sec                      1M+ msgs/sec                 Elastic       │
  │  Best For         Task queues, complex routing       Event streaming, audit logs  Cloud native  │
  └─────────────────────────────────────────────────────────────────────────────────────────────────┘

  WORKER POOLS & BACKGROUND JOBS (PHASE 11):
    - Decouples heavy tasks (generating PDF, image thumbnailing, sending emails) from client HTTP requests.
    - Failure Handling: Retries with exponential backoff and randomized jitter -> Dead Letter Queue (DLQ)
      after max retries (e.g. 5 attempts) to prevent poison pill messages from stalling worker loops.

  HIGH-SCALE NOTIFICATION SYSTEM DESIGN (PHASES 12, 13, 44):
    Problem: Build an engine sending 100 Million Push, SMS, and Email alerts per day.

  ┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
  │  NOTIFICATION SYSTEM ARCHITECTURE (VERSIONS 1 THROUGH 7 INTEGRATED)                             │
  │                                                                                                 │
  │  Upstream Services (Order, Auth, Marketing)                                                     │
  │        │                                                                                        │
  │        v POST /api/v1/notifications                                                             │
  │  +──────────────────────────────────────────────────────────+                                   │
  │  |  Notification Ingestion Service                          |                                   │
  │  |  - Validates Idempotency Key in Redis                    |                                   │
  │  |  - Fetches User Opt-Out Preferences (Cassandra/Redis)    |                                   │
  │  +─────────────────────────────┬────────────────────────────+                                   │
  │                                │ Route by Priority & Channel                                    │
  │                                v                                                                │
  │  +──────────────────────────────────────────────────────────+                                   │
  │  |  Apache Kafka Priority Topics                            |                                   │
  │  |  - High Priority Topic: OTPs & Security Alerts (No Delay)|                                   │
  │  |  - Low Priority Topic: Promotional Marketing Newsletters |                                   │
  │  +───────┬─────────────────────┬────────────────────┬───────+                                   │
  │          │                     │                    │                                           │
  │          v                     v                    v                                           │
  │   [ Push Workers ]      [ SMS Workers ]      [ Email Workers ]                                  │
  │   - Render Template     - Rate Limiter       - Render Handlebars                                │
  │   - Circuit Breaker     - Provider Failover  - DKIM Signature                                   │
  │          │                     │                    │                                           │
  │          v                     v                    v                                           │
  │      FCM / APNs         Twilio / MessageBird    AWS SES / SendGrid                              │
  │          │                     │                    │                                           │
  │          v                     v                    v                                           │
  │   Mobile Devices       Telecom Carriers     User Inboxes                                        │
  └─────────────────────────────────────────────────────────────────────────────────────────────────┘

  SMTP & EMAIL DELIVERABILITY (PHASES 14, 15):
    - SMTP (Simple Mail Transfer Protocol): Push protocol operating on Port 587 (STARTTLS) or 465 (TLS).
    - Deliverability Authentication Triangle:
      * SPF (Sender Policy Framework): DNS TXT record listing IP addresses authorized to send email for domain.
      * DKIM (DomainKeys Identified Mail): Cryptographic public/private key signature in email header verified via DNS.
      * DMARC: Policy record telling receivers what to do (none, quarantine, reject) if SPF or DKIM fails.
    - Bounces: Soft bounce (mailbox full, retry); Hard bounce (invalid address, suppress immediately to protect sender reputation).

────────────────────────────────────────────────────────────────────────────────
  8. MODULE 7: MICROSERVICES, DISTRIBUTED SYSTEMS & RELIABILITY (PHASES 18 - 25, 29, 30)
────────────────────────────────────────────────────────────────────────────────

  MICROSERVICES ARCHITECTURE (PHASE 18):
    - Database per Service: Each service owns its private database. Services communicate ONLY through
      APIs (synchronous gRPC) or event streams (asynchronous Kafka).
    - The Distributed Transaction Problem: Solved via the SAGA Pattern:
      * Choreography: Services react to Kafka events autonomously.
      * Orchestration: Dedicated workflow orchestrator (Temporal, AWS Step Functions) manages state transitions
        and coordinates compensating transactions upon failure.

  EVENT-DRIVEN ARCHITECTURE & OUTBOX PATTERN (PHASE 19):
    - Transactional Outbox Pattern: Prevents dual-write bugs by saving entity mutations and outbox events
      in the same ACID database transaction, read by Debezium CDC and streamed to Kafka.

  DISTRIBUTED LOCKS WITH REDIS REDLOCK (PHASE 23):
    - When two servers attempt to reserve the final concert ticket simultaneously:
      * Acquire Lock: SET lock:ticket:101 <random_token> NX PX 5000 (Atomic: set if not exists, 5s TTL).
      * Release Lock: Lua script verifies random token matches before deleting key, preventing accidental
        unlocking if process ran over TTL.

  IDEMPOTENCY IN PAYMENTS & APIS (PHASE 24):
    - Client generates unique UUID 'Idempotency-Key' in HTTP header.
    - Server checks Redis:
      * If key absent: Record key as 'PENDING', process payment, save result, return 200.
      * If key 'PENDING': Return 409 Conflict.
      * If key 'COMPLETED': Return cached previous response without recharging card.

  OBSERVABILITY (PHASES 29, 30):
    - Three Pillars: Metrics (Prometheus), Logs (ELK / Loki), Distributed Tracing (OpenTelemetry / Jaeger).
    - Correlation IDs: Injected at API Gateway as 'X-Correlation-ID', propagated across every gRPC/HTTP
      header, allowing engineers to trace a single user click across 20 downstream microservices.

────────────────────────────────────────────────────────────────────────────────
  9. MODULE 8: CLOUD, DEVOPS & BACK-OF-THE-ENVELOPE ESTIMATIONS (PHASES 32, 33, 50)
────────────────────────────────────────────────────────────────────────────────

  ESTIMATION NUMBERS CHEAT SHEET (PHASE 50):
    - Latency Numbers Every Engineer Must Know:
      * L1 CPU Cache: 0.5 ns
      * L2 CPU Cache: 7 ns
      * RAM Access: 100 ns
      * Read 1 MB sequentially from RAM: 250,000 ns (0.25 ms)
      * Read 1 MB sequentially from NVMe SSD: 1,000,000 ns (1 ms)
      * Send packet California to Netherlands & back: 150,000,000 ns (150 ms)
    - Scale Math Conversions:
      * 1 Million requests per day = ~12 requests/second.
      * 100 Million requests per day = ~1,160 requests/second average (Peak: 2,500 - 5,000 QPS).
      * 1 Billion requests per day = ~11,600 requests/second.
    - Storage Estimation Example:
      * 5 Million image uploads daily @ 2 MB each.
      * Daily Storage: 5M * 2 MB = 10 Terabytes/day.
      * Yearly Storage: 10 TB * 365 = 3.65 Petabytes/year.

────────────────────────────────────────────────────────────────────────────────
  10. MODULE 9: THE 17-STEP INTERVIEW FRAMEWORK & TOP 20 SYSTEM DESIGNS (PHASES 34 - 44)
────────────────────────────────────────────────────────────────────────────────

  THE 17-STEP SYSTEM DESIGN INTERVIEW SEQUENCE (PHASE 34):
    Step 1: Clarify Requirements & Scope.
    Step 2: Define Functional Requirements (Top 3 core user capabilities).
    Step 3: Define Non-Functional Requirements (Latency <100ms, 99.99% Availability, Eventual vs Strong Consistency).
    Step 4: Estimate Scale (DAU, Read/Write ratio, QPS, Storage, Network Bandwidth).
    Step 5: Define REST/gRPC API Contracts.
    Step 6: Design Database Data Models & Schemas.
    Step 7: High-Level Architecture Block Diagram.
    Step 8: Deep Dive into Request & Data Flows.
    Step 9: Identify Single Points of Failure (SPOF) & Bottlenecks.
    Step 10: Introduce Multi-Tier Caching (Redis/CDN).
    Step 11: Scale Compute via Load Balancers & Stateless Services.
    Step 12: Introduce Asynchronous Queues & Event Streaming (Kafka).
    Step 13: Scale Database Tier (Read Replicas, Partitioning, Sharding).
    Step 14: Design for Resilience (Circuit Breakers, Retries, Dead Letter Queues).
    Step 15: Security & Rate Limiting Enforcement.
    Step 16: Telemetry, Observability & Distributed Tracing.
    Step 17: Summarize Trade-offs & Future Improvements.

  THE 20 CRITICAL SYSTEM DESIGN ARCHITECTURES:

  1. ATS (Applicant Tracking System / Naukri / LinkedIn Jobs) [Phase 37]:
     - Candidate, Recruiter, Job, Application, Search, and Document Services.
     - Resume Parsing Pipeline: S3 Pre-Signed Upload -> SQS -> Python OCR/Parser Worker -> Elasticsearch.
     - Recruiter Full-Text Search: Elasticsearch inverted index with filtered facets.
     - Recruiter-Specific SMTP: Dynamic tenant configuration routing via custom SES identities.

  2. Interview Scheduling System [Phase 38]:
     - Prevents double-booking via PostgreSQL isolation / Redis distributed locks.
     - Slot reservation: SELECT ... FOR UPDATE or Redis temporary 10-minute hold lock.
     - Time zone conversions stored strictly as UTC in database; converted in client timezone.

  3. Video Meeting Service (Zoom / Google Meet) [Phase 39]:
     - WebRTC for peer media transmission; WebSocket for signaling (SDP offer/answer exchange).
     - NAT Traversal: STUN (discovers public IP) + TURN (relay fallback when symmetric NAT blocks direct P2P).
     - Selective Forwarding Unit (SFU): Media server forwarding video streams without transcoding,
       scaling meetings beyond P2P 4-person limits up to 500 participants.

  4. Payment Processing System [Phase 40]:
     - Strict Idempotency Keys stored in Redis to prevent double-charging.
     - Webhook ingestion with cryptographic signature verification and Dead Letter Queue retries.
     - Reconciliation Worker: Nightly batch job matching local database ledgers against Stripe/PayPal settlements.

  5. Real-Time Chat System (WhatsApp) [Phase 41]:
     - WebSocket Gateway managing persistent connections mapped in Redis Session Registry.
     - Message flow: Sender -> WS Gateway -> Chat Service -> Cassandra (Message Store) -> Kafka -> Recipient WS Gateway.
     - E2E Encryption: Signal Protocol with double ratchet key derivation.

  6. URL Shortener (Bitly) [Phase 42]:
     - Base62 encoding on unique 64-bit auto-increment or Snowflake IDs.
     - Cache 20% most popular URLs in Redis (80/20 Pareto principle).
     - HTTP 301 (Permanent Redirect - browser caches) vs HTTP 302 (Temporary - server tracks analytics).

  7. Distributed Rate Limiter [Phase 43]:
     - Sliding Window Counter implemented via Redis Lua script to maintain atomic increments.
     - Placed at API Gateway level; returns HTTP 429 with 'Retry-After' header.

  8. Notification Engine (100M alerts/day) [Phase 44]:
     - Decoupled priority topics (OTP vs Promo), worker pools, circuit breakers, and template caching.

  9. File Storage & Drive Service (Google Drive / Dropbox) [Phase 35]:
     - Chunking: Files split into 4MB chunks; deduplicated via SHA-256 hash before S3 storage.
     - Metadata Service: PostgreSQL tracks user folders, permissions, and chunk maps.

  10. News Feed System (Instagram / Twitter / X) [Phase 36]:
      - Fan-Out on Write (Push) for normal users (pushes post ID into follower Redis timelines).
      - Fan-Out on Read (Pull) for celebrities (fetched and merged dynamically at query time).

────────────────────────────────────────────────────────────────────────────────
  11. PRODUCTION CODE IMPLEMENTATIONS: JAVA, PYTHON & NODE.JS
────────────────────────────────────────────────────────────────────────────────

  [Language: Java Spring Boot]
  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // 1. Resilient Microservice Client with Circuit Breaker & Retry        │
  │  package com.enterprise.systemdesign.client;                             │
  │                                                                          │
  │  import io.github.resilience4j.circuitbreaker.annotation.CircuitBreaker;  │
  │  import io.github.resilience4j.retry.annotation.Retry;                   │
  │  import org.springframework.stereotype.Service;                         │
  │  import org.springframework.web.client.RestTemplate;                    │
  │                                                                          │
  │  @Service                                                                │
  │  public class OrderServiceClient {                                       │
  │      private final RestTemplate restTemplate = new RestTemplate();       │
  │                                                                          │
  │      @CircuitBreaker(name = "paymentService", fallbackMethod = "fallback")│
  │      @Retry(name = "paymentService")                                     │
  │      public String executePayment(String orderId, double amount) {       │
  │          return restTemplate.postForObject(                              │
  │              "http://payment-service/api/v1/charge",                     │
  │              new ChargePayload(orderId, amount),                         │
  │              String.class                                                │
  │          );                                                              │
  │      }                                                                   │
  │                                                                          │
  │      public String fallback(String orderId, double amount, Throwable t) {│
  │          return "PAYMENT_FALLBACK_RECORDED";                             │
  │      }                                                                   │
  │      record ChargePayload(String orderId, double amount) {}              │
  │  }                                                                       │
  └──────────────────────────────────────────────────────────────────────────┘

  [Language: Python & FastAPI]
  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // 2. High-Performance Distributed Rate Limiter & Async Worker in Python │
  │  from fastapi import FastAPI, HTTPException, Request                     │
  │  import redis.asyncio as redis                                           │
  │  import time                                                             │
  │                                                                          │
  │  app = FastAPI()                                                         │
  │  r = redis.Redis(host="localhost", port=6379, decode_responses=True)     │
  │                                                                          │
  │  @app.middleware("http")                                                 │
  │  async def rate_limiter_middleware(request: Request, call_next):         │
  │      client_ip = request.client.host                                     │
  │      current_window = int(time.time() // 60)                             │
  │      key = f"rate:{client_ip}:{current_window}"                          │
  │                                                                          │
  │      requests = await r.incr(key)                                        │
  │      if requests == 1:                                                   │
  │          await r.expire(key, 60)                                         │
  │                                                                          │
  │      if requests > 100:                                                  │
  │          raise HTTPException(status_code=429, detail="Too Many Requests")│
  │                                                                          │
  │      return await call_next(request)                                     │
  └──────────────────────────────────────────────────────────────────────────┘

  [Language: Node.js & Express]
  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // 3. Asynchronous Job Dispatcher using BullMQ and Redis                │
  │  const express = require('express');                                     │
  │  const { Queue, Worker } = require('bullmq');                            │
  │                                                                          │
  │  const app = express();                                                  │
  │  app.use(express.json());                                                │
  │                                                                          │
  │  const notificationQueue = new Queue('notifications', {                  │
  │      connection: { host: 'localhost', port: 6379 }                       │
  │  });                                                                     │
  │                                                                          │
  │  // Producer: Accepts API request and returns immediately                │
  │  app.post('/api/v1/notify', async (req, res) => {                        │
  │      const { userId, message, channel } = req.body;                      │
  │      const job = await notificationQueue.add('send_alert', {             │
  │          userId, message, channel                                        │
  │      }, { attempts: 3, backoff: { type: 'exponential', delay: 1000 } }); │
  │      res.status(202).json({ status: 'Accepted', jobId: job.id });        │
  │  });                                                                     │
  │                                                                          │
  │  // Consumer Worker (Runs in isolated worker process)                    │
  │  const worker = new Worker('notifications', async job => {               │
  │      console.log(`Processing notification ${job.id} for ${job.data.userId}`);│
  │      // Executes external push/SMS integration                           │
  │  }, { connection: { host: 'localhost', port: 6379 } });                  │
  │                                                                          │
  │  app.listen(3000, () => console.log('API Gateway running on port 3000'));│
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  12. MODULE 10: INTERVIEW DRILLS, FAILURE MODES & CHECKLIST (PHASES 45 - 55)
────────────────────────────────────────────────────────────────────────────────

  FAILURE SCENARIOS DRILL (PHASE 45):
    - What happens if the Database crashes? Read replicas take over via automated failover
      (e.g. AWS RDS Multi-AZ); write requests queue in Kafka; app returns cached reads from Redis.
    - What happens if Redis crashes? Circuit breaker temporarily routes traffic to DB with strict
      rate limiting, or falls back to local in-memory caffeine cache.
    - What happens if Kafka crashes? Producers buffer events in local disk memory; consumer lag freezes
      temporarily until broker quorum re-elects partition leaders via KRaft.
    - What happens if traffic spikes 100x? Horizontal Pod Autoscalers (HPA) spin up additional container
      replicas; CloudFront caches absorb static edge traffic; rate limiters shed excess load (HTTP 429).

  PERFORMANCE TROUBLESHOOTING DRILL (PHASE 46):
    - API takes 10 seconds: Check APM distributed trace. Isolate whether bottleneck is database lock,
      external third-party synchronous HTTP call, or unindexed slow SQL query.
    - Database CPU hits 100%: Run 'pg_stat_statements' to identify unindexed full table scans;
      terminate blocked locks; add composite index; divert read traffic to replicas.

  FINAL BACKEND & SYSTEM DESIGN CHECKLIST (PHASE 55):
    [x] Networking (DNS, TCP 3-way handshake, TLS 1.3, HTTP/2/3)
    [x] API Design (REST idempotency, cursor pagination, gRPC, WebSockets)
    [x] Auth & Security (JWT rotation, RBAC, bcrypt salting, OWASP)
    [x] Databases (PostgreSQL B+Tree, ACID, Sharding, MongoDB, Cassandra)
    [x] Caching (Redis Cache-Aside, Eviction policies, Stampede prevention)
    [x] Load Balancing (L4 vs L7, Nginx reverse proxy, ALB, Consistent Hashing)
    [x] Event Streaming (Kafka partitions, consumer groups, exactly-once, Outbox)
    [x] Background Work (BullMQ, Celery, Dead Letter Queues, Exponential Jitter)
    [x] Microservices (Saga Pattern, Circuit Breakers, OpenTelemetry tracing)
    [x] High Availability (Active-Active, Multi-AZ failover, CAP Theorem)

================================================================================
  END OF FILE 098B
================================================================================
