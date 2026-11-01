================================================================================
  FILE 113: KUBERNETES ARCHITECTURE & FUNDAMENTALS
  Section: J - Docker & Kubernetes
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  Kubernetes Architecture: The Engine of Container Orchestration

  Managing a handful of Docker containers on a single server is straightforward using Docker Compose. However, when managing thousands of containers across hundreds of servers (nodes) in production, you need an orchestration platform to handle scheduling, networking, scaling, and self-healing. Kubernetes (K8s) is the industry-standard container orchestration system. This module dissects the Kubernetes architecture, explaining the distinct roles of the Control Plane (the brain) and the Worker Nodes (the brawn), and introduces the declarative model of infrastructure using YAML and kubectl.

  Prerequisites:
  - Solid understanding of Docker and Containerization (Files 109-112).
  - Basic understanding of distributed systems.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  Kubernetes Cluster Architecture                                        │
  │                                                                         │
  │                             +-----------------------------------------------------+│
  │                             |                   CONTROL PLANE                     |│
  │                             |                                                     |│
  │   [Developer/CI]  ------->  |  +---------------+       +-----------------------+  |│
  │   (kubectl apply)           |  | kube-apiserver| <---> |        etcd           |  |│
  │                             |  +---------------+       | (Cluster State Store) |  |│
  │                             |    ^           ^         +-----------------------+  |│
  │                             |    |           |                                    |│
  │                             |    v           v                                    |│
  │                             | +---------+  +-------------------------+            |│
  │                             | | kube-   |  | kube-controller-manager |            |│
  │                             | |scheduler|  | (Reconciliation Loops)  |            |│
  │                             | +---------+  +-------------------------+            |│
  │                             +-----------------------------------------------------+│
  │                                    ^   |                           ^   |│
  │                                    |   |                           |   |│
  │        +---------------------------+   |                           |   +-----------------------+│
  │        |                               |                           |                           |│
  │        v                               v                           v                           v│
  │  +---------------------------------------+                   +---------------------------------------+│
  │  |              WORKER NODE 1            |                   |              WORKER NODE 2            |│
  │  |                                       |                   |                                       |│
  │  |  +---------+   +------------+         |                   |  +---------+   +------------+         |│
  │  |  | kubelet |   | kube-proxy |         |                   |  | kubelet |   | kube-proxy |         |│
  │  |  +---------+   +------------+         |                   |  +---------+   +------------+         |│
  │  |      |               |                |                   |      |               |                |│
  │  |      v               v                |                   |      v               v                |│
  │  |  +---------------------------+        |                   |  +---------------------------+        |│
  │  |  |     Container Runtime     |        |                   |  |     Container Runtime     |        |│
  │  |  |  +-----+         +-----+  |        |                   |  |  +-----+         +-----+  |        |│
  │  |  |  | Pod |         | Pod |  |        |                   |  |  | Pod |         | Pod |  |        |│
  │  |  |  +-----+         +-----+  |        |                   |  |  +-----+         +-----+  |        |│
  │  |  +---------------------------+        |                   |  +---------------------------+        |│
  │  +---------------------------------------+                   +---------------------------------------+│
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  API Request Flow (e.g., creating a Pod)                                │
  │                                                                         │
  │  1. User types `kubectl apply -f pod.yaml`                              │
  │  2. API Server authenticates and authorizes the request.                │
  │  3. API Server writes the initial Pod object to etcd (State = Pending). │
  │  4. Scheduler notices a Pending Pod (via API Server watch).             │
  │  5. Scheduler algorithms choose Node X. It tells API Server to bind Pod to Node X.│
  │  6. API Server updates etcd with the node binding.                      │
  │  7. Kubelet on Node X notices (via API Server watch) a Pod assigned to it.│
  │  8. Kubelet instructs Container Runtime on Node X to pull image and start containers.│
  │  9. Kubelet updates API Server that Pod is Running. API Server updates etcd.│
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: bash]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Essential `kubectl` Commands                                         │
  │                                                                          │
  │  # 1. Cluster Info                                                       │
  │  kubectl cluster-info                                                    │
  │  kubectl get nodes           # List worker/master nodes                  │
  │                                                                          │
  │  # 2. Imperative vs Declarative                                          │
  │  kubectl run my-nginx --image=nginx        # Imperative creation         │
  │  kubectl apply -f deployment.yaml          # Declarative creation (Best Practice)│
  │                                                                          │
  │  # 3. Viewing Resources                                                  │
  │  kubectl get pods            # List pods in default namespace            │
  │  kubectl get pods -A         # List pods in ALL namespaces               │
  │  kubectl get pods -o wide    # List with extra info (IP, Node)           │
  │  kubectl get all             # List all core resources in namespace      │
  │                                                                          │
  │  # 4. Inspecting and Debugging                                           │
  │  kubectl describe pod my-nginx    # Detailed lifecycle events and config │
  │  kubectl logs my-nginx            # View stdout/stderr logs of the container│
  │  kubectl logs -f my-nginx         # Stream logs                          │
  │  kubectl exec -it my-nginx -- sh  # Open an interactive shell inside the pod│
  │                                                                          │
  │  # 5. Modifying Resources                                                │
  │  kubectl delete pod my-nginx      # Delete resource imperatively         │
  │  kubectl delete -f deploy.yaml    # Delete resource declaratively        │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: yaml]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │                                                                          │
  │  apiVersion: v1                                                          │
  │  kind: Pod                                                               │
  │  metadata:                                                               │
  │    name: nginx-pod                                                       │
  │    labels:                                                               │
  │      app: frontend                                                       │
  │  spec:                                                                   │
  │    containers:                                                           │
  │    - name: nginx-container                                               │
  │      image: nginx:1.25-alpine                                            │
  │      ports:                                                              │
  │      - containerPort: 80                                                 │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

  [Language: yaml]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │                                                                          │
  │  apiVersion: apps/v1                                                     │
  │  kind: Deployment                                                        │
  │  metadata:                                                               │
  │    name: frontend-deployment                                             │
  │  spec:                                                                   │
  │    replicas: 3                                                           │
  │    selector:                                                             │
  │      matchLabels:                                                        │
  │        app: frontend                                                     │
  │    template: # This is the Pod Template                                  │
  │      metadata:                                                           │
  │        labels:                                                           │
  │          app: frontend                                                   │
  │      spec:                                                               │
  │        containers:                                                       │
  │        - name: nginx-container                                           │
  │          image: nginx:1.25-alpine                                        │
  │          ports:                                                          │
  │          - containerPort: 80                                             │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  7. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

