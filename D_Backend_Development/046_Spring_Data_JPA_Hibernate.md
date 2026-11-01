================================================================================
  FILE 046: Spring Data JPA & Hibernate
  Section: D - Backend Development
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  Jakarta Persistence API (JPA) is the standard specification for Object-Relational
  Mapping (ORM) in Java, with Hibernate serving as its dominant reference implementation.
  This document delivers an in-depth operational analysis of entity lifecycles,
  persistence contexts, Hibernate Level 1 and Level 2 caching mechanisms, relationship
  mappings, transaction isolation, HikariCP connection pooling, and how to eliminate
  the catastrophic N+1 query problem using JOIN FETCH and EntityGraphs.

  Prerequisites: Relational database theory (SQL, Foreign Keys), File 045 (Spring Boot).
  What You'll Learn: JPA dirty checking, cascading, orphan removal, FetchType.LAZY
  vs EAGER, L1/L2 cache mechanics, Spring Data Derived Queries, and HikariCP tuning.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  JPA vs Hibernate
    JPA is a formal Java specification (interface definitions and annotations like
    @Entity, @Table). Hibernate is the concrete ORM engine implementing the JPA
    specification, translating high-level Java object operations into dialect-specific SQL.

  Persistence Context
    A first-level in-memory cache managed by an EntityManager instance where managed
    entity objects are tracked for state mutations during a database transaction.

  Entity Lifecycle States
    - Transient: Newly created object with 'new', not associated with a DB row or session.
    - Managed: Attached to the Persistence Context; mutations are tracked by dirty checking.
    - Detached: Previously managed entity whose Session has closed; changes are not tracked.
    - Removed: Scheduled for deletion upon transaction commit.

  Hibernate Dirty Checking
    An automatic mechanism where Hibernate snapshots an entity upon loading into the
    L1 cache. At transaction commit (flush), it compares the current object state
    against the snapshot and issues SQL UPDATEs only for modified fields.

  The N+1 Query Problem
    A critical performance flaw occurring when fetching N parent records triggers
    1 initial query followed by N individual subsequent queries to load each child
    relationship (totaling N+1 queries).

  Level 1 (L1) Cache
    Mandatory, non-configurable cache bound strictly to the current EntityManager /
    Hibernate Session lifecycle. Prevents repeated SELECTs for the same entity within
    a single transaction.

  Level 2 (L2) Cache
    Optional, distributed cache (e.g. Ehcache, Redis) shared across all EntityManager
    instances within an ApplicationContext (SessionFactory-wide).

  HikariCP
    The lightning-fast, zero-overhead JDBC connection pool used by default in Spring
    Boot to manage reusable physical PostgreSQL/MySQL database connections.

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  HIBERNATE PERSISTENCE CONTEXT & CACHE ARCHITECTURE                     │
  │                                                                         │
  │  Application Layer (Spring @Transactional Service)                      │
  │     │                                                                   │
  │     v                                                                   │
  │  +───────────────────────────────────────────────────────────────────+  │
  │  |  Hibernate Session / EntityManager (Level 1 Cache - Thread-Bound)  |  │
  │  |                                                                   |  │
  │  |  UserEntity id=10 ──> [ Managed Object ] <──> [ Original Snapshot]|  │
  │  |                                                     │             |  │
  │  +───────────────────────────────────┬─────────────────┼─────────────+  │
  │                                      │ Cache Miss      │ Dirty Check    │
  │                                      v                 v at Flush       │
  │  +───────────────────────────────────────────────────────────────────+  │
  │  |  Hibernate SessionFactory (Level 2 Cache - Shared / Redis/Ehcache)|  │
  │  |                                                                   |  │
  │  |  Key: UserEntity:10 ──> Cached Dehydrated State (Row Data)        |  │
  │  +───────────────────────────────────┬───────────────────────────────+  │
  │                                      │ Cache Miss                       │
  │                                      v                                  │
  │  +───────────────────────────────────────────────────────────────────+  │
  │  |  HikariCP Connection Pool (Active Connection Borrowed)            |  │
  │  +───────────────────────────────────┬───────────────────────────────+  │
  │                                      │ Physical TCP Socket              │
  │                                      v                                  │
  │  +───────────────────────────────────────────────────────────────────+  │
  │  |  PostgreSQL Database (Disk & Shared Buffers)                      |  │
  │  +───────────────────────────────────────────────────────────────────+  │
  └─────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  THE N+1 SELECT PROBLEM VS. JOIN FETCH RESOLUTION                       │
  │                                                                         │
  │  [ PROBLEM: Naive findAll() with LAZY/EAGER Relationship ]              │
  │  Query 1: SELECT * FROM authors LIMIT 10;                               │
  │  Query 2: SELECT * FROM books WHERE author_id = 1;                      │
  │  Query 3: SELECT * FROM books WHERE author_id = 2;                      │
  │  ...                                                                    │
  │  Query 11: SELECT * FROM books WHERE author_id = 10; (10+1 = 11 queries!)│
  │                                                                         │
  │  [ SOLUTION: Single Query with JOIN FETCH ]                             │
  │  Query 1: SELECT a, b FROM Author a JOIN FETCH a.books b;               │
  │  Result: EXACTLY 1 SQL Query returning parent + children via SQL JOIN!  │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  4. EXPLANATION & THEORY
