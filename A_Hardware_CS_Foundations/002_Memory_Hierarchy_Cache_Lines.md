================================================================================
  FILE 002: Memory Hierarchy & Cache Lines
  Section: A - Hardware & CS Foundations
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  Memory Hierarchy & Cache Lines: Bridging the CPU-Memory Gap
  
  This document explores the memory hierarchy, focusing on CPU caches (L1, L2, L3) and how they mitigate the massive latency gap between CPU execution speeds and main memory (RAM) access times. You will understand cache lines, spatial and temporal locality, and how data layout in memory drastically affects software performance.
  Prerequisites: Understanding of basic CPU concepts and RAM.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  L1/L2/L3 Caches
    SRAM (Static RAM) memory built directly into or very close to the CPU die. They act as staging areas for data needed by the CPU.

  L1 Cache
    Smallest, fastest, per-core. Split into L1i (instructions) and L1d (data). (e.g., 32KB - 64KB, ~1 ns).

  L2 Cache
    Larger, slightly slower, typically per-core. (e.g., 256KB - 1MB, ~3-4 ns).

  L3 Cache
    Largest, slowest cache, usually shared across all cores on a CPU die. (e.g., 8MB - 64MB, ~10-15 ns).

  Main Memory (RAM)
    DRAM (Dynamic RAM). Much larger but slower than cache. (~50-100 ns).

  Cache Line (Cache Block)
    The smallest unit of data transferred between main memory and the cache. Almost universally 64 bytes in modern processors. When you read 1 byte, the CPU fetches the entire 64-byte chunk containing that byte into the cache.

  Locality of Reference
    

  Spatial Locality
    If a memory location is accessed, nearby memory locations are likely to be accessed soon (e.g., iterating through an array). Cache lines inherently exploit this.

  Temporal Locality
    If a memory location is accessed, it is likely to be accessed again soon (e.g., a loop counter variable). Caching keeps recently used data fast.

  Hardware Prefetcher
    CPU hardware that detects patterns in memory access (like sequential array reading) and speculatively loads upcoming cache lines into the cache before the CPU actually requests them.

  NUMA (Non-Uniform Memory Access)
    In multi-socket servers, memory is attached directly to specific CPUs. Accessing "local" memory (attached to your CPU) is fast, while accessing "remote" memory (attached to another CPU) is slower due to traversing the interconnect (e.g., QPI/UPI).

  Cache Associativity
    How memory blocks map to cache lines.

  Direct-Mapped
    Each memory block maps to exactly one cache line. Fast lookup, high conflict misses.

  Fully-Associative
    A memory block can go to any cache line. Lowest miss rate, but very slow/expensive to search.

  Set-Associative (e.g., 8-way)
    A compromise. Memory maps to a specific "set", but can occupy any of the N (e.g., 8) lines within that set.

  Cache Eviction Policies
    When cache is full, which block gets kicked out?

  LRU (Least Recently Used)
    Most common. Evict the block that hasn't been accessed for the longest time.

  FIFO (First In First Out)
    Evict the oldest block.

  Random
    Pick a block randomly (used in some ARM architectures for simplicity).

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  MEMORY HIERARCHY PYRAMID                                               │
  │                                                                         │
  │                 /\                                                      │
  │                /  \         Latency        Size (Typical)               │
  │               /Reg-\         ~0.3 ns       Bytes                        │
  │              /isters\                                                   │
  │             /--------\                                                  │
  │            / L1 Cache \       ~1 ns        32KB - 64KB (Per Core)       │
  │           /------------\                                                │
  │          /   L2 Cache   \     ~3-4 ns      256KB - 2MB (Per Core)       │
  │         /----------------\                                              │
  │        /     L3 Cache     \   ~10-20 ns    8MB - 64MB (Shared)          │
  │       /--------------------\                                            │
  │      /     Main Memory      \ ~50-100 ns   16GB - 1TB+                  │
  │     /         (RAM)          \                                          │
  │    /--------------------------\                                         │
  │   /      Local Disk (SSD/HDD)  \ ~10-100us/ms  Terabytes                │
  │  /------------------------------\                                       │
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
  │  import java.util.LinkedList;                                            │
  │  import java.util.List;                                                  │
  │                                                                          │
  │  public class CacheLocalityDemo {                                        │
  │      private static final int ELEMENTS = 10_000_000;                     │
  │                                                                          │
  │      public static void main(String[] args) {                            │
  │          // Pre-allocate and fill both collections                       │
  │          int[] primitiveArray = new int[ELEMENTS];                       │
  │          List<Integer> linkedList = new LinkedList<>();                  │
  │                                                                          │
  │          for (int i = 0; i < ELEMENTS; i++) {                            │
  │              primitiveArray[i] = i;                                      │
  │              linkedList.add(i);                                          │
  │          }                                                               │
  │                                                                          │
  │          // Test Array (High Spatial Locality)                           │
  │          long startArray = System.nanoTime();                            │
  │          long sumArray = 0;                                              │
  │          for (int i = 0; i < ELEMENTS; i++) {                            │
  │              sumArray += primitiveArray[i];                              │
  │          }                                                               │
  │          long endArray = System.nanoTime();                              │
  │                                                                          │
  │          // Test LinkedList (Low Spatial Locality)                       │
  │          long startList = System.nanoTime();                             │
  │          long sumList = 0;                                               │
  │          for (Integer val : linkedList) {                                │
  │              sumList += val;                                             │
  │          }                                                               │
  │          long endList = System.nanoTime();                               │
  │                                                                          │
  │          System.out.println("Array traversal time (ms): " + (endArray - startArray) / 1_000_000);│
  │          System.out.println("LinkedList traversal time (ms): " + (endList - startList) / 1_000_000);│
  │          // Note: Array is typically 10x-50x faster due to cache lines and prefetching!│
  │      }                                                                   │
  │  }                                                                       │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: C++]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │                                                                          │
  │  #include <iostream>                                                     │
  │  #include <thread>                                                       │
  │  #include <vector>                                                       │
  │  #include <chrono>                                                       │
  │                                                                          │
  │  // Using C++17 hardware_destructive_interference_size which is usually 64│
  │  #ifdef __cpp_lib_hardware_interference_size                             │
  │      using std::hardware_destructive_interference_size;                  │
  │  #else                                                                   │
  │      constexpr std::size_t hardware_destructive_interference_size = 64;  │
  │  #endif                                                                  │
  │                                                                          │
  │  // BAD: Counters are adjacent. Thread 0 modifies counter[0],            │
  │  // invalidating counter[1] in Thread 1's L1 cache!                      │
  │  struct BadCounters {                                                    │
  │      long long counter[2] = {0, 0};                                      │
  │  };                                                                      │
  │                                                                          │
  │  // GOOD: Aligning variables to cache line boundaries prevents false sharing.│
  │  struct GoodCounters {                                                   │
  │      alignas(hardware_destructive_interference_size) long long counter0 = 0;│
  │      alignas(hardware_destructive_interference_size) long long counter1 = 0;│
  │  };                                                                      │
  │                                                                          │
  │  template <typename T>                                                   │
  │  void worker(T* counters, int index) {                                   │
  │      for (int i = 0; i < 100000000; ++i) {                               │
  │          if constexpr (std::is_same_v<T, BadCounters>) {                 │
  │              counters->counter[index]++;                                 │
  │          } else {                                                        │
  │              if (index == 0) counters->counter0++;                       │
  │              else counters->counter1++;                                  │
  │          }                                                               │
  │      }                                                                   │
  │  }                                                                       │
  │                                                                          │
  │  int main() {                                                            │
  │      BadCounters bad;                                                    │
  │      GoodCounters good;                                                  │
  │                                                                          │
  │      auto run_test = [](auto* obj, const char* name) {                   │
  │          auto start = std::chrono::high_resolution_clock::now();         │
  │          std::thread t1(worker<std::remove_pointer_t<decltype(obj)>>, obj, 0);│
  │          std::thread t2(worker<std::remove_pointer_t<decltype(obj)>>, obj, 1);│
  │          t1.join();                                                      │
  │          t2.join();                                                      │
  │          auto end = std::chrono::high_resolution_clock::now();           │
  │          std::cout << name << " time: "                                  │
  │                    << std::chrono::duration_cast<std::chrono::milliseconds>(end - start).count() │
  │                    << " ms\n";                                           │
  │      };                                                                  │
  │                                                                          │
  │      run_test(&bad, "Bad Counters (False Sharing)");                     │
  │      run_test(&good, "Good Counters (Padded)");                          │
  │                                                                          │
  │      return 0;                                                           │
  │  }                                                                       │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  7. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: What is a Cache Miss and what are the three types (The 3 C's)?

  ANSWER:
    A cache miss happens when requested data is not in cache. 
       - Compulsory: First time data is accessed (inevitable).
       - Capacity: Cache is too small to hold all needed working set data.
       - Conflict: Multiple memory blocks map to the same set in set-associative cache and evict each other, even if overall cache isn't full.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: Explain the 64-byte cache line concept.

  ANSWER:
    Memory isn't read byte-by-byte. It's read in 64-byte chunks. If you read a 4-byte integer at memory address `0x1000`, the CPU loads bytes `0x1000` to `0x103F` into the L1 cache. Subsequent reads to adjacent memory hit the L1 cache instantly.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: What is False Sharing and how do you fix it?

  ANSWER:
    False sharing happens when two CPU cores independently modify separate variables that share the same 64-byte cache line. The cache coherence protocol (like MESI) forces one core to invalidate the other core's cache line, causing memory stalls. Fix it by adding padding (dummy variables) between the variables so they sit on different cache lines, or using `alignas(64)`.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: Why is looping over a 2D array row-by-row faster than column-by-column in C/Java?

  ANSWER:
    C and Java store 2D arrays in Row-Major order. Accessing row-by-row means memory is accessed sequentially, taking advantage of spatial locality and hardware prefetching (fetching entire 64-byte cache lines). Column-by-column strides across memory, causing cache misses on almost every read.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: What is NUMA and why should a software engineer care?

  ANSWER:
    Non-Uniform Memory Access. On modern servers, RAM is split among CPU sockets. Accessing memory on a different socket is slower. Database engines (like SQL Server, Postgres) or JVMs must be NUMA-aware to allocate memory on the same socket as the thread processing the data to maximize performance.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: How does the Hardware Prefetcher work?

  ANSWER:
    It's a CPU hardware component that monitors memory access patterns. If it sees you accessing `array[0], array[1], array[2]`, it predicts you'll want `array[3]` and fetches that cache line from RAM into L1 cache before you even execute the instruction requesting it.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q7: What is Cache Coherence?

  ANSWER:
    In multi-core systems, each core has its own L1/L2 cache. If Core 1 modifies variable X, Core 2's cached copy of X is now stale. Cache coherence protocols (like MESI - Modified, Exclusive, Shared, Invalid) ensure all cores see a consistent view of memory via the system bus.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q8: What's the difference between fully associative and direct-mapped cache?

  ANSWER:
    Direct-mapped: A memory address maps to exactly ONE location in cache. Easy hardware, but high conflict misses. Fully associative: A memory address can be stored ANYWHERE in the cache. No conflict misses, but looking up data requires searching every single cache slot simultaneously (expensive hardware). Modern CPUs use N-way set-associative (a compromise).

────────────────────────────────────────────────────────────────────────────────
  8. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: The Matrix Traversal

  c
  int matrix[1000][1000];
  long sum = 0;
  // What is inefficient here?
  for (int col = 0; col < 1000; col++) {
  for (int row = 0; row < 1000; row++) {
  sum += matrix[row][col];
  }
  }

  SOLUTION:
    It traverses column-by-column. C uses row-major ordering. Every read skips ahead by 1000 integers (~4000 bytes), constantly missing the 64-byte cache line and rendering the hardware prefetcher useless. Swap the loops!

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 2: The Bloated Struct Array

  cpp
  struct Player {
  bool isActive;           // 1 byte
  // padding will occur
  double position[3];      // 24 bytes
  // ... 100 more bytes of data ...
  };
  Player players[100000];
  // Loop just checking active status
  int count = 0;
  for(int i = 0; i < 100000; i++) {
  if(players[i].isActive) count++;
  }

  SOLUTION:
    This is an "Array of Structs" (AoS). To check isActive, we load the whole 64-byte cache line, getting isActive and a bunch of useless position data. For the next player, we likely need to fetch a new cache line. Memory bandwidth is wasted.
    Use "Struct of Arrays" (SoA): bool isActive[100000]; double posX[100000];. Then the loop packs 64 isActive booleans into a single cache line! Data-Oriented Design (DOD).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 3: The Slow Multi-threading

  You split a loop processing an array of 1M elements across 4 threads. You pass a shared array of 4 long variables for each thread to write its intermediate sum. It is slower than a single thread.

  SOLUTION:
    The 4 long variables (4 * 8 = 32 bytes) easily fit into a single 64-byte cache line. All 4 threads are blasting writes to the same cache line, triggering False Sharing and constant L1 cache invalidations across the 4 cores.

────────────────────────────────────────────────────────────────────────────────
  9. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  - High-Performance Computing & Game Dev: Game engines (like Unity's DOTS) and trading systems heavily rely on Data-Oriented Design. Structuring data in Arrays of Structs vs Structs of Arrays dictates whether you hit 60 FPS or 15 FPS strictly due to cache misses.
  - Database Architecture: Databases map data to 8KB or 16KB pages. Understanding how B-Trees fit into cache lines dictates indexing performance.
  - Cloud Infrastructure: Multi-tenant VMs on NUMA nodes can suffer "noisy neighbor" latency spikes if NUMA boundaries and CPU pinning aren't respected by the hypervisor.

────────────────────────────────────────────────────────────────────────────────
  10. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

  -> File 001: 001_CPU_Architecture_Instruction_Pipeline.md (How the CPU processes the data fetched by the cache.)
  -> File 003: 003_Virtual_Memory_Pages_PageFaults.md (How RAM is mapped to disk (the next, slowest level of the hierarchy).)

================================================================================
  END OF FILE 002
================================================================================
