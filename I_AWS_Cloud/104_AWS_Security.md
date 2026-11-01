================================================================================
  FILE 104: AWS SECURITY SERVICES
  Section: I - AWS Cloud Services
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  AWS Security: IAM, KMS, Secrets Manager, and WAF
  Security in the cloud is "Job

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  **IAM (IDENTITY AND ACCESS MANAGEMENT)
    ** A web service that helps you securely control access to AWS resources. You use IAM to control who is authenticated (signed in) and authorized (has permissions) to use resources.

  **IAM POLICY
    ** A JSON document that defines permissions. Policies can be attached to Users, Groups, or Roles. Follows the structure: Effect, Action, Resource, Condition.

  **IAM ROLE
    ** An identity with permission policies that determine what the identity can and cannot do. Unlike a user, a role does not have long-term credentials (passwords or access keys). It is meant to be assumed by an AWS service (like EC2 or Lambda) or a federated user.

  **PRINCIPLE OF LEAST PRIVILEGE
    ** A core security concept stating that a user, program, or system should have only the bare minimum privileges necessary to perform its function.

  **AWS STS (SECURITY TOKEN SERVICE)
    ** A web service that enables you to request temporary, limited-privilege credentials for IAM users or for users that you authenticate (federated users). Utilizes the AssumeRole API.

  **KMS (KEY MANAGEMENT SERVICE)
    ** A managed service that makes it easy for you to create and manage cryptographic keys and control their use across a wide range of AWS services.

  **CMK (CUSTOMER MASTER KEY)
    ** The primary logical key resource in KMS, used to encrypt and decrypt data keys.

  **ENVELOPE ENCRYPTION
    ** The practice of encrypting plaintext data with a data key, and then encrypting the data key under another key (the CMK). AWS KMS operates on this principle.

  **SECRETS MANAGER
    ** A service that helps you protect secrets needed to access your applications, services, and IT resources. It enables you to easily rotate, manage, and retrieve database credentials, API keys, and other secrets through their lifecycle.

  **AWS WAF (WEB APPLICATION FIREWALL)
    ** Helps protect web applications or APIs against common web exploits and bots (e.g., SQL injection, Cross-Site Scripting) that may affect availability, compromise security, or consume excessive resources.

  **AWS SHIELD
    ** A managed Distributed Denial of Service (DDoS) protection service. Standard is free and on by default; Advanced provides enhanced protections and cost protection against massive attacks.

  **GUARDDUTY
    ** A threat detection service that continuously monitors for malicious activity and unauthorized behavior to protect your AWS accounts and workloads (uses ML to detect anomalies).

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  IAM Policy Evaluation Flowchart                                        │
  │                                                                         │
  │         Request Made (e.g., DeleteS3Bucket)                             │
  │                  |                                                      │
  │                  v                                                      │
  │   +-------------------------------------+                               │
  │   |  Are there any explicit DENYs?      |                               │
  │   |  (In IAM, SCP, or Resource Policy)  |                               │
  │   +-------------------------------------+                               │
  │          | YES                      | NO                                │
  │          v                          |                                   │
  │   [ DENY EVALUATION ]               v                                   │
  │          |               +-----------------------------------+          │
  │          |               | Are there any explicit ALLOWs?    |          │
  │          |               | (In IAM or Resource Policy)       |          │
  │          |               +-----------------------------------+          │
  │          |                       | YES               | NO               │
  │          v                       v                   v                  │
  │   +---------------+      +---------------+   +---------------+          │
  │   |  ACCESS       |      |  ACCESS       |   |  ACCESS       |          │
  │   |  DENIED       |      |  ALLOWED      |   |  DENIED       |          │
  │   +---------------+      +---------------+   +---------------+          │
  │     (Explicit)             (Explicit)          (Implicit Default)       │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  KMS Envelope Encryption Process                                        │
  │                                                                         │
  │   1. Application asks KMS for a Data Key using CMK.                     │
  │   2. KMS returns Plaintext Data Key + Encrypted Data Key.               │
  │                                                                         │
  │   +--------------+       +-------------------+      +-------------------+│
  │   |  Plaintext   |   +   | Plaintext Data Key|  ->  |  Encrypted Data   |│
  │   |  Data (File) |       | (Used by App)     |      |  (Ciphertext)     |│
  │   +--------------+       +-------------------+      +-------------------+│
  │                                                            |            │
  │   3. App drops plaintext key from memory.                  v            │
  │   4. App stores Encrypted Data alongside Encrypted Data Key.            │
  │                                                                         │
  │   STORAGE (S3/EBS):                                                     │
  │   +-----------------------------------------------------------------+   │
  │   | [ Encrypted Data Key ] + [ Encrypted Data (Ciphertext) ]        |   │
  │   +-----------------------------------------------------------------+   │
  │                                                                         │
  │   5. To decrypt, App sends Encrypted Data Key to KMS, KMS uses CMK to   │
  │      return Plaintext Data Key. App decrypts the data locally.          │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: json]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // IAM Policy Structure (JSON)                                          │
  │                                                                          │
  │  {                                                                       │
  │    "Version": "2012-10-17",                                              │
  │    "Statement": [                                                        │
  │      {                                                                   │
  │        "Sid": "AllowS3ReadWithMFA",                                      │
  │        "Effect": "Allow",                                                │
  │        "Action": [                                                       │
  │          "s3:GetObject"                                                  │
  │        ],                                                                │
  │        "Resource": [                                                     │
  │          "arn:aws:s3:::my-secure-bucket/financials/*"                    │
  │        ],                                                                │
  │        "Condition": {                                                    │
  │          "Bool": {                                                       │
  │            "aws:MultiFactorAuthPresent": "true"                          │
  │          }                                                               │
  │        }                                                                 │
  │      }                                                                   │
  │    ]                                                                     │
  │  }                                                                       │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: python]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │                                                                          │
  │  import boto3                                                            │
  │  from botocore.exceptions import ClientError                             │
  │  import json                                                             │
  │  import logging                                                          │
  │                                                                          │
  │  logger = logging.getLogger()                                            │
  │                                                                          │
  │  def get_third_party_api_key(secret_name: str, region_name: str = "us-east-1") -> str:│
  │      """                                                                 │
  │      Retrieves an API key from AWS Secrets Manager safely.               │
  │      """                                                                 │
  │      # Create a Secrets Manager client                                   │
  │      session = boto3.session.Session()                                   │
  │      client = session.client(                                            │
  │          service_name='secretsmanager',                                  │
  │          region_name=region_name                                         │
  │      )                                                                   │
  │                                                                          │
  │      try:                                                                │
  │          get_secret_value_response = client.get_secret_value(            │
  │              SecretId=secret_name                                        │
  │          )                                                               │
  │      except ClientError as e:                                            │
  │          error_code = e.response['Error']['Code']                        │
  │          logger.error(f"Failed to retrieve secret. Reason: {error_code}")│
  │          # Handle specific exceptions like ResourceNotFoundException     │
  │          raise e                                                         │
  │      else:                                                               │
  │          # Secrets Manager decrypts the secret value using the associated KMS CMK│
  │          if 'SecretString' in get_secret_value_response:                 │
  │              secret_dict = json.loads(get_secret_value_response['SecretString'])│
  │              return secret_dict.get('api_key')                           │
  │          else:                                                           │
  │              # Handle binary secrets if applicable                       │
  │              decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary'])│
  │              return decoded_binary_secret                                │
  │                                                                          │
  │  if __name__ == "__main__":                                              │
  │      # Example usage:                                                    │
  │      # my_key = get_third_party_api_key("prod/Stripe/ApiKey")            │
  │      pass                                                                │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  7. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: Explain the Principle of Least Privilege in the context of IAM.

  ANSWER:
    It means granting an entity (user, group, or role) only the exact permissions needed to perform its required tasks, and nothing more. If an EC2 instance only needs to read from an S3 bucket, it should have an s3:GetObject policy for that specific bucket ARN, not s3:* or AdministratorAccess.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: What is the difference between an Identity-based policy and a Resource-based policy?

  ANSWER:
    Identity-based policies are attached to IAM users, groups, or roles and dictate what that identity can do. Resource-based policies are attached directly to a resource (like an S3 Bucket Policy or KMS Key Policy) and dictate who can access that resource.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: How do you grant an EC2 instance access to an S3 bucket securely?

  ANSWER:
    You create an IAM Role with a policy granting S3 access. You attach this Role to an EC2 Instance Profile, and assign that profile to the EC2 instance. The software on EC2 retrieves temporary credentials automatically via the instance metadata service. You NEVER put long-term access keys on the instance.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: What is AWS STS and what does AssumeRole do?

  ANSWER:
    STS (Security Token Service) provides temporary, short-lived security credentials. AssumeRole is an API call where an identity requests STS to temporarily take on the permissions of a specified IAM Role, returning temporary Access Key, Secret Key, and Session Token.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: Explain Envelope Encryption in AWS KMS.

  ANSWER:
    It is a performance and security optimization. Instead of sending large amounts of data to KMS to be encrypted, KMS generates a small "Data Key". The data is encrypted locally using the plaintext data key. The data key itself is encrypted using the KMS Customer Master Key (CMK). The encrypted data and encrypted data key are stored together.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: What is the difference between AWS Secrets Manager and AWS Systems Manager Parameter Store?

  ANSWER:
    Both store secrets, but Secrets Manager natively supports automatic password rotation (e.g., changing an RDS password every 30 days automatically using a Lambda function) and cross-account access easily. Parameter Store is simpler, free for standard parameters, but lacks native automatic rotation.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q7: An IAM policy has an explicit Allow for S3 access, but a Resource-based S3 bucket policy has an explicit Deny for the same user. Does the user get access?

  ANSWER:
    No. In IAM evaluation logic, an explicit Deny ALWAYS overrides any explicit Allow.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q8: What does AWS WAF protect against?

  ANSWER:
    WAF is a Web Application Firewall that operates at Layer 7. It protects against common web exploits like SQL Injection (SQLi), Cross-Site Scripting (XSS), bad bots, and rate-limits IPs making too many requests. It attaches to ALBs, API Gateway, or CloudFront.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q9: What is AWS GuardDuty?

  ANSWER:
    GuardDuty is an intelligent threat detection service. It continuously analyzes VPC Flow Logs, CloudTrail events, and DNS logs using machine learning to identify anomalous behavior, like a compromised EC2 instance communicating with a known cryptocurrency mining pool.

────────────────────────────────────────────────────────────────────────────────
  8. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: Riddle 1

  *I am not a user, and I have no password. Machines and services wear me like a mask to gain temporary superpowers. What am I?*

  SOLUTION:
    An IAM Role.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 2: Riddle 2

  *I lock the box containing your data, but I am too small to lock the data myself. Instead, I lock the smaller key that locked the data. What am I?*

  SOLUTION:
    A KMS Customer Master Key (CMK) / Envelope Encryption.

────────────────────────────────────────────────────────────────────────────────
  9. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  *   Preventing Financial Ruin: A leaked IAM access key with AdministratorAccess can bankrupt a startup in hours via crypto-mining attacks. Enforcing Least Privilege limits the blast radius of compromised keys.
  *   Compliance (HIPAA/SOC2): Regulators require data to be encrypted "at rest." Understanding KMS Envelope encryption is mandatory to prove to auditors that customer data (like healthcare records) is secure.
  *   Operational Security: Manually rotating database passwords requires coordinating application downtime and causes outages if done wrong. Secrets Manager automates this lifecycle entirely, keeping the system secure without human intervention.
  ---

================================================================================
  END OF FILE 104
================================================================================
