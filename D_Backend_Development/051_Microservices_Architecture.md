================================================================================
  FILE 051: Microservices Architecture & Distributed Systems Patterns
  Section: D - Backend Development
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  Transitioning from monolithic applications to microservices solves organizational
  scaling bottlenecks but introduces severe distributed systems challenges: partial
  network failures, data consistency divergences, and cascading service outages.
  This document provides an exhaustive architectural reference covering Domain-Driven
  Design (DDD) bounded contexts, API Gateways, Circuit Breaker state machines
  (Resilience4j), distributed tracing (OpenTelemetry), and eventual consistency via
  the Saga Pattern (Choreography vs. Orchestration).

  Prerequisites: File 048 (API Design Patterns), File 049 (Kafka Event Streaming).
  What You'll Learn: Strangler Fig migration, Circuit Breaker states (Closed, Open,
  Half-Open), correlation IDs, the Dual-Write problem, Outbox Pattern, and CQRS.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  Bounded Context (DDD)
    A central pattern in Domain-Driven Design defining explicit logical boundaries
    within which a domain model applies and terms maintain strict, unambiguous meanings.

  Strangler Fig Pattern
    An incremental migration strategy where new microservice features are built
    around a legacy monolith, gradually intercepting and replacing legacy routes
    until the old monolith can be safely decommissioned.

  API Gateway
    A single reverse-proxy entry point for client applications that handles request
    routing, SSL termination, authentication, global rate limiting, and response aggregation.

  Circuit Breaker Pattern
    A fail-fast stability pattern that monitors remote service calls. When failures
    cross a threshold, the circuit trips ("Opens"), immediately failing subsequent
    calls to protect downstream services from cascading collapse.
    - CLOSED: Normal operation; requests pass through.
    - OPEN: Calls fail immediately; fallback logic executes without hitting network.
    - HALF-OPEN: Allows trial requests to evaluate if the downstream service recovered.

  Saga Pattern
    A sequence of local database transactions coordinating distributed multi-service
    workflows without blocking distributed two-phase commits (2PC). Each transaction
    updates data in a single service and publishes an event; if a step fails, the
    Saga executes compensating transactions to undo preceding changes.

  Transactional Outbox Pattern
    A pattern ensuring atomic database mutation and event publishing by saving
    events into a local database table ('outbox') in the same ACID transaction
    as the business entity, which is subsequently read and published to Kafka
    by a Change Data Capture (CDC) worker.

  Distributed Tracing
    A telemetry methodology tracing a request across dozens of microservices by
    propagating a unique 'Trace ID' and hierarchical 'Span IDs' through HTTP/gRPC headers.

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  ENTERPRISE MICROSERVICES ARCHITECTURE TOPOLOGY                         │
  │                                                                         │
  │  [ Web / Mobile Clients ]                                               │
  │              │                                                          │
  │              v                                                          │
  │  +───────────────────────────────────────────────────────────────────+  │
  │  |   API Gateway (Kong / Envoy / AWS API Gateway)                    |  │
  │  |   - JWT Validation   - Rate Limiting   - Route Forwarding         |  │
  │  +───────┬───────────────────────────┬───────────────────────────┬───+  │
  │          │ Sync gRPC                 │ Sync gRPC                 │      │
  │          v                           v                           v      │
  │  +───────────────────+       +───────────────────+       +───────────+  │
  │  |  Order Service    |       |  Payment Service  |       | Inventory |  │
  │  |  (PostgreSQL DB)  |       |  (PostgreSQL DB)  |       | (Mongo DB)|  │
  │  +─────────┬─────────+       +─────────┬─────────+       +─────┬─────+  │
  │            │ Event Emit                │ Event Emit            │        │
  │            +─────────────────────┬─────+───────────────────────+        │
  │                                  v                                      │
  │  +───────────────────────────────────────────────────────────────────+  │
  │  |   Event Backbone (Apache Kafka Cluster)                           |  │
  │  |   Topics: [orders-created] [payment-charged] [inventory-reserved] |  │
  │  +───────────────────────────────────────────────────────────────────+  │
  └─────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  RESILIENCE4J CIRCUIT BREAKER STATE MACHINE                             │
  │                                                                         │
  │            +--------------------------------------------+               │
  │            |                                            |               │
  │            v                                            |               │
  │     +──────────────+      Error Rate > 50%       +────────────+         │
  │     |    CLOSED    | ──────────────────────────> |    OPEN    |         │
  │     | (Calls Pass) |                             | (Fail-Fast)|         │
  │     +──────────────+                             +─────┬──────+         │
  │            ^                                           |                │
  │            | Success Rate                              | Wait Duration  │
  │            | > 80%                                     | Elapsed (10s)  │
  │            |             +─────────────────+           |                │
  │            +──────────── |    HALF-OPEN    | <─────────+                │
  │                          | (Trial Requests)|                            │
  │                          +─────────────────+                            │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  4. EXPLANATION & THEORY