────────────────────────────────────────────────────────────────────────────────

  Why FetchType.EAGER is Considered Harmful:
  When an entity relation is marked FetchType.EAGER, Hibernate fetches the child
  automatically whenever the parent is loaded. If you query a list of 1,000 orders
  having eager items, Spring Data JPA executes 1,001 SQL queries! Even worse,
  EAGER cannot be overridden at query time.
  Rule: Always define every relationship as FetchType.LAZY. When you need related
  children for a specific operation, fetch them explicitly using JOIN FETCH or
  @EntityGraph.

  Orphan Removal vs. CascadeType.REMOVE:
  - CascadeType.REMOVE deletes child records if the parent entity itself is deleted.
  - orphanRemoval = true deletes a child record from the database if it is simply
    removed from the parent's in-memory collection (e.g. order.getItems().remove(item)).

────────────────────────────────────────────────────────────────────────────────
  5. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: Java]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Properly Configured JPA Entities with Bi-Directional Relationship    │
  │                                                                          │
  │  package com.enterprise.library.model;                                   │
  │                                                                          │
  │  import jakarta.persistence.*;                                           │
  │  import java.util.ArrayList;                                             │
  │  import java.util.List;                                                  │
  │                                                                          │
  │  @Entity                                                                 │
  │  @Table(name = "authors")                                                │
  │  public class Author {                                                   │
  │      @Id                                                                 │
  │      @GeneratedValue(strategy = GenerationType.IDENTITY)                │
  │      private Long id;                                                    │
  │                                                                          │
  │      @Column(nullable = false)                                           │
  │      private String name;                                                │
  │                                                                          │
  │      // Always use FetchType.LAZY on collection relations!               │
  │      @OneToMany(mappedBy = "author", cascade = CascadeType.ALL, orphanRemoval = true, fetch = FetchType.LAZY)                                  │
  │      private List<Book> books = new ArrayList<>();                       │
  │                                                                          │
  │      // Helper synchronization method for bi-directional mapping         │
  │      public void addBook(Book book) {                                    │
  │          books.add(book);                                                │
  │          book.setAuthor(this);                                           │
  │      }                                                                   │
  │                                                                          │
  │      public void removeBook(Book book) {                                 │
  │          books.remove(book);                                             │
  │          book.setAuthor(null);                                           │
  │      }                                                                   │
  │      // Getters & Setters                                                │
  │  }                                                                       │
  │                                                                          │
  │  @Entity                                                                 │
  │  @Table(name = "books")                                                  │
  │  public class Book {                                                     │
  │      @Id                                                                 │
  │      @GeneratedValue(strategy = GenerationType.IDENTITY)                │
  │      private Long id;                                                    │
  │                                                                          │
  │      private String title;                                               │
  │                                                                          │
  │      @ManyToOne(fetch = FetchType.LAZY)                                  │
  │      @JoinColumn(name = "author_id", nullable = false)                  │
  │      private Author author;                                              │
  │      // Getters & Setters                                                │
  │  }                                                                       │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: Java]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Spring Data JPA Repository Solving N+1 via JOIN FETCH & @EntityGraph │
  │                                                                          │
  │  package com.enterprise.library.repository;                              │
  │                                                                          │
  │  import com.enterprise.library.model.Author;                             │
  │  import org.springframework.data.jpa.repository.EntityGraph;             │
  │  import org.springframework.data.jpa.repository.JpaRepository;           │
  │  import org.springframework.data.jpa.repository.Query;                  │
  │  import org.springframework.data.repository.query.Param;                 │
  │  import java.util.List;                                                  │
  │  import java.util.Optional;                                              │
  │                                                                          │
  │  public interface AuthorRepository extends JpaRepository<Author, Long> { │
  │      // Solution A: Explicit JPQL JOIN FETCH                             │
  │      @Query("SELECT DISTINCT a FROM Author a LEFT JOIN FETCH a.books WHERE a.name = :name")                                                     │
  │      List<Author> findByNameWithBooksFetch(@Param("name") String name);  │
  │                                                                          │
  │      // Solution B: Declarative EntityGraph (loads books eagerly in 1 query)                                                                    │
  │      @EntityGraph(attributePaths = {"books"})                            │
  │      @Query("SELECT a FROM Author a")                                    │
  │      List<Author> findAllWithBooksOptimized();                           │
  │                                                                          │
  │      // Solution C: Projection for High-Performance Read-Only Workloads  │
  │      interface AuthorSummaryView {                                       │
  │          Long getId();                                                   │
  │          String getName();                                               │
  │      }                                                                   │
  │      List<AuthorSummaryView> findByOrderByNameAsc();                     │
  │  }                                                                       │
  │                                                                          │
  │  // HikariCP Production Configuration (application.yml snippet)          │
  │  // spring:                                                              │
  │  //   datasource:                                                        │
  │  //     hikari:                                                          │
  │  //       maximum-pool-size: 20                                          │
  │  //       minimum-idle: 10                                               │
  │  //       idle-timeout: 300000                                           │
  │  //       connection-timeout: 20000                                      │
  │  //       max-lifetime: 1800000                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  7. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: What causes LazyInitializationException in Hibernate, and how do you resolve it?

  ANSWER:
    LazyInitializationException occurs when client code accesses a lazy-loaded
    child relationship (e.g. author.getBooks()) after the Hibernate Session
    (EntityManager) has already closed.
    Solutions:
    1. Fetch the collection within the original transaction using JOIN FETCH or @EntityGraph.
    2. Map the data directly to a DTO projection inside the @Transactional service boundary.
    Anti-pattern to avoid: 'spring.jpa.open-in-view=true' (keeps database connections
    held open during entire HTTP rendering, exhausting connection pools).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: How does Hibernate Dirty Checking work under the hood?

  ANSWER:
    When an entity is loaded into the Persistence Context (L1 cache), Hibernate
    creates an internal array containing a copy of all loaded property values
    (the "loaded snapshot"). During flush/commit time, Hibernate iterates through
    all managed entities and checks if current properties != snapshot properties.
    If differences exist, an UPDATE query is generated automatically.

