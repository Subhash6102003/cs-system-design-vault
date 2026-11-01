================================================================================
  FILE 023: Dynamic Programming 2D, Knapsack, and Subsequences
  Section: B - DSA in Java
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  2D DP: Grids, Subsequences, and the Knapsack Problem
  This file extends 1D DP concepts into two dimensions. It covers grid navigation, string comparisons, and the legendary Knapsack problem.
  Prerequisites: Solid understanding of 1D DP, state definitions, and transitions.
  What you'll learn: How to manage `dp[i][j]` states, solving classic 2D problems like Longest Common Subsequence (LCS), 0/1 Knapsack, and unbounded variations, plus applying space optimization on 2D matrices.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  2D DP
    The state requires two variables to be uniquely identified. Common scenarios:
    1. Grids: `dp[i][j]` represents the answer at row `i`, col `j`.
    2. Two Strings: `dp[i][j]` represents the answer considering string A up to index `i` and string B up to index `j`.
    3. Items & Capacity (Knapsack): `dp[i][w]` represents using the first `i` items with a knapsack capacity of `w`.

  0/1 Knapsack
    You have a set of items, each with a weight and a value. Determine the items to include in a collection so that the total weight is less than or equal to a given limit, maximizing total value. An item can either be taken (1) or not taken (0).

  Unbounded Knapsack
    Similar to 0/1 Knapsack, but you have an infinite supply of each item.

  Subsequence
    A sequence derived from another sequence by deleting some elements without changing the order of the remaining elements.

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  2D DP Table Filling (Unique Paths)                                     │
  │                                                                         │
  │  Grid size 3x3. Start at (0,0), end at (2,2). Can only move Right or Down.│
  │  dp[i][j] = dp[i-1][j] (from top) + dp[i][j-1] (from left)              │
  │                                                                         │
  │      0    1    2  (cols)                                                │
  │  0 [ 1 ][ 1 ][ 1 ]                                                      │
  │  1 [ 1 ][ 2 ][ 3 ]                                                      │
  │  2 [ 1 ][ 3 ][ 6 ]                                                      │
  │  (rows)      ^                                                          │
  │        (Answer is 6 ways)                                               │
  └─────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  0/1 Knapsack Transition                                                │
  │                                                                         │
  │  Item `i` with weight `wt` and value `val`. We are at capacity `w`.     │
  │  Option 1: Don't take it -> dp[i-1][w]                                  │
  │  Option 2: Take it -> val + dp[i-1][w - wt]                             │
  │  Result: Max(Option 1, Option 2)                                        │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  Language: Java

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  public class Knapsack {                                                 │
  │                                                                          │
  │      // Standard 2D implementation                                       │
  │      public int knapsack2D(int[] weights, int[] values, int W) {         │
  │          int n = weights.length;                                         │
  │          int[][] dp = new int[n + 1][W + 1];                             │
  │                                                                          │
  │          for (int i = 1; i <= n; i++) {                                  │
  │              for (int w = 1; w <= W; w++) {                              │
  │                  if (weights[i-1] <= w) {                                │
  │                      // Max of taking the item vs not taking it          │
  │                      dp[i][w] = Math.max(dp[i-1][w], values[i-1] + dp[i-1][w - weights[i-1]]);│
  │                  } else {                                                │
  │                      dp[i][w] = dp[i-1][w];                              │
  │                  }                                                       │
  │              }                                                           │
  │          }                                                               │
  │          return dp[n][W];                                                │
  │      }                                                                   │
  │                                                                          │
  │      // Space-optimized 1D implementation                                │
  │      // Notice: We iterate backwards through capacities to prevent re-using the same item!│
  │      public int knapsack1D(int[] weights, int[] values, int W) {         │
  │          int n = weights.length;                                         │
  │          int[] dp = new int[W + 1];                                      │
  │                                                                          │
  │          for (int i = 0; i < n; i++) {                                   │
  │              // Traverse right to left                                   │
  │              for (int w = W; w >= weights[i]; w--) {                     │
  │                  dp[w] = Math.max(dp[w], values[i] + dp[w - weights[i]]);│
  │              }                                                           │
  │          }                                                               │
  │          return dp[W];                                                   │
  │      }                                                                   │
  │  }                                                                       │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

  Language: Java

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Problem 1: Longest Common Subsequence (LCS)                          │
  │  class SolutionLCS {                                                     │
  │      public int longestCommonSubsequence(String text1, String text2) {   │
  │          int m = text1.length(), n = text2.length();                     │
  │          int[][] dp = new int[m + 1][n + 1];                             │
  │                                                                          │
  │          // Base cases: implicitly 0 when i=0 or j=0 due to array initialization│
  │          for (int i = 1; i <= m; i++) {                                  │
  │              for (int j = 1; j <= n; j++) {                              │
  │                  if (text1.charAt(i - 1) == text2.charAt(j - 1)) {       │
  │                      // Match! Diagonal + 1                              │
  │                      dp[i][j] = 1 + dp[i - 1][j - 1];                    │
  │                  } else {                                                │
  │                      // No match, take max of skipping char from text1 or text2│
  │                      dp[i][j] = Math.max(dp[i - 1][j], dp[i][j - 1]);    │
  │                  }                                                       │
  │              }                                                           │
  │          }                                                               │
  │                                                                          │
  │          return dp[m][n];                                                │
  │      }                                                                   │
  │  }                                                                       │
  │                                                                          │
  │  // Problem 2: Minimum Path Sum                                          │
  │  class SolutionMinPathSum {                                              │
  │      public int minPathSum(int[][] grid) {                               │
  │          int rows = grid.length;                                         │
  │          int cols = grid[0].length;                                      │
  │                                                                          │
  │          // Overwrite the original grid to save space                    │
  │          for (int i = 0; i < rows; i++) {                                │
  │              for (int j = 0; j < cols; j++) {                            │
  │                  if (i == 0 && j == 0) continue; // Start point          │
  │                                                                          │
  │                  if (i == 0) {                                           │
  │                      grid[i][j] += grid[i][j - 1]; // Top row can only come from left│
  │                  } else if (j == 0) {                                    │
  │                      grid[i][j] += grid[i - 1][j]; // Left col can only come from above│
  │                  } else {                                                │
  │                      grid[i][j] += Math.min(grid[i - 1][j], grid[i][j - 1]);│
  │                  }                                                       │
  │              }                                                           │
  │          }                                                               │
  │                                                                          │
  │          return grid[rows - 1][cols - 1];                                │
  │      }                                                                   │
  │  }                                                                       │
  │                                                                          │
  │  // Problem 3: Coin Change II (Unbounded Knapsack)                       │
  │  class SolutionCoinChange2 {                                             │
  │      public int change(int amount, int[] coins) {                        │
  │          int[] dp = new int[amount + 1];                                 │
  │          dp[0] = 1; // 1 way to make amount 0 (use no coins)             │
  │                                                                          │
  │          // For combinations, coin loop MUST be on the outside!          │
  │          for (int coin : coins) {                                        │
  │              for (int i = coin; i <= amount; i++) {                      │
  │                  dp[i] += dp[i - coin];                                  │
  │              }                                                           │
  │          }                                                               │
  │                                                                          │
  │          return dp[amount];                                              │
  │      }                                                                   │
  │  }                                                                       │
  │                                                                          │
  │  // Problem 4: Edit Distance (Levenshtein Distance)                      │
  │  class SolutionEditDist {                                                │
  │      public int minDistance(String word1, String word2) {                │
  │          int m = word1.length(), n = word2.length();                     │
  │          int[][] dp = new int[m + 1][n + 1];                             │
  │                                                                          │
  │          // Base cases: empty string conversions                         │
  │          for (int i = 0; i <= m; i++) dp[i][0] = i; // Delete all        │
  │          for (int j = 0; j <= n; j++) dp[0][j] = j; // Insert all        │
  │                                                                          │
  │          for (int i = 1; i <= m; i++) {                                  │
  │              for (int j = 1; j <= n; j++) {                              │
  │                  if (word1.charAt(i - 1) == word2.charAt(j - 1)) {       │
  │                      dp[i][j] = dp[i - 1][j - 1]; // Characters match, no operation│
  │                  } else {                                                │
  │                      dp[i][j] = 1 + Math.min(dp[i - 1][j - 1], // Replace│
  │                                     Math.min(dp[i - 1][j],     // Delete │
  │                                              dp[i][j - 1]));   // Insert │
  │                  }                                                       │
  │              }                                                           │
  │          }                                                               │
  │          return dp[m][n];                                                │
  │      }                                                                   │
  │  }                                                                       │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  7. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: In the space-optimized 0/1 Knapsack, why do we loop capacity backwards?

  ANSWER:
    If we loop forwards, when calculating `dp[w]`, we might use `dp[w - weight]`, which has already been updated in the current item's loop. This means we might pick the same item multiple times (unbounded knapsack behavior). Looping backwards ensures we only use states from the previous row (`i-1`).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: In Coin Change II, what happens if we swap the loops (amount outside, coins inside)?

  ANSWER:
    Swapping the loops calculates the number of permutations (where order matters, e.g., 1+2 and 2+1 count as two ways), not combinations. By putting the coin loop outside, we process one coin type completely before moving to the next, enforcing an order and thus finding combinations.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: What is the time and space complexity of Edit Distance?

  ANSWER:
    Time: O(M * N). Space: O(M * N) for the full table, but it can be optimized to O(min(M, N)) because we only ever need the current row and the previous row.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: How does Subset Sum reduce to 0/1 Knapsack?

  ANSWER:
    In Subset Sum (e.g., Partition Equal Subset Sum), the capacity is half the total array sum. The values and weights are the same (the array elements). We try to find if we can achieve exactly the target sum.

