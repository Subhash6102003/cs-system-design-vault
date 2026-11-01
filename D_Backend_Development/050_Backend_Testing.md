================================================================================
  FILE 050: Backend Testing: Unit, Integration & Load Testing
  Section: D - Backend Development
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  Reliable backend systems require rigorous verification strategies that balance
  execution speed against real-world production fidelity. This guide provides an
  end-to-end framework covering the Testing Pyramid, unit testing with test doubles
  (mocks, stubs, spies), slice testing in Spring Boot, containerized integration
  testing with Testcontainers (real PostgreSQL instances), asynchronous testing
  in Python (pytest), and high-load stress testing using k6.

  Prerequisites: File 045 (Spring Boot), File 042 (FastAPI), basic Docker knowledge.
  What You'll Learn: Mockito verification semantics, @WebMvcTest vs @DataJpaTest,
  Testcontainers lifecycle, mutation testing, and writing deterministic API tests.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  Testing Pyramid
    An architectural heuristic popularized by Martin Fowler advocating for a large
    base of fast, cheap Unit Tests, a moderate middle layer of Integration Tests,
    and a small apex of slow, fragile End-to-End (E2E) tests.

  Test Double Types
    - Dummy: Objects passed around but never actually used (e.g. filling parameter lists).
    - Stub: Provides canned, predetermined answers to calls made during tests.
    - Spy: A real object wrapper that records invocations for verification.
    - Mock: Objects pre-programmed with expectations forming a specification of calls.
    - Fake: Working implementation with a shortcut (e.g. In-Memory H2 database).

  Testcontainers
    A Java library that supports JUnit tests by orchestrating lightweight, disposable
    Docker containers (real PostgreSQL, Kafka, Redis), eliminating H2 dialect drift.

  Slice Testing (Spring Boot)
    Focused testing that initializes only the specific Spring context slice required:
    - @WebMvcTest: Boots only the Controller layer and Jackson converters.
    - @DataJpaTest: Boots only the JPA Repository layer and configured DataSource.

  Mutation Testing (Pitest)
    A fault-injection technique where bugs ("mutants", e.g. replacing + with -) are
    injected into production bytecode to test if your unit test suite catches them.

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  THE MODERN BACKEND TESTING PYRAMID                                     │
  │                                                                         │
  │                   /\                                                    │
  │                  /  \   End-to-End (E2E) Tests                          │
  │                 /    \  - Slow (minutes), Fragile, Full System          │
  │                /──────\                                                 │
  │               /        \  Integration Tests (Testcontainers)            │
  │              /          \ - Medium speed, Real PostgreSQL & Kafka       │
  │             /────────────\                                              │
  │            /              \  Component / Slice Tests (@WebMvcTest)      │
  │           /                \ - Fast, Mocked DB / Real HTTP Validation   │
  │          /──────────────────\                                           │
  │         /                    \  Unit Tests (JUnit 5 + Mockito)          │
  │        /                      \ - Blazing fast (milliseconds), Isolated │
  │       /────────────────────────\                                        │
  └─────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  TESTCONTAINERS ISOLATED INTEGRATION TEST LIFECYCLE                     │
  │                                                                         │
  │  [ JUnit 5 Test Runner ]                                                │
  │        │ 1. @Container PostgreSQLContainer                              │
  │        v                                                                │
  │  [ Docker Daemon ] ──> Spins up ephemeral PostgreSQL 16 on random port  │
  │        │                                                                │
  │        v 2. @DynamicPropertySource dynamically sets jdbc:postgresql://  │
  │  [ Spring Application Context ]                                         │
  │        │ 3. Executes Flyway Migrations & Inserts Test Fixtures          │
  │        v                                                                │
  │  [ Runs Real SQL / Transaction Tests ]                                  │
  │        │                                                                │
  │        v 4. Test Completes ──> Docker container destroyed completely!   │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  4. EXPLANATION & THEORY
────────────────────────────────────────────────────────────────────────────────

  Why In-Memory H2 Databases Cause Production Incidents:
  Many teams test Spring JPA repositories using H2 in-memory databases because
  they start in 200ms. However:
  1. Dialect Drift: H2 accepts syntax that crashes PostgreSQL (e.g. JSONB operators,
     PostGIS geospatial functions, ILIKE vs LIKE, text search tsvector).
  2. Locking Differences: H2 does not implement PostgreSQL MVCC tuple versioning,
     masking deadlock bugs that only manifest in production under high concurrency.
  Solution: Always use Testcontainers to run real PostgreSQL instances during CI/CD.

