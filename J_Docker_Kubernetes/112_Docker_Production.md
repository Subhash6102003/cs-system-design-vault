================================================================================
  FILE 112: DOCKER IN PRODUCTION: OPTIMIZATION & SECURITY
  Section: J - Docker & Kubernetes
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  Docker in Production: Best Practices for Image Optimization, Security, and Reliability

  Building a Docker image that "works on my machine" is easy. Building a Docker image that is secure, lightweight, heavily cached, and ready for a production orchestrator like Kubernetes requires discipline. This module covers advanced Dockerfile techniques like Multi-stage builds to drastically reduce image sizes, security practices like running as non-root users, optimizing layer caching for faster CI/CD pipelines, handling application healthchecks, and managing resource constraints.

  Prerequisites:
  - Solid understanding of Dockerfiles and Layers (File 109).
  - Basic understanding of Linux user permissions.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  Multi-Stage Build Architecture                                         │
  │                                                                         │
  │    Stage 1: "builder" (Heavy)                 Stage 2: "production" (Lightweight)│
  │  +--------------------------------+         +--------------------------------+│
  │  | FROM node:18 AS builder        |         | FROM node:18-alpine            |│
  │  | (Size: ~1GB)                   |         | (Size: ~150MB)                 |│
  │  |                                |         |                                |│
  │  | 1. Install gcc, python, make   |         | 1. Install zero build tools    |│
  │  | 2. COPY source code            |         |                                |│
  │  | 3. npm install (compiles C++)  | ======> | 2. COPY --from=builder         |│
  │  | 4. npm run build               | (Only   |    /app/dist ./dist            |│
  │  |    (Generates /dist folder)    | moves   |    /app/node_modules ./node... |│
  │  +--------------------------------+ final   |                                |│
  │          | Discarded              | assets) | 3. CMD ["node", "dist/app.js"] |│
  │          V                        |         +--------------------------------+│
  │      (Thrown away)                |                 | Deployed to Production│
  │                                   +----------------->                   │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: dockerfile]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Optimizing Layer Caching                                             │
  │                                                                          │
  │  FROM node:18                                                            │
  │  WORKDIR /app                                                            │
  │  # Copies EVERYTHING. If any README or HTML file changes,                │
  │  # the cache is busted, and npm install runs again.                      │
  │  COPY . .                                                                │
  │  RUN npm install                                                         │
  │  CMD ["node", "app.js"]                                                  │
  └──────────────────────────────────────────────────────────────────────────┘

  [Language: bash]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Resource Limits & Logging Drivers (CLI)                              │
  │                                                                          │
  │  # Run container with strict resource limits                             │
  │  # max 512MB RAM, max 1.5 CPU cores                                      │
  │  docker run -d \                                                         │
  │    --memory="512m" \                                                     │
  │    --cpus="1.5" \                                                        │
  │    --name my-api \                                                       │
  │    my-api:latest                                                         │
  │                                                                          │
  │  # Run container with JSON logging driver and size limits                │
  │  # Prevents logs from consuming all disk space                           │
  │  docker run -d \                                                         │
  │    --log-driver json-file \                                              │
  │    --log-opt max-size=10m \                                              │
  │    --log-opt max-file=3 \                                                │
  │    nginx                                                                 │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: dockerfile]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │                                                                          │
  │  # ---------------------------------------------------                   │
  │  # Stage 1: Build Stage (Heavy, contains Go compiler)                    │
  │  # ---------------------------------------------------                   │
  │  FROM golang:1.21-alpine AS builder                                      │
  │                                                                          │
  │  # Install git, required for fetching dependencies                       │
  │  RUN apk update && apk add --no-cache git                                │
  │                                                                          │
  │  WORKDIR /app                                                            │
  │                                                                          │
  │  # Optimize cache by downloading dependencies first                      │
  │  COPY go.mod go.sum ./                                                   │
  │  RUN go mod download                                                     │
  │                                                                          │
  │  # Copy source code                                                      │
  │  COPY . .                                                                │
  │                                                                          │
  │  # Compile the Go application statically                                 │
  │  # CGO_ENABLED=0 ensures no C dependencies are linked                    │
  │  # -ldflags="-w -s" strips debugging info to reduce binary size          │
  │  RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -ldflags="-w -s" -o /go-api ./main.go│
  │                                                                          │
  │  # ---------------------------------------------------                   │
  │  # Stage 2: Runtime Stage (Ultra-light, secure)                          │
  │  # ---------------------------------------------------                   │
  │  # Use Google's distroless static image.                                 │
  │  # It contains NO shell, NO package manager. Extremely secure.           │
  │  FROM gcr.io/distroless/static-debian12:nonroot                          │
  │                                                                          │
  │  WORKDIR /                                                               │
  │                                                                          │
  │  # Copy the compiled binary from the builder stage                       │
  │  COPY --from=builder /go-api /go-api                                     │
  │                                                                          │
  │  # The distroless image automatically runs as a non-root user            │
  │                                                                          │
  │  EXPOSE 8080                                                             │
  │                                                                          │
  │  # Execute the binary                                                    │
  │  ENTRYPOINT ["/go-api"]                                                  │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

  [Language: dockerfile]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │                                                                          │
  │  FROM nginx:alpine                                                       │
  │                                                                          │
  │  COPY ./html /usr/share/nginx/html                                       │
  │                                                                          │
  │  # Tell Docker how to test if this container is healthy                  │
  │  # Curl the local server every 30s. If it fails 3 times, mark as 'unhealthy'│
  │  HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \ │
  │    CMD wget --quiet --tries=1 --spider http://localhost/ || exit 1       │
  │                                                                          │
  │  EXPOSE 80                                                               │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  7. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

