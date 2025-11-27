import argparse
import pandas as pd
import mlflow
import mlflow.sklearn
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score

def main():
    # 1. Start MLflow Run (This connects to Azure ML automatically)
    mlflow.start_run()
    mlflow.sklearn.autolog()

    # 2. Parse arguments (Azure passes the data path here)
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=str, help="Path to input data")
    args = parser.parse_args()

    # 3. Load Data
    print(f"Loading data from {args.data}...")
    # Using 'latin-1' as a fallback, though standard CSVs usually work with utf-8
    try:
        df = pd.read_csv(args.data)
    except UnicodeDecodeError:
        df = pd.read_csv(args.data, encoding='latin-1')

    # 4. Preprocessing based on your description (Text, Label)
    # Ensure no nulls
    df = df.dropna(subset=['Text', 'Label'])
    
    # Map labels if they are strings (assuming dataset might have 'spam'/'ham' or 1/0)
    # If your CSV already has 0 and 1, this line is safe (it just keeps them)
    # If they are strings, we force them to int:
    if df['Label'].dtype == 'object':
         df['Label'] = df['Label'].map({'spam': 1, 'ham': 0})

    X = df['Text']
    y = df['Label'].astype(int)

    print(f"Dataset size: {len(df)} rows")

    # 5. Split Data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 6. Build Pipeline 
    # CountVectorizer: Converts email text to matrix of token counts
    # MultinomialNB: Standard, fast, and effective for Spam classification
    pipeline = Pipeline([
        ('vectorizer', CountVectorizer(stop_words='english', max_features=10000)),
        ('classifier', MultinomialNB())
    ])

    # 7. Train
    print("Training model...")
    pipeline.fit(X_train, y_train)

    # 8. Evaluate
    print("Evaluating model...")
    predictions = pipeline.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    print(f"Accuracy: {accuracy}")
    print(classification_report(y_test, predictions))
    
    # Log specific metric explicitly if needed (Autolog does most of this)
    mlflow.log_metric("accuracy", accuracy)

    # 9. Register the model explicitly with a signature (Important for FastAPI later)
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
    mlflow.end_run()

if __name__ == "__main__":
    main()