================================================================================
  FILE 039: NODEJS AUTH SECURITY
  Section: D - Backend Development
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  Node.js Authentication, Authorization, and Security
  Securing a Node.js application involves verifying user identities (Authentication), ensuring they have correct permissions (Authorization), and protecting the server against common web vulnerabilities. This guide covers implementing JWTs, password hashing, OAuth 2.0 flows, and applying standard security headers and rate limits to Express APIs.
  Prerequisites: Node.js, Express.js middleware concepts, PostgreSQL basics.
  What you'll learn: JWT structure and security, Refresh token rotation, Bcrypt password hashing, OAuth 2.0 flows, input validation, and web security best practices (Helmet, rate limiting).
  
  ---

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  Authentication (AuthN)
    Proving *who* the user is (e.g., logging in with username/password).

  Authorization (AuthZ)
    Determining *what* the authenticated user is allowed to do (e.g., admin vs. normal user).

  JWT (JSON Web Token)
    An open standard (RFC 7519) that defines a compact and self-contained way for securely transmitting information between parties as a JSON object.

  Access Token
    A short-lived JWT (e.g., 15 mins) sent with every API request to authorize access to resources.

  Refresh Token
    A long-lived token (e.g., 7 days) stored securely and used only to request new access tokens.

  Bcrypt
    A password-hashing function designed to be computationally expensive (slow) to defend against brute-force attacks.

  Salt
    Random data added to a password before hashing to defend against precomputed rainbow table attacks.

  OAuth 2.0
    An authorization framework enabling third-party applications to obtain limited access to an HTTP service (e.g., "Login with Google").

  Rate Limiting
    Restricting the number of requests a client can make in a given timeframe to prevent DoS attacks and brute-forcing.

  Helmet
    A Node.js module that secures Express apps by setting various HTTP headers.

  Input Validation
    Ensuring user-provided data matches expected formats (using tools like Joi or Zod) before processing it.

  --

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  JWT Access + Refresh Token Flow

  ┌─────────────────────────────────────────────────────────────────────────┐
  │    Client (Browser/App)                           Server (Node/Express) │
  │            |                                               |            │
  │            | 1. POST /login (username, password)           |            │
  │            |---------------------------------------------->|            │
  │            |                                               | 2. Verify credentials│
  │            | 3. Returns Access Token (15m)                 | Generate Tokens│
  │            |    + Refresh Token (HttpOnly Cookie, 7d)      |            │
  │            |<----------------------------------------------|            │
  │            |                                               |            │
  │            | 4. GET /api/data + Access Token               |            │
  │            |---------------------------------------------->| 5. Validate Access Token│
  │            | 6. Returns Protected Data                     |            │
  │            |<----------------------------------------------|            │
  │            |                                               |            │
  │          (Time passes... Access Token expires)             |            │
  │            |                                               |            │
  │            | 7. GET /api/data + Expired Access Token       |            │
  │            |---------------------------------------------->| 8. Token Expired Error│
  │            | 9. 401 Unauthorized                           |            │
  │            |<----------------------------------------------|            │
  │            |                                               |            │
  │            | 10. POST /refresh + Refresh Token (Cookie)    |            │
  │            |---------------------------------------------->| 11. Validate Refresh Token│
  │            | 12. Returns NEW Access Token                  |     Generate new Access Token│
  │            |<----------------------------------------------|            │
  │            |                                               |            │
  │            | 13. GET /api/data + NEW Access Token          |            │
  │            |---------------------------------------------->|            │
  │            | 14. Returns Protected Data                    |            │
  │            |<----------------------------------------------|            │
  └─────────────────────────────────────────────────────────────────────────┘

### JWT Structure (Base64Url Encoded)

  ┌─────────────────────────────────────────────────────────────────────────┐
  │    Header         Payload              Signature                        │
  │  (Algorithm)   (Data/Claims)   (Verify sender & integrity)              │
  │    xxxxx    .     yyyyy      .          zzzzz                           │
  └─────────────────────────────────────────────────────────────────────────┘

