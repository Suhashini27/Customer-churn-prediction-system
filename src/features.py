import pandas as pd
import numpy as np

def add_features(df):
    """
    Add engineered features to the dataset.
    Requires: active_days, login_count, monthly_usage_hours,
    support_tickets, tenure_months, email_clicks, email_opens, billing_amount
    """
    df_feat = df.copy()
    
    # 1. engagement_rate
    # Active days relative to the 30-day cycle
    df_feat['engagement_rate'] = df_feat['active_days'] / 30.0
    
    # 2. usage_per_login
    # Hours of usage per login session
    df_feat['usage_per_login'] = np.where(df_feat['login_count'] > 0, 
                                          df_feat['monthly_usage_hours'] / df_feat['login_count'], 
                                          0)
    
    # 3. support_intensity
    # Support tickets relative to tenure (to capture recent frustration vs long-term baseline)
    df_feat['support_intensity'] = np.where(df_feat['tenure_months'] > 0,
                                            df_feat['support_tickets'] / df_feat['tenure_months'],
                                            df_feat['support_tickets'])
    
    # 4. email_ctr (Click-through rate)
    df_feat['email_ctr'] = np.where(df_feat['email_opens'] > 0,
                                    df_feat['email_clicks'] / df_feat['email_opens'],
                                    0)
    
    # 5. price_to_tenure
    # Ratio of billing amount to tenure months
    df_feat['price_to_tenure'] = np.where(df_feat['tenure_months'] > 0,
                                          df_feat['billing_amount'] / df_feat['tenure_months'],
                                          df_feat['billing_amount'])
                                          
    return df_feat