================================================================================
  FILE 067: FULL-STACK AUTHENTICATION
  Section: F - Full-Stack Integration
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  Full-Stack Authentication: Registration, JWT, and Security
  This file covers the implementation of a robust authentication system using a React frontend, Node.js/Express backend, and PostgreSQL database. You'll learn about registration flows (password hashing with bcrypt), login flows (verifying credentials and generating JWTs), token storage strategies (httpOnly cookies vs. localStorage), protected routing in React, refresh token rotation, and secure logout mechanisms. Prerequisites: Basic understanding of React, Express, and SQL.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

JWT (JSON WEB TOKEN)
    A compact, URL-safe means of representing claims to be transferred between two parties. Composed of Header, Payload, and Signature.
  BCRYPT
    A password-hashing function designed to be computationally expensive to thwart brute-force attacks.
  ACCESS TOKEN
    A short-lived JWT used to access protected resources.
  REFRESH TOKEN
    A long-lived token used to obtain new access tokens without requiring the user to log in again.
  HTTPONLY COOKIE
    A cookie attribute that prevents client-side scripts (like JavaScript) from accessing it, mitigating XSS attacks.
  LOCALSTORAGE
    Web storage allowing JS to save key/value pairs in a browser. Vulnerable to XSS.
  REFRESH TOKEN ROTATION
    Issuing a new refresh token every time the old one is used, enhancing security if a token is stolen.
  TOKEN BLACKLISTING
    Storing invalidated tokens (e.g., upon logout) to prevent their reuse before expiration.
  PROTECTED ROUTE
    A frontend component that restricts access to authenticated users only.

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

┌─────────────────────────────────────────────────────────────────────────┐
  │  COMPLETE AUTH FLOW                                                     │
  │                                                                         │
  │        CLIENT (React)                     SERVER (Express)                 DATABASE (Postgres)│
  │             |                                     |                                |│
  │    1. Submit Credentials -----------------------> |                                |│
  │             |                                     | 2. Find User                   |│
  │             |                                     | -----------------------------> |│
  │             |                                     | <----------------------------- |│
  │             |                                     | 3. Compare Password (bcrypt)   |│
  │             |                                     | 4. Generate JWTs (Access, Ref) |│
  │             |                                     | 5. Store Refresh Token in DB   |│
  │             |                                     | -----------------------------> |│
  │    6. Return Tokens <---------------------------- |                                |│
  │       (Access in Memory/Local,                    |                                |│
  │        Refresh in HttpOnly Cookie)                |                                |│
  │             |                                     |                                |│
  │    7. Request Protected Route                     |                                |│
  │       (Send Access Token) ----------------------> |                                |│
  │             |                                     | 8. Verify Access Token         |│
  │             |                                     | 9. Fetch Data                  |│
  │             |                                     | -----------------------------> |│
  │             |                                     | <----------------------------- |│
  │   10. Return Data <------------------------------ |                                |│
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  4. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

[Language: JavaScript]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Registration Flow (Backend)                                          │
  │                                                                          │
  │  const bcrypt = require('bcrypt');                                       │
  │  const jwt = require('jsonwebtoken');                                    │
  │                                                                          │
  │  // POST /register                                                       │
  │  app.post('/register', async (req, res) => {                             │
  │      const { username, password } = req.body;                            │
  │                                                                          │
  │      // 1. Validation                                                    │
  │      if (!username || !password) return res.status(400).send('Missing fields');│
  │                                                                          │
  │      // 2. Hash Password                                                 │
  │      const saltRounds = 10;                                              │
  │      const hashedPassword = await bcrypt.hash(password, saltRounds);     │
  │                                                                          │
  │      // 3. Store in DB                                                   │
  │      try {                                                               │
  │          const newUser = await db.query(                                 │
  │              'INSERT INTO users (username, password_hash) VALUES ($1, $2) RETURNING id, username',│
  │              [username, hashedPassword]                                  │
  │          );                                                              │
  │          res.status(201).json(newUser.rows[0]);                          │
  │      } catch (err) {                                                     │
  │          res.status(500).send('Error creating user');                    │
  │      }                                                                   │
  │  });                                                                     │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

