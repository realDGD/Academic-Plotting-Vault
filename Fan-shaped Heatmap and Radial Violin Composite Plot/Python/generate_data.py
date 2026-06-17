import numpy as np
import pandas as pd
import os

np.random.seed(4)
Data = np.random.rand(7, 12) + 1 + np.sin(np.linspace(0, 2*np.pi, 12) - np.pi/1.2) + (np.arange(1, 8).reshape(-1, 1)) / 12
Data = Data / np.max(Data)

VData = np.mean(Data, axis=0) + np.random.randn(50, 12) * 0.6

combined = np.vstack([Data, VData])
df = pd.DataFrame(combined, columns=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
df.to_csv('/Users/dgd/Files/Code/Python/Academic-Plotting-Vault-Private/Fan-shaped Heatmap and Radial Violin Composite Plot/Python/data.csv', index=False)
print("Data generated and saved to data.csv")
