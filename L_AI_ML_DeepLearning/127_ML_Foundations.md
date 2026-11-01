================================================================================
  FILE 127: ML Foundations
  Section: L - AI/ML/Deep Learning
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  This document covers the foundations of Machine Learning. Prerequisites include basic math and programming. You will learn about the ML workflow, supervised vs unsupervised vs reinforcement learning, bias-variance tradeoff, regularization, feature scaling, and cross-validation.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  SUPERVISED LEARNING
    Learning with labeled data.

  UNSUPERVISED LEARNING
    Discovering patterns in unlabeled data.

  REINFORCEMENT LEARNING
    Learning through trial and error using rewards.

  TRAIN/VAL/TEST SPLITS
    Partitioning data for model training, tuning, and evaluation.

  BIAS-VARIANCE TRADEOFF
    Balancing model simplicity (bias) and flexibility (variance).

  REGULARIZATION (L1/L2)
    Techniques to prevent overfitting by penalizing large weights.

  FEATURE SCALING
    Standardizing or normalizing features to a similar scale.

  CROSS-VALIDATION
    Resampling procedure to evaluate models on limited data.

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  ML Workflow:                                                           │
  │                                                                         │
  │  Data Collection -> Preprocessing -> Feature Engineering -> Model Selection -> Training -> Evaluation -> Deployment│
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  Bias-Variance:                                                         │
  │                                                                         │
  │  High Bias (Underfitting): Model too simple.                            │
  │  High Variance (Overfitting): Model memorizes training data.            │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  4. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: Python]

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  // Demo Code                                                           │
  │                                                                         │
  │  from sklearn.model_selection import train_test_split                   │
  │  from sklearn.preprocessing import StandardScaler                       │
  │                                                                         │
  │  X, y = [[1], [2], [3], [4]], [0, 0, 1, 1]                              │
  │  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)│
  │                                                                         │
  │  scaler = StandardScaler()                                              │
  │  X_train_scaled = scaler.fit_transform(X_train)                         │
  │  X_test_scaled = scaler.transform(X_test)                               │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: Python]

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  from sklearn.pipeline import Pipeline                                  │
  │  from sklearn.preprocessing import StandardScaler                       │
  │  from sklearn.linear_model import LogisticRegression                    │
  │  from sklearn.model_selection import cross_val_score                    │
  │                                                                         │
  │  def evaluate_model(X, y):                                              │
  │      pipeline = Pipeline([                                              │
  │          ('scaler', StandardScaler()),                                  │
  │          ('classifier', LogisticRegression(penalty='l2', C=1.0))        │
  │      ])                                                                 │
  │                                                                         │
  │      scores = cross_val_score(pipeline, X, y, cv=5, scoring='accuracy') │
  │      return scores.mean(), scores.std()                                 │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: Explain the bias-variance tradeoff.

  ANSWER:
    It is the property that models with lower bias have higher variance, and vice-versa. We seek a sweet spot that minimizes total error.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: What is the difference between L1 and L2 regularization?

  ANSWER:
    L1 (Lasso) promotes sparsity (feature selection), while L2 (Ridge) penalizes large weights heavily without forcing them to zero.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: Why do we need a validation set?

  ANSWER:
    To tune hyperparameters without contaminating the final test set, which should be used only once.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: When should you use k-fold cross-validation?

  ANSWER:
    When dealing with small datasets to get a reliable estimate of model performance.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: What is the difference between Normalization and Standardization?

  ANSWER:
    Normalization scales to [0,1], Standardization scales to mean=0, std=1.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: How do you handle class imbalance?

  ANSWER:
    Oversampling, undersampling, SMOTE, or adjusting class weights.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q7: What is data leakage?

  ANSWER:
    When information from outside the training dataset is used to create the model.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q8: Why is feature scaling important?

  ANSWER:
    Many algorithms (e.g., gradient descent, KNN) are sensitive to feature magnitudes.

────────────────────────────────────────────────────────────────────────────────
  7. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 2: What's Wrong

  scaler = StandardScaler()
  X_train_scaled = scaler.fit_transform(X_train)
  X_test_scaled = scaler.fit_transform(X_test)

  SOLUTION:
    

────────────────────────────────────────────────────────────────────────────────
  8. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  Solid foundations prevent catastrophic failures in production. Data leakage can result in models that look perfect in testing but fail entirely in the real world. Proper regularization ensures robustness against changing data distributions.

────────────────────────────────────────────────────────────────────────────────
  9. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

  -> File 123: Math for AI (related topic)
  -> File 128: Supervised Regression (related topic)
================================================================================
  END OF FILE 127
================================================================================
