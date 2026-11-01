================================================================================
  FILE 098: OBSERVABILITY & MONITORING
  Section: H - System Design at Scale
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  Observability & Monitoring explores how to maintain, debug, and ensure the reliability of complex distributed systems. Prerequisites include basic microservice architecture. You will learn the Three Pillars of Observability, how to define SLOs and SLAs, and how to track a single request across a dozen microservices using Distributed Tracing.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  THREE PILLARS OF OBSERVABILITY
    - Metrics: Numeric representations of data measured over time (e.g., CPU %, QPS).
    - Logs: Immutable timestamped records of discrete events (e.g., "User 123 logged in").
    - Traces: A representation of a series of causally related distributed events that encode the end-to-end request flow.

  METRICS TYPES
    - Counter: Only goes up (e.g., total HTTP requests).
    - Gauge: Can go up and down (e.g., current active users, memory usage).
    - Histogram: Samples observations and counts them in buckets (e.g., latency p99, p95).

  FOUR GOLDEN SIGNALS (GOOGLE SRE)
    Latency, Traffic, Errors, Saturation.

  SERVICE LEVELS
    - SLI (Indicator): The actual metric (e.g., 99.95% of requests succeeded).
    - SLO (Objective): The internal goal (e.g., We aim for 99.9% success rate).
    - SLA (Agreement): The legal contract (e.g., We refund clients if success rate < 99.9%).

  DISTRIBUTED TRACING
    Uses a Trace ID passed in HTTP headers to stitch together logs across microservices. Consists of a root Span and child Spans.

  CHAOS ENGINEERING
    Intentionally injecting failures into a production system to test resilience (e.g., Netflix Chaos Monkey).

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  DISTRIBUTED TRACING (SPAN TREE)                                        │
  │                                                                         │
  │  [ Trace ID: 9a3b... ]                                                  │
  │  Span 1: [ API Gateway ] (200ms)                                        │
  │     |                                                                   │
  │     +-- Span 2: [ Auth Service ] (50ms)                                 │
  │     |                                                                   │
  │     +-- Span 3: [ User Service ] (140ms)                                │
  │            |                                                            │
  │            +-- Span 4: [ Redis Cache ] (10ms)                           │
  │            |                                                            │
  │            +-- Span 5: [ PostgreSQL DB ] (120ms) -> **Bottleneck!**     │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  OBSERVABILITY STACK                                                    │
  │                                                                         │
  │  [ App Services ] -> (Prometheus Client) -> [ Prometheus (Metrics) ] -> [ Grafana (Dashboards) ]│
  │                   -> (JSON Logs to stdout) -> [ Fluentd ] -> [ Elasticsearch / Loki ]│
  │                   -> (OpenTelemetry API) -> [ Jaeger / Zipkin (Tracing) ]│
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  4. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: javascript]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Express.js with Prometheus Metrics                                   │
  │  const express = require('express');                                     │
  │  const promClient = require('prom-client');                              │
  │  const app = express();                                                  │
  │                                                                          │
  │  // 1. Setup default metrics (CPU, memory)                               │
  │  promClient.collectDefaultMetrics();                                     │
  │                                                                          │
  │  // 2. Custom Counter for HTTP Requests                                  │
  │  const httpRequestCounter = new promClient.Counter({                     │
  │    name: 'http_requests_total',                                          │
  │    help: 'Total number of HTTP requests',                                │
  │    labelNames: ['method', 'route', 'status']                             │
  │  });                                                                     │
  │                                                                          │
  │  // Middleware to track requests                                         │
  │  app.use((req, res, next) => {                                           │
  │      res.on('finish', () => {                                            │
  │          httpRequestCounter.labels(req.method, req.path, res.statusCode).inc();│
  │      });                                                                 │
  │      next();                                                             │
  │  });                                                                     │
  │                                                                          │
  │  // 3. Expose /metrics endpoint for Prometheus to scrape                 │
  │  app.get('/metrics', async (req, res) => {                               │
  │      res.set('Content-Type', promClient.register.contentType);           │
  │      res.end(await promClient.register.metrics());                       │
  │  });                                                                     │
  │                                                                          │
  │  app.get('/api/data', (req, res) => res.send('OK'));                     │
  │  app.listen(3000);                                                       │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: yaml]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │                                                                          │
  │  # Kubernetes Health Checks (Liveness and Readiness Probes)              │
  │  apiVersion: v1                                                          │
  │  kind: Pod                                                               │
  │  metadata:                                                               │
  │    name: user-service                                                    │
  │  spec:                                                                   │
  │    containers:                                                           │
  │    - name: user-service-app                                              │
  │      image: my-registry/user-service:v1                                  │
  │      ports:                                                              │
  │      - containerPort: 8080                                               │
  │                                                                          │
  │      # Liveness: Is the app dead? (If it fails, K8s restarts the pod)    │
  │      livenessProbe:                                                      │
  │        httpGet:                                                          │
  │          path: /health/liveness                                          │
  │          port: 8080                                                      │
  │        initialDelaySeconds: 10                                           │
  │        periodSeconds: 15                                                 │
  │                                                                          │
  │      # Readiness: Is the app ready to receive traffic?                   │
  │      # (If it fails, K8s removes it from Load Balancer, but doesn't restart it)│
  │      readinessProbe:                                                     │
  │        httpGet:                                                          │
  │          path: /health/readiness                                         │
  │          port: 8080                                                      │
  │        initialDelaySeconds: 5                                            │
  │        periodSeconds: 5                                                  │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: What are the Three Pillars of Observability?

  ANSWER:
    Metrics (aggregate data, alerting), Logs (high-fidelity debugging context), Traces (request flow across boundaries).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: Explain Push vs Pull monitoring.

  ANSWER:
    Push (Datadog, StatsD): Apps push metrics to the server. Pull (Prometheus): The server scrapes a /metrics endpoint on the apps. Pull is easier to secure and doesn't overwhelm the backend (it controls the scraping rate).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: What is the difference between an SLO and an SLA?

  ANSWER:
    SLO is the engineering team's target (e.g., 99.95%). SLA is the legal/business contract with the customer (e.g., 99.9%). The SLO is always stricter to act as a buffer.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: How do you track a request across 5 microservices?

  ANSWER:
    Using Distributed Tracing (OpenTelemetry/Jaeger). The API Gateway generates a unique X-Trace-Id header and passes it to downstream services. Each service logs its own Span-Id tied to the parent Trace-Id.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: What are the Google SRE Four Golden Signals?

  ANSWER:
    Latency (time to serve), Traffic (demand/QPS), Errors (rate of failures), Saturation (system capacity fullness).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: What is Alert Fatigue?

  ANSWER:
    When alerting rules are too sensitive, developers are flooded with non-actionable pages (e.g., CPU spiked to 80% for 1 second). Developers start ignoring alerts, missing real outages. Fix by alerting on SLO burn rate, not raw metrics.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q7: What's the difference between Liveness and Readiness probes in Kubernetes?

  ANSWER:
    Liveness failure = Restart the pod (e.g., deadlock). Readiness failure = Stop sending traffic to it (e.g., DB connection dropped, warming cache).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q8: Why not just log everything to debug?

  ANSWER:
    Logs are expensive to store and index at scale (Elasticsearch bills add up). You cannot easily write alerts on complex log aggregations compared to time-series Metrics.

────────────────────────────────────────────────────────────────────────────────
  7. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: Riddle 1

  "I am a tree whose leaves are milliseconds, whose roots are gateways, and whose branches cross the network. What am I?"

  SOLUTION:
    Problem: 
    Fix: A Distributed Trace.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 2: Riddle 2

  // Alert Rule Configuration
  if (cpu_usage > 90%):
      send_page_to_oncall()

  SOLUTION:
    Problem: 
    Fix: This causes Alert Fatigue. High CPU isn't a problem if latency and error rates are fine (it means you are using hardware efficiently). You should alert on Symptoms (e.g., High Latency) rather than Causes (e.g., High CPU).

────────────────────────────────────────────────────────────────────────────────
  8. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  When a microservice architecture crashes at 3:00 AM, you cannot SSH into machines to tail logs. Without Distributed Tracing, a 500 Error in the checkout flow is a mystery. Proper observability turns a chaotic multi-hour incident response into a targeted 10-minute fix.

────────────────────────────────────────────────────────────────────────────────
  9. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

  -> File 090: Load Balancing, CDN, & API Gateway (API Gateway as the Trace Root)
  -> File 089: SystemDesign Fundamentals (SLA calculation and Nines of Availability)

================================================================================
  END OF FILE 098
================================================================================
