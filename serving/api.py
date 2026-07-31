import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pandas as pd
import numpy as np
import joblib
import shap
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Dict, Any, List

from src.features import add_features

app = FastAPI(title="Customer Churn Prediction API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for model and explainer
pipeline = None
explainer = None
feature_names = None

class Customer(BaseModel):
    customer_id: str
    cycle_start: datetime
    cycle_end: datetime
    billing_amount: float
    last_payment_days_ago: int
    plan_tier: str
    tenure_months: int
    monthly_usage_hours: float
    active_days: int
    login_count: int
    avg_session_min: float
    device_count: int
    add_on_count: int
    support_tickets: int
    sla_breaches: int
    promotions_redeemed: int
    email_opens: int
    email_clicks: int
    last_campaign_days_ago: int
    nps_score: int
    region: str
    is_autopay: int
    is_discounted: int
    has_family_bundle: int

@app.on_event("startup")
def load_model():
    global pipeline, explainer, feature_names
    try:
        pipeline = joblib.load("models/churn_calibrated.joblib")
        
        # Setup explainer
        preprocessor = pipeline.named_steps['preprocessor']
        num_features = preprocessor.transformers_[0][2]
        cat_features = preprocessor.transformers_[1][1].named_steps['onehot'].get_feature_names_out().tolist()
        feature_names = num_features + cat_features
        
        calibrated_clf = pipeline.named_steps['classifier']
        xgb_model = calibrated_clf.calibrated_classifiers_[0].estimator
        explainer = shap.TreeExplainer(xgb_model)
        print("Model and explainer loaded successfully.")
    except Exception as e:
        print(f"Error loading model: {e}")

@app.get("/health")
def health_check():
    if pipeline is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    return {"status": "ok", "model_version": "1.0"}

def _prepare_data(customer: Customer) -> pd.DataFrame:
    df = pd.DataFrame([customer.dict()])
    df = add_features(df)
    # Ensure all required columns are present (some might be dropped later by the model, but pipeline expects them)
    return df

@app.post("/score")
def score(customer: Customer):
    df = _prepare_data(customer)
    X = df.drop(columns=['customer_id', 'cycle_start', 'cycle_end'], errors='ignore')
    
    prob = pipeline.predict_proba(X)[0, 1]
    
    segment = "Low"
    if prob >= 0.50:
        segment = "High"
    elif prob >= 0.25:
        segment = "Medium"
        
    return {
        "customer_id": customer.customer_id,
        "churn_prob": float(prob),
        "segment": segment
    }

@app.post("/explain")
def explain(customer: Customer):
    df = _prepare_data(customer)
    X = df.drop(columns=['customer_id', 'cycle_start', 'cycle_end'], errors='ignore')
    
    X_transformed = pipeline.named_steps['preprocessor'].transform(X)
    shap_values = explainer.shap_values(X_transformed)[0]
    
    # Pair feature names with their shap values
    feature_importance = []
    for name, val in zip(feature_names, shap_values):
        feature_importance.append({"feature": name, "impact": float(val)})
        
    # Sort by absolute impact
    feature_importance.sort(key=lambda x: abs(x["impact"]), reverse=True)
    top_5 = feature_importance[:5]
    
    return {
        "customer_id": customer.customer_id,
        "top_features": top_5
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)