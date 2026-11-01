================================================================================
  FILE 047: Java Virtual Threads & Reactive Programming
  Section: D - Backend Development
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  Java 21 revolutionized high-throughput concurrency with Project Loom Virtual
  Threads, dismantling the decades-old limitation where 1 Java thread mapped directly
  to 1 OS kernel thread (1:1 model). This document provides an exhaustive comparison
  between Virtual Threads (M:N user-mode scheduling) and Reactive Systems (Spring
  WebFlux / Project Reactor). You will learn how Virtual Threads unpark on carrier
  threads during blocking I/O, how to write structured concurrent code, and how to
  choose between Loom and Reactive architectures.

  Prerequisites: File 004 (JVM Architecture), File 005 (OS Threads), File 045 (Spring Boot).
  What You'll Learn: Carrier threads, continuations, thread pinning pitfalls,
  StructuredTaskScope, Mono/Flux streams, backpressure, and JVM memory scaling.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  Platform Thread
    A traditional Java thread (java.lang.Thread) implemented as a thin wrapper
    around an Operating System kernel thread. Typically allocates a fixed 1MB
    stack in native OS virtual memory.

  Virtual Thread (Project Loom)
    A lightweight, user-mode thread managed directly by the Java Virtual Machine.
    Its call stack is dynamically allocated on the JVM heap and resized on demand
    (starting at mere hundreds of bytes).

  Carrier Thread
    The underlying OS platform thread (managed by a ForkJoinPool inside the JVM)
    that physically executes bytecode on behalf of a virtual thread.

  Continuation
    The underlying JVM primitive supporting virtual threads. When a virtual thread
    encounters a blocking I/O operation (e.g. socket read, JDBC query, sleep), the
    JVM unmounts (yields) the continuation, saving its stack frames to the heap and
    freeing the carrier thread to execute other virtual threads.

  Thread Pinning
    An anti-pattern where a virtual thread cannot be unmounted from its carrier
    thread during a blocking operation. This occurs when blocking inside a
    'synchronized' block/method or native JNI call, defeating Loom's concurrency.

  Structured Concurrency
    A programming paradigm (StructuredTaskScope) where concurrent subtasks are
    syntactically bounded within a code block, ensuring that child threads cannot
    outlive their parent scope, drastically simplifying error handling and cancellation.

  Reactive Programming (Project Reactor)
    An asynchronous, non-blocking stream processing model based on the Reactive
    Streams specification (Publisher, Subscriber, Subscription, Processor).

  Backpressure
    A feedback mechanism in reactive streams where a slow downstream Subscriber
    signals to a fast upstream Publisher how many items it is ready to consume,
    preventing buffer overflow.

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  PLATFORM THREADS (1:1) VS. VIRTUAL THREADS (M:N LOOM SCHEDULING)       │
  │                                                                         │
  │  [ TRADITIONAL 1:1 PLATFORM THREADS ]                                   │
  │  Java Thread 1 ──> OS Kernel Thread 1 ──> Physical Core 0 [1MB Stack]  │
  │  Java Thread 2 ──> OS Kernel Thread 2 ──> Physical Core 1 [1MB Stack]  │
  │  Java Thread 3 ──> OS Kernel Thread 3 ──> (Blocked on Socket) ──> WAITING│
  │  (Limit: ~5,000 threads before OS Out-Of-Memory / Context Switch Thrashing)│
  │                                                                         │
  │  [ PROJECT LOOM M:N VIRTUAL THREADS ]                                   │
  │  1,000,000 Virtual Threads (Stacks allocated dynamically on JVM Heap)   │
  │  [ VT 1 ] [ VT 2 ] [ VT 3 ] ... [ VT 1,000,000 ]                        │
  │       │        │        │                                               │
  │       v        v        v  (Scheduled dynamically via ForkJoinPool)     │
  │  +-------------------------------------------------------------------+  │
  │  |   Carrier Threads (Platform Threads matching # of CPU Cores)      |  │
  │  |   [ Carrier 0 ]   [ Carrier 1 ]   [ Carrier 2 ]   [ Carrier 3 ]   |  │
  │  +────────┬───────────────┬───────────────┬───────────────┬──────────+  │
  │           v               v               v               v             │
  │        Core 0          Core 1          Core 2          Core 3           │
  │                                                                         │
  │  When VT 1 blocks on DB query:                                          │
  │  1. JVM unmounts VT 1 stack to Heap.                                    │
  │  2. Carrier 0 immediately mounts VT 2.                                  │
  │  3. When DB query returns, VT 1 re-enqueues in ForkJoinPool!            │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  4. EXPLANATION & THEORY
────────────────────────────────────────────────────────────────────────────────

  Virtual Threads vs. Reactive: When to Use Which?
  - Virtual Threads: The ultimate solution for I/O-bound web applications. You write
    clean, straightforward, imperative, synchronous-style code (try/catch, loops,
    standard debuggers, thread-local tracing) while achieving millions of concurrent
    connections with zero reactive complexity.
  - Reactive (WebFlux): Ideal when dealing with infinite data streams (SSE, WebSockets),
    complex event manipulation (windowing, throttling, combining multi-source streams),
    or when native reactive drivers (R2DBC) provide specialized backpressure.

  How to Enable Virtual Threads in Spring Boot 3.2+:
  Simply add one line to your application.yml:
    spring.threads.virtual.enabled: true
  This automatically instructs embedded Tomcat to dispatch every incoming HTTP
  request onto a new Virtual Thread!

────────────────────────────────────────────────────────────────────────────────
  5. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: Java]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Benchmark: Launching 100,000 Virtual Threads Concurrently            │
  │                                                                          │
  │  package com.enterprise.library.concurrency;                             │
  │                                                                          │
  │  import java.time.Duration;                                              │
  │  import java.time.Instant;                                               │
  │  import java.util.concurrent.Executors;                                  │
  │  import java.util.stream.IntStream;                                      │
  │                                                                          │
  │  public class VirtualThreadBenchmark {                                   │
  │      public static void main(String[] args) {                            │
  │          System.out.println("Starting 100,000 Virtual Threads...");      │
  │          Instant start = Instant.now();                                  │
  │                                                                          │
  │          // Thread-per-task executor using Virtual Threads               │
  │          try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {                                                                 │
  │              IntStream.range(0, 100_000).forEach(i -> {                  │
  │                  executor.submit(() -> {                                 │
  │                      // Simulates 100ms blocking I/O (sleep unmounts VT) │
  │                      Thread.sleep(Duration.ofMillis(100));               │
  │                      return i;                                           │
  │                  });                                                     │
  │              });                                                         │
  │          } // AutoCloseable executor waits for all tasks to complete!    │
  │                                                                          │
  │          Instant end = Instant.now();                                    │
  │          System.out.println("Completed in: " + Duration.between(start, end).toMillis() + " ms");                                           │
  │          // Typical result on 8-core CPU: ~500ms to complete 100,000 tasks!                                                                  │
  │      }                                                                   │
  │  }                                                                       │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: Java]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Production-Ready Structured Concurrency with StructuredTaskScope     │
  │                                                                          │
  │  package com.enterprise.library.concurrency;                             │
  │                                                                          │
  │  import java.util.concurrent.StructuredTaskScope;                        │
  │  import java.util.concurrent.StructuredTaskScope.Subtask;                │
  │  import java.time.Instant;                                               │
  │                                                                          │
  │  public class UserDashboardService {                                     │
  │      public record UserDashboard(String profile, String orders, double balance) {}                                                       │
  │                                                                          │
  │      public UserDashboard fetchDashboardData(String userId) throws Exception {                                                           │
  │          // ShutdownOnFailure cancels all sibling tasks if ANY single task fails!                                                        │
  │          try (var scope = new StructuredTaskScope.ShutdownOnFailure()) { │
  │              // Fork 3 independent microservice calls onto virtual threads                                                                │
  │              Subtask<String> profileTask = scope.fork(() -> fetchProfile(userId));                                                       │
  │              Subtask<String> ordersTask  = scope.fork(() -> fetchOrders(userId));                                                        │
  │              Subtask<Double> balanceTask = scope.fork(() -> fetchBalance(userId));                                                       │
  │                                                                          │
  │              // Join all subtasks and propagate failure if any threw exception                                                           │
  │              scope.join();                                               │
  │              scope.throwIfFailed();                                      │
  │                                                                          │
  │              // Safe to call .get() because join() and throwIfFailed() succeeded                                                         │
  │              return new UserDashboard(                                   │
  │                  profileTask.get(),                                      │
  │                  ordersTask.get(),                                       │
  │                  balanceTask.get()                                       │
  │              );                                                          │
  │          }                                                               │
  │      }                                                                   │
  │                                                                          │
  │      private String fetchProfile(String id) throws InterruptedException {                                                                │
  │          Thread.sleep(80); // Simulates network HTTP call                │
  │          return "ProfileData for " + id;                                 │
  │      }                                                                   │
  │      private String fetchOrders(String id) throws InterruptedException {                                                                 │
  │          Thread.sleep(120);                                              │
  │          return "OrdersList for " + id;                                  │
  │      }                                                                   │
  │      private double fetchBalance(String id) throws InterruptedException {                                                                │
  │          Thread.sleep(50);                                               │
  │          return 1450.75;                                                 │
  │      }                                                                   │
  │  }                                                                       │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  7. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: What is Thread Pinning in Virtual Threads, and how do you prevent it?

  ANSWER:
    Thread pinning occurs when a virtual thread cannot be unmounted from its
    underlying carrier platform thread during a blocking operation. This happens
    when:
    1. Blocking I/O is executed inside a 'synchronized' block or method.
    2. A native JNI method or foreign function is executed.
    Pinning starves the carrier thread pool, turning Loom into a bottleneck.
    Fix: Replace 'synchronized' blocks with 'java.util.concurrent.locks.ReentrantLock',
    which fully supports virtual thread unmounting. Run the JVM flag
    '-Djdk.tracePinnedThreads=full' to detect pinning in production logs.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: Why should you NEVER pool Virtual Threads (e.g. with a fixed-size thread pool)?

  ANSWER:
    Platform thread pools exist because creating an OS thread is expensive (~1MB
    memory, OS kernel syscall). In contrast, Virtual Threads are ephemeral, dirt-cheap
    JVM objects (costing nanoseconds to create and hundreds of bytes of heap).
    Pooling virtual threads adds lock contention and defeats their purpose. Always
    create a new virtual thread per task via 'Executors.newVirtualThreadPerTaskExecutor()'.
    To limit concurrency against external databases, use a java.util.concurrent.Semaphore.

