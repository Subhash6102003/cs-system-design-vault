================================================================================
  FILE 020: Graphs, BFS, and DFS in Java
  Section: B - DSA in Java
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  Graphs: BFS and DFS
  This file covers the fundamentals of graph theory, representation strategies in Java, and the two most critical traversal algorithms: Breadth-First Search (BFS) and Depth-First Search (DFS).
  Prerequisites: Understanding of basic data structures (Arrays, ArrayList, Queues, Stacks) and recursion.
  What you'll learn: How to model relationships using graphs, the memory/time tradeoffs of different graph representations, how to implement BFS and DFS from scratch, and how to apply these traversals to solve complex matrix/grid and node-based LeetCode problems.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  Graph
    A non-linear data structure consisting of Vertices (or Nodes) and Edges that connect these vertices.

  Vertex (Node)
    The fundamental unit of a graph, representing an entity (e.g., a city, a person, a state).

  Edge
    The connection between two vertices.

  Directed Graph
    Edges have a specific direction (A -> B means you can go from A to B, but not necessarily B to A).

  Undirected Graph
    Edges are bi-directional (A - B means you can travel both ways).

  Weighted Graph
    Edges have numerical values (weights/costs) associated with them.

  Unweighted Graph
    All edges have an equal cost (typically considered 1).

  Connected Graph
    There is a path between every pair of vertices.

  Cyclic Graph
    Contains at least one cycle (a path that starts and ends at the same vertex).

  Acyclic Graph
    A graph with no cycles. A Directed Acyclic Graph is called a DAG.

  Adjacency Matrix
    A 2D array `matrix[i][j]` where a non-zero value indicates an edge from `i` to `j`. Space: O(V²) — poor for sparse graphs. Edge Lookup: O(1).

  Adjacency List
    An array (or Map) of Lists, where `adj[i]` contains all neighbors of vertex `i`. Space: O(V + E) — highly efficient for sparse graphs. Edge Lookup: O(degree(V)).

  Edge List
    A simple list of all edges (e.g., `[[u, v, weight], ...]`). Commonly used as input format or for Kruskal's algorithm.

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  Memory Comparison of Representations                                   │
  │                                                                         │
  │  Consider a graph with 4 vertices and 3 edges: 0-1, 0-2, 1-3            │
  │                                                                         │
  │  Graph:                                                                 │
  │      0                                                                  │
  │     / \                                                                 │
  │    1   2                                                                │
  │    |                                                                    │
  │    3                                                                    │
  │                                                                         │
  │  Adjacency Matrix (Space: 4x4 = 16 cells)                               │
  │     0 1 2 3                                                             │
  │  0 [0 1 1 0]                                                            │
  │  1 [1 0 0 1]                                                            │
  │  2 [1 0 0 0]                                                            │
  │  3 [0 1 0 0]                                                            │
  │                                                                         │
  │  Adjacency List (Space: 4 array slots + 6 list nodes)                   │
  │  0 -> [1, 2]                                                            │
  │  1 -> [0, 3]                                                            │
  │  2 -> [0]                                                            │
  │  3 -> [1]                                                            │
  └─────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  BFS vs DFS Traversal Order                                             │
  │                                                                         │
  │  Starting from Node A:                                                  │
  │                                                                         │
  │          A                                                              │
  │        / | \                                                            │
  │       B  C  D                                                           │
  │      / \    |                                                           │
  │     E   F   G                                                           │
  │                                                                         │
  │  BFS Order (Level-by-Level):                                            │
  │  Level 0: A                                                             │
  │  Level 1: B, C, D                                                       │
  │  Level 2: E, F, G                                                       │
  │  Result: A, B, C, D, E, F, G                                            │
  │                                                                         │
  │  DFS Order (Depth-First - pre-order):                                   │
  │  Go deep into B, then E. Backtrack to F. Backtrack to C. Then D, then G.│
  │  Result: A, B, E, F, C, D, G                                            │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  Language: Java

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  import java.util.*;                                                     │
  │                                                                          │
  │  public class GraphTraversal {                                           │
  │                                                                          │
  │      // DFS implementation using Recursion                               │
  │      public static void dfs(int node, Map<Integer, List<Integer>> adj, Set<Integer> visited) { │
  │          // Mark current node as visited                                 │
  │          visited.add(node);                                              │
  │          System.out.print(node + " ");                                   │
  │                                                                          │
  │          // Explore all unvisited neighbors                              │
  │          for (int neighbor : adj.getOrDefault(node, new ArrayList<>())) {│
  │              if (!visited.contains(neighbor)) {                          │
  │                  dfs(neighbor, adj, visited);                            │
  │              }                                                           │
  │          }                                                               │
  │      }                                                                   │
  │                                                                          │
  │      // BFS implementation using a Queue                                 │
  │      public static void bfs(int start, Map<Integer, List<Integer>> adj) {│
  │          Queue<Integer> queue = new LinkedList<>();                      │
  │          Set<Integer> visited = new HashSet<>();                         │
  │                                                                          │
  │          queue.offer(start);                                             │
  │          visited.add(start);                                             │
  │                                                                          │
  │          while (!queue.isEmpty()) {                                      │
  │              int node = queue.poll();                                    │
  │              System.out.print(node + " ");                               │
  │                                                                          │
  │              // Add all unvisited neighbors to the queue                 │
  │              for (int neighbor : adj.getOrDefault(node, new ArrayList<>())) { │
  │                  if (!visited.contains(neighbor)) {                      │
  │                      visited.add(neighbor);                              │
  │                      queue.offer(neighbor);                              │
  │                  }                                                       │
  │              }                                                           │
  │          }                                                               │
  │      }                                                                   │
  │  }                                                                       │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

  Language: Java

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  import java.util.*;                                                     │
  │                                                                          │
  │  /**                                                                     │
  │   * A generic Undirected Graph using Adjacency List.                     │
  │   */                                                                     │
  │  public class Graph<T> {                                                 │
  │      private final Map<T, List<T>> adjacencyList;                        │
  │                                                                          │
  │      public Graph() {                                                    │
  │          this.adjacencyList = new HashMap<>();                           │
  │      }                                                                   │
  │                                                                          │
  │      /**                                                                 │
  │       * Adds a vertex to the graph.                                      │
  │       */                                                                 │
  │      public void addVertex(T vertex) {                                   │
  │          adjacencyList.putIfAbsent(vertex, new ArrayList<>());           │
  │      }                                                                   │
  │                                                                          │
  │      /**                                                                 │
  │       * Adds an undirected edge between v1 and v2.                       │
  │       */                                                                 │
  │      public void addEdge(T source, T destination) {                      │
  │          addVertex(source);                                              │
  │          addVertex(destination);                                         │
  │          adjacencyList.get(source).add(destination);                     │
  │          adjacencyList.get(destination).add(source); // Remove for directed graph │
  │      }                                                                   │
  │                                                                          │
  │      /**                                                                 │
  │       * Returns the shortest path (in terms of number of edges) using BFS.│
  │       */                                                                 │
  │      public List<T> getShortestPathBFS(T start, T end) {                 │
  │          if (!adjacencyList.containsKey(start) || !adjacencyList.containsKey(end)) { │
  │              return Collections.emptyList();                             │
  │          }                                                               │
  │                                                                          │
  │          Queue<T> queue = new LinkedList<>();                            │
  │          Map<T, T> parentMap = new HashMap<>();                          │
  │          Set<T> visited = new HashSet<>();                               │
  │                                                                          │
  │          queue.offer(start);                                             │
  │          visited.add(start);                                             │
  │          parentMap.put(start, null);                                     │
  │                                                                          │
  │          while (!queue.isEmpty()) {                                      │
  │              T current = queue.poll();                                   │
  │                                                                          │
  │              if (current.equals(end)) {                                  │
  │                  return reconstructPath(parentMap, end);                 │
  │              }                                                           │
  │                                                                          │
  │              for (T neighbor : adjacencyList.get(current)) {             │
  │                  if (!visited.contains(neighbor)) {                      │
  │                      visited.add(neighbor);                              │
  │                      parentMap.put(neighbor, current);                   │
  │                      queue.offer(neighbor);                              │
  │                  }                                                       │
  │              }                                                           │
  │          }                                                               │
  │          return Collections.emptyList(); // No path found                │
  │      }                                                                   │
  │                                                                          │
  │      private List<T> reconstructPath(Map<T, T> parentMap, T end) {       │
  │          List<T> path = new ArrayList<>();                               │
  │          T current = end;                                                │
  │          while (current != null) {                                       │
  │              path.add(current);                                          │
  │              current = parentMap.get(current);                           │
  │          }                                                               │
  │          Collections.reverse(path);                                      │
  │          return path;                                                    │
  │      }                                                                   │
  │  }                                                                       │
  └──────────────────────────────────────────────────────────────────────────┘

  Language: Java (Number of Islands)

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  public class NumberOfIslands {                                          │
  │      public int numIslands(char[][] grid) {                              │
  │          if (grid == null || grid.length == 0) return 0;                 │
  │          int count = 0;                                                  │
  │                                                                          │
  │          for (int i = 0; i < grid.length; i++) {                         │
  │              for (int j = 0; j < grid[0].length; j++) {                  │
  │                  if (grid[i][j] == '1') {                                │
  │                      count++;                                            │
  │                      dfs(grid, i, j);                                    │
  │                  }                                                       │
  │              }                                                           │
  │          }                                                               │
  │          return count;                                                   │
  │      }                                                                   │
  │                                                                          │
  │      private void dfs(char[][] grid, int i, int j) {                     │
  │          // Boundary checks and water check                              │
  │          if (i < 0 || i >= grid.length || j < 0 || j >= grid[0].length || grid[i][j] == '0') { │
  │              return;                                                     │
  │          }                                                               │
  │                                                                          │
  │          // Mark as visited by sinking the island                        │
  │          grid[i][j] = '0';                                               │
  │                                                                          │
  │          // Explore 4 directions                                         │
  │          dfs(grid, i+1, j);                                              │
  │          dfs(grid, i-1, j);                                              │
  │          dfs(grid, i, j+1);                                              │
  │          dfs(grid, i, j-1);                                              │
  │      }                                                                   │
  │  }                                                                       │
  └──────────────────────────────────────────────────────────────────────────┘

  Language: Java (Rotting Oranges)

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  import java.util.*;                                                     │
  │                                                                          │
  │  public class RottingOranges {                                           │
  │      public int orangesRotting(int[][] grid) {                           │
  │          int rows = grid.length;                                         │
  │          int cols = grid[0].length;                                      │
  │          Queue<int[]> queue = new LinkedList<>();                        │
  │          int freshCount = 0;                                             │
  │                                                                          │
  │          // Step 1: Enqueue all initially rotten oranges and count fresh ones │
  │          for (int i = 0; i < rows; i++) {                                │
  │              for (int j = 0; j < cols; j++) {                            │
  │                  if (grid[i][j] == 2) {                                  │
  │                      queue.offer(new int[]{i, j});                       │
  │                  } else if (grid[i][j] == 1) {                           │
  │                      freshCount++;                                       │
  │                  }                                                       │
  │              }                                                           │
  │          }                                                               │
  │                                                                          │
  │          if (freshCount == 0) return 0; // Already zero fresh oranges    │
  │                                                                          │
  │          int minutes = 0;                                                │
  │          int[][] dirs = {{1,0}, {-1,0}, {0,1}, {0,-1}};                  │
  │                                                                          │
  │          // Step 2: Multi-source BFS                                     │
  │          while (!queue.isEmpty() && freshCount > 0) {                    │
  │              int size = queue.size();                                    │
  │              minutes++;                                                  │
  │                                                                          │
  │              for (int i = 0; i < size; i++) {                            │
  │                  int[] curr = queue.poll();                              │
  │                                                                          │
  │                  for (int[] dir : dirs) {                                │
  │                      int r = curr[0] + dir[0];                           │
  │                      int c = curr[1] + dir[1];                           │
  │                                                                          │
  │                      // If out of bounds or not a fresh orange, skip     │
  │                      if (r < 0 || r >= rows || c < 0 || c >= cols || grid[r][c] != 1) { │
  │                          continue;                                       │
  │                      }                                                   │
  │                                                                          │
  │                      // Rot the orange                                   │
  │                      grid[r][c] = 2;                                     │
  │                      freshCount--;                                       │
  │                      queue.offer(new int[]{r, c});                       │
  │                  }                                                       │
  │              }                                                           │
  │          }                                                               │
  │                                                                          │
  │          return freshCount == 0 ? minutes : -1;                          │
  │      }                                                                   │
  │  }                                                                       │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  7. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: When would you choose BFS over DFS?

  ANSWER:
    BFS is optimal for finding the shortest path in an unweighted graph, as it explores level by level. DFS is better for exploring all paths, backtracking problems, or topological sorting. DFS generally uses less memory (proportional to max depth, whereas BFS queue can grow to the max width of the graph).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: How does graph cycle detection work?

  ANSWER:
    For undirected graphs, use DFS and keep track of a parent node; if you visit an already visited node that isn't the parent, a cycle exists. For directed graphs, use DFS with a "visiting" state (recursion stack); if you encounter a node currently in the recursion stack, there's a back-edge (cycle).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: What is a bipartite graph and how do you check for it?

  ANSWER:
    A graph whose vertices can be divided into two disjoint sets such that every edge connects a vertex in one set to a vertex in the other. Check it using BFS/DFS graph coloring: attempt to color neighbors with alternating colors. If a neighbor already has the same color, it's not bipartite.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: How do you handle disconnected components in a graph?

  ANSWER:
    Iterate through all vertices. For any unvisited vertex, launch a BFS or DFS. Each launch signifies a new disconnected component.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: Why use an adjacency list instead of a matrix?

  ANSWER:
    Most real-world graphs (like social networks or maps) are sparse (E << V²). Adjacency list saves enormous memory and allows faster iteration over a node's specific neighbors, preventing O(V) scan time per node.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: Can DFS be implemented iteratively?

  ANSWER:
    Yes, by using an explicit Stack instead of the call stack. However, the exact traversal order might differ slightly (right-to-left vs left-to-right) unless neighbors are pushed in reverse order.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q7: What are tree, back, forward, and cross edges in DFS?

  ANSWER:
    - Tree Edge: Edge to an unvisited node.
    - Back Edge: Edge to an ancestor node (indicates a cycle).
    - Forward Edge: Edge to a non-child descendant.
    - Cross Edge: Edge to a node that is neither ancestor nor descendant.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q8: How does multi-source BFS work?

  ANSWER:
    Instead of enqueuing a single start node, you enqueue ALL starting nodes at level 0 before starting the while-loop. The algorithm expands outwards uniformly from all sources simultaneously.