---

────────────────────────────────────────────────────────────────────────────────
  5. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  Password Hashing with Bcrypt


  Language: javascript


  ┌──────────────────────────────────────────────────────────────────────────┐
  │  const bcrypt = require('bcrypt');                                       │
  │                                                                          │
  │  async function hashPassword(plainTextPassword) {                        │
  │      // Salt rounds determine algorithm cost (10-12 is standard)         │
  │      const saltRounds = 12;                                              │
  │      const hash = await bcrypt.hash(plainTextPassword, saltRounds);      │
  │      return hash;                                                        │
  │  }                                                                       │
  │                                                                          │
  │  async function verifyPassword(plainTextPassword, storedHash) {          │
  │      // bcrypt extracts the salt from the storedHash automatically       │
  │      const isMatch = await bcrypt.compare(plainTextPassword, storedHash);│
  │      return isMatch;                                                     │
  │  }                                                                       │
  └──────────────────────────────────────────────────────────────────────────┘

  ---

────────────────────────────────────────────────────────────────────────────────
  6. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

  Auth System: Register, Login, Refresh, Middleware


  Language: javascript


  ┌──────────────────────────────────────────────────────────────────────────┐
  │  require('dotenv').config();                                             │
  │  const express = require('express');                                     │
  │  const jwt = require('jsonwebtoken');                                    │
  │  const bcrypt = require('bcrypt');                                       │
  │  const cookieParser = require('cookie-parser');                          │
  │  const helmet = require('helmet');                                       │
  │  const rateLimit = require('express-rate-limit');                        │
  │  const app = express();                                                  │
  │                                                                          │
  │  app.use(express.json());                                                │
  │  app.use(cookieParser());                                                │
  │  app.use(helmet()); // Sets security headers                             │
  │                                                                          │
  │  // Rate limiting for auth routes                                        │
  │  const authLimiter = rateLimit({                                         │
  │      windowMs: 15 * 60 * 1000, // 15 minutes                             │
  │      max: 10, // Limit each IP to 10 requests per window                 │
  │      message: "Too many login attempts, please try again later"          │
  │  });                                                                     │
  │                                                                          │
  │  // Mock Database                                                        │
  │  const usersDB = [];                                                     │
  │  const refreshTokensDB = new Set();                                      │
  │                                                                          │
  │  // --- 1. REGISTER ---                                                  │
  │  app.post('/api/register', async (req, res) => {                         │
  │      const { username, password } = req.body;                            │
  │      if (!username || !password) return res.status(400).json({ error: "Missing fields" });│
  │                                                                          │
  │      const hashedPassword = await bcrypt.hash(password, 12);             │
  │      const newUser = { id: Date.now(), username, password: hashedPassword };│
  │      usersDB.push(newUser);                                              │
  │                                                                          │
  │      res.status(201).json({ message: "User registered" });               │
  │  });                                                                     │
  │                                                                          │
  │  // --- 2. LOGIN ---                                                     │
  │  app.post('/api/login', authLimiter, async (req, res) => {               │
  │      const { username, password } = req.body;                            │
  │      const user = usersDB.find(u => u.username === username);            │
  │                                                                          │
  │      if (!user || !(await bcrypt.compare(password, user.password))) {    │
  │          return res.status(401).json({ error: "Invalid credentials" });  │
  │      }                                                                   │
  │                                                                          │
  │      // Generate Tokens                                                  │
  │      const accessToken = jwt.sign({ id: user.id, username: user.username }, process.env.JWT_SECRET, { expiresIn: '15m' });│
  │      const refreshToken = jwt.sign({ id: user.id }, process.env.REFRESH_SECRET, { expiresIn: '7d' });│
  │                                                                          │
  │      refreshTokensDB.add(refreshToken); // Store in DB (or Redis in production)│
  │                                                                          │
  │      // Send Refresh Token as HttpOnly cookie                            │
  │      res.cookie('jwt_refresh', refreshToken, {                           │
  │          httpOnly: true, // Prevents XSS accessing the cookie            │
  │          secure: process.env.NODE_ENV === 'production', // HTTPS only    │
  │          sameSite: 'Strict', // Prevents CSRF                            │
  │          maxAge: 7 * 24 * 60 * 60 * 1000 // 7 days                       │
  │      });                                                                 │
  │                                                                          │
  │      // Send Access Token in JSON body                                   │
  │      res.json({ accessToken });                                          │
  │  });                                                                     │
  │                                                                          │
  │  // --- 3. REFRESH TOKEN ---                                             │
  │  app.post('/api/refresh', (req, res) => {                                │
  │      const refreshToken = req.cookies?.jwt_refresh;                      │
  │      if (!refreshToken) return res.status(401).json({ error: "No refresh token" });│
  │      if (!refreshTokensDB.has(refreshToken)) return res.status(403).json({ error: "Invalid refresh token" });│
  │                                                                          │
  │      jwt.verify(refreshToken, process.env.REFRESH_SECRET, (err, decoded) => {│
  │          if (err) return res.status(403).json({ error: "Token expired/invalid" });│
  │                                                                          │
  │          // Generate new Access Token                                    │
  │          const newAccessToken = jwt.sign({ id: decoded.id }, process.env.JWT_SECRET, { expiresIn: '15m' });│
  │          res.json({ accessToken: newAccessToken });                      │
  │      });                                                                 │
  │  });                                                                     │
  │                                                                          │
  │  // --- 4. AUTH MIDDLEWARE ---                                           │
  │  const verifyJWT = (req, res, next) => {                                 │
  │      const authHeader = req.headers['authorization'];                    │
  │      if (!authHeader?.startsWith('Bearer ')) return res.sendStatus(401); │
  │                                                                          │
  │      const token = authHeader.split(' ')[1];                             │
  │                                                                          │
  │      jwt.verify(token, process.env.JWT_SECRET, (err, decoded) => {       │
  │          if (err) return res.sendStatus(403); // Forbidden (token invalid/expired)│
  │          req.user = decoded; // Attach payload to request                │
  │          next();                                                         │
  │      });                                                                 │
  │  };                                                                      │
  │                                                                          │
  │  // --- 5. PROTECTED ROUTE ---                                           │
  │  app.get('/api/protected', verifyJWT, (req, res) => {                    │
  │      res.json({ data: `Secret data for user ${req.user.username}` });    │
  │  });                                                                     │
  │                                                                          │
  │  // --- 6. LOGOUT ---                                                    │
  │  app.post('/api/logout', (req, res) => {                                 │
  │      const refreshToken = req.cookies?.jwt_refresh;                      │
  │      refreshTokensDB.delete(refreshToken); // Invalidate token on server │
  │      res.clearCookie('jwt_refresh'); // Clear cookie on client           │
  │      res.sendStatus(204);                                                │
  │  });                                                                     │
  │                                                                          │
  │  app.listen(3000, () => console.log('Auth Server running'));             │
  └──────────────────────────────────────────────────────────────────────────┘

  ---

