================================================================================
  FILE 004: JVM Architecture, Stack, Heap & Garbage Collection
  Section: A - Hardware & CS Foundations
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  JVM Architecture & GC: Memory Management Under the Hood
  
  This document details the Java Virtual Machine (JVM) internals, specifically how memory is structured (Heap vs. Stack) and how memory is reclaimed (Garbage Collection). Understanding this is critical for tuning high-performance Java/Kotlin applications, preventing OutOfMemory errors, and minimizing Stop-The-World latency spikes.
  Prerequisites: Understanding of basic Java and Object-Oriented concepts.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  JVM Architecture Overview
    

  Class Loader Subsystem
    Loads, links, and initializes .class files into memory.

  Runtime Data Areas
    Memory areas assigned by the OS to the JVM (Stack, Heap, Method Area/Metaspace, PC Registers, Native Method Stack).

  Execution Engine
    Executes the bytecode (Interpreter, JIT Compiler, Garbage Collector).

  Stack (Thread Local)
    Stores method frames. When a method is called, a new frame is pushed. When it returns, it's popped.

  Local Variable Array
    Holds primitive local variables and object references.

  Operand Stack
    Used for intermediate calculations (like a CPU register).

  Heap (Shared)
    Where all objects and arrays are allocated. Subject to Garbage Collection.

  Young Generation
    Where new objects are created. Contains Eden space and two Survivor spaces (S0, S1).

  Old (Tenured) Generation
    Where long-lived objects are moved after surviving several Young Gen GCs.

  Metaspace (formerly PermGen)
    Stores class metadata (methods, fields, constant pool). Resides in native memory, not the Java Heap.

  Object Layout in Memory
    

  Mark Word (8 bytes)
    HashCode, GC age, lock state.

  Klass Pointer (4/8 bytes)
    Points to the class metadata in Metaspace.

  Instance Data
    The actual fields of the object.

  Padding
    Objects are aligned to 8-byte boundaries for CPU cache efficiency.

  Compressed OOPs (Ordinary Object Pointers)
    A JVM trick to use 32-bit pointers on a 64-bit architecture (saving memory) if the heap is less than 32GB.

  Garbage Collection Algorithms
    

  Mark-Sweep
    Marks reachable objects, sweeps (deletes) unmarked ones. Leaves fragmentation.

  Mark-Compact
    Marks, sweeps, then compacts remaining objects to the start of memory. Prevents fragmentation but is slow.

  Copying
    Divides memory in half. Copies live objects to the other half sequentially. Fast, no fragmentation, but wastes 50% of space.

  GC Implementations
    

  Parallel GC
    Throughput-focused. Uses multiple threads for Young and Old gen.

  G1 GC (Garbage-First)
    Default since Java 9. Divides heap into equal-sized regions. Tries to meet a user-defined pause time goal.

  ZGC / Shenandoah
    Ultra-low latency GCs (pauses < 1ms) capable of compacting the heap concurrently with application threads.

  Stop-The-World (STW)
    A pause where all application threads are completely halted so the GC can safely move objects and update pointers.

  GC Roots
    The starting points for the Mark phase (Local variables on active stacks, static fields, JNI references). An object is unreachable if no chain of references connects it to a GC Root.

  Reference Types
    

  Strong
    Object obj = new Object(). Will never be GC'd while referenced.

  Soft
    GC'd only if JVM is absolutely out of memory. Good for caches.

  Weak
    GC'd on the very next cycle if no strong references exist. Used in WeakHashMap.

  Phantom
    Used for pre-mortem cleanup scheduling.

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  JVM RUNTIME DATA AREAS & HEAP LAYOUT                                   │
  │                                                                         │
  │  +-------------------------------------------------------------+        │
  │  |                     JVM Process (OS Level)                  |        │
  │  |                                                             |        │
  │  |  +--------------------+  +-------------------------------+  |        │
  │  |  | Thread 1 Stack     |  |           JAVA HEAP           |  |        │
  │  |  | +-------------+    |  | +---------------------------+ |  |        │
  │  |  | | Frame (m2)  |    |  | | Young Gen                 | |  |        │
  │  |  | +-------------+    |  | | [ Eden ] [ S0 ] [ S1 ]    | |  |        │
  │  |  | | Frame (m1)  |    |  | +---------------------------+ |  |        │
  │  |  | +-------------+    |  |                               | |  |      │
  │  |  +--------------------+  | +---------------------------+ |  |        │
  │  |                          | | Old (Tenured) Gen         | |  |        │
  │  |  +--------------------+  | | [.......................] | |  |        │
  │  |  | Thread 2 Stack     |  | +---------------------------+ |  |        │
  │  |  | +-------------+    |  +-------------------------------+  |        │
  │  |  | | Frame (m3)  |    |                                     |        │
  │  |  | +-------------+    |  +-------------------------------+  |        │
  │  |  +--------------------+  | Metaspace (Native Memory)     |  |        │
  │  |                          | Class metadata, static fields |  |        │
  │  |                          +-------------------------------+  |        │
  │  +-------------------------------------------------------------+        │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  G1 GC REGION LAYOUT                                                    │
  │                                                                         │
  │  +----+----+----+----+----+----+----+----+                              │
  │  | E  | E  | O  | O  | F  | S  | O  | H  |                              │
  │  +----+----+----+----+----+----+----+----+                              │
  │  | O  | E  | S  | F  | O  | O  | E  | H  |                              │
  │  +----+----+----+----+----+----+----+----+                              │
  │  | F  | O  | O  | O  | E  | E  | O  | O  |                              │
  │  +----+----+----+----+----+----+----+----+                              │
  │                                                                         │
  │  E = Eden, S = Survivor, O = Old, H = Humongous (large object), F = Free│
  │  G1 collects the regions with the most garbage first!                   │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: Java]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Demo Code                                                            │
  │                                                                          │
  │  import java.util.ArrayList;                                             │
  │  import java.util.List;                                                  │
  │                                                                          │
  │  public class JvmCrashDemo {                                             │
  │                                                                          │
  │      // 1. StackOverflowError                                            │
  │      // Caused by infinitely deep method calls exhausting the Thread Stack memory.│
  │      public static void causeStackOverflow() {                           │
  │          causeStackOverflow(); // Recursive call without base case       │
  │      }                                                                   │
  │                                                                          │
  │      // 2. OutOfMemoryError: Java heap space                             │
  │      // Caused by allocating objects until the Heap is entirely full.    │
  │      public static void causeOutOfMemory() {                             │
  │          List<byte[]> list = new ArrayList<>();                          │
  │          while (true) {                                                  │
  │              // Allocate 1MB continuously                                │
  │              list.add(new byte[1024 * 1024]);                            │
  │          }                                                               │
  │      }                                                                   │
  │                                                                          │
  │      public static void main(String[] args) {                            │
  │          if (args.length > 0 && args[0].equals("stack")) {               │
  │              System.out.println("Triggering StackOverflow...");          │
  │              causeStackOverflow();                                       │
  │          } else {                                                        │
  │              System.out.println("Triggering OutOfMemory...");            │
  │              causeOutOfMemory();                                         │
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
  │  import java.util.HashMap;                                               │
  │  import java.util.Map;                                                   │
  │  import java.util.UUID;                                                  │
  │                                                                          │
  │  public class MemoryLeakExample {                                        │
  │                                                                          │
  │      // BAD: Static collection. Lives for the lifetime of the application.│
  │      // If we put data in here and never remove it, the Heap will slowly fill up.│
  │      private static final Map<String, UserSession> SESSION_CACHE = new HashMap<>();│
  │                                                                          │
  │      static class UserSession {                                          │
  │          private final String sessionId;                                 │
  │          private final byte[] dataPayload = new byte[1024 * 100]; // 100KB payload│
  │                                                                          │
  │          public UserSession(String sessionId) {                          │
  │              this.sessionId = sessionId;                                 │
  │          }                                                               │
  │      }                                                                   │
  │                                                                          │
  │      public static void simulateUserLogins() throws InterruptedException {│
  │          int logins = 0;                                                 │
  │          while (true) {                                                  │
  │              String sessionId = UUID.randomUUID().toString();            │
  │                                                                          │
  │              // Memory Leak: We add sessions but never remove them when users log out!│
  │              SESSION_CACHE.put(sessionId, new UserSession(sessionId));   │
  │                                                                          │
  │              logins++;                                                   │
  │              if (logins % 1000 == 0) {                                   │
  │                  System.out.println("Active sessions: " + SESSION_CACHE.size());│
  │                  // In production, this would eventually crash with OutOfMemoryError.│
  │                  // FIX: Use an LRU Cache, WeakHashMap, or ensure explicit removal on logout.│
  │              }                                                           │
  │              Thread.sleep(1);                                            │
  │          }                                                               │
  │      }                                                                   │
  │                                                                          │
  │      public static void main(String[] args) throws InterruptedException {│
  │          simulateUserLogins();                                           │
  │      }                                                                   │
  │  }                                                                       │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  7. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: What is the difference between the Stack and the Heap?

  ANSWER:
    The Stack is per-thread, stores method frames, local primitive variables, and object references. It's fast and automatically managed (LIFO). The Heap is shared across all threads, stores the actual Objects, is slower to access, and requires Garbage Collection.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: When does an object become eligible for Garbage Collection?

  ANSWER:
    When there are no strong references to it reachable from any GC Root (like a live thread stack, static variable, or JNI reference).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: What is the generational hypothesis in Garbage Collection?

  ANSWER:
    "Most objects die young." Most objects created in Java are temporary (e.g., inside a method). Therefore, GCs split the heap into Young and Old. We run fast, frequent "Minor GCs" on the Young generation, and infrequent "Major GCs" on the Old generation.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: Explain how the Young Generation works (Eden, S0, S1).

  ANSWER:
    Objects are created in Eden. When Eden is full, a Minor GC occurs. Live objects are moved to S0. Next time Eden fills, live objects from Eden AND S0 are moved to S1, and S0 is cleared. They ping-pong between S0 and S1, incrementing their "age". Once age hits a threshold (e.g., 15), they are promoted to the Old generation.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: What causes a `java.lang.OutOfMemoryError: Metaspace`?

  ANSWER:
    The Metaspace (which holds class definitions) has filled up. This happens if the application dynamically generates too many classes at runtime (e.g., heavily using reflection, CGLib proxies, or deploying massive Spring applications without increasing `-XX:MaxMetaspaceSize`).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: What is the difference between Parallel GC and G1 GC?

  ANSWER:
    Parallel GC aims for maximum overall throughput (CPU time spent on app vs GC), but can have very long, unpredictable Stop-The-World pauses. G1 GC breaks the heap into regions and allows you to set a target pause time (e.g., 200ms). It prioritizes pausing for less time, even if it requires slightly more CPU overhead.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q7: How does ZGC achieve sub-millisecond pauses?

  ANSWER:
    ZGC does almost all its work—including compacting/moving objects—concurrently while the application threads are running. It uses "Colored Pointers" (storing GC metadata in the pointer bits) and Load Barriers (small code snippets inserted before object reads) to ensure the app thread safely reads an object even if the GC is currently moving it.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q8: What is a WeakReference and when would you use it?

  ANSWER:
    A reference that does not prevent its referent from being made finalizable, finalized, and then reclaimed by GC. Used primarily in `WeakHashMap` to associate metadata with an object without causing a memory leak if that object is no longer used elsewhere in the application.

────────────────────────────────────────────────────────────────────────────────
  8. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: The String Pool Trap

  java
  String s1 = "hello";
  String s2 = new String("hello");
  System.out.println(s1 == s2);

  SOLUTION:
    It prints false. s1 is in the String Pool (historically PermGen, now inside the Heap). s2 forces the creation of a brand new object on the Heap. Comparing with == compares references. Use .equals()!

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 2: The Finalizer Resurrection

  java
  class Zombie {
  static Zombie globalRef;
  @Override
  protected void finalize() throws Throwable {
  globalRef = this; // Resurrecting the object!
  }
  }

  SOLUTION:
    When the GC determines Zombie is unreachable, it runs finalize(). Inside, the object assigns itself to a static root, making it reachable again! The GC won't run finalize() a second time, leaving a confusing, un-killable object. (Note: finalize() is deprecated).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 3: The ThreadLocal Leak

  A Tomcat web server frequently crashes with OutOfMemoryError after a hot-deploy of a new WAR file.

  SOLUTION:
    The application uses ThreadLocal variables but doesn't clean them up (.remove()). The web server's Thread Pool keeps the threads alive forever. The ThreadLocal holds a reference to an object loaded by the application's ClassLoader. The ClassLoader, and thus all class definitions, can never be GC'd, leaking Metaspace/Heap on every deploy.

────────────────────────────────────────────────────────────────────────────────
  9. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  - Latency Spikes (The "GC Pause"): If a financial trading system or realtime multiplayer game uses a bad GC configuration, a 2-second Stop-The-World pause will disconnect players or lose money.
  - Heap Dumps & Profiling: When production crashes with OOM, engineers must download the `.hprof` file and use Eclipse MAT or VisualVM to find the GC Roots keeping the leaked objects alive.
  - Container Sizing (Docker/K8s): Setting container memory to 2GB but JVM Heap (`-Xmx`) to 2GB will cause the Linux OOM Killer to terminate the container, because JVM needs Heap + Metaspace + Stack + Native memory.

────────────────────────────────────────────────────────────────────────────────
  10. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

  -> File 003: 003_Virtual_Memory_Pages_PageFaults.md (How JVM heap memory maps to OS pages.)
  -> File 005: 005_Operating_System_Fundamentals.md (How OS threads relate to JVM threads and the thread stack.)

================================================================================
  END OF FILE 004
================================================================================
