================================================================================
  FILE 009: Two Pointers & Sliding Window
  Section: B - DSA in Java
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  Two Pointers and Sliding Window Techniques
  These techniques optimize nested loops (O(N^2)) into single passes (O(N)). Two Pointers often involves moving pointers from opposite ends or at different speeds. Sliding Window is ideal for finding contiguous subsets (subarrays/substrings).
  Prerequisites: Arrays, Big-O.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  Two Pointers (Opposite Ends)
    left starts at 0, right starts at N-1. Often used on sorted arrays.

  Two Pointers (Same Direction/Fast & Slow)
    Often used for linked lists or cyclic detection.

  Sliding Window (Fixed Size)
    The window size remains constant as it moves.

  Sliding Window (Variable Size)
    The window expands/shrinks based on a condition.

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  DIAGRAM                                                                │
  │                                                                         │
  │  Two Pointers (Opposite):                                               │
  │  [ 1,  2,  3,  4,  5 ]                                                  │
  │    ^               ^                                                    │
  │   left           right                                                  │
  │                                                                         │
  │  Sliding Window (Variable):                                             │
  │  [ 1,  2,  3,  4,  5 ]                                                  │
  │        ^       ^                                                        │
  │      left    right (expand right, shrink left)                          │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: Java]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Demo Code                                                            │
  │                                                                          │
  │  // Two Sum II (Sorted Array)                                            │
  │  public int[] twoSum(int[] numbers, int target) {                        │
  │      int left = 0, right = numbers.length - 1;                           │
  │      while (left < right) {                                              │
  │          int sum = numbers[left] + numbers[right];                       │
  │          if (sum == target) return new int[]{left + 1, right + 1};       │
  │          else if (sum < target) left++;                                  │
  │          else right--;                                                   │
  │      }                                                                   │
  │      return new int[]{-1, -1};                                           │
  │  }                                                                       │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: Java]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │                                                                          │
  │  // Longest Substring Without Repeating Characters                       │
  │  public int lengthOfLongestSubstring(String s) {                         │
  │      int[] chars = new int[128]; // ASCII map                            │
  │      int left = 0, right = 0;                                            │
  │      int maxLen = 0;                                                     │
  │                                                                          │
  │      while (right < s.length()) {                                        │
  │          char r = s.charAt(right);                                       │
  │          chars[r]++;                                                     │
  │                                                                          │
  │          while (chars[r] > 1) {                                          │
  │              char l = s.charAt(left);                                    │
  │              chars[l]--;                                                 │
  │              left++;                                                     │
  │          }                                                               │
  │                                                                          │
  │          maxLen = Math.max(maxLen, right - left + 1);                    │
  │          right++;                                                        │
  │      }                                                                   │
  │      return maxLen;                                                      │
  │  }                                                                       │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  7. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: When should you use a sliding window?

  ANSWER:
    For questions asking for longest/shortest/optimal contiguous subarray or substring.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: What is the time complexity of variable sliding window?

  ANSWER:
    O(N) total, because `left` and `right` both traverse the array at most once.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: Can Two Pointers be used on unsorted arrays?

  ANSWER:
    Only for certain problems like partitioning or fast/slow pointers. Opposite-end pointers usually require sorted data.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: How does Trapping Rain Water use two pointers?

  ANSWER:
    Maintain `leftMax` and `rightMax`, move the pointer pointing to the smaller max to safely compute trapped water.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: What is the space complexity of these techniques?

  ANSWER:
    Usually O(1) auxiliary space, making them highly efficient.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: What pattern is 3Sum?

  ANSWER:
    Sort the array, then iterate `i` and use Two Pointers for the remaining sum.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q7: How to handle negative numbers in Sliding Window?

  ANSWER:
    Variable sliding window logic often breaks if negative numbers can reduce the sum (e.g., Target Sum). In such cases, use Prefix Sum + HashMap instead.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q8: Fast & Slow pointers name?

  ANSWER:
    Floyd's Cycle Finding Algorithm.

────────────────────────────────────────────────────────────────────────────────
  8. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: Challenge

  java
  // Sliding window to find max sum of size k
  int maxSum = 0;
  for(int i=0; i<arr.length-k; i++) {
  int sum = 0;
  for(int j=i; j<i+k; j++) sum += arr[j];
  maxSum = Math.max(maxSum, sum);
  }

  SOLUTION:
    This is O(N*K), not an optimized O(N) sliding window. We should add the new element and subtract the old element as the window shifts.

────────────────────────────────────────────────────────────────────────────────
  9. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  Sliding window is heavily used in networking (TCP sliding window for packet transmission), rate limiting (token buckets over time windows), and stream processing (aggregating logs over the last 5 minutes).

────────────────────────────────────────────────────────────────────────────────
  10. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

  -> File 008: 008_Arrays_Memory_Addressing.md

================================================================================
  END OF FILE 009
================================================================================
