import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import average_precision_score
from sklearn.pipeline import Pipeline
from src.features import add_features
from src.pipeline import get_preprocessor

def train_baselines(data_path='data/ingested_churn_frame.parquet'):
    print("Loading data for baseline training...")
    df = pd.read_parquet(data_path)
    
    # Sort by cycle_end for TimeSeriesSplit
    df = df.sort_values('cycle_end').reset_index(drop=True)
    
    # Feature engineering
    df = add_features(df)
    
    X = df.drop(columns=['customer_id', 'cycle_start', 'cycle_end', 'churned_next_cycle'])
    y = df['churned_next_cycle']
    
    preprocessor = get_preprocessor()
    
    models = {
        'LogisticRegression': LogisticRegression(class_weight='balanced', max_iter=1000, random_state=42),
        'RandomForest': RandomForestClassifier(class_weight='balanced', random_state=42, n_jobs=-1)
    }
    
    tscv = TimeSeriesSplit(n_splits=5)
    
    print("\nTraining Baselines with TimeSeriesSplit (n=5)...")
    
    for name, model in models.items():
        pipeline = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('classifier', model)
        ])
        
        pr_aucs = []
        for train_index, test_index in tscv.split(X):
            X_train, X_test = X.iloc[train_index], X.iloc[test_index]
            y_train, y_test = y.iloc[train_index], y.iloc[test_index]
            
            pipeline.fit(X_train, y_train)
            y_proba = pipeline.predict_proba(X_test)[:, 1]
            
            pr_auc = average_precision_score(y_test, y_proba)
            pr_aucs.append(pr_auc)
            
        mean_pr_auc = np.mean(pr_aucs)
        print(f"[{name}] Mean PR-AUC: {mean_pr_auc:.4f}")

if __name__ == "__main__":
    train_baselines()