────────────────────────────────────────────────────────────────────────────────
  8. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: I search wide before I search deep. I am the reason water fills a maze level by level. What algorithm am I?

  SOLUTION:
    Breadth-First Search (BFS).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 2: Can you spot the bug in this undirected graph cycle detection code?

  boolean hasCycle(int node, boolean[] visited) {
      visited[node] = true;
      for (int neighbor : adj.get(node)) {
          if (!visited[neighbor]) {
              if (hasCycle(neighbor, visited)) return true;
          } else {
              return true;
          }
      }
      return false;
  }

  SOLUTION:
    In an undirected graph, an edge goes both ways (A-B and B-A). When node A calls node B, node B sees node A as a neighbor. Since node A is `visited`, it immediately returns `true` (false positive for a cycle).
    Fix: You must pass the `parent` node in the recursive call and skip the neighbor if it equals the parent. `if (neighbor != parent) return true;`

────────────────────────────────────────────────────────────────────────────────
  9. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  - Network Routing: OSPF (Open Shortest Path First) protocols use graph algorithms to propagate routes.
  - Social Networks: "People you may know" (friends of friends) leverages BFS limited to depth 2 or 3.
  - Garbage Collection: Tracing garbage collectors (like the JVM's G1 GC) model objects as nodes and references as directed edges, using DFS-like traversals to mark reachable objects.
  - Build Systems: Maven, Gradle, or Make represent dependencies as Directed Acyclic Graphs (DAGs) and use Topological Sort (based on DFS or BFS) to determine compilation order.
  - Web Crawlers: Googlebot traverses the web as a massive directed graph, using a distributed BFS to index pages level by level.

────────────────────────────────────────────────────────────────────────────────
  10. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

  -> File 021: Graphs_ShortestPath_MST_TopoSort.md (Advanced Graph Algorithms)
  -> File 012: Stacks_Queues.md (The underlying data structures for DFS/BFS)
  -> File 016: Trees_Traversals.md (DFS/BFS applied to Tree structures)

================================================================================
  END OF FILE 020
================================================================================
