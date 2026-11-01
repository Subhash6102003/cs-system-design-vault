================================================================================
  FILE 010: Strings and JVM String Pool
  Section: B - DSA in Java
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  Strings and JVM String Pool
  In Java, Strings are first-class citizens with unique memory management rules. This file explores String immutability, the String Pool (interning), differences between String, StringBuilder, and StringBuffer, and how character encoding works under the hood.
  Prerequisites: Arrays, Basic Java Objects.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  Immutability
    Once a String object is created, its value cannot be changed.

  String Pool
    A special memory region in the Heap that stores unique string literals to save memory.

  StringBuilder
    Mutable string builder, not thread-safe (faster).

  StringBuffer
    Mutable string builder, thread-safe (slower due to synchronization).

  Compact Strings (Java 9+)
    Strings use byte[] instead of char[] and a coder flag (LATIN1 vs UTF16) to save memory.

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  DIAGRAM                                                                │
  │                                                                         │
  │  JVM Heap Memory:                                                       │
  │  +---------------------------------------+                              │
  │  |             Heap                      |                              │
  │  |  +---------------------------------+  |                              │
  │  |  |        String Pool              |  |                              │
  │  |  |  "Hello"   "World"              |  |                              │
  │  |  +---------------------------------+  |                              │
  │  |                                       |                              │
  │  |  [String Object] -> "Hello"           |                              │
  │  +---------------------------------------+                              │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: Java]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Demo Code                                                            │
  │                                                                          │
  │  public class StringPoolDemo {                                           │
  │      public static void main(String[] args) {                            │
  │          String s1 = "Hello";           // Goes to String Pool           │
  │          String s2 = "Hello";           // Reuses from String Pool       │
  │          String s3 = new String("Hello"); // Creates new object in Heap  │
  │                                                                          │
  │          System.out.println(s1 == s2); // true                           │
  │          System.out.println(s1 == s3); // false                          │
  │          System.out.println(s1.equals(s3)); // true                      │
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
  │  // Efficient String concatenation using StringBuilder                   │
  │  public class LogBuilder {                                               │
  │      public String buildLog(String[] events) {                           │
  │          StringBuilder sb = new StringBuilder();                         │
  │          for (String event : events) {                                   │
  │              sb.append("[").append(java.time.Instant.now()).append("] ") │
  │                .append(event).append("\n");                              │
  │          }                                                               │
  │          return sb.toString();                                           │
  │      }                                                                   │
  │  }                                                                       │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  7. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: Why are Strings immutable in Java?

  ANSWER:
    Security (can't alter DB URL/passwords passed by ref), Thread safety, and to enable the String Pool for memory savings.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: What does `String.intern()` do?

  ANSWER:
    It puts the string in the String Pool if it's not already there, and returns the reference to the pooled string.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: `==` vs `.equals()` for Strings?

  ANSWER:
    `==` compares object references (memory addresses). `.equals()` compares the actual character content.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: Why is `new String("abc")` bad practice?

  ANSWER:
    It forces the creation of a new object on the heap, bypassing the memory optimization of the String Pool.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: Time complexity of String concatenation in a loop?

  ANSWER:
    If using `+`, it's O(N^2) because a new String is copied each time. With StringBuilder, it is O(N).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: How does Java store chars?

  ANSWER:
    UTF-16 (2 bytes per char) in Java 8. In Java 9+, it uses Latin-1 (1 byte) if possible, else UTF-16.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q7: Are String literals thread-safe?

  ANSWER:
    Yes, because they are immutable.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q8: How to check for anagrams efficiently?

  ANSWER:
    Count character frequencies using an int array of size 26 (for lowercase English letters).

────────────────────────────────────────────────────────────────────────────────
  8. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: Challenge

  java
  String s = "";
  for(int i=0; i<10000; i++) {
  s += "a";
  }

  SOLUTION:
    This creates 10,000 intermediate String and StringBuilder objects, thrashing the garbage collector and taking O(N^2) time.

────────────────────────────────────────────────────────────────────────────────
  9. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  Strings account for roughly 25-40% of memory in typical Java enterprise applications. Misunderstanding the String Pool or using `+` in loops leads to massive memory bloat, high Garbage Collection (GC) pauses, and latency spikes.

────────────────────────────────────────────────────────────────────────────────
  10. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

  -> File 008: 008_Arrays_Memory_Addressing.md

================================================================================
  END OF FILE 010
================================================================================
