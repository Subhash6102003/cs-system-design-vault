================================================================================
  FILE 117: CI/CD PIPELINES & GITOPS
  Section: J - Docker & Kubernetes
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  CI/CD Pipelines & GitOps: Automating the Path to Production

  Containerizing an application and writing Kubernetes manifests are only the first steps. To deliver software rapidly and reliably, teams must automate the entire process from code commit to production deployment. This module covers Continuous Integration (CI) and Continuous Delivery/Deployment (CD), detailing how to build automated pipelines using tools like GitHub Actions and Jenkins. Furthermore, it introduces GitOps—the modern paradigm for Kubernetes deployments using tools like ArgoCD, where Git serves as the single source of truth for your cluster's desired state.

  Prerequisites:
  - Understanding of Docker image building (File 109, 112).
  - Understanding of Kubernetes Deployments and Helm (File 116).

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  Complete CI/CD Pipeline Architecture (Push-Based)                      │
  │                                                                         │
  │    Developer              GitHub / GitLab                  CI/CD Server (Actions/Jenkins)│
  │    ---------              ---------------                  ------------------------------│
  │        |                         |                                      |│
  │  1. git push ------------------> |                                      |│
  │        |                         | 2. Webhook triggers CI               |│
  │        |                         |------------------------------------->| 3. Checkout Code│
  │        |                         |                                      | 4. Run Unit Tests│
  │        |                         |                                      | 5. docker build│
  │        |                         |                                      | 6. Image Scan (Trivy)│
  │                                                                         |│
  │  +------------------------------------------+                           | 7. docker push│
  │  |             Kubernetes Cluster           |                           v│
  │  |                                          |                  +-----------------+│
  │  | +-------------------------------------+  | 8. helm upgrade  | Container Reg.  |│
  │  | |             Deployment              | <-------------------| (DockerHub/ECR) |│
  │  | | (Pulls new image from registry)     |  |                  +-----------------+│
  │  | +-------------------------------------+  |                           │
  │  +------------------------------------------+                           │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  GitOps Flow with ArgoCD (Pull-Based)                                   │
  │                                                                         │
  │   1. CI Pipeline               2. Update Image Tag          3. GitOps Repository│
  │   (Builds & Pushes Image)      (via script/bot)             (Deployment Manifests)│
  │  +-----------------------+    +------------------+         +-----------------------+│
  │  |  App Source Repo      | => | Container Reg.   |         | apiVersion: apps/v1   |│
  │  | (Tests -> Build ->)   |    | (myapp:v2)       | =======>| image: myapp:v2       |│
  │  +-----------------------+    +------------------+         +-----------------------+│
  │                                                                        |│
  │                                                                        | 4. Monitor & Pull│
  │                                                                        v│
  │                                                             +-----------------------+│
  │                                                             | ArgoCD (Inside K8s)   |│
  │                                                             | (Detects drift between|│
  │                                                             | Git & Cluster)        |│
  │                                                             +-----------------------+│
  │                                                                        | 5. Sync/Apply│
  │                                                                        v│
  │                                                             +-----------------------+│
  │                                                             |   K8s API Server      |│
  │                                                             +-----------------------+│
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: groovy]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Jenkinsfile (Declarative Pipeline)                                   │
  │                                                                          │
  │  pipeline {                                                              │
  │      agent any                                                           │
  │      environment {                                                       │
  │          DOCKER_CREDENTIALS_ID = 'dockerhub-creds'                       │
  │          IMAGE_NAME = 'myorg/myapp'                                      │
  │          IMAGE_TAG = "${env.BUILD_NUMBER}"                               │
  │      }                                                                   │
  │      stages {                                                            │
  │          stage('Checkout') {                                             │
  │              steps { checkout scm }                                      │
  │          }                                                               │
  │          stage('Test') {                                                 │
  │              steps {                                                     │
  │                  sh 'npm ci'                                             │
  │                  sh 'npm run test'                                       │
  │              }                                                           │
  │          }                                                               │
  │          stage('Build & Push Docker Image') {                            │
  │              steps {                                                     │
  │                  script {                                                │
  │                      docker.withRegistry('https://index.docker.io/v1/', DOCKER_CREDENTIALS_ID) {│
  │                          def app = docker.build("${IMAGE_NAME}:${IMAGE_TAG}")│
  │                          app.push()                                      │
  │                          app.push('latest')                              │
  │                      }                                                   │
  │                  }                                                       │
  │              }                                                           │
  │          }                                                               │
  │          stage('Deploy to K8s') {                                        │
  │              steps {                                                     │
  │                  withKubeConfig([credentialsId: 'k8s-config']) {         │
  │                      // Update image imperatively or apply YAML          │
  │                      sh "kubectl set image deployment/myapp-deploy myapp=${IMAGE_NAME}:${IMAGE_TAG}"│
  │                  }                                                       │
  │              }                                                           │
  │          }                                                               │
  │      }                                                                   │
  │  }                                                                       │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: yaml]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │                                                                          │
  │  name: CI/CD Pipeline                                                    │
  │                                                                          │
  │  # Trigger on push to main branch                                        │
  │  on:                                                                     │
  │    push:                                                                 │
  │      branches:                                                           │
  │        - main                                                            │
  │                                                                          │
  │  env:                                                                    │
  │    REGISTRY: ghcr.io                                                     │
  │    IMAGE_NAME: ${{ github.repository }}                                  │
  │    # Generate a unique tag based on the Git commit SHA                   │
  │    IMAGE_TAG: ${{ github.sha }}                                          │
  │                                                                          │
  │  jobs:                                                                   │
  │    build-and-push:                                                       │
  │      runs-on: ubuntu-latest                                              │
  │      permissions:                                                        │
  │        contents: read                                                    │
  │        packages: write                                                   │
  │      steps:                                                              │
  │        - name: Checkout Code                                             │
  │          uses: actions/checkout@v3                                       │
  │                                                                          │
  │        - name: Run Unit Tests                                            │
  │          run: |                                                          │
  │            npm ci                                                        │
  │            npm run test                                                  │
  │                                                                          │
  │        - name: Log in to the Container registry                          │
  │          uses: docker/login-action@v2                                    │
  │          with:                                                           │
  │            registry: ${{ env.REGISTRY }}                                 │
  │            username: ${{ github.actor }}                                 │
  │            password: ${{ secrets.GITHUB_TOKEN }}                         │
  │                                                                          │
  │        - name: Build and push Docker image                               │
  │          uses: docker/build-push-action@v4                               │
  │          with:                                                           │
  │            context: .                                                    │
  │            push: true                                                    │
  │            tags: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ env.IMAGE_TAG }}│
  │                                                                          │
  │        # Optional: Run Trivy vulnerability scanner on the built image    │
  │        - name: Run Trivy vulnerability scanner                           │
  │          uses: aquasecurity/trivy-action@master                          │
  │          with:                                                           │
  │            image-ref: '${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ env.IMAGE_TAG }}'│
  │            format: 'table'                                               │
  │            exit-code: '1' # Fail pipeline if Critical CVEs found         │
  │            severity: 'CRITICAL,HIGH'                                     │
  │                                                                          │
  │    deploy:                                                               │
  │      needs: build-and-push                                               │
  │      runs-on: ubuntu-latest                                              │
  │      steps:                                                              │
  │        - name: Checkout Code                                             │
  │          uses: actions/checkout@v3                                       │
  │                                                                          │
  │        # Setup kubeconfig from a GitHub Secret                           │
  │        - name: Set up Kubeconfig                                         │
  │          uses: azure/k8s-set-context@v3                                  │
  │          with:                                                           │
  │            method: kubeconfig                                            │
  │            kubeconfig: ${{ secrets.KUBE_CONFIG }}                        │
  │                                                                          │
  │        - name: Setup Helm                                                │
  │          uses: azure/setup-helm@v3                                       │
  │                                                                          │
  │        - name: Deploy via Helm                                           │
  │          run: |                                                          │
  │            helm upgrade --install my-app ./helm-chart \                  │
  │              --namespace production \                                    │
  │              --set image.repository=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }} \│
  │              --set image.tag=${{ env.IMAGE_TAG }} \                      │
  │              --wait # Wait for pods to be ready                          │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  7. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

