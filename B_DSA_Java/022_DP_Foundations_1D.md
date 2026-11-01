================================================================================
  FILE 022: Dynamic Programming Foundations & 1D DP
  Section: B - DSA in Java
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  Dynamic Programming: Core Foundations and 1D Problems
  This file introduces Dynamic Programming (DP), a method for solving complex problems by breaking them down into simpler overlapping subproblems. 
  Prerequisites: Recursion, Time/Space Complexity.
  What you'll learn: How to identify DP problems, the differences between Top-Down (Memoization) and Bottom-Up (Tabulation), defining state and transitions, and optimizing memory space for 1D arrays to O(1).

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  Dynamic Programming (DP)
    An algorithmic technique for solving an optimization problem by breaking it down into simpler subproblems and utilizing the fact that the optimal solution to the overall problem depends on the optimal solution to its subproblems.

  Overlapping Subproblems
    The problem can be broken down into subproblems which are reused several times. (E.g., Fibonacci(5) requires Fibonacci(4) and Fibonacci(3). Fibonacci(4) also requires Fibonacci(3)).

  Optimal Substructure
    The optimal solution to a problem can be constructed from optimal solutions of its subproblems.

  Top-Down (Memoization)
    Starting from the main problem, you solve subproblems recursively and cache (memoize) their results to avoid redundant work.

  Bottom-Up (Tabulation)
    Starting from the smallest subproblems, you iteratively build up the solution to the main problem, usually filling an array or table.

  State
    The variables that uniquely identify a subproblem (e.g., `dp[i]` represents the max profit up to day `i`).

  Transition Equation
    The formula that relates a state to its previous states (e.g., `dp[i] = dp[i-1] + dp[i-2]`).

  Base Case
    The simplest subproblem that can be solved directly without further breakdown.

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  Recursion Tree (Fibonacci)                                             │
  │                                                                         │
  │  Without Memoization, Fib(4) calculates Fib(2) twice.                   │
  │                                                                         │
  │                   fib(4)                                                │
  │                 /        \                                              │
  │           fib(3)          fib(2)                                        │
  │          /      \        /      \                                       │
  │    fib(2)      fib(1)  fib(1)  fib(0)                                   │
  │    /    \                                                               │
  │  fib(1) fib(0)                                                          │
  │                                                                         │
  │  Overlapping Subproblem: fib(2) is calculated entirely multiple times!  │
  └─────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  Bottom-Up DP Table Filling Order (Fibonacci)                           │
  │                                                                         │
  │  dp array (size 5):                                                     │
  │  Index:  0    1    2    3    4                                          │
  │  Value: [0]  [1]  [ ]  [ ]  [ ]                                         │
  │                   ^                                                     │
  │              dp[2] = dp[1] + dp[0] = 1                                  │
  │                                                                         │
  │  Index:  0    1    2    3    4                                          │
  │  Value: [0]  [1]  [1]  [2]  [3]                                         │
  │                              ^                                          │
  │                        dp[4] = dp[3] + dp[2]                            │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  4. EXPLANATION & THEORY
────────────────────────────────────────────────────────────────────────────────

  How to Identify DP Problems (3 Indicators)
  1. Problem asks for the maximum/minimum/longest/shortest of something.
  2. Problem asks for the total number of ways to do something.
  3. Future decisions depend on past decisions, but past decisions can be abstracted into a "state".

