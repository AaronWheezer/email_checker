import argparse
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
import joblib
import os

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--clean_data", type=str)
    parser.add_argument("--model_output", type=str)
    args = parser.parse_args()

    df = pd.read_csv(os.path.join(args.clean_data, "processed_spam_data.csv"))

    X = df["text"]
    y = df["label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = Pipeline([
        ("vectorizer", CountVectorizer(stop_words="english", max_features=5000)),
        ("classifier", MultinomialNB())
    ])

    model.fit(X_train, y_train)

    # --- SAVE TO MODEL OUTPUT DIRECTORY ---
    os.makedirs(args.model_output, exist_ok=True)
    joblib.dump(model, os.path.join(args.model_output, "model.pkl"))

if __name__ == "__main__":
    main()
