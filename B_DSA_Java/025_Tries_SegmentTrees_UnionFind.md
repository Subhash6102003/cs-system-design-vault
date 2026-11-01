================================================================================
  FILE 025: Advanced Data Structures - Tries, Segment Trees, and Union-Find
  Section: B - DSA in Java
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  Advanced DSA: Tries, Segment Trees, and Union-Find (DSU)
  This file tackles three specialized data structures that act as "secret weapons" for specific classes of problems. 
  Prerequisites: Trees, Arrays, and basic Graph concepts.
  What you'll learn: How to implement a Trie for blazing-fast prefix matching, a Segment Tree for logarithmic range queries/updates, and Disjoint Set Union (Union-Find) for dynamic connectivity and graph cycles.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  Trie
    A tree-like data structure used to store a dynamic set of strings where keys are usually strings. Highly efficient for prefix searches (autocomplete, spell checkers).

  Node Structure
    Contains an array of children (e.g., `TrieNode[] children = new TrieNode[26]`) or a HashMap, and a boolean `isEndOfWord`.

  Time Complexity
    O(L) for insert and search, where L is the length of the word.

  Segment Tree
    A binary tree used for storing intervals or segments. It allows querying which of the stored segments contain a given point, or querying the sum/min/max of an array range in O(log N) time.

  Lazy Propagation
    An optimization technique for Segment Trees to delay updates to descendant nodes until required, keeping range updates O(log N).

  Union-Find
    A data structure that keeps track of a set of elements partitioned into a number of disjoint (non-overlapping) subsets.

  Find
    Determine which subset a particular element is in. Used to check if two elements are in the same subset.

  Union
    Join two subsets into a single subset.

  Path Compression
    Flattens the tree structure during `find()` so subsequent calls are faster.

  Union by Rank/Size
    Attaches the smaller tree to the root of the larger tree to keep trees shallow.

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  Trie Example                                                           │
  │                                                                         │
  │  Inserting "CAT", "CAR", and "DOG"                                      │
  │                                                                         │
  │           [Root]                                                        │
  │          /      \                                                       │
  │         C        D                                                      │
  │        /          \                                                     │
  │       A            O                                                    │
  │      / \            \                                                   │
  │    *T   *R           *G    (* indicates isEndOfWord = true)             │
  └─────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  Union-Find (Path Compression)                                          │
  │                                                                         │
  │  Suppose we have a degenerate tree: A -> B -> C -> D                    │
  │  Calling find(A) with path compression flattens it:                     │
  │                                                                         │
  │  Before:          After find(A):                                        │
  │     D                 D                                                 │
  │     |                /|\                                                │
  │     C               A B C                                               │
  │     |                                                                   │
  │     B                                                                   │
  │     |                                                                   │
  │     A                                                                   │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  Language: Java

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  public class UnionFind {                                                │
  │      private int[] root;                                                 │
  │      private int[] rank;                                                 │
  │      private int count; // Number of distinct sets                       │
  │                                                                          │
  │      public UnionFind(int size) {                                        │
  │          root = new int[size];                                           │
  │          rank = new int[size];                                           │
  │          count = size;                                                   │
  │          for (int i = 0; i < size; i++) {                                │
  │              root[i] = i; // Initially, every node is its own root       │
  │              rank[i] = 1;                                                │
  │          }                                                               │
  │      }                                                                   │
  │                                                                          │
  │      // Find with Path Compression                                       │
  │      public int find(int x) {                                            │
  │          if (x == root[x]) {                                             │
  │              return x;                                                   │
  │          }                                                               │
  │          return root[x] = find(root[x]); // Path compression             │
  │      }                                                                   │
  │                                                                          │
  │      // Union by Rank                                                    │
  │      public boolean union(int x, int y) {                                │
  │          int rootX = find(x);                                            │
  │          int rootY = find(y);                                            │
  │                                                                          │
  │          if (rootX != rootY) {                                           │
  │              if (rank[rootX] > rank[rootY]) {                            │
  │                  root[rootY] = rootX;                                    │
  │              } else if (rank[rootX] < rank[rootY]) {                     │
  │                  root[rootX] = rootY;                                    │
  │              } else {                                                    │
  │                  root[rootY] = rootX;                                    │
  │                  rank[rootX] += 1;                                       │
  │              }                                                           │
  │              count--; // Two sets merged into one                        │
  │              return true;                                                │
  │          }                                                               │
  │          return false; // Already in the same set (Cycle detected!)      │
  │      }                                                                   │
  │                                                                          │
  │      public int getCount() {                                             │
  │          return count;                                                   │
  │      }                                                                   │
  │  }                                                                       │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

  Language: Java

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Problem 1: Implement Trie (Prefix Tree)                              │
  │  class Trie {                                                            │
  │      class TrieNode {                                                    │
  │          TrieNode[] children = new TrieNode[26];                         │
  │          boolean isEndOfWord = false;                                    │
  │      }                                                                   │
  │                                                                          │
  │      private TrieNode root;                                              │
  │                                                                          │
  │      public Trie() {                                                     │
  │          root = new TrieNode();                                          │
  │      }                                                                   │
  │                                                                          │
  │      public void insert(String word) {                                   │
  │          TrieNode curr = root;                                           │
  │          for (char c : word.toCharArray()) {                             │
  │              int index = c - 'a';                                        │
  │              if (curr.children[index] == null) {                         │
  │                  curr.children[index] = new TrieNode();                  │
  │              }                                                           │
  │              curr = curr.children[index];                                │
  │          }                                                               │
  │          curr.isEndOfWord = true;                                        │
  │      }                                                                   │
  │                                                                          │
  │      public boolean search(String word) {                                │
  │          TrieNode node = getNode(word);                                  │
  │          return node != null && node.isEndOfWord;                        │
  │      }                                                                   │
  │                                                                          │
  │      public boolean startsWith(String prefix) {                          │
  │          return getNode(prefix) != null;                                 │
  │      }                                                                   │
  │                                                                          │
  │      private TrieNode getNode(String str) {                              │
  │          TrieNode curr = root;                                           │
  │          for (char c : str.toCharArray()) {                              │
  │              int index = c - 'a';                                        │
  │              if (curr.children[index] == null) return null;              │
  │              curr = curr.children[index];                                │
  │          }                                                               │
  │          return curr;                                                    │
  │      }                                                                   │
  │  }                                                                       │
  │                                                                          │
  │  // Problem 2: Number of Provinces (Union-Find)                          │
  │  class SolutionProvinces {                                               │
  │      public int findCircleNum(int[][] isConnected) {                     │
  │          int n = isConnected.length;                                     │
  │          UnionFind uf = new UnionFind(n); // Using the UnionFind class from above│
  │                                                                          │
  │          for (int i = 0; i < n; i++) {                                   │
  │              for (int j = i + 1; j < n; j++) {                           │
  │                  if (isConnected[i][j] == 1) {                           │
  │                      uf.union(i, j);                                     │
  │                  }                                                       │
  │              }                                                           │
  │          }                                                               │
  │          return uf.getCount(); // Returns number of disjoint sets        │
  │      }                                                                   │
  │  }                                                                       │
  │                                                                          │
  │  // Problem 3: Range Sum Query - Mutable (Segment Tree)                  │
  │  class NumArray {                                                        │
  │      int[] tree;                                                         │
  │      int n;                                                              │
  │                                                                          │
  │      public NumArray(int[] nums) {                                       │
  │          if (nums.length > 0) {                                          │
  │              n = nums.length;                                            │
  │              tree = new int[n * 2];                                      │
  │              buildTree(nums);                                            │
  │          }                                                               │
  │      }                                                                   │
  │                                                                          │
  │      private void buildTree(int[] nums) {                                │
  │          for (int i = n, j = 0;  i < 2 * n; i++,  j++)                   │
  │              tree[i] = nums[j];                                          │
  │          for (int i = n - 1; i > 0; --i)                                 │
  │              tree[i] = tree[i * 2] + tree[i * 2 + 1];                    │
  │      }                                                                   │
  │                                                                          │
  │      public void update(int pos, int val) {                              │
  │          pos += n;                                                       │
  │          tree[pos] = val;                                                │
  │          while (pos > 0) {                                               │
  │              int left = pos;                                             │
  │              int right = pos;                                            │
  │              if (pos % 2 == 0) {                                         │
  │                  right = pos + 1;                                        │
  │              } else {                                                    │
  │                  left = pos - 1;                                         │
  │              }                                                           │
  │              tree[pos / 2] = tree[left] + tree[right];                   │
  │              pos /= 2;                                                   │
  │          }                                                               │
  │      }                                                                   │
  │                                                                          │
  │      public int sumRange(int l, int r) {                                 │
  │          l += n;                                                         │
  │          r += n;                                                         │
  │          int sum = 0;                                                    │
  │          while (l <= r) {                                                │
  │              if ((l % 2) == 1) {                                         │
  │                 sum += tree[l];                                          │
  │                 l++;                                                     │
  │              }                                                           │
  │              if ((r % 2) == 0) {                                         │
  │                 sum += tree[r];                                          │
  │                 r--;                                                     │
  │              }                                                           │
  │              l /= 2;                                                     │
  │              r /= 2;                                                     │
  │          }                                                               │
  │          return sum;                                                     │
  │      }                                                                   │
  │  }                                                                       │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  7. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: Array vs HashMap for Trie children?

  ANSWER:
    An array `TrieNode[26]` is faster and easier to implement if the charset is strictly lowercase English letters. It uses more memory (sparse arrays). A `HashMap<Character, TrieNode>` saves memory if the tree is very sparse or supports a massive character set (like Unicode), but adds hashing overhead.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: What is the time complexity of Union-Find?

  ANSWER:
    With both Path Compression and Union by Rank, the time complexity of operations is O(α(N)), where α is the Inverse Ackermann function. For all practical values of N, α(N) ≤ 5, making it effectively O(1).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: Segment Tree vs Fenwick Tree (Binary Indexed Tree)?

  ANSWER:
    Fenwick Trees are easier to code, use less memory (exactly size N), and are strictly for prefix queries (like sums). Segment Trees take up to 4N space, are harder to code, but are far more versatile (can handle range Minimum, range Maximum, and complex lazy updates).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: How does Word Search II use a Trie?

  ANSWER:
    Instead of doing a DFS for every word in the dictionary (which is slow), we insert all dictionary words into a Trie. We then do a single DFS over the board, using the Trie to instantly prune DFS paths that don't match any valid prefix.

