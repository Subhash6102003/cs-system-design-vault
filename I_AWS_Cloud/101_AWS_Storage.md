================================================================================
  FILE 101: AWS STORAGE: S3, EBS, EFS, AND STORAGE GATEWAY
  Section: I - AWS Cloud Services
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  Storage in the cloud isn't just a hard drive attached to a server; it's a massive, distributed, highly durable ecosystem. AWS offers different storage services optimized for different use cases: object storage (S3) for web-scale unstructured data, block storage (EBS) for EC2 boot drives and databases, and file storage (EFS) for shared network drives.

  Prerequisites: Understanding of cloud fundamentals, compute resources (EC2).

  What you'll learn: 
  * S3 concepts, features, security, and storage classes.
  * The difference between Block, File, and Object storage.
  * EBS volume types and snapshots.
  * EFS usage for concurrent file access.
  * Hybrid cloud bridging with Storage Gateway.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  S3 (SIMPLE STORAGE SERVICE)
    An object storage service that offers industry-leading scalability, data availability, security, and performance.

  BUCKET
    A logical container in S3 where objects are stored. Bucket names must be globally unique across all of AWS.

  OBJECT
    A file and any metadata that describes that file, stored in a bucket.

  KEY
    The unique identifier (name) for an object within a bucket. (e.g., folder/image.png).

  S3 STORAGE CLASSES
    Different tiers of storage optimized for cost vs. access patterns.
    * Standard: Frequently accessed data (high throughput, low latency).
    * Standard-IA (Infrequent Access): Long-lived, less frequently accessed data (lower storage cost, but charges for retrieval).
    * One Zone-IA: Like IA but stored in only one AZ (cheapest, but less durable).
    * Glacier Instant/Flexible/Deep Archive: Cold storage for archiving and compliance. Retrieval times vary from milliseconds to 12 hours.
    * Intelligent-Tiering: Automatically moves data between frequent and infrequent tiers based on usage patterns to optimize costs.

  VERSIONING
    S3 feature that keeps multiple variants of an object in the same bucket, protecting against accidental deletion or overwrites.

  LIFECYCLE POLICIES
    Rules applied to an S3 bucket that automatically transition objects to cheaper storage classes over time or expire/delete them.

  PRE-SIGNED URLS
    A URL generated with AWS credentials that grants temporary access (download/upload) to an S3 object without requiring the user to have AWS credentials.

  EBS (ELASTIC BLOCK STORE)
    High-performance block storage volumes designed for use with EC2 instances. Think of it as a physical hard drive plugged into a virtual machine.
    * gp3/gp2: General purpose SSD.
    * io2/io1: Provisioned IOPS SSD for high-performance databases.
    * st1/sc1: HDD types for throughput-intensive or cold workloads.

  EBS SNAPSHOT
    A point-in-time backup of an EBS volume stored incrementally in S3.

  EFS (ELASTIC FILE SYSTEM)
    A simple, serverless, set-and-forget, elastic file system. It acts as a managed NFS (Network File System) that can be mounted by hundreds of EC2 instances simultaneously.

  AWS STORAGE GATEWAY
    A hybrid cloud storage service that gives on-premises applications access to virtually unlimited cloud storage using standard storage protocols (NFS, SMB, iSCSI).

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  S3 Storage Classes Lifecycle                                           │
  │                                                                         │
  │                    Lifecycle Policy Automation                          │
  │      ========================================================           │
  │                                                                         │
  │      [ Day 0: Object Created ]                                          │
  │              |                                                          │
  │              | (Standard Storage - $0.023/GB)                           │
  │              v                                                          │
  │      +---------------+                                                  │
  │      |  S3 Standard  | ----(Frequently Accessed)                        │
  │      +---------------+                                                  │
  │              |                                                          │
  │              | (After 30 days of infrequent access)                     │
  │              v                                                          │
  │      +---------------+                                                  │
  │      | S3 Standard-IA| ----(Access fees apply, cheaper storage)         │
  │      +---------------+                                                  │
  │              |                                                          │
  │              | (After 90 days, data no longer needed quickly)           │
  │              v                                                          │
  │      +---------------+                                                  │
  │      |  S3 Glacier   | ----(Archive - Hours to retrieve, very cheap)    │
  │      |   Flexible    |                                                  │
  │      +---------------+                                                  │
  │              |                                                          │
  │              | (After 365 days, compliance archive only)                │
  │              v                                                          │
  │      +---------------+                                                  │
  │      |S3 Deep Archive| ----(Long-term Archive - Lowest cost)            │
  │      +---------------+                                                  │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  EBS vs EFS vs S3 Comparison Matrix                                     │
  │                                                                         │
  │  +-------------------+--------------------+--------------------+--------------------+│
  │  | Feature           | EBS (Block)        | EFS (File)         | S3 (Object)        |│
  │  +-------------------+--------------------+--------------------+--------------------+│
  │  | Access Pattern    | Attached to 1 EC2* | Mounted by many EC2| Web APIs (HTTP)    |│
  │  | Performance       | High IOPS, low lat.| High throughput    | High scale/thruput |│
  │  | Data Structure    | Raw disk blocks    | File tree structure| Flat objects/keys  |│
  │  | Primary Use Case  | OS boot drives, DBs| Shared web hosting,| Media, backups,    |│
  │  |                   |                    | analytics, CMS     | static websites    |│
  │  | Persistence       | Bound to AZ        | Multi-AZ           | Global (Regional)  |│
  │  +-------------------+--------------------+--------------------+--------------------+│
  │  * io1/io2/gp3 support Multi-Attach, but generally EBS is 1:1 with an EC2 instance.│
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  Language: Python

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Generating an S3 Pre-signed URL (Python/Boto3)                       │
  │  // This script demonstrates how to generate a temporary link that allows│
  │  // a user to download a private file from S3.                           │
  │                                                                          │
  │  import boto3                                                            │
  │  from botocore.exceptions import ClientError                             │
  │  import logging                                                          │
  │                                                                          │
  │  def create_presigned_url(bucket_name, object_name, expiration=3600):    │
  │      """                                                                 │
  │      Generate a presigned URL to share an S3 object                      │
  │                                                                          │
  │      :param bucket_name: string                                          │
  │      :param object_name: string                                          │
  │      :param expiration: Time in seconds for the presigned URL to remain valid│
  │      :return: Presigned URL as string. If error, returns None.           │
  │      """                                                                 │
  │      # Generate a presigned URL for the S3 client                        │
  │      s3_client = boto3.client('s3')                                      │
  │      try:                                                                │
  │          response = s3_client.generate_presigned_url('get_object',       │
  │                                                      Params={'Bucket': bucket_name,│
  │                                                              'Key': object_name},│
  │                                                      ExpiresIn=expiration)│
  │      except ClientError as e:                                            │
  │          logging.error(e)                                                │
  │          return None                                                     │
  │                                                                          │
  │      # The response contains the presigned URL                           │
  │      return response                                                     │
  │                                                                          │
  │  # Usage                                                                 │
  │  url = create_presigned_url('my-secure-bucket', 'private-reports/q1_financials.pdf')│
  │  print(f"Temporary Download Link (valid for 1hr): {url}")                │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

  Language: Python

  ┌──────────────────────────────────────────────────────────────────────────┐
  │                                                                          │
  │  import boto3                                                            │
  │  import json                                                             │
  │                                                                          │
  │  def setup_production_s3_bucket(bucket_name: str, region: str = 'us-east-1'):│
  │      s3_client = boto3.client('s3', region_name=region)                  │
  │                                                                          │
  │      try:                                                                │
  │          # 1. Create the bucket                                          │
  │          print(f"Creating bucket: {bucket_name}")                        │
  │          if region == 'us-east-1':                                       │
  │              s3_client.create_bucket(Bucket=bucket_name)                 │
  │          else:                                                           │
  │              s3_client.create_bucket(                                    │
  │                  Bucket=bucket_name,                                     │
  │                  CreateBucketConfiguration={'LocationConstraint': region}│
  │              )                                                           │
  │                                                                          │
  │          # 2. Enable Block Public Access (Security Best Practice)        │
  │          print("Enabling Block Public Access...")                        │
  │          s3_client.put_public_access_block(                              │
  │              Bucket=bucket_name,                                         │
  │              PublicAccessBlockConfiguration={                            │
  │                  'BlockPublicAcls': True,                                │
  │                  'IgnorePublicAcls': True,                               │
  │                  'BlockPublicPolicy': True,                              │
  │                  'RestrictPublicBuckets': True                           │
  │              }                                                           │
  │          )                                                               │
  │                                                                          │
  │          # 3. Enable Versioning (Data Protection)                        │
  │          print("Enabling Versioning...")                                 │
  │          s3_client.put_bucket_versioning(                                │
  │              Bucket=bucket_name,                                         │
  │              VersioningConfiguration={'Status': 'Enabled'}               │
  │          )                                                               │
  │                                                                          │
  │          # 4. Apply a Lifecycle Policy (Cost Optimization)               │
  │          # Move to Standard-IA after 30 days, Glacier after 90 days.     │
  │          print("Applying Lifecycle Policy...")                           │
  │          lifecycle_config = {                                            │
  │              'Rules': [                                                  │
  │                  {                                                       │
  │                      'ID': 'MoveOldDataToArchive',                       │
  │                      'Filter': {'Prefix': ''}, # Applies to all objects  │
  │                      'Status': 'Enabled',                                │
  │                      'Transitions': [                                    │
  │                          {'Days': 30, 'StorageClass': 'STANDARD_IA'},    │
  │                          {'Days': 90, 'StorageClass': 'GLACIER'}         │
  │                      ],                                                  │
  │                      'NoncurrentVersionTransitions': [                   │
  │                          {'NoncurrentDays': 30, 'StorageClass': 'GLACIER'}│
  │                      ]                                                   │
  │                  }                                                       │
  │              ]                                                           │
  │          }                                                               │
  │          s3_client.put_bucket_lifecycle_configuration(                   │
  │              Bucket=bucket_name,                                         │
  │              LifecycleConfiguration=lifecycle_config                     │
  │          )                                                               │
  │                                                                          │
  │          print(f"Successfully provisioned secure, cost-optimized bucket: {bucket_name}")│
  │                                                                          │
  │      except Exception as e:                                              │
  │          print(f"Error provisioning bucket: {str(e)}")                   │
  │                                                                          │
  │  if __name__ == "__main__":                                              │
  │      # Ensure this bucket name is globally unique!                       │
  │      setup_production_s3_bucket("my-corp-archive-bucket-998877")         │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  7. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: Explain the S3 consistency model.

  ANSWER:
    S3 provides strong read-after-write consistency for PUTs and DELETEs of objects in an S3 bucket in all AWS Regions. This means if you write a new object or overwrite an existing one, a subsequent read will immediately return the latest version.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: What is the difference between EBS and EFS?

  ANSWER:
    EBS is block storage meant to be attached to a single EC2 instance (like a local hard drive), restricted to a single Availability Zone. EFS is file storage (NFS) designed to be mounted by hundreds or thousands of EC2 instances simultaneously across multiple Availability Zones.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: How can you protect against accidental deletion of objects in S3?

  ANSWER:
    Enable S3 Versioning, which keeps previous versions of an object instead of deleting them outright. For highly sensitive data, also enable MFA (Multi-Factor Authentication) Delete, which requires a physical token code to permanently delete an object.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: Your application serves static assets (images, CSS) to users globally, but you want to keep costs extremely low. Where should you store these assets?

  ANSWER:
    Store them in Amazon S3 and serve them via Amazon CloudFront (CDN). S3 is highly scalable and cheap for object storage, and CloudFront caches the assets at Edge Locations globally.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: You have compliance data that must be kept for 7 years. It is almost never accessed, but if it is, you can wait 12 hours to retrieve it. What is the most cost-effective storage class?

  ANSWER:
    S3 Glacier Deep Archive. It offers the absolute lowest storage cost for data that is rarely accessed and where retrieval times of 12 hours are acceptable.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: Can you mount an EBS volume to multiple EC2 instances at the same time?

  ANSWER:
    Standard gp2/gp3 volumes cannot. However, AWS introduced "EBS Multi-Attach" for provisioned IOPS io1/io2 volumes, allowing attachment to up to 16 instances in the same Availability Zone. If you need multi-AZ shared access, you must use EFS.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q7: How does AWS Storage Gateway work?

  ANSWER:
    It is a hybrid cloud service deployed as a virtual machine on-premises. It exposes standard storage protocols (like NFS or iSCSI) to local servers, but seamlessly backs up and caches that data into AWS S3 or EBS behind the scenes, bridging on-premises environments with cloud storage.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q8: What are the three types of Server-Side Encryption (SSE) supported by S3?

  ANSWER:
    1. SSE-S3: AWS manages the data and master keys completely.
    2. SSE-KMS: AWS manages the data key, but you manage the master key via AWS Key Management Service (giving you audit trails).
    3. SSE-C: You provide and manage your own encryption keys; AWS only performs the encryption/decryption math.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q9: What happens to an EBS volume when an EC2 instance is terminated?

  ANSWER:
    By default, the Root EBS volume is deleted when the instance terminates (the DeleteOnTermination flag is true). Any additionally attached data volumes are preserved. You can change this behavior in the instance configuration.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q10: What is S3 Intelligent-Tiering?

  ANSWER:
    It is a storage class that automatically optimizes storage costs by moving data to the most cost-effective access tier (Frequent, Infrequent, Archive) based on access frequency, without performance impact or operational overhead.

