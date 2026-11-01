================================================================================
  FILE 108: AWS DEPLOYMENT & INFRASTRUCTURE AS CODE (IAC)
  Section: I - AWS Cloud Services
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  AWS Deployment: CloudFormation, CDK, Terraform, and CI/CD
  Clicking through the AWS Console to create resources is fine for learning, but disastrous in production. Manual creation leads to human error, undocumented changes, and environments that cannot be replicated. Infrastructure as Code (IaC) solves this by defining infrastructure in code. This file covers AWS CloudFormation, AWS CDK, HashiCorp Terraform, and CI/CD pipelines.

  Prerequisites: Understanding of core AWS services (VPC, EC2, Lambda).
  What you'll learn:
  *   Why Infrastructure as Code is mandatory for production.
  *   AWS CloudFormation templates and state management.
  *   AWS CDK (Cloud Development Kit) constructs and synth process.
  *   AWS SAM for Serverless apps.
  *   Terraform vs CloudFormation.
  *   AWS CodePipeline and deployment strategies (Blue/Green, Canary).

  ---

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  **INFRASTRUCTURE AS CODE (IAC)
    ** The process of managing and provisioning cloud resources through machine-readable definition files, rather than physical hardware configuration or interactive configuration tools (like the AWS Console).

  **CLOUDFORMATION (CFN)
    ** AWS's native IaC service. You write templates in YAML or JSON, and CloudFormation provisions the resources.

  **STACK
    ** A collection of AWS resources that you can manage as a single unit using CloudFormation. You create, update, or delete a collection of resources by creating, updating, or deleting stacks.

  **DRIFT DETECTION
    ** A feature in CloudFormation that detects if someone manually changed a resource (e.g., changed a security group rule via the console) so it no longer matches the template.

  **AWS CDK (CLOUD DEVELOPMENT KIT)
    ** An open-source software development framework to define cloud infrastructure in code (Python, TypeScript, Java) and provision it through CloudFormation.

  **CONSTRUCTS
    ** The basic building blocks of CDK apps.

  *L1 (CFN RESOURCES)
    * 1-to-1 mapping to CloudFormation resources.

  *L2 (AWS CONSTRUCTS)
    * Higher-level abstractions with sensible defaults (e.g., ec2.Vpc creates subnets and IGWs automatically).

  *L3 (PATTERNS)
    * Architecture-level constructs (e.g., ApplicationLoadBalancedFargateService).

  **AWS SAM (SERVERLESS APPLICATION MODEL)
    ** An open-source framework specifically for building serverless applications. It extends CloudFormation with simplified syntax (AWS::Serverless::Function).

  **TERRAFORM
    ** An open-source IaC tool by HashiCorp. It uses HCL (HashiCorp Configuration Language) and supports multi-cloud deployments (AWS, Azure, GCP).

  **CI/CD (CONTINUOUS INTEGRATION/CONTINUOUS DEPLOYMENT)
    ** The practice of automating the integration of code changes and the deployment to production.

  **CODEPIPELINE / CODEBUILD / CODEDEPLOY
    ** AWS's suite of developer tools for orchestrating CI/CD pipelines, compiling source code, and deploying to EC2/ECS/Lambda.

  **BLUE/GREEN DEPLOYMENT
    ** A deployment strategy that creates two separate but identical environments. Traffic is routed to the "Blue" (old) environment, then switched entirely to the "Green" (new) environment.

  **CANARY DEPLOYMENT
    ** Slowly rolling out a new version to a small subset of users (e.g., 10%) before rolling it out to the entire infrastructure.

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  Infrastructure as Code CI/CD Pipeline                                  │
  │                                                                         │
  │   +----------------+      +-----------------+      +--------------------+│
  │   | Developer      |      | Version Control |      | AWS CodePipeline   |│
  │   | Writes App     | ---> | (GitHub /       | ---> | (Orchestrator)     |│
  │   | + CDK/CFN Code |      |  CodeCommit)    |      +---------+----------+│
  │   +----------------+      +-----------------+                |          │
  │                                                              v          │
  │                                                    +--------------------+│
  │                                                    | AWS CodeBuild      |│
  │                                                    | (Compiles code,    |│
  │                                                    |  Runs unit tests,  |│
  │                                                    |  'cdk synth')      |│
  │                                                    +---------+----------+│
  │                                                              |          │
  │                                                              v          │
  │                                                    +--------------------+│
  │                                                    | AWS CloudFormation |│
  │                                                    | (Provisions VPC,   |│
  │                                                    |  S3, DynamoDB)     |│
  │                                                    +---------+----------+│
  │                                                              |          │
  │                                                              v          │
  │                                                    +--------------------+│
  │                                                    | AWS CodeDeploy     |│
  │                                                    | (Deploys App code  |│
  │                                                    |  to EC2/ECS/Lambda)|│
  │                                                    +--------------------+│
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: yaml]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // AWS CloudFormation Template (YAML) - VPC & EC2                       │
  │                                                                          │
  │  AWSTemplateFormatVersion: '2010-09-09'                                  │
  │  Description: A simple EC2 instance with a Security Group.               │
  │                                                                          │
  │  Parameters:                                                             │
  │    InstanceTypeParam:                                                    │
  │      Type: String                                                        │
  │      Default: t3.micro                                                   │
  │      AllowedValues: [t3.micro, t3.small, t3.medium]                      │
  │      Description: Enter the EC2 instance type.                           │
  │                                                                          │
  │  Resources:                                                              │
  │    # 1. Create a Security Group                                          │
  │    WebServerSecurityGroup:                                               │
  │      Type: AWS::EC2::SecurityGroup                                       │
  │      Properties:                                                         │
  │        GroupDescription: Allow HTTP traffic                              │
  │        SecurityGroupIngress:                                             │
  │          - IpProtocol: tcp                                               │
  │            FromPort: 80                                                  │
  │            ToPort: 80                                                    │
  │            CidrIp: 0.0.0.0/0                                             │
  │                                                                          │
  │    # 2. Create the EC2 Instance                                          │
  │    MyWebServer:                                                          │
  │      Type: AWS::EC2::Instance                                            │
  │      Properties:                                                         │
  │        InstanceType: !Ref InstanceTypeParam                              │
  │        ImageId: ami-0c55b159cbfafe1f0 # Amazon Linux 2 in us-east-1      │
  │        SecurityGroupIds:                                                 │
  │          - !Ref WebServerSecurityGroup                                   │
  │                                                                          │
  │  Outputs:                                                                │
  │    PublicIp:                                                             │
  │      Description: Public IP of the web server                            │
  │      Value: !GetAtt MyWebServer.PublicIp                                 │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: python]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │                                                                          │
  │  from aws_cdk import (                                                   │
  │      aws_lambda as _lambda,                                              │
  │      aws_apigateway as apigw,                                            │
  │      App, Stack, Duration                                                │
  │  )                                                                       │
  │  from constructs import Construct                                        │
  │                                                                          │
  │  class ServerlessAppStack(Stack):                                        │
  │      def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:│
  │          super().__init__(scope, construct_id, **kwargs)                 │
  │                                                                          │
  │          # 1. Define the Lambda function                                 │
  │          # CDK automatically packages the 'src' directory into a zip, uploads it to S3,│
  │          # creates the IAM execution role, and wires it to the function. │
  │          hello_function = _lambda.Function(                              │
  │              self, 'HelloHandler',                                       │
  │              runtime=_lambda.Runtime.PYTHON_3_9,                         │
  │              code=_lambda.Code.from_asset('src'), # Directory containing app code│
  │              handler='hello.handler',                                    │
  │              timeout=Duration.seconds(10),                               │
  │              memory_size=128                                             │
  │          )                                                               │
  │                                                                          │
  │          # 2. Define the API Gateway                                     │
  │          # CDK automatically creates the RestApi, Deployment, Stage, and permissions│
  │          # to allow API Gateway to invoke the Lambda function.           │
  │          api = apigw.LambdaRestApi(                                      │
  │              self, 'Endpoint',                                           │
  │              handler=hello_function,                                     │
  │              description="My Serverless API Endpoint"                    │
  │          )                                                               │
  │                                                                          │
  │  # Boilerplate to synthesize the CloudFormation template                 │
  │  app = App()                                                             │
  │  ServerlessAppStack(app, "ProdServerlessStack")                          │
  │  app.synth()                                                             │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  7. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: Why is manual configuration via the AWS Console discouraged in production environments?

  ANSWER:
    It is unrepeatable, un-auditable, and prone to human error. If a VPC is configured manually and goes down, rebuilding it exactly the same way is nearly impossible. IaC ensures infrastructure is version-controlled, testable, and instantly reproducible.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: What is CloudFormation "Drift"?

  ANSWER:
    Drift occurs when the actual state of an AWS resource differs from the expected state defined in the CloudFormation template. This usually happens when an administrator manually modifies a resource (like opening a port in a Security Group) via the console instead of updating the code.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: Explain the difference between AWS CDK and AWS CloudFormation.

  ANSWER:
    CloudFormation uses declarative YAML/JSON files to define infrastructure. CDK is an imperative programming framework (Python, TS, Java) that allows you to use logic (loops, if-statements, object-oriented classes) to define infrastructure. Under the hood, CDK *synthesizes* (compiles) down into CloudFormation templates before deployment.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: Why might a company choose Terraform over AWS CloudFormation/CDK?

  ANSWER:
    Terraform is cloud-agnostic. If a company operates in a multi-cloud environment (AWS, Azure, GCP), Terraform allows them to use a single tool and language (HCL) to provision infrastructure across all providers. CloudFormation and CDK are strictly AWS-only.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: How does Terraform manage "state"?

  ANSWER:
    Terraform maps real-world resources to your configuration using a State file (terraform.tfstate). In production, this state file must be stored in a remote backend (like an S3 bucket) with state locking (via DynamoDB) to prevent multiple developers from corrupting the state simultaneously.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: What is a Canary Deployment?

  ANSWER:
    A deployment strategy where a new version of an application is rolled out to a small percentage of users (the "canary"). The system monitors for errors. If none are found, the rollout expands gradually (e.g., 10% -> 50% -> 100%). If errors spike, it automatically rolls back.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q7: What is AWS SAM and how does it relate to CloudFormation?

  ANSWER:
    SAM (Serverless Application Model) is an extension of CloudFormation optimized for serverless apps. It introduces simplified resources (like AWS::Serverless::Function). When deployed, SAM templates are transformed by AWS into standard, verbose CloudFormation templates.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q8: What does cdk synth do?

  ANSWER:
    It executes your CDK app code (e.g., Python/TypeScript) and translates all the L2/L3 constructs into a raw, deployable CloudFormation JSON/YAML template.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q9: You are deploying a critical update to a database schema and application code. Which deployment strategy offers the safest rollback path: Rolling or Blue/Green?

  ANSWER:
    Blue/Green. You deploy the new app and schema to the Green environment while users are still on Blue. You test Green. If it passes, you switch the router (Route53/ALB) to point to Green. If a critical bug appears, you simply switch the router back to Blue instantly.

