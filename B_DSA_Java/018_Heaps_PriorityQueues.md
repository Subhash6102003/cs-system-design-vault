================================================================================
  FILE 018: Heaps and Priority Queues
  Section: B - DSA in Java
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  A Heap is a specialized tree-based data structure that satisfies the heap property, making it extremely efficient for retrieving the maximum or minimum element. While conceptually a tree, it is almost always implemented as a flat array. In Java, this is represented by the PriorityQueue class.

  Prerequisites: Arrays, Trees, Logarithms.
  What you'll learn: Min/Max heap properties, array-to-tree index math, heapify operations, building a heap in O(N), and solving top-K/median problems.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  Complete Binary Tree
    A tree where every level is fully populated except possibly the last, which is filled left-to-right.

  Max-Heap Property
    Every parent node is >= its children. The absolute maximum is at the root.

  Min-Heap Property
    Every parent node is <= its children. The absolute minimum is at the root.

  Heapify Up (Swim)
    Used during insertion. If a new node violates the heap property, it swaps with its parent until the property is restored.

  Heapify Down (Sink)
    Used during deletion (extracting root). The root is replaced by the last element, which then swaps with its largest (or smallest) child until the property is restored.

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  Heap as a Tree and as an Array (Min-Heap)                              │
  │                                                                         │
  │  Tree View:               Array View:                                   │
  │        1                  Index: 0  1  2  3  4  5                       │
  │      /   \                Value: 1, 3, 6, 5, 9, 8                       │
  │     3     6                                                             │
  │    / \   /                Math:                                         │
  │   5   9 8                 Parent of 5 (idx 3) = (3-1)/2 = idx 1 (val 3) │
  │                           Left child of 3 (idx 1) = 2*1+1 = idx 3 (val 5)│
  │                           Right child of 3 (idx 1) = 2*1+2 = idx 4 (val 9)│
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  Extract Min (Heapify Down)                                             │
  │                                                                         │
  │  1. Extract 1. Move last element (8) to root.                           │
  │        8                                                                │
  │      /   \      -> violates Min-Heap. Swap 8 with smallest child (3).   │
  │     3     6                                                             │
  │    / \                                                                  │
  │   5   9                                                                 │
  │                                                                         │
  │  2. Swap 8 and 3:                                                       │
  │        3                                                                │
  │      /   \      -> violates Min-Heap. Swap 8 with smallest child (5).   │
  │     8     6                                                             │
  │    / \                                                                  │
  │   5   9                                                                 │
  │                                                                         │
  │  3. Final State:                                                        │
  │        3                                                                │
  │      /   \                                                              │
  │     5     6                                                             │
  │    / \                                                                  │
  │   8   9                                                                 │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  Language: Java

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  public class MinHeapDemo {                                                │
  │      private int[] heap;                                                 │
  │      private int size;                                                   │
  │      private int capacity;                                               │
  │                                                                          │
  │      public MinHeapDemo(int capacity) {                                  │
  │          this.capacity = capacity;                                       │
  │          this.size = 0;                                                  │
  │          this.heap = new int[capacity];                                  │
  │      }                                                                   │
  │                                                                          │
  │      private int parent(int i) { return (i - 1) / 2; }                   │
  │      private int leftChild(int i) { return 2 * i + 1; }                  │
  │      private int rightChild(int i) { return 2 * i + 2; }                 │
  │      private void swap(int i, int j) {                                   │
  │          int temp = heap[i]; heap[i] = heap[j]; heap[j] = temp;          │
  │      }                                                                   │
  │                                                                          │
  │      public void insert(int key) {                                       │
  │          if (size == capacity) throw new RuntimeException("Heap is full");│
  │          int i = size;                                                   │
  │          heap[i] = key;                                                  │
  │          size++;                                                         │
  │                                                                          │
  │          // Heapify Up                                                   │
  │          while (i != 0 && heap[parent(i)] > heap[i]) {                   │
  │              swap(i, parent(i));                                         │
  │              i = parent(i);                                              │
  │          }                                                               │
  │      }                                                                   │
  │                                                                          │
  │      public int extractMin() {                                           │
  │          if (size <= 0) return Integer.MAX_VALUE;                        │
  │          if (size == 1) { size--; return heap[0]; }                      │
  │                                                                          │
  │          int root = heap[0];                                             │
  │          heap[0] = heap[size - 1]; // Move last element to root          │
  │          size--;                                                         │
  │          heapifyDown(0);                                                 │
  │          return root;                                                    │
  │      }                                                                   │
  │                                                                          │
  │      private void heapifyDown(int i) {                                   │
  │          int left = leftChild(i);                                        │
  │          int right = rightChild(i);                                      │
  │          int smallest = i;                                               │
  │                                                                          │
  │          if (left < size && heap[left] < heap[smallest]) smallest = left;│
  │          if (right < size && heap[right] < heap[smallest]) smallest = right;│
  │                                                                          │
  │          if (smallest != i) {                                            │
  │              swap(i, smallest);                                          │
  │              heapifyDown(smallest); // Recursively heapify down          │
  │          }                                                               │
  │      }                                                                   │
  │  }                                                                       │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

  Language: Java

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  import java.util.PriorityQueue;                                         │
  │  import java.util.Collections;                                           │
  │                                                                          │
  │  /**                                                                     │
  │   * Using Java's built-in PriorityQueue.                                 │
  │   * By default, PriorityQueue is a Min-Heap.                             │
  │   * We can make it a Max-Heap using Collections.reverseOrder() or a custom Comparator. │
  │   */                                                                     │
  │  public class PriorityQueueProduction {                                  │
  │                                                                          │
  │      // Problem: Find the Kth Largest Element in an Array (O(N log K))   │
  │      public int findKthLargest(int[] nums, int k) {                      │
  │          // Min-Heap of size K                                           │
  │          PriorityQueue<Integer> pq = new PriorityQueue<>();              │
  │                                                                          │
  │          for (int num : nums) {                                          │
  │              pq.offer(num);                                              │
  │              // If size exceeds K, remove the smallest element.          │
  │              // This ensures the heap contains ONLY the top K largest elements. │
  │              if (pq.size() > k) {                                        │
  │                  pq.poll();                                              │
  │              }                                                           │
  │          }                                                               │
  │                                                                          │
  │          // The root of the Min-Heap is the Kth largest element          │
  │          return pq.peek();                                               │
  │      }                                                                   │
  │  }                                                                       │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  7. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: Why is a heap implemented as an array rather than a linked tree?

  ANSWER:
    Because it is a complete binary tree, there are no gaps. Using an array avoids the memory overhead of node pointers, and navigating via index math (`2*i+1`) is highly cache-friendly.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: What is the time complexity of building a heap from an unsorted array?

  ANSWER:
    O(N). By applying `heapifyDown` bottom-up (starting from the last non-leaf node down to the root), the math series converges to `O(N)`, which is faster than inserting elements one by one `O(N log N)`.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: How does HeapSort work?

  ANSWER:
    1) Build a Max-Heap `O(N)`. 2) Swap root with the last element, reduce heap size, and `heapifyDown(0)`. Repeat `N` times. Total time `O(N log N)`. Space `O(1)` (in-place).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: How do you find the Median from a Data Stream using heaps?

  ANSWER:
    Maintain two heaps: A Max-Heap for the lower half of numbers, and a Min-Heap for the upper half. Keep their sizes equal (or Max-Heap size + 1). The median is either the root of Max-Heap or the average of both roots.

