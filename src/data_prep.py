import pandas as pd
import numpy as np
import os

def prepare_data(input_path):
    df = pd.read_csv(input_path)
    
    # Column names lo extra spaces unte remove chestundi
    df.columns = df.columns.str.strip()

    # 1. Indian Names (If not already added)
    if 'CustomerName' not in df.columns:
        names = ["Arjun", "Aditi", "Rohan", "Sanya", "Vijay", "Ananya", "Rahul", "Priya", "Amit", "Sneha"]
        df['CustomerName'] = [np.random.choice(names) + f"_{i}" for i in range(len(df))]
    
    # 2. Rename Columns safely (Spending Score handling)
    # Ee list lo unna perlu ekkada unna vatini 'Spending_Score' ga marustundi
    rename_dict = {
        'Spending Score (1-100)': 'Spending_Score',
        'Spending Score': 'Spending_Score'
    }
    df = df.rename(columns=rename_dict)

    # 3. Currency conversion (If not already converted)
    if 'Annual Income (₹ Lakhs)' not in df.columns:
        income_col = 'Annual Income (k$)' if 'Annual Income (k$)' in df.columns else 'Annual Income'
        df['Annual Income (₹ Lakhs)'] = (df[income_col] * 0.83).round(2)
    
    # 4. RFM Features (Screenshot lo unnattu calculation)
    np.random.seed(42)
    if 'Frequency' not in df.columns:
        df['Frequency'] = np.random.randint(1, 50, size=len(df))
    
    # Calculation using the NEW name 'Spending_Score'
    df['Monetary'] = (df['Annual Income (₹ Lakhs)'] * df['Spending_Score'] * 100).round(2)
    
    # Save to data folder
    os.makedirs('data', exist_ok=True)
    output_path = 'data/mall_customers_india.csv'
    df.to_csv(output_path, index=False)
    
    print(f"✅ Data prepared and saved to {output_path}")
    return output_path