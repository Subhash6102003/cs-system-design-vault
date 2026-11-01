================================================================================
  FILE 140: AI Deployment & MLOps (Machine Learning Operations)
  Section: L - AI/ML/Deep Learning/LLM/RAG
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  Building an accurate ML model in a Jupyter Notebook is only half the battle. Deploying that model into a production environment where it is scalable, reliable, and continuously monitored requires MLOps. MLOps bridges the gap between Data Science and DevOps. You will learn about model serialization (ONNX), containerization (Docker), tracking experiments (MLflow), cloud deployment (AWS SageMaker), and crucial production concepts like Data Drift, A/B testing, and Feature Stores.

  Prerequisites: Deep Learning frameworks (PyTorch/Scikit-Learn), basic software engineering (Git, APIs).

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  MLOps
    A set of practices that aims to deploy and maintain machine learning models in production reliably and efficiently.

  Model Serialization
    Converting a trained model in memory into a file format that can be saved, loaded, and executed elsewhere.
    - Pickle/Joblib: Standard Python formats (security risks, Python-dependent).
    - TorchScript / ONNX (Open Neural Network Exchange): Interoperable formats that allow a model trained in PyTorch to be run in C++, Java, or optimized hardware without needing the original Python code.

  Containerization (Docker)
    Packaging an application (the ML model + API) and all its dependencies (libraries, OS level packages) into a standardized unit (a container). This ensures the code runs exactly the same way on a developer's laptop as it does in the cloud.

  Experiment Tracking
    Logging parameters, metrics, and models during the training phase to compare different runs and ensure reproducibility. MLflow is the industry standard for this.

  Model Registry
    A centralized repository to manage the lifecycle of ML models (Staging, Production, Archived).

  CI/CD for ML (CT - Continuous Training)
    Extending standard CI/CD. When new data arrives or model performance drops, pipelines automatically trigger data validation, model retraining, testing, and deployment.

  AWS SageMaker
    A fully managed AWS service that provides tools for every step of MLOps (Labeling, Training, Deploying endpoints).

  Feature Store
    A centralized repository for storing, managing, and serving ML features (e.g., "User's past 30-day click rate"). Ensures offline training data exactly matches online inference data, preventing training-serving skew.

  Data Drift & Concept Drift
    - Data Drift: Changes in the statistical distribution of the input data (e.g., users get older).
    - Concept Drift: Changes in the relationship between inputs and outputs (e.g., a pandemic changes what people buy, invalidating past buying patterns).

  A/B Testing / Canary Deployment
    Deploying a new model to a small fraction of users (Canary) or routing traffic between Model A and Model B to compare real-world business metrics before a full rollout.

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  The MLOps Lifecycle                                                    │
  │                                                                         │
  │    [ Feature Store ] ------------+                                      │
  │          |                       |                                      │
  │          v                       v                                      │
  │   [ Model Training ] <---- [ Retrain Trigger ]                          │
  │   (Tracked via MLflow)           ^                                      │
  │          |                       | (Drift Detected)                     │
  │          v                       |                                      │
  │   [ Model Registry ]             |                                      │
  │   (Staging -> Prod)              |                                      │
  │          |                       |                                      │
  │          v                       |                                      │
  │   [ CI/CD Pipeline ]             |                                      │
  │   (Docker build)                 |                                      │
  │          |                       |                                      │
  │          v                       |                                      │
  │   [ Model Serving ] ----> [ Monitoring & Observability ]                │
  │   (FastAPI + ONNX)                                                      │
  └─────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  Docker Containerization                                                │
  │                                                                         │
  │   +---------------------------------------+                             │
  │   | Docker Container                      |                             │
  │   |                                       |                             │
  │   |  [ FastAPI App (app.py) ]             |                             │
  │   |  [ Serialized Model (model.onnx) ]    |                             │
  │   |                                       |                             │
  │   |  [ Dependencies (requirements.txt) ]  |                             │
  │   |  [ OS Environment (Ubuntu/Python) ]   |                             │
  │   +---------------------------------------+                             │
  │                     |                                                   │
  │       Runs consistently on AWS, GCP, Azure, or Laptop                   │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  Language: Python

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Experiment Tracking with MLflow                                      │
  │                                                                          │
  │  # pip install mlflow scikit-learn                                       │
  │                                                                          │
  │  import mlflow                                                           │
  │  import mlflow.sklearn                                                   │
  │  from sklearn.ensemble import RandomForestClassifier                     │
  │  from sklearn.datasets import load_iris                                  │
  │  from sklearn.model_selection import train_test_split                    │
  │  from sklearn.metrics import accuracy_score                              │
  │                                                                          │
  │  def train_and_track():                                                  │
  │      # 1. Load Data                                                      │
  │      data = load_iris()                                                  │
  │      X_train, X_test, y_train, y_test = train_test_split(data.data, data.target)│
  │                                                                          │
  │      # 2. Set up MLflow                                                  │
  │      # Start an MLflow run                                               │
  │      with mlflow.start_run(run_name="Iris_Random_Forest"):               │
  │                                                                          │
  │          # Hyperparameters                                               │
  │          n_estimators = 100                                              │
  │          max_depth = 5                                                   │
  │                                                                          │
  │          # Log parameters                                                │
  │          mlflow.log_param("n_estimators", n_estimators)                  │
  │          mlflow.log_param("max_depth", max_depth)                        │
  │                                                                          │
  │          # 3. Train Model                                                │
  │          rf = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth)│
  │          rf.fit(X_train, y_train)                                        │
  │                                                                          │
  │          # 4. Evaluate and Log Metrics                                   │
  │          predictions = rf.predict(X_test)                                │
  │          accuracy = accuracy_score(y_test, predictions)                  │
  │          mlflow.log_metric("accuracy", accuracy)                         │
  │                                                                          │
  │          # 5. Log the Model itself                                       │
  │          mlflow.sklearn.log_model(rf, "random_forest_model")             │
  │                                                                          │
  │          print(f"Model trained with accuracy: {accuracy}")               │
  │          print("Run 'mlflow ui' in terminal to view the dashboard.")     │
  │                                                                          │
  │  if __name__ == "__main__":                                              │
  │      # train_and_track()                                                 │
  │      print("MLflow tracking script ready.")                              │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

  Language: Dockerfile/Python

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Dockerizing a FastAPI Model Server                                   │
  │                                                                          │
  │  To deploy a model, you create an API (like in 139) and package it in a Dockerfile.│
  │                                                                          │
  │  1. requirements.txt                                                     │
  │  fastapi==0.103.1                                                        │
  │  uvicorn==0.23.2                                                         │
  │  pydantic==2.3.0                                                         │
  │  onnxruntime==1.15.1                                                     │
  │  numpy==1.24.3                                                           │
  │                                                                          │
  │  2. app.py (Inference API using ONNX)                                    │
  │  from fastapi import FastAPI                                             │
  │  from pydantic import BaseModel                                          │
  │  import onnxruntime as ort                                               │
  │  import numpy as np                                                      │
  │                                                                          │
  │  app = FastAPI()                                                         │
  │                                                                          │
  │  # Load the ONNX model once on startup                                   │
  │  # (Assume model.onnx exists in the same directory)                      │
  │  # session = ort.InferenceSession("model.onnx")                          │
  │                                                                          │
  │  class PredictRequest(BaseModel):                                        │
  │      features: list[float]                                               │
  │                                                                          │
  │  @app.post("/predict")                                                   │
  │  def predict(request: PredictRequest):                                   │
  │      # Prepare input for ONNX Runtime                                    │
  │      # input_name = session.get_inputs()[0].name                         │
  │      # input_data = np.array([request.features], dtype=np.float32)       │
  │                                                                          │
  │      # Run inference                                                     │
  │      # result = session.run(None, {input_name: input_data})              │
  │                                                                          │
  │      # return {"prediction": result[0].tolist()}                         │
  │      return {"prediction": "dummy_response_for_demo"}                    │
  │                                                                          │
  │  3. Dockerfile                                                           │
  │  # Use an official lightweight Python image                              │
  │  FROM python:3.9-slim                                                    │
  │                                                                          │
  │  # Set working directory in the container                                │
  │  WORKDIR /app                                                            │
  │                                                                          │
  │  # Copy requirements and install dependencies                            │
  │  COPY requirements.txt .                                                 │
  │  RUN pip install --no-cache-dir -r requirements.txt                      │
  │                                                                          │
  │  # Copy the application code and the serialized model                    │
  │  COPY app.py .                                                           │
  │  # COPY model.onnx .                                                     │
  │                                                                          │
  │  # Expose the port the app runs on                                       │
  │  EXPOSE 8000                                                             │
  │                                                                          │
  │  # Command to run the application using Uvicorn                          │
  │  CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]       │
  │                                                                          │
  │  Commands to run (in terminal):                                          │
  │  # Build the Docker image                                                │
  │  # docker build -t my-ml-app .                                           │
  │                                                                          │
  │  # Run the container                                                     │
  │  # docker run -p 8000:8000 my-ml-app                                     │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  7. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: What is the difference between DevOps and MLOps?

  ANSWER:
    DevOps focuses on deploying code (which is deterministic). MLOps focuses on deploying code + data + models. Models degrade over time as data changes (drift), requiring continuous monitoring, retraining, and data validation, which are not present in traditional DevOps.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: Why should you avoid using Python's pickle for model serialization in production?

  ANSWER:
    Security and compatibility. Unpickling can execute arbitrary malicious code. Also, pickle is highly tied to the specific Python version and library versions used during training. ONNX or PMML are language-agnostic and safer.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: What is ONNX and what are its benefits?

  ANSWER:
    Open Neural Network Exchange. It's an open standard for representing ML models. A model trained in PyTorch (Python) can be exported to ONNX and run via ONNX Runtime in C++, Java, or Node.js, providing massive performance boosts and hardware optimization (GPU/CPU/Edge devices) without needing PyTorch installed in production.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: Explain Data Drift vs. Concept Drift.

  ANSWER:
    Data Drift is a shift in the input variables (e.g., a spam filter receives emails with new vocabulary). Concept Drift is a shift in the target variable's relationship to the inputs (e.g., the definition of what constitutes "spam" changes over time). Both require retraining the model.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: What is a Feature Store, and what problem does it solve?

  ANSWER:
    It's a centralized data management system for ML features. It solves "training-serving skew". Often, data scientists write messy pandas code to generate features for training, but data engineers write separate Java code to generate the same features in real-time. A Feature Store ensures the exact same feature logic is used for both offline training and online serving.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: How would you deploy an ML model that requires heavy GPU processing but doesn't need real-time responses?

  ANSWER:
    Use Batch Prediction instead of a real-time REST API. Store input data in a cloud bucket (S3), trigger an ephemeral GPU instance (via AWS SageMaker Batch Transform or Kubernetes Job) to process the data, write results to a database, and shut the GPU down to save costs.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q7: What is MLflow used for?

  ANSWER:
    It manages the ML lifecycle. Specifically, Experiment Tracking (logging hyperparameters, metrics like accuracy, and artifacts like charts to compare different runs), Model Registry (versioning models), and Deployment.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q8: How do you do A/B testing for ML models?

  ANSWER:
    Route 90% of live traffic to the existing model (Control) and 10% to the new model (Variant). Monitor business metrics (e.g., click-through rate, revenue), not just ML metrics (accuracy). If the new model performs better statistically, gradually roll it out to 100%.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q9: What is Shadow Deployment?

  ANSWER:
    A safe deployment strategy where the new model receives real production traffic, but its predictions are not returned to the user. Instead, the predictions are logged and compared to the current live model's predictions to ensure the new model behaves correctly under real loads without risking user experience.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q10: Why use Docker for ML deployment?

  ANSWER:
    It solves the "it works on my machine" problem. ML models have complex dependencies (CUDA versions, specific versions of TensorFlow/PyTorch). Docker isolates the application and guarantees the environment is identical across development, testing, and production servers.

