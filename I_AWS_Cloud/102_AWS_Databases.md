================================================================================
  FILE 102: AWS DATABASES: RELATIONAL, NOSQL, AND IN-MEMORY CACHING
  Section: I - AWS Cloud Services
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  Modern applications rely heavily on databases, and AWS provides a suite of purpose-built database services. Instead of managing database software, backups, and failovers manually on EC2, AWS offers fully managed services. This file covers RDS for relational workloads, DynamoDB for high-scale NoSQL, and ElastiCache for in-memory caching.

  Prerequisites: Understanding of basic database concepts (SQL vs NoSQL).

  What you'll learn: 
  * RDS managed features (Multi-AZ, Read Replicas).
  * Aurora architecture and serverless options.
  * DynamoDB core concepts (Partition keys, Sort keys, GSIs).
  * ElastiCache for Redis and Memcached.
  * How to choose the right database for the right workload.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  RDS (RELATIONAL DATABASE SERVICE)
    A managed service that makes it easy to set up, operate, and scale a relational database (PostgreSQL, MySQL, MariaDB, Oracle, SQL Server) in the cloud.

  MULTI-AZ
    A synchronous replication feature in RDS where AWS automatically maintains a standby replica of your database in a different Availability Zone. If the primary DB fails, AWS automatically fails over to the standby. (Used for High Availability/Disaster Recovery, NOT performance scaling).

  READ REPLICAS
    Asynchronous copies of your primary DB instance. Used to scale read workloads. You can have up to 15 read replicas, and they can be cross-region.

  AURORA
    AWS's proprietary, cloud-native relational database that is MySQL and PostgreSQL compatible. It replicates data 6 ways across 3 AZs automatically and is up to 5x faster than standard MySQL.

  AURORA SERVERLESS
    An on-demand, auto-scaling configuration for Aurora where the database automatically starts up, shuts down, and scales capacity up or down based on application needs.

  DYNAMODB
    A fully managed, serverless, NoSQL key-value and document database designed to deliver single-digit millisecond performance at any scale.

  PARTITION KEY (HASH KEY)
    Determines the physical partition (server) where the data is stored in DynamoDB. Must be unique if no sort key is used.

  SORT KEY (RANGE KEY)
    Combined with the Partition Key to form a composite primary key, allowing multiple items with the same partition key. Data is stored sorted by this key.

  GSI (GLOBAL SECONDARY INDEX)
    An index in DynamoDB with a partition key and a sort key that can be different from those on the base table. Used to enable queries on non-primary key attributes.

  DYNAMODB STREAMS
    A time-ordered sequence of item-level changes (inserts, updates, deletes) in a DynamoDB table. Often used to trigger Lambda functions in real-time.

  DAX (DYNAMODB ACCELERATOR)
    A fully managed, highly available, in-memory cache for DynamoDB that delivers up to a 10x performance improvement (from milliseconds to microseconds).

  ELASTICACHE
    A managed, in-memory caching service compatible with Redis or Memcached. Used to offload read traffic from primary databases and store session data.

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  RDS Multi-AZ Failover Architecture                                     │
  │                                                                         │
  │                              +-------------------+                      │
  │                              |  Application EC2  |                      │
  │                              +---------+---------+                      │
  │                                        | (Writes & Reads)               │
  │                                        |                                │
  │                  Endpoint (DNS points to Primary automatically)         │
  │                                        |                                │
  │         ===============================|=============================== │
  │         |           Availability Zone A (Primary)                     | │
  │         |                                                             | │
  │         |   +-----------------------+     +-----------------------+   | │
  │         |   | RDS Primary Instance  |====>|  EBS Volume (Data)    |   | │
  │         |   +-----------------------+     +-----------------------+   | │
  │         |               |                                             | │
  │         ================|============================================== │
  │                         |                                               │
  │                         | (Synchronous Replication)                     │
  │                         v                                               │
  │         ================|============================================== │
  │         |           Availability Zone B (Standby)                     | │
  │         |                                                             | │
  │         |   +-----------------------+     +-----------------------+   | │
  │         |   | RDS Standby Instance  |====>|  EBS Volume (Data)    |   | │
  │         |   +-----------------------+     +-----------------------+   | │
  │         |  (Inactive until failover)                                  | │
  │         =============================================================== │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  DynamoDB Partition and Sort Key Structure                              │
  │                                                                         │
  │   Table: "UserOrders" (Partition Key: UserID, Sort Key: OrderTimestamp) │
  │                                                                         │
  │   +----------------+----------------------+----------------+-------+    │
  │   | UserID (PK)    | OrderTimestamp (SK)  | TotalAmount    | Status|    │
  │   +----------------+----------------------+----------------+-------+    │
  │   | user_123       | 2023-10-01T14:30:00Z | $45.00         | Shipped    │
  │   | user_123       | 2023-11-15T09:15:00Z | $120.00        | Pending    │
  │   | user_123       | 2023-12-05T18:45:00Z | $15.50         | Shipped    │
  │   |----------------|----------------------|----------------|-------|    │
  │   | user_456       | 2023-10-05T10:00:00Z | $99.99         | Shipped    │
  │   +----------------+----------------------+----------------+-------+    │
  │     ^                      ^                                            │
  │     |                      |                                            │
  │   Determines physical      Determines sort order within that partition. │
  │   partition/server.        Allows querying: "Get all orders for user_123│
  │                            between Oct and Dec."                        │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  Language: Python

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // DynamoDB Operations (Python/Boto3)                                   │
  │                                                                          │
  │  import boto3                                                            │
  │  from boto3.dynamodb.conditions import Key                               │
  │                                                                          │
  │  dynamodb = boto3.resource('dynamodb', region_name='us-east-1')          │
  │  table = dynamodb.Table('UserOrders')                                    │
  │                                                                          │
  │  def add_order(user_id, timestamp, amount, status):                      │
  │      """Inserts a new order into DynamoDB."""                            │
  │      table.put_item(                                                     │
  │          Item={                                                          │
  │              'UserID': user_id,                                          │
  │              'OrderTimestamp': timestamp,                                │
  │              'TotalAmount': amount,                                      │
  │              'Status': status                                            │
  │          }                                                               │
  │      )                                                                   │
  │      print(f"Added order for {user_id}")                                 │
  │                                                                          │
  │  def get_recent_orders(user_id, start_date):                             │
  │      """Queries orders for a specific user after a certain date."""      │
  │      response = table.query(                                             │
  │          KeyConditionExpression=Key('UserID').eq(user_id) & Key('OrderTimestamp').gt(start_date)│
  │      )                                                                   │
  │      return response['Items']                                            │
  │                                                                          │
  │  # Usage                                                                 │
  │  # add_order('user_123', '2023-10-01T14:30:00Z', 45.00, 'Shipped')       │
  │  # items = get_recent_orders('user_123', '2023-01-01T00:00:00Z')         │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

  Language: Python

  ┌──────────────────────────────────────────────────────────────────────────┐
  │                                                                          │
  │  import sys                                                              │
  │  import logging                                                          │
  │  import pymysql                                                          │
  │  import boto3                                                            │
  │  import json                                                             │
  │  import os                                                               │
  │                                                                          │
  │  logger = logging.getLogger()                                            │
  │  logger.setLevel(logging.INFO)                                           │
  │                                                                          │
  │  # ==============================================================================│
  │  # Database Connection Logic (Outside Handler)                           │
  │  # Ensures connection is reused across warm starts to prevent connection exhaustion│
  │  # ==============================================================================│
  │  SECRET_NAME = os.environ['DB_SECRET_NAME']                              │
  │  REGION_NAME = os.environ['AWS_REGION']                                  │
  │                                                                          │
  │  def get_db_credentials():                                               │
  │      session = boto3.session.Session()                                   │
  │      client = session.client(service_name='secretsmanager', region_name=REGION_NAME)│
  │      try:                                                                │
  │          response = client.get_secret_value(SecretId=SECRET_NAME)        │
  │          return json.loads(response['SecretString'])                     │
  │      except Exception as e:                                              │
  │          logger.error(f"Failed to fetch secret: {e}")                    │
  │          sys.exit(1)                                                     │
  │                                                                          │
  │  creds = get_db_credentials()                                            │
  │  try:                                                                    │
  │      conn = pymysql.connect(                                             │
  │          host=creds['host'],                                             │
  │          user=creds['username'],                                         │
  │          passwd=creds['password'],                                       │
  │          db=creds['dbname'],                                             │
  │          connect_timeout=5,                                              │
  │          cursorclass=pymysql.cursors.DictCursor                          │
  │      )                                                                   │
  │      logger.info("SUCCESS: Connection to RDS MySQL instance succeeded")  │
  │  except pymysql.MySQLError as e:                                         │
  │      logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")│
  │      logger.error(e)                                                     │
  │      sys.exit(1)                                                         │
  │                                                                          │
  │  def lambda_handler(event, context):                                     │
  │      """                                                                 │
  │      Executes a simple query using the pre-established connection.       │
  │      """                                                                 │
  │      user_id = event.get('user_id')                                      │
  │      if not user_id:                                                     │
  │          return {"statusCode": 400, "body": "Missing user_id"}           │
  │                                                                          │
  │      try:                                                                │
  │          with conn.cursor() as cur:                                      │
  │              cur.execute("SELECT id, name, email FROM users WHERE id = %s", (user_id,))│
  │              user = cur.fetchone()                                       │
  │                                                                          │
  │          # Do NOT close the connection here, let it stay alive for the next warm start.│
  │          # conn.commit() if doing writes.                                │
  │                                                                          │
  │          if user:                                                        │
  │              return {"statusCode": 200, "body": json.dumps(user)}        │
  │          else:                                                           │
  │              return {"statusCode": 404, "body": "User not found"}        │
  │                                                                          │
  │      except pymysql.MySQLError as e:                                     │
  │          logger.error(f"Database execution error: {e}")                  │
  │          return {"statusCode": 500, "body": "Database Error"}            │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  7. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: What is the primary difference between RDS Multi-AZ and RDS Read Replicas?

  ANSWER:
    Multi-AZ is for Disaster Recovery and High Availability; it uses synchronous replication, but you cannot connect to the standby instance to run queries. Read Replicas are for performance scaling; they use asynchronous replication, and you can connect to them to offload read-heavy workloads from the primary DB.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: Why would you choose DynamoDB over RDS PostgreSQL for an application?

  ANSWER:
    DynamoDB is chosen for highly variable, massive-scale workloads requiring single-digit millisecond latency regardless of data size (e.g., IoT telemetry, gaming leaderboards, shopping carts). It is fully serverless. PostgreSQL is chosen when complex queries, joins, ACID transactions, and strict relational schemas are required.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: Explain the problem of a "Hot Partition" in DynamoDB.

  ANSWER:
    DynamoDB splits data across physical servers based on the Partition Key. If a Partition Key is poorly chosen (e.g., Status=Active where 90% of items are active), all traffic hits a single physical server, throttling throughput and neutralizing DynamoDB's scale advantage. Keys must have high cardinality (e.g., UserID or DeviceID).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: How does Aurora achieve its high durability and performance compared to standard RDS?

  ANSWER:
    Aurora separates the compute and storage layers. The storage layer automatically replicates 6 copies of data across 3 Availability Zones. It reduces network IO bottlenecks by only sending log records (not whole data pages) to the storage nodes, making it significantly faster than standard MySQL/PostgreSQL.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: What is ElastiCache and what problem does it solve?

  ANSWER:
    ElastiCache is a managed in-memory datastore (Redis or Memcached). It solves the problem of high database load and latency by caching frequently accessed data (like top 10 articles, or user session states) in memory, serving it in microseconds rather than hitting the disk-based primary database.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: Can you use DynamoDB Streams with AWS Lambda? How?

  ANSWER:
    Yes, it is a highly common event-driven pattern. When an item is inserted, updated, or deleted in DynamoDB, a record is written to the Stream. Lambda can poll this stream and trigger a function automatically (e.g., sending a welcome email when a new user is inserted).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q7: What happens to an RDS instance during the automated backup window?

  ANSWER:
    Automated backups create a storage volume snapshot. For Single-AZ instances, I/O is briefly suspended and you may experience elevated latency. For Multi-AZ instances, the backup is taken from the standby instance, so there is zero I/O suspension on the primary instance.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q8: What is the difference between On-Demand and Provisioned capacity in DynamoDB?

  ANSWER:
    Provisioned requires you to specify the exact number of Read/Write Capacity Units (RCU/WCU) per second you need (cheaper for predictable workloads). On-Demand automatically scales up and down instantly, charging you per request (ideal for unpredictable, spiky workloads).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q9: What is Aurora Serverless and when should it be used?

  ANSWER:
    Aurora Serverless automatically scales the database compute capacity up and down based on application load. It is ideal for infrequent, intermittent, or unpredictable workloads (like dev/test environments or new apps with unknown traffic) where paying for a 24/7 DB instance would be wasteful.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q10: What is a Global Secondary Index (GSI) in DynamoDB?

  ANSWER:
    A GSI allows you to query a table using attributes other than the primary key. It creates a secondary copy of the data, organized by the new partition/sort key, which is kept in sync asynchronously.