────────────────────────────────────────────────────────────────────────────────
  8. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: Riddle 1: The Bloated Image

  Scenario: A developer wants to shrink their image size by removing apt caches.
  `dockerfile
  FROM ubuntu:22.04
  RUN apt-get update
  RUN apt-get install -y curl nginx
  RUN rm -rf /var/lib/apt/lists/*
  `
  The image size didn't shrink at all!
  What's wrong?

  SOLUTION:
    Each RUN command creates a separate layer in the Union Filesystem. Layer 2 downloads the cache. Layer 3 installs. Layer 4 deletes the cache. Because earlier layers are read-only and preserved, the cache data still exists in Layer 2, consuming space in the final image.
    Fix: Chain the commands into a single RUN instruction using &&:
    RUN apt-get update && apt-get install -y curl nginx && rm -rf /var/lib/apt/lists/*

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 2: Riddle 2: The Permission Denied

  Scenario: You implement security best practices and switch to a non-root user.
  `dockerfile
  FROM node:18
  WORKDIR /app
  RUN addgroup --system mygroup && adduser --system myuser --ingroup mygroup
  USER myuser
  COPY . .
  RUN npm install
  CMD ["node", "app.js"]
  `
  The build fails at npm install with EACCES: permission denied, mkdir '/app/node_modules'.
  What's wrong?

  SOLUTION:
    WORKDIR /app was executed as root (default user). COPY . . was executed as root (because the USER instruction doesn't change file ownership). So /app is owned by root. When npm install runs as myuser, it doesn't have permission to write to /app.
    Fix: Use COPY --chown=myuser:mygroup . .

────────────────────────────────────────────────────────────────────────────────
  9. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  - Cost Savings: Multi-stage builds reduce image sizes from Gigabytes to Megabytes. This drastically reduces the network bandwidth needed to push/pull images from registries and reduces storage costs.
  - Speed to Recovery: If a node in Kubernetes dies, it must pull images to the new node to restart pods. Pulling a 50MB image takes 1 second. Pulling a 2GB image takes minutes. Time is uptime.
  - Security Posture: Smaller images (especially distroless) have a smaller attack surface. Less OS tools mean fewer CVEs in security scans, keeping the Security / SecOps teams happy and compliant.
  - Stability: Setting explicit resource limits prevents "noisy neighbor" problems, where one container with a memory leak crashes other applications running on the same host.

================================================================================
  END OF FILE 112
================================================================================
