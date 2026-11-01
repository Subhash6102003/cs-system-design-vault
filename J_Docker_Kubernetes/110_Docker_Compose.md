================================================================================
  FILE 110: DOCKER COMPOSE
  Section: J - Docker & Kubernetes
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  Docker Compose: Defining and Running Multi-Container Applications

  This module explores Docker Compose, a tool for defining and running multi-container Docker applications. While the Docker CLI is excellent for single containers, modern applications (e.g., a web frontend, an API backend, a database, and a cache) require multiple containers working together. Docker Compose uses a YAML file (docker-compose.yml) to configure application services, networks, and volumes in a single declarative file. By the end of this module, you will understand how to orchestrate local development environments, manage service dependencies, and configure networking and volumes across multiple containers.

  Prerequisites:
  - Completion of 109DockerFundamentals.
  - Basic understanding of YAML syntax.
  - Understanding of web application architectures (e.g., 3-tier architecture).

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  Multi-Container App Architecture (Compose)                             │
  │                                                                         │
  │                          Host Machine (Developer Laptop)                │
  │  +--------------------------------------------------------------------------------+│
  │  |                                                                                |│
  │  |  +--------------------+                                                        |│
  │  |  |   docker-compose   |                                                        |│
  │  |  |       .yml         |                                                        |│
  │  |  +---------+----------+                                                        |│
  │  |            | `docker-compose up`                                               |│
  │  |            v                                                                   |│
  │  |  ========================= Default Bridge Network =========================    |│
  │  |       |                           |                            |               |│
  │  |       v                           v                            v               |│
  │  | +-----------+  (HTTP :80)   +-----------+  (TCP :5432)   +-----------+         |│
  │  | | Frontend  | ------------> |  Backend  | -------------> | Database  |         |│
  │  | | (React)   |               | (Node.js) |                | (Postgres)|         |│
  │  | +-----------+               +-----+-----+                +-----+-----+         |│
  │  |       ^                           |                            |               |│
  │  |       | (Ports 3000:80)           | (TCP :6379)                | (Mount)       |│
  │  |       |                           v                            v               |│
  │  |       |                     +-----------+                +-----------+         |│
  │  |       |                     |   Cache   |                |  Volume   |         |│
  │  |       |                     |  (Redis)  |                | (pg_data) |         |│
  │  |       |                     +-----------+                +-----------+         |│
  │  +-------|------------------------------------------------------------------------+│
  │          |                                                              │
  │      [User Browser]                                                     │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: bash]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Essential Docker Compose Commands                                    │
  │                                                                          │
  │  # Start all services defined in docker-compose.yml in detached mode (-d)│
  │  docker-compose up -d                                                    │
  │                                                                          │
  │  # Stop and remove all containers, networks, and default volumes         │
  │  docker-compose down                                                     │
  │                                                                          │
  │  # Stop and remove, including named volumes                              │
  │  docker-compose down -v                                                  │
  │                                                                          │
  │  # Stop services (without removing containers)                           │
  │  docker-compose stop                                                     │
  │                                                                          │
  │  # Start stopped services                                                │
  │  docker-compose start                                                    │
  │                                                                          │
  │  # Rebuild images before starting services (if Dockerfiles changed)      │
  │  docker-compose up -d --build                                            │
  │                                                                          │
  │  # View logs for all services (follow mode)                              │
  │  docker-compose logs -f                                                  │
  │                                                                          │
  │  # View logs for a specific service                                      │
  │  docker-compose logs -f backend                                          │
  │                                                                          │
  │  # List running services in the current project                          │
  │  docker-compose ps                                                       │
  │                                                                          │
  │  # Execute a command in a running service container                      │
  │  docker-compose exec db psql -U postgres                                 │
  │                                                                          │
  │  # Scale a specific service to multiple instances                        │
  │  docker-compose up -d --scale frontend=3                                 │
  └──────────────────────────────────────────────────────────────────────────┘

  [Language: ini]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Environment Variable Interpolation (.env file)                       │
  │                                                                          │
  │  POSTGRES_USER=admin                                                     │
  │  POSTGRES_PASSWORD=supersecret                                           │
  │  PORT=8080                                                               │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: yaml]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │                                                                          │
  │  version: '3.8'                                                          │
  │                                                                          │
  │  services:                                                               │
  │    nginx:                                                                │
  │      image: nginx:alpine                                                 │
  │      ports:                                                              │
  │        - "80:80"                                                         │
  │      volumes:                                                            │
  │        - ./nginx.conf:/etc/nginx/nginx.conf:ro                           │
  │      depends_on:                                                         │
  │        - api                                                             │
  │      networks:                                                           │
  │        - app-network                                                     │
  │                                                                          │
  │    api:                                                                  │
  │      build:                                                              │
  │        context: ./api                                                    │
  │        dockerfile: Dockerfile                                            │
  │      image: my-node-api:1.0                                              │
  │      expose:                                                             │
  │        - "3000"                                                          │
  │      environment:                                                        │
  │        - NODE_ENV=production                                             │
  │        - DB_HOST=postgres_db                                             │
  │        - DB_USER=${DB_USER}                                              │
  │        - DB_PASSWORD=${DB_PASSWORD}                                      │
  │        - REDIS_HOST=redis_cache                                          │
  │      depends_on:                                                         │
  │        postgres_db:                                                      │
  │          condition: service_healthy                                      │
  │        redis_cache:                                                      │
  │          condition: service_started                                      │
  │      networks:                                                           │
  │        - app-network                                                     │
  │      restart: unless-stopped                                             │
  │                                                                          │
  │    postgres_db:                                                          │
  │      image: postgres:15-alpine                                           │
  │      environment:                                                        │
  │        - POSTGRES_USER=${DB_USER}                                        │
  │        - POSTGRES_PASSWORD=${DB_PASSWORD}                                │
  │        - POSTGRES_DB=myapp                                               │
  │      volumes:                                                            │
  │        - pgdata:/var/lib/postgresql/data                                 │
  │      networks:                                                           │
  │        - app-network                                                     │
  │      healthcheck:                                                        │
  │        test: ["CMD-SHELL", "pg_isready -U ${DB_USER} -d myapp"]          │
  │        interval: 10s                                                     │
  │        timeout: 5s                                                       │
  │        retries: 5                                                        │
  │      restart: always                                                     │
  │                                                                          │
  │    redis_cache:                                                          │
  │      image: redis:7-alpine                                               │
  │      networks:                                                           │
  │        - app-network                                                     │
  │      volumes:                                                            │
  │        - redisdata:/data                                                 │
  │      restart: always                                                     │
  │                                                                          │
  │  networks:                                                               │
  │    app-network:                                                          │
  │      driver: bridge                                                      │
  │                                                                          │
  │  volumes:                                                                │
  │    pgdata:                                                               │
  │    redisdata:                                                            │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

  [Language: yaml]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │                                                                          │
  │  version: '3.8'                                                          │
  │                                                                          │
  │  services:                                                               │
  │    fastapi_app:                                                          │
  │      build: ./backend                                                    │
  │      ports:                                                              │
  │        - "8000:8000"                                                     │
  │      environment:                                                        │
  │        - MONGO_URL=mongodb://mongo_db:27017                              │
  │      depends_on:                                                         │
  │        - mongo_db                                                        │
  │      volumes:                                                            │
  │        - ./backend:/app  # Bind mount for hot-reloading during development│
  │                                                                          │
  │    mongo_db:                                                             │
  │      image: mongo:6.0                                                    │
  │      ports:                                                              │
  │        - "27017:27017" # Exposed to host for direct DB debugging         │
  │      volumes:                                                            │
  │        - mongodb_data:/data/db                                           │
  │                                                                          │
  │  volumes:                                                                │
  │    mongodb_data:                                                         │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  7. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

