================================================================================
  FILE 045: Java Spring Boot Fundamentals
  Section: D - Backend Development
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  Spring Boot is the enterprise standard framework for building production-grade,
  resilient microservices and REST APIs in Java. This guide covers the Inversion
  of Control (IoC) container, Dependency Injection (DI) paradigms, component
  scanning, auto-configuration mechanics, application configuration profiles,
  and production monitoring with Spring Boot Actuator.

  Prerequisites: Java 17+, Object-Oriented Programming (Polymorphism, Interfaces).
  What You'll Learn: Bean lifecycles, Bean scopes, Constructor vs. Field Injection,
  conditional auto-configuration (@ConditionalOnProperty), Spring MVC request
  lifecycle, and writing enterprise-grade controllers with exception handling.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  Inversion of Control (IoC)
    A software architecture pattern where the framework controls program execution
    flow and object creation, reversing the traditional paradigm where custom code
    instantiates dependencies directly via the 'new' operator.

  Dependency Injection (DI)
    A specific implementation of IoC where an object's collaborators (dependencies)
    are supplied from the outside by the Spring ApplicationContext container.

  ApplicationContext
    The core Spring IoC container interface responsible for instantiating, configuring,
    wiring, and managing the entire lifecycle of Spring Beans.

  Spring Bean
    An object managed, assembled, and instantiated by the Spring IoC container.

  Bean Scopes
    The lifecycle bounds of a Bean:
    - Singleton (default): Exactly one shared instance per Spring container.
    - Prototype: A new instance created on every injection request.
    - Request: One instance per HTTP request lifecycle (Web-aware).
    - Session: One instance per HTTP user session (Web-aware).

  Auto-Configuration
    Spring Boot's opinionated mechanism that automatically registers beans based
    on JARs present on the classpath (e.g. adding 'spring-boot-starter-web' automatically
    configures an embedded Tomcat server, Jackson JSON mapper, and DispatcherServlet).

  DispatcherServlet
    The front-controller servlet in Spring MVC that intercepts all incoming HTTP
    requests, delegates them to appropriate HandlerMappings, invokes Controller
    endpoints, and formats responses.

  Actuator
    Production-ready monitoring and management endpoints exposing application metrics,
    health checks, thread dumps, environment configs, and HTTP trace logs.

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  SPRING BOOT INVERSION OF CONTROL (IoC) CONTAINER LIFECYCLE            │
  │                                                                         │
  │   1. Classpath Scanning (@SpringBootApplication)                        │
  │            │                                                            │
  │            v                                                            │
  │   2. Load Bean Definitions (@Component, @Service, @Repository, @Bean)   │
  │            │                                                            │
  │            v                                                            │
  │   3. Instantiate Beans (Dependency Resolution & Topological Sort)       │
  │            │                                                            │
  │            v                                                            │
  │   4. Populate Bean Properties (Constructor Dependency Injection)        │
  │            │                                                            │
  │            v                                                            │
  │   5. BeanPostProcessor (Before Initialization / Aware Interfaces)       │
  │            │                                                            │
  │            v                                                            │
  │   6. Custom Init Methods (@PostConstruct / InitializingBean)            │
  │            │                                                            │
  │            v                                                            │
  │   7. BeanPostProcessor (After Initialization - Proxies, AOP, CGLIB)     │
  │            │                                                            │
  │            v                                                            │
  │   [ READY IN APPLICATION CONTEXT (SINGLETON CACHE) ]                    │
  │            │                                                            │
  │            v  (On Context Shutdown)                                     │
  │   8. Custom Destruction (@PreDestroy / DisposableBean)                  │
  └─────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  SPRING MVC HTTP REQUEST DISPATCH FLOW                                  │
  │                                                                         │
  │  HTTP Request (e.g. GET /api/v1/orders/42)                              │
  │        │                                                                │
  │        v                                                                │
  │  +─────────────────────────+                                            │
  │  |    DispatcherServlet    | <── Front Controller                       │
  │  +───────────┬─────────────+                                            │
  │              │ 1. Consult URL Mappings                                  │
  │              v                                                          │
  │  +─────────────────────────+                                            │
  │  |     HandlerMapping      | ──> Finds OrderController.getOrder()       │
  │  +───────────┬─────────────+                                            │
  │              │ 2. Execute Interceptors (Auth, Logging)                  │
  │              v                                                          │
  │  +─────────────────────────+                                            │
  │  |     HandlerAdapter      | ──> Invokes Controller Method via Reflection│
  │  +───────────┬─────────────+                                            │
  │              │ 3. Execute Business Logic                                │
  │              v                                                          │
  │  +─────────────────────────+     +─────────────────────────+            │
  │  |     OrderController     | ──> |      OrderService       |            │
  │  +───────────┬─────────────+     +─────────────────────────+            │
  │              │ 4. Return DTO Entity                                     │
  │              v                                                          │
  │  +─────────────────────────+                                            │
  │  | HttpMessageConverter    | ──> Jackson serializes Java Object to JSON │
  │  +───────────┬─────────────+                                            │
  │              │                                                          │
  │              v                                                          │
  │  HTTP 200 OK + JSON Response Body                                       │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  4. EXPLANATION & THEORY