────────────────────────────────────────────────────────────────────────────────
  8. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: The Hidden Connection Exhaustion
  Look at this code running on a Virtual Thread server:

    @GetMapping("/users/{id}")
    public User getUser(@PathVariable Long id) {
        return jdbcTemplate.queryForObject("SELECT * FROM users WHERE id = ?", mapper, id);
    }

  The server runs 50,000 concurrent requests effortlessly, but suddenly requests
  fail with: "ConnectionTimeoutException: Connection is not available from pool".
  Why?

  SOLUTION:
    While Virtual Threads allow 50,000 concurrent threads, your database connection
    pool (HikariCP) only has e.g. 20 connections! The 50,000 virtual threads all
    rush to borrow a connection from HikariCP and block. Virtual threads do NOT
    magically scale your database server. You must protect database calls with a
    Semaphore or rate limiter.

────────────────────────────────────────────────────────────────────────────────
  9. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  1. Observability: Unlike reactive code where stack traces are fragmented across
     disjoint schedulers, Virtual Threads preserve standard synchronous stack
     traces, enabling APM tools (Datadog, OpenTelemetry) to trace errors seamlessly.
  2. Legacy Modernization: Existing blocking Java libraries (JDBC, Apache HttpClient)
     automatically gain massive scalability on Java 21 without requiring full
     code rewrites into non-blocking reactive APIs.

────────────────────────────────────────────────────────────────────────────────
  10. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

  -> File 005: Operating System Fundamentals (Kernel Context Switching)
  -> File 044: Python Asyncio & GIL (Alternative event-loop concurrency model)
  -> File 045: Spring Boot Fundamentals (Enabling virtual threads in Spring)
  -> File 046: Spring Data JPA & Hibernate (HikariCP connection pool integration)

================================================================================
  END OF FILE 047
================================================================================