────────────────────────────────────────────────────────────────────────────────
  8. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: The Infinite Sink

  private void heapifyDown(int i) {
      int left = 2 * i + 1;
      int right = 2 * i + 2;
      int smallest = i;
      
      if (left < size && heap[left] < heap[i]) smallest = left;
      if (right < size && heap[right] < heap[i]) smallest = right; // BUG HERE
      
      if (smallest != i) {
          swap(i, smallest);
          heapifyDown(smallest);
      }
  }

  SOLUTION:
    The right child check compares against `heap[i]` instead of `heap[smallest]`. If both children are smaller than `i`, but `right` is larger than `left`, it erroneously picks `right` as the smallest to swap with!

────────────────────────────────────────────────────────────────────────────────
  9. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  - Task Schedulers / Thread Pools: OS and JVM thread pools use Priority Queues to pick the highest priority thread/task to execute next.
  - Graph Algorithms: Dijkstra's Shortest Path and Prim's Minimum Spanning Tree rely heavily on Min-Heaps for fetching the next closest node efficiently.
  - Timer Events: Systems managing timeouts (e.g., HTTP requests) use Min-Heaps ordered by expiration timestamp.

────────────────────────────────────────────────────────────────────────────────
  10. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

  -> File 015: Binary_Trees_BST.md (Tree fundamentals)
  -> File 012: Sorting_Algorithms.md (HeapSort comparison with Merge/Quick Sort)

================================================================================
  END OF FILE 018
================================================================================
