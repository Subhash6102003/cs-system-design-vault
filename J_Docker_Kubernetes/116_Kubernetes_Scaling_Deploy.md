================================================================================
  FILE 116: KUBERNETES SCALING, DEPLOYMENTS & PACKAGE MANAGEMENT
  Section: J - Docker & Kubernetes
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  Kubernetes Scaling & Deployment Strategies: Automating Growth and Rollouts

  A major advantage of Kubernetes is its ability to automatically react to traffic spikes and execute zero-downtime updates. This module explores how K8s scales workloads horizontally (HPA) and vertically (VPA), and how the cluster itself scales (Cluster Autoscaler). We will also examine advanced deployment strategies—Rolling Updates, Blue-Green, and Canary deployments. Finally, managing raw YAML files becomes unmaintainable at scale, so we introduce Helm (the K8s package manager) and Kustomize (template-free configuration overlays).

  Prerequisites:
  - Understanding of Deployments and Services (File 114).
  - Understanding of Resource Requests and Limits (File 115).

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  Rolling Update Sequence                                                │
  │                                                                         │
  │  Desired State: Update Deployment from v1 to v2                         │
  │                                                                         │
  │  Time 0:   [Pod v1] [Pod v1] [Pod v1]    (100% Capacity)                │
  │  Time 1:   [Pod v1] [Pod v1] [Pod v1] [Pod v2 (Starting)]               │
  │               ^ maxSurge=1 allows creating 1 extra pod                  │
  │  Time 2:   [Pod v1] [Pod v1] [Pod v2 (Ready!)]                          │
  │               ^ maxUnavailable=0 means we terminate an old pod ONLY after new is ready│
  │  Time 3:   [Pod v1] [Pod v1] [Pod v2] [Pod v2 (Starting)]               │
  │  Time 4:   [Pod v2] [Pod v2] [Pod v2]    (Update Complete)              │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  Canary Deployment Traffic Split (Using Ingress/Service mesh)           │
  │                                                                         │
  │                         [User Traffic]                                  │
  │                               |                                         │
  │                               v                                         │
  │                      +-------------------+                              │
  │                      |      Ingress      |                              │
  │                      | (Traffic Splitter)|                              │
  │                      +-------------------+                              │
  │                         |              |                                │
  │                   95%   |              |  5%                            │
  │                         v              v                                │
  │                 +-----------+      +-----------+                        │
  │                 |  Service  |      |  Service  |                        │
  │                 | (Prod v1) |      | (Canary v2|                        │
  │                 +-----------+      +-----------+                        │
  │                       |                  |                              │
  │                 [Pod v1 (x10)]      [Pod v2 (x1)]                       │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: bash]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Horizontal Pod Autoscaler (HPA)                                      │
  │                                                                          │
  │  # Auto-scale the 'my-app' deployment between 2 and 10 pods,             │
  │  # attempting to keep average CPU utilization at 70%                     │
  │  kubectl autoscale deployment my-app --cpu-percent=70 --min=2 --max=10   │
  └──────────────────────────────────────────────────────────────────────────┘

  [Language: text]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Kustomize Overlays                                                   │
  │                                                                          │
  │  ├── base/                                                               │
  │  │   ├── kustomization.yaml                                              │
  │  │   └── deployment.yaml                                                 │
  │  └── overlays/                                                           │
  │      ├── dev/                                                            │
  │      │   ├── kustomization.yaml                                          │
  │      │   └── replica-patch.yaml                                          │
  │      └── prod/                                                           │
  │          ├── kustomization.yaml                                          │
  │          └── replica-patch.yaml                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: text]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │                                                                          │
  │  my-chart/                                                               │
  │    Chart.yaml          # Metadata (name, version)                        │
  │    values.yaml         # Default configuration values                    │
  │    templates/          # Go templates                                    │
  │      deployment.yaml                                                     │
  │      service.yaml                                                        │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

  [Language: yaml]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │                                                                          │
  │  replicaCount: 3                                                         │
  │  image:                                                                  │
  │    repository: nginx                                                     │
  │    tag: "1.21"                                                           │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

  [Language: yaml]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │                                                                          │
  │  apiVersion: apps/v1                                                     │
  │  kind: Deployment                                                        │
  │  metadata:                                                               │
  │    name: {{ .Release.Name }}-deployment                                  │
  │  spec:                                                                   │
  │    replicas: {{ .Values.replicaCount }}                                  │
  │    selector:                                                             │
  │      matchLabels:                                                        │
  │        app: {{ .Chart.Name }}                                            │
  │    template:                                                             │
  │      metadata:                                                           │
  │        labels:                                                           │
  │          app: {{ .Chart.Name }}                                          │
  │      spec:                                                               │
  │        containers:                                                       │
  │        - name: app                                                       │
  │          image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}" │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

  [Language: bash]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │                                                                          │
  │  # Install the chart, name the release 'my-prod-app', override replicas  │
  │  helm install my-prod-app ./my-chart --set replicaCount=5                │
  │                                                                          │
  │  # Upgrade the release (e.g., deploying a new image tag)                 │
  │  helm upgrade my-prod-app ./my-chart --set image.tag="1.22"              │
  │                                                                          │
  │  # Rollback to the previous version instantly                            │
  │  helm rollback my-prod-app 1                                             │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  7. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

────────────────────────────────────────────────────────────────────────────────
  8. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: Riddle 1: The Infinite Scaling Loop

  Scenario: You set up HPA to scale based on CPU at 50%. The Deployment scales up to the maximum 10 pods, but CPU utilization is still reading 100%, even with 10 pods. The pods are doing basically nothing.
  What's wrong?

  SOLUTION:
    Your Pods likely have a CPU request set way too low (e.g., requests: cpu: 10m). Even idle background processes in the container might use 20m CPU. 20m / 10m = 200% utilization. The HPA sees utilization constantly above 50% and scales to max, but it can never lower the utilization because the baseline request is unrealistically small.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 2: Riddle 2: The Blocked Rollout

  Scenario: You update a Deployment image.
  `yaml
  spec:
  replicas: 4
  strategy:
  rollingUpdate:
  maxUnavailable: 0
  maxSurge: 1
  `
  The new Pod starts, but it is failing its Readiness Probe. You check the rollout status, and it is completely paused. The old pods are not being deleted.
  What's wrong? (Wait, is this actually doing exactly what it's supposed to?)

  SOLUTION:
    This is a trick question. Nothing is wrong. This is K8s protecting you. Because maxUnavailable: 0, K8s refuses to terminate any of the 4 old pods until the 1 new pod (maxSurge: 1) becomes "Ready". Since the new pod is failing its probe, the rollout halts indefinitely, preventing an outage.

────────────────────────────────────────────────────────────────────────────────
  9. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  - Sleep Soundly (Autoscaling): E-commerce sites experience massive spikes during Black Friday. Without HPA and Cluster Autoscaler, Ops teams must manually provision servers at 3 AM. With K8s, the cluster smoothly expands at 3 AM and shrinks at 5 AM, saving cloud costs.
  - Risk Mitigation (Deployments): Rolling updates and Canary deployments turn software releases from high-stress "Maintenance Windows" into boring, routine operations that can happen in the middle of the day without users noticing.
  - Standardization (Helm): Helm allows you to standardize deployments across the organization. The Ops team builds a "Standard Microservice" Helm chart. Dev teams just provide a simple values.yaml with their image name, ensuring all microservices are deployed securely and consistently.

================================================================================
  END OF FILE 116
================================================================================
