================================================================================
  FILE 026: RELATIONAL DATABASE THEORY: THE FOUNDATION OF MODERN DATA STORAGE
  Section: C - DBMS & Databases
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  This document covers the fundamental principles of relational database management systems (RDBMS). Prerequisites include basic programming knowledge and a conceptual understanding of data storage. You will learn how to design robust database schemas using Entity-Relationship (ER) diagrams, enforce data integrity through normalization, understand functional dependencies, and grasp the core ACID properties that guarantee reliable transactions. This theoretical foundation is critical before writing a single line of SQL.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  ENTITY
    A real-world object or concept (e.g., User, Order) that is distinguishable from other objects.

  ATTRIBUTE
    A property or characteristic of an entity (e.g., email, price).

  TUPLE / RECORD
    A single row in a table representing a specific instance of an entity.

  RELATION / TABLE
    A collection of tuples sharing the same attributes.

  SCHEMA
    The structural definition of a database, detailing tables, columns, and constraints.

  SUPER KEY
    Any set of attributes that uniquely identifies a row in a table.

  CANDIDATE KEY
    A minimal super key; a set of attributes that can uniquely identify a row, with no redundant attributes.

  PRIMARY KEY (PK)
    The chosen candidate key used to uniquely identify records in a table.

  FOREIGN KEY (FK)
    An attribute in one table that references the primary key of another table, enforcing referential integrity.

  COMPOSITE KEY
    A primary key consisting of two or more attributes.

  FUNCTIONAL DEPENDENCY (FD)
    A relationship where the value of one attribute (or set) uniquely determines the value of another (denoted as X → Y).

  CLOSURE OF A SET OF ATTRIBUTES
    The complete set of attributes that can be functionally determined by the initial set.

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  ENTITY-RELATIONSHIP DIAGRAM (ERD) FLOW                                 │
  │                                                                         │
  │    [ CUSTOMER ] 1 --------- N < PLACES > N --------- 1 [ ORDER ]        │
  │    |-- CustomerID (PK)                                  |-- OrderID (PK)│
  │    |-- Name                                             |-- OrderDate   │
  │    |-- Email                                            |-- TotalAmount │
  │                                                                         │
  │         | 1                                                             │
  │         |                                                               │
  │         | N                                                             │
  │    < HAS_PROFILE >                                                      │
  │         | 1                                                             │
  │    [ PROFILE ]                                                          │
  │    |-- ProfileID (PK)                                                   │
  │    |-- CustomerID (FK, UK)                                              │
  │    |-- Bio                                                              │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

  1:1 Relationship: CUSTOMER to PROFILE. Each customer has exactly one profile.
  1:N Relationship: CUSTOMER to ORDER. One customer can place many orders.
  M:N Relationship: ORDER to PRODUCT. An order can have many products, and a product can appear in many orders (typically resolved using a junction table like ORDER_ITEM).

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  NORMALIZATION LADDER                                                   │
  │                                                                         │
  │  [ Unnormalized Data (UNF) ]                                            │
  │         |                                                               │
  │         v (Remove repeating groups)                                     │
  │  [ First Normal Form (1NF) ]                                            │
  │         |                                                               │
  │         v (Remove partial dependencies)                                 │
  │  [ Second Normal Form (2NF) ]                                           │
  │         |                                                               │
  │         v (Remove transitive dependencies)                              │
  │  [ Third Normal Form (3NF) ]                                            │
  │         |                                                               │
  │         v (Every determinant must be a candidate key)                   │
  │  [ Boyce-Codd Normal Form (BCNF) ]                                      │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  4. EXPLANATION & THEORY
────────────────────────────────────────────────────────────────────────────────

  ACID PROPERTIES EXPLAINED
  ATOMICITY ("All or Nothing"): A transaction is a single unit of work. If it fails halfway, all changes are rolled back. 
    Analogy: Transferring money. You deduct $100 from A and add $100 to B. If the addition fails, the deduction must be undone.
  CONSISTENCY: A transaction takes the DB from one valid state to another, strictly abiding by constraints and triggers.
    Analogy: Double-entry bookkeeping. The books must balance before and after the ledger update.
  ISOLATION: Concurrent transactions execute as if they were running sequentially.
    Analogy: Two people buying the last seat on a flight simultaneously. Only one succeeds; they don't get half a seat each.
  DURABILITY: Once a transaction is committed, it remains saved even in the event of a crash/power loss.
    Analogy: Writing in ink and storing the paper in a fireproof safe. (Implemented via Write-Ahead Logging).

