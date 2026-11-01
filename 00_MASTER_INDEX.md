# 📚 MASTER LIBRARY INDEX — 152-File Engineering Knowledge Base
> **Last Updated**: 2026-09-29  
> **Owner**: Subham  
> **Purpose**: Central tracking registry for the entire 152-file knowledge base. Used by the AI assistant to track progress, locate content, and answer questions by referencing the correct file.

---

## 🔍 How This Library Works
1. **Every file** in the knowledge base is registered here with its path, topic, key concepts, and status.
2. When you ask a question, the AI references this index to find the **exact file** containing the answer.
3. **Progress tracking**: Mark files as `READING`, `COMPLETED`, or `REVISION NEEDED` as you study.

---

## 📂 Directory Structure
```
d:\placement\LIBRARY\
├── 00_MASTER_INDEX.md              ← YOU ARE HERE
├── A_Hardware_CS_Foundations\       ← Files 001–006
├── B_DSA_Java\                     ← Files 007–025
├── C_DBMS_Databases\               ← Files 026–035
├── D_Backend_Development\          ← Files 036–051
├── E_Frontend_Development\         ← Files 052–065
├── F_FullStack_Integration\        ← Files 066–072
├── G_Android_Development\          ← Files 073–088
├── H_System_Design\                ← Files 089–098
├── I_AWS_Cloud\                    ← Files 099–108
├── J_Docker_Kubernetes\            ← Files 109–117
├── K_Python_Fundamentals\          ← Files 118–122
├── L_AI_ML_DeepLearning\           ← Files 123–140
├── M_Data_Science_Analytics\       ← Files 141–146
└── N_GTM_FDE\                      ← Files 147–152
```

---

## 📊 Progress Dashboard

| Section | Files | Status | Completion |
|:--------|:------|:-------|:-----------|
| A. Hardware & CS Foundations | 001–006 (6 files) | 🟢 READY | 6/6 |
| B. DSA in Java | 007–025 (19 files) | 🟢 READY | 19/19 |
| C. DBMS & Databases | 026–035 (10 files) | 🟢 READY | 10/10 |
| D. Backend Development | 036–051 (16 files) | 🟢 READY | 16/16 |
| E. Frontend Development | 052–065 (14 files) | 🟢 READY | 14/14 |
| F. Full-Stack Integration | 066–072 (7 files) | 🟢 READY | 7/7 |
| G. Android Development | 073–088 (16 files) | 🟢 READY | 16/16 |
| H. System Design at Scale | 089–098 (10 files) | 🟢 READY | 10/10 |
| I. AWS Cloud Services | 099–108 (10 files) | 🟢 READY | 10/10 |
| J. Docker & Kubernetes | 109–117 (9 files) | 🟢 READY | 9/9 |
| K. Python Fundamentals | 118–122 (5 files) | 🟢 READY | 5/5 |
| L. AI/ML/DL/LLM/RAG | 123–140 (18 files) | 🟢 READY | 18/18 |
| M. Data Science & Analytics | 141–146 (6 files) | 🟢 READY | 6/6 |
| N. GTM & Forward-Deployed Eng | 147–152 (6 files) | 🟢 READY | 6/6 |
| **TOTAL** | **152 files** | 🟢 **COMPLETE** | **152/152** |

---

## 📖 Complete File Registry

### Section A: Hardware & CS Foundations
| File # | Filename | Key Concepts | Status | Your Progress |
|:-------|:---------|:-------------|:-------|:--------------|
| 001 | `001_CPU_Architecture_Instruction_Pipeline.md` | Clock cycles, ALU, registers, pipelining, branch prediction, CISC vs RISC | READY | `[ ]` |
| 002 | `002_Memory_Hierarchy_Cache_Lines.md` | L1/L2/L3, 64-byte cache lines, spatial/temporal locality, NUMA, prefetcher | READY | `[ ]` |
| 003 | `003_Virtual_Memory_Pages_PageFaults.md` | Virtual addressing, MMU, TLB, 4KB pages, huge pages, swap, mmap | READY | `[ ]` |
| 004 | `004_JVM_Architecture_Stack_Heap_GC.md` | Stack frames, Heap generations, object headers, Compressed OOPs, G1/ZGC | READY | `[ ]` |
| 005 | `005_Operating_System_Fundamentals.md` | Processes, threads, context switching, scheduling, syscalls, file descriptors | READY | `[ ]` |
| 006 | `006_Networking_Fundamentals.md` | OSI model, TCP/UDP, HTTP/1.1/2/3, TLS, DNS, sockets, WebSocket | READY | `[ ]` |

