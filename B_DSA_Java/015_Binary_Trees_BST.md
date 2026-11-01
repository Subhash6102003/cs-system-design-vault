================================================================================
  FILE 015: Binary Trees and Binary Search Trees (BST)
  Section: B - DSA in Java
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  Binary Trees and BSTs are fundamental hierarchical data structures. A Binary Tree restricts nodes to at most two children. A Binary Search Tree (BST) introduces an ordering property, enabling fast search, insertion, and deletion.

  Prerequisites: Pointers/References, Recursion.
  What you'll learn: Tree terminology, traversal algorithms (recursive and iterative), BST properties, time complexities, and implementation of core operations.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  Root
    The topmost node of the tree.

  Leaf
    A node with no children.

  Height
    The number of edges on the longest downward path between the root and a leaf.

  Depth
    The number of edges from the root to a specific node.

  Balanced Tree
    A tree where the height of left and right subtrees of every node differs by at most 1 (e.g., AVL, Red-Black).

  Complete Tree
    Every level, except possibly the last, is completely filled, and all nodes are as far left as possible.

  Full Tree
    Every node has either 0 or 2 children.

  Perfect Tree
    All interior nodes have two children and all leaves are at the same level.

  Binary Search Tree (BST)
    For any node, all values in its left subtree are strictly less than its value, and all values in its right subtree are strictly greater.

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  BST Structure Example                                                  │
  │                                                                         │
  │            10                                                           │
  │          /    \                                                         │
  │         5      15                                                       │
  │        / \    /  \                                                      │
  │       2   7  12   20                                                    │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  Traversals on the above BST:                                           │
  │                                                                         │
  │  - Inorder (Left, Root, Right): 2, 5, 7, 10, 12, 15, 20 (Sorted!)       │
  │  - Preorder (Root, Left, Right): 10, 5, 2, 7, 15, 12, 20                │
  │  - Postorder (Left, Right, Root): 2, 7, 5, 12, 20, 15, 10               │
  │  - Level-Order (BFS): 10, 5, 15, 2, 7, 12, 20                           │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  Language: Java

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  class TreeNode {                                                        │
  │      int val;                                                            │
  │      TreeNode left, right;                                               │
  │      public TreeNode(int val) { this.val = val; }                        │
  │  }                                                                       │
  │                                                                          │
  │  public class TreeTraversals {                                           │
  │      // Inorder Traversal: Left -> Root -> Right                         │
  │      public void inorder(TreeNode root) {                                │
  │          if (root == null) return;                                       │
  │          inorder(root.left);                                             │
  │          System.out.print(root.val + " ");                               │
  │          inorder(root.right);                                            │
  │      }                                                                   │
  │                                                                          │
  │      // Iterative Level-Order using Queue                                │
  │      public void levelOrder(TreeNode root) {                             │
  │          if (root == null) return;                                       │
  │          java.util.Queue<TreeNode> q = new java.util.LinkedList<>();     │
  │          q.offer(root);                                                  │
  │                                                                          │
  │          while (!q.isEmpty()) {                                          │
  │              TreeNode curr = q.poll();                                   │
  │              System.out.print(curr.val + " ");                           │
  │              if (curr.left != null) q.offer(curr.left);                  │
  │              if (curr.right != null) q.offer(curr.right);                │
  │          }                                                               │
  │      }                                                                   │
  │  }                                                                       │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

  Language: Java

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  /**                                                                     │
  │   * Production-ready implementation of a Binary Search Tree              │
  │   */                                                                     │
  │  public class BinarySearchTree {                                         │
  │      private class Node {                                                │
  │          int key;                                                        │
  │          Node left, right;                                               │
  │          public Node(int item) { key = item; left = right = null; }      │
  │      }                                                                   │
  │                                                                          │
  │      private Node root;                                                  │
  │                                                                          │
  │      public void insert(int key) { root = insertRec(root, key); }        │
  │                                                                          │
  │      private Node insertRec(Node root, int key) {                        │
  │          if (root == null) return new Node(key);                         │
  │          if (key < root.key) root.left = insertRec(root.left, key);      │
  │          else if (key > root.key) root.right = insertRec(root.right, key);│
  │          return root;                                                    │
  │      }                                                                   │
  │                                                                          │
  │      public void delete(int key) { root = deleteRec(root, key); }        │
  │                                                                          │
  │      private Node deleteRec(Node root, int key) {                        │
  │          if (root == null) return root;                                  │
  │                                                                          │
  │          if (key < root.key) root.left = deleteRec(root.left, key);      │
  │          else if (key > root.key) root.right = deleteRec(root.right, key);│
  │          else {                                                          │
  │              // Case 1 & 2: Node with only one child or no child         │
  │              if (root.left == null) return root.right;                   │
  │              else if (root.right == null) return root.left;              │
  │                                                                          │
  │              // Case 3: Node with two children. Get inorder successor    │
  │              root.key = minValue(root.right);                            │
  │              // Delete the inorder successor                             │
  │              root.right = deleteRec(root.right, root.key);               │
  │          }                                                               │
  │          return root;                                                    │
  │      }                                                                   │
  │                                                                          │
  │      private int minValue(Node root) {                                   │
  │          int minv = root.key;                                            │
  │          while (root.left != null) {                                     │
  │              minv = root.left.key;                                       │
  │              root = root.left;                                           │
  │          }                                                               │
  │          return minv;                                                    │
  │      }                                                                   │
  │  }                                                                       │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  7. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: What is the time complexity of searching in a BST?

  ANSWER:
    O(log N) average case, but O(N) worst case if the tree is skewed (like a linked list).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: How does Morris Traversal achieve O(1) space?

  ANSWER:
    By temporarily modifying the tree structure, creating threaded links from the inorder predecessor's right child back to the current node.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: How do you validate if a Binary Tree is a BST?

  ANSWER:
    Pass down a `min` and `max` constraint for every recursive call. The root must be between negative and positive infinity, left child between `min` and `root.val`, etc.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: Why is level-order traversal implemented with a Queue?

  ANSWER:
    BFS explores nodes level by level. A FIFO structure ensures that nodes discovered earlier (closer to the root) are processed first.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: What is an Inorder Successor?

  ANSWER:
    The node that appears immediately after a given node in an inorder traversal (i.e., the smallest node in the right subtree).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: How do you serialize and deserialize a binary tree?

  ANSWER:
    Use Preorder or Level-order traversal. Store `null` pointers as specific markers (e.g., `"null"`) to preserve structural integrity.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q7: What is the diameter of a binary tree?

  ANSWER:
    The length of the longest path between any two nodes. This path may or may not pass through the root.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q8: How does deleting a node with two children work in a BST?

  ANSWER:
    Find the inorder successor (smallest in the right subtree) or predecessor (largest in the left), copy its value to the target node, and recursively delete the successor/predecessor.

