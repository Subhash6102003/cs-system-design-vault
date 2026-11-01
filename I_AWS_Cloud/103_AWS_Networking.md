================================================================================
  FILE 103: AWS NETWORKING: VPC, ROUTE53, AND CLOUDFRONT
  Section: I - AWS Cloud Services
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  Networking is the foundational plumbing of the cloud. Without a securely designed network, your compute and databases are either completely isolated or recklessly exposed to the public internet. This file covers building private networks with VPCs, routing traffic globally with Route53, and accelerating content delivery with CloudFront.

  Prerequisites: Basic understanding of IP addressing (IPv4), CIDR notation, and subnets.

  What you'll learn: 
  * VPC architecture: Subnets, Route Tables, IGWs, and NAT Gateways.
  * Security: The difference between Security Groups (stateful) and NACLs (stateless).
  * Connecting VPCs and Services via Peering and Endpoints.
  * Global DNS routing with Route 53.
  * Content delivery networks via CloudFront.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  VPC (VIRTUAL PRIVATE CLOUD)
    A logically isolated section of the AWS Cloud where you can launch AWS resources in a virtual network that you define.

  CIDR BLOCK
    Classless Inter-Domain Routing. A method of allocating IP addresses (e.g., 10.0.0.0/16 gives you 65,536 IPs for your VPC).

  SUBNET
    A subdivision of your VPC's IP range, tied to a single Availability Zone.
    * Public Subnet: Has a route to the Internet Gateway.
    * Private Subnet: Does NOT have a route to the Internet Gateway.

  INTERNET GATEWAY (IGW)
    A highly available, managed AWS component that allows communication between your VPC and the internet.

  NAT GATEWAY (NETWORK ADDRESS TRANSLATION)
    A managed service placed in a public subnet that allows instances in a private subnet to initiate outbound traffic to the internet (e.g., to download patches) while preventing the internet from initiating connections to those instances.

  ROUTE TABLE
    Contains a set of rules (routes) that determine where network traffic from your subnets or gateways is directed.

  SECURITY GROUP
    A virtual, stateful firewall for your EC2 instances to control inbound and outbound traffic. (Stateful means if you allow an inbound request, the return outbound traffic is automatically allowed).

  NACL (NETWORK ACCESS CONTROL LIST)
    An optional layer of security for your VPC that acts as a stateless firewall at the subnet level. (Stateless means you must explicitly allow both inbound AND outbound traffic using numbered rules).

  VPC PEERING
    A networking connection between two VPCs that enables you to route traffic between them using private IPv4/IPv6 addresses. Not transitive (if A peers with B, and B peers with C, A cannot talk to C).

  VPC ENDPOINTS
    Enables private connections between your VPC and supported AWS services (like S3 or DynamoDB) without requiring an internet gateway, NAT device, or VPN.

  ROUTE 53
    AWS's highly available and scalable cloud DNS (Domain Name System) web service. Maps human-readable names (www.example.com) to IPs.

  CLOUDFRONT
    AWS's Content Delivery Network (CDN). It caches data, videos, APIs, and applications at Edge Locations globally to reduce latency to users.

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  VPC Architecture with Public/Private Subnets                           │
  │                                                                         │
  │    AWS Cloud                                                            │
  │    +-----------------------------------------------------------------------+│
  │    |  VPC (10.0.0.0/16)                                                    |│
  │    |                                                                       |│
  │    |  +-----------------------+                    +--------------------+  |│
  │    |  |  Availability Zone A  |                    | Internet Gateway   |<====> INTERNET│
  │    |  |                       |                    +--------+-----------+  |│
  │    |  |  [Public Subnet]      |                             |              |│
  │    |  |  (10.0.1.0/24)        |  (Route Table: 0.0.0.0/0 -> IGW)           |│
  │    |  |  +-----------------+  |                             |              |│
  │    |  |  |   NAT Gateway   |--------------------------------+              |│
  │    |  |  +-------+---------+  |                                            |│
  │    |  |          ^            |                                            |│
  │    |  |          |            |                                            |│
  │    |  |  [Private Subnet]     |                                            |│
  │    |  |  (10.0.2.0/24)        |  (Route Table: 0.0.0.0/0 -> NAT Gateway)   |│
  │    |  |  +-----------------+  |                                            |│
  │    |  |  |   EC2 Server    |--+ (Outbound only to internet for updates)    |│
  │    |  |  |   (Database)    |  |                                            |│
  │    |  |  +-----------------+  |                                            |│
  │    |  +-----------------------+                                            |│
  │    +-----------------------------------------------------------------------+│
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  Route 53 DNS Resolution Flow                                           │
  │                                                                         │
  │   1. User types www.example.com                                         │
  │              |                                                          │
  │              v                                                          │
  │   +----------------------+                                              │
  │   |  ISP DNS Resolver    |                                              │
  │   +----------+-----------+                                              │
  │              | 2. Where is example.com?                                 │
  │              v                                                          │
  │   +----------------------+                                              │
  │   | AWS Route 53 (DNS)   |                                              │
  │   | (Latency Policy)     |                                              │
  │   +----------+-----------+                                              │
  │              | 3. Returns IP based on lowest latency to User            │
  │              v                                                          │
  │      User Browser Connects                                              │
  │              |                                                          │
  │      +-------+-------+                                                  │
  │      |               |                                                  │
  │      v               v                                                  │
  │   [ALB in US]     [ALB in EU]                                           │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  Language: Bash

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // VPC Setup Overview via AWS CLI                                       │
  │                                                                          │
  │  # 1. Create a VPC                                                       │
  │  VPC_ID=$(aws ec2 create-vpc --cidr-block 10.0.0.0/16 --query Vpc.VpcId --output text)│
  │  echo "Created VPC: $VPC_ID"                                             │
  │                                                                          │
  │  # 2. Create a Subnet                                                    │
  │  SUBNET_ID=$(aws ec2 create-subnet --vpc-id $VPC_ID --cidr-block 10.0.1.0/24 --query Subnet.SubnetId --output text)│
  │  echo "Created Subnet: $SUBNET_ID"                                       │
  │                                                                          │
  │  # 3. Create an Internet Gateway                                         │
  │  IGW_ID=$(aws ec2 create-internet-gateway --query InternetGateway.InternetGatewayId --output text)│
  │  echo "Created IGW: $IGW_ID"                                             │
  │                                                                          │
  │  # 4. Attach IGW to VPC                                                  │
  │  aws ec2 attach-internet-gateway --vpc-id $VPC_ID --internet-gateway-id $IGW_ID│
  │                                                                          │
  │  # 5. Create a custom route table                                        │
  │  RT_ID=$(aws ec2 create-route-table --vpc-id $VPC_ID --query RouteTable.RouteTableId --output text)│
  │                                                                          │
  │  # 6. Create a route to the internet (0.0.0.0/0) pointing to the IGW     │
  │  aws ec2 create-route --route-table-id $RT_ID --destination-cidr-block 0.0.0.0/0 --gateway-id $IGW_ID│
  │                                                                          │
  │  # 7. Associate the Route Table with the Subnet (Making it a Public Subnet)│
  │  aws ec2 associate-route-table --subnet-id $SUBNET_ID --route-table-id $RT_ID│
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

  Language: Python

  ┌──────────────────────────────────────────────────────────────────────────┐
  │                                                                          │
  │  from aws_cdk import (                                                   │
  │      aws_ec2 as ec2,                                                     │
  │      App, Stack                                                          │
  │  )                                                                       │
  │  from constructs import Construct                                        │
  │                                                                          │
  │  class NetworkStack(Stack):                                              │
  │      def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:│
  │          super().__init__(scope, construct_id, **kwargs)                 │
  │                                                                          │
  │          # Create a VPC with 2 Availability Zones                        │
  │          # Automatically provisions Public subnets, Private subnets, and NAT Gateways│
  │          self.vpc = ec2.Vpc(                                             │
  │              self, "ProductionVPC",                                      │
  │              ip_addresses=ec2.IpAddresses.cidr("10.10.0.0/16"),          │
  │              max_azs=2,                                                  │
  │              # Create a NAT Gateway in each AZ for high availability     │
  │              nat_gateways=2,                                             │
  │              subnet_configuration=[                                      │
  │                  ec2.SubnetConfiguration(                                │
  │                      subnet_type=ec2.SubnetType.PUBLIC,                  │
  │                      name="Ingress-Public",                              │
  │                      cidr_mask=24                                        │
  │                  ),                                                      │
  │                  ec2.SubnetConfiguration(                                │
  │                      subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS,     │
  │                      name="Application-Private",                         │
  │                      cidr_mask=24                                        │
  │                  ),                                                      │
  │                  ec2.SubnetConfiguration(                                │
  │                      subnet_type=ec2.SubnetType.PRIVATE_ISOLATED,        │
  │                      name="Database-Isolated",                           │
  │                      cidr_mask=24 # No internet access whatsoever        │
  │                  )                                                       │
  │              ]                                                           │
  │          )                                                               │
  │                                                                          │
  │          # Add a VPC Endpoint for S3 so private subnets can talk to S3   │
  │          # without paying NAT Gateway data transfer charges              │
  │          self.vpc.add_gateway_endpoint(                                  │
  │              "S3Endpoint",                                               │
  │              service=ec2.GatewayVpcEndpointAwsService.S3                 │
  │          )                                                               │
  │                                                                          │
  │  app = App()                                                             │
  │  NetworkStack(app, "SecureProductionNetworkStack")                       │
  │  app.synth()                                                             │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  7. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: Explain the difference between a Security Group and a Network ACL (NACL).

  ANSWER:
    Security Groups operate at the instance level (EC2), are stateful (return traffic is automatically allowed), and evaluate all rules before deciding. NACLs operate at the subnet level, are stateless (inbound and outbound rules must be explicitly defined), and evaluate rules in numerical order (lowest to highest), stopping at the first match.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: What makes a subnet "Public" or "Private"?

  ANSWER:
    A subnet is public if its associated Route Table has a route directing internet-bound traffic (0.0.0.0/0) to an Internet Gateway (IGW). If it does not have this route (or routes via a NAT Gateway instead), it is private.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: You have an EC2 instance in a private subnet. How can it download a software patch from the internet securely?

  ANSWER:
    You must deploy a NAT Gateway in a public subnet. The private subnet's route table points internet traffic (0.0.0.0/0) to the NAT Gateway. The NAT Gateway translates the private IP to a public IP and routes it through the IGW, retrieving the patch without allowing inbound internet connections.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: Explain VPC Peering and the concept of transitivity.

  ANSWER:
    VPC Peering connects two VPCs securely using private IPs. It is strictly non-transitive. If VPC A is peered with B, and B is peered with C, A cannot communicate with C unless you explicitly create a peering connection directly between A and C.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: What is a VPC Endpoint and why is it useful?

  ANSWER:
    A VPC Endpoint allows instances in a private subnet to connect to AWS public services (like S3 or DynamoDB) using the internal AWS network, without traversing the public internet. It enhances security and saves money on NAT Gateway data transfer fees.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: What are some common Route 53 routing policies?

  ANSWER:
    * Simple: Standard DNS resolution.
    * Weighted: Routes traffic based on assigned weights (e.g., 80% to server A, 20% to server B).
    * Latency: Routes users to the AWS region that provides the lowest network latency.
    * Failover: Routes traffic to a primary server, and shifts to a secondary if health checks fail.
    * Geolocation: Routes traffic based on the physical location of the user.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q7: What is CloudFront and how does it reduce latency?

  ANSWER:
    CloudFront is a Content Delivery Network (CDN). It caches static assets (images, videos, HTML) at Edge Locations globally. When a user in Tokyo requests an image stored in a Virginia S3 bucket, CloudFront serves the cached copy from the Tokyo Edge Location, drastically reducing latency.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q8: Can two VPCs with overlapping CIDR blocks (e.g., both are 10.0.0.0/16) be peered?

  ANSWER:
    No. VPC Peering requires non-overlapping IP address ranges to properly route traffic between the networks.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q9: What is an Elastic IP (EIP)?

  ANSWER:
    An Elastic IP is a static, public IPv4 address designed for dynamic cloud computing. Unlike a standard public IP (which changes if an EC2 instance is stopped and started), an EIP remains associated with your AWS account until you explicitly release it.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q10: What is the 169.254.169.254 IP address used for in AWS?

  ANSWER:
    It is the local link address for the EC2 Instance Metadata Service (IMDS). An instance can query this IP via HTTP to retrieve data about itself (instance ID, region) and, crucially, to retrieve temporary IAM credentials if a role is attached.