### Section B: DSA in Java
| File # | Filename | Key Concepts | Status | Your Progress |
|:-------|:---------|:-------------|:-------|:--------------|
| 007 | `007_BigO_Complexity_Analysis.md` | Time/space complexity, amortized, Big-O vs real hardware | READY | `[ ]` |
| 008 | `008_Arrays_Memory_Addressing.md` | Contiguous memory, index formula, int[] vs ArrayList | READY | `[ ]` |
| 009 | `009_Two_Pointers_Sliding_Window.md` | Patterns + problems: Two Sum II, Container, Trapping Rain Water | READY | `[ ]` |
| 010 | `010_Strings_JVM_String_Pool.md` | Immutability, String Pool, StringBuilder, substring patterns | READY | `[ ]` |
| 011 | `011_Linked_Lists.md` | Singly/Doubly, pointer chasing, Floyd's, Merge K Lists, LRU Cache | READY | `[ ]` |
| 012 | `012_Stacks_Applications.md` | Array-backed stack, call stack, Min Stack, Valid Parentheses | READY | `[ ]` |
| 013 | `013_Queues_Deques_CircularBuffers.md` | ArrayDeque, circular buffer, BFS queue, Sliding Window Max | READY | `[ ]` |
| 014 | `014_Monotonic_Stack_Queue.md` | Invariants, Daily Temperatures, Largest Rectangle, Next Greater | READY | `[ ]` |
| 015 | `015_Binary_Trees_BST.md` | Traversals, BST ops, Validate BST, LCA, Max Path Sum | READY | `[ ]` |
| 016 | `016_AVL_RedBlack_Trees.md` | Rotations, balancing, TreeMap internals, sorted structure use cases | READY | `[ ]` |
| 017 | `017_BTrees_BPlusTrees.md` | Disk-oriented design, fan-out, page sizing, leaf linked lists | READY | `[ ]` |
| 018 | `018_Heaps_PriorityQueues.md` | Binary heap array, min/max heap, Top K, Median Stream | READY | `[ ]` |
| 019 | `019_HashTables_Hashing.md` | HashMap deep dive, collisions, treeification, Design HashMap | READY | `[ ]` |
| 020 | `020_Graphs_BFS_DFS.md` | Adjacency list/matrix, BFS/DFS, Islands, Clone Graph, Word Ladder | READY | `[ ]` |
| 021 | `021_Graphs_ShortestPath_MST_TopoSort.md` | Dijkstra, Bellman-Ford, Kruskal, Prim, Topological Sort | READY | `[ ]` |
| 022 | `022_DP_Foundations_1D.md` | Memoization vs Tabulation, Climbing Stairs, Coin Change, Word Break | READY | `[ ]` |
| 023 | `023_DP_2D_Knapsack_Subsequences.md` | 0/1 Knapsack, LCS, LIS, Edit Distance, Palindrome Partitioning | READY | `[ ]` |
| 024 | `024_Greedy_Backtracking.md` | Greedy choice, Activity Selection, N-Queens, Sudoku, Subsets | READY | `[ ]` |
| 025 | `025_Tries_SegmentTrees_UnionFind.md` | Trie ops, Segment Tree, DSU, Word Search II, Accounts Merge | READY | `[ ]` |

### Section C: DBMS & Databases
| File # | Filename | Key Concepts | Status | Your Progress |
|:-------|:---------|:-------------|:-------|:--------------|
| 026 | `026_Relational_Database_Theory.md` | ER diagrams, normalization 1NF–BCNF, functional dependencies | READY | `[ ]` |
| 027 | `027_SQL_Mastery.md` | JOINs, subqueries, CTEs, window functions, GROUP BY/HAVING | READY | `[ ]` |
| 028 | `028_PostgreSQL_MVCC_WAL.md` | Process arch, shared buffers, xmin/xmax, VACUUM, WAL, checkpoints | READY | `[ ]` |
| 029 | `029_PostgreSQL_Indexing_QueryOpt.md` | B-Tree, GIN, GiST, BRIN, EXPLAIN ANALYZE, Leftmost Prefix | READY | `[ ]` |
| 030 | `030_PostgreSQL_Advanced.md` | Partitioning, replication, TOAST, JSONB, PgBouncer | READY | `[ ]` |
| 031 | `031_MongoDB.md` | Document model, aggregation, indexing, replica sets, sharding | READY | `[ ]` |
| 032 | `032_Redis.md` | Data structures, persistence, pub/sub, Lua, cluster, cache patterns | READY | `[ ]` |
| 033 | `033_Database_Comparison.md` | PostgreSQL vs MySQL vs MongoDB vs Redis feature matrix | READY | `[ ]` |
| 034 | `034_Database_Scaling.md` | Replicas, sharding, consistent hashing, connection pooling | READY | `[ ]` |
| 035 | `035_Transactions_Concurrency.md` | Isolation levels, locking, deadlocks, 2PC, saga pattern | READY | `[ ]` |