────────────────────────────────────────────────────────────────────────────────
  8. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: The Broken Validator

  public boolean isValidBST(TreeNode root) {
      if (root == null) return true;
      if (root.left != null && root.left.val >= root.val) return false;
      if (root.right != null && root.right.val <= root.val) return false;
      return isValidBST(root.left) && isValidBST(root.right);
  }

  SOLUTION:
    It only checks children against their immediate parent. In a valid BST, the right child of a left child must still be less than the root node. We need global `min` and `max` bounds.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 2: Endless Morris

  TreeNode pre = curr.left;
  while (pre.right != null) { // BUG
      pre = pre.right;
  }

  SOLUTION:
    In Morris Traversal, `pre.right` might point back to `curr` (the threaded link). The condition must be `while(pre.right != null && pre.right != curr)`.

────────────────────────────────────────────────────────────────────────────────
  9. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  Binary Trees map naturally to hierarchical data such as:
  - DOM Trees in web browsers (HTML structure).
  - Abstract Syntax Trees (AST) in compilers and interpreters.
  - Routing tables in network routers.
  - Underlying structure for more complex types like B-Trees (Databases) and Heaps (Schedulers).

────────────────────────────────────────────────────────────────────────────────
  10. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

  -> File 016: AVL_RedBlack_Trees.md (Fixing the O(N) worst-case of standard BSTs)
  -> File 018: Heaps_PriorityQueues.md (Complete binary trees used for priority)

================================================================================
  END OF FILE 015
================================================================================
