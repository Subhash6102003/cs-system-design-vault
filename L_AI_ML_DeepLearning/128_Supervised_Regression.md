================================================================================
  FILE 128: Supervised Regression
  Section: L - AI/ML/Deep Learning
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  This document covers Supervised Regression models. Prerequisites include linear algebra and ML foundations. You will learn about linear regression, gradient descent, polynomial regression, regularization (Ridge/Lasso/ElasticNet), and evaluation metrics.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  LINEAR REGRESSION
    Modeling the linear relationship between a dependent variable and independent variables.

  MSE (MEAN SQUARED ERROR)
    Average of squared differences between predicted and actual values.

  GRADIENT DESCENT
    Optimization algorithm to find minimum of a function (Batch, SGD, Mini-batch).

  NORMAL EQUATION
    Analytical solution to find the optimum weights for linear regression.

  POLYNOMIAL REGRESSION
    Expanding features to polynomial terms for non-linear relationships.

  R-SQUARED (R²)
    Proportion of variance in dependent variable explained by the model.

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  Gradient Descent:                                                      │
  │                                                                         │
  │       \      /                                                          │
  │        \    /                                                           │
  │         \  /                                                            │
  │          \/ (Global Minimum)                                            │
  │  Step towards the bottom via negative gradient.                         │
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
  │  def normal_equation(X, y):                                             │
  │      X_b = np.c_[np.ones((len(X), 1)), X] # Add bias term               │
  │      theta_best = np.linalg.inv(X_b.T.dot(X_b)).dot(X_b.T).dot(y)       │
  │      return theta_best                                                  │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: Python]

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  from sklearn.linear_model import Ridge                                 │
  │  from sklearn.metrics import mean_squared_error, r2_score               │
  │  from sklearn.model_selection import train_test_split                   │
  │                                                                         │
  │  def train_ridge_model(X, y, alpha=1.0):                                │
  │      X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)│
  │                                                                         │
  │      model = Ridge(alpha=alpha)                                         │
  │      model.fit(X_train, y_train)                                        │
  │                                                                         │
  │      predictions = model.predict(X_test)                                │
  │      mse = mean_squared_error(y_test, predictions)                      │
  │      r2 = r2_score(y_test, predictions)                                 │
  │                                                                         │
  │      return model, mse, r2                                              │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: What are the assumptions of linear regression?

  ANSWER:
    Linearity, independence, homoscedasticity, and normal distribution of errors.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: Difference between Batch GD, SGD, and Mini-batch GD?

  ANSWER:
    Batch uses all data per step, SGD uses one sample, Mini-batch uses a subset.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: Why use Ridge regression over standard Linear Regression?

  ANSWER:
    Ridge introduces L2 penalty, reducing overfitting when features are highly correlated or p > n.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: How do you evaluate a regression model?

  ANSWER:
    Using metrics like MSE, RMSE, MAE, and R-squared.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: What is ElasticNet?

  ANSWER:
    A combination of L1 and L2 regularization.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: How does polynomial regression relate to linear regression?

  ANSWER:
    It's a linear model, but applied to transformed polynomial features.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q7: What is multicollinearity?

  ANSWER:
    When independent variables are highly correlated, leading to unstable coefficients.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q8: What does an R² of 0 mean?

  ANSWER:
    The model explains none of the variability; it performs as poorly as just predicting the mean.

────────────────────────────────────────────────────────────────────────────────
  7. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 2: What's Wrong

  from sklearn.linear_model import LinearRegression
  model = LinearRegression()
  model.fit(X, y)

  SOLUTION:
    

────────────────────────────────────────────────────────────────────────────────
  8. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  Regression models are used constantly for forecasting, pricing, and risk modeling. They are lightweight, highly interpretable, and serve as strong baselines before complex neural networks are introduced.

────────────────────────────────────────────────────────────────────────────────
  9. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

  -> File 127: ML Foundations (related topic)
  -> File 131: Model Evaluation & Tuning (related topic)
================================================================================
  END OF FILE 128
================================================================================
