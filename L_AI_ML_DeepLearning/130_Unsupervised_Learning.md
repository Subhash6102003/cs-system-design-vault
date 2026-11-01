================================================================================
  FILE 130: Unsupervised Learning
  Section: L - AI/ML/Deep Learning
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  This document covers Unsupervised Learning. Prerequisites include linear algebra and ML foundations. You will learn about clustering (K-Means, DBSCAN, Hierarchical), dimensionality reduction (PCA, t-SNE, UMAP), and anomaly detection.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  K-MEANS
    Partitions data into K distinct clusters by minimizing variance within clusters.

  K-MEANS++
    Smart initialization for K-Means to avoid local minima.

  DBSCAN
    Density-based clustering, capable of finding arbitrarily shaped clusters and identifying outliers.

  PCA (PRINCIPAL COMPONENT ANALYSIS)
    Linear dimensionality reduction via eigenvalue decomposition to maximize variance.

  T-SNE & UMAP
    Non-linear dimensionality reduction for visualization.

  ANOMALY DETECTION
    Identifying rare items or observations (e.g., Isolation Forest).

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  PCA Concept:                                                           │
  │                                                                         │
  │  Data points in 2D forming an ellipse.                                  │
  │  Principal Component 1: Major axis of ellipse (most variance).          │
  │  Principal Component 2: Minor axis of ellipse (orthogonal to PC1).      │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  4. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: Python]

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  // Demo Code                                                           │
  │                                                                         │
  │  from sklearn.cluster import KMeans                                     │
  │  import numpy as np                                                     │
  │                                                                         │
  │  X = np.array([[1, 2], [1, 4], [1, 0], [10, 2], [10, 4], [10, 0]])      │
  │  kmeans = KMeans(n_clusters=2, random_state=0, n_init='auto').fit(X)    │
  │  print("Cluster Centers:", kmeans.cluster_centers_)                     │
  │  print("Labels:", kmeans.labels_)                                       │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: Python]

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  from sklearn.decomposition import PCA                                  │
  │  from sklearn.preprocessing import StandardScaler                       │
  │  import pandas as pd                                                    │
  │                                                                         │
  │  def apply_pca(df, n_components=2):                                     │
  │      # Scale data (crucial for PCA)                                     │
  │      scaler = StandardScaler()                                          │
  │      scaled_data = scaler.fit_transform(df)                             │
  │                                                                         │
  │      # Apply PCA                                                        │
  │      pca = PCA(n_components=n_components)                               │
  │      principal_components = pca.fit_transform(scaled_data)              │
  │                                                                         │
  │      # Variance explained                                               │
  │      explained_variance = pca.explained_variance_ratio_                 │
  │                                                                         │
  │      pca_df = pd.DataFrame(data=principal_components,                   │
  │                            columns=[f'PC{i+1}' for i in range(n_components)])│
  │      return pca_df, explained_variance                                  │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: How do you choose K in K-Means?

  ANSWER:
    Elbow method (plotting inertia vs K) or Silhouette Score.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: Advantages of DBSCAN over K-Means?

  ANSWER:
    Does not require specifying number of clusters, handles non-spherical clusters, and detects outliers natively.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: How does PCA work mathematically?

  ANSWER:
    Computes the covariance matrix of the data, finds its eigenvectors/eigenvalues, and projects data onto the top eigenvectors.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: Why MUST you scale data before PCA?

  ANSWER:
    PCA seeks to maximize variance. Unscaled features with larger magnitudes will disproportionately dominate the principal components.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: Difference between t-SNE and PCA?

  ANSWER:
    PCA is linear and preserves global structure. t-SNE is non-linear, preserves local structure, and is mainly for visualization.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: What is an Isolation Forest?

  ANSWER:
    An ensemble anomaly detection method that isolates observations by randomly selecting a feature and split value. Anomalies require fewer splits to isolate.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q7: What is hierarchical clustering?

  ANSWER:
    Builds a hierarchy of clusters (agglomerative or divisive), often visualized with a dendrogram.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q8: Why not use t-SNE as a preprocessing step for clustering?

  ANSWER:
    t-SNE distorts distances and densities, meaning clusters in t-SNE space may not reflect true high-dimensional distances.

────────────────────────────────────────────────────────────────────────────────
  7. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 2: What's Wrong

  pca = PCA(n_components=2)
  reduced = pca.fit_transform(X_train)

  SOLUTION:
    

────────────────────────────────────────────────────────────────────────────────
  8. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  Unsupervised learning unlocks insights from unlabeled data. PCA speeds up downstream training by removing noise. Isolation forests are critical for real-time fraud detection and system health monitoring.

────────────────────────────────────────────────────────────────────────────────
  9. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

  -> File 123: Math for AI (Eigenvalues) (related topic)
  -> File 127: ML Foundations (related topic)
================================================================================
  END OF FILE 130
================================================================================