[Language: TypeScript/React]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Frontend Protected Route & Auth Context                              │
  │                                                                          │
  │  // AuthContext.tsx                                                      │
  │  import React, { createContext, useState, useContext, useEffect } from 'react';│
  │                                                                          │
  │  const AuthContext = createContext(null);                                │
  │                                                                          │
  │  export const AuthProvider = ({ children }) => {                         │
  │      const [user, setUser] = useState(null);                             │
  │      const [loading, setLoading] = useState(true);                       │
  │                                                                          │
  │      useEffect(() => {                                                   │
  │          // Check for active session on mount                            │
  │          checkAuthStatus().then(userData => {                            │
  │              setUser(userData);                                          │
  │              setLoading(false);                                          │
  │          });                                                             │
  │      }, []);                                                             │
  │                                                                          │
  │      const login = async (credentials) => {                              │
  │          const userData = await performLogin(credentials);               │
  │          setUser(userData);                                              │
  │      };                                                                  │
  │                                                                          │
  │      const logout = async () => {                                        │
  │          await performLogout();                                          │
  │          setUser(null);                                                  │
  │      };                                                                  │
  │                                                                          │
  │      return (                                                            │
  │          <AuthContext.Provider value={{ user, login, logout, loading }}> │
  │              {children}                                                  │
  │          </AuthContext.Provider>                                         │
  │      );                                                                  │
  │  };                                                                      │
  │                                                                          │
  │  export const useAuth = () => useContext(AuthContext);                   │
  │                                                                          │
  │  // PrivateRoute.tsx                                                     │
  │  import { Navigate, Outlet } from 'react-router-dom';                    │
  │                                                                          │
  │  export const PrivateRoute = () => {                                     │
  │      const { user, loading } = useAuth();                                │
  │                                                                          │
  │      if (loading) return <div>Loading...</div>;                          │
  │      return user ? <Outlet /> : <Navigate to="/login" replace />;        │
  │  };                                                                      │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

  [Language: JavaScript]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Backend Refresh Token Rotation (Express)                             │
  │                                                                          │
  │  // POST /refresh                                                        │
  │  app.post('/refresh', async (req, res) => {                              │
  │      const refreshToken = req.cookies.refreshToken;                      │
  │      if (!refreshToken) return res.sendStatus(401);                      │
  │                                                                          │
  │      // Verify token                                                     │
  │      jwt.verify(refreshToken, process.env.REFRESH_SECRET, async (err, decoded) => {│
  │          if (err) return res.sendStatus(403);                            │
  │                                                                          │
  │          // Check if token matches the one in DB (detect reuse)          │
  │          const user = await db.query('SELECT * FROM users WHERE id = $1', [decoded.id]);│
  │          if (user.rows[0].refresh_token !== refreshToken) {              │
  │              // Token reuse detected! Revoke all tokens for this user    │
  │              await db.query('UPDATE users SET refresh_token = null WHERE id = $1', [decoded.id]);│
  │              return res.sendStatus(403);                                 │
  │          }                                                               │
  │                                                                          │
  │          // Generate new tokens (Rotation)                               │
  │          const newAccessToken = generateAccessToken(user.rows[0]);       │
  │          const newRefreshToken = generateRefreshToken(user.rows[0]);     │
  │                                                                          │
  │          // Save new refresh token in DB                                 │
  │          await db.query('UPDATE users SET refresh_token = $1 WHERE id = $2', [newRefreshToken, decoded.id]);│
  │                                                                          │
  │          // Send new tokens                                              │
  │          res.cookie('refreshToken', newRefreshToken, { httpOnly: true, secure: true, sameSite: 'strict' });│
  │          res.json({ accessToken: newAccessToken });                      │
  │      });                                                                 │
  │  });                                                                     │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

