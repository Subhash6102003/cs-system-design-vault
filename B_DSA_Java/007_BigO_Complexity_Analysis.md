================================================================================
  FILE 007: Big-O Complexity Analysis
  Section: B - DSA in Java
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  Big-O Complexity Analysis
  This file covers the mathematical and practical foundations of analyzing algorithmic efficiency. You will learn the definitions of Big-O, Big-Theta, and Big-Omega, how to analyze the time and space complexity of common operations, and why theoretical complexity sometimes lies in practice.
  Prerequisites: Basic Java programming, basic math.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  Time Complexity
    The amount of time an algorithm takes to run as a function of the length of the input.

  Space Complexity
    The amount of memory an algorithm takes to run. Includes auxiliary space (extra space) and input space.

  Big-O (O)
    The upper bound on time/space. Worst-case scenario.

  Big-Omega (Ω)
    The lower bound. Best-case scenario.

  Big-Theta (Θ)
    Tight bound. When upper and lower bounds match.

  Amortized Analysis
    The average time taken per operation, if one operation is expensive but rare (e.g., ArrayList resize).

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  DIAGRAM                                                                │
  │                                                                         │
  │  Growth Rates:                                                          │
  │  O(1)        : --------------------------                               │
  │  O(log N)    :     ------------------                                   │
  │  O(N)        :           /                                              │
  │  O(N log N)  :          /                                               │
  │  O(N^2)      :        /                                                 │
  │  O(2^N)      :      /                                                   │
  │  O(N!)       :     |                                                    │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: Java]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Demo Code                                                            │
  │                                                                          │
  │  public class ComplexityDemo {                                           │
  │      // O(1) Time                                                        │
  │      public int getFirst(int[] arr) {                                    │
  │          return arr[0];                                                  │
  │      }                                                                   │
  │                                                                          │
  │      // O(N) Time                                                        │
  │      public int sum(int[] arr) {                                         │
  │          int total = 0;                                                  │
  │          for (int num : arr) {                                           │
  │              total += num;                                               │
  │          }                                                               │
  │          return total;                                                   │
  │      }                                                                   │
  │                                                                          │
  │      // O(N^2) Time                                                      │
  │      public void printPairs(int[] arr) {                                 │
  │          for (int i = 0; i < arr.length; i++) {                          │
  │              for (int j = 0; j < arr.length; j++) {                      │
  │                  System.out.println(arr[i] + ", " + arr[j]);             │
  │              }                                                           │
  │          }                                                               │
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
  │  import java.util.ArrayList;                                             │
  │                                                                          │
  │  public class AmortizedResizeDemo {                                      │
  │      public static void main(String[] args) {                            │
  │          // ArrayList resize is amortized O(1)                           │
  │          ArrayList<Integer> list = new ArrayList<>(1);                   │
  │          long start = System.nanoTime();                                 │
  │          list.add(1); // O(1)                                            │
  │          list.add(2); // O(N) resize, but amortized O(1)                 │
  │          long end = System.nanoTime();                                   │
  │          System.out.println("Time taken: " + (end - start) + " ns");     │
  │      }                                                                   │
  │  }                                                                       │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  7. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: What is the complexity of nested loops where the inner loop depends on the outer loop?

  ANSWER:
    Usually O(N^2) (e.g., `for(i=0..N) for(j=i..N)` runs N(N-1)/2 times).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: What is amortized O(1)?

  ANSWER:
    A sequence of operations takes O(N) total time, so averaging it out gives O(1) per operation.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: Does space complexity include the input array size?

  ANSWER:
    Total space complexity does; auxiliary space complexity does not.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: What is the time complexity of adding to a HashMap?

  ANSWER:
    O(1) on average, O(N) worst case if there are hash collisions.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: What's the space complexity of a recursive function that goes N deep?

  ANSWER:
    O(N) due to the call stack frames.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: Is O(1000 N) better than O(N^2)?

  ANSWER:
    Yes, for sufficiently large N.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q7: What is the complexity of binary search?

  ANSWER:
    O(log N).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q8: How does cache locality affect Big-O?

  ANSWER:
    An O(N) algorithm with good cache locality (like array traversal) can be faster than an O(N) algorithm with poor locality (like linked list traversal).

────────────────────────────────────────────────────────────────────────────────
  8. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: Challenge

  I run in O(N) time but take O(N) space. If you replace me with an iterative version, I take O(1) space. What am I?

  SOLUTION:
    A recursive function doing a linear scan.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 2: Challenge

  java
  // What's the Big-O?
  for(int i=1; i<=n; i*=2) {
  System.out.println(i);
  }

  SOLUTION:
    O(log N). The loop variable multiplies by 2, halving the remaining distance to n each step.

────────────────────────────────────────────────────────────────────────────────
  9. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  Big-O tells you how your code will scale when traffic or data size increases 10x or 100x. An O(N^2) algorithm might work fine in dev with 10 records, but will crash production with 10,000 records.

────────────────────────────────────────────────────────────────────────────────
  10. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

  -> File 008: 008_Arrays_Memory_Addressing.md ([011_Linked_Lists.md](011_Linked_Lists.md))

================================================================================
  END OF FILE 007
================================================================================
