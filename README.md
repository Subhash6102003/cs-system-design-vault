# 🏛️ Computer Science & System Design Knowledge Vault

> **A Comprehensive 152-Module Engineering Knowledge Base** covering Hardware Architecture, Java DSA, Relational & Distributed Databases, Backend Engineering, Frontend Deep Dives, Fullstack Integration, Android Development, Large-Scale System Design (HLD & LLD), AWS Cloud, Docker & Kubernetes, Python, Machine Learning / LLMs / RAG, and Forward-Deployed Engineering.

[![Modules](https://img.shields.io/badge/Modules-152%20Complete-brightgreen)]()
[![System Design](https://img.shields.io/badge/System%20Design-HLD%20%26%20LLD-blue)]()
[![Java DSA](https://img.shields.io/badge/DSA-LeetCode%20Patterns-orange)]()
[![Cloud & DevOps](https://img.shields.io/badge/Cloud-AWS%20%7C%20K8s%20%7C%20Docker-3b82f6)]()
[![AI & LLM](https://img.shields.io/badge/AI%2FML-PyTorch%20%7C%20Transformers%20%7C%20RAG-purple)]()
[![License](https://img.shields.io/badge/License-MIT-green)]()

---

## 🏛️ System Design & Distributed Architecture Diagrams

### 1. Hyperscale Distributed System Topology (HLD)

This diagram illustrates the canonical end-to-end architecture for high-concurrency distributed systems covered throughout Section H and Section C:

```mermaid
flowchart TD
    subgraph Client_Layer ["📱 Client Layer"]
        Mobile["Native Android / iOS Apps\n(Jetpack Compose, Swift)"]
        WebClient["Web Applications\n(Next.js, React 19)"]
        IoT["IoT & External Systems\n(MQTT / WebSockets)"]
    end

    subgraph Edge_Security ["🌐 Global Edge & Security Network"]
        DNS["Route 53 / Anycast DNS\n(Latency-Based Routing & Health Checks)"]
        CDN["CloudFront / Cloudflare Edge CDN\n(Static Assets, SSL Termination, DDoS Guard)"]
        WAF["AWS WAF / Shield\n(Rate Limiting & OWASP Rules)"]
    end

    subgraph Ingress_Routing ["🚪 API Ingress & Gateway Layer"]
        ALB["Application Load Balancer / NLB\n(L4/L7 Flow Distribution)"]
        APIGateway["API Gateway (Envoy / Kong)\n(JWT Auth, Token Bucket Rate Limiter, Tracing)"]
    end

    subgraph Core_Services ["⚙️ Microservices Compute Cluster (EKS / ECS)"]
        AuthSvc["Auth Service\n(OAuth2 / OIDC / Session Tokens)"]
        UserSvc["User & Profile Service\n(Domain Driven Design)"]
        FeedSvc["Feed & Ranking Service\n(Graph & Vector Retrieval)"]
        PaymentSvc["Payment & Transaction Service\n(Idempotent Saga Pattern)"]
        NotifSvc["Notification Dispatcher\n(Push, SMS, WebHooks)"]
    end

    subgraph Event_Stream ["📨 Event Bus & Streaming Backbone"]
        Kafka[("Apache Kafka Cluster\n(Distributed Event Log, CQRS, CDC via Debezium)")]
    end

    subgraph Caching_Tier ["⚡ High-Speed Caching Layer"]
        RedisCluster[("Redis Enterprise Cluster\n(Cluster Sharding, Cache-Aside, Write-Through)")]
    end

    subgraph Persistence_Tier ["💾 Polyglot Storage & Database Tier"]
        PGPrimary[("PostgreSQL Primary\n(ACID Writes & WAL Streaming)")]
        PGReplicas[("PostgreSQL Read Replicas\n(High-Throughput Read Scaling)")]
        CassandraCluster[("Cassandra / ScyllaDB\n(Wide-Column NoSQL, High-Volume Time-Series)")]
        DocDB[("MongoDB / DynamoDB\n(Document & Key-Value Schemas)")]
    end

    subgraph Analytics_OLAP ["📊 Analytical Lakehouse & OLAP Tier"]
        VectorDB[("Pinecone / Qdrant\n(Vector Embeddings & Semantic Search)")]
        Lakehouse[("Snowflake / ClickHouse / Apache Iceberg\n(Columnar Analytics & Real-Time Aggregates)")]
    end

    Client_Layer --> DNS
    DNS --> CDN
    CDN --> WAF
    WAF --> ALB
    ALB --> APIGateway
    APIGateway --> Core_Services

    Core_Services <--> RedisCluster
    Core_Services --> Kafka
    Kafka --> Core_Services
    Kafka --> Lakehouse

    UserSvc --> PGPrimary
    FeedSvc --> PGReplicas
    PaymentSvc --> PGPrimary
    PGPrimary -->|WAL Replication| PGReplicas
    NotifSvc --> CassandraCluster
    FeedSvc <--> VectorDB
```

---

### 2. End-to-End Layered Execution Lifecycle (LLD & Microservices)

This sequence diagram maps the complete request lifecycle across client presentation, offline-first caching, network interceptors, gateway validation, and distributed data persistence:

```mermaid
sequenceDiagram
    autonumber
    actor User as User
    participant UI as Jetpack Compose / React UI
    participant VM as ViewModel / State Manager
    participant Repo as Repository Pattern
    participant LocalDB as Local Cache (Room / SQLite)
    participant Net as Network Interceptor (Auth & Retry)
    participant Gateway as API Gateway (Envoy)
    participant Svc as Domain Microservice
    participant Redis as Redis Cache
    participant DB as Relational Database

    User->>UI: Trigger Action (e.g., Post Creation)
    UI->>VM: Dispatch Intent / Event
    VM->>Repo: Execute createPost(payload)
    Repo->>LocalDB: Optimistic Write (status: PENDING)
    LocalDB-->>UI: Instantly render optimistic UI state
    Repo->>Net: Send HTTP/2 request with Idempotency-Key
    Net->>Gateway: Signed request + Bearer JWT
    Gateway->>Gateway: Token verification & Rate limit check
    Gateway->>Svc: Route to PostService.create()
    Svc->>Redis: Check idempotency key in cache
    alt Key already exists (Duplicate Request)
        Redis-->>Svc: Return cached response
        Svc-->>Gateway: 200 OK (Idempotent response)
    else First-time Execution
        Svc->>DB: Execute Transaction (INSERT post + outbox event)
        DB-->>Svc: Commit confirmed
        Svc->>Redis: Cache response with 1-hour TTL
        Svc-->>Gateway: 201 Created
    end
    Gateway-->>Net: 201 Created Response
    Net-->>Repo: Response payload received
    Repo->>LocalDB: Update local post (status: SYNCED)
    LocalDB-->>UI: Emit updated StateFlow to UI
```

---

### 3. The 55-Phase System Design Interview Execution Framework

A structured methodology for tackling complex Large-Scale System Design problems in top-tier engineering interviews:

```mermaid
flowchart LR
    subgraph Step1 ["Phase 1: Clarification"]
        P1["1. Scope & Constraints\n2. Functional Requirements\n3. Non-Functional SLAs (99.99%)"]
    end

    subgraph Step2 ["Phase 2: Estimation"]
        P2["4. DAU / MAU & QPS Math\n5. Read / Write Ratios\n6. Storage & Bandwidth Budgets"]
    end

    subgraph Step3 ["Phase 3: API Contracts"]
        P3["7. REST / gRPC Schemas\n8. Pagination & Headers\n9. Error Codes & Idempotency"]
    end

    subgraph Step4 ["Phase 4: Data Modeling"]
        P4["10. Relational vs NoSQL\n11. Sharding Keys\n12. Indexing Strategy"]
    end

    subgraph Step5 ["Phase 5: High-Level Design"]
        P5["13. Gateway & Balancers\n14. Stateless Microservices\n15. Caching & Queue Topology"]
    end

    subgraph Step6 ["Phase 6: Deep Dives"]
        P6["16. Bottleneck Resolution\n17. Consensus & Replication\n18. Disaster Recovery"]
    end

    Step1 --> Step2 --> Step3 --> Step4 --> Step5 --> Step6
```

---

## 🧭 Master Knowledge Map

```
cs-system-design-vault/
├── 00_MASTER_INDEX.md              # Complete tracking registry & concept index
├── A_Hardware_CS_Foundations/      # CPU architecture, Memory hierarchy, Cache lines, Virtual memory, OS, Networking
├── B_DSA_Java/                     # Big-O, Two pointers, Linked lists, Trees, Heaps, Graphs, DP (1D/2D), Greedy, Tries
├── C_DBMS_Databases/               # Relational theory, PostgreSQL MVCC/WAL, Indexing, MongoDB, Redis, Cassandra, Kafka
├── D_Backend_Development/          # REST/gRPC/GraphQL, Spring Boot, Node.js/Go, Auth/JWT/OAuth2, Security, Microservices
├── E_Frontend_Development/         # DOM, JS Event loop, React 19 internals, State management, Web performance, Webpack/Vite
├── F_FullStack_Integration/        # API integration, WebSocket, Caching strategies, End-to-end testing, Monorepo setups
├── G_Android_Development/          # Android runtime (ART), Jetpack Compose, Coroutines/Flow, Clean Architecture, Dependency Injection
├── H_System_Design/                # HLD & LLD, Instagram, WhatsApp, URL Shortener, Distributed systems, 55-Phase Interview Mastery
├── I_AWS_Cloud/                    # AWS Well-Architected, IAM, VPC, EC2, ECS/EKS, Lambda, S3, DynamoDB, CloudWatch
├── J_Docker_Kubernetes/            # Container runtimes, Dockerfiles, K8s Architecture, Pods, Deployments, Services, Helm
├── K_Python_Fundamentals/          # Python data model, GIL, Asyncio, Memory management, Decorators, Metaclasses
├── L_AI_ML_DeepLearning/           # Math foundations, Classical ML, PyTorch, CNNs/RNNs, Transformers, LLMs, RAG & Vector DBs
├── M_Data_Science_Analytics/       # Data pipelines, Pandas, Feature engineering, Statistical modeling, A/B Testing
└── N_GTM_FDE/                      # Forward-deployed engineering, Production debugging, Observability, Post-mortems
```

---

## 📊 Modules & Curriculum Overview

| # | Domain Section | Files | Core Highlights |
|:---|:---|:---|:---|
| **A** | **Hardware & CS Foundations** | 6 files | Clock cycles, ALU, cache lines, virtual memory paging, MMU/TLB, JVM stack/heap, TCP/UDP sockets |
| **B** | **DSA in Java** | 19 files | Contiguous memory, two pointers, sliding window, monotonic queues, BSTs, AVL/Red-Black, DP, Dijkstra, Tries |
| **C** | **DBMS & Storage Engines** | 10 files | 1NF–BCNF normalization, SQL CTEs/window functions, PostgreSQL MVCC & WAL, B-Tree/GIN/BRIN indexing |
| **D** | **Backend Engineering** | 16 files | Idempotency, rate limiters, Spring Boot, Go concurrency, OAuth2/OIDC, circuit breakers, CQRS, event sourcing |
| **E** | **Frontend Internals** | 14 files | Browser rendering pipeline, VDOM diffing, React Fiber, concurrent rendering, memory leaks, SSR/SSG/ISR |
| **F** | **Full-Stack Integration** | 7 files | SSE vs WebSockets, schema registries, distributed tracing, resilience engineering, fullstack telemetry |
| **G** | **Modern Android Architecture** | 16 files | ART vs Dalvik, lifecycle, Jetpack Compose recomposition, Coroutines, Flow, Hilt/Koin, Clean Architecture |
| **H** | **System Design at Hyperscale** | 10 files | Load balancers, consistent hashing, distributed caching, Instagram/WhatsApp designs, 55-Phase Interview Mastery |
| **I** | **AWS Cloud Infrastructure** | 10 files | Multi-AZ VPC topology, IAM least privilege, ECS Fargate vs EKS, DynamoDB single-table design, CloudFront |
| **J** | **Docker & Kubernetes** | 9 files | Namespaces & cgroups, multi-stage Docker builds, Pod lifecycle, K8s scheduler, Service mesh, Helm charts |
| **K** | **Python Engineering** | 5 files | CPython internals, memory management, GIL, asyncio event loop, generators, descriptors |
| **L** | **AI, Machine Learning & LLMs** | 18 files | Linear algebra, backpropagation, PyTorch tensors, self-attention, Transformers, LoRA fine-tuning, RAG pipelines |
| **M** | **Data Science & Analytics** | 6 files | Exploratory data analysis, feature stores, experiment design, hypothesis testing, metrics layers |
| **N** | **Forward-Deployed & Production** | 6 files | Production incident triage, root cause analysis, SLO/SLA management, telemetry, post-mortems |

---

## 🎯 How to Use This Vault

- **For Technical Interviews (HLD/LLD)**: Start with [`H_System_Design/`](H_System_Design/) alongside [`C_DBMS_Databases/`](C_DBMS_Databases/) and [`I_AWS_Cloud/`](I_AWS_Cloud/).
- **For Coding Practice & DSA**: Jump into [`B_DSA_Java/`](B_DSA_Java/) for deep, pattern-by-pattern derivations and real hardware memory models.
- **For AI/ML Engineering**: Follow the sequential path in [`L_AI_ML_DeepLearning/`](L_AI_ML_DeepLearning/) from mathematical foundations to modern Transformer and RAG deployments.
- **Master Registry**: Explore [`00_MASTER_INDEX.md`](00_MASTER_INDEX.md) for individual file checklists, key concept indices, and progress tracking.

---

## 📜 License
MIT © [Subhash](https://github.com/Subhash6102003)