### Section D: Backend Development
| File # | Filename | Key Concepts | Status | Your Progress |
|:-------|:---------|:-------------|:-------|:--------------|
| 036 | `036_NodeJS_Fundamentals.md` | V8, event loop, Libuv, streams, buffers | READY | `[ ]` |
| 037 | `037_ExpressJS.md` | Routing, middleware, error handling, CORS | READY | `[ ]` |
| 038 | `038_NodeJS_PostgreSQL.md` | pg-pool, parameterized queries, transactions, migrations | READY | `[ ]` |
| 039 | `039_NodeJS_Auth_Security.md` | JWT, bcrypt, OAuth2, rate limiting, helmet | READY | `[ ]` |
| 040 | `040_NodeJS_Advanced.md` | Clustering, worker threads, WebSocket, PM2, file uploads | READY | `[ ]` |
| 041 | `041_Python_Backend_Fundamentals.md` | Python syntax for backend, type hints, venv, project structure | READY | `[ ]` |
| 042 | `042_Python_FastAPI.md` | Path/query params, Pydantic, async, dependency injection, OpenAPI | READY | `[ ]` |
| 043 | `043_Python_SQLAlchemy.md` | Engine, sessions, models, Alembic migrations, async SQLAlchemy | READY | `[ ]` |
| 044 | `044_Python_Asyncio_GIL.md` | Event loop, async/await, GIL, Uvicorn ASGI | READY | `[ ]` |
| 045 | `045_Java_SpringBoot_Fundamentals.md` | IoC, DI, auto-config, annotations, application.yml | READY | `[ ]` |
| 046 | `046_Spring_Data_JPA_Hibernate.md` | Entity mapping, JPQL, L1/L2 cache, N+1 problem, Flyway | READY | `[ ]` |
| 047 | `047_Java_VirtualThreads_Reactive.md` | Project Loom, structured concurrency, WebFlux | READY | `[ ]` |
| 048 | `048_API_Design_Patterns.md` | REST, GraphQL, gRPC, WebSocket, SSE, versioning | READY | `[ ]` |
| 049 | `049_Apache_Kafka.md` | Commit log, partitions, consumer groups, zero-copy, Kafka Streams | READY | `[ ]` |
| 050 | `050_Backend_Testing.md` | JUnit, pytest, Jest, mocking, integration tests, load testing | READY | `[ ]` |
| 051 | `051_Microservices_Architecture.md` | Service discovery, API gateway, circuit breaker, saga, event sourcing | READY | `[ ]` |

### Section E: Frontend Development
| File # | Filename | Key Concepts | Status | Your Progress |
|:-------|:---------|:-------------|:-------|:--------------|
| 052 | `052_HTML5_Essentials.md` | Semantic elements, forms, accessibility, SEO, Web APIs | READY | `[ ]` |
| 053 | `053_CSS3_Mastery.md` | Flexbox, Grid, animations, responsive design, variables | READY | `[ ]` |
| 054 | `054_JavaScript_ES6Plus.md` | let/const, arrow, destructuring, spread/rest, modules, Map/Set | READY | `[ ]` |
| 055 | `055_JavaScript_DeepDive.md` | Closures, prototypes, this, event loop, event delegation | READY | `[ ]` |
| 056 | `056_JavaScript_Async.md` | Promises, async/await, Promise.all, Fetch API, AbortController | READY | `[ ]` |
| 057 | `057_TypeScript.md` | Types, interfaces, generics, utility types, discriminated unions | READY | `[ ]` |
| 058 | `058_React_Fundamentals.md` | JSX, components, props, state, conditional rendering, lists/keys | READY | `[ ]` |
| 059 | `059_React_Hooks.md` | useState, useEffect, useContext, useReducer, useMemo, custom hooks | READY | `[ ]` |
| 060 | `060_React_StateManagement.md` | Context API, Redux Toolkit, Zustand, global vs local state | READY | `[ ]` |
| 061 | `061_React_Advanced.md` | React Router, forms, performance, code splitting, error boundaries | READY | `[ ]` |
| 062 | `062_NextJS.md` | App Router, Server/Client Components, SSR/SSG/ISR, API routes | READY | `[ ]` |
| 063 | `063_TailwindCSS_UILibraries.md` | Utility-first CSS, shadcn/ui, Radix, dark mode, design systems | READY | `[ ]` |
| 064 | `064_Frontend_Performance.md` | Core Web Vitals, bundle optimization, image optimization, PWA | READY | `[ ]` |
| 065 | `065_Frontend_Testing.md` | Jest, React Testing Library, Cypress, Playwright, a11y testing | READY | `[ ]` |

