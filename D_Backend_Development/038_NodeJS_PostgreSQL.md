================================================================================
  FILE 038: NODEJS POSTGRESQL
  Section: D - Backend Development
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  Node.js Database Integration with PostgreSQL
  PostgreSQL is a powerful, open-source object-relational database. Integrating it with Node.js allows for building robust, data-driven applications. This file covers how to securely and efficiently connect Node.js to PostgreSQL using the `pg` library, handle connection pooling, prevent SQL injection, and manage database schemas via migrations.
  Prerequisites: Node.js, Express.js fundamentals, and basic SQL knowledge (CRUD operations, joins).
  What you'll learn: Client vs. Pool, Connection Pooling architecture, Parameterized Queries, Database Transactions, Migrations, and Query Building basics.
  
  ---

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  `pg` (node-postgres)
    Non-blocking PostgreSQL client for Node.js.

  Client
    A single, persistent connection to the database. Useful for one-off scripts, but terrible for web servers handling concurrent requests.

  Pool (`pg-pool`)
    A cache of reusable database connections. Crucial for web servers to handle multiple concurrent requests without overwhelming the database with new connection handshakes.

  Connection String
    A URL-like string containing all credentials to connect to the DB: `postgresql://user:password@host:port/database`.

  Parameterized Queries
    Separating SQL code from user-provided data using placeholders (`$1, $2`). This is the primary defense against SQL Injection.

  Transactions
    A sequence of database operations treated as a single unit of work (`BEGIN`, `COMMIT`, `ROLLBACK`). Guarantees ACID properties (e.g., deducting from account A and adding to account B must either both succeed or both fail).

  Migrations
    Version control for your database schema. Scripts that safely upgrade (`up`) or downgrade (`down`) tables and columns.

  Query Builder (e.g., Knex.js)
    A library that allows writing SQL queries using JavaScript methods rather than raw strings, abstracting away SQL dialect differences.

  --

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  Connection Pool Architecture

  ┌─────────────────────────────────────────────────────────────────────────┐
  │   Node.js Express App                  Connection Pool (pg-pool)               PostgreSQL Database│
  │  +-------------------+               +-------------------------+               +-------------------+│
  │  | Request 1 (GET)   | -- queries -> | [ Idle Connection 1 ]   | -- queries -> | Database Engine   |│
  │  | Request 2 (POST)  | -- queries -> | [ Idle Connection 2 ]   | -- queries -> |                   |│
  │  | Request 3 (PUT)   | -- queries -> | [ Active Connection 3 ] | -- queries -> |                   |│
  │  | Request 4 (GET)   | -- queries -> | [ Active Connection 4 ] | -- queries -> |                   |│
  │  +-------------------+               | [ Idle Connection 5 ]   |               +-------------------+│
  │                                      +-------------------------+        │
  │                                                                         │
  │  If Request 6 arrives and max size is 5 (all active):                   │
  │  Request 6 is QUEUED in Node.js memory until a connection is returned to the pool.│
  └─────────────────────────────────────────────────────────────────────────┘

---

────────────────────────────────────────────────────────────────────────────────
  5. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  Parameterized Queries & Transactions


  Language: javascript


  ┌──────────────────────────────────────────────────────────────────────────┐
  │  const { Pool } = require('pg');                                         │
  │                                                                          │
  │  const pool = new Pool({                                                 │
  │      connectionString: process.env.DATABASE_URL                          │
  │  });                                                                     │
  │                                                                          │
  │  async function transferFunds(fromAccountId, toAccountId, amount) {      │
  │      // 1. Get a dedicated client from the pool for the transaction      │
  │      const client = await pool.connect();                                │
  │                                                                          │
  │      try {                                                               │
  │          // 2. Begin transaction                                         │
  │          await client.query('BEGIN');                                    │
  │                                                                          │
  │          // 3. Deduct from sender (Parameterized query uses $1, $2)      │
  │          const deductQuery = `                                           │
  │              UPDATE accounts                                             │
  │              SET balance = balance - $1                                  │
  │              WHERE id = $2 AND balance >= $1                             │
  │              RETURNING id;                                               │
  │          `;                                                              │
  │          const res1 = await client.query(deductQuery, [amount, fromAccountId]);│
  │                                                                          │
  │          if (res1.rowCount === 0) {                                      │
  │              throw new Error('Insufficient funds or account not found'); │
  │          }                                                               │
  │                                                                          │
  │          // 4. Add to receiver                                           │
  │          const addQuery = `                                              │
  │              UPDATE accounts                                             │
  │              SET balance = balance + $1                                  │
  │              WHERE id = $2;                                              │
  │          `;                                                              │
  │          await client.query(addQuery, [amount, toAccountId]);            │
  │                                                                          │
  │          // 5. Commit transaction                                        │
  │          await client.query('COMMIT');                                   │
  │          console.log('Transfer successful');                             │
  │                                                                          │
  │      } catch (e) {                                                       │
  │          // 6. Rollback on error                                         │
  │          await client.query('ROLLBACK');                                 │
  │          console.error('Transfer failed, rolled back:', e.message);      │
  │          throw e;                                                        │
  │      } finally {                                                         │
  │          // 7. ALWAYS release the client back to the pool                │
  │          client.release();                                               │
  │      }                                                                   │
  │  }                                                                       │
  └──────────────────────────────────────────────────────────────────────────┘

  ---

