import os
import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta

def generate_synthetic_data(num_samples=10000):
    fake = Faker()
    np.random.seed(42)
    Faker.seed(42)

    data = []
    
    # Base churn probabilities for realistic data
    plan_tiers = ['Basic', 'Standard', 'Premium', 'Enterprise']
    regions = ['North America', 'Europe', 'Asia Pacific', 'Latin America']
    
    for _ in range(num_samples):
        # Time aspects
        cycle_end = fake.date_time_between(start_date='-30d', end_date='now')
        cycle_start = cycle_end - timedelta(days=30)
        
        # Categorical
        plan_tier = np.random.choice(plan_tiers, p=[0.4, 0.3, 0.2, 0.1])
        region = np.random.choice(regions)
        is_autopay = np.random.choice([0, 1], p=[0.3, 0.7])
        is_discounted = np.random.choice([0, 1], p=[0.8, 0.2])
        has_family_bundle = np.random.choice([0, 1], p=[0.75, 0.25])
        
        # Base numerical metrics
        tenure_months = max(1, int(np.random.normal(loc=18, scale=12)))
        billing_amount = {
            'Basic': np.random.uniform(10, 30),
            'Standard': np.random.uniform(30, 60),
            'Premium': np.random.uniform(60, 100),
            'Enterprise': np.random.uniform(100, 300)
        }[plan_tier]
        
        if is_discounted:
            billing_amount *= 0.8
            
        last_payment_days_ago = max(0, int(np.random.normal(loc=15, scale=10)))
        
        # Usage metrics
        monthly_usage_hours = max(0, np.random.normal(loc=50, scale=20))
        active_days = min(30, max(1, int(np.random.normal(loc=15, scale=8))))
        login_count = int(active_days * np.random.uniform(0.5, 3.0))
        avg_session_min = max(5, np.random.normal(loc=25, scale=10))
        device_count = np.random.randint(1, 5)
        add_on_count = np.random.randint(0, 4)
        
        # Support and engagement
        support_tickets = np.random.randint(0, 5)
        sla_breaches = np.random.randint(0, 2) if support_tickets > 0 else 0
        promotions_redeemed = np.random.randint(0, 3)
        email_opens = np.random.randint(0, 10)
        email_clicks = min(email_opens, np.random.randint(0, 5))
        last_campaign_days_ago = np.random.randint(1, 60)
        nps_score = np.random.randint(0, 11)
        
        # Calculate a realistic churn probability score based on factors
        churn_risk = 0.0
        if tenure_months < 6: churn_risk += 0.2
        if support_tickets > 2: churn_risk += 0.15
        if nps_score <= 6: churn_risk += 0.2
        if monthly_usage_hours < 20: churn_risk += 0.1
        if not is_autopay: churn_risk += 0.1
        if plan_tier == 'Basic': churn_risk += 0.05
        
        # Target ~18-22% overall churn rate
        churn_prob = min(0.9, max(0.05, churn_risk))
        churned_next_cycle = np.random.choice([0, 1], p=[1 - churn_prob, churn_prob])
        
        data.append({
            'customer_id': f"#USR-{fake.unique.random_number(digits=5, fix_len=True)}",
            'cycle_start': cycle_start,
            'cycle_end': cycle_end,
            'billing_amount': round(billing_amount, 2),
            'last_payment_days_ago': last_payment_days_ago,
            'plan_tier': plan_tier,
            'tenure_months': tenure_months,
            'monthly_usage_hours': round(monthly_usage_hours, 1),
            'active_days': active_days,
            'login_count': login_count,
            'avg_session_min': round(avg_session_min, 1),
            'device_count': device_count,
            'add_on_count': add_on_count,
            'support_tickets': support_tickets,
            'sla_breaches': sla_breaches,
            'promotions_redeemed': promotions_redeemed,
            'email_opens': email_opens,
            'email_clicks': email_clicks,
            'last_campaign_days_ago': last_campaign_days_ago,
            'nps_score': nps_score,
            'region': region,
            'is_autopay': is_autopay,
            'is_discounted': is_discounted,
            'has_family_bundle': has_family_bundle,
            'churned_next_cycle': churned_next_cycle
        })

    df = pd.DataFrame(data)
    
    # Adjust overall churn rate to strictly fall into 18-22% if it's off
    current_churn = df['churned_next_cycle'].mean()
    if current_churn < 0.18 or current_churn > 0.22:
        target_churn = np.random.uniform(0.18, 0.22)
        diff = target_churn - current_churn
        if diff > 0:
            # Need more churners
            non_churners = df[df['churned_next_cycle'] == 0].index
            num_to_flip = int(diff * len(df))
            flip_idx = np.random.choice(non_churners, size=num_to_flip, replace=False)
            df.loc[flip_idx, 'churned_next_cycle'] = 1
        else:
            # Need fewer churners
            churners = df[df['churned_next_cycle'] == 1].index
            num_to_flip = int(abs(diff) * len(df))
            flip_idx = np.random.choice(churners, size=num_to_flip, replace=False)
            df.loc[flip_idx, 'churned_next_cycle'] = 0

    return df

if __name__ == "__main__":
    print("Generating synthetic data...")
    os.makedirs('data', exist_ok=True)
    df = generate_synthetic_data(10000)
    
    csv_path = 'data/churn_frame.csv'
    parquet_path = 'data/churn_frame.parquet'
    
    df.to_csv(csv_path, index=False)
    df.to_parquet(parquet_path, index=False)
    
    print(f"Data generated and saved to {csv_path} and {parquet_path}")
    print(f"Dataset shape: {df.shape}")
    print(f"Churn rate: {df['churned_next_cycle'].mean():.2%}")