────────────────────────────────────────────────────────────────────────────────
  8. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: The Training-Serving Skew

  # During Training (Jupyter Notebook)
  df['age'] = df['age'].fillna(df['age'].mean())
  model.fit(df)
  
  # During Inference (app.py API)
  @app.post("/predict")
  def predict(request: UserData):
      # No handling of missing age!
      pred = model.predict([request.age, request.income])

  SOLUTION:
    The model was trained with imputation (filling missing ages with the training set's mean). The production API does not do this. If a real user omits their age, the API will crash or the model will fail. The preprocessing logic must be saved (e.g., sklearn.pipeline.Pipeline) and applied during inference.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 2: The GPU API Bottleneck

  @app.post("/predict")
  def predict(image: UploadFile):
      # Model takes 2 seconds to run on CPU
      result = model.predict(image.file)
      return result

  SOLUTION:
    Running heavy models synchronously inside a web request blocks the server. If 10 users hit the API, it will take 20 seconds for the last user to get a response. Heavy ML inference should be placed behind a message queue (like Celery/Redis or Kafka) where workers process requests asynchronously, or use specialized serving tools (Triton Inference Server) that handle dynamic batching.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 3: The Hardcoded Model Path

  model = load_model("/Users/john/desktop/projects/model_v2.pkl")

  SOLUTION:
    When this code is put into a Docker container and deployed to the cloud, the path /Users/john/... will not exist, causing a crash. Models should be loaded using relative paths within the project directory or downloaded dynamically from a cloud storage bucket (S3) or a Model Registry (MLflow) at startup.

────────────────────────────────────────────────────────────────────────────────
  9. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  The "Last Mile" Problem: A staggering number of ML models never make it to production because Data Science teams don't know how to deploy them, and DevOps teams don't understand the models. MLOps engineers are heavily sought after to bridge this gap.
  Cost Management: Leaving GPU instances running 24/7 for an API that gets 10 requests a day is a massive waste of money. MLOps involves knowing how to scale infrastructure down to zero (Serverless inference) or batch process to save costs.
  Trust: If a model's accuracy degrades silently over time (due to drift) and no monitoring alerts are set up, the business loses money and trust in AI.

────────────────────────────────────────────────────────────────────────────────
  10. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

  -> File 139_Building_AI_Apps.md: The FastAPI code that is actually placed inside the Docker container.
  -> File 137_LLM.md: Deploying 70B parameter LLMs requires specialized MLOps infrastructure (like vLLM and multi-GPU serving) compared to standard Scikit-Learn models.
  -> File 132_ANN_DeepLearning.md: The PyTorch code that generates the models we are trying to serialize and deploy.

================================================================================
  END OF FILE 140
================================================================================
