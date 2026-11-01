================================================================================
  FILE 072: WEB PERFORMANCE & MONITORING
  Section: F - Full-Stack Integration
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  Monitoring and Performance: APM, Logging, and Audits
  This file covers how to keep a full-stack application running smoothly in production. You will learn about Application Performance Monitoring (APM), structured logging (ELK stack), error tracking (Sentry), performance budgets, Lighthouse auditing, and Real User Monitoring (RUM). Prerequisite: Experience deploying applications to production.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

APM (APPLICATION PERFORMANCE MONITORING)
    Tools (e.g., Datadog, New Relic) that track app performance, database queries, and server health.
  STRUCTURED LOGGING
    Writing logs in a machine-readable format (usually JSON) rather than plain text, making them easily searchable.
  LOG LEVELS
    Standardized categories of logs: ERROR, WARN, INFO, DEBUG.
  ELK STACK
    Elasticsearch (search engine), Logstash (log ingestion pipeline), Kibana (visualization dashboard).
  ERROR TRACKING
    Tools (e.g., Sentry) that automatically capture exceptions, stack traces, and environment context when an app crashes.
  SOURCE MAPS
    Files that map minified/transpiled production code back to the original source code, crucial for debugging production errors.
  LIGHTHOUSE
    An open-source, automated tool for improving the quality of web pages (Performance, Accessibility, SEO).
  RUM (REAL USER MONITORING)
    Collecting performance metrics from actual users using the application in their browsers.
  SYNTHETIC MONITORING
    Simulating user traffic (bots) to test if critical paths (e.g., checkout flow) are working globally.

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

┌─────────────────────────────────────────────────────────────────────────┐
  │  MONITORING STACK ARCHITECTURE                                          │
  │                                                                         │
  │  +-------------------+        +-------------------+       +-------------------+│
  │  |                   |        |                   |       |                   |│
  │  |  Client Browser   +-------->  Node.js Backend  +------->    Database       |│
  │  |  (React App)      |        |  (Express API)    |       |  (PostgreSQL)     |│
  │  |                   |        |                   |       |                   |│
  │  +--------+----------+        +---------+---------+       +---------+---------+│
  │           |                             |                           |   │
  │           | (1. Errors/RUM)             | (2. Logs/Metrics)         | (3. Query Stats)│
  │           v                             v                           v   │
  │  +-------------------+        +-----------------------------------------------+│
  │  |      Sentry       |        |                  Datadog / ELK                |│
  │  | (Error Tracking)  |        |            (APM & Centralized Logs)           |│
  │  +-------------------+        +-----------------------+-----------------------+│
  │                                                       |                 │
  │                                                       | (4. Alerts)     │
  │                                                       v                 │
  │                                            +-------------------+        │
  │                                            |   PagerDuty/Slack |        │
  │                                            +-------------------+        │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  4. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

[Language: JavaScript]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Structured Logging with Pino (Node.js)                               │
  │                                                                          │
  │  const pino = require('pino');                                           │
  │  // Pino is much faster than Winston because it logs JSON by default     │
  │  const logger = pino({                                                   │
  │    level: process.env.LOG_LEVEL || 'info',                               │
  │    formatters: {                                                         │
  │      level: (label) => {                                                 │
  │        return { level: label.toUpperCase() };                            │
  │      },                                                                  │
  │    },                                                                    │
  │    timestamp: pino.stdTimeFunctions.isoTime,                             │
  │  });                                                                     │
  │                                                                          │
  │  logger.info({ user_id: 123, action: 'login' }, 'User logged in successfully');│
  │  logger.error({ err: new Error('DB Connection Failed') }, 'Database error occurred');│
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

[Language: JavaScript]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Sentry Integration in React (Frontend)                               │
  │                                                                          │
  │  import * as Sentry from "@sentry/react";                                │
  │  import { BrowserTracing } from "@sentry/tracing";                       │
  │                                                                          │
  │  // Initialize Sentry early in the application lifecycle                 │
  │  Sentry.init({                                                           │
  │    dsn: "https://examplePublicKey@o0.ingest.sentry.io/0",                │
  │    integrations: [new BrowserTracing()],                                 │
  │                                                                          │
  │    // Set tracesSampleRate to 1.0 to capture 100% of transactions for performance monitoring.│
  │    // We recommend adjusting this value in production                    │
  │    tracesSampleRate: 0.2,                                                │
  │    release: "my-project-name@" + process.env.npm_package_version,        │
  │  });                                                                     │
  │                                                                          │
  │  // Using ErrorBoundary to catch React rendering errors                  │
  │  function App() {                                                        │
  │    return (                                                              │
  │      <Sentry.ErrorBoundary fallback={<p>An error has occurred</p>}>      │
  │        <MyMainComponent />                                               │
  │      </Sentry.ErrorBoundary>                                             │
  │    );                                                                    │
  │  }                                                                       │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

