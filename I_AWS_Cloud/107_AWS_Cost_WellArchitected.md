================================================================================
  FILE 107: AWS COST OPTIMIZATION & WELL-ARCHITECTED FRAMEWORK
  Section: I - AWS Cloud Services
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  AWS Cost Optimization and the Well-Architected Framework
  The cloud provides infinite scalability, but also infinite ways to spend money. Without governance, AWS bills can spiral out of control. This file covers the financial mechanics of AWS (pricing models, Cost Explorer) and introduces the AWS Well-Architected Framework—a set of best practices for designing reliable, secure, and cost-efficient systems.

  Prerequisites: Understanding of AWS compute, storage, and networking services.
  What you'll learn:
  *   Pricing models: On-Demand, Reserved, Spot, Savings Plans.
  *   Tools for tracking spend: Cost Explorer, Budgets, Trusted Advisor.
  *   The 6 Pillars of the AWS Well-Architected Framework.
  *   Strategies for "right-sizing" infrastructure.

  ---

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  **ON-DEMAND PRICING
    ** Pay for compute or database capacity by the hour or second with no long-term commitments. Most expensive, but most flexible.

  **RESERVED INSTANCES (RIS)
    ** A billing discount (up to 72%) in exchange for committing to a specific instance type and operating system within a specific region for a 1-year or 3-year term.

  **SAVINGS PLANS
    ** A flexible pricing model offering lower prices in exchange for a commitment to a consistent amount of usage (measured in $/hour) for a 1 or 3-year term. More flexible than RIs.

  **SPOT INSTANCES
    Spare AWS compute capacity available at massive discounts (up to 90%). Warning:** AWS can reclaim these instances with only a 2-minute notice if they need the capacity back.

  **AWS COST EXPLORER
    ** A tool that enables you to view and analyze your AWS costs and usage, identifying trends and cost drivers.

  **AWS BUDGETS
    ** Gives you the ability to set custom budgets that alert you when your costs or usage exceed (or are forecasted to exceed) your budgeted amount.

  **AWS TRUSTED ADVISOR
    ** An online tool that provides real-time guidance to help you provision your resources following AWS best practices (Cost, Performance, Security, Fault Tolerance, Service Limits).

  **WELL-ARCHITECTED FRAMEWORK
    ** A set of guiding principles designed by AWS to help cloud architects build secure, high-performing, resilient, and efficient infrastructure. It consists of 6 pillars.

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  Cost Optimization Decision Tree (Compute)                              │
  │                                                                         │
  │                       What is the nature of the workload?               │
  │                                       |                                 │
  │             +-------------------------+-------------------------+       │
  │             |                         |                         |       │
  │        [ Continuous /           [ Spiky /                 [ Batch Processing /│
  │          Predictable ]            Unpredictable ]           Fault Tolerant ]│
  │             |                         |                         |       │
  │             v                         v                         v       │
  │   +-------------------+     +-------------------+     +-------------------+│
  │   | 1-yr or 3-yr      |     | On-Demand or      |     | Spot Instances    |│
  │   | Savings Plan      |     | Serverless        |     | (Up to 90% off!)  |│
  │   | (Up to 72% off)   |     | (Pay exactly      |     |                   |│
  │   |                   |     |  for what is used)|     |                   |│
  │   +-------------------+     +-------------------+     +-------------------+│
  │             |                         |                         |       │
  │             +-------------------------+-------------------------+       │
  │                                       |                                 │
  │                                       v                                 │
  │                          [ Always apply Right-Sizing ]                  │
  │                 (Don't run a 16-core instance for a 2-core job)         │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  The 6 Pillars of the Well-Architected Framework                        │
  │                                                                         │
  │   +---------------------------------------------------------------+     │
  │   |               AWS WELL-ARCHITECTED FRAMEWORK                  |     │
  │   +---------------------------------------------------------------+     │
  │   | 1. Operational Excellence (Run and monitor systems)           |     │
  │   | 2. Security (Protect data, systems, and assets)               |     │
  │   | 3. Reliability (Recover from infrastructure failures)         |     │
  │   | 4. Performance Efficiency (Use IT and computing efficiently)  |     │
  │   | 5. Cost Optimization (Avoid unneeded costs)                   |     │
  │   | 6. Sustainability (Minimize environmental impacts)            |     │
  │   +---------------------------------------------------------------+     │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: bash]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Checking Trusted Advisor via AWS CLI                                 │
  │                                                                          │
  │  #!/bin/bash                                                             │
  │  # Note: Requires AWS Business or Enterprise Support plan for full checks.│
  │                                                                          │
  │  echo "Querying AWS Trusted Advisor Cost Optimization Checks..."         │
  │                                                                          │
  │  # List available Trusted Advisor checks                                 │
  │  aws support describe-trusted-advisor-checks \                           │
  │      --language "en" \                                                   │
  │      --query "checks[?category=='cost_optimizing'].[id, name]" \         │
  │      --output table                                                      │
  │                                                                          │
  │  # Check a specific ID (e.g., "Idle Load Balancers")                     │
  │  # aws support describe-trusted-advisor-check-result \                   │
  │  #    --check-id "eGs7NmtV6D" \                                          │
  │  #    --language "en"                                                    │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: python]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │                                                                          │
  │  import boto3                                                            │
  │  import logging                                                          │
  │                                                                          │
  │  logger = logging.getLogger()                                            │
  │  logger.setLevel(logging.INFO)                                           │
  │                                                                          │
  │  def lambda_handler(event, context):                                     │
  │      """                                                                 │
  │      Finds and stops all EC2 instances tagged with 'Environment=Dev'.    │
  │      Intended to be run via a nightly EventBridge cron schedule.         │
  │      """                                                                 │
  │      ec2_client = boto3.client('ec2', region_name='us-east-1')           │
  │                                                                          │
  │      # Filter for instances that are currently running AND tagged as Dev │
  │      filters = [                                                         │
  │          {'Name': 'instance-state-name', 'Values': ['running']},         │
  │          {'Name': 'tag:Environment', 'Values': ['Dev']}                  │
  │      ]                                                                   │
  │                                                                          │
  │      try:                                                                │
  │          response = ec2_client.describe_instances(Filters=filters)       │
  │          instances_to_stop = []                                          │
  │                                                                          │
  │          for reservation in response['Reservations']:                    │
  │              for instance in reservation['Instances']:                   │
  │                  instances_to_stop.append(instance['InstanceId'])        │
  │                                                                          │
  │          if instances_to_stop:                                           │
  │              logger.info(f"Stopping Dev instances: {instances_to_stop}") │
  │              ec2_client.stop_instances(InstanceIds=instances_to_stop)    │
  │              return {"status": "SUCCESS", "stopped_instances": instances_to_stop}│
  │          else:                                                           │
  │              logger.info("No running Dev instances found.")              │
  │              return {"status": "SUCCESS", "stopped_instances": []}       │
  │                                                                          │
  │      except Exception as e:                                              │
  │          logger.error(f"Error stopping instances: {str(e)}")             │
  │          return {"status": "ERROR", "message": str(e)}                   │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  7. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: What are Spot Instances and when should you use them?

  ANSWER:
    Spot instances use spare AWS capacity and are heavily discounted (up to 90%). However, AWS can interrupt them with 2 minutes' notice. They should be used for fault-tolerant, stateless workloads like batch processing, image rendering, or stateless web server fleets behind a load balancer. They should NEVER be used for databases.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: Explain the difference between Reserved Instances (RIs) and Savings Plans.

  ANSWER:
    Both offer discounts for 1 or 3-year commitments. RIs are tied to a specific instance family (e.g., m5) in a specific region. Savings Plans are more flexible; you commit to a dollar amount per hour (e.g., $10/hr), and the discount applies to *any* compute usage (EC2, Fargate, Lambda) across families and regions.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: What is "Right-Sizing" in AWS?

  ANSWER:
    Right-sizing is the process of matching instance types and sizes to your workload performance and capacity requirements at the lowest possible cost. It involves looking at CloudWatch metrics (CPU, memory) and down-sizing oversized instances (e.g., moving from an m5.xlarge to an m5.large).

────────────────────────────────────────────────────────────────────────────────
  8. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: Riddle 1

  *I am extremely cheap to hire, but I am very unreliable. If my boss needs me for a higher-paying job, I will pack my bags and leave your project with only 120 seconds of warning. What am I?*

  SOLUTION:
    An EC2 Spot Instance.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 2: Riddle 2

  *I sit quietly analyzing your account. I will tell you if your ports are open to the world, if your load balancers are lonely and idle, and if you are about to hit an AWS limit. What am I?*

  SOLUTION:
    AWS Trusted Advisor.

────────────────────────────────────────────────────────────────────────────────
  9. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  *   Startup Runways: Cloud costs are often the second highest expense for a startup (after payroll). Failing to understand CloudWatch, right-sizing, and idle resource cleanup can shorten a company's financial runway by months.
  *   Architecture Reviews: Before launching a major application, enterprise companies conduct a "Well-Architected Review." Engineers must prove they have considered security, backups, and cost controls before the architecture is approved for production.
  *   Spot Instance Savings: Using Spot instances for CI/CD pipelines (Jenkins runners) or data processing (Hadoop/Spark) can reduce compute bills by hundreds of thousands of dollars annually for large enterprises.
  ---

================================================================================
  END OF FILE 107
================================================================================
