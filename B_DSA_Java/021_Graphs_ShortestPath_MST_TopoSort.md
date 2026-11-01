================================================================================
  FILE 021: Graphs: Shortest Path, MST, and Topological Sort
  Section: B - DSA in Java
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  Graphs: Dijkstra, MST, and Topological Sort
  This file delves into advanced graph algorithms used for optimization problems. You will explore finding the lowest cost path, connecting all nodes with minimum wiring, and ordering tasks with dependencies.
  Prerequisites: Understanding of Graphs, BFS/DFS, Priority Queues (Min-Heaps), and Disjoint Sets (Union-Find).
  What you'll learn: Dijkstra's, Bellman-Ford, and Floyd-Warshall for shortest paths; Kruskal's and Prim's for Minimum Spanning Trees; Kahn's algorithm and DFS for Topological Sorting.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  Shortest Path Problem
    Finding a path between two vertices such that the sum of the weights of its constituent edges is minimized.

  Dijkstra's Algorithm
    A greedy algorithm that finds the shortest path from a source to all other nodes. Fails with negative weights.

  Bellman-Ford Algorithm
    Handles negative weights and detects negative cycles by relaxing all edges V-1 times.

  Floyd-Warshall Algorithm
    Dynamic programming approach to find shortest paths between all pairs of vertices.

  Minimum Spanning Tree (MST)
    A subset of edges in a connected, edge-weighted undirected graph that connects all vertices without any cycles and with the minimum possible total edge weight.

  Kruskal's Algorithm
    Greedy MST algorithm that sorts all edges and adds them using Union-Find to avoid cycles.

  Prim's Algorithm
    Greedy MST algorithm that builds the tree from an arbitrary starting vertex, always picking the lowest-weight edge to an unvisited node.

  Topological Sort
    A linear ordering of vertices in a Directed Acyclic Graph (DAG) such that for every directed edge u -> v, u comes before v.

  In-Degree
    The number of edges coming into a vertex.

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  Dijkstra's Step-by-Step                                                │
  │                                                                         │
  │  Graph: A --(4)--> B, A --(1)--> C, C --(2)--> B                        │
  │                                                                         │
  │  Initialize Distances: A=0, B=∞, C=∞                                    │
  │  MinHeap: [(A, 0)]                                                      │
  │                                                                         │
  │  Step 1: Pop A (dist=0). Relax neighbors B and C.                       │
  │          Distances: B=4, C=1                                            │
  │          MinHeap: [(C, 1), (B, 4)]                                      │
  │                                                                         │
  │  Step 2: Pop C (dist=1). Relax neighbor B.                              │
  │          Path A->C->B costs 1+2 = 3. 3 < 4 (current dist to B).         │
  │          Update Distance: B=3                                           │
  │          MinHeap: [(B, 3), (B, 4)]                                      │
  │                                                                         │
  │  Step 3: Pop B (dist=3). No neighbors.                                  │
  │  Step 4: Pop B (dist=4). Ignore (stale distance 4 > current 3).         │
  │  Final Distances: A=0, B=3, C=1                                         │
  └─────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  Minimum Spanning Tree (MST)                                            │
  │                                                                         │
  │  Original Graph:         MST (Cost: 1+2+3 = 6)                          │
  │      A                     A                                            │
  │    1/ \3                 1/                                             │
  │    B---C                 B---C                                          │
  │    | 2 |                 | 2                                            │
  │   4|   |5               4|                                              │
  │    D---E                 D   E (disconnected? No, must connect E)       │
  │                                                                         │
  │  Wait, if we need to connect E, we must pick edge C-E (5) or D-E        │
  │  (weight let's say 3).                                                  │
  │  Let's trace Kruskal's: Sort edges: AB(1), BC(2), AC(3), DE(3), BD(4),  │
  │  CE(5). Pick AB, pick BC, AC creates cycle (skip), pick DE, pick BD.    │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  Language: Java

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  import java.util.*;                                                     │
  │                                                                          │
  │  public class TopologicalSort {                                          │
  │      // Kahn's Algorithm (BFS based)                                     │
  │      public List<Integer> topoSort(int numVertices, int[][] edges) {     │
  │          List<Integer> result = new ArrayList<>();                       │
  │          int[] inDegree = new int[numVertices];                          │
  │          List<List<Integer>> adj = new ArrayList<>();                    │
  │                                                                          │
  │          for (int i = 0; i < numVertices; i++) adj.add(new ArrayList<>());│
  │                                                                          │
  │          // Build graph and populate in-degrees                          │
  │          for (int[] edge : edges) {                                      │
  │              int u = edge[0], v = edge[1];                               │
  │              adj.get(u).add(v);                                          │
  │              inDegree[v]++;                                              │
  │          }                                                               │
  │                                                                          │
  │          Queue<Integer> queue = new LinkedList<>();                      │
  │          // Enqueue all nodes with in-degree 0                           │
  │          for (int i = 0; i < numVertices; i++) {                         │
  │              if (inDegree[i] == 0) queue.offer(i);                       │
  │          }                                                               │
  │                                                                          │
  │          while (!queue.isEmpty()) {                                      │
  │              int curr = queue.poll();                                    │
  │              result.add(curr);                                           │
  │                                                                          │
  │              for (int neighbor : adj.get(curr)) {                        │
  │                  inDegree[neighbor]--;                                   │
  │                  if (inDegree[neighbor] == 0) {                          │
  │                      queue.offer(neighbor);                              │
  │                  }                                                       │
  │              }                                                           │
  │          }                                                               │
  │                                                                          │
  │          // If result size != numVertices, graph has a cycle!            │
  │          if (result.size() != numVertices) return new ArrayList<>(); // DAG violation │
  │          return result;                                                  │
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
  │  public class DijkstraShortestPath {                                     │
  │                                                                          │
  │      static class Edge {                                                 │
  │          int to;                                                         │
  │          int weight;                                                     │
  │          Edge(int to, int weight) {                                      │
  │              this.to = to;                                               │
  │              this.weight = weight;                                       │
  │          }                                                               │
  │      }                                                                   │
  │                                                                          │
  │      static class Node implements Comparable<Node> {                     │
  │          int id;                                                         │
  │          int dist;                                                       │
  │          Node(int id, int dist) {                                        │
  │              this.id = id;                                               │
  │              this.dist = dist;                                           │
  │          }                                                               │
  │                                                                          │
  │          @Override                                                       │
  │          public int compareTo(Node other) {                              │
  │              return Integer.compare(this.dist, other.dist);              │
  │          }                                                               │
  │      }                                                                   │
  │                                                                          │
  │      /**                                                                 │
  │       * Finds shortest paths from a source to all other nodes.           │
  │       * @return int array where index is node id and value is shortest distance. │
  │       */                                                                 │
  │      public int[] getShortestPaths(int numNodes, List<List<Edge>> graph, int source) { │
  │          int[] distances = new int[numNodes];                            │
  │          Arrays.fill(distances, Integer.MAX_VALUE);                      │
  │          distances[source] = 0;                                          │
  │                                                                          │
  │          PriorityQueue<Node> pq = new PriorityQueue<>();                 │
  │          pq.offer(new Node(source, 0));                                  │
  │                                                                          │
  │          while (!pq.isEmpty()) {                                         │
  │              Node current = pq.poll();                                   │
  │              int u = current.id;                                         │
  │                                                                          │
  │              // Optimization: if we found a shorter path previously, skip│
  │              if (current.dist > distances[u]) continue;                  │
  │                                                                          │
  │              for (Edge edge : graph.get(u)) {                            │
  │                  int v = edge.to;                                        │
  │                  int weight = edge.weight;                               │
  │                                                                          │
  │                  // Relaxation step                                      │
  │                  if (distances[u] + weight < distances[v]) {             │
  │                      distances[v] = distances[u] + weight;               │
  │                      pq.offer(new Node(v, distances[v]));                │
  │                  }                                                       │
  │              }                                                           │
  │          }                                                               │
  │          return distances;                                               │
  │      }                                                                   │
  │  }                                                                       │
  └──────────────────────────────────────────────────────────────────────────┘

  Language: Java (Network Delay Time)

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  class Solution {                                                        │
  │      public int networkDelayTime(int[][] times, int n, int k) {          │
  │          // Build graph: 1-indexed                                       │
  │          List<List<int[]>> graph = new ArrayList<>();                    │
  │          for (int i = 0; i <= n; i++) graph.add(new ArrayList<>());      │
  │          for (int[] t : times) {                                         │
  │              graph.get(t[0]).add(new int[]{t[1], t[2]});                 │
  │          }                                                               │
  │                                                                          │
  │          int[] dist = new int[n + 1];                                    │
  │          Arrays.fill(dist, Integer.MAX_VALUE);                           │
  │          dist[k] = 0;                                                    │
  │                                                                          │
  │          PriorityQueue<int[]> pq = new PriorityQueue<>((a, b) -> a[1] - b[1]); │
  │          pq.offer(new int[]{k, 0});                                      │
  │                                                                          │
  │          while (!pq.isEmpty()) {                                         │
  │              int[] curr = pq.poll();                                     │
  │              int u = curr[0];                                            │
  │              int d = curr[1];                                            │
  │                                                                          │
  │              if (d > dist[u]) continue;                                  │
  │                                                                          │
  │              for (int[] edge : graph.get(u)) {                           │
  │                  int v = edge[0];                                        │
  │                  int weight = edge[1];                                   │
  │                  if (dist[u] + weight < dist[v]) {                       │
  │                      dist[v] = dist[u] + weight;                         │
  │                      pq.offer(new int[]{v, dist[v]});                    │
  │                  }                                                       │
  │              }                                                           │
  │          }                                                               │
  │                                                                          │
  │          int maxTime = 0;                                                │
  │          for (int i = 1; i <= n; i++) {                                  │
  │              if (dist[i] == Integer.MAX_VALUE) return -1; // Unreachable node │
  │              maxTime = Math.max(maxTime, dist[i]);                       │
  │          }                                                               │
  │                                                                          │
  │          return maxTime;                                                 │
  │      }                                                                   │
  │  }                                                                       │
  └──────────────────────────────────────────────────────────────────────────┘

  Language: Java (Min Cost to Connect All Points)

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  class Solution {                                                        │
  │      class UnionFind {                                                   │
  │          int[] parent, rank;                                             │
  │          UnionFind(int n) {                                              │
  │              parent = new int[n]; rank = new int[n];                     │
  │              for (int i = 0; i < n; i++) parent[i] = i;                  │
  │          }                                                               │
  │          int find(int i) {                                               │
  │              if (parent[i] == i) return i;                               │
  │              return parent[i] = find(parent[i]); // Path compression     │
  │          }                                                               │
  │          boolean union(int i, int j) {                                   │
  │              int rootI = find(i), rootJ = find(j);                       │
  │              if (rootI == rootJ) return false;                           │
  │              if (rank[rootI] < rank[rootJ]) parent[rootI] = rootJ;       │
  │              else if (rank[rootI] > rank[rootJ]) parent[rootJ] = rootI;  │
  │              else { parent[rootJ] = rootI; rank[rootI]++; }              │
  │              return true;                                                │
  │          }                                                               │
  │      }                                                                   │
  │                                                                          │
  │      public int minCostConnectPoints(int[][] points) {                   │
  │          int n = points.length;                                          │
  │          List<int[]> edges = new ArrayList<>();                          │
  │                                                                          │
  │          // Build all edges (O(N^2))                                     │
  │          for (int i = 0; i < n; i++) {                                   │
  │              for (int j = i + 1; j < n; j++) {                           │
  │                  int cost = Math.abs(points[i][0] - points[j][0]) + Math.abs(points[i][1] - points[j][1]); │
  │                  edges.add(new int[]{i, j, cost});                       │
  │              }                                                           │
  │          }                                                               │
  │                                                                          │
  │          // Sort by cost                                                 │
  │          Collections.sort(edges, (a, b) -> a[2] - b[2]);                 │
  │                                                                          │
  │          UnionFind uf = new UnionFind(n);                                │
  │          int mstCost = 0;                                                │
  │          int edgesUsed = 0;                                              │
  │                                                                          │
  │          for (int[] edge : edges) {                                      │
  │              if (uf.union(edge[0], edge[1])) {                           │
  │                  mstCost += edge[2];                                     │
  │                  edgesUsed++;                                            │
  │                  if (edgesUsed == n - 1) break; // MST complete          │
  │              }                                                           │
  │          }                                                               │
  │          return mstCost;                                                 │
  │      }                                                                   │
  │  }                                                                       │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  7. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: Why does Dijkstra fail with negative edges?

  ANSWER:
    Dijkstra assumes that once a node is popped from the min-heap, its shortest distance is finalized because any other path would only add positive weight. Negative edges violate this greedy assumption.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: What is the time complexity of Kahn's Algorithm?

  ANSWER:
    O(V + E) where V is vertices and E is edges, because every vertex and edge is processed exactly once.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: How does Bellman-Ford detect negative weight cycles?

  ANSWER:
    By relaxing all edges V-1 times, we guarantee shortest paths in a valid graph. If we relax all edges one more time (the V-th time) and a distance still decreases, it proves the existence of a negative weight cycle.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: Difference between Prim's and Dijkstra's?

  ANSWER:
    Very similar structurally! Dijkstra tracks the total distance from the source to the current node. Prim's tracks the minimum distance from the growing tree to the current node.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: When would you use Floyd-Warshall?

  ANSWER:
    When you need shortest paths between ALL pairs of nodes, the graph is small (due to O(V³) complexity), or when dealing with an adjacency matrix with dense edges and potential negative weights.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: Can Topological Sort yield multiple valid orderings?

  ANSWER:
    Yes, any time the queue in Kahn's algorithm contains more than 1 node, you have a choice, leading to multiple valid topological sorts.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q7: What is the "stale pair" problem in PriorityQueue implementations of Dijkstra?

  ANSWER:
    Because Java's `PriorityQueue` doesn't have an efficient `decreaseKey` operation, we just insert duplicate nodes with new smaller distances. When we pop a node with a distance greater than `dist[u]`, it's stale and should be ignored (e.g., `if (d > dist[u]) continue;`).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q8: Why is Path Compression important in Kruskal's?

  ANSWER:
    Without it, Union-Find could degrade to O(N) per find operation, making Kruskal's slower. Path compression ensures near O(1) amortized time, making the edge sorting O(E log E) the dominant factor.

────────────────────────────────────────────────────────────────────────────────
  8. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: I run V-1 times, and one time more, to catch the cycles that steal from the poor (negative weights). Who am I?

  SOLUTION:
    Bellman-Ford Algorithm.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 2: Can you find the bug in this Topological Sort check?

  // inside Kahn's algo loop
  while (!queue.isEmpty()) {
      int u = queue.poll();
      count++; // count processed nodes
      for (int v : adj.get(u)) {
          inDegree[v]--;
          // BUG HERE?
          queue.offer(v);
      }
  }

  SOLUTION:
    The code enqueues the neighbor `v` immediately after decrementing `inDegree`, regardless of whether it hit 0.
    Fix: It should only enqueue `if (inDegree[v] == 0) queue.offer(v);`. Otherwise, a node is processed prematurely before its dependencies are resolved.

────────────────────────────────────────────────────────────────────────────────
  9. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  - Google Maps Navigation: Uses A* search (an optimized variant of Dijkstra with heuristics) to calculate fastest routes.
  - Microservices & Task Schedulers: DAGs (Airflow, Kubernetes init containers) heavily rely on Topological Sort to guarantee dependencies boot in the correct order.
  - Telecommunications: Laying fiber optic cables between cities for minimal cost is exactly the Minimum Spanning Tree problem.
  - Currency Arbitrage: Detecting negative cycles using Bellman-Ford can identify situations where exchanging currencies in a specific loop yields a net profit.

────────────────────────────────────────────────────────────────────────────────
  10. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

  -> File 020: Graphs_BFS_DFS.md (Graph traversal fundamentals)
  -> File 025: Tries_SegmentTrees_UnionFind.md (Deep dive into Disjoint Set Union (Union-Find))

================================================================================
  END OF FILE 021
================================================================================
