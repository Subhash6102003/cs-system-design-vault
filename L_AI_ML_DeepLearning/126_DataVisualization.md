================================================================================
  FILE 126: Data Visualization
  Section: L - AI/ML/Deep Learning
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  This document covers data visualization techniques in Python using Matplotlib, Seaborn, and Plotly. Prerequisites include Pandas and basic statistics. You will learn chart selection, figure/axes manipulation, statistical plotting, and creating interactive visualizations.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  FIGURE
    The overall window or page that everything is drawn on.

  AXES
    An individual plot within a Figure.

  MATPLOTLIB
    Low-level, fundamental plotting library in Python.

  SEABORN
    High-level interface for statistical graphics, built on Matplotlib.

  PLOTLY
    Library for interactive, web-based plots.

  CHART SELECTION
    Choosing the right visual (e.g., bar, line, scatter) based on data types.

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  Matplotlib Hierarchy:                                                  │
  │                                                                         │
  │  [ Figure ]                                                             │
  │    |-- [ Axes 1 (Subplot) ]                                             │
  │    |     |-- X-axis, Y-axis, Line, Title                                │
  │    |-- [ Axes 2 (Subplot) ]                                             │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  4. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: Python]

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  // Demo Code                                                           │
  │                                                                         │
  │  import matplotlib.pyplot as plt                                        │
  │  import numpy as np                                                     │
  │                                                                         │
  │  x = np.linspace(0, 10, 100)                                            │
  │  y = np.sin(x)                                                          │
  │                                                                         │
  │  fig, ax = plt.subplots()                                               │
  │  ax.plot(x, y, label='Sine Wave')                                       │
  │  ax.set_title('Basic Plot')                                             │
  │  ax.legend()                                                            │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: Python]

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  import seaborn as sns                                                  │
  │  import matplotlib.pyplot as plt                                        │
  │  import pandas as pd                                                    │
  │                                                                         │
  │  def create_correlation_heatmap(df, save_path=None):                    │
  │      plt.figure(figsize=(10, 8))                                        │
  │                                                                         │
  │      # Calculate correlation matrix                                     │
  │      corr = df.corr()                                                   │
  │                                                                         │
  │      # Plot heatmap                                                     │
  │      sns.heatmap(corr, annot=True, cmap='coolwarm', vmin=-1, vmax=1, fmt=".2f")│
  │      plt.title('Feature Correlation Heatmap')                           │
  │      plt.tight_layout()                                                 │
  │                                                                         │
  │      if save_path:                                                      │
  │          plt.savefig(save_path, dpi=300)                                │
  │      plt.close()                                                        │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: When would you use Seaborn instead of Matplotlib?

  ANSWER:
    When needing complex statistical plots (like violin plots or pairplots) with minimal code and better default aesthetics.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: Difference between Figure and Axes?

  ANSWER:
    A Figure is the canvas; Axes are the individual plots on that canvas.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: What chart is best for showing distribution?

  ANSWER:
    Histogram, KDE plot, or Box plot.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: How do you handle overlapping points in a scatter plot?

  ANSWER:
    Adjust alpha (transparency), add jitter, or use a hexbin/density plot.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: Why use Plotly?

  ANSWER:
    For interactive dashboards where users need to hover, zoom, and pan.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: How to save a high-quality image?

  ANSWER:
    `plt.savefig('file.png', dpi=300, bbox_inches='tight')`.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q7: What is a pairplot?

  ANSWER:
    A grid of scatterplots showing pairwise relationships in a dataset.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q8: What do the box and whiskers represent in a boxplot?

  ANSWER:
    Box shows IQR (25th to 75th percentile), line is median, whiskers show range (often 1.5*IQR), points are outliers.

────────────────────────────────────────────────────────────────────────────────
  7. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 2: What's Wrong

  plt.plot(x, y)
  plt.title('My Plot')
  plt.show()
  plt.savefig('plot.png')

  SOLUTION:
    

────────────────────────────────────────────────────────────────────────────────
  8. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  Visualizations are the primary tool for communicating model performance and data insights to stakeholders. Clear, well-designed plots build trust in data-driven systems.

────────────────────────────────────────────────────────────────────────────────
  9. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

  -> File 125: Pandas Guide (related topic)
  -> File 127: ML Foundations (related topic)
================================================================================
  END OF FILE 126
================================================================================
