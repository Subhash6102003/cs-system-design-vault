================================================================================
  FILE 014: Monotonic Stack and Queue
  Section: B - DSA in Java
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  Monotonic Stacks and Queues are specialized data structures used to solve a specific class of problems efficiently. A monotonic stack or queue is simply a normal stack or queue that maintains its elements in a strictly increasing or decreasing order. 

  Prerequisites: Basic understanding of Stacks, Queues, and Arrays.
  What you'll learn: How to identify problems that require finding the "next greater/smaller element," how to use a monotonic stack to optimize O(N²) naive solutions to O(N) time complexity, and how to apply these concepts to sliding window maximums using a monotonic queue.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  Monotonic
    A sequence is monotonic if it is either entirely non-increasing or non-decreasing.

  Monotonic Increasing Stack
    Elements from bottom to top are in strictly increasing order. If a new element is smaller than or equal to the top element, we pop the top element until the new element is strictly greater than the top.

  Monotonic Decreasing Stack
    Elements from bottom to top are in strictly decreasing order.

  Next Greater Element (NGE)
    The first element to the right (or left) of the current element that is strictly greater than the current element.

  Next Smaller Element (NSE)
    The first element to the right (or left) of the current element that is strictly smaller than the current element.

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  State of a Monotonic Decreasing Stack (Finding NGE)                    │
  │                                                                         │
  │  Given array: [73, 74, 75, 71, 69, 72, 76, 73]                          │
  │                                                                         │
  │  Processing 73: Stack: [73]                                             │
  │  Processing 74: 74 > 73. Pop 73 (NGE of 73 is 74). Push 74. Stack: [74] │
  │  Processing 75: 75 > 74. Pop 74. Push 75. Stack: [75]                   │
  │  Processing 71: 71 < 75. Push 71. Stack: [75, 71]                       │
  │  Processing 69: 69 < 71. Push 69. Stack: [75, 71, 69]                   │
  │  Processing 72: 72 > 69. Pop 69 (NGE is 72). 72 > 71. Pop 71 (NGE is 72). Push 72. Stack: [75, 72] │
  │  Processing 76: 76 > 72. Pop 72. 76 > 75. Pop 75. Push 76. Stack: [76]  │
  │  Processing 73: 73 < 76. Push 73. Stack: [76, 73]                       │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  Language: Java

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Finds the Next Greater Element (NGE) for each element in the array.  │
  │  // Uses a Monotonic Decreasing Stack.                                   │
  │                                                                          │
  │  import java.util.Stack;                                                 │
  │  import java.util.Arrays;                                                │
  │                                                                          │
  │  public class MonotonicStackDemo {                                       │
  │      public static int[] nextGreaterElements(int[] nums) {               │
  │          int[] result = new int[nums.length];                            │
  │          Arrays.fill(result, -1);                                        │
  │          // Stack stores indices of elements                             │
  │          Stack<Integer> stack = new Stack<>();                           │
  │                                                                          │
  │          for (int i = 0; i < nums.length; i++) {                         │
  │              // While stack is not empty and current element is greater than the element at stack top index │
  │              while (!stack.isEmpty() && nums[i] > nums[stack.peek()]) {  │
  │                  int index = stack.pop();                                │
  │                  result[index] = nums[i]; // Found the NGE for nums[index] │
  │              }                                                           │
  │              stack.push(i);                                              │
  │          }                                                               │
  │          return result;                                                  │
  │      }                                                                   │
  │  }                                                                       │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

  Language: Java

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  import java.util.ArrayDeque;                                            │
  │  import java.util.Deque;                                                 │
  │                                                                          │
  │  /**                                                                     │
  │   * Production-ready implementation for sliding window maximum using Monotonic Queue. │
  │   * Time Complexity: O(N), Space Complexity: O(K) where K is window size. │
  │   */                                                                     │
  │  public class MonotonicQueueImpl {                                       │
  │                                                                          │
  │      public int[] maxSlidingWindow(int[] nums, int k) {                  │
  │          if (nums == null || nums.length == 0) return new int[0];        │
  │                                                                          │
  │          int n = nums.length;                                            │
  │          int[] result = new int[n - k + 1];                              │
  │          int ri = 0;                                                     │
  │                                                                          │
  │          // Deque stores indices. Elements are in monotonic decreasing order. │
  │          Deque<Integer> dq = new ArrayDeque<>();                         │
  │                                                                          │
  │          for (int i = 0; i < n; i++) {                                   │
  │              // Remove indices that are out of the current window        │
  │              while (!dq.isEmpty() && dq.peek() < i - k + 1) {            │
  │                  dq.poll();                                              │
  │              }                                                           │
  │                                                                          │
  │              // Remove indices whose values are smaller than the current value │
  │              // They can never be the maximum in this or future windows  │
  │              while (!dq.isEmpty() && nums[dq.peekLast()] < nums[i]) {    │
  │                  dq.pollLast();                                          │
  │              }                                                           │
  │                                                                          │
  │              dq.offer(i);                                                │
  │                                                                          │
  │              // The first element in deque is the maximum for the current window │
  │              if (i >= k - 1) {                                           │
  │                  result[ri++] = nums[dq.peek()];                         │
  │              }                                                           │
  │          }                                                               │
  │                                                                          │
  │          return result;                                                  │
  │      }                                                                   │
  │  }                                                                       │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  7. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: When should you consider using a monotonic stack?

  ANSWER:
    When a problem requires finding the "next greater" or "next smaller" element, or involves calculating areas in a histogram, spans, or evaluating conditions based on elements' relative sizes in a sequence.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: What is the time complexity of building a monotonic stack?

  ANSWER:
    O(N). Even though there is a `while` loop inside a `for` loop, every element is pushed onto the stack exactly once and popped at most once. Thus, operations are bounded by 2N, making it O(N).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: Should we store values or indices in the monotonic stack?

  ANSWER:
    Usually indices. Storing indices allows us to calculate distances (like in Daily Temperatures) and access the actual values from the array when needed.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: How does a Monotonic Queue differ from a Monotonic Stack?

  ANSWER:
    A monotonic queue (usually implemented with a Deque) allows insertion and deletion from both ends, which is crucial for sliding window problems where elements naturally "expire" from the front.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: How do you handle circular arrays with a monotonic stack (e.g., Next Greater Element II)?

  ANSWER:
    You can simulate a circular array by looping twice (up to `2N-1`) and using modulo arithmetic `i % N` to wrap around indices.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: In "Largest Rectangle in Histogram", do you use an increasing or decreasing stack?

  ANSWER:
    Strictly increasing stack. When you encounter a smaller bar, you know the right boundary for the taller bars on the stack, and you can calculate their maximum possible area.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q7: Can monotonic stacks handle duplicate elements?

  ANSWER:
    Yes. Depending on the problem, you may need a strictly monotonic (pop on `>=`) or non-strictly monotonic (pop on `>`) stack.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q8: Why is Monotonic Stack preferred over brute-force O(N²)?

  ANSWER:
    It reduces the redundant comparisons by caching the pending elements that still need a "next greater/smaller" resolution.

