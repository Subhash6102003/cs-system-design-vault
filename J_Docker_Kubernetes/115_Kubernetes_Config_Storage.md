================================================================================
  FILE 115: KUBERNETES CONFIGURATION, STORAGE, & SECURITY
  Section: J - Docker & Kubernetes
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  Kubernetes Configuration & Storage: Decoupling Code from State and Securing the Cluster

  Twelve-Factor App methodology states that configuration should be strictly separated from code. In Kubernetes, this is achieved using ConfigMaps and Secrets. Furthermore, containers are inherently stateless, meaning data is lost when a Pod dies. To run stateful applications, K8s provides an elegant, abstract storage model using Persistent Volumes (PVs) and Claims (PVCs). Finally, this module covers essential cluster security and governance via Namespaces, Resource Quotas, and Role-Based Access Control (RBAC).

  Prerequisites:
  - Understanding of Pods and Deployments (File 114).
  - Basic understanding of storage arrays and user permissions.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  PV, PVC, and StorageClass Relationship                                 │
  │                                                                         │
  │    User / Developer                      Cluster Administrator / Cloud Provider│
  │    ----------------                      --------------------------------------│
  │                                                                         │
  │  1. Create PVC YAML                      4. K8s checks StorageClass     │
  │  +------------------+                    +-----------------------+      │
  │  | PVC: "my-claim"  |                    | StorageClass: "aws-gp2|      │
  │  | Size: 10Gi       | =======(requests)==> Provisioner: ebs      |      │
  │  | Class: aws-gp2   |                    +-----------------------+      │
  │  +------------------+                                | 5. Dynamically provisions│
  │           |                                          v                  │
  │           | 3. Pod mounts PVC            +-----------------------+      │
  │           v                              | PV: "pvc-xyz123"      | <-- Actual Cloud Disk│
  │  +------------------+                    | Size: 10Gi            |     (e.g., AWS EBS vol)│
  │  |       Pod        |                    | Class: aws-gp2        |      │
  │  +------------------+                    +-----------------------+      │
  │                                                      ^                  │
  │                                                      | 2. Automatic Binding│
  │                                              (PVC binds to PV)          │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: bash]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // ConfigMaps and Secrets                                               │
  │                                                                          │
  │  # The literal values will be automatically base64 encoded by kubectl    │
  │  kubectl create secret generic db-passwords \                            │
  │    --from-literal=username=admin \                                       │
  │    --from-literal=password=supersecret                                   │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: yaml]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │                                                                          │
  │  apiVersion: v1                                                          │
  │  kind: PersistentVolumeClaim                                             │
  │  metadata:                                                               │
  │    name: postgres-data-claim                                             │
  │  spec:                                                                   │
  │    accessModes:                                                          │
  │      - ReadWriteOnce                                                     │
  │    storageClassName: standard # Must match an existing StorageClass in the cluster│
  │    resources:                                                            │
  │      requests:                                                           │
  │        storage: 50Gi                                                     │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

  [Language: yaml]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │                                                                          │
  │  apiVersion: apps/v1                                                     │
  │  kind: Deployment                                                        │
  │  metadata:                                                               │
  │    name: postgres                                                        │
  │  spec:                                                                   │
  │    replicas: 1 # RWO storage generally limits you to 1 replica           │
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
  │          volumeMounts:                                                   │
  │          - mountPath: "/var/lib/postgresql/data"                         │
  │            name: storage-volume                                          │
  │        volumes:                                                          │
  │        - name: storage-volume                                            │
  │          persistentVolumeClaim:                                          │
  │            claimName: postgres-data-claim # References the PVC above     │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

  [Language: yaml]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │                                                                          │
  │  # 1. Create the ServiceAccount                                          │
  │  apiVersion: v1                                                          │
  │  kind: ServiceAccount                                                    │
  │  metadata:                                                               │
  │    name: cicd-deployer                                                   │
  │    namespace: frontend                                                   │
  │  ---                                                                     │
  │  # 2. Create the Role (Permissions)                                      │
  │  apiVersion: rbac.authorization.k8s.io/v1                                │
  │  kind: Role                                                              │
  │  metadata:                                                               │
  │    namespace: frontend                                                   │
  │    name: deployer-role                                                   │
  │  rules:                                                                  │
  │  - apiGroups: ["apps", ""]                                               │
  │    resources: ["deployments", "pods", "services"]                        │
  │    verbs: ["get", "list", "watch", "create", "update", "patch", "delete"]│
  │  ---                                                                     │
  │  # 3. Bind the Role to the ServiceAccount                                │
  │  apiVersion: rbac.authorization.k8s.io/v1                                │
  │  kind: RoleBinding                                                       │
  │  metadata:                                                               │
  │    name: cicd-deployer-binding                                           │
  │    namespace: frontend                                                   │
  │  subjects:                                                               │
  │  - kind: ServiceAccount                                                  │
  │    name: cicd-deployer                                                   │
  │    namespace: frontend                                                   │
  │  roleRef:                                                                │
  │    kind: Role                                                            │
  │    name: deployer-role                                                   │
  │    apiGroup: rbac.authorization.k8s.io                                   │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  7. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

────────────────────────────────────────────────────────────────────────────────
  8. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: Riddle 1: The OOMKilled Mystery

  Scenario: A Java application Pod keeps crashing with OOMKilled.
  Pod YAML:
  `yaml
  resources:
  requests:
  memory: "512Mi"
  limits:
  memory: "1Gi"
  `
  The JVM is configured with -Xmx1024m (Max Heap 1GB).
  What's wrong?

  SOLUTION:
    The JVM max heap is set to 1GB. However, the JVM requires *extra* memory outside the heap for thread stacks, garbage collection, and metaspace. If the heap uses 1GB, the total JVM process will exceed 1GB, hit the K8s limit (1Gi), and be OOMKilled by the kernel.
    Fix: Set the K8s memory limit higher (e.g., 1.5Gi) or lower the JVM heap (-Xmx768m).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 2: Riddle 2: The Stale Config

  Scenario: You have a ConfigMap mounted as a volume in a Pod. The ConfigMap contains an application.properties file. You update the ConfigMap using kubectl edit configmap. You wait 10 minutes, but the application isn't picking up the changes.
  What's wrong?

  SOLUTION:
    While Kubernetes *does* automatically update ConfigMap volumes in running Pods (it can take up to a minute), the *application* inside the container (like a Spring Boot app or Node.js server) usually only reads its configuration files on startup. The app doesn't know the file changed.
    Fix: You must restart the Pod to force the app to reload the config, or implement hot-reloading logic inside the application itself. (Tools like Reloader can automate K8s deployments when ConfigMaps change).

────────────────────────────────────────────────────────────────────────────────
  9. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  - Security & Blast Radius: Namespaces and RBAC are the foundation of multi-tenancy. You can have the Frontend team and Backend team share a K8s cluster safely. If a frontend developer runs kubectl delete pods --all, RBAC ensures they only delete frontend pods, preventing a cluster-wide catastrophe.
  - Cost Allocation: Resource Requests/Limits allow administrators to prevent a single application from hogging the entire cluster. By combining Limits with ResourceQuotas on Namespaces, you can restrict the Dev namespace to a maximum of 10 CPUs, controlling cloud costs.
  - Stateful Agility: Dynamic provisioning allows developers to request storage instantly via PVCs without waiting for IT/Ops to manually provision LUNs or NAS shares. This accelerates deployment pipelines.

================================================================================
  END OF FILE 115
================================================================================
