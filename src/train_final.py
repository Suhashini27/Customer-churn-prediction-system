import os
import json
import joblib
import pandas as pd
from xgboost import XGBClassifier
from sklearn.pipeline import Pipeline
from sklearn.calibration import CalibratedClassifierCV
from src.features import add_features
from src.pipeline import get_preprocessor

def train_final(data_path='data/ingested_churn_frame.parquet'):
    print("Training final model...")
    df = pd.read_parquet(data_path)
    df = add_features(df)
    
    X = df.drop(columns=['customer_id', 'cycle_start', 'cycle_end', 'churned_next_cycle'])
    y = df['churned_next_cycle']
    
    scale_pos_weight = (len(y) - sum(y)) / sum(y)
    
    with open('models/best_params.json', 'r') as f:
        best_params = json.load(f)
    
    best_params['scale_pos_weight'] = scale_pos_weight
    best_params['random_state'] = 42
    best_params['n_jobs'] = -1
    
    preprocessor = get_preprocessor()
    xgb = XGBClassifier(**best_params)
    calibrated_xgb = CalibratedClassifierCV(xgb, method='isotonic', cv=5)
    
    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', calibrated_xgb)
    ])
    
    print("Fitting final pipeline on full dataset...")
    pipeline.fit(X, y)
    
    joblib.dump(pipeline, 'models/churn_calibrated.joblib')
    print("Final model saved to models/churn_calibrated.joblib")

if __name__ == "__main__":
    train_final()