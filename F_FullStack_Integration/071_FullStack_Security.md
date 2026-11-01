================================================================================
  FILE 071: FULL-STACK SECURITY
  Section: F - Full-Stack Integration
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  Web Application Security: Vulnerabilities and Mitigations
  This file covers the essential security concepts every full-stack developer must know, heavily focused on the OWASP Top 10. You will learn about Cross-Site Scripting (XSS), Cross-Site Request Forgery (CSRF), SQL Injection, rate limiting algorithms, Content Security Policy (CSP), and supply chain security (dependency scanning). Prerequisites: Knowledge of HTTP, databases, and frontend rendering.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

OWASP (OPEN WEB APPLICATION SECURITY PROJECT)
    A nonprofit foundation that works to improve the security of software.
  XSS (CROSS-SITE SCRIPTING)
    Injecting malicious scripts into benign and trusted websites.
  *STORED*
    Script is saved to DB and served to users.
  *REFLECTED*
    Script is embedded in URL and reflected by the server.
  *DOM-BASED*
    Script payload modifies the DOM entirely in the browser.
  CSRF (CROSS-SITE REQUEST FORGERY)
    Forcing an end user to execute unwanted actions on a web application in which they're currently authenticated.
  SQL INJECTION (SQLI)
    Interfering with the queries an application makes to its database.
  CSP (CONTENT SECURITY POLICY)
    An HTTP header that restricts the resources (e.g., JS, CSS, Images) that a browser is allowed to load.
  HSTS (HTTP STRICT TRANSPORT SECURITY)
    A web security policy mechanism that helps to protect websites against man-in-the-middle attacks by forcing HTTPS.
  RATE LIMITING
    Controlling the rate of traffic sent or received by a network interface.
  TOKEN BUCKET / SLIDING WINDOW
    Algorithms used to implement rate limiting.

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

┌─────────────────────────────────────────────────────────────────────────┐
  │  CROSS-SITE SCRIPTING (STORED XSS)                                      │
  │                                                                         │
  │  1. Attacker writes comment: <script>stealToken()</script>              │
  │     |                                                                   │
  │     v                                                                   │
  │  2. Server saves comment to Database                                    │
  │     |                                                                   │
  │     v                                                                   │
  │  3. Victim requests page                                                │
  │     |                                                                   │
  │     v                                                                   │
  │  4. Server serves comment unescaped                                     │
  │     |                                                                   │
  │     v                                                                   │
  │  5. Victim's browser executes script, sending token to Attacker         │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  CSRF ATTACK                                                            │
  │                                                                         │
  │  Victim is logged into Bank.com (Session Cookie set)                    │
  │                                                                         │
  │  1. Attacker tricks victim into visiting Evil.com                       │
  │  2. Evil.com contains an invisible form:                                │
  │     <form action="https://bank.com/transfer" method="POST">             │
  │       <input type="hidden" name="to" value="Attacker">                  │
  │     </form>                                                             │
  │     <script>document.forms[0].submit()</script>                         │
  │  3. Browser automatically attaches Bank.com session cookie!             │
  │  4. Bank processes transfer, thinking Victim requested it.              │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  4. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

[Language: JavaScript]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // SQL Injection Vulnerability vs Fix (Node.js/Postgres)                │
  │                                                                          │
  │  // VULNERABLE CODE (Never do this)                                      │
  │  app.post('/login', async (req, res) => {                                │
  │      const { username, password } = req.body;                            │
  │      // Attack: username = "admin' OR '1'='1", password = "any"          │
  │      // Query becomes: SELECT * FROM users WHERE username='admin' OR '1'='1' AND password='any'│
  │      const query = `SELECT * FROM users WHERE username='${username}' AND password='${password}'`;│
  │      const result = await db.query(query);                               │
  │  });                                                                     │
  │                                                                          │
  │  // SECURE CODE (Parameterized Queries)                                  │
  │  app.post('/login', async (req, res) => {                                │
  │      const { username, password } = req.body;                            │
  │      // The database driver treats $1 and $2 purely as data, not executable SQL│
  │      const query = 'SELECT * FROM users WHERE username=$1 AND password=$2';│
  │      const result = await db.query(query, [username, password]);         │
  │  });                                                                     │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

