================================================================================
  FILE 100: AWS COMPUTE: EC2, CONTAINERS, AND SERVERLESS
  Section: I - AWS Cloud Services
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  Compute is the brain of the cloud, encompassing everything from raw virtual machines to managed container orchestrators and highly abstracted serverless functions. This file covers the spectrum of AWS compute offerings, including EC2, Auto Scaling, Load Balancing, ECS/Fargate, Elastic Beanstalk, and Lambda.

  Prerequisites: Understanding of cloud fundamentals (File 99), operating systems, and basic networking.

  What you'll learn: 
  * EC2 instance lifecycles, families, and AMIs.
  * How to scale applications dynamically using ASGs and ALBs.
  * Container management with ECS and Fargate.
  * Serverless concepts, cold starts, and Lambda execution.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  EC2 (ELASTIC COMPUTE CLOUD)
    Secure, resizable compute capacity in the cloud. Think of it as a virtual server (VM) where you have full root/admin access.

  AMI (AMAZON MACHINE IMAGE)
    A template that contains a software configuration (e.g., an operating system, an application server, and applications) required to launch an EC2 instance.

  INSTANCE FAMILIES
    AWS categorizes EC2 instances based on their hardware optimization:
    * General Purpose (T, M): Balanced CPU, memory, networking.
    * Compute Optimized (C): High performance processors (batch processing, gaming).
    * Memory Optimized (R, X): Fast performance for workloads that process large data sets in memory (databases).
    * Storage Optimized (I, D): High sequential read/write access to large data sets on local storage.
    * Accelerated Computing (P, G): Hardware accelerators or co-processors (GPUs for ML/AI).

  USER DATA
    A script that automatically runs exactly once when an EC2 instance first boots up. Used for bootstrapping (installing software, fetching updates).

  AUTO SCALING GROUP (ASG)
    A logical collection of EC2 instances that share similar characteristics and are treated as a logical grouping for the purposes of automatic scaling and management.

  LAUNCH TEMPLATE
    A saved configuration that specifies instance configuration information (AMI, instance type, security groups) used by an ASG to launch new instances.

  ELASTIC LOAD BALANCER (ELB)
    Automatically distributes incoming application traffic across multiple targets, such as EC2 instances, containers, and IP addresses. Types include:
    * Application Load Balancer (ALB): Layer 7 (HTTP/HTTPS), routes traffic based on URL path, host, or HTTP headers.
    * Network Load Balancer (NLB): Layer 4 (TCP/UDP), ultra-high performance, ultra-low latency, handles millions of requests per second.
    * Gateway Load Balancer (GWLB): Layer 3 (Network), used to deploy, scale, and manage third-party virtual appliances (firewalls).

  LAMBDA
    A serverless, event-driven compute service that lets you run code without provisioning or managing servers. You pay only for the compute time you consume.

  COLD START
    The latency experienced when an AWS Lambda function is invoked for the first time or after a period of inactivity, as AWS provisions the execution environment and loads the code.

  ECS (ELASTIC CONTAINER SERVICE)
    A highly scalable, high-performance container orchestration service that supports Docker containers.

  FARGATE
    A serverless compute engine for containers that works with both ECS and EKS. Fargate removes the need to provision and manage the underlying EC2 instances.

  ELASTIC BEANSTALK
    A PaaS offering for deploying and scaling web applications and services developed with Java, .NET, PHP, Node.js, Python, Ruby, Go, and Docker on familiar servers such as Apache, Nginx, Passenger, and IIS.

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  Auto Scaling Group with Application Load Balancer                      │
  │                                                                         │
  │                                  +-------------+                        │
  │                                  |  End Users  |                        │
  │                                  +------+------+                        │
  │                                         |                               │
  │                                         v                               │
  │                                 +----------------+                      │
  │                                 |  Route 53 DNS  |                      │
  │                                 +-------+--------+                      │
  │                                         |                               │
  │                                         v                               │
  │                            +-------------------------+                  │
  │                            | Application Load Balancer| (Layer 7 Routing)│
  │                            +----+---------------+----+                  │
  │                                 |               |                       │
  │               +-----------------v---------------+---------------v----------------+│
  │               |                     Auto Scaling Group                           |│
  │               |                                                                  |│
  │               |  +---------------+  +---------------+  +---------------+         |│
  │               |  | EC2 Instance  |  | EC2 Instance  |  | EC2 Instance  |         |│
  │               |  |   (AZ-A)      |  |   (AZ-B)      |  |   (AZ-C)      |         |│
  │               |  +---------------+  +---------------+  +---------------+         |│
  │               |         (Dynamically scales in/out based on CPU metrics)         |│
  │               +------------------------------------------------------------------+│
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  Lambda Execution Lifecycle (Cold vs. Warm Start)                       │
  │                                                                         │
  │   Event Trigger (API Gateway, S3, SQS)                                  │
  │          |                                                              │
  │          v                                                              │
  │   +--------------------------------------------------------------------------------+│
  │   | AWS Lambda Service                                                             |│
  │   |                                                                                |│
  │   |  Is there an idle execution environment available?                             |│
  │   |                                                                                |│
  │   |       [ NO ] (Cold Start)                         [ YES ] (Warm Start)         |│
  │   |         |                                            |                         |│
  │   |  1. Provision Runtime Env (~100ms-1s)                |                         |│
  │   |         |                                            |                         |│
  │   |  2. Download Code / Load Image                       |                         |│
  │   |         |                                            |                         |│
  │   |  3. Run init code (outside handler)                  |                         |│
  │   |         |                                            |                         |│
  │   |         +-------------------> 4. Execute Handler Function <--------------------+│
  │   |                                      (Code runs)                               |│
  │   |                                           |                                    |│
  │   |                                           v                                    |│
  │   |                       Environment stays idle for ~10-15 mins                   |│
  │   |                       Waiting for next invocation (Warm Start)                 |│
  │   +--------------------------------------------------------------------------------+│
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  Language: Bash/JSON

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // EC2 User Data Script (Bash)                                          │
  │  // This script can be pasted into the "User Data" field when launching  │
  │  // an EC2 instance. It installs an Apache web server, starts it, and    │
  │  // creates a basic HTML page.                                           │
  │                                                                          │
  │  #!/bin/bash                                                             │
  │  # Update the OS packages                                                │
  │  yum update -y                                                           │
  │  # Install Apache web server                                             │
  │  yum install -y httpd                                                    │
  │  # Start the web server service                                          │
  │  systemctl start httpd                                                   │
  │  # Enable it to start on boot                                            │
  │  systemctl enable httpd                                                  │
  │  # Create a simple webpage with the instance hostname                    │
  │  echo "<html><body><h1>Hello from EC2!</h1><p>Instance: $(hostname -f)</p></body></html>" > /var/www/html/index.html│
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // ECS Task Definition (JSON snippet)                                   │
  │  // A simplified representation of an ECS task definition, showing how   │
  │  // memory and CPU are allocated to a specific Docker image.             │
  │                                                                          │
  │  {                                                                       │
  │    "family": "web-app-task",                                             │
  │    "networkMode": "awsvpc",                                              │
  │    "requiresCompatibilities": [ "FARGATE" ],                             │
  │    "cpu": "256",                                                         │
  │    "memory": "512",                                                      │
  │    "containerDefinitions": [                                             │
  │      {                                                                   │
  │        "name": "nginx-web-container",                                    │
  │        "image": "nginx:latest",                                          │
  │        "essential": true,                                                │
  │        "portMappings": [                                                 │
  │          {                                                               │
  │            "containerPort": 80,                                          │
  │            "hostPort": 80,                                               │
  │            "protocol": "tcp"                                             │
  │          }                                                               │
  │        ]                                                                 │
  │      }                                                                   │
  │    ]                                                                     │
  │  }                                                                       │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

  Language: Python

  ┌──────────────────────────────────────────────────────────────────────────┐
  │                                                                          │
  │  import json                                                             │
  │  import logging                                                          │
  │  import os                                                               │
  │  import boto3                                                            │
  │  from botocore.exceptions import ClientError                             │
  │                                                                          │
  │  # Set up logging                                                        │
  │  logger = logging.getLogger()                                            │
  │  logger.setLevel(logging.INFO)                                           │
  │                                                                          │
  │  # ==============================================================================│
  │  # Initialization Code (Runs ONCE per Cold Start)                        │
  │  # Initialize AWS clients outside the handler so they are reused in warm starts.│
  │  # This significantly improves performance and reduces latency.          │
  │  # ==============================================================================│
  │  REGION = os.environ.get('AWS_REGION', 'us-east-1')                      │
  │  dynamodb = boto3.resource('dynamodb', region_name=REGION)               │
  │  TABLE_NAME = os.environ.get('TABLE_NAME', 'UsersTable')                 │
  │  table = dynamodb.Table(TABLE_NAME)                                      │
  │                                                                          │
  │  def build_response(status_code: int, body: dict) -> dict:               │
  │      """Helper to format API Gateway responses."""                       │
  │      return {                                                            │
  │          'statusCode': status_code,                                      │
  │          'headers': {                                                    │
  │              'Content-Type': 'application/json',                         │
  │              'Access-Control-Allow-Origin': '*'  # CORS support          │
  │          },                                                              │
  │          'body': json.dumps(body)                                        │
  │      }                                                                   │
  │                                                                          │
  │  def lambda_handler(event, context):                                     │
  │      """                                                                 │
  │      Main Lambda entry point.                                            │
  │      """                                                                 │
  │      logger.info(f"Received event: {json.dumps(event)}")                 │
  │                                                                          │
  │      # Extract HTTP method and query parameters from API Gateway event   │
  │      http_method = event.get('httpMethod')                               │
  │      query_params = event.get('queryStringParameters') or {}             │
  │      user_id = query_params.get('userId')                                │
  │                                                                          │
  │      if not user_id:                                                     │
  │          return build_response(400, {'error': 'Missing userId parameter'})│
  │                                                                          │
  │      try:                                                                │
  │          if http_method == 'GET':                                        │
  │              # Fetch user from DynamoDB                                  │
  │              response = table.get_item(Key={'userId': user_id})          │
  │              item = response.get('Item')                                 │
  │                                                                          │
  │              if item:                                                    │
  │                  return build_response(200, item)                        │
  │              else:                                                       │
  │                  return build_response(404, {'error': 'User not found'}) │
  │                                                                          │
  │          else:                                                           │
  │              return build_response(405, {'error': f'Method {http_method} not allowed'})│
  │                                                                          │
  │      except ClientError as e:                                            │
  │          logger.error(f"DynamoDB ClientError: {e.response['Error']['Message']}")│
  │          return build_response(500, {'error': 'Internal server error'})  │
  │      except Exception as e:                                              │
  │          logger.error(f"Unexpected error: {str(e)}")                     │
  │          return build_response(500, {'error': 'Internal server error'})  │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  7. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: What is a Lambda "Cold Start" and how can you mitigate it?

  ANSWER:
    A cold start occurs when Lambda has to provision a new execution environment (download code, start runtime) before running the function. Mitigation strategies include writing initialization code outside the handler (reused in warm starts), using Provisioned Concurrency (keeps instances permanently warm), and minimizing deployment package size.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: How does an Application Load Balancer (ALB) differ from a Network Load Balancer (NLB)?

  ANSWER:
    ALB operates at Layer 7 (Application layer) and routes based on HTTP/HTTPS characteristics like URL path or headers. It's ideal for web apps and microservices. NLB operates at Layer 4 (Transport layer), routing based on IP/TCP/UDP. It is capable of handling millions of requests per second with extremely low latency, ideal for gaming or real-time streaming.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: What are the key differences between EC2 and Fargate?

  ANSWER:
    Both are compute engines. With EC2, you must provision, manage, patch, and scale the underlying virtual machines yourself (even when running containers). Fargate is a serverless compute engine for containers; you only specify the vCPU and memory needed for your task, and AWS completely abstracts away the underlying infrastructure.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: Explain how an Auto Scaling Group (ASG) scales dynamically.

  ANSWER:
    An ASG uses scaling policies linked to CloudWatch alarms. For example, a Target Tracking policy can be set to keep average CPU utilization at 50%. If CPU rises to 70%, the alarm triggers the ASG to launch more instances. If it drops to 30%, it terminates instances.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: What is the maximum execution duration for an AWS Lambda function?

  ANSWER:
    15 minutes (900 seconds). If a workload takes longer, it should be moved to ECS, AWS Batch, or broken down using Step Functions.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: How do you securely pass a database password to an EC2 instance on boot?

  ANSWER:
    You should store the password in AWS Secrets Manager or Systems Manager Parameter Store. During boot, the EC2 User Data script (using an attached IAM Role with appropriate permissions) queries the API to retrieve the secret. You should never hardcode secrets in User Data scripts or AMIs.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q7: What is Lambda@Edge?

  ANSWER:
    Lambda@Edge allows you to run Lambda functions at AWS Edge Locations (CloudFront). It intercepts HTTP requests/responses between the user and the origin, enabling custom logic like URL rewrites, A/B testing, or custom authentication closer to the user to reduce latency.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q8: You need to launch an application on AWS that relies on an older version of Windows Server and requires modifying the registry. Which compute service is most appropriate?

  ANSWER:
    EC2. EC2 gives you full administrative (RDP/root) access to the underlying OS, allowing custom registry edits and legacy OS support. Fargate or Elastic Beanstalk abstract the OS away and might not support legacy configurations.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q9: Explain the concept of EC2 User Data. When does it run?

  ANSWER:
    User Data is a script that runs automatically only once during the very first boot cycle of an EC2 instance. It is typically used for bootstrapping (e.g., installing packages, starting services).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q10: What is a Launch Template in AWS?

  ANSWER:
    A Launch Template defines the parameters for launching an EC2 instance (AMI ID, instance type, security groups, key pairs, user data). It is used primarily by Auto Scaling Groups to know what kind of instance to spin up when a scaling event occurs.

