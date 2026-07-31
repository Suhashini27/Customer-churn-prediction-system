import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def run_eda(data_path='data/ingested_churn_frame.parquet'):
    print(f"Running EDA on {data_path}...")
    df = pd.read_parquet(data_path)
    
    os.makedirs('outputs', exist_ok=True)
    
    # Class distribution
    print("\nClass Distribution:")
    print(df['churned_next_cycle'].value_counts(normalize=True))
    
    # Missing values
    print("\nMissing Values:")
    print(df.isnull().sum()[df.isnull().sum() > 0])
    
    # 1. Correlation heatmap (numerical only)
    plt.figure(figsize=(12, 10))
    num_cols = df.select_dtypes(include=['int64', 'float64']).columns
    corr = df[num_cols].corr()
    sns.heatmap(corr, cmap='coolwarm', vmin=-1, vmax=1, annot=False)
    plt.title('Correlation Heatmap')
    plt.tight_layout()
    plt.savefig('outputs/correlation.png')
    plt.close()
    
    # 2. Churn by Plan Tier
    plt.figure(figsize=(10, 6))
    sns.barplot(data=df, x='plan_tier', y='churned_next_cycle', errorbar=None, palette='Blues_d')
    plt.title('Churn Rate by Plan Tier')
    plt.ylabel('Churn Rate')
    plt.tight_layout()
    plt.savefig('outputs/churn_by_plan.png')
    plt.close()
    
    # 3. Tenure vs Churn
    plt.figure(figsize=(10, 6))
    sns.histplot(data=df, x='tenure_months', hue='churned_next_cycle', multiple='stack', bins=30, palette='Set1')
    plt.title('Tenure Distribution by Churn')
    plt.tight_layout()
    plt.savefig('outputs/tenure_churn.png')
    plt.close()
    
    # 4. Usage vs Churn
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=df, x='churned_next_cycle', y='monthly_usage_hours', palette='Set2')
    plt.title('Monthly Usage by Churn Status')
    plt.tight_layout()
    plt.savefig('outputs/usage_churn.png')
    plt.close()
    
    print("EDA completed. Plots saved to outputs/")

if __name__ == "__main__":
    run_eda()