────────────────────────────────────────────────────────────────────────────────
  5. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  Language: Java

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  public class Fibonacci {                                                │
  │                                                                          │
  │      // 1. Pure Recursion: O(2^n) time, O(n) space (call stack)          │
  │      public int fibRec(int n) {                                          │
  │          if (n <= 1) return n;                                           │
  │          return fibRec(n - 1) + fibRec(n - 2);                           │
  │      }                                                                   │
  │                                                                          │
  │      // 2. Top-Down Memoization: O(n) time, O(n) space                   │
  │      public int fibMemo(int n, Integer[] memo) {                         │
  │          if (n <= 1) return n;                                           │
  │          if (memo[n] != null) return memo[n]; // Return cached result    │
  │                                                                          │
  │          memo[n] = fibMemo(n - 1, memo) + fibMemo(n - 2, memo);          │
  │          return memo[n];                                                 │
  │      }                                                                   │
  │                                                                          │
  │      // 3. Bottom-Up Tabulation: O(n) time, O(n) space                   │
  │      public int fibTab(int n) {                                          │
  │          if (n <= 1) return n;                                           │
  │          int[] dp = new int[n + 1];                                      │
  │          dp[0] = 0;                                                      │
  │          dp[1] = 1;                                                      │
  │                                                                          │
  │          for (int i = 2; i <= n; i++) {                                  │
  │              dp[i] = dp[i-1] + dp[i-2]; // Transition                    │
  │          }                                                               │
  │          return dp[n];                                                   │
  │      }                                                                   │
  │                                                                          │
  │      // 4. Space Optimized Bottom-Up: O(n) time, O(1) space              │
  │      public int fibOpt(int n) {                                          │
  │          if (n <= 1) return n;                                           │
  │          int prev2 = 0; // dp[i-2]                                       │
  │          int prev1 = 1; // dp[i-1]                                       │
  │                                                                          │
  │          for (int i = 2; i <= n; i++) {                                  │
  │              int current = prev1 + prev2;                                │
  │              prev2 = prev1;                                              │
  │              prev1 = current;                                            │
  │          }                                                               │
  │          return prev1;                                                   │
  │      }                                                                   │
  │  }                                                                       │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

  Language: Java

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Problem 1: Climbing Stairs                                           │
  │  class SolutionClimb {                                                   │
  │      public int climbStairs(int n) {                                     │
  │          if (n <= 2) return n;                                           │
  │          int oneStepBefore = 2;                                          │
  │          int twoStepsBefore = 1;                                         │
  │          int allWays = 0;                                                │
  │                                                                          │
  │          for(int i = 3; i <= n; i++){                                    │
  │              allWays = oneStepBefore + twoStepsBefore;                   │
  │              twoStepsBefore = oneStepBefore;                             │
  │              oneStepBefore = allWays;                                    │
  │          }                                                               │
  │          return allWays;                                                 │
  │      }                                                                   │
  │  }                                                                       │
  │                                                                          │
  │  // Problem 2: House Robber I                                            │
  │  class SolutionRob {                                                     │
  │      public int rob(int[] nums) {                                        │
  │          if (nums == null || nums.length == 0) return 0;                 │
  │          if (nums.length == 1) return nums[0];                           │
  │                                                                          │
  │          int prev2 = 0; // dp[i-2]                                       │
  │          int prev1 = nums[0]; // dp[i-1]                                 │
  │                                                                          │
  │          for (int i = 1; i < nums.length; i++) {                         │
  │              int current = Math.max(prev1, prev2 + nums[i]);             │
  │              prev2 = prev1;                                              │
  │              prev1 = current;                                            │
  │          }                                                               │
  │                                                                          │
  │          return prev1;                                                   │
  │      }                                                                   │
  │  }                                                                       │
  │                                                                          │
  │  // Problem 3: Coin Change (Minimum Coins)                               │
  │  class SolutionCoinChange {                                              │
  │      public int coinChange(int[] coins, int amount) {                    │
  │          int[] dp = new int[amount + 1];                                 │
  │          Arrays.fill(dp, amount + 1); // Initialize to an impossible high value│
  │          dp[0] = 0; // Base case: 0 coins needed to make amount 0        │
  │                                                                          │
  │          for (int i = 1; i <= amount; i++) {                             │
  │              for (int coin : coins) {                                    │
  │                  if (coin <= i) {                                        │
  │                      dp[i] = Math.min(dp[i], dp[i - coin] + 1);          │
  │                  }                                                       │
  │              }                                                           │
  │          }                                                               │
  │                                                                          │
  │          return dp[amount] > amount ? -1 : dp[amount];                   │
  │      }                                                                   │
  │  }                                                                       │
  │                                                                          │
  │  // Problem 4: Longest Increasing Subsequence (O(N²))                    │
  │  class SolutionLIS {                                                     │
  │      public int lengthOfLIS(int[] nums) {                                │
  │          if (nums == null || nums.length == 0) return 0;                 │
  │                                                                          │
  │          int[] dp = new int[nums.length];                                │
  │          Arrays.fill(dp, 1); // Every element is an LIS of length 1 on its own│
  │          int maxLength = 1;                                              │
  │                                                                          │
  │          for (int i = 1; i < nums.length; i++) {                         │
  │              for (int j = 0; j < i; j++) {                               │
  │                  if (nums[i] > nums[j]) {                                │
  │                      dp[i] = Math.max(dp[i], dp[j] + 1);                 │
  │                  }                                                       │
  │              }                                                           │
  │              maxLength = Math.max(maxLength, dp[i]);                     │
  │          }                                                               │
  │                                                                          │
  │          return maxLength;                                               │
  │      }                                                                   │
  │  }                                                                       │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  7. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: How do you decide between Top-Down and Bottom-Up DP?

  ANSWER:
    Bottom-Up is generally preferred because it avoids recursion stack overflow and function call overhead. However, Top-Down is easier to write initially since it mirrors the recursion structure, and it implicitly only calculates states that are actually needed, which can be faster if the state space is sparse.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: What is a "Rolling Array" optimization?

  ANSWER:
    When a DP state `dp[i]` only depends on `dp[i-1]` and `dp[i-2]`, we don't need to keep the entire `N`-sized array in memory. We can just keep the last two values, reducing space complexity from O(N) to O(1).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: Why do we initialize `dp` arrays with specific values (like `amount + 1` in Coin Change)?

  ANSWER:
    For minimization problems, we need a baseline "infinity" so that `Math.min()` updates correctly. If we use `Integer.MAX_VALUE`, `dp[i - coin] + 1` might cause an integer overflow to a massive negative number. Thus, `amount + 1` is a safe infinity.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: What's the difference between DP and Divide and Conquer?

  ANSWER:
    Both break problems into subproblems. Divide and Conquer subproblems do NOT overlap (e.g., Merge Sort). DP subproblems overlap, which is why we must cache their results.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: Can you explain the state for Kadane's Algorithm?

  ANSWER:
    Kadane's algorithm for Maximum Subarray is essentially DP! The state `dp[i]` is the max subarray sum ending at index `i`. Transition: `dp[i] = max(nums[i], dp[i-1] + nums[i])`. It's commonly space-optimized to O(1).

