import argparse
import pandas as pd
import mlflow
import mlflow.sklearn
from sklearn.model_selection import train_test_split
# ... (rest of imports) ...

def main():
    # 1. Enable Autologging (Tracks metrics/params in Azure automatically)
    mlflow.sklearn.autolog()
    
    # We rely on Azure ML to establish the run context for the job. 
    # Calling start_run() explicitly often causes the unsupported URI error.
    
    # 2. Parse arguments (Azure will pass the data path here)
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=str, help="Path to input data")
    args = parser.parse_args()
    
    # ... (Load Data, Preprocessing, Splitting, Pipeline build) ...
    
    # 6. Train (MLflow autologs this)
    print("Training model...")
    pipeline.fit(X_train, y_train)

    # ... (Evaluation) ...
    
    # 9. Register the model explicitly with a signature 
    from mlflow.models.signature import infer_signature
    signature = infer_signature(X_test, predictions)
    
    # Save model to the 'outputs' folder so Azure picks it up
    mlflow.sklearn.log_model(
        sk_model=pipeline,
        artifact_path="spam_model",
        signature=signature,
        registered_model_name="Spam_Classifier_Model" 
    )
    
    print("Model trained and registered.")
    # REMOVE mlflow.end_run() - Azure ML handles job termination
    
if __name__ == "__main__":
    main()