────────────────────────────────────────────────────────────────────────────────
  8. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: Riddle 1: The Ignored Update

  Scenario: You have a CI pipeline that builds an image myapi:latest and pushes it to DockerHub. The final step is kubectl apply -f deployment.yaml. The deployment.yaml specifies image: myapi:latest.
  You merge a bug fix. The pipeline runs. The image is built and pushed. kubectl apply runs. The pods don't restart, and the bug is still in production.
  What's wrong?

  SOLUTION:
    Kubernetes checks the declarative state. The previous state had image: myapi:latest. The new YAML applied also has image: myapi:latest. K8s sees absolutely no change in the desired state, so it does nothing. It does not pull the new image.
    Fix: Tag images with unique IDs (like the Git commit SHA or build number) and update the YAML with the new tag so K8s detects a change in the Deployment spec.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 2: Riddle 2: The Stale ConfigMap GitOps

  Scenario: You use ArgoCD (GitOps). You have a Deployment and a ConfigMap in Git. You update a value in the ConfigMap in Git. ArgoCD detects the change and syncs it. The ConfigMap in K8s is updated. However, the application Pods are still using the old configuration values.
  What's wrong?

  SOLUTION:
    This is a classic K8s behavior, not an ArgoCD bug. Updating a ConfigMap does not automatically restart Pods that consume it.
    Fix: In Helm, you can use a common trick: adding an annotation to the Pod template that hashes the ConfigMap contents (checksum/config: {{ include (print $.Template.BasePath "/configmap.yaml") . | sha256sum }}). When the ConfigMap changes, the hash changes, which alters the Pod template annotation, triggering K8s to roll out new Pods.

────────────────────────────────────────────────────────────────────────────────
  9. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  - Velocity: Automated pipelines allow companies like Amazon or Netflix to deploy thousands of times a day. Manual deployments limit you to deploying once a week or month.
  - Reliability: Humans make mistakes when typing commands in a terminal. Automated pipelines execute the exact same steps in the exact same order every single time, drastically reducing deployment failures.
  - Auditability & Compliance: With GitOps, every change to production infrastructure is a Git commit. You have a full history of *who* made the change, *why* (via PR descriptions), and *when*. This is critical for SOC2 compliance and security audits.

================================================================================
  END OF FILE 117
================================================================================