────────────────────────────────────────────────────────────────────────────────
  8. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: Riddle 1

  *I am written in Python or TypeScript, but the cloud doesn't understand me. I must be translated into a massive YAML document before AWS will build my castles. What am I?*

  SOLUTION:
    AWS CDK.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 2: Riddle 2

  *A developer panicked and opened port 22 directly in the AWS console because the site was down. My code says port 22 should be closed. What state am I in?*

  SOLUTION:
    Drifted (CloudFormation Drift).

────────────────────────────────────────────────────────────────────────────────
  9. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  *   Disaster Recovery: If an entire AWS region (e.g., us-east-1) goes down, a company using IaC can simply point their CDK/Terraform code to us-west-2, run deploy, and have an identical copy of their infrastructure running in minutes. Without IaC, rebuilding takes days.
  *   Code Reviews for Infrastructure: By treating infrastructure as code, changes to a firewall (Security Group) must be made via a Pull Request. Security engineers can review and approve the PR before the firewall is opened, ensuring compliance.
  *   Developer Velocity: CI/CD pipelines allow companies to deploy code dozens of times a day safely. Automated testing and Canary deployments ensure that if a bad bug is deployed, it only affects 5% of users and is rolled back instantly without human intervention.
  ---

================================================================================
  END OF FILE 108
================================================================================
