================================================================================
  FILE 031: MONGODB: THE DOCUMENT DATABASE
  Section: C - DBMS & Databases
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  This document covers MongoDB, the leading NoSQL document database. It explores how to store data as flexible JSON-like documents (BSON), when to use embedding vs referencing, and how to query, aggregate, and scale databases horizontally. You will learn about the Aggregation Pipeline, Replica Sets for high availability, and Sharding for massive scale. Prerequisites include basic understanding of JSON and database concepts.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  DOCUMENT
    A record in MongoDB, formatted as BSON (Binary JSON), consisting of field-value pairs.

  COLLECTION
    A group of MongoDB documents (analogous to a relational table).

  DATABASE
    A physical container for collections.

  BSON
    Binary representation of JSON, extending JSON with additional types (Date, ObjectId, Regex, binary data).

  EMBEDDED DOCUMENT
    A document nested inside another document. Promotes locality of reference (single read operation).

  REFERENCE
    Storing a link (usually _id) to a document in another collection (analogous to a Foreign Key, but application-managed).

  REPLICA SET
    A group of mongod processes that maintain the same data set. Provides redundancy and high availability.

  SHARDING
    The process of distributing data across multiple machines.

  SHARD KEY
    A field or fields that exist in every document, used by MongoDB to distribute the collection's documents across shards.

  ODM (OBJECT DATA MODELING)
    e.g., Mongoose. A library that provides schema validation and relationship management in application code.

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  REPLICA SET ARCHITECTURE                                               │
  │                                                                         │
  │             [ Client Application ]                                      │
  │                      |                                                  │
  │        +-------------+-------------+                                    │
  │        | (Reads/Writes)            | (Failover)                         │
  │        v                           |                                    │
  │  [ PRIMARY Node ]                  |                                    │
  │    |       |                       |                                    │
  │  (Oplog) (Oplog)                   |                                    │
  │    |       |                       v                                    │
  │    v       v                 [ ARBITER Node ] (Optional)                │
  │  [ SECONDARY ]              (Only votes in elections, holds no data)    │
  │  [ SECONDARY ]                                                          │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘
  If Primary fails, Secondaries hold an election to promote a new Primary.

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  SHARDED CLUSTER ARCHITECTURE                                           │
  │                                                                         │
  │         [ Client App ]                                                  │
  │               |                                                         │
  │         [ mongos (Router) ] ---> (Queries Config Servers for routing rules)│
  │               |                                                         │
  │     +---------+---------+                                               │
  │     |                   |                                               │
  │  [ Shard 1 ]         [ Shard 2 ]  <-- Each Shard is a Replica Set       │
  │  (A - M)             (N - Z)      <-- Data split by Shard Key           │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: JAVASCRIPT]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // CRUD & Query Operators                                               │
  │                                                                          │
  │  // Using MongoDB Node.js Driver / Mongo Shell                           │
  │                                                                          │
  │  // 1. Insert                                                            │
  │  db.users.insertMany([                                                   │
  │    { name: "Alice", age: 28, skills: ["Node", "React"] },                │
  │    { name: "Bob", age: 35, skills: ["Python", "Mongo"] }                 │
  │  ]);                                                                     │
  │                                                                          │
  │  // 2. Query (Find)                                                      │
  │  // $gt = Greater Than, $in = In Array                                   │
  │  db.users.find({                                                         │
  │    age: { $gt: 30 },                                                     │
  │    skills: { $in: ["Mongo", "AWS"] }                                     │
  │  });                                                                     │
  │                                                                          │
  │  // 3. Update                                                            │
  │  db.users.updateOne(                                                     │
  │    { name: "Alice" },                                                    │
  │    {                                                                     │
  │      $set: { age: 29 },                                                  │
  │      $push: { skills: "Docker" } // Append to array                      │
  │    }                                                                     │
  │  );                                                                      │
  │                                                                          │
  │  // 4. Delete                                                            │
  │  db.users.deleteOne({ name: "Bob" });                                    │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: JAVASCRIPT]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // The Aggregation Pipeline                                             │
  │                                                                          │
  │  // Scenario: Find total revenue per category for active products        │
  │  db.orders.aggregate([                                                   │
  │    // 1. Filter (WHERE)                                                  │
  │    { $match: { status: "completed" } },                                  │
  │    // 2. Join (LEFT JOIN)                                                │
  │    {                                                                     │
  │      $lookup: {                                                          │
  │        from: "products",                                                 │
  │        localField: "productId",                                          │
  │        foreignField: "_id",                                              │
  │        as: "productDetails"                                              │
  │      }                                                                   │
  │    },                                                                    │
  │    // 3. Unwind array from lookup (flatten)                              │
  │    { $unwind: "$productDetails" },                                       │
  │    // 4. Group and aggregate (GROUP BY)                                  │
  │    {                                                                     │
  │      $group: {                                                           │
  │        _id: "$productDetails.category",                                  │
  │        totalRevenue: { $sum: { $multiply: ["$quantity", "$price"] } }    │
  │      }                                                                   │
  │    },                                                                    │
  │    // 5. Sort (ORDER BY)                                                 │
  │    { $sort: { totalRevenue: -1 } }                                       │
  │  ]);                                                                     │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘
  Powerful framework for data transformation (similar to SQL GROUP BY + Window functions).

  [Language: JAVASCRIPT]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Mongoose ODM (Node.js)                                               │
  │                                                                          │
  │  const mongoose = require('mongoose');                                   │
  │                                                                          │
  │  // Schema with Validation                                               │
  │  const userSchema = new mongoose.Schema({                                │
  │    email: { type: String, required: true, unique: true },                │
  │    passwordHash: { type: String, required: true },                       │
  │    role: { type: String, enum: ['user', 'admin'], default: 'user' },     │
  │    posts: [{ type: mongoose.Schema.Types.ObjectId, ref: 'Post' }] // References│
  │  }, { timestamps: true });                                               │
  │                                                                          │
  │  // Pre-save Middleware (Hooks)                                          │
  │  userSchema.pre('save', async function(next) {                           │
  │    if (this.isModified('passwordHash')) {                                │
  │      // Hash password before saving                                      │
  │      // this.passwordHash = await bcrypt.hash(this.passwordHash, 10);    │
  │    }                                                                     │
  │    next();                                                               │
  │  });                                                                     │
  │                                                                          │
  │  const User = mongoose.model('User', userSchema);                        │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  7. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: When would you embed a document vs reference it?

  ANSWER:
    Embed when the data is queried together (1:1 or 1:few), doesn't change frequently, and won't exceed the 16MB document limit. Reference when data is frequently updated, shared across multiple entities (N:M), or constitutes a massive array (1:many unbounded).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: What is an ObjectId?

  ANSWER:
    A 12-byte BSON type used for _id. It consists of a 4-byte timestamp, 5-byte random value, and 3-byte incrementing counter. It guarantees uniqueness and naturally sorts by creation time.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: Explain the phases of the Aggregation Pipeline.

  ANSWER:
    Documents pass through a sequence of stages. E.g., $match filters documents, $group aggregates them, $project shapes the output, $sort orders them. Output from one stage is input to the next.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: What is a Replica Set and how does Failover work?

  ANSWER:
    A cluster of MongoDB nodes holding the same data. One Primary handles writes; Secondaries replicate the oplog. If the Primary drops, Secondaries hold an election and the one with the most up-to-date oplog becomes the new Primary.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: What is the oplog?

  ANSWER:
    The Operations Log. A capped collection that keeps a rolling record of all operations that modify data. Secondaries apply operations from the Primary's oplog to replicate data.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: How do you choose a Shard Key?

  ANSWER:
    A good shard key has high cardinality (many distinct values), even distribution (no single value dominates), and aligns with query patterns. Hash-based sharding ensures even distribution, while range-based sharding optimizes range queries.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q7: What is a Covered Query?

  ANSWER:
    A query where all fields being filtered and returned are present in the index. MongoDB can fulfill the query entirely from RAM without examining the actual documents (similar to an Index-Only Scan in SQL).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q8: Does MongoDB support ACID transactions?

  ANSWER:
    Yes, starting in v4.0, MongoDB supports multi-document ACID transactions across replica sets, and in v4.2 across sharded clusters. However, they incur a performance cost.

