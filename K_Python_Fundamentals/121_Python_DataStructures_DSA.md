================================================================================
  FILE 121: Python Data Structures & DSA
  Section: K - Python Fundamentals
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW

────────────────────────────────────────────────────────────────────────────────
  This file maps abstract Data Structures and Algorithms (DSA) concepts to Python's specific built-in types and collections. Python's standard library provides highly optimized C implementations for many common DSA patterns.
  Prerequisites: Python Core Fundamentals, Big-O Notation.
  What you'll learn: Python collection performance (Big-O), `heapq`, `bisect`, `collections` module, algorithm patterns in Python, and Pythonic tricks for competitive programming/interviews.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY

────────────────────────────────────────────────────────────────────────────────
  LIST
    A dynamic array (not a linked list). Fast appends, slow inserts at the beginning.

  DICT
    Hash map. Extremely fast lookups. As of Python 3.7, maintains insertion order.

  SET
    Hash set. Fast membership testing (`O(1)`).

  DEQUE
    Double-ended queue from `collections`. Fast `O(1)` append/pop from both ends.

  HEAPQ
    Min-heap implementation on top of standard lists.

  BISECT
    Binary search algorithms for maintaining sorted lists.

  TWO POINTERS / SLIDING WINDOW
    Algorithmic patterns made easy with Python list slicing and multi-assignment.

────────────────────────────────────────────────────────────────────────────────
  3. DEMO CODE

────────────────────────────────────────────────────────────────────────────────
  [Language: Python]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Demo Code                                                            │
  │                                                                          │
  │  import heapq                                                            │
  │  import bisect                                                           │
  │  from collections import Counter, defaultdict, deque                     │
  │                                                                          │
  │  # 1. heapq (Min-Heap)                                                   │
  │  nums = [5, 7, 9, 1, 3]                                                  │
  │  heapq.heapify(nums)          # O(N) to transform list into heap         │
  │  heapq.heappush(nums, 2)      # O(log N)                                 │
  │  min_val = heapq.heappop(nums) # 1, O(log N)                             │
  │  # To use as Max-Heap, multiply values by -1 before pushing              │
  │                                                                          │
  │  # 2. bisect (Binary Search)                                             │
  │  sorted_arr = [1, 3, 4, 7, 8]                                            │
  │  pos = bisect.bisect_left(sorted_arr, 5) # pos = 3 (where 5 should be inserted)│
  │  bisect.insort(sorted_arr, 5)            # Insert maintaining order: [1, 3, 4, 5, 7, 8]│
  │                                                                          │
  │  # 3. Counter (Frequency Map)                                            │
  │  word = "mississippi"                                                    │
  │  counts = Counter(word)                                                  │
  │  print(counts.most_common(2)) # [('i', 4), ('s', 4)]                     │
  │                                                                          │
  │  # 4. defaultdict (Auto-initialization)                                  │
  │  graph = defaultdict(list)                                               │
  │  graph['A'].append('B') # No KeyError if 'A' doesn't exist               │
  │                                                                          │
  │  # 5. deque (BFS / Queue)                                                │
  │  queue = deque([1, 2, 3])                                                │
  │  queue.append(4)      # Right append O(1)                                │
  │  queue.popleft()      # Left pop O(1), highly preferred over list.pop(0) │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  4. PRODUCTION CODE

────────────────────────────────────────────────────────────────────────────────
  [Language: Python]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │                                                                          │
  │  from collections import deque, defaultdict                              │
  │  from typing import List                                                 │
  │                                                                          │
  │  class GraphAlgorithms:                                                  │
  │      @staticmethod                                                       │
  │      def bfs_shortest_path(edges: List[List[int]], start: int, target: int) -> int:│
  │          """Finds shortest path in unweighted graph using BFS and deque."""│
  │          graph = defaultdict(list)                                       │
  │          for u, v in edges:                                              │
  │              graph[u].append(v)                                          │
  │              graph[v].append(u)                                          │
  │                                                                          │
  │          queue = deque([(start, 0)]) # (node, distance)                  │
  │          visited = {start}                                               │
  │                                                                          │
  │          while queue:                                                    │
  │              node, dist = queue.popleft()                                │
  │              if node == target:                                          │
  │                  return dist                                             │
  │                                                                          │
  │              for neighbor in graph[node]:                                │
  │                  if neighbor not in visited:                             │
  │                      visited.add(neighbor)                               │
  │                      queue.append((neighbor, dist + 1))                  │
  │          return -1                                                       │
  │                                                                          │
  │  class ArrayPatterns:                                                    │
  │      @staticmethod                                                       │
  │      def sliding_window_max_sum(nums: List[int], k: int) -> int:         │
  │          """Fixed size sliding window O(N)."""                           │
  │          if not nums or k <= 0: return 0                                 │
  │          window_sum = sum(nums[:k])                                      │
  │          max_sum = window_sum                                            │
  │                                                                          │
  │          for i in range(k, len(nums)):                                   │
  │              window_sum += nums[i] - nums[i - k]                         │
  │              max_sum = max(max_sum, window_sum)                          │
  │                                                                          │
  │          return max_sum                                                  │
  │                                                                          │
  │  # Pythonic Tricks: Sorting with keys                                    │
  │  students = [('Alice', 95), ('Bob', 80), ('Charlie', 95)]                │
  │  # Sort by grade descending, then name ascending                         │
  │  students.sort(key=lambda x: (-x[1], x[0]))                              │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. INTERVIEW QUESTIONS

