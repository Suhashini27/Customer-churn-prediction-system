import os
import json
import pandas as pd
import optuna
from xgboost import XGBClassifier
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import average_precision_score
from sklearn.pipeline import Pipeline
from sklearn.calibration import CalibratedClassifierCV
from src.features import add_features
from src.pipeline import get_preprocessor

def tune_optuna(data_path='data/ingested_churn_frame.parquet'):
    print("Loading data for Optuna tuning...")
    df = pd.read_parquet(data_path)
    df = df.sort_values('cycle_end').reset_index(drop=True)
    df = add_features(df)
    
    X = df.drop(columns=['customer_id', 'cycle_start', 'cycle_end', 'churned_next_cycle'])
    y = df['churned_next_cycle']
    
    preprocessor = get_preprocessor()
    X_preprocessed = preprocessor.fit_transform(X)
    
    scale_pos_weight = (len(y) - sum(y)) / sum(y)
    
    def objective(trial):
        params = {
            'n_estimators': trial.suggest_int('n_estimators', 100, 500),
            'max_depth': trial.suggest_int('max_depth', 3, 10),
            'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3, log=True),
            'subsample': trial.suggest_float('subsample', 0.6, 1.0),
            'colsample_bytree': trial.suggest_float('colsample_bytree', 0.6, 1.0),
            'min_child_weight': trial.suggest_int('min_child_weight', 1, 10),
            'scale_pos_weight': scale_pos_weight,
            'random_state': 42,
            'n_jobs': -1
        }
        
        xgb = XGBClassifier(**params)
        calibrated_clf = CalibratedClassifierCV(xgb, method='isotonic', cv=3)
        
        tscv = TimeSeriesSplit(n_splits=3)
        pr_aucs = []
        
        for train_index, test_index in tscv.split(X_preprocessed):
            X_train, X_test = X_preprocessed[train_index], X_preprocessed[test_index]
            y_train, y_test = y.iloc[train_index], y.iloc[test_index]
            
            calibrated_clf.fit(X_train, y_train)
            y_proba = calibrated_clf.predict_proba(X_test)[:, 1]
            pr_auc = average_precision_score(y_test, y_proba)
            pr_aucs.append(pr_auc)
            
        return sum(pr_aucs) / len(pr_aucs)
    
    study = optuna.create_study(direction='maximize')
    print("Starting Optuna optimization (40 trials)...")
    study.optimize(objective, n_trials=40)
    
    print("\nBest params found by Optuna:")
    print(study.best_params)
    
    os.makedirs('models', exist_ok=True)
    with open('models/best_params.json', 'w') as f:
        json.dump(study.best_params, f)
        
    print("Saved best_params.json to models/")

if __name__ == "__main__":
    tune_optuna()