────────────────────────────────────────────────────────────────────────────────
  8. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: Riddle 1: The Impatient API

  Scenario: You start your stack. The API container crashes immediately with "Connection Refused: Database".
  `yaml
  services:
  api:
  image: myapi
  depends_on:
  - db
  db:
  image: postgres
  `
  What's wrong?

  SOLUTION:
    depends_on only ensures the db container is *created and started* before the api container. PostgreSQL takes a few seconds to initialize its internal data and start accepting connections. The API starts instantly and tries to connect before Postgres is ready.
    Fix: Add a healthcheck to the db service and use dependson: db: condition: servicehealthy.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 2: Riddle 2: The Port Conflict

  Scenario: You want to run 3 instances of your backend web service.
  `yaml
  services:
  web:
  image: myweb
  ports:
  - "8080:80"
  `
  You run docker-compose up --scale web=3. Docker throws an error and fails to start.
  What's wrong?

  SOLUTION:
    By specifying 8080:80, you are forcing Docker to bind port 80 of the container to port 8080 on the host machine. When scaling to 3 containers, Docker tries to bind the second container to host port 8080, which is already in use by the first container.
    Fix: Change ports to -"80" (Docker assigns random host ports) or put a reverse proxy in front.

────────────────────────────────────────────────────────────────────────────────
  9. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  While Docker Compose is predominantly used as a local development tool, its concepts mirror production orchestration systems like Kubernetes.
  - Local Dev Parity: Compose allows developers to spin up the entire application stack (DB, Cache, Queues, APIs) locally with a single command, ensuring the dev environment closely matches production.
  - On-Premise Deployments: For smaller applications or single-server deployments, docker-compose is absolutely a valid production deployment strategy. Tools like Docker Swarm even natively consume Compose files.
  - Automated Testing: Compose is heavily used in CI pipelines. You can spin up a transient database, run integration tests against it using a test runner container, and tear the whole stack down (docker-compose down) ensuring a clean state every time.

================================================================================
  END OF FILE 110
================================================================================
