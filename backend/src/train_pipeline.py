# backend/src/train_pipeline.py
import argparse
import pandas as pd
import mlflow
import mlflow.sklearn
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from mlflow.models.signature import infer_signature
import os

def main():
    mlflow.sklearn.autolog()
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--clean_data", type=str, help="Path to input clean data (folder)")
    parser.add_argument("--model_output", type=str, help="Path to output model")
    args = parser.parse_args()
    
    # Load the processed CSV file from the input directory
    input_file = os.path.join(args.clean_data, 'processed_spam_data.csv')
    df = pd.read_csv(input_file)

    X = df['text']
    y = df['label'].astype(int)

    # Split Data 
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Build and Train Pipeline
    pipeline = Pipeline([
        ('vectorizer', CountVectorizer(stop_words='english', max_features=10000)),
        ('classifier', MultinomialNB())
    ])
    print("Training model...")
    pipeline.fit(X_train, y_train) 
    
    # Evaluate
    predictions = pipeline.predict(X_test)
    
    # Save Model Artifact using MLflow
    signature = infer_signature(X_test, predictions)
    
    # IMPORTANT: Save model to the path specified by the pipeline output
    mlflow.sklearn.save_model(
        sk_model=pipeline,
        path=args.model_output, 
        signature=signature
    )
    
    print(f"Model saved to: {args.model_output}")

if __name__ == "__main__":
    main()