================================================================================
  FILE 012: Stacks and Applications
  Section: B - DSA in Java
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  Stacks and Applications
  A Stack is a Last-In, First-Out (LIFO) data structure. This file explains how stacks operate, the difference between the Call Stack (OS/JVM memory) and Stack ADT, and why Java's Stack class is obsolete compared to ArrayDeque.
  Prerequisites: Arrays, Linked Lists.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  LIFO
    Last In, First Out.

  Push
    Add item to top.

  Pop
    Remove item from top.

  Peek
    View top item without removing.

  Call Stack
    JVM structure tracking active method executions and local variables.

  Stack Frame
    The chunk of memory on the call stack allocated for a single method call.

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  DIAGRAM                                                                │
  │                                                                         │
  │  Stack Operations:                                                      │
  │  Push(3) ->  | 3 |  (Top)                                               │
  │  Push(2) ->  | 2 |                                                      │
  │  Push(1) ->  | 1 |                                                      │
  │              +---+                                                      │
  │                                                                         │
  │  Call Stack:                                                            │
  │  | methodC() | <- active frame                                          │
  │  | methodB() |                                                          │
  │  | methodA() |                                                          │
  │  +-----------+                                                          │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: Java]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Demo Code                                                            │
  │                                                                          │
  │  import java.util.ArrayDeque;                                            │
  │  import java.util.Deque;                                                 │
  │                                                                          │
  │  public class StackDemo {                                                │
  │      public static void main(String[] args) {                            │
  │          // Use ArrayDeque instead of java.util.Stack                    │
  │          Deque<Integer> stack = new ArrayDeque<>();                      │
  │          stack.push(10);                                                 │
  │          stack.push(20);                                                 │
  │          System.out.println(stack.peek()); // 20                         │
  │          System.out.println(stack.pop());  // 20                         │
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
  │  // Valid Parentheses                                                    │
  │  public boolean isValid(String s) {                                      │
  │      java.util.Deque<Character> stack = new java.util.ArrayDeque<>();    │
  │      for (char c : s.toCharArray()) {                                    │
  │          if (c == '(') stack.push(')');                                  │
  │          else if (c == '{') stack.push('}');                             │
  │          else if (c == '[') stack.push(']');                             │
  │          else if (stack.isEmpty() || stack.pop() != c) return false;     │
  │      }                                                                   │
  │      return stack.isEmpty();                                             │
  │  }                                                                       │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  7. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: Why use ArrayDeque instead of java.util.Stack?

  ANSWER:
    `java.util.Stack` extends `Vector`, which has synchronized methods. This lock overhead is slow and usually unnecessary. `ArrayDeque` is faster and not synchronized.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: How to implement a Min Stack with O(1) getMin()?

  ANSWER:
    Use two stacks. One for normal values, one that strictly pushes the minimum value seen so far.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: Difference between StackOverflowError and OutOfMemoryError?

  ANSWER:
    StackOverflow occurs when the call stack exceeds its limit (infinite recursion). OutOfMemory happens when the Heap is full.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: How do you evaluate Postfix notation (Reverse Polish Notation)?

  ANSWER:
    Push operands to a stack. When you see an operator, pop two operands, apply the operator, and push the result back.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: Can a stack be implemented with a Linked List?

  ANSWER:
    Yes, inserting and deleting at the Head gives O(1) push and pop.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: Monotonic Stack?

  ANSWER:
    A stack whose elements are strictly increasing or decreasing. Used for problems like "Next Greater Element".

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q7: How to implement a queue using stacks?

  ANSWER:
    Use two stacks. Push to Stack1. For pop/peek, if Stack2 is empty, pop all elements from Stack1 into Stack2 to reverse the order.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q8: Space complexity of recursion?

  ANSWER:
    O(N) where N is the maximum depth of the call stack.

────────────────────────────────────────────────────────────────────────────────
  8. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: Challenge

  java
  public int sum(int n) {
  if (n == 0) return 0;
  return n + sum(n);
  }

  SOLUTION:
    Infinite recursion (sum(n) instead of sum(n-1)). Throws StackOverflowError.

────────────────────────────────────────────────────────────────────────────────
  9. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  The JVM relies on the Call Stack for method execution and thread isolation. Understanding stack frames is crucial for reading stack traces during debugging. Monotonic stacks are heavily used in quantitative trading algorithms for finding local max/mins in price history.

────────────────────────────────────────────────────────────────────────────────
  10. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

  -> File 013: 013_Queues_Deques_CircularBuffers.md

================================================================================
  END OF FILE 012
================================================================================