────────────────────────────────────────────────────────────────────────────────

  Why Two-Phase Commit (2PC) Fails in Microservices:
  Distributed ACID transactions using 2PC require coordinator locks on database
  rows across multiple microservices. Under high network latency or node crashes,
  locks are held indefinitely, destroying system throughput and causing widespread
  deadlocks (CAP Theorem: Consistency chosen over Availability). Modern microservices
  embrace Eventual Consistency via the Saga Pattern.

  Saga Choreography vs. Orchestration:
  - Choreography: Services listen to Kafka events and autonomously decide when to
    execute their local transaction (good for simple 2-3 step workflows; hard to track).
  - Orchestration: A centralized Orchestrator service (e.g. Temporal, Camunda,
    AWS Step Functions) tells participants which transaction to execute via command
    messages, keeping workflow logic centralized and observable.

────────────────────────────────────────────────────────────────────────────────
  5. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: Java & Resilience4j]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Declarative Resilience4j Circuit Breaker in Spring Boot              │
  │                                                                          │
  │  package com.enterprise.library.client;                                  │
  │                                                                          │
  │  import io.github.resilience4j.circuitbreaker.annotation.CircuitBreaker;  │
  │  import io.github.resilience4j.retry.annotation.Retry;                   │
  │  import org.springframework.stereotype.Service;                         │
  │  import org.springframework.web.client.RestTemplate;                    │
  │                                                                          │
  │  @Service                                                                │
  │  public class PaymentServiceClient {                                     │
  │      private final RestTemplate restTemplate = new RestTemplate();       │
  │                                                                          │
  │      @CircuitBreaker(name = "paymentService", fallbackMethod = "paymentFallback")                                                               │
  │      @Retry(name = "paymentService")                                     │
  │      public String processPayment(String orderId, double amount) {       │
  │          // Remote HTTP call to downstream Payment Microservice          │
  │          return restTemplate.postForObject(                              │
  │              "https://payment.internal.service/charge",                  │
  │              new ChargeRequest(orderId, amount),                         │
  │              String.class                                                │
  │          );                                                              │
  │      }                                                                   │
  │                                                                          │
  │      // Fallback method executed when Circuit is OPEN or call times out  │
  │      public String paymentFallback(String orderId, double amount, Throwable t) {                                                                │
  │          System.err.println("Payment service unavailable: " + t.getMessage());                                                                  │
  │          return "PAYMENT_QUEUED_FOR_OFFLINE_PROCESSING";                 │
  │      }                                                                   │
  │                                                                          │
  │      record ChargeRequest(String orderId, double amount) {}              │
  │  }                                                                       │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: Java]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Transactional Outbox Pattern to Prevent Dual-Write Inconsistencies   │
  │                                                                          │
  │  package com.enterprise.library.orders;                                  │
  │                                                                          │
  │  import jakarta.persistence.*;                                           │
  │  import org.springframework.stereotype.Service;                         │
  │  import org.springframework.transaction.annotation.Transactional;       │
  │  import java.time.Instant;                                               │
  │  import java.util.UUID;                                                  │
  │                                                                          │
  │  @Entity                                                                 │
  │  @Table(name = "outbox_events")                                          │
  │  public class OutboxEvent {                                              │
  │      @Id                                                                 │
  │      private String id = UUID.randomUUID().toString();                   │
  │      private String aggregateType = "ORDER";                             │
  │      private String aggregateId;                                         │
  │      private String eventType = "ORDER_CREATED";                         │
  │      @Column(columnDefinition = "TEXT")                                  │
  │      private String payloadJson;                                         │
  │      private Instant createdAt = Instant.now();                          │
  │      private boolean published = false;                                  │
  │      // Constructors, Getters, Setters                                   │
  │  }                                                                       │
  │                                                                          │
  │  @Service                                                                │
  │  public class OrderPlacementService {                                    │
  │      private final OrderRepository orderRepo;                            │
  │      private final OutboxRepository outboxRepo;                          │
  │                                                                          │
  │      public OrderPlacementService(OrderRepository o, OutboxRepository ob){│
  │          this.orderRepo = o;                                             │
  │          this.outboxRepo = ob;                                           │
  │      }                                                                   │
  │                                                                          │
  │      // ATOMIC: Both order and outbox event write in EXACT SAME SQL TX!  │
  │      @Transactional                                                      │
  │      public String placeOrder(OrderEntity order) {                       │
  │          OrderEntity saved = orderRepo.save(order);                      │
  │                                                                          │
  │          // Save event locally; CDC worker (Debezium) publishes to Kafka!│
  │          OutboxEvent event = new OutboxEvent();                          │
  │          event.setAggregateId(saved.getId());                            │
  │          event.setPayloadJson("{\"orderId\":\"" + saved.getId() + "\"}");│
  │          outboxRepo.save(event);                                         │
  │                                                                          │
  │          return saved.getId();                                           │
  │      }                                                                   │
  │  }                                                                       │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  7. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: What is the "Dual-Write" problem in distributed systems?

  ANSWER:
    The Dual-Write problem occurs when a microservice updates its local relational
    database and subsequently publishes an event to Apache Kafka. Because these
    two operations involve disparate distributed storage systems, there is no
    global ACID guarantee. If the database update succeeds but the app crashes
    before the Kafka write finishes, data is inconsistent. If Kafka is called
    first and the DB commit fails, consumers process phantom events.
    Fix: The Transactional Outbox Pattern with Change Data Capture (Debezium).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: What is the difference between Service Discovery and an API Gateway?

  ANSWER:
    Service Discovery (Kubernetes CoreDNS, Netflix Eureka) is a dynamic registry
    tracking the fluctuating IP addresses and ports of ephemeral microservice
    instances. An API Gateway is a client-facing reverse proxy that routes external
    traffic, terminates SSL, validates authentication tokens, and invokes service
    discovery to find the healthy target instance.

