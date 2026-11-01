================================================================================
  FILE 024: Greedy Algorithms & Backtracking
  Section: B - DSA in Java
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  Greedy Choices and Backtracking Trees
  This file covers two fundamentally different paradigms: Greedy Algorithms, which make locally optimal choices hoping for a global optimum, and Backtracking, which exhaustively explores all possibilities but abandons ("prunes") dead ends early. 
  Prerequisites: Sorting, Recursion, Time Complexity.
  What you'll learn: How to prove a greedy strategy using exchange arguments, how to identify when greedy fails (and requires DP), and how to structure backtracking recursion templates to solve Combinations, Permutations, and Sudoku.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  Greedy Choice Property
    A global optimum can be arrived at by selecting a local optimum. You never need to reconsider past choices.

  Optimal Substructure
    An optimal solution to the problem contains optimal solutions to subproblems.

  Proof by Exchange Argument
    A technique to prove a greedy algorithm's correctness by showing that exchanging any element of the greedy solution for an element of another optimal solution cannot improve it.

  Backtracking
    An algorithmic technique for solving problems recursively by trying to build a solution incrementally, one piece at a time, removing those solutions that fail to satisfy the constraints of the problem at any point of time.

  State Space Tree (Recursion Tree)
    The theoretical tree of all possible choices.

  Pruning
    Cutting off a branch of the recursion tree when you realize it cannot possibly lead to a valid solution.

  Template Steps
    Choose -> Explore (Recurse) -> Un-choose (Backtrack).

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  Backtracking Recursion Tree with Pruning (Subsets)                     │
  │                                                                         │
  │  Generating subsets for [1, 2]                                          │
  │                                                                         │
  │                       []                                                │
  │                    /      \                                             │
  │                 [1]        []  <-- (exclude 1)                          │
  │                /   \      /   \                                         │
  │            [1,2]  [1]   [2]   []                                        │
  │                                                                         │
  │  Result: [[], [2], [1], [1,2]]                                          │
  └─────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  When Greedy Fails (Coin Change)                                        │
  │                                                                         │
  │  Suppose coins are [1, 3, 4] and target is 6.                           │
  │  Greedy Approach (take largest first):                                  │
  │  - Take 4. Remaining: 2.                                                │
  │  - Take 1. Remaining: 1.                                                │
  │  - Take 1. Remaining: 0.                                                │
  │  Greedy Total Coins = 3 (Coins: 4, 1, 1)                                │
  │                                                                         │
  │  Optimal Approach (DP/BFS):                                             │
  │  - Take 3.                                                              │
  │  - Take 3.                                                              │
  │  Optimal Total Coins = 2 (Coins: 3, 3)                                  │
  │  Conclusion: Greedy fails here! DP is required.                         │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  Language: Java

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  public class BacktrackingTemplate {                                     │
  │                                                                          │
  │      public List<List<Integer>> generate(int[] nums) {                   │
  │          List<List<Integer>> result = new ArrayList<>();                 │
  │          backtrack(result, new ArrayList<>(), nums, 0);                  │
  │          return result;                                                  │
  │      }                                                                   │
  │                                                                          │
  │      private void backtrack(List<List<Integer>> result, List<Integer> tempList, int[] nums, int start) {│
  │          // 1. Base Case / Goal State (Example: Add copy of tempList to result)│
  │          result.add(new ArrayList<>(tempList));                          │
  │                                                                          │
  │          // 2. Iterate through choices                                   │
  │          for (int i = start; i < nums.length; i++) {                     │
  │                                                                          │
  │              // (Optional) Pruning: if (!isValid) continue;              │
  │                                                                          │
  │              // 3. Choose                                                │
  │              tempList.add(nums[i]);                                      │
  │                                                                          │
  │              // 4. Explore (Recurse)                                     │
  │              backtrack(result, tempList, nums, i + 1);                   │
  │                                                                          │
  │              // 5. Un-choose (Backtrack)                                 │
  │              tempList.remove(tempList.size() - 1);                       │
  │          }                                                               │
  │      }                                                                   │
  │  }                                                                       │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

  Language: Java

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Problem 1: Merge Intervals (Greedy)                                  │
  │  import java.util.*;                                                     │
  │                                                                          │
  │  class SolutionMerge {                                                   │
  │      public int[][] merge(int[][] intervals) {                           │
  │          if (intervals.length <= 1) return intervals;                    │
  │                                                                          │
  │          // Greedy choice: Sort by start time                            │
  │          Arrays.sort(intervals, (a, b) -> Integer.compare(a[0], b[0]));  │
  │                                                                          │
  │          List<int[]> merged = new ArrayList<>();                         │
  │          int[] currentInterval = intervals[0];                           │
  │          merged.add(currentInterval);                                    │
  │                                                                          │
  │          for (int[] interval : intervals) {                              │
  │              int currentEnd = currentInterval[1];                        │
  │              int nextBegin = interval[0];                                │
  │              int nextEnd = interval[1];                                  │
  │                                                                          │
  │              if (currentEnd >= nextBegin) { // Overlap!                  │
  │                  currentInterval[1] = Math.max(currentEnd, nextEnd);     │
  │              } else { // Disjoint                                        │
  │                  currentInterval = interval;                             │
  │                  merged.add(currentInterval);                            │
  │              }                                                           │
  │          }                                                               │
  │                                                                          │
  │          return merged.toArray(new int[merged.size()][]);                │
  │      }                                                                   │
  │  }                                                                       │
  │                                                                          │
  │  // Problem 2: Jump Game (Greedy)                                        │
  │  class SolutionJump {                                                    │
  │      public boolean canJump(int[] nums) {                                │
  │          int maxReach = 0;                                               │
  │                                                                          │
  │          for (int i = 0; i < nums.length; i++) {                         │
  │              if (i > maxReach) {                                         │
  │                  return false; // We can't even reach index i            │
  │              }                                                           │
  │              maxReach = Math.max(maxReach, i + nums[i]);                 │
  │              if (maxReach >= nums.length - 1) {                          │
  │                  return true; // We can reach the end                    │
  │              }                                                           │
  │          }                                                               │
  │          return true;                                                    │
  │      }                                                                   │
  │  }                                                                       │
  │                                                                          │
  │  // Problem 3: Permutations (Backtracking)                               │
  │  class SolutionPermute {                                                 │
  │      public List<List<Integer>> permute(int[] nums) {                    │
  │          List<List<Integer>> result = new ArrayList<>();                 │
  │          backtrack(result, new ArrayList<>(), nums);                     │
  │          return result;                                                  │
  │      }                                                                   │
  │                                                                          │
  │      private void backtrack(List<List<Integer>> result, List<Integer> tempList, int[] nums) {│
  │          if (tempList.size() == nums.length) {                           │
  │              result.add(new ArrayList<>(tempList)); // Goal reached      │
  │              return;                                                     │
  │          }                                                               │
  │                                                                          │
  │          for (int i = 0; i < nums.length; i++) {                         │
  │              if (tempList.contains(nums[i])) continue; // Prune: element already in permutation│
  │                                                                          │
  │              tempList.add(nums[i]); // Choose                            │
  │              backtrack(result, tempList, nums); // Explore               │
  │              tempList.remove(tempList.size() - 1); // Un-choose          │
  │          }                                                               │
  │      }                                                                   │
  │  }                                                                       │
  │                                                                          │
  │  // Problem 4: Word Search (Backtracking)                                │
  │  class SolutionWordSearch {                                              │
  │      public boolean exist(char[][] board, String word) {                 │
  │          for (int i = 0; i < board.length; i++) {                        │
  │              for (int j = 0; j < board[0].length; j++) {                 │
  │                  if (board[i][j] == word.charAt(0) && dfs(board, i, j, 0, word)) {│
  │                      return true;                                        │
  │                  }                                                       │
  │              }                                                           │
  │          }                                                               │
  │          return false;                                                   │
  │      }                                                                   │
  │                                                                          │
  │      private boolean dfs(char[][] board, int i, int j, int count, String word) {│
  │          if (count == word.length()) return true; // Found the word      │
  │                                                                          │
  │          // Bounds check and character match check                       │
  │          if (i < 0 || i >= board.length || j < 0 || j >= board[0].length || board[i][j] != word.charAt(count)) {│
  │              return false;                                               │
  │          }                                                               │
  │                                                                          │
  │          char temp = board[i][j];                                        │
  │          board[i][j] = ' '; // Mark as visited (Choose)                  │
  │                                                                          │
  │          // Explore all 4 directions                                     │
  │          boolean found = dfs(board, i + 1, j, count + 1, word) ||        │
  │                          dfs(board, i - 1, j, count + 1, word) ||        │
  │                          dfs(board, i, j + 1, count + 1, word) ||        │
  │                          dfs(board, i, j - 1, count + 1, word);          │
  │                                                                          │
  │          board[i][j] = temp; // Un-choose (Backtrack)                    │
  │                                                                          │
  │          return found;                                                   │
  │      }                                                                   │
  │  }                                                                       │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  7. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: What is the time complexity of generating all subsets of a set?

  ANSWER:
    O(N * 2^N). There are 2^N subsets, and for each subset, it takes O(N) time to copy `tempList` into the `result` list.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: What is the time complexity of generating all permutations?

  ANSWER:
    O(N * N!). There are N! permutations, and copying each takes O(N) time.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: How do you handle duplicates in backtracking (e.g., Subsets II or Permutations II)?

  ANSWER:
    Sort the input array first. Then, in the for-loop, add a condition to skip duplicates: `if (i > start && nums[i] == nums[i-1]) continue;`.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: Why do we pass `new ArrayList<>(tempList)` into the result instead of just `tempList`?

  ANSWER:
    Because `tempList` is passed by reference. If you add it directly, subsequent modifications to `tempList` (the un-choose steps) will alter the lists already inside your result array. You must take a snapshot (deep copy).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: How can you prove a greedy algorithm is correct?

  ANSWER:
    Usually via an "Exchange Argument". Assume there is an optimal solution that differs from the greedy one. Show that by exchanging an element in the optimal solution with the greedy choice, the solution is not worsened. Thus, the greedy solution is also optimal.