### Section F: Full-Stack Integration
| File # | Filename | Key Concepts | Status | Your Progress |
|:-------|:---------|:-------------|:-------|:--------------|
| 066 | `066_FullStack_Architecture.md` | Monolith vs microservices, MVC, 3-tier architecture | READY | `[ ]` |
| 067 | `067_FullStack_Project_Auth.md` | React + Node + PostgreSQL JWT auth flow | READY | `[ ]` |
| 068 | `068_FullStack_Project_CRUD.md` | CRUD, file upload, pagination, WebSocket real-time | READY | `[ ]` |
| 069 | `069_FullStack_Deployment.md` | Env vars, CORS, Nginx, PM2, SSL, domains | READY | `[ ]` |
| 070 | `070_Git_VersionControl.md` | Git internals, branching strategies, rebasing, PR workflows | READY | `[ ]` |
| 071 | `071_FullStack_Security.md` | OWASP Top 10, XSS, CSRF, SQL injection, CSP, rate limiting | READY | `[ ]` |
| 072 | `072_Web_Performance_Monitoring.md` | Lighthouse, APM tools, logging, Sentry, performance budgets | READY | `[ ]` |
| 072B | `072B_Web_Architecture_URL_HTTP_HTTPS_Redis_Nginx.md` | URL anatomy, HTTP/1.1 vs HTTP/2/3, TLS 1.3 handshake, Nginx reverse proxy, Redis cache-aside | READY | `[ ]` |

### Section G: Android Development
| File # | Filename | Key Concepts | Status | Your Progress |
|:-------|:---------|:-------------|:-------|:--------------|
| 073 | `073_Kotlin_Fundamentals.md` | Null safety, extensions, data classes, scope functions | READY | `[ ]` |
| 074 | `074_Kotlin_Advanced.md` | Coroutines, Flow, StateFlow, Channel, structured concurrency | READY | `[ ]` |
| 075 | `075_Android_Internals_Runtime.md` | ART, AOT/JIT, Zygote, Binder IPC, AIDL | READY | `[ ]` |
| 076 | `076_Activity_Fragment_Lifecycle.md` | States, config changes, ViewModel survival, process death | READY | `[ ]` |
| 077 | `077_JetpackCompose_Fundamentals.md` | Composable, state, remember, LaunchedEffect, recomposition | READY | `[ ]` |
| 078 | `078_JetpackCompose_Advanced.md` | Navigation, Material3, animations, custom layouts, Canvas | READY | `[ ]` |
| 079 | `079_Android_MVVM_CleanArch.md` | ViewModel, Repository, UseCase, MVI comparison | READY | `[ ]` |
| 080 | `080_Room_Database.md` | Entity, Dao, migrations, TypeConverters, Flow queries, Paging3 | READY | `[ ]` |
| 081 | `081_Retrofit_OkHttp.md` | Annotations, converters, interceptors, connection pooling, cert pinning | READY | `[ ]` |
| 082 | `082_Hilt_DependencyInjection.md` | @Inject, @Module, @Provides, scopes, Hilt testing | READY | `[ ]` |
| 083 | `083_Background_Processing.md` | WorkManager, Foreground Services, Doze, App Standby | READY | `[ ]` |
| 084 | `084_Android_Memory_Performance.md` | Leaks, LeakCanary, Profiler, 16ms frame budget, StrictMode | READY | `[ ]` |
| 085 | `085_Android_OfflineFirst_Sync.md` | Offline-first, Room as SSOT, conflict resolution, NetworkBoundResource | READY | `[ ]` |
| 086 | `086_Android_Notifications_Permissions.md` | NotificationChannel, PendingIntent, runtime permissions, CameraX | READY | `[ ]` |
| 087 | `087_Android_Testing.md` | JUnit, MockK, Turbine, Compose UI testing, Espresso | READY | `[ ]` |
| 088 | `088_Android_Publishing.md` | ProGuard/R8, signing, Play Store, CI/CD, app bundle | READY | `[ ]` |

