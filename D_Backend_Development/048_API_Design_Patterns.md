================================================================================
  FILE 048: API Design Patterns: REST, GraphQL, gRPC & WebSockets
  Section: D - Backend Development
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  Modern distributed architectures rely on distinct API protocols tailored to
  varying network constraints and communication semantics. This document provides
  an architectural deep dive into REST (Representational State Transfer), GraphQL,
  gRPC, WebSockets, and Server-Sent Events (SSE). You will explore Richardson's
  Maturity Model, cursor-based pagination, Protocol Buffers binary serialization,
  HTTP/2 multiplexing, and distributed rate limiting algorithms.

  Prerequisites: Networking fundamentals (OSI Model, TCP/IP, HTTP/1.1 vs HTTP/2).
  What You'll Learn: Protocol selection matrices, schema design, over-fetching vs.
  under-fetching, bidirectional streaming, token bucket rate limiters, and idempotency.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  REST (Representational State Transfer)
    An architectural style based on stateless, client-server communication using
    standard HTTP verbs (GET, POST, PUT, PATCH, DELETE) to manipulate uniform
    resource identifiers (URIs).

  Richardson Maturity Model
    A heuristic classification framework for RESTful APIs:
    - Level 0: The Swamp of POX (single URI, single HTTP POST method, e.g. SOAP).
    - Level 1: Resources (distinct URIs for individual resources, e.g. /orders/1).
    - Level 2: HTTP Verbs (proper use of GET, POST, PUT, DELETE and HTTP status codes).
    - Level 3: Hypermedia Controls (HATEOAS - response contains discoverable links).

  GraphQL
    A query language and server-side runtime created by Meta that allows clients
    to define the exact structure of data required, preventing over-fetching and
    under-fetching via a strongly-typed schema.

  gRPC
    A high-performance, open-source Remote Procedure Call framework developed by
    Google that runs on HTTP/2 transport and uses binary Protocol Buffers (Protobuf)
    for contract definition and ultra-compact serialization.

  WebSocket
    A persistent, bidirectional, full-duplex TCP protocol initiated via an HTTP
    'Upgrade' handshake, enabling real-time microsecond messaging between client and server.

  Server-Sent Events (SSE)
    A lightweight, unidirectional protocol built over standard HTTP where the server
    pushes a continuous stream of text events (text/event-stream) to the client.

  Cursor-Based Pagination
    A pagination technique using an opaque unique pointer (e.g. base64-encoded
    created_at timestamp + UUID) rather than LIMIT/OFFSET, eliminating duplicate/skipped
    records and executing in O(1) database index seek time.

  Idempotency
    A property of an HTTP method where making multiple identical requests yields
    the exact same server state as a single request (GET, PUT, DELETE are idempotent;
    POST is not).

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  API PROTOCOL COMPARISON & SELECTION MATRIX                             │
  │                                                                         │
  │  Protocol    Transport  Serialization   Directionality    Primary Use   │
  │  ─────────────────────────────────────────────────────────────────────  │
  │  REST        HTTP/1.1   JSON / XML      Req / Res         Public APIs   │
  │  GraphQL     HTTP/1.1+2 JSON            Req / Res + Sub   Complex Frontends│
  │  gRPC        HTTP/2     Binary Protobuf Bidirectional     Microservices │
  │  WebSocket   TCP        Binary / Text   Full-Duplex       Real-Time Chat│
  │  SSE         HTTP/1.1+2 UTF-8 Text      Server -> Client  Live Feeds/LLM│
  └─────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  OFFSET PAGINATION (SLOW O(N)) VS. CURSOR PAGINATION (FAST O(1))        │
  │                                                                         │
  │  [ OFFSET PAGINATION ]                                                  │
  │  Query: SELECT * FROM items ORDER BY id LIMIT 20 OFFSET 500000;         │
  │  DB Action: Scans and discards 500,000 index entries before returning 20!│
  │  Vulnerability: If item inserted between pages, user sees duplicates!   │
  │                                                                         │
  │  [ CURSOR PAGINATION ]                                                  │
  │  Query: SELECT * FROM items WHERE id > 499980 ORDER BY id LIMIT 20;     │
  │  DB Action: Direct B+Tree Index Seek to key 499980 and reads 20 rows!   │
  │  Performance: Constant O(log N) search time regardless of dataset size! │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  4. EXPLANATION & THEORY
────────────────────────────────────────────────────────────────────────────────

  Why gRPC Outperforms REST for Microservices:
  1. Binary Payload vs Text: Protocol Buffers encode integers with variable-length
     varints and field tags instead of verbose string keys ("productId": 12345),
     cutting payload size by 60-80%.
  2. HTTP/2 Multiplexing: Multiple concurrent gRPC calls travel across a single
     persistent TCP connection without Head-of-Line blocking.
  3. Strong Code Generation: .proto files compile directly into type-safe client
     stubs in Java, Go, Python, and C++, eliminating manual client SDK authoring.

  When to Use WebSockets vs Server-Sent Events (SSE):
  - Use WebSockets if the client must also send rapid, continuous messages upstream
    (e.g. multiplayer gaming, collaborative canvas editing like Figma, financial trading).
  - Use SSE if communication is predominantly downstream (e.g. ChatGPT token
    streaming, live crypto ticker, stock price dashboards). SSE handles automatic
    reconnection, polyfills through corporate firewalls, and runs over standard HTTP/2.

