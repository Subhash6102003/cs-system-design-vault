================================================================================
  FILE 069: FULL-STACK DEPLOYMENT
  Section: F - Full-Stack Integration
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  Deploying Full-Stack Applications: Proxies, Environments, and Processes
  This file explains how to take a full-stack application from local development to a production environment. You will learn how to manage environment variables, configure CORS safely, optimize builds, set up Nginx as a reverse proxy with SSL/TLS, manage Node.js processes with PM2, and understand DNS domain configuration. Prerequisites: Linux command line basics, basic networking concepts.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

ENVIRONMENT VARIABLES (.ENV)
    Externalizing configuration (secrets, DB URIs) so the code acts differently in dev vs. production without code changes.
  CORS (CROSS-ORIGIN RESOURCE SHARING)
    A security feature implemented by browsers that prevents a script on one domain from making a request to another domain unless explicitly allowed by the server.
  REVERSE PROXY
    A server that sits in front of web servers and forwards client requests to those web servers. (e.g., Nginx, HAProxy).
  SSL/TLS TERMINATION
    The process where a reverse proxy decrypts incoming HTTPS traffic and passes it unencrypted to the internal backend server.
  PROCESS MANAGER (PM2)
    A tool to keep Node.js applications alive forever, auto-restarting them on crash, and allowing clustering.
  DNS (DOMAIN NAME SYSTEM)
    Translates human-readable domain names to IP addresses.
  A RECORD
    Points a domain to an IPv4 address.
  CNAME RECORD
    Points a domain to another domain.
  VPS (VIRTUAL PRIVATE SERVER)
    A virtual machine sold as a service (e.g., DigitalOcean Droplet, AWS EC2).
  PAAS (PLATFORM AS A SERVICE)
    Cloud computing service that provides a platform allowing customers to develop, run, and manage applications without the complexity of building and maintaining infrastructure (e.g., Heroku, Render).

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

┌─────────────────────────────────────────────────────────────────────────┐
  │  NGINX REVERSE PROXY ARCHITECTURE                                       │
  │                                                                         │
  │             INTERNET                                                    │
  │                | HTTPS (Port 443)                                       │
  │                v                                                        │
  │  +-----------------------------+                                        │
  │  |        NGINX SERVER         |  <-- SSL/TLS Termination happens here  │
  │  |       (Reverse Proxy)       |                                        │
  │  +------+---------------+------+                                        │
  │         | HTTP          | HTTP                                          │
  │         | (Port 3000)   | (Static Files)                                │
  │         v               v                                               │
  │  +-------------+ +-------------+                                        │
  │  |   Node.js   | | React Build |                                        │
  │  |   Backend   | |  (HTML/JS)  |                                        │
  │  |  (via PM2)  | |             |                                        │
  │  +-------------+ +-------------+                                        │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  4. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

[Language: JavaScript]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Configuring CORS in Express                                          │
  │                                                                          │
  │  const express = require('express');                                     │
  │  const cors = require('cors');                                           │
  │  const app = express();                                                  │
  │                                                                          │
  │  // Basic usage (allow all - bad for production)                         │
  │  // app.use(cors());                                                     │
  │                                                                          │
  │  // Production usage                                                     │
  │  const corsOptions = {                                                   │
  │      origin: ['https://myfrontend.com', 'https://www.myfrontend.com'],   │
  │      credentials: true, // Allow cookies to be sent                      │
  │      optionsSuccessStatus: 200                                           │
  │  };                                                                      │
  │                                                                          │
  │  app.use(cors(corsOptions));                                             │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

