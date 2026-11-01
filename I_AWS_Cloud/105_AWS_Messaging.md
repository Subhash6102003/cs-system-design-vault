================================================================================
  FILE 105: AWS MESSAGING & EVENT-DRIVEN ARCHITECTURE
  Section: I - AWS Cloud Services
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  AWS Messaging: SQS, SNS, EventBridge, and Kinesis
  Modern cloud architectures rely heavily on decoupled, asynchronous communication. Instead of microservices calling each other synchronously (and failing if one is down), they use message brokers and event buses. This file covers how to decouple systems using queues (SQS), pub/sub notifications (SNS), event routers (EventBridge), and real-time data streams (Kinesis).

  Prerequisites: Understanding of microservices, Lambda (File 100), and basic architecture.
  What you'll learn:
  *   Decoupling applications using SQS.
  *   Standard vs. FIFO queues.
  *   Pub/Sub patterns with SNS.
  *   Event-Driven architecture using EventBridge.
  *   Streaming data with Kinesis.
  *   The Fan-out architectural pattern.

  ---

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  **SQS (SIMPLE QUEUE SERVICE)
    ** A fully managed message queuing service that enables you to decouple and scale microservices, distributed systems, and serverless applications. Messages are "pulled" (polled) by consumers.

  **STANDARD QUEUE
    ** Offers maximum throughput, best-effort ordering, and at-least-once delivery (meaning duplicates can occasionally occur).

  **FIFO QUEUE (FIRST-IN-FIRST-OUT)
    ** Guarantees that messages are processed exactly once, in the exact order that they are sent. Has lower throughput than Standard.

  **VISIBILITY TIMEOUT
    ** The period of time during which SQS prevents other consumers from receiving and processing a message that is currently being processed by one consumer. If the consumer fails to process it in time, it reappears in the queue.

  **DLQ (DEAD LETTER QUEUE)
    ** A queue where other queues can send messages that cannot be processed successfully after a certain number of retries.

  **SNS (SIMPLE NOTIFICATION SERVICE)
    ** A fully managed pub/sub messaging service. A publisher sends a message to a "Topic", and SNS "pushes" that message to all subscribers (SQS queues, Lambda, HTTP endpoints, SMS, Email) immediately.

  **FAN-OUT PATTERN
    ** An architecture where an SNS topic has multiple SQS queues subscribed to it. One message published to SNS is fanned out to multiple queues for parallel processing by different microservices.

  **EVENTBRIDGE
    ** A serverless event bus that makes it easy to connect applications together using data from your own apps, SaaS apps, and AWS services. Uses rules to route events to targets.

  **KINESIS DATA STREAMS
    ** A massively scalable and durable real-time data streaming service. Unlike SQS (where messages are deleted after processing), Kinesis streams retain data for a period (hours to days), allowing multiple consumers to read the same stream simultaneously.

  **KINESIS DATA FIREHOSE
    ** The easiest way to reliably load streaming data into data lakes, data stores, and analytics services (like S3 or Redshift) in near-real-time.

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  SNS + SQS Fan-Out Architecture                                         │
  │                                                                         │
  │                                  +-------------------+                  │
  │                                  |    Order API      |                  │
  │                                  |   (Publisher)     |                  │
  │                                  +---------+---------+                  │
  │                                            |                            │
  │                                  1. Publishes "OrderCreated"            │
  │                                            v                            │
  │                                  +-------------------+                  │
  │                                  |     SNS Topic     |                  │
  │                                  |  "OrdersTopic"    |                  │
  │                                  +----+---------+----+                  │
  │                                       |         |                       │
  │                    2. Pushes copy     |         |    2. Pushes copy     │
  │                    of message         v         v    of message         │
  │              +------------------------+         +------------------------+│
  │              |      SQS Queue         |         |      SQS Queue         |│
  │              | "InventoryUpdateQ"     |         | "ShippingLabelQ"       |│
  │              +----------+-------------+         +----------+-------------+│
  │                         |                                  |            │
  │              3. Polls   v                                  v  3. Polls  │
  │              +------------------------+         +------------------------+│
  │              |  Inventory Service     |         |   Shipping Service     |│
  │              |  (Updates Stock)       |         |   (Prints Label)       |│
  │              +------------------------+         +------------------------+│
  │              (Both services process the same event asynchronously, at their own pace)│
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: python]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // SNS Publish and SQS Consumer (Python/Boto3)                          │
  │                                                                          │
  │  import boto3                                                            │
  │  import json                                                             │
  │                                                                          │
  │  # --- PUBLISHER ---                                                     │
  │  def publish_order(sns_topic_arn, order_data):                           │
  │      sns = boto3.client('sns', region_name='us-east-1')                  │
  │                                                                          │
  │      response = sns.publish(                                             │
  │          TopicArn=sns_topic_arn,                                         │
  │          Message=json.dumps(order_data),                                 │
  │          Subject='New Order Received'                                    │
  │      )                                                                   │
  │      print(f"Published to SNS: MessageId {response['MessageId']}")       │
  │                                                                          │
  │  # --- CONSUMER ---                                                      │
  │  def process_queue(sqs_queue_url):                                       │
  │      sqs = boto3.client('sqs', region_name='us-east-1')                  │
  │                                                                          │
  │      # 1. Long Poll for messages (WaitTimeSeconds > 0)                   │
  │      response = sqs.receive_message(                                     │
  │          QueueUrl=sqs_queue_url,                                         │
  │          MaxNumberOfMessages=1,                                          │
  │          WaitTimeSeconds=10                                              │
  │      )                                                                   │
  │                                                                          │
  │      messages = response.get('Messages', [])                             │
  │      for msg in messages:                                                │
  │          receipt_handle = msg['ReceiptHandle']                           │
  │          body = json.loads(msg['Body'])                                  │
  │                                                                          │
  │          print(f"Processing Order: {body}")                              │
  │                                                                          │
  │          # 2. Delete message after successful processing                 │
  │          # (If this fails, Visibility Timeout expires and message reappears in queue)│
  │          sqs.delete_message(                                             │
  │              QueueUrl=sqs_queue_url,                                     │
  │              ReceiptHandle=receipt_handle                                │
  │          )                                                               │
  │          print("Message processed and deleted from queue.")              │
  │                                                                          │
  │  # Usage:                                                                │
  │  # publish_order('arn:aws:sns:us-east-1:123:Orders', {"id": 101, "item": "Laptop"})│
  │  # process_queue('https://sqs.us-east-1.amazonaws.com/123/InventoryQ')   │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: yaml]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │                                                                          │
  │  AWSTemplateFormatVersion: '2010-09-09'                                  │
  │  Resources:                                                              │
  │    # 1. Create the Dead Letter Queue                                     │
  │    MyDeadLetterQueue:                                                    │
  │      Type: AWS::SQS::Queue                                               │
  │      Properties:                                                         │
  │        QueueName: my-application-dlq                                     │
  │        MessageRetentionPeriod: 1209600 # 14 days (Max allowed to give devs time to debug)│
  │                                                                          │
  │    # 2. Create the Main Queue and attach the DLQ                         │
  │    MyMainQueue:                                                          │
  │      Type: AWS::SQS::Queue                                               │
  │      Properties:                                                         │
  │        QueueName: my-application-queue                                   │
  │        VisibilityTimeout: 30 # Must be greater than Lambda execution time│
  │        RedrivePolicy:                                                    │
  │          deadLetterTargetArn: !GetAtt MyDeadLetterQueue.Arn              │
  │          # If the message fails to process 3 times, move it to the DLQ   │
  │          maxReceiveCount: 3                                              │
  │                                                                          │
  │  Outputs:                                                                │
  │    MainQueueUrl:                                                         │
  │      Value: !Ref MyMainQueue                                             │
  │    DLQUrl:                                                               │
  │      Value: !Ref MyDeadLetterQueue                                       │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  7. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: What is the difference between SQS and SNS?

  ANSWER:
    SNS is a push-based pub/sub service; it actively pushes messages to subscribers immediately. SQS is a pull-based queuing service; consumers must actively poll the queue to retrieve messages. They are often used together in a fan-out pattern.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: Explain the SQS Visibility Timeout.

  ANSWER:
    When a consumer pulls a message from SQS, the message remains in the queue but becomes "invisible" to other consumers for the duration of the visibility timeout. If the consumer deletes the message before the timeout expires, it's gone. If the consumer crashes and the timeout expires, the message becomes visible again for another consumer to retry.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: What is a Dead Letter Queue (DLQ) and why is it important?

  ANSWER:
    A DLQ is a secondary queue used to store messages that could not be processed successfully by a consumer after a specified number of retries (e.g., due to a bug in the code parsing the payload). It prevents "poison pill" messages from infinitely blocking the queue.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: When would you choose Kinesis Data Streams over SQS?

  ANSWER:
    You use Kinesis when you need real-time routing of massive data streams (like website clickstreams or IoT telemetry), when you need multiple consumers reading the *same* data simultaneously, or when you need strict ordering at high scale. SQS is better for standard task decoupling where a message should be processed once and then deleted.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: What is SQS Long Polling?

  ANSWER:
    Standard polling returns immediately, even if the queue is empty, which wastes CPU cycles and incurs AWS API costs. Long Polling (WaitTimeSeconds > 0) keeps the connection open for up to 20 seconds waiting for a message to arrive, drastically reducing API calls and latency.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: How does an SNS + SQS Fan-Out pattern work?

  ANSWER:
    A publisher sends a single message to an SNS Topic. Multiple SQS queues are subscribed to that topic. SNS immediately pushes a copy of the message into each queue. This allows multiple independent microservices to process the exact same event asynchronously at their own pace.