────────────────────────────────────────────────────────────────────────────────
  Q1: Why is `list.pop(0)` a bad idea in Python?

  ANSWER:
    A Python list is implemented as an array of contiguous memory pointers. Removing the first element requires shifting all remaining elements left by one index, taking `O(N)` time. Use `collections.deque.popleft()` for `O(1)`.


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: How is a Python `dict` implemented?

  ANSWER:
    It's a hash table. It uses a hash function to map keys to indices in an array. Collisions are handled using open addressing with quadratic probing. (Since 3.7, it also keeps an insertion ordered array).


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: How do you reverse a list efficiently?

  ANSWER:
    `arr[::-1]` (slicing, creates a copy), `arr.reverse()` (in-place `O(N)`), or `reversed(arr)` (returns an iterator, `O(1)` memory).


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: How do you implement a Max-Heap in Python?

  ANSWER:
    `heapq` only provides a min-heap. Multiply all numbers by `-1` before pushing, and multiply by `-1` again when popping.


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: How does `bisect` differ from `list.index`?

  ANSWER:
    `list.index` does a linear search `O(N)`. `bisect` performs binary search `O(log N)` but strictly requires the list to be sorted beforehand.


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: What makes `tuple` hashable while `list` is not?

  ANSWER:
    Tuples are immutable. Hash tables require keys to be immutable so their hash value never changes; otherwise, you couldn't find them in the hash table later.


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q7: Explain the memory/time tradeoff of using `@lru_cache` for DP.

  ANSWER:
    It trades `O(2^N)` time complexity (e.g., naive recursion) for `O(N)` time and `O(N)` space (memory) by caching results in a dictionary behind the scenes.


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q8: Python vs Java for DSA:

  ANSWER:
    Python code is shorter, avoids boilerplate, has built-in tuples for composite keys, and dynamic typing speeds up writing. However, Java runs faster natively and has built-in Treemap (balanced BST), which Python standard library lacks.

────────────────────────────────────────────────────────────────────────────────
  6. RIDDLES & DEBUGGING CHALLENGES

────────────────────────────────────────────────────────────────────────────────
  CHALLENGE 1: 2D Array Initialization



  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  grid = [[0] * 3] * 3


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  grid[0][0] = 1


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  print(grid)


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─




  SOLUTION:
    `*` duplicates the reference to the inner list. Modifying one modifies all rows. Output: `[[1, 0, 0], [1, 0, 0], [1, 0, 0]]`. Fix: `[[0]*3 for _ in range(3)]`.


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 2: Modifying dict keys while iterating



  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  counts = {"a": 1, "b": 2, "c": 3}


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  for k in counts:


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

      if counts[k] % 2 != 0:


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

          del counts[k]


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─




  SOLUTION:
    `RuntimeError: dictionary changed size during iteration`. Fix: iterate over `list(counts.keys())`.


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 3: Tuple Mutability



  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  t = (1, 2, [3, 4])


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  t[2].append(5)


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─




  SOLUTION:
    Nothing! It works. Tuples are immutable regarding *which objects* they point to, but if they point to a mutable object (like a list), the internal state of that object can still change.

────────────────────────────────────────────────────────────────────────────────
  7. WHY THIS MATTERS IN PRODUCTION

────────────────────────────────────────────────────────────────────────────────
  Using the wrong data structure leads to massive CPU spikes. Using `list` for membership checks `item in my_list` `O(N)` instead of a `set` `O(1)` will crash a production server when the list grows to millions of items.

────────────────────────────────────────────────────────────────────────────────
  8. CROSS-REFERENCES

────────────────────────────────────────────────────────────────────────────────
  -> File 120: Python Advanced (Type Hints for DSA)
================================================================================
  END OF FILE 121
================================================================================
