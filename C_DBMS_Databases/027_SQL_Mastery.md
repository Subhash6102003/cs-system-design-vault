================================================================================
  FILE 027: SQL MASTERY: ADVANCED QUERYING AND DATA MANIPULATION
  Section: C - DBMS & Databases
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  This document transitions from database theory into practical execution. It covers advanced SQL concepts essential for backend engineering and data analysis. Prerequisites include basic SQL syntax. You will learn to write complex joins, leverage window functions, master aggregations, utilize Common Table Expressions (CTEs), and handle concurrency with UPSERTs.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  DQL (DATA QUERY LANGUAGE)
    Statements used to query data (SELECT).

  DML (DATA MANIPULATION LANGUAGE)
    Statements used to modify data (INSERT, UPDATE, DELETE).

  DDL (DATA DEFINITION LANGUAGE)
    Statements used to define schemas (CREATE, ALTER, DROP).

  JOIN
    Combining rows from two or more tables based on a related column.

  CTE (COMMON TABLE EXPRESSION)
    A temporary named result set created via the WITH clause, improving readability.

  WINDOW FUNCTION
    Functions that perform calculations across a set of table rows related to the current row, without collapsing them into a single output row.

  SUBQUERY
    A query nested inside another query.
    - Correlated: The inner query depends on values from the outer query.
    - Non-Correlated: The inner query can be run independently.

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  SQL JOINS VENN DIAGRAMS                                                │
  │                                                                         │
  │  INNER JOIN              LEFT JOIN               RIGHT JOIN              FULL OUTER JOIN│
  │  Intersection            All Left + Match Right  All Right + Match Left  Everything│
  │     ___       ___           ___       ___           ___       ___           ___       ___    │
  │    /   \     /   \         /   \     /   \         /   \     /   \         /   \     /   \   │
  │   /  A  ( A∩B )  B  \     /  A  ( A∩B )  B  \     /  A  ( A∩B )  B  \     /  A  ( A∩B )  B  \  │
  │   \     / \     /         \+++++/ \     /         \     / \+++++/         \+++++/ \+++++/  │
  │    \___/   \___/           \___/   \___/           \___/   \___/           \___/   \___/   │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  WINDOW FUNCTIONS VS AGGREGATE FUNCTIONS                                │
  │                                                                         │
  │  Aggregate (GROUP BY): Multiple Rows -> Single Row Output               │
  │  [Row 1, Row 2, Row 3] => SUM() => [Result]                             │
  │                                                                         │
  │  Window Function (OVER): Multiple Rows -> Multiple Row Outputs          │
  │  [Row 1] => SUM() OVER (...) => [Row 1 + Result]                        │
  │  [Row 2] => SUM() OVER (...) => [Row 2 + Result]                        │
  │  [Row 3] => SUM() OVER (...) => [Row 3 + Result]                        │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: SQL]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Filtering & Sorting                                                  │
  │                                                                          │
  │  SELECT employee_id, first_name, salary                                  │
  │  FROM employees                                                          │
  │  WHERE department = 'Engineering' AND salary > 100000                    │
  │  ORDER BY salary DESC, first_name ASC                                    │
  │  LIMIT 10 OFFSET 20; -- Pagination: gets rows 21-30                      │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

  [Language: SQL]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Advanced Joins & Aggregation                                         │
  │                                                                          │
  │  SELECT                                                                  │
  │      d.department_name,                                                  │
  │      COUNT(e.employee_id) AS total_employees,                            │
  │      AVG(e.salary) AS avg_salary                                         │
  │  FROM departments d                                                      │
  │  LEFT JOIN employees e ON d.department_id = e.department_id              │
  │  GROUP BY d.department_name                                              │
  │  HAVING COUNT(e.employee_id) > 5; -- Filtering on aggregated values      │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

  [Language: SQL]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Set Operations (UNION, INTERSECT, EXCEPT)                            │
  │                                                                          │
  │  -- Get emails of all users who are both customers and employees         │
  │  SELECT email FROM customers                                             │
  │  INTERSECT                                                               │
  │  SELECT email FROM employees;                                            │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: SQL]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // CTEs and Window Functions                                            │
  │                                                                          │
  │  WITH DepartmentStats AS (                                               │
  │      SELECT                                                              │
  │          employee_id,                                                    │
  │          first_name,                                                     │
  │          department_id,                                                  │
  │          salary,                                                         │
  │          -- Window function 1: Rank within department                    │
  │          DENSE_RANK() OVER (PARTITION BY department_id ORDER BY salary DESC) as rank_in_dept,│
  │          -- Window function 2: Average salary of department              │
  │          AVG(salary) OVER (PARTITION BY department_id) as dept_avg_salary│
  │      FROM employees                                                      │
  │  )                                                                       │
  │  SELECT                                                                  │
  │      d.department_name,                                                  │
  │      ds.first_name,                                                      │
  │      ds.salary,                                                          │
  │      ds.dept_avg_salary,                                                 │
  │      (ds.salary - ds.dept_avg_salary) AS difference_from_avg             │
  │  FROM DepartmentStats ds                                                 │
  │  JOIN departments d ON ds.department_id = d.department_id                │
  │  WHERE ds.rank_in_dept <= 2                                              │
  │  ORDER BY d.department_name, ds.rank_in_dept;                            │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘
  Scenario: Find the top 2 highest-paid employees in each department, and show how their salary compares to the department average.

  [Language: SQL]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Conditional Logic (CASE WHEN) & Running Totals                       │
  │                                                                          │
  │  SELECT                                                                  │
  │      order_date,                                                         │
  │      amount,                                                             │
  │      -- Running total using window function                              │
  │      SUM(amount) OVER (ORDER BY order_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) as running_total,│
  │      -- Conditional labeling                                             │
  │      CASE                                                                │
  │          WHEN amount > 1000 THEN 'High Value'                            │
  │          WHEN amount > 500 THEN 'Medium Value'                           │
  │          ELSE 'Low Value'                                                │
  │      END AS order_category                                               │
  │  FROM orders;                                                            │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

  [Language: SQL]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // UPSERT (ON CONFLICT DO UPDATE)                                       │
  │                                                                          │
  │  INSERT INTO user_logins (user_id, last_login_date, login_count)         │
  │  VALUES (101, CURRENT_TIMESTAMP, 1)                                      │
  │  ON CONFLICT (user_id)                                                   │
  │  DO UPDATE SET                                                           │
  │      last_login_date = EXCLUDED.last_login_date,                         │
  │      login_count = user_logins.login_count + 1;                          │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘
  Essential for idempotent operations and sync scripts.