Q1: What is the difference between Access Tokens and Refresh Tokens?

  ANSWER:
    Access tokens are short-lived and used to authorize API requests. Refresh tokens are long-lived and used only to obtain new access tokens. This limits the window of opportunity if an access token is compromised.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: Where should you store a JWT on the client side?

  ANSWER:
    Store access tokens in memory (app state) and refresh tokens in httpOnly secure cookies. Using localStorage exposes tokens to Cross-Site Scripting (XSS) attacks.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: What is Refresh Token Rotation?

  ANSWER:
    Issuing a new refresh token every time a refresh token is used. If a token is stolen, the legitimate user will use the old token, invalidating it, and the system can detect the anomaly and revoke all access.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: How do you securely hash a password?

  ANSWER:
    Use an algorithm like bcrypt, Argon2, or PBKDF2 with a unique salt for each user. Never use MD5 or SHA-256 directly.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: How does httpOnly protect cookies?

  ANSWER:
    It instructs the browser not to expose the cookie to client-side scripts (document.cookie), completely mitigating XSS token theft.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: What is Token Blacklisting and why is it needed for logout?

  ANSWER:
    JWTs are stateless; they are valid until they expire. To force immediate invalidation (logout), you must store the logged-out token's ID (jti) in a database/Redis "blacklist" and check against it on every request.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q7: Explain the purpose of the JWT Signature.

  ANSWER:
    The signature guarantees that the payload and header have not been tampered with. The server verifies it using its secret key.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q8: How do you handle auth state in a React app on page refresh?

  ANSWER:
    Since memory state is lost, the app mounts, calls an /api/me endpoint using the httpOnly cookie or hits a /refresh endpoint to get a new access token and repopulate the context.

────────────────────────────────────────────────────────────────────────────────
  7. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

CHALLENGE 1: Riddle

  I am passed in every request, but the JavaScript running on the page can never see me. What am I?

  SOLUTION:
    An httpOnly cookie.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─


  CHALLENGE 2: Riddle

  I am stateless and self-contained, trusting only my signature. What am I?

  SOLUTION:
    A JWT.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─


  CHALLENGE 3: 

  // Registration route snippet
  const hashedPassword = bcrypt.hashSync(password, 1); 

  SOLUTION:
    The salt rounds are set to 1, making the hash computation incredibly fast. This defeats the purpose of bcrypt, allowing attackers to brute-force hashes rapidly. Fix: Use at least 10-12 rounds.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─


  CHALLENGE 4: 

  const token = jwt.sign({ id: user.id }, SECRET_KEY); // Default options

  SOLUTION:
    Missing an expiresIn option. This token will never expire. If stolen, it provides indefinite access.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─


  CHALLENGE 5: 

  // Login success handler in React
  localStorage.setItem('accessToken', res.data.token);

  SOLUTION:
    Storing access tokens in localStorage makes them accessible via document.cookie. Any XSS vulnerability on the site will result in token theft. Fix: Use httpOnly cookies or in-memory storage.

────────────────────────────────────────────────────────────────────────────────
  8. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  Authentication is the highest-stakes part of any application. A flaw in JWT handling, token storage, or password hashing can lead to complete data breaches. Implementing robust auth flows (refresh rotation, secure cookies) protects against XSS and CSRF, ensuring user trust and compliance with security standards.

────────────────────────────────────────────────────────────────────────────────
  9. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

-> File 066: 066 FullStack Architecture (Understanding where auth sits in the architecture.)
  -> File 071: 071 FullStack Security (Deep dive into XSS and CSRF vulnerabilities.)
  -> File 068: 068 FullStack Project CRUD (Securing CRUD operations with auth tokens.)

================================================================================
  END OF FILE 067
================================================================================
