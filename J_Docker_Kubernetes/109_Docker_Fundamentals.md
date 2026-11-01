================================================================================
  FILE 109: DOCKER FUNDAMENTALS
  Section: J - Docker & Kubernetes
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  Docker Fundamentals: Understanding Containerization and Image Building

  This module introduces the core concepts of containerization using Docker. You will learn the difference between Virtual Machines and Containers, explore the architecture of the Docker engine, understand how Docker images are layered and built using Dockerfiles, and master the Docker CLI to manage container lifecycles. By the end of this module, you will be able to containerize applications written in Node.js, Python, and Java, understand the intricacies of CMD vs ENTRYPOINT, and manage images in registries.

  Prerequisites:
  - Basic understanding of operating systems (Linux/Unix).
  - Familiarity with command-line interfaces.
  - Basic software development concepts.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  Container vs Virtual Machine Architecture                              │
  │                                                                         │
  │    VIRTUAL MACHINES                           CONTAINERS                │
  │                                                                         │
  │  +------------------------+             +------------------------+      │
  │  |       App A            |             |       App A            |      │
  │  |------------------------|             |------------------------|      │
  │  |     Bins/Libs          |             |     Bins/Libs          |      │
  │  |------------------------|             +------------------------+      │
  │  |      Guest OS          |             |       App B            |      │
  │  +------------------------+             |------------------------|      │
  │  |       App B            |             |     Bins/Libs          |      │
  │  |------------------------|             +------------------------+      │
  │  |     Bins/Libs          |             |       App C            |      │
  │  |------------------------|             |------------------------|      │
  │  |      Guest OS          |             |     Bins/Libs          |      │
  │  +------------------------+             +------------------------+      │
  │  |      Hypervisor        |             |      Docker Engine     |      │
  │  +------------------------+             +------------------------+      │
  │  |    Host Operating      |             |    Host Operating      |      │
  │  |        System          |             |        System          |      │
  │  +------------------------+             +------------------------+      │
  │  |       Server           |             |       Server           |      │
  │  +------------------------+             +------------------------+      │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  Docker Image Layers (Union Filesystem)                                 │
  │                                                                         │
  │  +---------------------------------------------------+                  │
  │  | Container Layer (Read/Write)                      |  <-- Created when container runs│
  │  +---------------------------------------------------+                  │
  │  | Layer 4 (Read-Only): RUN apt-get install python3  |  \               │
  │  +---------------------------------------------------+   |              │
  │  | Layer 3 (Read-Only): COPY . /app                  |   |              │
  │  +---------------------------------------------------+    > Image Layers (Immutable)│
  │  | Layer 2 (Read-Only): RUN mkdir /app               |   |              │
  │  +---------------------------------------------------+   |              │
  │  | Layer 1 (Read-Only): FROM ubuntu:20.04            |  /               │
  │  +---------------------------------------------------+                  │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: bash]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Essential Docker CLI Commands                                        │
  │                                                                          │
  │  # 1. Pulling an image                                                   │
  │  docker pull nginx:latest                                                │
  │                                                                          │
  │  # 2. Running a container                                                │
  │  # -d: detached mode (background)                                        │
  │  # -p: map host port 8080 to container port 80                           │
  │  # --name: assign a name to the container                                │
  │  docker run -d -p 8080:80 --name my-nginx nginx:latest                   │
  │                                                                          │
  │  # 3. Listing containers                                                 │
  │  docker ps         # List running containers                             │
  │  docker ps -a      # List all containers (running and stopped)           │
  │                                                                          │
  │  # 4. Stopping and Starting containers                                   │
  │  docker stop my-nginx                                                    │
  │  docker start my-nginx                                                   │
  │                                                                          │
  │  # 5. Viewing container logs                                             │
  │  docker logs my-nginx                                                    │
  │  docker logs -f my-nginx  # Follow the logs live                         │
  │                                                                          │
  │  # 6. Executing commands inside a running container                      │
  │  # -i: interactive, -t: allocate a pseudo-TTY                            │
  │  docker exec -it my-nginx /bin/bash                                      │
  │                                                                          │
  │  # 7. Removing a container                                               │
  │  docker rm my-nginx         # Container must be stopped                  │
  │  docker rm -f my-nginx      # Force remove (kills it first)              │
  │                                                                          │
  │  # 8. Listing and removing images                                        │
  │  docker images                                                           │
  │  docker rmi nginx:latest                                                 │
  └──────────────────────────────────────────────────────────────────────────┘

  [Language: dockerfile]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Dockerfile Instructions                                              │
  │                                                                          │
  │  # Exec form (JSON array) - PREFERRED                                    │
  │  CMD ["executable","param1","param2"]                                    │
  │                                                                          │
  │  # Shell form (invokes /bin/sh -c)                                       │
  │  CMD command param1 param2                                               │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: dockerfile]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │                                                                          │
  │  # Use an official, lightweight Node.js base image                       │
  │  FROM node:18-alpine                                                     │
  │                                                                          │
  │  # Set environment variables                                             │
  │  ENV NODE_ENV=production                                                 │
  │                                                                          │
  │  # Set the working directory inside the container                        │
  │  WORKDIR /usr/src/app                                                    │
  │                                                                          │
  │  # Copy package.json and package-lock.json first to leverage layer caching│
  │  COPY package*.json ./                                                   │
  │                                                                          │
  │  # Install only production dependencies                                  │
  │  # ci (clean install) is preferred for reproducible builds               │
  │  RUN npm ci --only=production                                            │
  │                                                                          │
  │  # Copy the rest of the application code                                 │
  │  COPY . .                                                                │
  │                                                                          │
  │  # Expose the port the app runs on                                       │
  │  EXPOSE 3000                                                             │
  │                                                                          │
  │  # Define the command to run the application                             │
  │  # Using exec form to ensure proper signal handling (e.g., SIGTERM)      │
  │  CMD ["node", "server.js"]                                               │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

  [Language: dockerfile]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │                                                                          │
  │  # Use an official lightweight Python image                              │
  │  FROM python:3.11-slim                                                   │
  │                                                                          │
  │  # Prevent Python from writing pyc files to disc                         │
  │  ENV PYTHONDONTWRITEBYTECODE 1                                           │
  │  # Prevent Python from buffering stdout and stderr                       │
  │  ENV PYTHONUNBUFFERED 1                                                  │
  │                                                                          │
  │  WORKDIR /app                                                            │
  │                                                                          │
  │  # Install system dependencies (if any) and clean up apt cache to reduce image size│
  │  RUN apt-get update && apt-get install -y --no-install-recommends gcc \  │
  │      && rm -rf /var/lib/apt/lists/*                                      │
  │                                                                          │
  │  # Copy requirements file and install python dependencies                │
  │  COPY requirements.txt .                                                 │
  │  RUN pip install --no-cache-dir -r requirements.txt                      │
  │                                                                          │
  │  # Copy the application code                                             │
  │  COPY . .                                                                │
  │                                                                          │
  │  # Expose the port                                                       │
  │  EXPOSE 8000                                                             │
  │                                                                          │
  │  # Create a non-root user for security                                   │
  │  RUN adduser --disabled-password --gecos '' myuser                       │
  │  USER myuser                                                             │
  │                                                                          │
  │  # Run the application                                                   │
  │  CMD ["gunicorn", "--bind", "0.0.0.0:8000", "-k", "uvicorn.workers.UvicornWorker", "main:app"]│
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

  [Language: dockerfile]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │                                                                          │
  │  # -------------------------                                             │
  │  # Stage 1: Build Stage                                                  │
  │  # -------------------------                                             │
  │  FROM maven:3.9.4-eclipse-temurin-17 AS builder                          │
  │                                                                          │
  │  WORKDIR /app                                                            │
  │  COPY pom.xml .                                                          │
  │  # Download dependencies first for caching                               │
  │  RUN mvn dependency:go-offline                                           │
  │                                                                          │
  │  COPY src ./src                                                          │
  │  # Build the application                                                 │
  │  RUN mvn clean package -DskipTests                                       │
  │                                                                          │
  │  # -------------------------                                             │
  │  # Stage 2: Runtime Stage                                                │
  │  # -------------------------                                             │
  │  FROM eclipse-temurin:17-jre-alpine                                      │
  │                                                                          │
  │  WORKDIR /app                                                            │
  │                                                                          │
  │  # Copy the JAR from the builder stage                                   │
  │  COPY --from=builder /app/target/myapp-1.0.0.jar app.jar                 │
  │                                                                          │
  │  EXPOSE 8080                                                             │
  │                                                                          │
  │  ENTRYPOINT ["java", "-jar", "app.jar"]                                  │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  7. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

────────────────────────────────────────────────────────────────────────────────
  8. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: Riddle 1: The Ignored Argument

  Scenario: You have this Dockerfile:
  `dockerfile
  FROM node:14
  ENTRYPOINT ["node", "server.js"]
  CMD ["--port", "8080"]
  `
  You run docker run myapp --env prod. The app crashes saying "Unknown argument: --env".
  What's wrong?

  SOLUTION:
    CMD provides default arguments. When you run docker run myapp --env prod, the string --env prod completely *overrides* the CMD. So the container executes node server.js --env prod, missing the --port 8080 part. You must provide all required arguments when overriding CMD.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 2: Riddle 2: The Cache Buster

  Scenario: A developer complains their Docker build takes 5 minutes every time they change one line of HTML code.
  `dockerfile
  FROM python:3.9
  WORKDIR /app
  COPY . .
  RUN pip install -r requirements.txt
  CMD ["python", "app.py"]
  `
  What's wrong?

  SOLUTION:
    COPY . . copies all application code *before* running pip install. Any change to the HTML file invalidates the cache for the COPY layer, forcing RUN pip install to execute again and download all packages.
    Fix: Copy requirements.txt first, run pip install, and then copy the rest of the code.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 3: Riddle 3: The Ghost Process

  Scenario: You start a container running an Nginx web server in the background using docker run -d my-nginx. You check docker ps immediately after, but the container is not there. You check docker ps -a and see it exited with code 0.
  Dockerfile snippet:
  `dockerfile
  CMD service nginx start
  `
  What's wrong?

  SOLUTION:
    Containers live only as long as their main foreground process lives. service nginx start starts Nginx as a background daemon, then the script finishes. Since the main command finished, the container immediately exits.
    Fix: Run Nginx in the foreground: CMD ["nginx", "-g", "daemon off;"]

────────────────────────────────────────────────────────────────────────────────
  9. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  - Consistency: "It works on my machine" is solved. The container has the exact same OS, libraries, and binaries in Dev, QA, and Prod.
  - Microservices Enabler: Docker makes it trivial to package hundreds of small microservices individually, each with distinct dependencies, without conflict on the host machine.
  - Resource Efficiency: Because containers share the OS kernel, you can run significantly more containers on a physical server compared to VMs, reducing cloud infrastructure costs.
  - CI/CD Integration: Docker images are the standard artifact in modern CI/CD pipelines. You build the image once, test the image, and deploy that exact same image to production.
  - Fast Scaling: Containers start in milliseconds (unlike VMs which take minutes to boot the OS). This allows orchestrators like Kubernetes to rapidly scale up applications under heavy traffic load.

================================================================================
  END OF FILE 109
================================================================================
