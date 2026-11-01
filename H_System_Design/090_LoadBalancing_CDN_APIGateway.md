================================================================================
  FILE 090: LOAD BALANCING, CDN, & API GATEWAY
  Section: H - System Design at Scale
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  Load Balancing, CDN, & API Gateway covers the critical ingress components of modern web architectures. Prerequisites include networking basics (TCP/IP, HTTP). You'll learn how Load Balancers distribute traffic, how CDNs accelerate content delivery globally, and how API Gateways manage microservice routing and security.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  LOAD BALANCING
    Distributing incoming network traffic across a group of backend servers.
    - L4 (Transport): Routes based on IP and Port (TCP/UDP). Very fast, no payload inspection.
    - L7 (Application): Routes based on HTTP headers, cookies, URL paths.

  LB ALGORITHMS
    - Round Robin: Sequential distribution.
    - Weighted Round Robin: Sequential, but accounts for server capacity.
    - Least Connections: Sends traffic to the server with the fewest active connections.
    - Consistent Hashing: Maps requests to servers so that adding/removing servers only remaps a small fraction of keys.

  HEALTH CHECKS
    - Active: LB pings the server (e.g., HTTP GET /health).
    - Passive: LB observes traffic and removes servers returning 5xx errors.

  CDN (CONTENT DELIVERY NETWORK)
    A geographically distributed network of proxy servers that cache static/dynamic content closer to end-users (Edge Locations).

  API GATEWAY
    A reverse proxy acting as a single entry point for APIs. Handles routing, auth, rate limiting, and request transformation.

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  MULTI-TIER ARCHITECTURE                                                │
  │                                                                         │
  │  [ Clients ] ---> [ Route 53 (DNS LB) ] ---> [ CloudFront CDN ]         │
  │                                                    | (Cache Miss)       │
  │                                                    v                    │
  │                                           [ API Gateway (L7) ]          │
  │                                              /      |      \            │
  │                                            [ Auth / Rate Limiter ]      │
  │                                            /        |        \          │
  │                                       [ Microservice A, B, C ]          │
  │                                         (Internal L4 LBs)               │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  CDN EDGE CACHING FLOW                                                  │
  │                                                                         │
  │  User (Tokyo) -> [CDN Edge Tokyo] --(Cache Hit)--> Returns Asset        │
  │                        |                                                │
  │                   (Cache Miss)                                          │
  │                        v                                                │
  │                  [Origin Server (US-East)] -> Fetches Asset -> Caches at Edge -> Returns to User│
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  4. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: nginx]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // NGINX L7 Load Balancer configuration demo                            │
  │                                                                          │
  │  http {                                                                  │
  │      # Define a group of backend servers                                 │
  │      upstream backend_servers {                                          │
  │          least_conn; # Use least connections algorithm                   │
  │          server 10.0.0.1:8080 weight=3;                                  │
  │          server 10.0.0.2:8080;                                           │
  │          server 10.0.0.3:8080 backup; # Only used if others fail         │
  │      }                                                                   │
  │                                                                          │
  │      server {                                                            │
  │          listen 80;                                                      │
  │          server_name api.example.com;                                    │
  │                                                                          │
  │          location / {                                                    │
  │              proxy_pass http://backend_servers;                          │
  │              proxy_set_header Host $host;                                │
  │              proxy_set_header X-Real-IP $remote_addr;                    │
  │                                                                          │
  │              # Health check timeout                                      │
  │              proxy_connect_timeout 2s;                                   │
  │          }                                                               │
  │      }                                                                   │
  │  }                                                                       │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: javascript]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │                                                                          │
  │  // Express.js API Gateway with Rate Limiting and Circuit Breaker        │
  │  const express = require('express');                                     │
  │  const { createProxyMiddleware } = require('http-proxy-middleware');     │
  │  const rateLimit = require('express-rate-limit');                        │
  │  const CircuitBreaker = require('opossum'); // Standard circuit breaker  │
  │                                                                          │
  │  const app = express();                                                  │
  │                                                                          │
  │  // 1. Rate Limiting: Max 100 requests per 15 minutes                    │
  │  const limiter = rateLimit({                                             │
  │    windowMs: 15 * 60 * 1000,                                             │
  │    max: 100,                                                             │
  │    message: 'Too many requests from this IP, please try again later.'    │
  │  });                                                                     │
  │  app.use(limiter);                                                       │
  │                                                                          │
  │  // 2. Mock Circuit Breaker wrapped proxy execution                      │
  │  const proxyOptions = {                                                  │
  │      target: 'http://internal-microservice:8080',                        │
  │      changeOrigin: true,                                                 │
  │      pathRewrite: {'^/api' : ''}                                         │
  │  };                                                                      │
  │                                                                          │
  │  const proxyRequest = (req, res, next) => {                              │
  │      return new Promise((resolve, reject) => {                           │
  │          // Execute real proxy middleware...                             │
  │          createProxyMiddleware(proxyOptions)(req, res, next);            │
  │          resolve();                                                      │
  │      });                                                                 │
  │  };                                                                      │
  │                                                                          │
  │  const breaker = new CircuitBreaker(proxyRequest, {                      │
  │      timeout: 3000, // If request takes >3s, trigger failure             │
  │      errorThresholdPercentage: 50, // When 50% fail, open breaker        │
  │      resetTimeout: 10000 // Try again in 10s                             │
  │  });                                                                     │
  │                                                                          │
  │  breaker.fallback(() => ({ error: "Service currently unavailable. Circuit open." }));│
  │                                                                          │
  │  // 3. Routing                                                           │
  │  app.use('/api', (req, res, next) => {                                   │
  │      breaker.fire(req, res, next).catch(err => {                         │
  │          res.status(503).json(err);                                      │
  │      });                                                                 │
  │  });                                                                     │
  │                                                                          │
  │  app.listen(80, () => console.log('API Gateway running on port 80'));    │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: What is the difference between an L4 and L7 Load Balancer?

  ANSWER:
    L4 operates at the transport layer (IP/Port), routing packets without inspecting HTTP bodies, making it ultra-fast. L7 operates at the application layer, inspecting HTTP headers, cookies, and URLs for smart routing.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: What is Consistent Hashing and why is it useful?

  ANSWER:
    It maps keys and servers on a hash ring. When a server is added/removed, only 1/N keys are remapped, minimizing cache misses compared to hash(key) % N.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: How does a CDN work for dynamic content?

  ANSWER:
    Dynamic Site Acceleration (DSA) uses optimized, persistent TCP connections between the edge and origin, route optimization, and edge-computing (Lambda@Edge) to speed up dynamic requests.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: What is the difference between Pull and Push CDN?

  ANSWER:
    Pull CDN automatically fetches content from the origin upon a cache miss. Push CDN requires the developer to actively upload (push) assets to the CDN servers.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: Why use an API Gateway instead of direct client-to-microservice communication?

  ANSWER:
    Consolidates cross-cutting concerns (auth, rate limiting, logging), reduces client round-trips, prevents exposing internal network structures, and translates protocols (e.g., HTTP to gRPC).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: What is a reverse proxy?

  ANSWER:
    A server that sits in front of backend servers and forwards client requests to them (e.g., Nginx, Envoy).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q7: How do you handle CDN cache invalidation?

  ANSWER:
    Use versioned URLs (e.g., app-v2.js), TTLs, or explicitly call CDN invalidate APIs (which can be slow and expensive).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q8: What is a Circuit Breaker in an API Gateway?

  ANSWER:
    A pattern that detects systemic failures and temporarily halts requests to a failing backend, preventing cascading failures and giving the backend time to recover.