────────────────────────────────────────────────────────────────────────────────
  8. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: The Exploding Array

  // A blog post document
  {
    _id: 1,
    title: "My popular post",
    comments: [ { user: "A", msg: "Hi"}, /* ... 500,000 more comments ... */ ]
  }

  SOLUTION:
    Problem: Unbounded array growth. MongoDB has a strict 16MB limit per document. Appending indefinitely will eventually throw a BSONObjectTooLarge exception.
    Answer: Use the "Subset Pattern" (embed the 50 most recent comments, put the rest in a separate Comments collection with a reference).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 2: The Missing Index

  db.users.createIndex({ "address.city": 1 });
  db.users.find({ address: { city: "New York", state: "NY" } });

  SOLUTION:
    Problem: The query asks for exact equality on the address object, which bypasses the index on address.city. It expects the object fields to match exactly, in exact order.
    Answer: Query the specific field using dot notation: db.users.find({ "address.city": "New York" }).

────────────────────────────────────────────────────────────────────────────────
  9. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  SCHEMA FLEXIBILITY: In an agile startup, schema changes happen daily. RDBMS ALTER TABLE locks can cause downtime. MongoDB allows iterative development where code defines the schema (via ODM).
  MASSIVE SCALE: While scaling PostgreSQL requires complex logical replication or Application-level sharding, MongoDB was built with automatic Sharding as a first-class citizen, making horizontal scaling transparent to the app.

────────────────────────────────────────────────────────────────────────────────
  10. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

  -> File 033: Database_Comparison (RDBMS vs Document DBs.)
  -> File 034: Database_Scaling (Deep dive into Sharding.)

================================================================================
  END OF FILE 031
================================================================================
