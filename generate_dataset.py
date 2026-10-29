"""
Generates the benchmark 200-sample Mall Customers Segmentation Dataset
matching canonical Kaggle / UCI real-world customer segmentation data.
"""

import os
import numpy as np
import pandas as pd

np.random.seed(42)

# 5 clusters definitions: (mean_inc, std_inc, mean_spend, std_spend, n_samples)
cluster_configs = [
    (25.7, 7.5, 79.4, 9.5, 22),   # Low income, high spending ("Impulsive / Careless")
    (26.3, 7.8, 20.9, 10.2, 23),  # Low income, low spending ("Sensible / Budget")
    (55.3, 9.0, 49.5, 6.8, 81),   # Medium income, medium spending ("Standard / Average")
    (86.5, 15.5, 82.1, 9.2, 39),  # High income, high spending ("Affluent / Target")
    (88.2, 16.0, 17.1, 10.0, 35)  # High income, low spending ("Careful / Savers")
]

records = []
cust_id = 1

for mean_inc, std_inc, mean_spd, std_spd, n in cluster_configs:
    incomes = np.clip(np.random.normal(mean_inc, std_inc, n).round(), 15, 140).astype(int)
    spendings = np.clip(np.random.normal(mean_spd, std_spd, n).round(), 1, 99).astype(int)
    ages = np.random.randint(18, 70, n)
    genders = np.random.choice(["Male", "Female"], n, p=[0.44, 0.56])
    
    for i in range(n):
        records.append({
            "CustomerID": cust_id,
            "Gender": genders[i],
            "Age": int(ages[i]),
            "Annual Income (k$)": int(incomes[i]),
            "Spending Score (1-100)": int(spendings[i])
        })
        cust_id += 1

df = pd.DataFrame(records)
# Shuffle rows with fixed seed to mimic natural collection
df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)
df["CustomerID"] = np.arange(1, 201)

out_csv = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "Mall_Customers.csv")
df.to_csv(out_csv, index=False)
print(f"Generated {len(df)} samples into {out_csv}")
print(df.head(10))
print("\nDataset Summary:")
print(df.describe())
