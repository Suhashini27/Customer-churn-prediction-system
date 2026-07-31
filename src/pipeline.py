from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

NUMERIC_FEATURES = [
    'billing_amount', 'last_payment_days_ago', 'tenure_months', 
    'monthly_usage_hours', 'active_days', 'login_count', 
    'avg_session_min', 'device_count', 'add_on_count', 
    'support_tickets', 'sla_breaches', 'promotions_redeemed', 
    'email_opens', 'email_clicks', 'last_campaign_days_ago', 
    'nps_score', 'is_autopay', 'is_discounted', 'has_family_bundle',
    'engagement_rate', 'usage_per_login', 'support_intensity', 
    'email_ctr', 'price_to_tenure'
]

CATEGORICAL_FEATURES = [
    'plan_tier', 'region'
]

def get_preprocessor():
    """
    Returns a ColumnTransformer configured for the churn dataset.
    """
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])

    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, NUMERIC_FEATURES),
            ('cat', categorical_transformer, CATEGORICAL_FEATURES)
        ])
        
    return preprocessor