────────────────────────────────────────────────────────────────────────────────
  8. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: I remember the past so I don't repeat my mistakes. I build tables from the ground up. What am I?

  SOLUTION:
    Dynamic Programming (Tabulation).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 2: Find the bug in this Top-Down Memoization for Fibonacci:

  public int fib(int n, int[] memo) {
      if (n <= 1) return n;
      if (memo[n] != 0) return memo[n];
      return fib(n-1, memo) + fib(n-2, memo);
  }

  SOLUTION:
    The code calculates the recursive calls but forgets to store the result in the memo array before returning. It will execute in O(2^n) time!
    Fix: `memo[n] = fib(n-1, memo) + fib(n-2, memo); return memo[n];`

────────────────────────────────────────────────────────────────────────────────
  9. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  - String Matching: Spell checkers and diff tools (like Git) use DP (Edit Distance/LCS) to find how close two strings are.
  - Resource Allocation: Knapsack-style DP helps in allocating limited resources (CPU cycles, truck cargo space) for maximum profit.
  - Game AI: Solving game states often relies on DP or memoized searches to avoid re-evaluating board positions.

────────────────────────────────────────────────────────────────────────────────
  10. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

  -> File 023: DP_2D_Knapsack_Subsequences.md (Expanding DP to 2D)
  -> File 024: Greedy_Backtracking.md (When to use Greedy instead of DP)

================================================================================
  END OF FILE 022
================================================================================
