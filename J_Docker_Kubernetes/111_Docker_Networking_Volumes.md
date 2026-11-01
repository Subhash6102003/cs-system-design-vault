================================================================================
  FILE 111: DOCKER NETWORKING & VOLUMES
  Section: J - Docker & Kubernetes
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  Docker Networking & Volumes: Mastering Container Communication and Data Persistence

  By default, Docker containers are ephemeral and isolated. Any data created inside a container is lost when the container is removed, and containers cannot communicate with each other or the outside world without explicit network configurations. This module dives deep into how Docker handles communication through Networking Drivers (Bridge, Host, Overlay) and how it handles data persistence through Volumes (Named Volumes, Bind Mounts, tmpfs). Understanding these concepts is critical for running stateful applications like databases and building distributed architectures.

  Prerequisites:
  - Understanding of Docker container lifecycles (File 109).
  - Basic understanding of networking (IP addresses, ports, DNS).

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  Bridge Network Architecture                                            │
  │                                                                         │
  │                       Docker Host (Physical/Virtual Machine)            │
  │  +-------------------------------------------------------------------------+│
  │  |    Host Network Interface (eth0) IP: 192.168.1.100                      |│
  │  |                                                                         |│
  │  |    Port Mapping: 8080 -> 80                                             |│
  │  |          |                                                              |│
  │  |          v                                                              |│
  │  |  +-------------------------------------------------------------------+  |│
  │  |  |                 Custom Bridge Network: "my-net"                   |  |│
  │  |  |                        Subnet: 172.18.0.0/16                      |  |│
  │  |  +-------------------------------------------------------------------+  |│
  │  |          |                                            |                 |│
  │  |          v                                            v                 |│
  │  | +-------------------+ (eth0)                 +-------------------+      |│
  │  | | Container A (Web) | IP: 172.18.0.2         | Container B (DB)  |      |│
  │  | | DNS Name: web     | <--------------------> | DNS Name: db      |      |│
  │  | +-------------------+       Internal Comms   +-------------------+      |│
  │  |                                                                         |│
  │  +-------------------------------------------------------------------------+│
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  Volume Mount Types Comparison                                          │
  │                                                                         │
  │  +-----------------------+       +-------------------+       +-----------------------+│
  │  |  Host Filesystem      |       |  Docker Managed   |       |    Host Memory        |│
  │  |  (e.g., /app/src)     |       |  /var/lib/docker/ |       |       (RAM)           |│
  │  +-----------------------+       +-------------------+       +-----------------------+│
  │            |                               |                             |│
  │            | BIND MOUNT                    | NAMED VOLUME                | TMPFS MOUNT│
  │            v                               v                             v│
  │  +-------------------------------------------------------------------------------+│
  │  |                             Docker Container                                  |│
  │  |                             (e.g., /usr/src/app)                              |│
  │  +-------------------------------------------------------------------------------+│
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: bash]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Networking Commands                                                  │
  │                                                                          │
  │  # 1. List all networks                                                  │
  │  docker network ls                                                       │
  │                                                                          │
  │  # 2. Create a custom bridge network                                     │
  │  docker network create my-app-network                                    │
  │                                                                          │
  │  # 3. Inspect a network (see subnet, gateway, and connected containers)  │
  │  docker network inspect my-app-network                                   │
  │                                                                          │
  │  # 4. Run a container attached to the custom network                     │
  │  docker run -d --name web --network my-app-network nginx                 │
  │                                                                          │
  │  # 5. Connect an already running container to a network                  │
  │  docker network connect my-app-network existing-container                │
  │                                                                          │
  │  # 6. Run a container on the host network (Warning: port conflicts possible)│
  │  docker run -d --name host-web --network host nginx                      │
  └──────────────────────────────────────────────────────────────────────────┘

  [Language: bash]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Volumes and Data Persistence Commands                                │
  │                                                                          │
  │  # 1. List volumes                                                       │
  │  docker volume ls                                                        │
  │                                                                          │
  │  # 2. Create a named volume                                              │
  │  docker volume create pg_data                                            │
  │                                                                          │
  │  # 3. Inspect a volume (shows Mountpoint on host)                        │
  │  docker volume inspect pg_data                                           │
  │                                                                          │
  │  # 4. Run a container using a Named Volume                               │
  │  # Syntax: -v <volume-name>:<container-path>                             │
  │  docker run -d --name postgres-db \                                      │
  │    -e POSTGRES_PASSWORD=secret \                                         │
  │    -v pg_data:/var/lib/postgresql/data \                                 │
  │    postgres:15                                                           │
  │                                                                          │
  │  # 5. Run a container using a Bind Mount                                 │
  │  # Syntax: -v <absolute-host-path>:<container-path>                      │
  │  docker run -d --name dev-node \                                         │
  │    -v $(pwd)/src:/usr/src/app \                                          │
  │    -p 3000:3000 \                                                        │
  │    node:18 npm start                                                     │
  │                                                                          │
  │  # 6. Run a container using tmpfs (Memory only)                          │
  │  docker run -d --name secure-cache \                                     │
  │    --tmpfs /app/secrets \                                                │
  │    my-app                                                                │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: bash]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │                                                                          │
  │  #!/bin/bash                                                             │
  │  VOLUME_NAME=$1                                                          │
  │  BACKUP_DIR="/opt/backups"                                               │
  │                                                                          │
  │  # Run a temporary alpine container                                      │
  │  # Mount the named volume to /volume                                     │
  │  # Bind mount the host backup dir to /backup                             │
  │  # Tar the contents                                                      │
  │  docker run --rm \                                                       │
  │    -v ${VOLUME_NAME}:/volume \                                           │
  │    -v ${BACKUP_DIR}:/backup \                                            │
  │    alpine tar -czf /backup/${VOLUME_NAME}_backup_$(date +%Y%m%d).tar.gz -C /volume .│
  │                                                                          │
  │  echo "Backup created at ${BACKUP_DIR}"                                  │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

  [Language: bash]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │                                                                          │
  │  #!/bin/bash                                                             │
  │  VOLUME_NAME=$1                                                          │
  │  BACKUP_FILE=$2                                                          │
  │                                                                          │
  │  # Create volume if it doesn't exist                                     │
  │  docker volume create ${VOLUME_NAME}                                     │
  │                                                                          │
  │  # Extract tarball into the volume                                       │
  │  docker run --rm \                                                       │
  │    -v ${VOLUME_NAME}:/volume \                                           │
  │    -v $(pwd):/backup \                                                   │
  │    alpine tar -xzf /backup/${BACKUP_FILE} -C /volume                     │
  │                                                                          │
  │  echo "Restore complete"                                                 │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  7. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

