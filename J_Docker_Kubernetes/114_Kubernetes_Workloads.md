================================================================================
  FILE 114: KUBERNETES WORKLOADS & NETWORKING
  Section: J - Docker & Kubernetes
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  Kubernetes Workloads & Networking: Deploying and Routing Applications

  While the Kubernetes architecture provides the infrastructure, Workloads are the actual applications running on that infrastructure. This module explores the various types of workload resources—from stateless Deployments and Jobs to stateful databases via StatefulSets. We will also demystify Kubernetes Networking, explaining how internal Services load-balance traffic between Pods, and how Ingress controllers route external HTTP traffic into the cluster.

  Prerequisites:
  - Understanding of Kubernetes Architecture and the Control Loop (File 113).
  - Knowledge of YAML syntax.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  Workload Controller Hierarchy                                          │
  │                                                                         │
  │  +-----------------------------------------------------+                │
  │  |                     Deployment                      |  <-- You manage this via YAML│
  │  |    (Defines desired state: image, 3 replicas)       |                │
  │  +-----------------------------------------------------+                │
  │                            | manages                                    │
  │                            v                                            │
  │  +-----------------------------------------------------+                │
  │  |                     ReplicaSet                      |  <-- Auto-created by Deployment│
  │  |    (Ensures exactly 3 Pods are always running)      |                │
  │  +-----------------------------------------------------+                │
  │               |            |            |                               │
  │        creates|     creates|     creates|                               │
  │               v            v            v                               │
  │          +-------+    +-------+    +-------+                            │
  │          | Pod 1 |    | Pod 2 |    | Pod 3 |      <-- The actual running containers│
  │          | (IP:A)|    | (IP:B)|    | (IP:C)|                            │
  │          +-------+    +-------+    +-------+                            │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  Ingress & Service Traffic Routing                                      │
  │                                                                         │
  │                               [Internet/User Browser]                   │
  │                                          | (HTTPS traffic)              │
  │                                          v                              │
  │  +---------------------------------------------------------------------------------+│
  │  |                                 Kubernetes Cluster                              |│
  │  |                                                                                 |│
  │  |  +-------------------------------------------------------------------------+    |│
  │  |  |                           Ingress Controller                            |    |│
  │  |  |  (Reads Ingress rules. E.g., NGINX resolving api.myapp.com/v1)          |    |│
  │  |  +-------------------------------------------------------------------------+    |│
  │  |                               |                  |                              |│
  │  |          If Host: api.myapp.com                  If Host: web.myapp.com         |│
  │  |          Path: /v1                               Path: /                        |│
  │  |                               |                  |                              |│
  │  |                               v                  v                              |│
  │  |                  +--------------------+     +--------------------+              |│
  │  |                  | Service (ClusterIP)|     | Service (ClusterIP)|              |│
  │  |                  | Name: api-svc      |     | Name: web-svc      |              |│
  │  |                  +--------------------+     +--------------------+              |│
  │  |                      |             |             |             |                |│
  │  |                      v             v             v             v                |│
  │  |                  +-------+     +-------+     +-------+     +-------+            |│
  │  |                  | Pod 1 |     | Pod 2 |     | Pod A |     | Pod B |            |│
  │  |                  | (API) |     | (API) |     | (Web) |     | (Web) |            |│
  │  |                  +-------+     +-------+     +-------+     +-------+            |│
  │  +---------------------------------------------------------------------------------+│
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: yaml]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Deployments and Services (YAML)                                      │
  │                                                                          │
  │  apiVersion: apps/v1                                                     │
  │  kind: Deployment                                                        │
  │  metadata:                                                               │
  │    name: my-backend                                                      │
  │  spec:                                                                   │
  │    replicas: 3                                                           │
  │    selector:                                                             │
  │      matchLabels:                                                        │
  │        app: backend          # 1. Deployment looks for Pods with this label│
  │    template:                                                             │
  │      metadata:                                                           │
  │        labels:                                                           │
  │          app: backend        # 2. Pods are created with this label       │
  │      spec:                                                               │
  │        containers:                                                       │
  │        - name: api                                                       │
  │          image: my-api:v1.0                                              │
  │          ports:                                                          │
  │          - containerPort: 8080                                           │
  └──────────────────────────────────────────────────────────────────────────┘

  [Language: yaml]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Ingress Manifest (YAML)                                              │
  │                                                                          │
  │  apiVersion: networking.k8s.io/v1                                        │
  │  kind: Ingress                                                           │
  │  metadata:                                                               │
  │    name: my-app-ingress                                                  │
  │    annotations:                                                          │
  │      nginx.ingress.kubernetes.io/rewrite-target: /                       │
  │  spec:                                                                   │
  │    rules:                                                                │
  │    - host: myapp.company.com                                             │
  │      http:                                                               │
  │        paths:                                                            │
  │        - path: /api                                                      │
  │          pathType: Prefix                                                │
  │          backend:                                                        │
  │            service:                                                      │
  │              name: backend-service                                       │
  │              port:                                                       │
  │                number: 80                                                │
  │        - path: /                                                         │
  │          pathType: Prefix                                                │
  │          backend:                                                        │
  │            service:                                                      │
  │              name: frontend-service                                      │
  │              port:                                                       │
  │                number: 80                                                │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: yaml]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │                                                                          │
  │  apiVersion: apps/v1                                                     │
  │  kind: StatefulSet                                                       │
  │  metadata:                                                               │
  │    name: postgres-statefulset                                            │
  │  spec:                                                                   │
  │    serviceName: "postgres-headless" # Required for network identity      │
  │    replicas: 3                                                           │
  │    selector:                                                             │
  │      matchLabels:                                                        │
  │        app: postgres                                                     │
  │    template:                                                             │
  │      metadata:                                                           │
  │        labels:                                                           │
  │          app: postgres                                                   │
  │      spec:                                                               │
  │        containers:                                                       │
  │        - name: postgres                                                  │
  │          image: postgres:15                                              │
  │          ports:                                                          │
  │          - containerPort: 5432                                           │
  │          env:                                                            │
  │          - name: POSTGRES_PASSWORD                                       │
  │            value: "supersecret"                                          │
  │          volumeMounts:                                                   │
  │          - name: pg-data                                                 │
  │            mountPath: /var/lib/postgresql/data                           │
  │    # This dynamically provisions a unique PV for each Pod (pod-0, pod-1, pod-2)│
  │    volumeClaimTemplates:                                                 │
  │    - metadata:                                                           │
  │        name: pg-data                                                     │
  │      spec:                                                               │
  │        accessModes: [ "ReadWriteOnce" ]                                  │
  │        storageClassName: "standard"                                      │
  │        resources:                                                        │
  │          requests:                                                       │
  │            storage: 10Gi                                                 │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  7. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