### Section H: System Design at Scale
| File # | Filename | Key Concepts | Status | Your Progress |
|:-------|:---------|:-------------|:-------|:--------------|
| 089 | `089_SystemDesign_Fundamentals.md` | Scalability, availability, CAP theorem, consistency models | READY | `[ ]` |
| 090 | `090_LoadBalancing_CDN_APIGateway.md` | L4/L7, algorithms, CDN edge, API gateway patterns | READY | `[ ]` |
| 091 | `091_Caching_AtScale.md` | Cache-Aside, Write-Through, stampede, penetration, avalanche | READY | `[ ]` |
| 092 | `092_Design_Instagram.md` | Feed, stories, celebrity fan-out, like counter architecture | READY | `[ ]` |
| 093 | `093_Design_WhatsApp.md` | WebSocket, message queue, E2E encryption, presence | READY | `[ ]` |
| 094 | `094_Design_URLShortener_RateLimiter.md` | Base62, token bucket, notification fan-out | READY | `[ ]` |
| 095 | `095_LLD_DesignPatterns.md` | SOLID, Factory, Observer, Strategy, Singleton, Decorator | READY | `[ ]` |
| 096 | `096_Distributed_Systems.md` | Consensus, leader election, vector clocks, CRDTs, Redlock | READY | `[ ]` |
| 097 | `097_Data_Pipeline_Architecture.md` | ETL, batch vs stream, Lambda arch, data lakes, CQRS | READY | `[ ]` |
| 098 | `098_Observability_Monitoring.md` | Prometheus, ELK, Jaeger, SLI/SLO, golden signals, chaos eng | READY | `[ ]` |
| 098B | `098B_System_Design_Complete_55_Phase_Interview_Mastery.md` | 55-Phase Roadmap, Networking, Microservices (Java/Node/Python), 20 System Designs | READY | `[ ]` |

### Section I: AWS Cloud Services
| File # | Filename | Key Concepts | Status | Your Progress |
|:-------|:---------|:-------------|:-------|:--------------|
| 099 | `099_Cloud_AWS_Fundamentals.md` | IaaS/PaaS/SaaS, Regions/AZs, shared responsibility | READY | `[ ]` |
| 100 | `100_AWS_Compute.md` | EC2, Lambda, ECS, Fargate, auto-scaling, spot instances | READY | `[ ]` |
| 101 | `101_AWS_Storage.md` | S3 tiers, lifecycle policies, EBS, EFS | READY | `[ ]` |
| 102 | `102_AWS_Databases.md` | RDS, Aurora, DynamoDB, ElastiCache | READY | `[ ]` |
| 103 | `103_AWS_Networking.md` | VPC, subnets, NAT, Route53, CloudFront | READY | `[ ]` |
| 104 | `104_AWS_Security.md` | IAM, KMS, Secrets Manager, WAF, Shield | READY | `[ ]` |
| 105 | `105_AWS_Messaging.md` | SQS, SNS, EventBridge, Kinesis | READY | `[ ]` |
| 106 | `106_AWS_Architecture_Patterns.md` | 3-tier, serverless, event-driven diagrams | READY | `[ ]` |
| 107 | `107_AWS_Cost_WellArchitected.md` | Cost Explorer, Reserved Instances, 6 pillars | READY | `[ ]` |
| 108 | `108_AWS_Deployment_IaC.md` | CloudFormation, CDK, SAM, Terraform | READY | `[ ]` |