────────────────────────────────────────────────────────────────────────────────
  5. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: Protobuf & Java]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // 1. gRPC Protocol Buffer Definition (order_service.proto)             │
  │                                                                          │
  │  syntax = "proto3";                                                      │
  │  package orders;                                                         │
  │  option java_package = "com.enterprise.orders.grpc";                    │
  │                                                                          │
  │  service OrderRpcService {                                               │
  │    rpc GetOrder (OrderLookupRequest) returns (OrderModel);               │
  │    rpc StreamOrderUpdates (OrderLookupRequest) returns (stream OrderStatusUpdate);                                                               │
  │  }                                                                       │
  │                                                                          │
  │  message OrderLookupRequest {                                            │
  │    string order_id = 1;                                                  │
  │  }                                                                       │
  │                                                                          │
  │  message OrderModel {                                                    │
  │    string order_id = 1;                                                  │
  │    string customer_id = 2;                                               │
  │    double total_price = 3;                                               │
  │    string status = 4;                                                    │
  │  }                                                                       │
  │                                                                          │
  │  message OrderStatusUpdate {                                             │
  │    string status = 1;                                                    │
  │    int64 timestamp = 2;                                                  │
  │  }                                                                       │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: Java]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Production-Ready Token Bucket Distributed Rate Limiter               │
  │                                                                          │
  │  package com.enterprise.library.ratelimiter;                             │
  │                                                                          │
  │  import java.time.Instant;                                               │
  │  import java.util.concurrent.ConcurrentHashMap;                          │
  │                                                                          │
  │  public class TokenBucketRateLimiter {                                   │
  │      private final long capacity;       // Max tokens bucket can hold    │
  │      private final double refillRate;   // Tokens added per second       │
  │      private final ConcurrentHashMap<String, Bucket> clientBuckets = new ConcurrentHashMap<>();                                                  │
  │                                                                          │
  │      public TokenBucketRateLimiter(long capacity, double refillRate) {   │
  │          this.capacity = capacity;                                       │
  │          this.refillRate = refillRate;                                   │
  │      }                                                                   │
  │                                                                          │
  │      private static class Bucket {                                       │
  │          double tokens;                                                  │
  │          long lastRefillTimestamp;                                       │
  │          Bucket(double tokens, long timestamp) {                         │
  │              this.tokens = tokens;                                       │
  │              this.lastRefillTimestamp = timestamp;                       │
  │          }                                                               │
  │      }                                                                   │
  │                                                                          │
  │      public synchronized boolean allowRequest(String clientId, int tokensRequested) {                                                            │
  │          long now = Instant.now().toEpochMilli();                        │
  │          Bucket bucket = clientBuckets.computeIfAbsent(clientId,         │
  │              k -> new Bucket(capacity, now));                            │
  │                                                                          │
  │          // Calculate tokens to refill based on elapsed time             │
  │          double elapsedSeconds = (now - bucket.lastRefillTimestamp) / 1000.0;                                                                    │
  │          bucket.tokens = Math.min(capacity, bucket.tokens + (elapsedSeconds * refillRate));                                                       │
  │          bucket.lastRefillTimestamp = now;                               │
  │                                                                          │
  │          if (bucket.tokens >= tokensRequested) {                         │
  │              bucket.tokens -= tokensRequested;                           │
  │              return true;  // Request allowed                            │
  │          }                                                               │
  │          return false;     // HTTP 429 Too Many Requests                 │
  │      }                                                                   │
  │  }                                                                       │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  7. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: Why is PUT considered idempotent while POST is not?

  ANSWER:
    PUT defines replacement semantics: sending 'PUT /users/42 {"name": "Alice"}'
    ten times consecutively results in the exact same resource state where user 42
    has name "Alice". POST defines creation/append semantics: sending
    'POST /users {"name": "Alice"}' ten times creates ten distinct users with
    ten new unique IDs.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: How do you handle idempotency for non-idempotent POST operations (e.g. payment processing)?

  ANSWER:
    Clients generate a unique 'Idempotency-Key' UUID header with the request.
    The server checks a fast in-memory store (Redis):
    1. If key does not exist: Store key with a PENDING state, execute payment,
       cache final response, and return.
    2. If key exists with PENDING: Return HTTP 409 Conflict (request in progress).
    3. If key exists with COMPLETED: Immediately return cached response without
       re-charging the credit card.

────────────────────────────────────────────────────────────────────────────────
  8. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: The Broken Mobile Feed Offset Bug
  Users report seeing duplicate posts while scrolling infinite-scroll newsfeeds
  powered by: 'GET /feed?page=3&limit=20'. Why does this happen exclusively during
  peak posting hours?

  SOLUTION:
    The API uses OFFSET pagination (OFFSET = page * limit). While the user was
    browsing page 2, 5 new posts were published at the top of the feed (index 0).
    All existing posts shifted down by 5 slots. When page 3 requested OFFSET 40,
    the last 5 posts from page 2 were re-read, appearing as duplicates!
    Fix: Switch to Cursor-Based Pagination ('GET /feed?cursor=post_9874&limit=20').

────────────────────────────────────────────────────────────────────────────────
  9. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  1. Bandwidth Economy: Netflix and Uber slashed inter-microservice networking
     costs by migrating internal REST JSON traffic to gRPC Protobuf, achieving
     sub-millisecond latencies and eliminating JSON serialization CPU overhead.
  2. Resilient Real-Time Feeds: Production LLM applications (ChatGPT) rely on SSE
     to stream tokens progressively to the client as they are generated, rather
     than forcing the user to endure a 15-second blank screen before receiving
     the complete response.

────────────────────────────────────────────────────────────────────────────────
  10. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

  -> File 006: Networking Fundamentals (OSI Model, TCP Handshake, HTTP/2)
  -> File 032: Redis (Implementing distributed rate limiters and pub/sub)
  -> File 037: Express.js (REST API middleware architectures)
  -> File 094: Design URL Shortener & Rate Limiter (System design integration)

================================================================================
  END OF FILE 048
================================================================================
