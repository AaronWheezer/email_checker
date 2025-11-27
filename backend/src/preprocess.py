# backend/src/preprocess.py
import argparse
import pandas as pd
import os

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw_data", type=str, help="Path to input raw data")
    parser.add_argument("--output_data", type=str, help="Path to output clean data")
    args = parser.parse_args()

    # Load Data
    print(f"Loading data from {args.raw_data}...")
    try:
        df = pd.read_csv(args.raw_data)
    except UnicodeDecodeError:
        df = pd.read_csv(args.raw_data, encoding='latin-1')

    # Preprocessing 
    df = df.dropna(subset=['text', 'label'])
    
    if df['label'].dtype == 'object':
        df['label'] = df['label'].map({'Spam': 1, 'Ham': 0})

    print(f"Cleaned dataset size: {len(df)} rows")
    
    # Save processed data to the output path
    os.makedirs(args.output_data, exist_ok=True)
    output_path = os.path.join(args.output_data, 'processed_spam_data.csv')
    df.to_csv(output_path, index=False)
    print(f"Processed data saved to {output_path}")

if __name__ == "__main__":
    main()