────────────────────────────────────────────────────────────────────────────────
  8. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: The Cascading Thread Starvation Avalanche
  Service A calls Service B with a 30-second HTTP timeout. Service B's database
  locks up, causing Service B responses to stall from 50ms to 29 seconds.
  Suddenly, Service A (which had nothing wrong with its code) runs out of
  Tomcat threads, stops responding to users, and crashes! Why?

  SOLUTION:
    Without a Circuit Breaker, incoming requests to Service A continue spawning
    threads that block for 29 seconds waiting on Service B. Within seconds, all
    200 Tomcat worker threads are exhausted waiting on the stalled network socket.
    Service A suffers cascading failure.
    Fix: Configure Resilience4j with a short socket timeout (e.g. 1 second) and
    a Circuit Breaker that trips to OPEN after 5 consecutive timeouts, immediately
    returning fallback responses without blocking worker threads.

────────────────────────────────────────────────────────────────────────────────
  9. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  1. Organizational Scalability: Amazon famously introduced the "Two-Pizza Team"
     rule enabled by microservices: teams independently deploy decoupled services
     without coordinating complex monolithic release trains or blocking on shared
     database schema migrations.
  2. Fault Isolation: In a resilient microservices architecture, if the Recommendation
     Service crashes, the checkout flow still completes seamlessly, displaying a
     default static bestseller list rather than showing an HTTP 500 error page.

────────────────────────────────────────────────────────────────────────────────
  10. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

  -> File 048: API Design Patterns (REST, gRPC, and GraphQL contracts)
  -> File 049: Apache Kafka (Event streaming for asynchronous microservices)
  -> File 096: Distributed Systems (Consensus, Raft, and CAP Theorem)
  -> File 098: Observability & Monitoring (Distributed Tracing with OpenTelemetry)

================================================================================
  END OF FILE 051
================================================================================
