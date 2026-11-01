================================================================================
  FILE 125: Pandas
  Section: L - AI/ML/Deep Learning
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  This document covers Pandas, the premier data manipulation library in Python. You will learn about Series, DataFrames, indexing, GroupBy operations, merging, handling missing data, and performing complete Exploratory Data Analysis (EDA) workflows.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  SERIES
    A 1D labeled array.

  DATAFRAME
    A 2D labeled data structure with columns of potentially different types.

  LOC/ILOC
    Label-based (`loc`) and integer-position based (`iloc`) indexers.

  GROUPBY
    Process involving splitting data, applying a function, and combining the results.

  MERGE/JOIN
    Combining DataFrames based on keys or indices.

  MISSING DATA
    Represented as NaN (Not a Number), requires special handling.

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  DataFrame Structure:                                                   │
  │                                                                         │
  │  Index | Col A | Col B                                                  │
  │  ---------------------                                                  │
  │    0   |   10  |  'X'                                                   │
  │    1   |   20  |  'Y'                                                   │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  GroupBy Concept:                                                       │
  │                                                                         │
  │  [Data] -> Split by Key -> Apply Function per Key -> Combine to [Result]│
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  4. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: Python]

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  // Demo Code                                                           │
  │                                                                         │
  │  import pandas as pd                                                    │
  │                                                                         │
  │  data = {'Name': ['Alice', 'Bob', 'Charlie'], 'Age': [25, 30, 35]}      │
  │  df = pd.DataFrame(data)                                                │
  │                                                                         │
  │  print(df.loc[0, 'Name']) # Alice                                       │
  │  print(df.iloc[1, 1])     # 30                                          │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: Python]

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  import pandas as pd                                                    │
  │                                                                         │
  │  def clean_and_aggregate_data(file_path):                               │
  │      # Read data                                                        │
  │      df = pd.read_csv(file_path)                                        │
  │                                                                         │
  │      # Handle missing values                                            │
  │      df.fillna({'Age': df['Age'].median(), 'City': 'Unknown'}, inplace=True)│
  │                                                                         │
  │      # GroupBy operation                                                │
  │      summary = df.groupby('City').agg(                                  │
  │          avg_age=('Age', 'mean'),                                       │
  │          count=('Name', 'count')                                        │
  │      ).reset_index()                                                    │
  │                                                                         │
  │      return summary                                                     │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: Difference between `loc` and `iloc`?

  ANSWER:
    `loc` is label-based, `iloc` is integer position-based.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: How does `merge` differ from `concat`?

  ANSWER:
    `merge` joins on columns/indices (like SQL JOIN), `concat` stacks DataFrames vertically or horizontally.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: What is the split-apply-combine strategy?

  ANSWER:
    Splitting data into groups based on some criteria, applying a function to each group independently, and combining results.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: How to handle missing data?

  ANSWER:
    `dropna()` to remove, `fillna()` or interpolation to impute.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: Explain pivot tables in pandas.

  ANSWER:
    A tool to summarize and aggregate data, reshaping it based on index and columns.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: How to optimize memory in pandas?

  ANSWER:
    Downcast numerical types, use categorical types for low cardinality strings.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q7: Vectorization in pandas?

  ANSWER:
    Applying operations over whole columns without iterating, utilizing underlying C implementations.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q8: How to apply a custom function?

  ANSWER:
    Using `apply()`, `applymap()`, or `map()`.

────────────────────────────────────────────────────────────────────────────────
  7. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 2: What's Wrong

  df[df['Age'] > 20]['Name'] = 'Adult'

  SOLUTION:
    

────────────────────────────────────────────────────────────────────────────────
  8. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  Pandas is the standard for data wrangling before feeding data into ML models. Efficient data manipulation saves hours of processing time and prevents errors down the pipeline.

────────────────────────────────────────────────────────────────────────────────
  9. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

  -> File 124: NumPy Guide (related topic)
  -> File 126: Data Visualization (related topic)
================================================================================
  END OF FILE 125
================================================================================
