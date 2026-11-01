================================================================================
  FILE 013: Queues, Deques, and Circular Buffers
  Section: B - DSA in Java
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  Queues, Deques, and Circular Buffers
  A Queue is a First-In, First-Out (FIFO) data structure. We will explore simple queues, double-ended queues (Deques), and how Circular Buffers optimize space and time using modulo arithmetic.
  Prerequisites: Arrays, Linked Lists.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  FIFO
    First In, First Out.

  Enqueue (Offer)
    Add element to the back/tail.

  Dequeue (Poll)
    Remove element from the front/head.

  Deque
    Double-Ended Queue (add/remove from both ends).

  Circular Buffer (Ring Buffer)
    An array implementation of a queue that wraps around when it hits the end of the array.

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  DIAGRAM                                                                │
  │                                                                         │
  │  Queue Operations:                                                      │
  │  Front -> [1, 2, 3] <- Back (Enqueue 4)                                 │
  │  Dequeue -> Front becomes 2                                             │
  │                                                                         │
  │  Circular Buffer (Size 5):                                              │
  │  [ 4,  5,  _,  2,  3 ]                                                  │
  │            ^   ^                                                        │
  │         Tail   Head                                                     │
  │  (Modulo arithmetic: next index = (index + 1) % size)                   │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: Java]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Demo Code                                                            │
  │                                                                          │
  │  import java.util.LinkedList;                                            │
  │  import java.util.Queue;                                                 │
  │                                                                          │
  │  public class QueueDemo {                                                │
  │      public static void main(String[] args) {                            │
  │          Queue<Integer> q = new LinkedList<>();                          │
  │          q.offer(1); // Enqueue                                          │
  │          q.offer(2);                                                     │
  │          System.out.println(q.poll()); // 1 (Dequeue)                    │
  │      }                                                                   │
  │  }                                                                       │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: Java]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │                                                                          │
  │  // Array-based Circular Queue                                           │
  │  public class CircularQueue {                                            │
  │      private int[] data;                                                 │
  │      private int head, tail, size;                                       │
  │                                                                          │
  │      public CircularQueue(int k) {                                       │
  │          data = new int[k];                                              │
  │          head = 0; tail = 0; size = 0;                                   │
  │      }                                                                   │
  │                                                                          │
  │      public boolean enQueue(int value) {                                 │
  │          if (size == data.length) return false;                          │
  │          data[tail] = value;                                             │
  │          tail = (tail + 1) % data.length;                                │
  │          size++;                                                         │
  │          return true;                                                    │
  │      }                                                                   │
  │                                                                          │
  │      public boolean deQueue() {                                          │
  │          if (size == 0) return false;                                    │
  │          head = (head + 1) % data.length;                                │
  │          size--;                                                         │
  │          return true;                                                    │
  │      }                                                                   │
  │  }                                                                       │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  7. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: ArrayDeque vs LinkedList for Queues?

  ANSWER:
    `ArrayDeque` is backed by a circular array and is generally faster due to cache locality and no node allocation overhead.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: How does a Circular Buffer prevent shifting elements?

  ANSWER:
    By maintaining `head` and `tail` pointers that wrap around the array using modulo arithmetic, achieving O(1) operations.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: What is a Priority Queue?

  ANSWER:
    A queue where elements are dequeued based on their priority (usually backed by a Min/Max Heap), not strictly FIFO.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: How is a queue used in graph algorithms?

  ANSWER:
    Breadth-First Search (BFS) uses a queue to process nodes level by level.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: Sliding Window Maximum using Deque?

  ANSWER:
    Keep indices of potentially maximum elements in a Deque. Remove elements from the back that are smaller than the new element.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: BlockingQueue in Java?

  ANSWER:
    Thread-safe queues that block the thread if trying to dequeue from an empty queue or enqueue to a full queue. Used in thread pools.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q7: Can Deque be used as a Stack?

  ANSWER:
    Yes, using `push()` and `pop()`. It is the recommended implementation.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q8: What happens if tail == head in a circular queue?

  ANSWER:
    It means the queue is either completely empty or completely full, depending on the `size` variable tracker.

────────────────────────────────────────────────────────────────────────────────
  8. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: Challenge

  java
  // Trying to increment tail in circular array of size N
  tail = tail + 1 % N;

  SOLUTION:
    Operator precedence bug. % happens before +. It should be tail = (tail + 1) % N;

────────────────────────────────────────────────────────────────────────────────
  9. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  Queues decouple producers from consumers (e.g., Kafka, RabbitMQ). Circular buffers (like Disruptor) are heavily used in high-frequency trading for zero-allocation, ultra-low latency messaging between threads.

────────────────────────────────────────────────────────────────────────────────
  10. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

  -> File 011: 011_Linked_Lists.md ([012_Stacks_Applications.md](012_Stacks_Applications.md))

================================================================================
  END OF FILE 013
================================================================================