────────────────────────────────────────────────────────────────────────────────
  8. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: Riddle 1

  *I am a megaphone. When you shout into me, everyone who subscribed to my channel hears you instantly, whether they are a Lambda, a Queue, or a cellphone. What am I?*

  SOLUTION:
    Amazon SNS.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 2: Riddle 2

  *I am a waiting room. I hold onto tasks until a worker is ready to ask for them. But if a worker takes a task and dies before finishing it, I put the task back in the room. What am I?*

  SOLUTION:
    Amazon SQS.

────────────────────────────────────────────────────────────────────────────────
  9. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  *   System Resilience: If Service A directly calls Service B via HTTP (synchronous), and Service B crashes, Service A also fails (cascading failure). If Service A puts a message in SQS, and Service B crashes, the message safely waits in the queue. When Service B reboots, it catches up. This is the essence of decoupled microservices.
  *   Peak Load Handling: During a flash sale, thousands of orders per second might overwhelm a database. Putting those orders into an SQS queue acts as a "shock absorber." The database consumes them from the queue at a steady, manageable rate, preventing crashes.
  *   Real-time Analytics: Kinesis allows companies like Netflix to ingest millions of telemetry events per second from user TVs, feeding them into machine learning models to adjust video bitrate in real-time.
  ---

================================================================================
  END OF FILE 105
================================================================================