────────────────────────────────────────────────────────────────────────────────
  5. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: SQL]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // SQL: Enforcing Keys and Relationships                                │
  │                                                                          │
  │  -- Demonstrating 1:N and M:N relationships using standard SQL DDL       │
  │  CREATE TABLE Customer (                                                 │
  │      CustomerID INT PRIMARY KEY, -- Primary Key                          │
  │      Email VARCHAR(255) UNIQUE NOT NULL, -- Candidate Key                │
  │      Name VARCHAR(100) NOT NULL                                          │
  │  );                                                                      │
  │                                                                          │
  │  CREATE TABLE Product (                                                  │
  │      ProductID INT PRIMARY KEY,                                          │
  │      SKU VARCHAR(50) UNIQUE NOT NULL,                                    │
  │      Price DECIMAL(10, 2) NOT NULL                                       │
  │  );                                                                      │
  │                                                                          │
  │  CREATE TABLE "Order" (                                                  │
  │      OrderID INT PRIMARY KEY,                                            │
  │      CustomerID INT NOT NULL,                                            │
  │      OrderDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,                      │
  │      FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID)            │
  │          ON DELETE CASCADE -- Enforces 1:N relationship                  │
  │  );                                                                      │
  │                                                                          │
  │  -- Junction table for M:N relationship                                  │
  │  CREATE TABLE OrderItem (                                                │
  │      OrderID INT,                                                        │
  │      ProductID INT,                                                      │
  │      Quantity INT NOT NULL CHECK (Quantity > 0),                         │
  │      PRIMARY KEY (OrderID, ProductID), -- Composite Primary Key          │
  │      FOREIGN KEY (OrderID) REFERENCES "Order"(OrderID),                  │
  │      FOREIGN KEY (ProductID) REFERENCES Product(ProductID)               │
  │  );                                                                      │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

  Let's walk through normalizing a raw e-commerce dataset into BCNF.

  [Language: TEXT]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Unnormalized Form (UNF)                                              │
  │                                                                          │
  │  Table: SalesData                                                        │
  │  OrderID, OrderDate, CustomerID, CustomerName, [ProductID, ProductName, Quantity, Price]│
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

  [Language: SQL]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // 1NF (First Normal Form)                                              │
  │                                                                          │
  │  -- Flatten the repeating groups.                                        │
  │  CREATE TABLE Sales_1NF (                                                │
  │      OrderID INT,                                                        │
  │      ProductID INT,                                                      │
  │      OrderDate DATE,                                                     │
  │      CustomerID INT,                                                     │
  │      CustomerName VARCHAR(100),                                          │
  │      ProductName VARCHAR(100),                                           │
  │      Quantity INT,                                                       │
  │      Price DECIMAL(10,2),                                                │
  │      PRIMARY KEY (OrderID, ProductID)                                    │
  │  );                                                                      │
  │  -- Functional Dependencies (FDs):                                       │
  │  -- {OrderID, ProductID} -> {Quantity}                                   │
  │  -- {OrderID} -> {OrderDate, CustomerID, CustomerName}                   │
  │  -- {ProductID} -> {ProductName, Price}                                  │
  │  -- {CustomerID} -> {CustomerName}                                       │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘
  Rule: Atomic values, no repeating groups.

  [Language: SQL]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // 2NF (Second Normal Form)                                             │
  │                                                                          │
  │  -- Break into tables based on partial dependencies.                     │
  │  CREATE TABLE Orders_2NF (                                               │
  │      OrderID INT PRIMARY KEY,                                            │
  │      OrderDate DATE,                                                     │
  │      CustomerID INT,                                                     │
  │      CustomerName VARCHAR(100)                                           │
  │  );                                                                      │
  │                                                                          │
  │  CREATE TABLE Products_2NF (                                             │
  │      ProductID INT PRIMARY KEY,                                          │
  │      ProductName VARCHAR(100),                                           │
  │      Price DECIMAL(10,2)                                                 │
  │  );                                                                      │
  │                                                                          │
  │  CREATE TABLE OrderItems_2NF (                                           │
  │      OrderID INT,                                                        │
  │      ProductID INT,                                                      │
  │      Quantity INT,                                                       │
  │      PRIMARY KEY (OrderID, ProductID),                                   │
  │      FOREIGN KEY (OrderID) REFERENCES Orders_2NF(OrderID),               │
  │      FOREIGN KEY (ProductID) REFERENCES Products_2NF(ProductID)          │
  │  );                                                                      │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘
  Rule: 1NF + No partial dependencies (no non-prime attribute depends on part of a composite primary key).

  [Language: SQL]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // 3NF (Third Normal Form) & BCNF                                       │
  │                                                                          │
  │  -- CustomerName depends on CustomerID, which is not the PK of Orders_2NF (transitive).│
  │  CREATE TABLE Customers_3NF (                                            │
  │      CustomerID INT PRIMARY KEY,                                         │
  │      CustomerName VARCHAR(100)                                           │
  │  );                                                                      │
  │                                                                          │
  │  CREATE TABLE Orders_3NF (                                               │
  │      OrderID INT PRIMARY KEY,                                            │
  │      OrderDate DATE,                                                     │
  │      CustomerID INT,                                                     │
  │      FOREIGN KEY (CustomerID) REFERENCES Customers_3NF(CustomerID)       │
  │  );                                                                      │
  │  -- Products_2NF and OrderItems_2NF remain the same.                     │
  │  -- This schema is now in BCNF.                                          │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘
  Rule: 2NF + No transitive dependencies (non-prime attributes must not depend on other non-prime attributes). For BCNF: Every determinant must be a candidate key.

  [Language: SQL]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Denormalization Example                                              │
  │                                                                          │
  │  -- Analytics flat table (Denormalized)                                  │
  │  CREATE TABLE MonthlySalesSummary (                                      │
  │      YearMonth VARCHAR(7), -- e.g., '2023-10'                            │
  │      CustomerID INT,                                                     │
  │      CustomerName VARCHAR(100), -- Redundant, but fast for BI tools      │
  │      TotalSpent DECIMAL(12,2),                                           │
  │      PRIMARY KEY (YearMonth, CustomerID)                                 │
  │  );                                                                      │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘
  In read-heavy analytics systems, JOINs are expensive. We intentionally violate 3NF.

