================================================================================
  FILE 017: B-Trees and B+Trees
  Section: B - DSA in Java
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  B-Trees and B+Trees are self-balancing search trees specifically designed for storage systems that read and write large blocks of data, like hard drives or SSDs. Unlike binary trees which are narrow and deep, B-Trees are wide and shallow, severely reducing the number of disk I/O operations required to find a record.

  Prerequisites: BSTs, Disk I/O vs Memory architecture.
  What you'll learn: Why binary trees fail on disk, B-Tree properties and node splitting, B+Tree structure (internal index nodes + leaf linked list), and how these power systems like PostgreSQL and SQLite.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  Disk Page / Block
    The minimum unit of data transferred between disk and memory (often 4KB or 8KB).

  B-Tree
    A generalized search tree where nodes can have multiple keys and multiple children. Keys are kept sorted.

  Minimum Degree (t)
    Defines the bounds on the number of keys a node can hold. Every node (except root) must have at least t-1 keys and at most 2t-1 keys.

  Node Splitting
    When an insertion causes a node to exceed 2t-1 keys, it splits into two nodes, and the median key moves up to the parent.

  B+Tree
    A variant of a B-Tree where all data/records are stored ONLY in the leaf nodes. Internal nodes contain only keys (used as routing indexes). Leaf nodes form a linked list for fast range queries.

  Fan-out
    The maximum number of children a node can have. High fan-out keeps the tree extremely shallow.

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  B-Tree Node Splitting (Degree t=2, max keys=3)                         │
  │                                                                         │
  │  Inserting 40 into full node [10, 20, 30]:                              │
  │  1. Node overflows: [10, 20, 30, 40]                                    │
  │  2. Median (20) moves up to parent.                                     │
  │  3. Node splits into [10] and [30, 40].                                 │
  │                                                                         │
  │        [... 20 ...]                                                     │
  │           /    \                                                        │
  │        [10]    [30, 40]                                                 │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  B+Tree Architecture                                                    │
  │                                                                         │
  │  Internal (Index):         [ 50 ]                                       │
  │                           /      \                                      │
  │  Internal (Index):   [ 25 ]      [ 75 ]                                 │
  │                      /    \      /    \                                 │
  │  Leaves (Data): [10,20]->[30,40]->[60,70]->[80,90]                      │
  │                                                                         │
  │  Notice how leaves are linked (->). A range query SELECT * WHERE val    │
  │  BETWEEN 20 AND 80 finds 20, then just traverses the linked list!       │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  Language: Java

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Simplified B-Tree Search logic (Conceptual)                          │
  │  class BTreeNode {                                                       │
  │      int[] keys;                                                         │
  │      BTreeNode[] children;                                               │
  │      int n; // Current number of keys                                    │
  │      boolean leaf;                                                       │
  │                                                                          │
  │      // O(log t) binary search within a node, O(log_t N) traversing down │
  │      public BTreeNode search(int k) {                                    │
  │          int i = 0;                                                      │
  │          // Find the first key greater than or equal to k                │
  │          while (i < n && k > keys[i]) {                                  │
  │              i++;                                                        │
  │          }                                                               │
  │                                                                          │
  │          // If the found key is equal to k, return this node             │
  │          if (i < n && keys[i] == k) {                                    │
  │              return this;                                                │
  │          }                                                               │
  │                                                                          │
  │          // If key is not found and this is a leaf node                  │
  │          if (leaf) {                                                     │
  │              return null;                                                │
  │          }                                                               │
  │                                                                          │
  │          // Go to the appropriate child                                  │
  │          return children[i].search(k);                                   │
  │      }                                                                   │
  │  }                                                                       │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

  Language: Java

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Because full B-Tree implementations are hundreds of lines of code    │
  │  // primarily managing arrays and splits, production systems use B+Trees │
  │  // deeply integrated with File I/O. In Java, B-Tree concepts are used   │
  │  // in libraries like MapDB or embedded databases like H2.               │
  │                                                                          │
  │  // Conceptual B+Tree Range Query Simulation                             │
  │  public class BPlusTreeRangeQuery {                                      │
  │      class LeafNode {                                                    │
  │          int[] keys;                                                     │
  │          String[] values; // Actual Data                                 │
  │          LeafNode next;   // Linked List pointer                         │
  │      }                                                                   │
  │                                                                          │
  │      // Given the starting leaf node found via O(log N) tree traversal   │
  │      public void executeRangeQuery(LeafNode start, int minKey, int maxKey) { │
  │          LeafNode curr = start;                                          │
  │          while (curr != null) {                                          │
  │              for (int i = 0; i < curr.keys.length; i++) {                │
  │                  if (curr.keys[i] >= minKey && curr.keys[i] <= maxKey) { │
  │                      System.out.println("Found: " + curr.values[i]);     │
  │                  }                                                       │
  │                  if (curr.keys[i] > maxKey) {                            │
  │                      return; // Stop scanning once we exceed max bound   │
  │                  }                                                       │
  │              }                                                           │
  │              curr = curr.next; // Follow linked list to next disk page   │
  │          }                                                               │
  │      }                                                                   │
  │  }                                                                       │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  7. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: Why not use a Red-Black tree for a database index?

  ANSWER:
    Red-Black trees have a fan-out of 2. A tree with 1 million records would have a height of ~20. Traversing it requires ~20 pointer dereferences, which in a DB means 20 random Disk I/O seeks (very slow). A B+Tree with fan-out 100 has a height of ~3, needing only 3 disk seeks.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: What is the main advantage of a B+Tree over a B-Tree?

  ANSWER:
    In a B+Tree, internal nodes don't store data, only keys. This means internal nodes can hold significantly more keys per disk page (higher fan-out), making the tree shallower. Additionally, the leaf-node linked list makes range queries blazing fast.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: How does a B-Tree determine its degree (t)?

  ANSWER:
    It is calculated based on the OS disk page size (e.g., 4KB) minus node overhead, divided by the size of a key-pointer pair. The goal is to fit exactly one node into one disk page.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: What happens when a B-Tree root node splits?

  ANSWER:
    The median key moves up into a new root node, and the height of the tree increases by 1. This is the only way a B-Tree grows in height.

────────────────────────────────────────────────────────────────────────────────
  8. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: The Memory-Bound B-Tree

  Design Flaw: A developer implements a B-Tree in Java but uses `ArrayList<Object>` for `keys` and `children`, constantly resizing and creating objects.

  SOLUTION:
    B-Trees are meant to optimize storage layouts. Using dynamic object lists in Java scatters the node data all over the heap (losing CPU cache locality) and adds massive object header overhead. Production B-Trees in Java use pre-allocated flat byte arrays (`byte[]`) or `ByteBuffer` aligned to page sizes.

────────────────────────────────────────────────────────────────────────────────
  9. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  - Relational Databases (PostgreSQL, MySQL, Oracle): The default index type (CREATE INDEX) is a B+Tree.
  - File Systems (NTFS, Ext4, APFS): Use B-Trees to index directory structures and file metadata blocks.
  - Embedded DBs (SQLite, Android Room): B-Trees are the backbone of SQLite storage files.

────────────────────────────────────────────────────────────────────────────────
  10. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

  -> File 016: AVL_RedBlack_Trees.md (Memory-optimized balanced trees vs Disk-optimized B-trees)
  -> File 028: PostgreSQL_MVCC.md (How PostgreSQL uses B+Trees in conjunction with visibility maps)
  -> File 080: Android_Room.md (SQLite B-Tree usage on mobile)

================================================================================
  END OF FILE 017
================================================================================