────────────────────────────────────────────────────────────────────────────────
  8. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: Riddle 1: The Disappearing Pod

  Scenario: You have a cluster. You run kubectl run my-test-pod --image=nginx. The pod starts successfully. Five minutes later, the node that the pod was running on experiences a hard kernel panic and crashes. You check kubectl get pods an hour later. Where is my-test-pod?

  SOLUTION:
    It's gone (or stuck in Terminating/Unknown, but it will never be rescheduled).
    Explanation: A raw Pod is the smallest execution unit, but it has no controller managing it. Because you didn't create a Deployment or ReplicaSet to manage desired state, K8s assumes this was a one-off pod. When the node died, the pod died with it, and nothing in the Control Plane is configured to recreate it. *Never use raw pods in production.*

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 2: Riddle 2: The Stalled Creation

  Scenario: You apply a valid YAML file: kubectl apply -f big-app.yaml. The output says deployment.apps/big-app created. However, kubectl get pods shows 0 pods. You check the API server logs; no errors. You check kubelet logs; no errors.
  What's wrong?

  SOLUTION:
    The Scheduler is dead or broken. The API server successfully saved the desired state in etcd (hence "created"). The Controller Manager successfully created the Pod objects (State = Pending). But because the Scheduler isn't running, no Node is ever selected, so the Pods sit in Pending state forever, and the Kubelets never get the command to start them.

────────────────────────────────────────────────────────────────────────────────
  9. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  - High Availability (HA): Understanding architecture dictates how you deploy. A production K8s cluster cannot have a single Control Plane node. You deploy 3 or 5 Control Plane nodes spread across different physical availability zones (A

================================================================================
  END OF FILE 113
================================================================================