────────────────────────────────────────────────────────────────────────────────
  8. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: Riddle 1

  I am lightning fast and live purely in memory. When the server reboots, everything inside me vanishes. I am used to shield databases from repetitive questions. What am I?

  SOLUTION:
    ElastiCache (Memcached/Redis).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 2: Riddle 2

  You tell me to write to my primary side, and I instantly, quietly whisper it to my shadow in another zone. You can't read from my shadow, but if I die, my shadow takes my place instantly. What am I?

  SOLUTION:
    RDS Multi-AZ.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 3: What's Wrong With This Design?

  Scenario: A developer wants to query DynamoDB to find all users whose `age > 30` and `city == 'New York'`. Their Partition Key is `UserID`. They write a `Scan` operation with a filter expression on Age and City to get the results.

  SOLUTION:
    A `Scan` operation reads every single item in the entire database table before applying the filter. If the table has a million users, it consumes massive amounts of read capacity and is incredibly slow/expensive. They should create a GSI (Global Secondary Index) with `City` as the Partition Key and `Age` as the Sort Key, and perform a `Query` instead.

────────────────────────────────────────────────────────────────────────────────
  9. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  * Database Scaling: Monolithic databases are usually the first thing to break under scale. Using ElastiCache to offload reads, or RDS Read Replicas, is often the difference between an application staying up during a viral event versus completely crashing.
  * Cost Overruns: DynamoDB `Scans` can cost thousands of dollars if run frequently on large tables. Understanding NoSQL access patterns and using `Queries` is mandatory for cloud engineers.
  * Disaster Recovery: A single AZ failure can wipe out a company if they run a database on a single EC2 instance without backups. RDS Multi-AZ ensures that hardware failures are handled automatically with minimal RPO/RTO (Recovery Point/Time Objectives).

────────────────────────────────────────────────────────────────────────────────
  10. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

  -> File 100: AWS Compute (How Lambda and EC2 connect to these databases)
  -> File 104: AWS Security (Using Secrets Manager for database credentials)
  -> File 106: AWS Architecture Patterns (How databases fit into 3-tier and serverless architectures)

================================================================================
  END OF FILE 102
================================================================================
