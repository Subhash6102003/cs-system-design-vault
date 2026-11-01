================================================================================
  FILE 106: AWS ARCHITECTURE PATTERNS
  Section: I - AWS Cloud Services
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  AWS Architecture Patterns: Combining Services for Production
  Understanding individual AWS services is only half the battle. Cloud engineering requires knowing how to stitch these services together into resilient, scalable, and cost-effective architectures. This file covers the most common architectural patterns used in the industry, from legacy 3-tier web apps to modern event-driven serverless designs.

  Prerequisites: Knowledge of VPC, EC2, S3, RDS, DynamoDB, Lambda, and SQS/SNS.
  What you'll learn:
  *   Traditional 3-Tier Web Application Architecture.
  *   Serverless Microservices Architecture.
  *   Event-Driven and Fan-Out Patterns.
  *   Static Website Hosting Pattern.
  *   How to evaluate cost, operational overhead, and scalability for each.

  ---

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  **MONOLITH
    ** An application where the UI, business logic, and database access are tightly coupled in a single codebase and deployed on a single server structure.

  **MICROSERVICES
    ** An architectural style that structures an application as a collection of loosely coupled, independently deployable services.

  **STATEFUL VS STATELESS
    ** A stateful architecture relies on local server memory to store user sessions. A stateless architecture pushes all session state to an external database (like ElastiCache or DynamoDB), allowing any server to handle any request. Cloud architectures *must* be stateless to scale effectively.

  **HIGH AVAILABILITY (HA)
    ** A system designed to operate continuously without failure for a long time. In AWS, this implies deploying resources across multiple Availability

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