────────────────────────────────────────────────────────────────────────────────
  7. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: What is the difference between a Primary Key and a Unique Key?

  ANSWER:
    A table can have only one Primary Key but multiple Unique Keys. Primary Keys cannot contain NULLs, whereas Unique Keys typically allow one or more NULL values (depending on the RDBMS).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: Explain the difference between 3NF and BCNF.

  ANSWER:
    3NF ensures no non-prime attribute is transitively dependent on the primary key. BCNF is stricter: every determinant must be a candidate key. BCNF handles cases where a table has multiple overlapping candidate keys.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: What is a composite key, and when would you use it?

  ANSWER:
    A primary key made of multiple columns. Often used in junction/mapping tables (e.g., user_id, role_id in a user_roles table) to enforce uniqueness on the combination.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: When is denormalization justified?

  ANSWER:
    In OLAP (data warehousing) or high-traffic read-heavy OLTP systems where complex JOINs cause unacceptable latency. It trades storage space and write-consistency overhead for read performance.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: How do foreign keys impact database performance?

  ANSWER:
    They add write overhead because the DB must check the parent table for existence on INSERT/UPDATE and check child tables on DELETE/UPDATE. They improve read reliability.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: What is an entity vs an attribute?

  ANSWER:
    Entity is a distinct object (Employee). Attribute is a property of that object (Salary).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q7: What is an identifying vs non-identifying relationship?

  ANSWER:
    Identifying: The child's existence depends entirely on the parent, and the parent's PK is part of the child's PK (e.g., Room in a Building). Non-identifying: The child can exist independently (e.g., Employee in a Department).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q8: Describe the concept of "Closure" in functional dependencies.

  ANSWER:
    The closure of a set of attributes is the complete set of attributes that can be uniquely determined by them, computed using Armstrong's axioms. It helps in finding candidate keys.

────────────────────────────────────────────────────────────────────────────────
  8. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: The Infinite Loop Delete

  CREATE TABLE Category (
      CatID INT PRIMARY KEY,
      ParentCatID INT,
      FOREIGN KEY (ParentCatID) REFERENCES Category(CatID) ON DELETE CASCADE
  );

  SOLUTION:
    Problem: Deleting the root node of a deeply nested category tree can cause a massive cascade, potentially locking the table for a long time or exceeding stack/memory limits in some DBs.
    Answer: Use soft deletes (IsDeleted = 1), or handle hierarchical deletion in application code/stored procedures to batch deletes.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 2: The Redundant Constraint

  CREATE TABLE UserSession (
      SessionID UUID PRIMARY KEY UNIQUE,
      UserID INT NOT NULL,
      CreatedAt TIMESTAMP
  );

  SOLUTION:
    Problem: PRIMARY KEY UNIQUE is redundant. PRIMARY KEY intrinsically enforces uniqueness.
    Answer: Just use PRIMARY KEY.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 3: Normalization Nightmare

  Table: Employee
  Columns: EmpID, Name, Skills (varchar containing "Java, SQL, AWS")

  SOLUTION:
    Problem: Violates 1NF (repeating groups / non-atomic values in Skills). Impossible to efficiently query "all employees with SQL skills" without full table scans and string parsing.
    Answer: Create an EmployeeSkill mapping table.

────────────────────────────────────────────────────────────────────────────────
  9. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  SCHEMA RIGIDITY: Altering massive tables (billions of rows) in production to fix a bad schema design can take hours of downtime. Getting the ERD right initially saves immense pain.
  DATA ANOMALIES: Without normalization, updating a customer's name might require updating 10,000 order records. If one update fails, you have an "update anomaly" (inconsistent data).
  MICROSERVICES: Understanding bounded contexts and entities is critical when splitting a monolithic database into microservice databases.

────────────────────────────────────────────────────────────────────────────────
  10. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

  -> File 027: SQL_Mastery (Applying these theories using SQL.)
  -> File 028: PostgreSQL_MVCC_WAL (How PostgreSQL implements ACID.)
  -> File 033: Database_Comparison (Relational vs NoSQL trade-offs.)

================================================================================
  END OF FILE 026
================================================================================