────────────────────────────────────────────────────────────────────────────────

  Why Field Injection (@Autowired on private fields) is an Anti-Pattern:
  1. Immobility for Unit Testing: You cannot inject mock dependencies without
     spinning up a heavyweight Spring Context or using reflection hacks.
  2. Immutability Violation: Fields cannot be declared 'final', making beans mutable.
  3. Circular Dependencies Hidden: It conceals circular dependency bugs until
     runtime rather than catching them fail-fast at compile/startup time.
  Best Practice: Always use Constructor Injection. It enforces final fields,
  guarantees all required dependencies are present at construction, and makes
  unit testing effortless with plain 'new MyService(mockRepo)'.

  Auto-Configuration Mechanics (@EnableAutoConfiguration):
  Spring Boot scans META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports.
  It evaluates conditional annotations on each configuration class:
  - @ConditionalOnClass: Bean registers only if a specified library is on classpath.
  - @ConditionalOnMissingBean: Registers only if developer hasn't defined custom bean.
  - @ConditionalOnProperty: Checks if application.yml flag is enabled.

────────────────────────────────────────────────────────────────────────────────
  5. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: Java]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Standard Application Setup & Configuration Profiles                  │
  │                                                                          │
  │  package com.enterprise.library;                                         │
  │                                                                          │
  │  import org.springframework.boot.SpringApplication;                     │
  │  import org.springframework.boot.autoconfigure.SpringBootApplication;   │
  │  import org.springframework.boot.context.properties.ConfigurationProperties;                                                           │
  │  import org.springframework.context.annotation.Configuration;           │
  │                                                                          │
  │  @SpringBootApplication                                                  │
  │  public class BackendApplication {                                       │
  │      public static void main(String[] args) {                            │
  │          SpringApplication.run(BackendApplication.class, args);         │
  │      }                                                                   │
  │  }                                                                       │
  │                                                                          │
  │  // Type-safe Configuration Properties (application.yml mapping)        │
  │  @Configuration                                                          │
  │  @ConfigurationProperties(prefix = "app.security")                       │
  │  public class SecurityConfigProperties {                                 │
  │      private int tokenExpirationMinutes = 60;                            │
  │      private String issuer = "https://auth.company.com";                 │
  │                                                                          │
  │      public int getTokenExpirationMinutes() { return tokenExpirationMinutes; }                                                                 │
  │      public void setTokenExpirationMinutes(int m) { this.tokenExpirationMinutes = m; }                                                          │
  │      public String getIssuer() { return issuer; }                        │
  │      public void setIssuer(String i) { this.issuer = i; }                │
  │  }                                                                       │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: Java]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Production-Ready Layered REST Controller with Global Exception Handling│
  │                                                                          │
  │  package com.enterprise.library.orders;                                  │
  │                                                                          │
  │  import org.springframework.http.HttpStatus;                             │
  │  import org.springframework.http.ResponseEntity;                         │
  │  import org.springframework.web.bind.annotation.*;                      │
  │  import jakarta.validation.Valid;                                        │
  │  import jakarta.validation.constraints.NotNull;                          │
  │  import jakarta.validation.constraints.Positive;                         │
  │  import java.time.Instant;                                               │
  │  import java.util.UUID;                                                  │
  │                                                                          │
  │  // 1. Data Transfer Objects (DTOs)                                      │
  │  public record OrderRequest(                                             │
  │      @NotNull String productId,                                          │
  │      @Positive int quantity,                                             │
  │      @Positive double unitPrice                                          │
  │  ) {}                                                                    │
  │                                                                          │
  │  public record OrderResponse(                                            │
  │      String orderId,                                                     │
  │      String productId,                                                   │
  │      double totalAmount,                                                 │
  │      String status,                                                      │
  │      Instant createdAt                                                   │
  │  ) {}                                                                    │
  │                                                                          │
  │  // 2. Service Layer (Constructor Injection)                             │
  │  @org.springframework.stereotype.Service                                 │
  │  public class OrderService {                                             │
  │      public OrderResponse createOrder(OrderRequest request) {            │
  │          String id = UUID.randomUUID().toString();                       │
  │          double total = request.quantity() * request.unitPrice();        │
  │          return new OrderResponse(id, request.productId(), total, "CONFIRMED", Instant.now());                                                 │
  │      }                                                                   │
  │  }                                                                       │
  │                                                                          │
  │  // 3. REST Controller                                                   │
  │  @RestController                                                         │
  │  @RequestMapping("/api/v1/orders")                                       │
  │  public class OrderController {                                          │
  │      private final OrderService orderService;                            │
  │                                                                          │
  │      // Recommended Constructor Injection (No @Autowired needed in Spring 4.3+)                                                                │
  │      public OrderController(OrderService orderService) {                 │
  │          this.orderService = orderService;                               │
  │      }                                                                   │
  │                                                                          │
  │      @PostMapping                                                        │
  │      public ResponseEntity<OrderResponse> placeOrder(@Valid @RequestBody OrderRequest req) {                                                    │
  │          OrderResponse res = orderService.createOrder(req);              │
  │          return ResponseEntity.status(HttpStatus.CREATED).body(res);     │
  │      }                                                                   │
  │  }                                                                       │
  │                                                                          │
  │  // 4. Centralized Global Exception Handler (RFC 7807 Problem Detail)    │
  │  @RestControllerAdvice                                                   │
  │  public class GlobalExceptionHandler {                                   │
  │      @ExceptionHandler(IllegalArgumentException.class)                   │
  │      public ResponseEntity<ErrorResponse> handleBadRequest(IllegalArgumentException ex) {                                                      │
  │          ErrorResponse err = new ErrorResponse(HttpStatus.BAD_REQUEST.value(), ex.getMessage(), Instant.now());                                 │
  │          return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(err); │
  │      }                                                                   │
  │                                                                          │
  │      public record ErrorResponse(int status, String message, Instant timestamp) {}                                                             │
  │  }                                                                       │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  7. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: What is the difference between @Component, @Service, and @Repository?

  ANSWER:
    Architecturally, all three are meta-annotated with @Component, registering
    the annotated class as a Spring Bean. However, they express distinct architectural
    layers:
    - @Repository marks database data-access components and automatically enables
      DataAccessException translation into Spring's consistent unchecked exception
      hierarchy.
    - @Service marks the service layer encapsulating business transactions.
    - @Component is the generic stereotype for any Spring-managed component.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: Why does Spring default to Singleton scope, and is it thread-safe?

  ANSWER:
    Spring defaults to Singleton scope to minimize memory allocation and Garbage
    Collection overhead by keeping only one shared instance of services/controllers
    in memory. HOWEVER, Spring Singletons are NOT inherently thread-safe. Because
    multiple web request threads call the same Singleton instance simultaneously,
    beans must remain STATELESS (containing no mutable instance variables).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: What is the purpose of Spring Boot Starters?

  ANSWER:
    Starters are convenient dependency descriptors (e.g. spring-boot-starter-web)
    that bundle a curated, compatible set of transitive dependencies with tested
    version alignments, eliminating manual Maven/Gradle dependency conflicts.