[Language: JavaScript]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Express Security Headers & Rate Limiting                             │
  │                                                                          │
  │  const express = require('express');                                     │
  │  const helmet = require('helmet'); // Sets various HTTP headers          │
  │  const rateLimit = require('express-rate-limit');                        │
  │                                                                          │
  │  const app = express();                                                  │
  │                                                                          │
  │  // 1. Helmet sets CSP, HSTS, X-Frame-Options, X-XSS-Protection, etc.    │
  │  app.use(helmet());                                                      │
  │                                                                          │
  │  // Custom CSP configuration if needed                                   │
  │  app.use(helmet.contentSecurityPolicy({                                  │
  │      directives: {                                                       │
  │          defaultSrc: ["'self'"],                                         │
  │          scriptSrc: ["'self'", "https://trusted-cdn.com"],               │
  │          objectSrc: ["'none'"],                                          │
  │          upgradeInsecureRequests: [],                                    │
  │      }                                                                   │
  │  }));                                                                    │
  │                                                                          │
  │  // 2. Rate Limiting (Token Bucket / Window based)                       │
  │  const apiLimiter = rateLimit({                                          │
  │      windowMs: 15 * 60 * 1000, // 15 minutes                             │
  │      max: 100, // Limit each IP to 100 requests per `window`             │
  │      message: 'Too many requests from this IP, please try again after 15 minutes',│
  │      standardHeaders: true, // Return rate limit info in the `RateLimit-*` headers│
  │      legacyHeaders: false, // Disable the `X-RateLimit-*` headers        │
  │  });                                                                     │
  │                                                                          │
  │  app.use('/api/', apiLimiter);                                           │
  │                                                                          │
  │  app.listen(3000);                                                       │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

Q1: How do you prevent XSS attacks?

  ANSWER:
    Primarily by output encoding (escaping HTML entities before rendering). Frameworks like React do this automatically ({variable}). Additionally, implement a strict Content Security Policy (CSP) and sanitize rich text input (e.g., using DOMPurify).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: What is CSRF and how do you prevent it?

  ANSWER:
    It forces an authenticated user to execute an action on a site where they are logged in. Prevent it using Anti-CSRF Tokens (synchronizer token pattern) OR by setting the SameSite=Strict or SameSite=Lax attribute on session cookies.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: What is SQL Injection and how is it prevented?

  ANSWER:
    Injecting malicious SQL into input fields. Prevented entirely by using Parameterized Queries (Prepared Statements) or an ORM. Never concatenate strings to build SQL queries.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: Explain the SameSite cookie attribute.

  ANSWER:
    It controls when cookies are sent with cross-site requests. Strict means cookies are only sent for first-party requests. Lax allows cookies on top-level navigations (like clicking a link). None allows all cross-site requests (requires Secure attribute).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: What is a Content Security Policy (CSP)?

  ANSWER:
    An HTTP header that acts as a whitelist for where resources (scripts, images, styles) can be loaded from and executed. It is a major defense-in-depth mitigation against XSS.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: How does a Token Bucket rate limiting algorithm work?

  ANSWER:
    A bucket holds tokens. Tokens are added at a fixed rate. Each request consumes a token. If the bucket is empty, the request is dropped. It allows for short bursts of traffic while maintaining an average rate.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q7: What is Dependency Vulnerability Scanning?

  ANSWER:
    Tools like npm audit, Snyk, or Dependabot scan your package.json against databases of known vulnerabilities (CVEs) and warn you or automatically open PRs to update insecure packages.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q8: What does the helmet package do in Express?

  ANSWER:
    It secures Express apps by setting various HTTP headers. It removes the X-Powered-By header, sets HSTS, sets X-Frame-Options to prevent Clickjacking, and sets baseline CSP.

────────────────────────────────────────────────────────────────────────────────
  7. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

CHALLENGE 1: Riddle

  I let you type your name, but if your name is <script>alert('pwned')</script>, I'll happily make your browser scream it. What am I?

  SOLUTION:
    A Reflected XSS Vulnerability.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─


  CHALLENGE 2: Riddle

  I blindly append your variables to my database query string, trusting you implicitly. What vulnerability do I invite?

  SOLUTION:
    SQL Injection.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─


  CHALLENGE 3: 

  // React component rendering a blog post body
  function BlogPost({ post }) {
      // post.body comes from user input
      return <div dangerouslySetInnerHTML={{ __html: post.body }} />;
  }

  SOLUTION:
    Using dangerouslySetInnerHTML bypasses React's automatic escaping. If post.body contains <script>, it will execute. Fix: Run post.body through a sanitizer like DOMPurify before rendering it.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─


  CHALLENGE 4: 

  // Express route for changing password
  app.post('/change-password', checkAuthCookie, (req, res) => {
      // Updates password based on req.body
  });

  SOLUTION:
    If the session relies on a cookie without SameSite restrictions, an attacker's website can submit a form to this endpoint, and the browser will attach the auth cookie automatically. Fix: Require a CSRF token or use SameSite cookies.

────────────────────────────────────────────────────────────────────────────────
  8. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  A single XSS vulnerability can lead to mass account takeovers. A SQL injection can leak your entire database. Securing web applications is not optional; failure to do so results in data breaches, loss of customer trust, and severe legal consequences.

────────────────────────────────────────────────────────────────────────────────
  9. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

-> File 067: 067 FullStack Project Auth (Secure cookie usage.)
  -> File 069: 069 FullStack Deployment (Configuring CORS correctly.)

================================================================================
  END OF FILE 071
================================================================================
