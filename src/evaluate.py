import os
import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import shap
from sklearn.metrics import (
    roc_auc_score, average_precision_score, f1_score, 
    confusion_matrix, classification_report
)
from src.features import add_features

def evaluate_model(data_path='data/ingested_churn_frame.parquet'):
    print("Evaluating final model...")
    df = pd.read_parquet(data_path)
    df = add_features(df)
    
    # Sort by cycle end to get the most recent 20% for pseudo-testing
    df = df.sort_values('cycle_end').reset_index(drop=True)
    
    # Evaluate on the last 20% of data
    test_size = int(len(df) * 0.2)
    test_df = df.iloc[-test_size:]
    
    X_test = test_df.drop(columns=['customer_id', 'cycle_start', 'cycle_end', 'churned_next_cycle'])
    y_test = test_df['churned_next_cycle']
    
    pipeline = joblib.load('models/churn_calibrated.joblib')
    
    y_proba = pipeline.predict_proba(X_test)[:, 1]
    y_pred = pipeline.predict(X_test)
    
    # Lift at 10%
    sorted_indices = np.argsort(y_proba)[::-1]
    top_10_percent_idx = sorted_indices[:int(len(y_test) * 0.1)]
    churn_rate_top_10 = y_test.iloc[top_10_percent_idx].mean()
    overall_churn_rate = y_test.mean()
    lift_at_10 = churn_rate_top_10 / overall_churn_rate
    
    print(f"ROC-AUC: {roc_auc_score(y_test, y_proba):.4f}")
    print(f"PR-AUC: {average_precision_score(y_test, y_proba):.4f}")
    print(f"F1 Score: {f1_score(y_test, y_pred):.4f}")
    print(f"Lift@10%: {lift_at_10:.4f}")
    
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    os.makedirs('outputs', exist_ok=True)
    
    # Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title('Confusion Matrix')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.tight_layout()
    plt.savefig('outputs/confusion_matrix.png')
    plt.close()
    
    # SHAP
    # Extract the preprocessor and the first base estimator from the calibrated classifier
    preprocessor = pipeline.named_steps['preprocessor']
    X_test_transformed = preprocessor.transform(X_test)
    
    # Get feature names from preprocessor
    num_features = pipeline.named_steps['preprocessor'].transformers_[0][2]
    cat_features = pipeline.named_steps['preprocessor'].transformers_[1][1].named_steps['onehot'].get_feature_names_out().tolist()
    feature_names = num_features + cat_features
    
    # We use the first underlying XGB model of the calibrated CV
    calibrated_clf = pipeline.named_steps['classifier']
    xgb_model = calibrated_clf.calibrated_classifiers_[0].estimator
    
    explainer = shap.TreeExplainer(xgb_model)
    shap_values = explainer.shap_values(X_test_transformed)
    
    plt.figure(figsize=(10, 8))
    shap.summary_plot(shap_values, X_test_transformed, feature_names=feature_names, show=False)
    plt.tight_layout()
    plt.savefig('outputs/shap_summary.png')
    plt.close()
    
    print("Evaluation completed. Plots saved to outputs/")

if __name__ == "__main__":
    evaluate_model()