────────────────────────────────────────────────────────────────────────────────
  8. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: The Loop Never Ends

  // Trying to find Next Greater Element
  Stack<Integer> stack = new Stack<>();
  for (int i = 0; i < nums.length; i++) {
      while (!stack.isEmpty() && nums[i] > stack.peek()) { // BUG HERE
          result[stack.pop()] = nums[i];
      }
      stack.push(nums[i]); // BUG HERE
  }

  SOLUTION:
    The stack is storing the actual `nums[i]` values instead of the indices `i`. As a result, `result[stack.pop()]` tries to use the array value as an index, causing an `ArrayIndexOutOfBoundsException`.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 2: The Sliding Window that Stopped Sliding

  Deque<Integer> dq = new ArrayDeque<>();
  for (int i = 0; i < nums.length; i++) {
      while (!dq.isEmpty() && nums[dq.peekLast()] < nums[i]) {
          dq.pollLast();
      }
      dq.offer(i);
      // Missing cleanup of out-of-bounds indices!
      if (i >= k - 1) {
          result[ri++] = nums[dq.peek()];
      }
  }

  SOLUTION:
    The code forgets to remove elements from the front of the deque that are no longer in the window (i.e., `dq.peek() < i - k + 1`).

────────────────────────────────────────────────────────────────────────────────
  9. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  In real-world systems, finding local minimums or maximums over a streaming window of data is crucial for:
  - Financial Trading Systems: Calculating real-time moving minimum/maximum stock prices.
  - Network Traffic Monitoring: Identifying bursts of data in time windows.
  - UI Render Engines: Calculating visible bounding boxes or histogram-based layout optimizations.

────────────────────────────────────────────────────────────────────────────────
  10. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

  -> File 010: Stacks_Queues.md (Basic Stack and Queue concepts)
  -> File 015: Binary_Trees_BST.md (Using stacks for iterative traversals)

================================================================================
  END OF FILE 014
================================================================================
