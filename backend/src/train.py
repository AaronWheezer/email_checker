import argparse
import pandas as pd
from sklearn import pipeline
import mlflow
import mlflow.sklearn
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
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
    
# 3. Load Data
    print(f"Loading data from {args.data}...")
    try:
        df = pd.read_csv(args.data)
    except UnicodeDecodeError:
        df = pd.read_csv(args.data, encoding='latin-1')

    # 4. Preprocessing 
    df = df.dropna(subset=['text', 'label'])
    
    if df['label'].dtype == 'object':
         # Assuming 'spam' and 'ham' are the labels based on your dataset
         df['label'] = df['label'].map({'Spam': 1, 'Ham': 0})
    X = df['text']
    y = df['label'].astype(int)

    # 5. Split Data (DEFINES X_train and y_train)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 6. Build Pipeline (DEFINES pipeline)
    pipeline = Pipeline([
        # Limit features to 10k to manage memory and complexity
        ('vectorizer', CountVectorizer(stop_words='english', max_features=10000)),
        ('classifier', MultinomialNB())
    ])
    print("Training model...")
    pipeline.fit(X_train, y_train) 
    # 7. Evaluate (DEFINES predictions)
    predictions = pipeline.predict(X_test)
    

    # 9. Register the model explicitly with a signature 
    from mlflow.models.signature import infer_signature
    signature = infer_signature(X_test, predictions)

    # --- CRITICAL CHANGE START ---
    # Use 'model' as the path. Azure ML will put this in /outputs/model/
    mlflow.sklearn.save_model(
        sk_model=pipeline,
        path='model', 
        signature=signature
    )
    # --- CRITICAL CHANGE END ---

    print("Model trained and registered.")
    
if __name__ == "__main__":
    main()