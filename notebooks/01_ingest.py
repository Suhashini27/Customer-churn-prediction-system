import os
import pandas as pd

SCHEMA = {
    'customer_id': 'str',
    'cycle_start': 'datetime64[ns]',
    'cycle_end': 'datetime64[ns]',
    'billing_amount': 'float64',
    'last_payment_days_ago': 'int64',
    'plan_tier': 'category',
    'tenure_months': 'int64',
    'monthly_usage_hours': 'float64',
    'active_days': 'int64',
    'login_count': 'int64',
    'avg_session_min': 'float64',
    'device_count': 'int64',
    'add_on_count': 'int64',
    'support_tickets': 'int64',
    'sla_breaches': 'int64',
    'promotions_redeemed': 'int64',
    'email_opens': 'int64',
    'email_clicks': 'int64',
    'last_campaign_days_ago': 'int64',
    'nps_score': 'int64',
    'region': 'category',
    'is_autopay': 'int64',
    'is_discounted': 'int64',
    'has_family_bundle': 'int64',
    'churned_next_cycle': 'int64'
}

def ingest_data(csv_path='data/churn_frame.csv', parquet_path='data/ingested_churn_frame.parquet'):
    print(f"Ingesting data from {csv_path}...")
    
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"{csv_path} not found. Please run data/generate_data.py first.")
        
    df = pd.read_csv(csv_path)
    
    # Enforce schema
    for col, dtype in SCHEMA.items():
        if dtype == 'datetime64[ns]':
            df[col] = pd.to_datetime(df[col])
        elif dtype == 'category':
            df[col] = df[col].astype('category')
        else:
            df[col] = df[col].astype(dtype)
            
    print("Schema enforcement successful.")
    print(f"Shape: {df.shape}")
    print(f"Overall Churn Rate: {df['churned_next_cycle'].mean():.2%}")
    
    os.makedirs('data', exist_ok=True)
    df.to_parquet(parquet_path, index=False)
    print(f"Ingested data saved to {parquet_path}")

if __name__ == "__main__":
    ingest_data()