[Language: Nginx]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Complete Nginx Configuration (nginx.conf)                            │
  │                                                                          │
  │  # /etc/nginx/sites-available/myapp                                      │
  │  server {                                                                │
  │      listen 80;                                                          │
  │      server_name myapp.com www.myapp.com;                                │
  │                                                                          │
  │      # Redirect HTTP to HTTPS (Handled by Certbot usually)               │
  │      return 301 https://$host$request_uri;                               │
  │  }                                                                       │
  │                                                                          │
  │  server {                                                                │
  │      listen 443 ssl;                                                     │
  │      server_name myapp.com www.myapp.com;                                │
  │                                                                          │
  │      ssl_certificate /etc/letsencrypt/live/myapp.com/fullchain.pem;      │
  │      ssl_certificate_key /etc/letsencrypt/live/myapp.com/privkey.pem;    │
  │                                                                          │
  │      # Serve React Frontend (Static Files)                               │
  │      location / {                                                        │
  │          root /var/www/myapp/client/build;                               │
  │          index index.html index.htm;                                     │
  │          # Fallback to index.html for React Router                       │
  │          try_files $uri $uri/ /index.html;                               │
  │      }                                                                   │
  │                                                                          │
  │      # Proxy API requests to Node.js backend                             │
  │      location /api/ {                                                    │
  │          proxy_pass http://localhost:3000;                               │
  │          proxy_http_version 1.1;                                         │
  │          proxy_set_header Upgrade $http_upgrade;                         │
  │          proxy_set_header Connection 'upgrade';                          │
  │          proxy_set_header Host $host;                                    │
  │          proxy_cache_bypass $http_upgrade;                               │
  │                                                                          │
  │          # Forward real IP to backend                                    │
  │          proxy_set_header X-Real-IP $remote_addr;                        │
  │          proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;    │
  │      }                                                                   │
  │  }                                                                       │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

  [Language: JavaScript]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // PM2 Ecosystem File (ecosystem.config.js)                             │
  │                                                                          │
  │  module.exports = {                                                      │
  │    apps: [{                                                              │
  │      name: "api-server",                                                 │
  │      script: "./server.js",                                              │
  │      instances: "max", // Cluster mode: utilize all CPU cores            │
  │      exec_mode: "cluster",                                               │
  │      env: {                                                              │
  │        NODE_ENV: "development",                                          │
  │      },                                                                  │
  │      env_production: {                                                   │
  │        NODE_ENV: "production",                                           │
  │        PORT: 3000                                                        │
  │      }                                                                   │
  │    }]                                                                    │
  │  }                                                                       │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

Q1: What is a Reverse Proxy and why use Nginx instead of exposing Node.js directly to port 80?

  ANSWER:
    A reverse proxy handles incoming requests and routes them to internal servers. Nginx is highly optimized for handling thousands of concurrent connections, serving static files efficiently, and performing SSL termination, offloading these resource-heavy tasks from the single-threaded Node process.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: Explain what CORS is and why it exists.

  ANSWER:
    CORS is a browser security mechanism that restricts cross-origin HTTP requests. It exists to prevent malicious scripts on one site from making unauthorized requests to another site's API on behalf of the user.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: What is SSL Termination?

  ANSWER:
    The process where a proxy (like Nginx) decrypts incoming HTTPS traffic and forwards it as plain HTTP to the internal network server, saving the internal server the CPU overhead of decryption.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: Why do we need PM2 for Node.js apps?

  ANSWER:
    Node.js crashes if an unhandled exception occurs. PM2 ensures the process restarts automatically. It also enables clustering (running multiple instances on multiple CPU cores).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: How does React Router work with Nginx? (The try_files directive)

  ANSWER:
    Because React is an SPA, URLs like /dashboard don't exist as physical files. try_files $uri /index.html tells Nginx to serve index.html if the requested file isn't found, allowing React Router to take over routing on the client side.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: What is the difference between an A record and a CNAME?

  ANSWER:
    An A record maps a domain directly to an IP address. A CNAME maps a domain to another domain name (e.g., mapping www.example.com to example.com).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q7: What is the difference between IaaS, PaaS, and SaaS?

  ANSWER:
    IaaS (AWS EC2) gives you raw servers. PaaS (Heroku, Render) abstracts the OS and lets you deploy code directly. SaaS (Google Workspace) is a finished software product.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q8: Why should you never commit .env files?

  ANSWER:
    They contain sensitive secrets (database passwords, API keys). Committing them exposes them to anyone with repository access or the public (if open source).

────────────────────────────────────────────────────────────────────────────────
  7. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

CHALLENGE 1: Riddle

  I intercept all your secure secrets at the gate, stripping off their armor before passing them to the king inside. What process am I?

  SOLUTION:
    SSL Termination.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─


  CHALLENGE 2: Riddle

  A Node app dies, but instantly returns to life. I am the necromancer of processes. Who am I?

  SOLUTION:
    PM2 (Process Manager).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─


  CHALLENGE 3: 

  # Nginx config for React app
  location / {
      root /var/www/build;
      index index.html;
  }

  SOLUTION:
    When a user refreshes the page at myapp.com/profile, Nginx looks for a folder named profile and returns a 404. Fix: Add try_files $uri $uri/ /index.html;.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─


  CHALLENGE 4: 

  // Express server running on api.myapp.com
  app.use(cors({ origin: 'myapp.com' }));

  SOLUTION:
    myapp.com is not a valid origin string. The browser sends https://myapp.com. The string must match exactly, including the protocol.

────────────────────────────────────────────────────────────────────────────────
  8. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  Localhost works differently than production. Without a proxy, your Node server is exposed and unoptimized. Without PM2, your app will experience downtime when it inevitably crashes. Proper deployment architecture ensures high availability, security (HTTPS), and efficient resource utilization.

────────────────────────────────────────────────────────────────────────────────
  9. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

-> File 066: 066 FullStack Architecture (related topic)
  -> File 071: 071 FullStack Security (For more on TLS and Headers.)

================================================================================
  END OF FILE 069
================================================================================
