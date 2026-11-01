================================================================================
  FILE 124: NumPy
  Section: L - AI/ML/Deep Learning
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  This document covers NumPy, the foundational package for numerical computing in Python. Prerequisites include basic Python programming. You will learn about ndarrays, dtypes, indexing/slicing, broadcasting, vectorized operations, linear algebra, random number generation, and performance optimization techniques.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  NDARRAY
    N-dimensional array object.

  DTYPES
    Data types of the elements in the array.

  INDEXING/SLICING
    Accessing specific elements or subarrays.

  BROADCASTING
    Rules for performing mathematical operations on arrays of different shapes.

  VECTORIZATION
    Performing operations on whole arrays without explicit loops.

  CONTIGUOUS MEMORY
    Storing elements in adjacent memory locations for faster access.

  C-ORDER VS F-ORDER
    Row-major (C) vs Column-major (Fortran) memory layouts.

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  Broadcasting Example:                                                  │
  │                                                                         │
  │  [1]       [1, 2, 3]       [2, 3, 4]                                    │
  │  [2]   +   [1, 2, 3]   =   [3, 4, 5]                                    │
  │  [3]       [1, 2, 3]       [4, 5, 6]                                    │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  4. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: Python]

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  // Demo Code                                                           │
  │                                                                         │
  │  import numpy as np                                                     │
  │                                                                         │
  │  a = np.array([1, 2, 3])                                                │
  │  b = np.array([[1], [2], [3]])                                          │
  │  print(a + b)                                                           │
  │                                                                         │
  │  c = np.array([[1, 2], [3, 4]])                                         │
  │  print(np.sum(c, axis=0)) # Sum over rows                               │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: Python]

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  import numpy as np                                                     │
  │  import time                                                            │
  │                                                                         │
  │  def vectorized_vs_loop(size=1000000):                                  │
  │      a = np.random.rand(size)                                           │
  │      b = np.random.rand(size)                                           │
  │                                                                         │
  │      # Loop                                                             │
  │      start = time.time()                                                │
  │      c = np.zeros(size)                                                 │
  │      for i in range(size):                                              │
  │          c[i] = a[i] * b[i]                                             │
  │      loop_time = time.time() - start                                    │
  │                                                                         │
  │      # Vectorized                                                       │
  │      start = time.time()                                                │
  │      c_vec = a * b                                                      │
  │      vec_time = time.time() - start                                     │
  │                                                                         │
  │      return loop_time, vec_time                                         │
  │                                                                         │
  │  print(vectorized_vs_loop())                                            │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: What is broadcasting in NumPy?

  ANSWER:
    Broadcasting allows NumPy to work with arrays of different shapes when performing arithmetic operations.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: Explain the difference between C-order and F-order.

  ANSWER:
    C-order is row-major (elements of a row are contiguous), F-order is column-major.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: How do you reverse a NumPy array?

  ANSWER:
    `arr[::-1]`

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: What is the purpose of `np.newaxis`?

  ANSWER:
    It increases the dimension of the array by one.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: Difference between `np.dot` and `*`?

  ANSWER:
    `np.dot` performs matrix multiplication or dot product, while `*` performs element-wise multiplication.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: How to handle missing values in NumPy?

  ANSWER:
    Use `np.nan` and handle them with functions like `np.nansum`.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q7: What is an advanced indexing in NumPy?

  ANSWER:
    Indexing using integer arrays or boolean arrays.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q8: Why is NumPy faster than Python lists?

  ANSWER:
    Homogeneous data types, contiguous memory allocation, and operations implemented in C.

────────────────────────────────────────────────────────────────────────────────
  7. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: Riddle

  I expand to fit the mold, without copying data, so I'm told. What am I?

  SOLUTION:
    Broadcasting.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 2: What's Wrong

  a = np.array([1, 2, 3])
  b = a
  b[0] = 99

  SOLUTION:
    

────────────────────────────────────────────────────────────────────────────────
  8. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  NumPy forms the core of Pandas, Scikit-learn, and acts as the bridge for data loading in PyTorch/TensorFlow. Efficient vectorization and broadcasting prevent bottlenecks in data preprocessing pipelines.

────────────────────────────────────────────────────────────────────────────────
  9. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

  -> File 123: Math for AI (related topic)
  -> File 125: Pandas (related topic)
================================================================================
  END OF FILE 124
================================================================================
