================================================================================
  FILE 019: Hash Tables and Hashing
  Section: B - DSA in Java
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  A Hash Table (or Hash Map) maps keys to values for highly efficient O(1) average time lookups, insertions, and deletions. It relies on a mathematical Hash Function to convert keys into array indices. Understanding Java's HashMap internals, collision resolution, and the hashCode/equals contract is mandatory for Java interviews.

  Prerequisites: Arrays, Linked Lists.
  What you'll learn: Hash functions, hashCode contracts, collision resolution (Separate Chaining vs Open Addressing), Load Factors, and Java 8's Treeification.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  Hash Function
    An algorithm mapping data of arbitrary size to a fixed-size integer (hash code).

  Bucket / Slot
    An index in the underlying array of the hash table.

  Collision
    When two different keys produce the same hash code or map to the same bucket index.

  Separate Chaining
    A collision resolution strategy where each bucket holds a Linked List (or Tree) of entries.

  Open Addressing
    A collision resolution strategy where all elements are stored directly in the array. If a bucket is occupied, it probes for the next empty bucket (Linear, Quadratic, Double Hashing).

  Load Factor
    The ratio of elements to capacity (Size / Capacity). Determines when the hash table should resize.

  Rehashing
    Creating a larger array (usually 2x) and redistributing all existing elements into the new array when the load factor threshold is crossed.

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  Java HashMap: Separate Chaining & Treeification                        │
  │                                                                         │
  │  Array Capacity = 8 (Indices 0 to 7)                                    │
  │                                                                         │
  │  [0] -> null                                                            │
  │  [1] -> [Key: "A", Val: 1] -> null                                      │
  │  [2] -> [Key: "B", Val: 2] -> [Key: "C", Val: 3] -> null  <-- Linked List (Chain) │
  │  [3] -> null                                                            │
  │  [4] -> (Red-Black Tree for high collision!)                            │
  │           [K: "X"]                                                      │
  │           /      \                                                      │
  │        [K:"Y"]  [K:"Z"]                                                 │
  │  [5] -> null                                                            │
  └─────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  Open Addressing (Linear Probing)                                       │
  │                                                                         │
  │  Insert 10 (hash 2), Insert 20 (hash 2), Insert 30 (hash 2)             │
  │  [0] : null                                                             │
  │  [1] : null                                                             │
  │  [2] : [10]  <-- 10 goes to target hash                                 │
  │  [3] : [20]  <-- 20 hits collision at 2, probes +1 to 3                 │
  │  [4] : [30]  <-- 30 hits collision at 2, probes 3 (full), probes +1 to 4│
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  Language: Java

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  import java.util.Objects;                                               │
  │                                                                          │
  │  // Defining a custom object as a HashMap key requires overriding equals and hashCode │
  │  class UserKey {                                                         │
  │      String email;                                                       │
  │      int id;                                                             │
  │                                                                          │
  │      public UserKey(String email, int id) {                              │
  │          this.email = email;                                             │
  │          this.id = id;                                                   │
  │      }                                                                   │
  │                                                                          │
  │      @Override                                                           │
  │      public boolean equals(Object o) {                                   │
  │          if (this == o) return true;                                     │
  │          if (o == null || getClass() != o.getClass()) return false;      │
  │          UserKey userKey = (UserKey) o;                                  │
  │          return id == userKey.id && Objects.equals(email, userKey.email);│
  │      }                                                                   │
  │                                                                          │
  │      @Override                                                           │
  │      public int hashCode() {                                             │
  │          // Effective Java pattern: multiply by prime number 31          │
  │          return Objects.hash(email, id);                                 │
  │      }                                                                   │
  │  }                                                                       │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

  Language: Java

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  /**                                                                     │
  │   * Simplified Custom HashMap implementation (Array + Separate Chaining).│
  │   */                                                                     │
  │  public class CustomHashMap<K, V> {                                      │
  │      private class Node {                                                │
  │          K key;                                                          │
  │          V value;                                                        │
  │          Node next;                                                      │
  │          public Node(K key, V value) { this.key = key; this.value = value; } │
  │      }                                                                   │
  │                                                                          │
  │      private Node[] buckets;                                             │
  │      private int size;                                                   │
  │      private static final int INITIAL_CAPACITY = 16;                     │
  │      private static final float LOAD_FACTOR = 0.75f;                     │
  │                                                                          │
  │      @SuppressWarnings("unchecked")                                      │
  │      public CustomHashMap() {                                            │
  │          buckets = new CustomHashMap.Node[INITIAL_CAPACITY];             │
  │          size = 0;                                                       │
  │      }                                                                   │
  │                                                                          │
  │      private int getBucketIndex(K key) {                                 │
  │          int hash = key == null ? 0 : key.hashCode();                    │
  │          // Bitwise AND against capacity-1 to get array index (capacity must be power of 2) │
  │          return (hash ^ (hash >>> 16)) & (buckets.length - 1);           │
  │      }                                                                   │
  │                                                                          │
  │      public void put(K key, V value) {                                   │
  │          int index = getBucketIndex(key);                                │
  │          Node head = buckets[index];                                     │
  │          Node curr = head;                                               │
  │                                                                          │
  │          while (curr != null) {                                          │
  │              if (Objects.equals(curr.key, key)) {                        │
  │                  curr.value = value; // Update existing                  │
  │                  return;                                                 │
  │              }                                                           │
  │              curr = curr.next;                                           │
  │          }                                                               │
  │                                                                          │
  │          // Insert at head                                               │
  │          Node newNode = new Node(key, value);                            │
  │          newNode.next = head;                                            │
  │          buckets[index] = newNode;                                       │
  │          size++;                                                         │
  │                                                                          │
  │          if ((float) size / buckets.length > LOAD_FACTOR) {              │
  │              // resize(); // Omitted for brevity                         │
  │          }                                                               │
  │      }                                                                   │
  │                                                                          │
  │      public V get(K key) {                                               │
  │          int index = getBucketIndex(key);                                │
  │          Node curr = buckets[index];                                     │
  │          while (curr != null) {                                          │
  │              if (Objects.equals(curr.key, key)) return curr.value;       │
  │              curr = curr.next;                                           │
  │          }                                                               │
  │          return null;                                                    │
  │      }                                                                   │
  │  }                                                                       │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  7. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: Why does Java's HashMap calculate index using `(n-1) & hash` instead of `hash % n`?

  ANSWER:
    Bitwise AND is heavily optimized by CPUs and is significantly faster than the modulo operator. This only works perfectly when the capacity `n` is a power of 2 (e.g., 16, 32, 64).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: Explain the `equals()` and `hashCode()` contract in Java.

  ANSWER:
    - If `a.equals(b)` is true, `a.hashCode()` MUST equal `b.hashCode()`.
    - If `a.hashCode() == b.hashCode()`, `a.equals(b)` is NOT necessarily true (Collision).
    - If you override `equals`, you MUST override `hashCode`.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: What is Treeification in Java 8?

  ANSWER:
    When a bucket's linked list size exceeds 8 elements (and total capacity > 64), Java converts the list into a Red-Black Tree. This prevents worst-case lookup degradation from O(N) to O(log N) during severe collisions.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: Why is the default Load Factor 0.75?

  ANSWER:
    It represents the mathematical sweet spot (Poisson distribution) between time complexity (too high = many collisions, slow lookups) and space complexity (too low = sparse array, wasted memory).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: What is Open Addressing vs Separate Chaining?

  ANSWER:
    Separate Chaining uses linked lists outside the main array structure. Open Addressing keeps all data in the array; if full, it finds the next open slot. Open addressing is more cache-friendly but degrades terribly at high load factors.

────────────────────────────────────────────────────────────────────────────────
  8. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: The Lost Object

  Map<Point, String> map = new HashMap<>();
  Point p1 = new Point(1, 2);
  map.put(p1, "Origin");
  p1.x = 99; // Modifying the object!
  System.out.println(map.get(p1)); // Returns null!

  SOLUTION:
    HashMaps rely on the `hashCode` remaining constant while the object is in the map. By changing `p1.x`, its hash code changed. When `get()` hashes `p1`, it maps to a completely different bucket, returning `null`. Keys should generally be Immutable.

────────────────────────────────────────────────────────────────────────────────
  9. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  - Caching: Memcached and Redis are essentially distributed hash tables.
  - De-duplication: Tracking seen IP addresses, URLs, or transactions quickly.
  - Database Joins: "Hash Joins" are a primary database algorithm where one table is hashed in memory, and the other is scanned against it for matches.

────────────────────────────────────────────────────────────────────────────────
  10. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

  -> File 016: AVL_RedBlack_Trees.md (Treeification internals)
  -> File 001: Arrays_Strings.md (Bitwise operations for indexing)

================================================================================
  END OF FILE 019
================================================================================
