import os
import pandas as pd
import joblib
from src.features import add_features
from src.predict import assign_segment

def batch_score(data_path='data/ingested_churn_frame.parquet'):
    print(f"Batch scoring {data_path}...")
    df = pd.read_parquet(data_path)
    
    df_feat = add_features(df)
    X = df_feat.drop(columns=['customer_id', 'cycle_start', 'cycle_end', 'churned_next_cycle'], errors='ignore')
    
    pipeline = joblib.load('models/churn_calibrated.joblib')
    
    probs = pipeline.predict_proba(X)[:, 1]
    
    df['churn_prob'] = probs
    df['segment'] = df['churn_prob'].apply(assign_segment)
    
    os.makedirs('outputs', exist_ok=True)
    output_path = 'outputs/churn_scores.parquet'
    df.to_parquet(output_path, index=False)
    
    print(f"Batch scores saved to {output_path}")
    print("\nSummary Stats:")
    print(f"Total scored: {len(df)}")
    print(f"Average predicted probability: {df['churn_prob'].mean():.4f}")
    print("\nSegment Distribution:")
    print(df['segment'].value_counts())

if __name__ == "__main__":
    batch_score()