────────────────────────────────────────────────────────────────────────────────
  7. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: Riddle 1

  "I stand in the middle, blind to your messages, yet perfectly capable of directing your mail to the right house based on the envelope. What am I?"

  SOLUTION:
    Problem: 
    Fix: Layer 4 (Transport) Load Balancer.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 2: Riddle 2

  # What is the flaw?
  upstream backend {
      server 10.0.0.1;
      server 10.0.0.2;
  }
  location / {
      proxy_pass http://backend;
  }

  SOLUTION:
    Problem: 
    Fix: There are no health checks configured. If 10.0.0.1 goes down, Nginx will still blindly route 50% of traffic to it, resulting in 502 Bad Gateway errors for clients.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 3: Riddle 3

  A developer sets Cache-Control: max-age=31536000 for index.html on a CDN.

  SOLUTION:
    Problem: 
    Fix: index.html is the entry point. If cached for a year, users will never see updates. Root HTML files should have no-cache or a very short TTL, while static assets (JS/CSS) should be fingerprinted (main.123.js) and cached for a year.

────────────────────────────────────────────────────────────────────────────────
  8. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  Without load balancers, single servers crash under heavy traffic. Without CDNs, users in Australia wait 500ms to load images from a server in New York. Without API Gateways, every single microservice would have to independently implement JWT validation and rate limiting, creating massive code duplication and security risks.

────────────────────────────────────────────────────────────────────────────────
  9. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

  -> File 091: Caching at Scale (Caching strategies)
  -> File 094: Design URLShortener RateLimiter (Rate limiting algorithms inside API Gateways)
  -> File 089: SystemDesign Fundamentals (Horizontal scalability concepts)

================================================================================
  END OF FILE 090
================================================================================
