================================================================================
  FILE 016: AVL and Red-Black Trees
  Section: B - DSA in Java
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  Self-Balancing Binary Search Trees ensure that operations (insert, delete, search) remain strictly logarithmic O(log N) by dynamically adjusting their structure to prevent severe skewing. AVL Trees and Red-Black Trees are the two most prominent self-balancing architectures.

  Prerequisites: Binary Search Trees.
  What you'll learn: The need for self-balancing, AVL balance factors, rotations (LL, RR, LR, RL), Red-Black tree properties, recoloring vs rotations, and why Java uses Red-Black trees in TreeMap.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  Self-Balancing
    Algorithms applied during insertion and deletion to keep tree height as close to O(log N) as possible.

  AVL Tree
    A strictly balanced BST where the height difference (Balance Factor) between left and right subtrees for any node is -1, 0, or +1.

  Rotations
    Local structural transformations (Left Rotation, Right Rotation) that restore balance without violating the BST property.

  Red-Black Tree
    A balanced BST that relaxes AVL's strict height bounds using coloring (Red/Black) to guarantee O(log N) while speeding up insertion/deletion.

  Black-Height
    The number of black nodes from a given node down to any of its descendant leaves. Must be equal for all paths.

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  AVL Right Rotation (LL Imbalance)                                      │
  │                                                                         │
  │        [Z] (BF=2)                 [Y]                                   │
  │        /                        /     \                                 │
  │      [Y] (BF=1)    ---->      [X]     [Z]                               │
  │      /   \                          /                                   │
  │    [X]   (T3)                     (T3)                                  │
  │                                                                         │
  │  Node Z is unbalanced. We perform a Right Rotation on Z.                │
  └─────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  Red-Black Tree Insertion (Recoloring)                                  │
  │                                                                         │
  │        [B: 10]                  [R: 10]                                 │
  │        /     \                  /     \                                 │
  │     [R: 5] [R: 15]   ---->   [B: 5] [B: 15]                             │
  │      /                         /                                        │
  │   [R: 2]                    [R: 2]                                      │
  │                                                                         │
  │  Red node (5) has a Red child (2) and Red sibling (15). Recoloring      │
  │  pushes Red up to the parent (10).                                      │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  Language: Java

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Simplified AVL Tree Rotation Snippets                                │
  │  class AVLNode {                                                         │
  │      int key, height;                                                    │
  │      AVLNode left, right;                                                │
  │      AVLNode(int d) { key = d; height = 1; }                             │
  │  }                                                                       │
  │                                                                          │
  │  public class AVLRotationDemo {                                          │
  │                                                                          │
  │      int height(AVLNode N) {                                             │
  │          return (N == null) ? 0 : N.height;                              │
  │      }                                                                   │
  │                                                                          │
  │      // Right Rotate                                                     │
  │      AVLNode rightRotate(AVLNode y) {                                    │
  │          AVLNode x = y.left;                                             │
  │          AVLNode T2 = x.right;                                           │
  │                                                                          │
  │          // Perform rotation                                             │
  │          x.right = y;                                                    │
  │          y.left = T2;                                                    │
  │                                                                          │
  │          // Update heights                                               │
  │          y.height = Math.max(height(y.left), height(y.right)) + 1;       │
  │          x.height = Math.max(height(x.left), height(x.right)) + 1;       │
  │                                                                          │
  │          return x; // New root                                           │
  │      }                                                                   │
  │                                                                          │
  │      // Get Balance Factor                                               │
  │      int getBalance(AVLNode N) {                                         │
  │          return (N == null) ? 0 : height(N.left) - height(N.right);      │
  │      }                                                                   │
  │  }                                                                       │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

  Language: Java

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  import java.util.TreeMap;                                               │
  │                                                                          │
  │  /**                                                                     │
  │   * Production usage of Red-Black Trees in Java via TreeMap.             │
  │   * TreeMap internally implements a Red-Black Tree, providing O(log N) time│
  │   * for containsKey, get, put, and remove.                               │
  │   */                                                                     │
  │  public class TreeMapProductionDemo {                                    │
  │      public static void main(String[] args) {                            │
  │          TreeMap<Integer, String> map = new TreeMap<>();                 │
  │                                                                          │
  │          // Insertions - internally handled by Red-Black insertion and rotations│
  │          map.put(10, "Ten");                                             │
  │          map.put(5, "Five");                                             │
  │          map.put(15, "Fifteen");                                         │
  │          map.put(2, "Two");                                              │
  │                                                                          │
  │          // Keys are kept sorted                                         │
  │          System.out.println("First Key: " + map.firstKey()); // 2        │
  │          System.out.println("Last Key: " + map.lastKey());   // 15       │
  │                                                                          │
  │          // Range queries                                                │
  │          System.out.println("SubMap: " + map.subMap(5, 16)); // {5=Five, 10=Ten, 15=Fifteen}│
  │      }                                                                   │
  │  }                                                                       │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  7. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: Why are Red-Black trees preferred over AVL trees in most standard libraries (like Java's TreeMap)?

  ANSWER:
    AVL trees are strictly balanced, meaning they require more rotations during insertion and deletion. Red-Black trees are loosely balanced, meaning fewer rotations for writes, making them faster for workloads heavy in insertions/deletions, while still maintaining O(log N) lookup.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: What are the primary properties of a Red-Black Tree?

  ANSWER:
    - Root is Black.
    - Every node is either Red or Black.
    - Red nodes cannot have Red children (no two consecutive reds).
    - Every path from a node to its descendant leaves contains the same number of Black nodes.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: In an AVL tree, when do you need an LR (Left-Right) rotation?

  ANSWER:
    When the imbalance occurs in the Right child of the Left child of the unbalanced node. First, left-rotate the left child, then right-rotate the unbalanced node.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: What is the maximum height of a Red-Black Tree?

  ANSWER:
    2 * log(N+1). An AVL tree is bounded tighter at ~1.44 * log(N).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: How does a TreeMap differ from a HashMap?

  ANSWER:
    HashMap offers O(1) average lookup/insertion but unordered keys. TreeMap offers O(log N) operations but keeps keys strictly ordered, allowing range queries and order statistics.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: Can a Red-Black tree have a leaf that is Red?

  ANSWER:
    Yes, but its null pointer children are technically considered Black leaves in RB theory.

────────────────────────────────────────────────────────────────────────────────
  8. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: The Infinite Spin

  AVLNode leftRotate(AVLNode x) {
      AVLNode y = x.right;
      x.right = y.left;
      y.left = x;
      // Forgot to update heights!
      return y;
  }

  SOLUTION:
    The rotation shifts nodes properly, but failing to update the `height` attributes will cause the `getBalance` logic on subsequent inserts to calculate entirely incorrect values, leading to skipped or infinite rotations.

────────────────────────────────────────────────────────────────────────────────
  9. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  - Java Collections Framework: `java.util.TreeMap` and `java.util.TreeSet` rely strictly on Red-Black Trees. `HashMap` uses Red-Black trees internally when a bucket's collision chain gets too long (Treeification).
  - Linux Kernel: Uses Red-Black trees for the Completely Fair Scheduler (CFS) to track process execution times.
  - In-Memory Range Queries: When caching requires fetching a range of data (e.g., getting all events between Timestamp A and Timestamp B), self-balancing trees are essential.

────────────────────────────────────────────────────────────────────────────────
  10. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

  -> File 015: Binary_Trees_BST.md (Foundation of Tree structures)
  -> File 017: BTrees_BPlusTrees.md (How trees adapt for Disk I/O rather than memory)
  -> File 019: HashTables_Hashing.md (When HashMap chains convert to Red-Black trees)

================================================================================
  END OF FILE 016
================================================================================