────────────────────────────────────────────────────────────────────────────────
  7. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: What is the difference between Authentication and Authorization?

  ANSWER:
    Authentication verifies identity (Are you who you say you are? e.g., logging in). Authorization verifies permissions (Are you allowed to do this? e.g., admin deleting a user).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: Why do we use Access Tokens AND Refresh Tokens instead of just one long-lived token?

  ANSWER:
    Security. Access tokens are sent with every request; if stolen, they grant access. By keeping their lifespan very short (15m), the damage window is minimized. Refresh tokens are stored securely (HttpOnly cookies), sent rarely, and can be revoked by the server if a device is lost.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: Where should you store JWT Access Tokens on the frontend?

  ANSWER:
    In application memory (state). Never store them in `localStorage` as they are vulnerable to XSS (Cross-Site Scripting) attacks where malicious scripts can read local storage.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: What is an HttpOnly cookie?

  ANSWER:
    A cookie with the `HttpOnly` flag cannot be accessed via client-side JavaScript (`document.cookie`). This entirely mitigates XSS attacks targeting the cookie.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: Why do we salt passwords before hashing?

  ANSWER:
    Without salts, identical passwords result in identical hashes. Attackers use precomputed "Rainbow Tables" of hashes for common passwords. A unique salt added to each password before hashing ensures identical passwords have different hashes, invalidating rainbow tables.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: What is JWT Signature and why is it important?

  ANSWER:
    The signature is created by hashing the header and payload using a secret key known only to the server. When the server receives a JWT, it recalculates the signature. If it matches, the token was not tampered with. If an attacker alters the payload (e.g., changing `role: user` to `role: admin`), the signature will become invalid.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q7: How do you invalidate (logout) a stateless JWT?

  ANSWER:
    True stateless JWTs cannot be invalidated before they expire. To handle logout, you either: 1) Keep expiration short so it dies quickly, 2) Invalidate the Refresh Token on the server so no new access tokens can be minted, or 3) Maintain a "Token Blacklist" in a fast cache like Redis, making it stateful.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q8: What is the OAuth 2.0 Authorization Code Flow?

  ANSWER:
    Used for server-side apps. The user is redirected to the Auth Provider (Google). User logs in and grants consent. Google redirects back to your server with an Authorization Code. Your server securely exchanges this code + client secret for an Access Token directly with Google (server-to-server).