────────────────────────────────────────────────────────────────────────────────
  8. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: The Invisible Transaction Rollback Bug
  Look at this code:

    @Service
    public class AccountService {
        public void transferMoney(Long from, Long to, Double amt) {
            updateBalance(from, -amt);
            updateBalance(to, amt);
        }

        @Transactional
        public void updateBalance(Long id, Double amt) {
            // DB update that throws RuntimeException on failure
        }
    }

  Why does the transaction FAIL to roll back if the second updateBalance throws
  an exception?

  SOLUTION:
    Spring's @Transactional relies on dynamic AOP proxies. When 'transferMoney'
    calls 'updateBalance' directly (self-invocation via 'this'), the call bypasses
    the Spring proxy completely! The @Transactional advice is never intercepted.
    To fix this, annotate the public entry method 'transferMoney' with @Transactional.

────────────────────────────────────────────────────────────────────────────────
  9. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  1. Enterprise Resilience: Spring Boot Actuator health checks (/actuator/health)
     integrate directly with Kubernetes Liveness and Readiness probes to automate
     container restarts and traffic routing during microservice failures.
  2. Standardized Configuration: Using Spring Profiles (application-prod.yml vs
     application-dev.yml) allows identical container images to adapt cleanly to
     AWS RDS databases in staging vs production without modifying bytecode.

────────────────────────────────────────────────────────────────────────────────
  10. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

  -> File 004: JVM Architecture (Memory Layout, Metaspace & Garbage Collection)
  -> File 046: Spring Data JPA & Hibernate (Database ORM & Persistence)
  -> File 047: Java Virtual Threads (High-throughput Spring concurrency)
  -> File 051: Microservices Architecture (Decomposition & Service Discovery)

================================================================================
  END OF FILE 045
================================================================================