────────────────────────────────────────────────────────────────────────────────
  8. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: Riddle 1: The Deaf Containers

  Scenario: You start a Node backend and a Mongo database.
  `bash
  docker run -d --name mongo mongo:latest
  docker run -d --name backend -e MONGO_URL=mongodb://mongo:27017 mynode:latest
  `
  The backend logs show: MongoNetworkError: getaddrinfo ENOTFOUND mongo.
  What's wrong?

  SOLUTION:
    When you run containers without specifying a network, they join the default docker0 bridge. The default bridge does *not* support automatic DNS resolution via container name.
    Fix: Create a custom network first: docker network create mynet, then append --network mynet to both run commands.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 2: Riddle 2: The Missing Files

  Scenario: A developer wants to inject a config file into Nginx.
  `bash
  docker run -d -p 80:80 -v /opt/nginx.conf:/etc/nginx/nginx.conf nginx
  `
  Docker crashes with an error: failed to create containerd task: OCI runtime create failed: containerlinux.go:380: starting container process caused: processlinux.go:545: container init caused: rootfs_linux.go:76: mounting "/opt/nginx.conf" to rootfs at "/etc/nginx/nginx.conf" caused: mount through procfd: not a directory.
  What's wrong?

  SOLUTION:
    If /opt/nginx.conf does not exist on the host machine before running the command, Docker assumes you meant to mount a *directory*, so it automatically creates a directory named /opt/nginx.conf/ on the host, and tries to mount it over a *file* inside the container.
    Fix: Ensure the file exists on the host machine *before* running the docker run command.

────────────────────────────────────────────────────────────────────────────────
  9. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  - Security & Isolation: Networks allow you to create micro-segmentation. You can put your Web containers on a frontend network and DB containers on a backend network, ensuring the Web containers can talk to the backend API, but *not* directly to the DB.
  - Stateful Applications: Databases, message queues (Kafka, RabbitMQ), and caching servers require persistent storage. Without volumes, containers are strictly stateless. Volumes are the bridge between ephemeral compute and durable data.
  - Performance: For I/O intensive databases, the container's overlay filesystem is too slow. Volumes bypass the Union Filesystem entirely, writing directly to the host's disk at native speeds.

================================================================================
  END OF FILE 111
================================================================================