────────────────────────────────────────────────────────────────────────────────
  8. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: Riddle 1: The Disconnected Service

  Scenario: You deploy your web app and a Service. But curl http://my-service from inside the cluster times out.
  Deployment YAML label: app: web-frontend
  Service YAML selector: app: webfrontend (No hyphen).
  What's wrong?

  SOLUTION:
    The label selector in the Service must perfectly match the labels in the Deployment's Pod template. Because of the typo, the Service finds 0 matching Pods. It exists, it has an IP, but it has no endpoints to route traffic to, causing a timeout.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 2: Riddle 2: The CrashLoopBackOff

  Scenario: You create a Job to run a one-time database migration script. The script connects to the DB, runs the migration, prints "Success!", and exits with code 0. However, K8s restarts the pod over and over, and it enters CrashLoopBackOff.
  Job YAML snippet: (Wait, if it's a Job, it shouldn't restart on success).
  Wait, what if it was accidentally deployed as a Deployment?
  Scenario revised: You deployed a one-time script as a Deployment. The script prints "Success!" and exits with code 0. The Pod restarts endlessly.

  SOLUTION:
    Deployments are designed for long-running processes (like web servers). The Kubelet sees the container exit, assumes it crashed (even though it exited cleanly with code 0), and restarts it to maintain the desired state.
    Fix: Use a Job resource instead of a Deployment for tasks that are meant to complete and exit.

────────────────────────────────────────────────────────────────────────────────
  9. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  - **

================================================================================
  END OF FILE 114
================================================================================
