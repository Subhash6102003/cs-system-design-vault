================================================================================
  FILE 131: Model Evaluation & Tuning
  Section: L - AI/ML/Deep Learning
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  This document covers Model Evaluation and Hyperparameter Tuning. You will learn about cross-validation, grid/random search, Bayesian optimization (Optuna), deep dive into metrics, learning curves, and feature importance using SHAP.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  GRIDSEARCHCV
    Exhaustive search over specified parameter values for an estimator.

  RANDOMIZEDSEARCHCV
    Randomized search over parameters, evaluating a fixed number of combinations.

  BAYESIAN OPTIMIZATION
    Probabilistic model-based optimization to find minimum of objective function efficiently (e.g., Optuna).

  LEARNING CURVES
    Plots showing model performance on train/val sets over varying amounts of training data.

  SHAP (SHAPLEY ADDITIVE EXPLANATIONS)
    Game theoretic approach to explain the output of any machine learning model.

  HYPERPARAMETER
    A parameter whose value is used to control the learning process.

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  Cross Validation (K=5):                                                │
  │                                                                         │
  │  Iter 1: [Test] [Train] [Train] [Train] [Train]                         │
  │  Iter 2: [Train] [Test] [Train] [Train] [Train]                         │
  │  ...                                                                    │
  │  Averages results to prevent overfitting to a single split.             │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  4. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: Python]

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  // Demo Code                                                           │
  │                                                                         │
  │  from sklearn.model_selection import GridSearchCV                       │
  │  from sklearn.svm import SVC                                            │
  │                                                                         │
  │  parameters = {'kernel':('linear', 'rbf'), 'C':[1, 10]}                 │
  │  svc = SVC()                                                            │
  │  clf = GridSearchCV(svc, parameters, cv=5)                              │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: Python]

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  import optuna                                                          │
  │  from sklearn.ensemble import RandomForestClassifier                    │
  │  from sklearn.model_selection import cross_val_score                    │
  │                                                                         │
  │  def objective(trial, X, y):                                            │
  │      # Suggest hyperparameters                                          │
  │      n_estimators = trial.suggest_int('n_estimators', 50, 300)          │
  │      max_depth = trial.suggest_int('max_depth', 3, 20)                  │
  │      min_samples_split = trial.suggest_int('min_samples_split', 2, 10)  │
  │                                                                         │
  │      # Create model                                                     │
  │      clf = RandomForestClassifier(                                      │
  │          n_estimators=n_estimators,                                     │
  │          max_depth=max_depth,                                           │
  │          min_samples_split=min_samples_split                            │
  │      )                                                                  │
  │                                                                         │
  │      # Evaluate                                                         │
  │      score = cross_val_score(clf, X, y, n_jobs=-1, cv=3).mean()         │
  │      return score                                                       │
  │                                                                         │
  │  def run_optuna(X, y):                                                  │
  │      study = optuna.create_study(direction='maximize')                  │
  │      study.optimize(lambda trial: objective(trial, X, y), n_trials=50)  │
  │      return study.best_params                                           │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: Grid Search vs Random Search?

  ANSWER:
    Grid search tries all combinations (computationally expensive). Random search tries a random sample, often finding better models in less time.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: What is Bayesian Optimization?

  ANSWER:
    It builds a probability model of the objective function and uses it to select the most promising hyperparameters to evaluate next.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: How do learning curves diagnose bias/variance?

  ANSWER:
    High bias (underfitting): train and val curves converge to a low score. High variance (overfitting): gap between train and val curves remains large.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: What are SHAP values?

  ANSWER:
    They quantify the contribution of each feature to a specific prediction, ensuring local accuracy and consistency.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: Difference between parameter and hyperparameter?

  ANSWER:
    Parameters are learned from data (e.g., neural network weights). Hyperparameters are set before training (e.g., learning rate).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: Why use stratification in cross-validation?

  ANSWER:
    To ensure each fold has the same proportion of class labels as the original dataset.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q7: What is the macro vs micro average in F1 score?

  ANSWER:
    Macro calculates metric for each class and averages them unweighted. Micro aggregates contributions from all classes to compute average.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q8: When would you use ROC-AUC vs PR-AUC?

  ANSWER:
    Use PR-AUC (Precision-Recall) for heavily imbalanced datasets; ROC-AUC for balanced data.

────────────────────────────────────────────────────────────────────────────────
  7. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 2: What's Wrong

  clf = GridSearchCV(model, params, cv=5)
  clf.fit(X_test, y_test)

  SOLUTION:
    

────────────────────────────────────────────────────────────────────────────────
  8. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  Proper tuning squeezes out the best performance from a model. robust evaluation ensures that what looks good in Jupyter notebooks actually translates to revenue and accuracy in production. SHAP brings transparency for stakeholders.

────────────────────────────────────────────────────────────────────────────────
  9. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

  -> File 129: Supervised Classification (related topic)
  -> File 128: Supervised Regression (related topic)
================================================================================
  END OF FILE 131
================================================================================