### Section J: Docker & Kubernetes
| File # | Filename | Key Concepts | Status | Your Progress |
|:-------|:---------|:-------------|:-------|:--------------|
| 109 | `109_Docker_Fundamentals.md` | Containers vs VMs, images, layers, Dockerfile | READY | `[ ]` |
| 110 | `110_Docker_Compose.md` | docker-compose.yml, multi-container, networking, volumes | READY | `[ ]` |
| 111 | `111_Docker_Networking_Volumes.md` | Bridge/host/overlay, port mapping, data persistence | READY | `[ ]` |
| 112 | `112_Docker_Production.md` | Multi-stage builds, scanning, caching, resource limits | READY | `[ ]` |
| 113 | `113_Kubernetes_Architecture.md` | Control plane, etcd, scheduler, kubelet, kube-proxy | READY | `[ ]` |
| 114 | `114_Kubernetes_Workloads.md` | Pods, Deployments, Services, Ingress, StatefulSets | READY | `[ ]` |
| 115 | `115_Kubernetes_Config_Storage.md` | ConfigMaps, Secrets, PVs, PVCs, RBAC, namespaces | READY | `[ ]` |
| 116 | `116_Kubernetes_Scaling_Deploy.md` | HPA, VPA, rolling updates, blue-green, canary, Helm | READY | `[ ]` |
| 117 | `117_CICD_Pipeline.md` | GitHub Actions, Docker registry, ArgoCD, GitOps | READY | `[ ]` |

### Section K: Python Fundamentals
| File # | Filename | Key Concepts | Status | Your Progress |
|:-------|:---------|:-------------|:-------|:--------------|
| 118 | `118_Python_Core.md` | Syntax, types, control flow, functions, file I/O, exceptions | READY | `[ ]` |
| 119 | `119_Python_OOP.md` | Classes, inheritance, dunder methods, decorators, property | READY | `[ ]` |
| 120 | `120_Python_Advanced.md` | Generators, context managers, comprehensions, type hints | READY | `[ ]` |
| 121 | `121_Python_DataStructures_DSA.md` | Lists, dicts, heapq, bisect, collections, DSA in Python | READY | `[ ]` |
| 122 | `122_Python_Concurrency.md` | Threading, multiprocessing, asyncio, GIL deep dive | READY | `[ ]` |

### Section L: AI/ML/Deep Learning/LLM/RAG
| File # | Filename | Key Concepts | Status | Your Progress |
|:-------|:---------|:-------------|:-------|:--------------|
| 123 | `123_Math_For_AI.md` | Linear algebra, calculus, probability, statistics | READY | `[ ]` |
| 124 | `124_NumPy.md` | ndarray, broadcasting, vectorized ops, linear algebra | READY | `[ ]` |
| 125 | `125_Pandas.md` | DataFrame, indexing, groupby, merge, missing data | READY | `[ ]` |
| 126 | `126_DataVisualization.md` | Matplotlib, Seaborn, plotting, storytelling | READY | `[ ]` |
| 127 | `127_ML_Foundations.md` | Supervised/unsupervised, workflow, bias-variance | READY | `[ ]` |
| 128 | `128_Supervised_Regression.md` | Linear/Polynomial regression, gradient descent, regularization | READY | `[ ]` |
| 129 | `129_Supervised_Classification.md` | Logistic Regression, Decision Trees, RF, SVM, KNN | READY | `[ ]` |
| 130 | `130_Unsupervised_Learning.md` | K-Means, DBSCAN, PCA, t-SNE, anomaly detection | READY | `[ ]` |
| 131 | `131_Model_Evaluation_Tuning.md` | Cross-validation, GridSearch, ROC/AUC, feature importance | READY | `[ ]` |
| 132 | `132_ANN_DeepLearning.md` | Perceptron, MLP, activations, backpropagation, PyTorch | READY | `[ ]` |
| 133 | `133_CNN.md` | Convolution, filters, pooling, ResNet, transfer learning | READY | `[ ]` |
| 134 | `134_RNN_LSTM_GRU.md` | Sequence models, vanishing gradient, LSTM gates, text gen | READY | `[ ]` |
| 135 | `135_NLP_Foundations.md` | Tokenization, embeddings, Word2Vec, TF-IDF, sentiment | READY | `[ ]` |
| 136 | `136_Transformer_Architecture.md` | Self-attention, multi-head, positional encoding, from scratch | READY | `[ ]` |
| 137 | `137_LLM.md` | GPT/LLaMA, pre-training, fine-tuning, LoRA, quantization | READY | `[ ]` |
| 138 | `138_RAG.md` | Vector DBs, FAISS, ChromaDB, chunking, retrieval pipeline | READY | `[ ]` |
| 139 | `139_Building_AI_Apps.md` | LangChain, LlamaIndex, FastAPI serving, prompt engineering | READY | `[ ]` |
| 140 | `140_AI_Deployment_MLOps.md` | ONNX, Docker ML, SageMaker, MLflow, model monitoring | READY | `[ ]` |

