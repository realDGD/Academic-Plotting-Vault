import pandas as pd
import numpy as np
import os

np.random.seed(32)

sources = []
targets = []
values = []

for c in 'ABCDEFGH':
    for i in range(1, 6):
        sources.append(f"{c.lower()}{i}")
        targets.append(c)
        values.append(np.random.rand() * 10)

# 6 extra random links
for _ in range(6):
    sources.append(f"{chr(ord('a') + np.random.randint(0, 8))}{np.random.randint(1, 6)}")
    targets.append(chr(ord('A') + np.random.randint(0, 8)))
    values.append(np.random.rand() * 10)

# We do NOT remove the first row anymore, since my python logic didn't have the empty row!

df_sankey = pd.DataFrame({'source': sources, 'target': targets, 'value': values})
os.makedirs('Python', exist_ok=True)
df_sankey.to_csv('Python/data_sankey.csv', index=False)

targets_unique = list('ABCDEFGH')
n_log_pvalue = np.linspace(2, -0.3, 8)
count = np.random.randint(1, 9, size=8)
hit_ratio = 0.1 + 0.4 * np.random.rand(8)

df_bubble = pd.DataFrame({
    'target': targets_unique,
    'NLogPvalue': n_log_pvalue,
    'Count': count,
    'HitRatio': hit_ratio
})
df_bubble.to_csv('Python/data_bubble.csv', index=False)
print("Data generated")
