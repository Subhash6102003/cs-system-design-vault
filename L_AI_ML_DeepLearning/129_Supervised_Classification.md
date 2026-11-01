================================================================================
  FILE 129: Supervised Classification
  Section: L - AI/ML/Deep Learning
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  This document covers Supervised Classification techniques. You will learn about Logistic Regression, Decision Trees, Random Forests, SVMs, KNN, and Gradient Boosting. We also deep-dive into evaluation metrics like Precision, Recall, F1, and ROC-AUC.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  LOGISTIC REGRESSION
    Linear model for binary classification, using sigmoid function.

  DECISION TREES
    Tree-structured models based on splitting data to maximize information gain (Gini/Entropy).

  RANDOM FOREST
    Ensemble of decision trees using bagging and random feature selection.

  SVM (SUPPORT VECTOR MACHINE)
    Finds a hyperplane that maximizes the margin between classes (Kernel trick for non-linear).

  KNN (K-NEAREST NEIGHBORS)
    Instance-based learning classifying based on nearest neighbors.

  GRADIENT BOOSTING
    Sequential ensemble method correcting errors of previous models (XGBoost, LightGBM).

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  Decision Tree Split:                                                   │
  │                                                                         │
  │            [Feature X > 5?]                                             │
  │           /                \                                            │
  │        Yes                  No                                          │
  │     [Class A]            [Class B]                                      │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  4. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: Python]

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  // Demo Code                                                           │
  │                                                                         │
  │  from sklearn.linear_model import LogisticRegression                    │
  │  from sklearn.metrics import accuracy_score                             │
  │                                                                         │
  │  X_train, y_train = [[1], [2], [10], [11]], [0, 0, 1, 1]                │
  │  clf = LogisticRegression()                                             │
  │  clf.fit(X_train, y_train)                                              │
  │                                                                         │
  │  preds = clf.predict([[3], [9]])                                        │
  │  print("Predictions:", preds) # [0, 1]                                  │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: Python]

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  from xgboost import XGBClassifier                                      │
  │  from sklearn.metrics import classification_report, confusion_matrix    │
  │  from sklearn.model_selection import train_test_split                   │
  │                                                                         │
  │  def train_xgboost(X, y):                                               │
  │      X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)│
  │                                                                         │
  │      # Train XGBoost with early stopping                                │
  │      model = XGBClassifier(n_estimators=100, learning_rate=0.1, max_depth=5)│
  │      model.fit(X_train, y_train)                                        │
  │                                                                         │
  │      # Evaluate                                                         │
  │      preds = model.predict(X_test)                                      │
  │      report = classification_report(y_test, preds)                      │
  │      cm = confusion_matrix(y_test, preds)                               │
  │                                                                         │
  │      return model, report, cm                                           │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: Why is it called Logistic Regression if it's a classification algorithm?

  ANSWER:
    It predicts a continuous probability (regression) using the logistic function, which is then thresholded into a class.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: What is the Kernel Trick in SVM?

  ANSWER:
    Computing the dot product of data in a high-dimensional space without explicitly transforming the data, allowing linear separation of non-linear data.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: Difference between Bagging and Boosting?

  ANSWER:
    Bagging builds independent models in parallel (Random Forest). Boosting builds sequential models, each correcting the previous (XGBoost).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: How do Decision Trees handle categorical variables?

  ANSWER:
    Through one-hot encoding or specific implementations (like LightGBM) that natively split categories.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: Explain Precision vs Recall.

  ANSWER:
    Precision = TP / (TP+FP) (accuracy of positive predictions). Recall = TP / (TP+FN) (ability to find all positives).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: What is the ROC-AUC?

  ANSWER:
    Area under the Receiver Operating Characteristic curve. Measures model ability to distinguish between classes.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q7: When would you prefer KNN?

  ANSWER:
    Small datasets, or when a simple, interpretable, instance-based baseline is needed.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q8: What is Gini Impurity?

  ANSWER:
    A measure of how often a randomly chosen element would be incorrectly labeled if it was randomly labeled according to the distribution of labels in the node.

────────────────────────────────────────────────────────────────────────────────
  7. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 2: What's Wrong

  model = XGBClassifier()
  model.fit(X_train_scaled, y_train)

  SOLUTION:
    

────────────────────────────────────────────────────────────────────────────────
  8. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  Classification is the core of fraud detection, spam filtering, and medical diagnosis. Choosing the right algorithm and threshold balances critical tradeoffs between false positives and false negatives.

────────────────────────────────────────────────────────────────────────────────
  9. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

  -> File 127: ML Foundations (related topic)
  -> File 131: Model Evaluation & Tuning (related topic)
================================================================================
  END OF FILE 129
================================================================================