Q1: What is Structured Logging and why is it superior to plain text logging?

  ANSWER:
    Structured logging outputs logs in JSON format instead of flat strings. This allows log aggregation tools (like Elasticsearch or Datadog) to parse, index, and query the logs easily (e.g., search: user_id=123 AND level=ERROR).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: What are Source Maps and why are they critical for production error tracking?

  ANSWER:
    Source maps map minified, obfuscated production code back to the original developer source code. Without them, a Sentry error stack trace will point to a.js line 1 col 50000, which is useless for debugging.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: Difference between Real User Monitoring (RUM) and Synthetic Monitoring?

  ANSWER:
    RUM tracks performance metrics from actual users in their actual browsers (measuring real-world latency). Synthetic monitoring uses bots from various geographic locations to constantly ping your site and ensure uptime and critical flows are working.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: What are the key categories audited by Google Lighthouse?

  ANSWER:
    Performance (load speed), Accessibility (screen readers, contrast), Best Practices (HTTPS, secure cross-origin links), and SEO.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: How do you set a Performance Budget?

  ANSWER:
    A performance budget sets limits on metrics (e.g., "JS bundle size must be < 200KB" or "Time to Interactive < 3s"). You enforce this by integrating tools like Lighthouse CI into your GitHub Actions; the CI fails if the PR exceeds the budget.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: Explain the ELK stack.

  ANSWER:
    Elasticsearch stores and indexes the logs. Logstash collects, parses, and transforms logs from servers. Kibana is the UI dashboard to visualize and search the data in Elasticsearch.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q7: What is distributed tracing?

  ANSWER:
    A method to track a single request as it flows through multiple microservices. A unique "Trace ID" is generated at the entry point and passed along via HTTP headers, allowing APM tools to visualize the entire journey and pinpoint bottlenecks.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q8: Why shouldn't you log everything at the INFO level?

  ANSWER:
    It creates noise, increases storage costs, and makes finding actual problems harder. Use DEBUG for verbose development logs, INFO for significant business events, WARN for recoverable issues, and ERROR for system failures requiring attention.

────────────────────────────────────────────────────────────────────────────────
  7. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

CHALLENGE 1: Riddle

  I translate the gibberish of minified javascript back into the beautiful code you wrote, so when things break, you know exactly where to look. What am I?

  SOLUTION:
    A Source Map.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─


  CHALLENGE 2: Riddle

  I am the librarian of logs. I index billions of JSON lines so you can search them in milliseconds. Who am I?

  SOLUTION:
    Elasticsearch.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─


  CHALLENGE 3: 

  // Node.js Express error handler
  app.use((err, req, res, next) => {
      console.log("Error occurred: " + err); 
      res.status(500).send("Something broke");
  });

  SOLUTION:
    Concatenating an Error object with a string calls its .toString() method, which outputs Error: message but completely loses the stack trace! Fix: console.error("Error occurred", err) or use a structured logger.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─


  CHALLENGE 4: 

  // Webpack config
  module.exports = {
    mode: 'production',
    devtool: 'source-map',
    // ...
  }

  SOLUTION:
    Generating source maps and hosting them publicly allows anyone to download your entire original, unminified source code. Fix: Upload source maps to your error tracker (Sentry) during CI/CD, but do not deploy the .map files to your public web server.

────────────────────────────────────────────────────────────────────────────────
  8. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  Without monitoring, you are flying blind. Users will encounter broken pages and leave before you even realize there's a bug. Centralized logging and APM alert you to performance degradation and errors instantly, drastically reducing Mean Time To Resolution (MTTR).

────────────────────────────────────────────────────────────────────────────────
  9. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

-> File 069: 069 FullStack Deployment (Deploying the Node process that generates these logs.)

================================================================================
  END OF FILE 072
================================================================================
