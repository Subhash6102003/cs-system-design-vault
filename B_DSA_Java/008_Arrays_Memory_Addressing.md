================================================================================
  FILE 008: Arrays and Memory Addressing
  Section: B - DSA in Java
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  Arrays and Memory Addressing
  This file delves into how arrays are stored in memory, how indexing works mathematically, and the differences between static and dynamic arrays. You will also learn about cache implications in multi-dimensional arrays.
  Prerequisites: Memory basics, Big-O notation.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  Contiguous Memory
    Memory blocks located back-to-back.

  Base Address
    The memory address of the first element in the array.

  Row-Major vs Column-Major Order
    How 2D arrays are flattened in memory (Java is technically arrays of arrays, so row-major by reference).

  Dynamic Array (ArrayList)
    An array that automatically resizes when it reaches capacity.

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  DIAGRAM                                                                │
  │                                                                         │
  │  Memory Addressing Formula:                                             │
  │  Address(index) = Base_Address + (Index * Element_Size)                 │
  │                                                                         │
  │  Array Layout:                                                          │
  │  +------+------+------+------+                                          │
  │  |  10  |  20  |  30  |  40  |                                          │
  │  +------+------+------+------+                                          │
  │   0x100  0x104  0x108  0x10C  (assuming 4-byte int)                     │
  │                                                                         │
  │  ArrayList Resize (1.5x):                                               │
  │  Capacity 4: [1, 2, 3, 4]                                               │
  │  Add 5 -> Capacity 6: [1, 2, 3, 4, 5, _]                                │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: Java]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Demo Code                                                            │
  │                                                                          │
  │  public class ArrayDemo {                                                │
  │      public static void main(String[] args) {                            │
  │          // Static Array                                                 │
  │          int[] arr = new int[5];                                         │
  │                                                                          │
  │          // 2D Array                                                     │
  │          int[][] matrix = new int[3][3];                                 │
  │                                                                          │
  │          // Dynamic Array                                                │
  │          java.util.ArrayList<Integer> list = new java.util.ArrayList<>();│
  │          list.add(1);                                                    │
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
  │  public class CustomArrayList {                                          │
  │      private int[] data;                                                 │
  │      private int size;                                                   │
  │                                                                          │
  │      public CustomArrayList() {                                          │
  │          data = new int[2]; // initial capacity                          │
  │          size = 0;                                                       │
  │      }                                                                   │
  │                                                                          │
  │      public void add(int element) {                                      │
  │          if (size == data.length) {                                      │
  │              resize();                                                   │
  │          }                                                               │
  │          data[size++] = element;                                         │
  │      }                                                                   │
  │                                                                          │
  │      private void resize() {                                             │
  │          int[] newData = new int[data.length * 2];                       │
  │          System.arraycopy(data, 0, newData, 0, data.length);             │
  │          data = newData;                                                 │
  │      }                                                                   │
  │  }                                                                       │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  7. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: Why is array access O(1)?

  ANSWER:
    Because of the direct memory addressing formula.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: How much does ArrayList grow in Java?

  ANSWER:
    By 1.5x its current size.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: What is Kadane's Algorithm used for?

  ANSWER:
    Finding the maximum contiguous subarray sum in O(N) time.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: Difference between Array and ArrayList?

  ANSWER:
    Array is fixed-size and can hold primitives; ArrayList is dynamic and holds objects (boxed primitives).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: Why do arrays have good cache locality?

  ANSWER:
    Elements are stored contiguously, so a cache block fetch brings in multiple adjacent elements.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: How does a 2D array work in Java?

  ANSWER:
    It is an array of references to other arrays.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q7: What is the time complexity of inserting at the beginning of an ArrayList?

  ANSWER:
    O(N) because all elements must be shifted.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q8: Is there memory fragmentation with arrays?

  ANSWER:
    External fragmentation no, but large arrays might fail to allocate if no sufficiently large contiguous block exists.

────────────────────────────────────────────────────────────────────────────────
  8. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: Challenge

  java
  int[] arr = {1, 2, 3};
  for(int i = 0; i <= arr.length; i++) {
  System.out.println(arr[i]);
  }

  SOLUTION:
    ArrayIndexOutOfBoundsException on i == arr.length.

────────────────────────────────────────────────────────────────────────────────
  9. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  Arrays are the most cache-friendly data structure. High-performance systems (like trading engines or game engines) use arrays over object-heavy collections to maximize CPU cache hits and minimize garbage collection.

────────────────────────────────────────────────────────────────────────────────
  10. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

  -> File 007: 007_BigO_Complexity_Analysis.md ([011_Linked_Lists.md](011_Linked_Lists.md))

================================================================================
  END OF FILE 008
================================================================================