────────────────────────────────────────────────────────────────────────────────
  8. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: Riddle 1

  I am stateless and strict. I guard the entire neighborhood (subnet), checking every packet that enters and leaves against a numbered list. What am I?

  SOLUTION:
    Network ACL (NACL).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 2: Riddle 2

  My instances are shy; they hide in private subnets. But when they want to talk to S3 without using the scary public internet or paying the NAT Gateway toll, they use me. What am I?

  SOLUTION:
    A VPC Gateway Endpoint.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 3: What's Wrong With This Architecture?

  Scenario: A junior developer deploys an internal HR database in an AWS VPC. To ensure nobody on the internet can access it, they place the DB in a Public Subnet but configure the Security Group to deny all inbound traffic (`0.0.0.0/0`) on port 3306.

  SOLUTION:
    Security Groups in AWS are implicit deny. You do not write "deny" rules in Security Groups (you can only write "allow" rules). Furthermore, putting a highly sensitive database in a Public Subnet is an architectural anti-pattern. It should be in a Private Subnet, relying on network isolation as the primary layer of defense, with Security Groups acting as the secondary layer.

────────────────────────────────────────────────────────────────────────────────
  9. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  * Security Breaches: Misconfigured Route Tables and Security Groups are the #1 cause of cloud data breaches. Exposing a database to `0.0.0.0/0` will result in automated bots attempting to brute-force the password within minutes.
  * Cost Management: Pushing terabytes of data from a private subnet to S3 via a NAT Gateway incurs massive data transfer charges. Utilizing a Gateway VPC Endpoint for S3 avoids the NAT Gateway entirely, often saving thousands of dollars.
  * Global User Experience: An application hosted in `us-east-1` (Virginia) will feel sluggish to users in Australia due to the speed of light. Using CloudFront and Route 53 Latency Routing ensures a snappy experience for users globally.

────────────────────────────────────────────────────────────────────────────────
  10. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

  -> File 100: AWS Compute (Deploying EC2 instances within these VPCs)
  -> File 104: AWS Security (IAM roles vs Network isolation)
  -> File 108: AWS Deployment IaC (Why using CloudFormation/CDK is better than clicking through the console for networking)

================================================================================
  END OF FILE 103
================================================================================
