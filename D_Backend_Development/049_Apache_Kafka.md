================================================================================
  FILE 049: Apache Kafka & Distributed Event Streaming
  Section: D - Backend Development
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  Apache Kafka is the distributed event store and stream-processing platform that
  serves as the nervous system for modern high-scale architectures (LinkedIn, Uber,
  Netflix). Rather than operating as a traditional message queue (like RabbitMQ),
  Kafka is fundamentally an append-only distributed commit log. This guide deconstructs
  Kafka's storage internals, partition rebalancing, Zero-Copy data transfer, exactly-once
  semantics (EOS), and producer-consumer architectures.

  Prerequisites: File 005 (Operating System Page Cache), File 006 (Networking Sockets).
  What You'll Learn: Log segments, OS page cache utilization, sendfile() system call,
  partition assignment strategies, offset commit management, consumer group rebalancing,
  and building fault-tolerant producers and consumers in Java / Spring Kafka.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  Distributed Commit Log
    An append-only, ordered, immutable sequence of records persisted directly to disk.
    Records are never modified in place; consumers read from the log at their own pace.

  Topic & Partition
    A Topic is a logical stream category. A Topic is divided into multiple Partitions—
    the fundamental unit of parallelism and physical storage distribution across brokers.

  Offset
    A sequential 64-bit integer assigned to each record within a partition that uniquely
    identifies its position. Consumers track their progress by committing offsets.

  Consumer Group
    A collection of consumers collaborating to read from a topic. Each partition in
    a topic is consumed by exactly one consumer within a group at any given time,
    enabling linear horizontal scale-out.

  Zero-Copy (sendfile syscall)
    A Linux kernel optimization where the OS kernel transfers data directly from
    the OS page cache (disk buffer) to the network socket buffer without copying
    data into user-space application memory, bypassing CPU context switches.

  OS Page Cache
    Operating system memory used to cache disk blocks. Kafka relies on the OS page
    cache rather than maintaining massive in-memory Java heap buffers, avoiding JVM GC pauses.

  Exactly-Once Semantics (EOS)
    A processing guarantee ensuring that each message is delivered and processed
    precisely once, enabled via idempotent producers (PID + sequence numbers) and
    two-phase transactional commits across multiple partitions.

  Log Compaction
    A retention mechanism where Kafka retains only the latest record for each key
    within a partition, creating an up-to-date snapshot of stateful data.

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  KAFKA CLUSTER TOPOLOGY & CONSUMER GROUP PARALLELISM                    │
  │                                                                         │
  │  [ PRODUCER ] ──> Hash(Key) % 3 ──────────────────────────────+         │
  │                                                               │         │
  │  Kafka Cluster (Topic: "orders")                              v         │
  │  +─────────────────────────+  +─────────────────────────+  +─────────+  │
  │  | Broker 1 (Leader P0)    |  | Broker 2 (Leader P1)    |  | Broker 3 |  │
  │  | Log: [0][1][2][3][4]... |  | Log: [0][1][2][3]...    |  | (Leader  |  │
  │  +────────────┬────────────+  +────────────┬────────────+  |  P2)     |  │
  │               │                            │               +────┬────+  │
  │               │ Offset Read                │ Offset Read        │       │
  │               v                            v                    v       │
  │  Consumer Group A (Analytics Service - 3 Consumers)                     │
  │  +─────────────────────────+  +─────────────────────────+  +─────────+  │
  │  |   Consumer Instance 1   |  |   Consumer Instance 2   |  | Instance|  │
  │  |   (Processes Part 0)    |  |   (Processes Part 1)    |  | 3 (Part2|  │
  │  +─────────────────────────+  +─────────────────────────+  +─────────+  │
  └─────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  TRADITIONAL DISK READ VS. KAFKA ZERO-COPY (sendfile) PIPELINE          │
  │                                                                         │
  │  [ TRADITIONAL TRANSFER: 4 Context Switches, 4 Data Copies ]            │
  │  Disk ──(1.DMA)──> OS Page Cache ──(2.CPU Copy)──> Java User Space Heap │
  │                                                          │              │
  │  Network NIC <──(4.DMA)── Socket Buffer <──(3.CPU Copy)──+              │
  │                                                                         │
  │  [ KAFKA ZERO-COPY: 2 Context Switches, 0 CPU Data Copies ]             │
  │  Disk ──(1.DMA Copy)──> OS Page Cache ──(2.DMA Direct)──> Network NIC   │
  │  (Data NEVER enters Java heap; zero CPU overhead, wire-speed transfer!) │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  4. EXPLANATION & THEORY
────────────────────────────────────────────────────────────────────────────────

  Why Kafka is Fast Despite Persisting to Mechanical Disk:
  1. Sequential Disk Access: Sequential writes to disk achieve 600 MB/s on HDDs and
     3+ GB/s on NVMe SSDs, rivaling random memory access speeds. Kafka writes
     records purely as an append-only sequential log.
  2. Heavy Page Cache Reuse: Active producers write to the OS page cache; active
     consumers read directly from that exact same page cache in RAM without ever
     touching physical disk platters!
  3. Batching: Producers buffer and send batches of messages together (batch.size
     and linger.ms), reducing network packet overhead and amortizing disk syncs.

  Partition Rebalancing:
  When a consumer crashes or a new consumer joins a group, a "Rebalance" triggers.
  Modern Kafka uses Cooperative Sticky Assignors: instead of stopping all consumers
  worldwide (Eager Rebalance), only partitions moving between consumers are reassigned,
  minimizing downtime.

────────────────────────────────────────────────────────────────────────────────
  5. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: Java]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Idempotent Kafka Producer Configuration                              │
  │                                                                          │
  │  package com.enterprise.library.kafka;                                   │
  │                                                                          │
  │  import org.apache.kafka.clients.producer.*;                             │
  │  import org.apache.kafka.common.serialization.StringSerializer;          │
  │  import java.util.Properties;                                            │
  │                                                                          │
  │  public class ResilientKafkaProducer {                                   │
  │      public static void main(String[] args) {                            │
  │          Properties props = new Properties();                            │
  │          props.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");                                                                  │
  │          props.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());                                                │
  │          props.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());                                              │
  │                                                                          │
  │          // Crucial Settings for Zero Data Loss:                         │
  │          props.put(ProducerConfig.ENABLE_IDEMPOTENCE_CONFIG, "true");    │
  │          props.put(ProducerConfig.ACKS_CONFIG, "all"); // Wait for all ISR replicas!                                                            │
  │          props.put(ProducerConfig.RETRIES_CONFIG, Integer.MAX_VALUE);    │
  │          props.put(ProducerConfig.LINGER_MS_CONFIG, "10"); // Batching window                                                                   │
  │                                                                          │
  │          try (Producer<String, String> producer = new KafkaProducer<>(props)) {                                                                 │
  │              ProducerRecord<String, String> record =                     │
  │                  new ProducerRecord<>("orders", "user_102", "{\"item\": \"Laptop\", \"price\": 1200}");                                         │
  │                                                                          │
  │              producer.send(record, (metadata, exception) -> {            │
  │                  if (exception == null) {                                │
  │                      System.out.printf("Sent to partition %d at offset %d%n",                                                                    │
  │                          metadata.partition(), metadata.offset());       │
  │                  } else {                                                │
  │                      exception.printStackTrace();                        │
  │                  }                                                       │
  │              });                                                         │
  │          }                                                               │
  │      }                                                                   │
  │  }                                                                       │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: Java]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Production Spring Kafka Consumer with Manual Offset Acknowledgment   │
  │                                                                          │
  │  package com.enterprise.library.kafka;                                   │
  │                                                                          │
  │  import org.springframework.kafka.annotation.KafkaListener;              │
  │  import org.springframework.kafka.support.Acknowledgment;                │
  │  import org.springframework.stereotype.Service;                         │
  │  import org.apache.kafka.clients.consumer.ConsumerRecord;                │
  │  import org.slf4j.Logger;                                                │
  │  import org.slf4j.LoggerFactory;                                         │
  │                                                                          │
  │  @Service                                                                │
  │  public class OrderPaymentConsumer {                                     │
  │      private static final Logger log = LoggerFactory.getLogger(OrderPaymentConsumer.class);                                                     │
  │                                                                          │
  │      // ContainerFactory configured with AckMode.MANUAL_IMMEDIATE        │
  │      @KafkaListener(                                                     │
  │          topics = "orders",                                              │
  │          groupId = "payment-processing-group",                           │
  │          concurrency = "3" // Spawns 3 consumer threads for 3 partitions │
  │      )                                                                   │
  │      public void processOrder(ConsumerRecord<String, String> record, Acknowledgment ack) {                                                      │
  │          try {                                                           │
  │              log.info("Processing order key: {}, partition: {}, offset: {}",                                                                     │
  │                  record.key(), record.partition(), record.offset());     │
  │                                                                          │
  │              // 1. Execute Business Logic (Credit Card Charge)           │
  │              processPayment(record.value());                             │
  │                                                                          │
  │              // 2. Commit offset only AFTER successful processing!       │
  │              ack.acknowledge();                                          │
  │                                                                          │
  │          } catch (Exception ex) {                                        │
  │              log.error("Failed processing order at offset: {}. Routing to Dead Letter Queue (DLQ)...",                                          │
  │                  record.offset(), ex);                                   │
  │              // Handle DLQ routing or retry policy                       │
  │              throw ex; // Triggers Spring Kafka ErrorHandler retry       │
  │          }                                                               │
  │      }                                                                   │
  │                                                                          │
  │      private void processPayment(String payload) {                       │
  │          // Payment gateway integration logic                            │
  │      }                                                                   │
  │  }                                                                       │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  7. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: What happens if a consumer group has more consumers than partitions in a topic?

  ANSWER:
    Any excess consumers will remain idle and receive zero messages. Because
    Kafka enforces a strict 1-to-1 mapping where each partition is assigned to
    at most one consumer per consumer group, the maximum parallelism of a topic
    is strictly bounded by its number of partitions.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: How does Kafka guarantee message ordering?

  ANSWER:
    Kafka guarantees strict total ordering ONLY within a single partition, NOT
    across an entire topic. To ensure sequential ordering for a specific entity
    (e.g. all bank transactions for Account #12345), the producer must specify
    the Account ID as the message Key. Kafka hashes the key (MurmurHash2) to
    route all messages with identical keys to the exact same partition.

────────────────────────────────────────────────────────────────────────────────
  8. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: The Infinite Consumer Rebalance Loop
  A consumer joins a group, reads a batch of 500 records, starts processing
  them, but before finishing, Kafka kicks the consumer out of the group, causing
  a rebalance! The new consumer reads the exact same batch, gets kicked out,
  and the entire group gets stuck in an infinite crash loop. Why?

  SOLUTION:
    The processing of the 500 records took longer than 'max.poll.interval.ms'
    (default 5 minutes). When the consumer failed to invoke another .poll() before
    the timeout expired, the Kafka coordinator concluded the consumer thread was
    dead and evicted it from the group.
    Fixes:
    1. Lower 'max.poll.records' (e.g. from 500 to 50).
    2. Increase 'max.poll.interval.ms'.
    3. Offload time-consuming work to a worker thread pool.

────────────────────────────────────────────────────────────────────────────────
  9. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  1. Decoupled Microservices: At Instagram and Uber, core order/ride events are
     broadcast to Kafka once. Fraud detection, billing, user notifications, and
     data warehouse ingest systems read the identical stream independently without
     placing load on the transactional OLTP database.
  2. Event Sourcing & Audit Logs: Because Kafka logs are immutable and durable,
     financial ledgers can replay history from offset 0 to reconstruct complete
     account balances following database corruption.

────────────────────────────────────────────────────────────────────────────────
  10. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

  -> File 005: Operating System Fundamentals (Page Cache & Zero-Copy DMA)
  -> File 092: Design Instagram (Like counter pipeline & event queues)
  -> File 097: Data Pipeline Architecture (Lambda vs Kappa architectures)
  -> File 105: AWS Messaging (Kafka vs AWS Kinesis / SQS tradeoffs)

================================================================================
  END OF FILE 049
================================================================================