────────────────────────────────────────────────────────────────────────────────
  8. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: I let you steal without limits. Fill your bag again and again with the same jewels until it bursts. What problem am I?

  SOLUTION:
    Unbounded Knapsack.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 2: Can you find the bug in this Unique Paths implementation?

  public int uniquePaths(int m, int n) {
      int[][] dp = new int[m][n];
      for (int i = 1; i < m; i++) {
          for (int j = 1; j < n; j++) {
              dp[i][j] = dp[i-1][j] + dp[i][j-1];
          }
      }
      return dp[m-1][n-1];
  }

  SOLUTION:
    The base cases are missing! The first row (`dp[0][j]`) and first column (`dp[i][0]`) are never initialized, meaning they remain `0`. Thus, every inner cell will calculate `0 + 0` and return `0`.
    Fix: Add `for(int i=0; i<m; i++) dp[i][0] = 1;` and `for(int j=0; j<n; j++) dp[0][j] = 1;` before the nested loop.

────────────────────────────────────────────────────────────────────────────────
  9. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  - DNA Sequence Analysis: Bioinformatics heavily relies on variants of Edit Distance and LCS (like the Needleman-Wunsch algorithm) to align protein sequences.
  - Git Merge/Diff: Identifying which lines changed between two file versions relies on LCS algorithms.
  - Inventory/Logistics: Supply chain software uses Knapsack variations to maximize the value of shipments given a container's weight limits.

────────────────────────────────────────────────────────────────────────────────
  10. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

  -> File 022: DP_Foundations_1D.md (Review state transitions and 1D basics)
  -> File 024: Greedy_Backtracking.md (Understanding when Greedy algorithms fail on Knapsack)

================================================================================
  END OF FILE 023
================================================================================