────────────────────────────────────────────────────────────────────────────────
  5. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: Python & pytest]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Asynchronous API Integration Test with pytest & httpx                │
  │                                                                          │
  │  import pytest                                                           │
  │  from httpx import AsyncClient                                           │
  │  from unittest.mock import AsyncMock                                     │
  │                                                                          │
  │  # Mocking external payment gateway                                      │
  │  @pytest.fixture                                                         │
  │  def mock_stripe_gateway(monkeypatch):                                   │
  │      mock = AsyncMock()                                                  │
  │      mock.charge.return_value = {"status": "succeeded", "tx_id": "tx_99"}│
  │      monkeypatch.setattr("app.services.payment.stripe_client", mock)     │
  │      return mock                                                         │
  │                                                                          │
  │  @pytest.mark.asyncio                                                    │
  │  async def test_order_creation_success(mock_stripe_gateway):             │
  │      async with AsyncClient(app=app, base_url="http://test") as client:  │
  │          response = await client.post("/api/v1/checkout", json={         │
  │              "product_id": "item_123",                                   │
  │              "amount": 99.50                                             │
  │          })                                                              │
  │                                                                          │
  │      assert response.status_code == 201                                  │
  │      assert response.json()["status"] == "PAID"                          │
  │      mock_stripe_gateway.charge.assert_awaited_once_with(amount=99.50)   │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: Java]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Full Spring Boot Integration Test with Real PostgreSQL Testcontainer │
  │                                                                          │
  │  package com.enterprise.library.tests;                                   │
  │                                                                          │
  │  import org.junit.jupiter.api.Test;                                      │
  │  import org.springframework.beans.factory.annotation.Autowired;         │
  │  import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;                                                           │
  │  import org.springframework.boot.test.context.SpringBootTest;            │
  │  import org.springframework.http.MediaType;                              │
  │  import org.springframework.test.context.DynamicPropertyRegistry;        │
  │  import org.springframework.test.context.DynamicPropertySource;          │
  │  import org.springframework.test.web.servlet.MockMvc;                    │
  │  import org.testcontainers.containers.PostgreSQLContainer;               │
  │  import org.testcontainers.junit.jupiter.Container;                      │
  │  import org.testcontainers.junit.jupiter.Testcontainers;                 │
  │                                                                          │
  │  import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;                                                      │
  │  import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;                                                            │
  │                                                                          │
  │  @SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)                                                             │
  │  @AutoConfigureMockMvc                                                   │
  │  @Testcontainers                                                         │
  │  public class OrderIntegrationTest {                                     │
  │                                                                          │
  │      @Container                                                          │
  │      static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:16-alpine")                                                  │
  │          .withDatabaseName("testdb")                                     │
  │          .withUsername("testuser")                                       │
  │          .withPassword("testpass");                                      │
  │                                                                          │
  │      // Dynamically registers random container port into Spring DataSource                                                                       │
  │      @DynamicPropertySource                                              │
  │      static void configureProperties(DynamicPropertyRegistry registry) { │
  │          registry.add("spring.datasource.url", postgres::getJdbcUrl);   │
  │          registry.add("spring.datasource.username", postgres::getUsername);                                                                     │
  │          registry.add("spring.datasource.password", postgres::getPassword);                                                                     │
  │      }                                                                   │
  │                                                                          │
  │      @Autowired                                                          │
  │      private MockMvc mockMvc;                                            │
  │                                                                          │
  │      @Test                                                               │
  │      void shouldPersistOrderAndReturnHttp201() throws Exception {        │
  │          String payload = """                                            │
  │              {                                                           │
  │                  "productId": "prod_88",                                 │
  │                  "quantity": 2,                                          │
  │                  "unitPrice": 45.0                                       │
  │              }                                                           │
  │              """;                                                        │
  │                                                                          │
  │          mockMvc.perform(post("/api/v1/orders")                          │
  │                  .contentType(MediaType.APPLICATION_JSON)               │
  │                  .content(payload))                                      │
  │              .andExpect(status().isCreated())                            │
  │              .andExpect(jsonPath("$.orderId").exists())                  │
  │              .andExpect(jsonPath("$.totalAmount").value(90.0))           │
  │              .andExpect(jsonPath("$.status").value("CONFIRMED"));        │
  │      }                                                                   │
  │  }                                                                       │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  7. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: What is the difference between Mockito's mock() and spy()?

  ANSWER:
    A mock() creates a completely synthetic object instance where all methods
    return default values (null, 0, false) unless explicitly stubbed using
    'when(m.foo()).thenReturn(...)'. A spy() wraps an existing real object
    instance; all methods execute real production code unless a specific method
    is overridden with 'doReturn(...).when(spy).bar()'.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: Why should unit tests never test private methods directly?

  ANSWER:
    Private methods are internal implementation details. Testing them directly
    creates brittle tests that break upon simple refactoring. You should test
    private methods indirectly through the public interface, verifying the
    observable behavior and state changes of the class.

────────────────────────────────────────────────────────────────────────────────
  8. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: The Flaky Timestamp Test
  Look at this assertion:

    Order order = orderService.create();
    assertEquals(Instant.now(), order.getCreatedAt());

  Why does this test fail intermittently in CI/CD pipeline builds?

  SOLUTION:
    Execution elapsed between 'orderService.create()' and the subsequent call to
    'Instant.now()', causing millisecond/nanosecond divergence.
    Fixes:
    1. Pass a java.time.Clock bean into the service and freeze time in the test
       using 'Clock.fixed(Instant.parse("2026-01-01T00:00:00Z"), ZoneOffset.UTC)'.
    2. Assert within a tolerance threshold (e.g. within(1, ChronoUnit.SECONDS)).

────────────────────────────────────────────────────────────────────────────────
  9. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  1. CI/CD Release Confidence: High-performing engineering organizations (Stripe,
     Google) gate production deployments behind automated test suites running in
     isolated ephemeral containers, catching data migration regressions before
     customer traffic is routed.
  2. Capacity Planning via k6: Running load tests simulating 10,000 requests/sec
     exposes database connection leaks, CPU memory limits, and thread starvation
     long before real-world Black Friday traffic spikes occur.

────────────────────────────────────────────────────────────────────────────────
  10. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

  -> File 045: Spring Boot Fundamentals (Layered Architecture & Dependency Injection)
  -> File 046: Spring Data JPA & Hibernate (Database Entity Testing)
  -> File 109: Docker Fundamentals (Container lifecycle for Testcontainers)
  -> File 117: CI/CD Pipelines (Automated testing gates in GitHub Actions)

================================================================================
  END OF FILE 050
================================================================================