────────────────────────────────────────────────────────────────────────────────
  7. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: What is the difference between WHERE and HAVING?

  ANSWER:
    WHERE filters rows before aggregation (GROUP BY). HAVING filters rows after aggregation.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: Explain the difference between RANK(), DENSE_RANK(), and ROW_NUMBER().

  ANSWER:
    If values are tied (e.g., 100, 100, 90):
    ROW_NUMBER() assigns strictly unique sequential integers (1, 2, 3).
    RANK() gives ties the same rank, and skips the next rank (1, 1, 3).
    DENSE_RANK() gives ties the same rank, but doesn't skip (1, 1, 2).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: What is a correlated subquery and why can it be slow?

  ANSWER:
    A subquery that references columns from the outer query. It's often slow because it executes once for every row processed by the outer query (O(N) executions), whereas a non-correlated subquery executes only once.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: How does a LEFT JOIN differ from an INNER JOIN?

  ANSWER:
    INNER JOIN returns only rows where there is a match in both tables. LEFT JOIN returns all rows from the left table, and matching rows from the right table (filling missing right side data with NULLs).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: Explain the CROSS JOIN and when you might use it.

  ANSWER:
    It produces the Cartesian product of two tables (every row in A combined with every row in B). Used rarely, but helpful for generating combinations, like a table of all T-shirt sizes cross-joined with all colors.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: What does UNION do compared to UNION ALL?

  ANSWER:
    Both combine the result sets of two queries. UNION removes duplicate rows, requiring a sort/hash operation (slower). UNION ALL keeps duplicates and is faster.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q7: How do you write a query to find duplicate records?

  ANSWER:
    SELECT email, COUNT(*) FROM users GROUP BY email HAVING COUNT(*) > 1;

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q8: What is a Self Join?

  ANSWER:
    Joining a table to itself. Useful for hierarchical data (e.g., Employee table with a ManagerID that references EmployeeID).

────────────────────────────────────────────────────────────────────────────────
  8. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: The Invisible NULLs

  SELECT count(*) FROM users WHERE status NOT IN ('BANNED', 'DELETED', NULL);

  SOLUTION:
    Problem: This will always return 0 rows. In SQL, comparing anything to NULL (even with NOT IN) yields UNKNOWN. NOT IN (A, NULL) translates to status != A AND status != NULL. Since status != NULL is UNKNOWN, the WHERE clause fails for all rows.
    Answer: Remove NULL from the list and use IS NOT NULL.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 2: The Exploding Join

  SELECT u.name, o.order_id 
  FROM users u 
  LEFT JOIN orders o ON 1=1;

  SOLUTION:
    Problem: Using 1=1 as the join condition effectively turns the LEFT JOIN into a CROSS JOIN. If there are 1000 users and 1000 orders, this returns 1,000,000 rows.
    Answer: Use the proper relational condition: ON u.id = o.user_id.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 3: Aggregation Error

  SELECT department_id, first_name, MAX(salary)
  FROM employees
  GROUP BY department_id;

  SOLUTION:
    Problem: first_name is neither in the GROUP BY clause nor wrapped in an aggregate function. SQL standard rejects this.
    Answer: Use a window function, or join a grouped subquery back to the main table.

────────────────────────────────────────────────────────────────────────────────
  9. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  PAGINATION EFFICIENCY: Using LIMIT and OFFSET becomes extremely slow on large tables (e.g., OFFSET 1000000). Production systems use "Keyset Pagination" (e.g., WHERE id > last_seen_id ORDER BY id LIMIT 10).
  DATA PIPELINE COMPLEXITY: Heavy ETL operations are often just massive, highly optimized SQL queries utilizing CTEs and Window Functions. Knowing these prevents doing O(N^2) data manipulation in application code.

────────────────────────────────────────────────────────────────────────────────
  10. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

  -> File 026: Relational_Database_Theory (Theoretical basis for tables and joins.)
  -> File 029: PostgreSQL_Indexing_QueryOpt (How to make these SQL queries execute fast.)
  -> File 035: Transactions_Concurrency (Handling SQL commands in concurrent environments.)

================================================================================
  END OF FILE 027
================================================================================