────────────────────────────────────────────────────────────────────────────────
  8. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: I take what looks best right now, and I never look back. Sometimes I win big, sometimes I fail terribly. What am I?

  SOLUTION:
    A Greedy Algorithm.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 2: Why does this Combination Sum recursion throw an infinite loop/StackOverflow?

  // Target: 7, Candidates: [2, 3, 6, 7]
  private void backtrack(List<List<Integer>> res, List<Integer> temp, int[] cands, int remain, int start) {
      if (remain < 0) return;
      if (remain == 0) { res.add(new ArrayList<>(temp)); return; }
      
      for (int i = start; i < cands.length; i++) {
          temp.add(cands[i]);
          // BUG HERE
          backtrack(res, temp, cands, remain - cands[i], 0);
          temp.remove(temp.size() - 1);
      }
  }

  SOLUTION:
    The recursive call passes `0` as the `start` index instead of `i`. This means it always restarts checking from index 0, allowing permutations (e.g., [2,2,3] and [3,2,2]) and causing massive redundant exploration.
    Fix: Pass `i` (if numbers can be reused) or `i + 1` (if numbers cannot be reused) as the new `start` index.

────────────────────────────────────────────────────────────────────────────────
  9. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  - Database Query Optimizers: Greedy algorithms are often used to select the cheapest execution plan by making locally optimal index/join choices.
  - Regular Expressions: Regex engines use backtracking extensively to match complex patterns (though excessive backtracking can cause catastrophic performance issues, hence ReDoS attacks).
  - Scheduling/Resource Allocation: CPU process scheduling, room bookings, and packing problems often use greedy heuristics when an exact optimal solution (NP-Hard) is too slow to compute.

────────────────────────────────────────────────────────────────────────────────
  10. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

  -> File 022: DP_Foundations_1D.md (Learn when Greedy fails and DP is required.)
  -> File 016: Trees_Traversals.md (Understanding the recursion trees behind Backtracking.)

================================================================================
  END OF FILE 024
================================================================================