────────────────────────────────────────────────────────────────────────────────
  6. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

  Complete CRUD API Setup


  Language: javascript


  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // db.js - Database Configuration                                       │
  │  require('dotenv').config();                                             │
  │  const { Pool } = require('pg');                                         │
  │                                                                          │
  │  const pool = new Pool({                                                 │
  │      user: process.env.DB_USER,                                          │
  │      host: process.env.DB_HOST,                                          │
  │      database: process.env.DB_NAME,                                      │
  │      password: process.env.DB_PASSWORD,                                  │
  │      port: process.env.DB_PORT,                                          │
  │      max: 20, // Max number of connections in the pool                   │
  │      idleTimeoutMillis: 30000, // Close idle clients after 30 seconds    │
  │      connectionTimeoutMillis: 2000, // Return an error after 2 seconds if connection could not be established│
  │  });                                                                     │
  │                                                                          │
  │  module.exports = {                                                      │
  │      // Helper to run queries without manually managing clients          │
  │      query: (text, params) => pool.query(text, params),                  │
  │      pool                                                                │
  │  };                                                                      │
  │                                                                          │
  │  // ==========================================                           │
  │  // server.js - Express App                                              │
  │  // ==========================================                           │
  │  const express = require('express');                                     │
  │  const db = require('./db');                                             │
  │  const app = express();                                                  │
  │  app.use(express.json());                                                │
  │                                                                          │
  │  // GET all users                                                        │
  │  app.get('/api/users', async (req, res) => {                             │
  │      try {                                                               │
  │          const { rows } = await db.query('SELECT id, username, email, created_at FROM users ORDER BY id ASC');│
  │          res.json(rows);                                                 │
  │      } catch (err) {                                                     │
  │          console.error(err);                                             │
  │          res.status(500).json({ error: 'Database error' });              │
  │      }                                                                   │
  │  });                                                                     │
  │                                                                          │
  │  // GET single user                                                      │
  │  app.get('/api/users/:id', async (req, res) => {                         │
  │      try {                                                               │
  │          const { id } = req.params;                                      │
  │          // Parameterized query preventing SQL injection                 │
  │          const { rows } = await db.query('SELECT * FROM users WHERE id = $1', [id]);│
  │                                                                          │
  │          if (rows.length === 0) return res.status(404).json({ error: 'User not found' });│
  │          res.json(rows[0]);                                              │
  │      } catch (err) {                                                     │
  │          res.status(500).json({ error: 'Database error' });              │
  │      }                                                                   │
  │  });                                                                     │
  │                                                                          │
  │  // CREATE user                                                          │
  │  app.post('/api/users', async (req, res) => {                            │
  │      try {                                                               │
  │          const { username, email } = req.body;                           │
  │          const text = 'INSERT INTO users(username, email) VALUES($1, $2) RETURNING *';│
  │          const values = [username, email];                               │
  │                                                                          │
  │          const { rows } = await db.query(text, values);                  │
  │          res.status(201).json(rows[0]);                                  │
  │      } catch (err) {                                                     │
  │          if (err.code === '23505') { // Postgres unique violation error code│
  │              res.status(400).json({ error: 'Email already exists' });    │
  │          } else {                                                        │
  │              res.status(500).json({ error: 'Database error' });          │
  │          }                                                               │
  │      }                                                                   │
  │  });                                                                     │
  │                                                                          │
  │  app.listen(3000, () => console.log('Server running on port 3000'));     │
  └──────────────────────────────────────────────────────────────────────────┘

  Migration Script Example (using `node-pg-migrate`)


  Language: javascript


  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // migrations/162819234_create_users_table.js                           │
  │  exports.up = (pgm) => {                                                 │
  │    pgm.createTable('users', {                                            │
  │      id: 'id', // shorthand for serial primary key                       │
  │      username: { type: 'varchar(50)', notNull: true },                   │
  │      email: { type: 'varchar(255)', notNull: true, unique: true },       │
  │      created_at: {                                                       │
  │        type: 'timestamp',                                                │
  │        notNull: true,                                                    │
  │        default: pgm.func('current_timestamp'),                           │
  │      },                                                                  │
  │    });                                                                   │
  │  };                                                                      │
  │                                                                          │
  │  exports.down = (pgm) => {                                               │
  │    pgm.dropTable('users');                                               │
  │  };                                                                      │
  └──────────────────────────────────────────────────────────────────────────┘

  ---

