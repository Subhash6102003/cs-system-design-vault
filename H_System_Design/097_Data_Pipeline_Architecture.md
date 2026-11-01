================================================================================
  FILE 097: DATA PIPELINE ARCHITECTURE
  Section: H - System Design at Scale
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  Data Pipeline Architecture focuses on the movement, transformation, and storage of massive datasets for analytics and machine learning. Prerequisites include SQL and basic message queues. You will learn the difference between ETL and ELT, Batch vs Stream processing, the Lambda/Kappa architectures, and Event Sourcing.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  ETL (EXTRACT, TRANSFORM, LOAD)
    Data is extracted, transformed in an external compute engine, and loaded into the Data Warehouse.

  ELT (EXTRACT, LOAD, TRANSFORM)
    Data is extracted and loaded raw into the Warehouse; transformation happens inside the warehouse using its massive compute power (e.g., Snowflake, BigQuery).

  BATCH PROCESSING
    Processing large volumes of data at scheduled intervals (e.g., nightly Hadoop/Spark jobs).

  STREAM PROCESSING
    Processing data in real-time as it arrives (e.g., Apache Kafka Streams, Flink).

  LAMBDA ARCHITECTURE
    A hybrid data system with a Batch Layer (accurate, slow) and a Speed Layer (real-time, approx) that merge into a Serving Layer.

  KAPPA ARCHITECTURE
    Simplifies Lambda by removing the Batch layer—everything is treated as an immutable stream.

  DATA LAKE VS DATA WAREHOUSE
    Lake is raw, unstructured (Schema-on-Read). Warehouse is structured, relational (Schema-on-Write).

  EVENT SOURCING
    Storing the history of state changes as an immutable sequence of events, rather than just storing the current state.

  CQRS (COMMAND QUERY RESPONSIBILITY SEGREGATION)
    Separating the write model (Commands) from the read model (Queries).

  CDC (CHANGE DATA CAPTURE)
    Tapping into a database's Write-Ahead Log (WAL) to stream row-level changes in real-time (e.g., Debezium).

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  LAMBDA ARCHITECTURE                                                    │
  │                                                                         │
  │                       +--> [ Batch Layer (Hadoop/Spark) ] ------+       │
  │                       |                                         v       │
  │  [ New Data Stream ] -+                                  [ Serving Layer (DB) ] -> [ BI / UI ]│
  │                       |                                         ^       │
  │                       +--> [ Speed Layer (Storm/Flink) ] -------+       │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  CQRS WITH EVENT SOURCING                                               │
  │                                                                         │
  │  [ Client ] --(Write Command)--> [ Command Service ] -> Stores Event in [ Event Store (Kafka/DB) ]│
  │                                                                  |      │
  │                                                            (Async Event)│
  │                                                                  v      │
  │  [ Client ] <-----(Read Query)-- [ Query Service ]   <- Updates [ Read DB (Elasticsearch/Redis) ]│
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  4. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: python]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Conceptual Event Sourcing                                            │
  │                                                                          │
  │  class BankAccount:                                                      │
  │      def __init__(self):                                                 │
  │          self.balance = 0                                                │
  │          self.events = [] # Event Store                                  │
  │                                                                          │
  │      def deposit(self, amount):                                          │
  │          event = {"type": "DEPOSIT", "amount": amount}                   │
  │          self.events.append(event)                                       │
  │          self.apply(event)                                               │
  │                                                                          │
  │      def withdraw(self, amount):                                         │
  │          if self.balance >= amount:                                      │
  │              event = {"type": "WITHDRAW", "amount": amount}              │
  │              self.events.append(event)                                   │
  │              self.apply(event)                                           │
  │                                                                          │
  │      def apply(self, event):                                             │
  │          # The projection logic                                          │
  │          if event["type"] == "DEPOSIT":                                  │
  │              self.balance += event["amount"]                             │
  │          elif event["type"] == "WITHDRAW":                               │
  │              self.balance -= event["amount"]                             │
  │                                                                          │
  │  # State can be entirely rebuilt by replaying events                     │
  │  account = BankAccount()                                                 │
  │  account.deposit(100)                                                    │
  │  account.withdraw(40)                                                    │
  │  print(f"Current Balance: {account.balance}") # 60                       │
  │  print(f"Audit Log: {account.events}")                                   │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: sql]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │                                                                          │
  │  -- Transformation in an ELT Pipeline (dbt / BigQuery)                   │
  │  -- Raw data was loaded directly from Kafka to raw.pageviews via CDC     │
  │                                                                          │
  │  -- Create a materialized view or scheduled table for the transformed data│
  │  CREATE OR REPLACE TABLE analytics.daily_user_engagement AS              │
  │  WITH raw_views AS (                                                     │
  │      SELECT                                                              │
  │          user_id,                                                        │
  │          page_url,                                                       │
  │          CAST(timestamp AS TIMESTAMP) as view_time                       │
  │      FROM                                                                │
  │          raw.pageviews                                                   │
  │      WHERE                                                               │
  │          DATE(timestamp) = CURRENT_DATE() - 1                            │
  │  ),                                                                      │
  │  sessionized AS (                                                        │
  │      SELECT                                                              │
  │          user_id,                                                        │
  │          COUNT(DISTINCT page_url) as unique_pages,                       │
  │          MIN(view_time) as first_view,                                   │
  │          MAX(view_time) as last_view                                     │
  │      FROM                                                                │
  │          raw_views                                                       │
  │      GROUP BY                                                            │
  │          user_id                                                         │
  │  )                                                                       │
  │  SELECT                                                                  │
  │      user_id,                                                            │
  │      unique_pages,                                                       │
  │      TIMESTAMP_DIFF(last_view, first_view, MINUTE) as session_length_minutes│
  │  FROM                                                                    │
  │      sessionized;                                                        │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: Why is ELT replacing ETL in modern architectures?

  ANSWER:
    Cloud Data Warehouses (Snowflake, BigQuery) have decoupled compute and storage, making them powerful enough to do transformations in-database using SQL. It removes the need for separate Spark/Hadoop ETL clusters.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: What is the difference between a Data Lake and a Data Warehouse?

  ANSWER:
    A Lake stores raw data in cheap object storage (S3) in formats like Parquet (Schema-on-Read). A Warehouse stores structured, relational data optimized for fast BI querying (Schema-on-Write).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: What is Change Data Capture (CDC)?

  ANSWER:
    A technique to stream database changes. Instead of querying SELECT * FROM users WHERE updated_at > X (polling), a tool like Debezium reads the database's internal Write-Ahead Log (WAL) and streams inserts/updates to Kafka.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: Explain the Lambda Architecture.

  ANSWER:
    It processes data twice. The Speed Layer gives low-latency approximate results (e.g., real-time dashboard). The Batch Layer runs overnight, providing highly accurate, fully reconciled data that overwrites the Speed Layer's approximations.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: Why use Event Sourcing?

  ANSWER:
    It provides a perfect audit trail, allows for time-travel debugging (rebuilding state at any point in time), and makes it easy to build new read-projections later (e.g., adding an Elasticsearch view years later by replaying the event log).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: What is the trade-off of CQRS?

  ANSWER:
    It allows extreme optimization of both Read and Write models independently. The tradeoff is complexity and Eventual Consistency (the Read DB lags behind the Write DB).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q7: Batch vs Stream Processing?

  ANSWER:
    Batch handles massive bounded datasets efficiently (high throughput, high latency). Stream handles unbounded continuous data (lower throughput per node, millisecond latency).