────────────────────────────────────────────────────────────────────────────────
  8. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: I am a forest of trees, but I specialize in uniting enemies. As I search for your roots, I flatten your family tree. What am I?

  SOLUTION:
    Disjoint Set Union (Union-Find) with Path Compression.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 2: What's wrong with this Trie Search method?

  public boolean search(String word) {
      TrieNode curr = root;
      for (char c : word.toCharArray()) {
          if (curr.children[c - 'a'] == null) {
              return false;
          }
          curr = curr.children[c - 'a'];
      }
      return true; // BUG!
  }

  SOLUTION:
    Returning `true` at the end just means the string exists as a prefix in the Trie. It doesn't mean it was inserted as a complete word.
    Fix: You must return `curr.isEndOfWord;`.

────────────────────────────────────────────────────────────────────────────────
  9. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  - Search Engines: Autocomplete systems and search query suggestions are fundamentally powered by highly optimized, distributed Tries.
  - Network Routing: IP routing tables use variants of Tries (Radix Trees) for Longest Prefix Matching to figure out where to send packets.
  - Image Processing/Gaming: Segment trees (and their 2D equivalents like Quad Trees) are used heavily in rendering and collision detection to quickly query spatial regions.
  - Image Segments/Graph Analysis: Union-Find is used in Kruskal's algorithm (spanning networks) and image processing to find distinct blobs/regions in pixels.

────────────────────────────────────────────────────────────────────────────────
  10. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

  -> File 021: Graphs_ShortestPath_MST_TopoSort.md (See Union-Find in action within Kruskal's Algorithm.)
  -> File 017: Strings_Tries.md (Deep dive into String manipulations.)

================================================================================
  END OF FILE 025
================================================================================