---

────────────────────────────────────────────────────────────────────────────────
  8. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: The Trusting Server

  app.post('/api/data', (req, res) => {
      const token = req.headers.authorization;
      const decoded = jwt.decode(token);
      
      if (decoded.role === 'admin') {
          deleteDatabase();
      }
  });

  SOLUTION:
    What's wrong? `jwt.decode()` merely decodes the Base64 payload; it does **not** verify the signature. An attacker can easily craft a fake token with `role: admin`.
    Fix: Always use `jwt.verify(token, secret)` to ensure the token was signed by your server and hasn't been altered.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─
  CHALLENGE 2: The Fast Hash

  const crypto = require('crypto');
  
  function hashPassword(password) {
      return crypto.createHash('sha256').update(password).digest('hex');
  }

  SOLUTION:
    What's wrong? SHA-256 is designed to be extremely fast. A modern GPU can compute billions of SHA-256 hashes per second, making brute-forcing trivial. It also lacks a salt here.
    Fix: Use an algorithm designed for password hashing (key derivation functions) that are intentionally slow, like `bcrypt`, `Argon2`, or `scrypt`.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─
  CHALLENGE 3: The Predictable Secret

  const JWT_SECRET = 'my_secret_key_123';
  const token = jwt.sign({ id: user.id }, JWT_SECRET);

  SOLUTION:
    What's wrong? The secret key is hardcoded and weak. If a hacker guesses or brute-forces the secret key, they can mint valid JWTs for any user (including admins) and completely compromise the system.
    Fix: Use a long, cryptographically random string (e.g., generated via `openssl rand -hex 64`) and load it via environment variables (`process.env.JWT_SECRET`).

---


────────────────────────────────────────────────────────────────────────────────
  9. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  - Data Breaches: Improper password hashing (or storing plain text) is how companies end up in the news when their DB is dumped.
  - XSS vs CSRF: Storing tokens in LocalStorage makes them vulnerable to XSS. Storing them in Cookies makes them vulnerable to CSRF. You must use HttpOnly + SameSite cookies to defend against both.
  - Rate Limiting: Without rate limiters on `/login`, attackers can use botnets to execute credential stuffing attacks (trying millions of leaked passwords against your users).
  ---

────────────────────────────────────────────────────────────────────────────────
  10. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

  -> File 37: ExpressJS (Learn how to inject authentication middleware into the Express request lifecycle.)
  -> File 38: NodeJS PostgreSQL (Learn how to securely query the database for users during the login flow.)
  -> File 40: NodeJS Advanced (Learn how to use Redis for token blacklisting and session management in cluster environments.)

================================================================================
  END OF FILE 039
================================================================================
