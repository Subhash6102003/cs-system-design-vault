================================================================================
  FILE 011: Linked Lists
  Section: B - DSA in Java
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  Linked Lists
  A Linked List is a linear data structure where elements are not stored in contiguous memory locations. Instead, each element (node) contains data and a reference (pointer) to the next node. We'll cover Singly, Doubly, and Circular Linked Lists, their memory overhead, and cache implications.
  Prerequisites: Objects, References, Big-O.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  Node
    An object containing data and pointer(s).

  Head
    The first node of the list.

  Tail
    The last node of the list.

  Singly Linked List
    Nodes point only to the next node.

  Doubly Linked List
    Nodes point to both previous and next nodes.

  Pointer Chasing
    Following references scattered across the heap, which causes CPU cache misses.

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  DIAGRAM                                                                │
  │                                                                         │
  │  Singly Linked List:                                                    │
  │  [Head] -> [Data|Next] -> [Data|Next] -> null                           │
  │                                                                         │
  │  Doubly Linked List:                                                    │
  │  null <- [Prev|Data|Next] <-> [Prev|Data|Next] -> null                  │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: Java]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Demo Code                                                            │
  │                                                                          │
  │  public class ListNode {                                                 │
  │      int val;                                                            │
  │      ListNode next;                                                      │
  │      ListNode(int x) { val = x; }                                        │
  │  }                                                                       │
  │                                                                          │
  │  public class LinkedListDemo {                                           │
  │      public void traverse(ListNode head) {                               │
  │          ListNode curr = head;                                           │
  │          while(curr != null) {                                           │
  │              System.out.print(curr.val + " -> ");                        │
  │              curr = curr.next;                                           │
  │          }                                                               │
  │          System.out.println("null");                                     │
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
  │  // Reversing a Linked List                                              │
  │  public class ReverseLinkedList {                                        │
  │      public ListNode reverseList(ListNode head) {                        │
  │          ListNode prev = null;                                           │
  │          ListNode curr = head;                                           │
  │          while (curr != null) {                                          │
  │              ListNode nextTemp = curr.next;                              │
  │              curr.next = prev;                                           │
  │              prev = curr;                                                │
  │              curr = nextTemp;                                            │
  │          }                                                               │
  │          return prev;                                                    │
  │      }                                                                   │
  │  }                                                                       │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  7. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: ArrayList vs LinkedList time complexities?

  ANSWER:
    LinkedList: O(1) insert/delete at known position, O(N) search/access. ArrayList: O(N) insert/delete, O(1) access.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: Why is LinkedList slow in practice?

  ANSWER:
    Poor cache locality. Array elements are contiguous (cache friendly), while Linked List nodes are scattered on the heap.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: Floyd's Tortoise and Hare algorithm?

  ANSWER:
    Use a slow pointer (moves 1 step) and fast pointer (moves 2 steps). If they meet, there is a cycle.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: How to find the middle of a linked list?

  ANSWER:
    Fast and slow pointers. When fast reaches the end, slow is at the middle.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: Memory overhead of LinkedList?

  ANSWER:
    High. Each node needs object headers and pointer fields (4-8 bytes each) in addition to the actual data.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: When would you actually use a LinkedList?

  ANSWER:
    When building LRU Caches (DoublyLinkedList + HashMap) or queues where you strictly add/remove from ends without random access.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q7: How to remove Nth node from the end?

  ANSWER:
    Two pointers separated by N steps. Move both until the lead pointer hits the end.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q8: Merge Two Sorted Lists complexity?

  ANSWER:
    O(N + M) time, O(1) auxiliary space by rewiring pointers.

────────────────────────────────────────────────────────────────────────────────
  8. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: Challenge

  java
  // Trying to delete a node given only its reference
  public void deleteNode(ListNode node) {
  node = node.next;
  }

  SOLUTION:
    Changing the local variable node doesn't affect the list. You must do: node.val = node.next.val; node.next = node.next.next; (assuming it's not the tail).

────────────────────────────────────────────────────────────────────────────────
  9. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  While standard `java.util.LinkedList` is almost never used in modern Java (ArrayDeque is preferred), the linked node *concept* is foundational for HashMaps (chaining), Concurrent queues (Michael-Scott queue), and LRU Caches.

────────────────────────────────────────────────────────────────────────────────
  10. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

  -> File 008: 008_Arrays_Memory_Addressing.md ([012_Stacks_Applications.md](012_Stacks_Applications.md))

================================================================================
  END OF FILE 011
================================================================================