────────────────────────────────────────────────────────────────────────────────
  7. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: Why use a Connection Pool instead of a single Client?

  ANSWER:
    Establishing a TCP connection to the database is slow and resource-intensive. A single client can only execute one query at a time, blocking concurrent requests. A pool maintains open connections, reusing them across multiple requests, massively improving throughput and reducing latency.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: What is SQL Injection and how do you prevent it in Node.js?

  ANSWER:
    SQL Injection happens when untrusted user input is directly concatenated into a SQL string, allowing attackers to manipulate the query logic (e.g., `WHERE username = '${userInput}'`). Prevent it by ALWAYS using parameterized queries (`$1, $2`), where the database driver safely escapes the data separate from the SQL structure.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: How do transactions work in the `pg` library?

  ANSWER:
    You must check out a specific client from the pool (`pool.connect()`). You send `BEGIN`, execute your queries, and send `COMMIT`. If an error occurs, you catch it and send `ROLLBACK`. Finally, you must call `client.release()` to return the connection to the pool.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: What happens if you forget to call `client.release()`?

  ANSWER:
    The connection remains checked out indefinitely. Eventually, the pool is exhausted (reaches `max` connections), and all subsequent queries will queue up and eventually time out, bringing down the application (Connection Leak).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: Why use Database Migrations instead of manually running SQL scripts?

  ANSWER:
    Migrations provide version control for the database schema. They ensure that all environments (dev, staging, prod) have identical schemas, allow for automated deployments, and provide a rollback mechanism if a deployment introduces breaking database changes.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: What is the N+1 query problem?

  ANSWER:
    Occurs when an application queries a database for a list of $N$ items, then makes an additional query for *each* of those $N$ items to fetch related data. This results in $N+1$ total queries. Fixed by using SQL `JOIN`s or data loading libraries (like DataLoader in GraphQL).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q7: How do you handle schema changes in a zero-downtime deployment?

  ANSWER:
    Break changes into non-destructive steps. E.g., to rename a column: 1) Add new column. 2) Deploy app that writes to both but reads from old. 3) Backfill old data to new column. 4) Deploy app that reads/writes to new column. 5) Drop old column.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q8: What is Knex.js and when should you use it?

  ANSWER:
    Knex is a query builder. It abstracts SQL syntax into JavaScript functions (`knex('users').where('id', 1)`). Use it when building dynamic queries programmatically or if you want an abstraction layer over raw SQL without the heavy overhead of a full ORM.

---

────────────────────────────────────────────────────────────────────────────────
  8. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: The Accidental Injection

  app.get('/search', async (req, res) => {
      const { name } = req.query;
      // We want to find anyone whose name contains the search term
      const query = `SELECT * FROM users WHERE name LIKE '%$1%'`;
      const { rows } = await pool.query(query, [name]);
      res.json(rows);
  });

  SOLUTION:
    What's wrong? Parameter placeholders inside string quotes (`'%$1%'`) are treated as literal strings, not parameters. The query will literally search for the string "$1", and the database driver will complain that parameter 1 was provided but not used.
    Fix: Construct the wildcard in the array: 
`query = 'SELECT * FROM users WHERE name LIKE $1'; pool.query(query, ['%' + name + '%']);`

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─
  CHALLENGE 2: The Pool Exhaustion

  async function updateStatus(userId) {
      const client = await pool.connect();
      const res = await client.query('UPDATE users SET status = $1 WHERE id = $2', ['active', userId]);
      return res.rows[0];
  }

  SOLUTION:
    What's wrong? `client.release()` is never called. Every time this function runs, a connection is permanently lost from the pool.
    Fix: Add a `finally` block that calls `client.release()`. Even better, for single queries, just use `pool.query()` directly, which handles acquiring and releasing automatically.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─
  CHALLENGE 3: Transaction Trouble

  async function bulkInsert() {
      await pool.query('BEGIN');
      await pool.query('INSERT INTO logs (msg) VALUES ($1)', ['Start']);
      await pool.query('INSERT INTO logs (msg) VALUES ($1)', ['End']);
      await pool.query('COMMIT');
  }

  SOLUTION:
    What's wrong? Using `pool.query()` directly for transactions does not guarantee that the same database connection is used for all statements. `BEGIN` might execute on connection A, and the `INSERT` on connection B.
    Fix: You must use `pool.connect()` to get a dedicated client for the lifespan of the transaction.

---


────────────────────────────────────────────────────────────────────────────────
  9. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  - Connection Leaks: A single unreleased client in a high-traffic endpoint will crash a production server within minutes due to pool exhaustion.
  - SQL Injection: The #1 database vulnerability. Hackers use automated tools to find endpoints not using parameterized queries to dump your entire user table.
  - Transactions for Data Integrity: If an API crashes halfway through processing an order, transactions ensure you don't charge the customer's credit card without actually creating the order in the database.
  ---

────────────────────────────────────────────────────────────────────────────────
  10. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

  -> File 37: ExpressJS (Integrating the database pool with Express routers.)
  -> File 39: NodeJS Auth Security (How to safely store passwords in PostgreSQL using bcrypt.)
  -> File 43: Python SQLAlchemy (Compare Node.js raw SQL queries with Python's ORM approach.)

================================================================================
  END OF FILE 038
================================================================================