────────────────────────────────────────────────────────────────────────────────
  7. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: Riddle 1

  "I am the ledger of all that has ever happened. You cannot change my past, but from my past, you can build any future."

  SOLUTION:
    Problem: 
    Fix: An Event Store (Event Sourcing).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 2: Riddle 2

  # Polling for database changes
  while True:
      new_rows = db.query("SELECT * FROM orders WHERE status = 'NEW'")
      for row in new_rows:
          send_to_kafka(row)
          db.query("UPDATE orders SET status = 'PROCESSED' WHERE id = ?", row.id)
      time.sleep(5)

  SOLUTION:
    Problem: 
    Fix: This polling architecture is slow, puts heavy load on the DB, and risks missing data if the DB crashes between updates. CDC (reading the WAL) is the production solution.

────────────────────────────────────────────────────────────────────────────────
  8. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  Without proper data pipelines, Machine Learning models train on garbage, BI dashboards crash under load, and executives make decisions on stale data. Event Sourcing and CDC are the backbone of modern microservices, preventing distributed data monoliths and enabling true real-time analytics.

────────────────────────────────────────────────────────────────────────────────
  9. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

  -> File 092: Design Instagram (Async ML pipelines)
  -> File 096: Distributed Systems (CRDTs vs Event Sourcing)

================================================================================
  END OF FILE 097
================================================================================