────────────────────────────────────────────────────────────────────────────────
  5. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: bash]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Evaluating the Static Website Pattern (AWS CLI)                      │
  │                                                                          │
  │  # 1. Create a bucket for the website                                    │
  │  aws s3 mb s3://my-global-react-app-12345                                │
  │                                                                          │
  │  # 2. Configure bucket for static website hosting                        │
  │  aws s3 website s3://my-global-react-app-12345/ \                        │
  │      --index-document index.html \                                       │
  │      --error-document error.html                                         │
  │                                                                          │
  │  # 3. Upload the build folder (e.g., React build output)                 │
  │  aws s3 sync ./build s3://my-global-react-app-12345/                     │
  │                                                                          │
  │  # 4. Attach a bucket policy to allow public read access (simplified)    │
  │  # In production, you would restrict this to CloudFront using an OAC (Origin Access Control)│
  │  aws s3api put-bucket-policy \                                           │
  │      --bucket my-global-react-app-12345 \                                │
  │      --policy file://public_policy.json                                  │
  │                                                                          │
  │  # (Next step in console/IaC would be deploying a CloudFront distribution pointing to this bucket)│
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: python]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │                                                                          │
  │  from aws_cdk import (                                                   │
  │      aws_dynamodb as dynamodb,                                           │
  │      aws_lambda as _lambda,                                              │
  │      aws_apigateway as apigw,                                            │
  │      RemovalPolicy,                                                      │
  │      App, Stack                                                          │
  │  )                                                                       │
  │  from constructs import Construct                                        │
  │                                                                          │
  │  class ServerlessApiStack(Stack):                                        │
  │      def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:│
  │          super().__init__(scope, construct_id, **kwargs)                 │
  │                                                                          │
  │          # 1. Create DynamoDB Table (Serverless Database)                │
  │          table = dynamodb.Table(                                         │
  │              self, "UsersTable",                                         │
  │              partition_key=dynamodb.Attribute(name="userId", type=dynamodb.AttributeType.STRING),│
  │              billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST, # On-demand scaling│
  │              removal_policy=RemovalPolicy.DESTROY # For dev only!        │
  │          )                                                               │
  │                                                                          │
  │          # 2. Create Lambda Function (Compute)                           │
  │          user_handler = _lambda.Function(                                │
  │              self, "UserHandlerFunction",                                │
  │              runtime=_lambda.Runtime.PYTHON_3_9,                         │
  │              handler="app.handler",                                      │
  │              code=_lambda.Code.from_asset("lambda_src"),                 │
  │              environment={                                               │
  │                  "TABLE_NAME": table.table_name                          │
  │              }                                                           │
  │          )                                                               │
  │                                                                          │
  │          # 3. Grant the Lambda function Read/Write permissions to the table (Least Privilege)│
  │          table.grant_read_write_data(user_handler)                       │
  │                                                                          │
  │          # 4. Create API Gateway (Entry point)                           │
  │          api = apigw.RestApi(                                            │
  │              self, "UserApi",                                            │
  │              rest_api_name="User Service",                               │
  │              description="Handles user CRUD operations."                 │
  │          )                                                               │
  │                                                                          │
  │          # Link API /users endpoint to Lambda                            │
  │          users_resource = api.root.add_resource("users")                 │
  │          users_integration = apigw.LambdaIntegration(user_handler)       │
  │          users_resource.add_method("GET", users_integration)             │
  │          users_resource.add_method("POST", users_integration)            │
  │                                                                          │
  │  app = App()                                                             │
  │  ServerlessApiStack(app, "ProductionServerlessStack")                    │
  │  app.synth()                                                             │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  7. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: In a 3-tier architecture, why do we place the database in a private isolated subnet?

  ANSWER:
    Security. The database holds the most sensitive data. Placing it in a private isolated subnet ensures it has no route to the internet, meaning attackers cannot reach it directly from the outside. It can only be accessed by the Application tier servers located in the private subnet.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: What are the trade-offs of using a Serverless Microservices architecture (API Gateway + Lambda + DynamoDB) versus a traditional 3-Tier EC2 architecture?

  ANSWER:
    Serverless eliminates OS maintenance, auto-scales instantly, and charges only per request (zero cost when idle). However, it suffers from Lambda cold starts, vendor lock-in, and can become expensive under massive, sustained, continuous load where reserved EC2 instances would be cheaper.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: How do you make an EC2-based web application "stateless" so it can scale horizontally?

  ANSWER:
    You must decouple session state and file storage from the EC2 instances. Store user session data in ElastiCache (Redis) or DynamoDB, and store uploaded files in S3. This allows any EC2 instance in the Auto Scaling Group to safely terminate or serve any user request.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: Explain how you would design an architecture to handle a video processing job that takes 30 minutes.

  ANSWER:
    Use an Event-Driven Batch architecture. The user uploads a video to S3. S3 triggers an EventBridge event. The event places a message in an SQS queue. An ECS (Fargate) cluster runs worker containers that poll the queue, download the video, process it (since containers have no 15-minute Lambda timeout), and save the result back to S3.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: Why combine CloudFront with S3 for a static website?

  ANSWER:
    While S3 can host a website natively, it serves files from a single region. Adding CloudFront caches the site globally, providing massive latency reduction for international users, enabling custom SSL certificates via ACM, and providing DDoS protection via AWS Shield.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: What is the "Strangler Fig" pattern in cloud migration?

  ANSWER:
    It is a strategy to migrate a legacy monolith to microservices. Instead of a risky "big bang" rewrite, you place an API Gateway in front of the monolith. You slowly build new features as microservices (Lambda/ECS) and route traffic for those specific endpoints to the new services, gradually "strangling" the monolith until it can be retired.

────────────────────────────────────────────────────────────────────────────────
  8. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: Riddle 1

  *I am the architecture that developers love for small apps. I have no servers to patch, no instances to monitor, and I cost exactly $0.00 if nobody visits your site. What am I?*

  SOLUTION:
    Serverless Architecture.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 2: Riddle 2

  *I sit between the internet and your servers. I am the great balancer, distributing weight evenly so no single server collapses under pressure. What am I?*

  SOLUTION:
    Elastic Load Balancer.

────────────────────────────────────────────────────────────────────────────────
  9. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  *   Passing the AWS Solutions Architect Exam: Architecture patterns are the core of the AWS certification exams. You are rarely tested on isolated services; you are tested on how they interact.
  *   Startup Survival: A startup that builds a monolithic app on a single massive EC2 instance will suffer a total outage when they get mentioned on Reddit (the "hug of death"). A startup using an S3+CloudFront static frontend and an API Gateway+Lambda backend will absorb the traffic spike effortlessly without crashing.
  *   Enterprise Migration: Understanding 3-Tier architectures is mandatory for cloud consultants, as this is the pattern used to lift-and-shift legacy enterprise applications from on-premises data centers into the cloud.
  ---

================================================================================
  END OF FILE 106
================================================================================