────────────────────────────────────────────────────────────────────────────────
  8. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: Riddle 1

  I listen on Layer 7 and read your HTTP paths. I send `/api` traffic to Lambda and `/web` traffic to EC2. What am I?

  SOLUTION:
    Application Load Balancer (ALB).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 2: Riddle 2

  You deploy your code to me, and I vanish into thin air. But when a file hits S3, I spring to life for just a few seconds, do my job, and disappear again. I charge you by the millisecond. What am I?

  SOLUTION:
    AWS Lambda.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 3: What's Wrong With This Architecture?

  Scenario: A developer wants to run a background video processing job that takes exactly 45 minutes to complete per video. They decide to use AWS Lambda triggered by an S3 event because they want it to be "serverless".

  SOLUTION:
    AWS Lambda has a hard maximum timeout limit of 15 minutes. A 45-minute job will consistently fail and time out. The developer should use AWS ECS with Fargate (which has no time limit but remains serverless), or AWS Batch.

────────────────────────────────────────────────────────────────────────────────
  9. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  * Handling Spiky Traffic: E-commerce sites on Black Friday rely on ASGs and ALBs. Without them, servers would crash under load. With them, the infrastructure dynamically expands to handle thousands of requests per second, then scales down to save money when the sale ends.
  * Microservices Evolution: Companies are moving away from massive monolithic EC2 instances toward microservices running on ECS/Eargate or Lambda. This allows different teams to deploy, scale, and manage their services independently without affecting the rest of the application.
  * Cost Efficiency (Serverless): For unpredictable, low-volume internal tools, provisioning an EC2 instance 24/7 is a waste of money. Using Lambda, you only pay exactly for the execution time, which can reduce a $30/month EC2 bill down to literally $0.00 if it falls within the Free Tier.

────────────────────────────────────────────────────────────────────────────────
  10. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

  -> File 099: Cloud AWS Fundamentals (Understanding Global Infrastructure)
  -> File 103: AWS Networking (VPCs and Security Groups that wrap around EC2)
  -> File 106: AWS Architecture Patterns (How to combine these compute services into full applications)

================================================================================
  END OF FILE 100
================================================================================