### Section M: Data Science & Analytics
| File # | Filename | Key Concepts | Status | Your Progress |
|:-------|:---------|:-------------|:-------|:--------------|
| 141 | `141_DataScience_Workflow.md` | EDA, feature engineering, data cleaning, imbalanced data | READY | `[ ]` |
| 142 | `142_Statistical_Analysis_ABTesting.md` | Hypothesis testing, p-values, A/B tests, Bayesian | READY | `[ ]` |
| 143 | `143_Data_Pipelines_Engineering.md` | ETL, Airflow, Spark, data warehousing, data lakes | READY | `[ ]` |
| 144 | `144_SQL_Analytics_BI.md` | Window functions, dashboards, KPI frameworks | READY | `[ ]` |
| 145 | `145_Data_Storytelling.md` | Chart selection, narrative structure, stakeholder comms | READY | `[ ]` |
| 146 | `146_DataScience_Projects.md` | Churn prediction, recommendation engine, forecasting | READY | `[ ]` |

### Section N: GTM & Forward-Deployed Engineer
| File # | Filename | Key Concepts | Status | Your Progress |
|:-------|:---------|:-------------|:-------|:--------------|
| 147 | `147_GTM_Engineer_Role.md` | Role definition, engineering + sales + product bridge | READY | `[ ]` |
| 148 | `148_GTM_Technical_Skills.md` | Demos, API integrations, CRM tools, automations | READY | `[ ]` |
| 149 | `149_GTM_Product_Business.md` | TAM/SAM/SOM, pricing, onboarding, documentation | READY | `[ ]` |
| 150 | `150_FDE_Role.md` | Forward-Deployed Engineer definition, Palantir-style | READY | `[ ]` |
| 151 | `151_FDE_Technical_Execution.md` | Custom integrations, data pipelines, internal tools, glue code | READY | `[ ]` |
| 152 | `152_FDE_ClientFacing_Engineering.md` | Technical presentations, translating business to code, trust | READY | `[ ]` |

---

## 🔎 Quick Lookup: "I Have a Question About..."

| If you ask about... | Go to File(s) |
|:--------------------|:--------------|
| Cache lines, CPU cache, L1/L2/L3 | 001, 002 |
| Why arrays are faster than linked lists | 002, 008, 011 |
| JVM memory, garbage collection, object headers | 004 |
| Any DSA algorithm + Java code | 007–025 (by topic) |
| PostgreSQL internals, MVCC, WAL | 028, 029, 030 |
| Why PostgreSQL is better than others | 033 |
| Database scaling, sharding | 034, 035 |
| Node.js event loop, Express.js | 036, 037 |
| Python FastAPI, asyncio | 042, 044 |
| Spring Boot, Hibernate | 045, 046 |
| Kafka message queues | 049 |
| HTML/CSS/JavaScript basics | 052–056 |
| React.js, hooks, state management | 058–061 |
| Next.js SSR/SSG | 062 |
| Full-stack auth, CRUD, deployment | 067–069 |
| Git branching, rebasing | 070 |
| Security (XSS, CSRF, injection) | 071 |
| Kotlin, Coroutines, Flow | 073, 074 |
| Jetpack Compose | 077, 078 |
| Room DB, Retrofit | 080, 081 |
| Android memory leaks, performance | 084 |
| System design (Instagram, WhatsApp) | 092, 093 |
| Design patterns (SOLID, Factory, etc.) | 095 |
| AWS services (EC2, S3, Lambda, etc.) | 099–108 |
| Docker containers, Dockerfile | 109–112 |
| Kubernetes pods, deployments | 113–116 |
| CI/CD pipelines | 117 |
| Python basics (for AI/ML prep) | 118–122 |
| Machine learning algorithms | 127–131 |
| Neural networks, ANN, CNN, RNN | 132–134 |
| Transformers, LLMs, GPT | 136, 137 |
| RAG, vector databases | 138 |
| LangChain, building AI apps | 139 |
| Data science, analytics, A/B testing | 141–146 |
| GTM engineer role & skills | 147–149 |
| Forward-deployed engineer role | 150–152 |