────────────────────────────────────────────────────────────────────────────────
  8. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: Riddle 1

  I am locked to a single Availability Zone. If my EC2 instance dies, I live on, but I cannot easily move across the country. What am I?

  SOLUTION:
    An EBS Volume.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 2: Riddle 2

  My name must be globally unique, like a domain name. I can hold exabytes of data, but I am terrible at running an operating system. What am I?

  SOLUTION:
    An S3 Bucket.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 3: What's Wrong With This Logic?

  Scenario: A developer is building a high-traffic e-commerce site. The web servers run on an Auto Scaling Group of EC2 instances. To ensure all web servers have access to the exact same uploaded product images, the developer attaches a massive EBS volume to one EC2 instance, and shares it over the network to the others using custom scripts.

  SOLUTION:
    This is a terrible anti-pattern. EBS is not designed to be shared over a network via custom scripts—it creates a massive single point of failure and a network bottleneck. The developer should either use EFS (which natively supports multi-instance mounting) or, better yet, upload all images directly to S3 and serve them via CloudFront.

────────────────────────────────────────────────────────────────────────────────
  9. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  * Disaster Recovery: EBS Snapshots stored in S3 are the backbone of cloud backups. If an AZ goes down or an instance is corrupted, launching a new instance from a recent snapshot takes minutes, saving businesses from catastrophic data loss.
  * Cost Management: Storing petabytes of logs in S3 Standard costs thousands of dollars a month. Applying a simple 30-day lifecycle rule to move them to Glacier Deep Archive can cut the storage bill by 90% almost instantly.
  * Decoupled Architecture: Using S3 pre-signed URLs allows massive file uploads (like 4K video) to go directly from the user's browser to S3, bypassing the web servers entirely. This prevents the EC2 instances from being bottlenecked by large file transfers.

────────────────────────────────────────────────────────────────────────────────
  10. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

  -> File 100: AWS Compute (Understanding EC2 which utilizes EBS for boot drives)
  -> File 104: AWS Security (Deep dive into KMS, which powers S3 and EBS encryption)
  -> File 102: AWS Databases (Contrast raw storage (S3/EBS) with structured data storage (RDS/DynamoDB))

================================================================================
  END OF FILE 101
================================================================================
