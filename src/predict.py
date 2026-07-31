import os
import joblib
import pandas as pd
from src.features import add_features

def assign_segment(prob):
    if prob >= 0.50:
        return 'High'
    elif prob >= 0.25:
        return 'Medium'
    else:
        return 'Low'

def predict_batch(data_path='data/ingested_churn_frame.parquet'):
    print(f"Scoring data from {data_path}...")
    df = pd.read_parquet(data_path)
    
    # Save original for output
    df_out = df[['customer_id', 'plan_tier', 'tenure_months']].copy()
    
    df_feat = add_features(df)
    X = df_feat.drop(columns=['customer_id', 'cycle_start', 'cycle_end', 'churned_next_cycle'], errors='ignore')
    
    pipeline = joblib.load('models/churn_calibrated.joblib')
    
    probs = pipeline.predict_proba(X)[:, 1]
    df_out['churn_prob'] = probs
    df_out['segment'] = df_out['churn_prob'].apply(assign_segment)
    
    # Sort by probability descending
    df_out = df_out.sort_values('churn_prob', ascending=False).reset_index(drop=True)
    
    os.makedirs('outputs', exist_ok=True)
    output_path = 'outputs/predictions.csv'
    df_out.to_csv(output_path, index=False)
    print(f"Predictions saved to {output_path}")
    print(df_out.head(10))

if __name__ == "__main__":
    predict_batch()