────────────────────────────────────────────────────────────────────────────────
  8. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: The Accidental Full-Table UPDATE
  Look at this code:

    @Transactional
    public void updateUserEmail(Long id, String email) {
        User user = userRepository.findById(id).orElseThrow();
        user.setEmail(email);
        userRepository.save(user); // Redundant?
    }

  Does calling 'save()' do anything extra here, and what happens if we change 5
  different setters on the user object?

  SOLUTION:
    Calling 'userRepository.save(user)' is completely redundant because 'user' is
    already in the MANAGED state. Hibernate's dirty checking will automatically
    detect the changed email and issue the UPDATE statement at commit time.
    Furthermore, Hibernate issues an UPDATE with ALL columns by default; to update
    only modified columns, annotate the entity with @org.hibernate.annotations.DynamicUpdate.

────────────────────────────────────────────────────────────────────────────────
  9. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  1. Database Starvation Prevention: An undiscovered N+1 query problem on a homepage
     rendering 50 items will turn 1,000 concurrent web requests into 51,000 database
     queries, rapidly exhausting HikariCP pools and crashing downstream PostgreSQL instances.
  2. Batch Processing: When inserting 100,000 records, you must periodically call
     entityManager.flush() and entityManager.clear() every 50 records to prevent
     Hibernate's Level 1 Cache from consuming gigabytes of heap and causing OutOfMemoryErrors.

────────────────────────────────────────────────────────────────────────────────
  10. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

  -> File 028: PostgreSQL MVCC & WAL (Underlying transaction engine)
  -> File 029: PostgreSQL Indexing & Query Optimization (SQL execution plans)
  -> File 045: Spring Boot Fundamentals (Dependency Injection & Profiles)
  -> File 080: Room Database (Android SQLite ORM comparison)

================================================================================
  END OF FILE 046
================================================================================
