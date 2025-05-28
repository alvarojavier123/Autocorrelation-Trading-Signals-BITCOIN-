import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('seaborn-darkgrid')
pd.set_option("display.max_rows", None)
import talib as ta
import datetime as dt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

backtests = pd.read_csv('parameter_sweep (STOP LOSS-HOLD PERIOD-LOOKBACKS)-(2020-2024)-TRAIN.csv')
print("TOTAL STRATEGIES = ", len(backtests))

features = backtests[['sharpe_ratio', 'max_drawdown', 'compounded_return']]

# Standardize features for KMeans
scaler = StandardScaler()
scaled_features = scaler.fit_transform(features)

# Try 5 clusters instead of 3
kmeans = KMeans(n_clusters=5, random_state=42)
clusters = kmeans.fit_predict(features)

# Assign new clusters to DataFrame
backtests['cluster'] = clusters

# Find cluster with highest mean Sharpe
cluster_means = backtests.groupby('cluster')['sharpe_ratio'].mean()
best_cluster_label = cluster_means.idxmax()
best_cluster_df = backtests[backtests['cluster'] == best_cluster_label]
print(best_cluster_df)


positive_performance = (best_cluster_df['compounded_return'] > 0).sum()
negative_performance = (best_cluster_df['compounded_return'] < 0).sum()
total = len(best_cluster_df)

print(f"Positive: {positive_performance} ({100 * positive_performance / total:.2f}%)")
print(f"Negative: {negative_performance} ({100 * negative_performance / total:.2f}%)")
print("# STARTEGIES IN THE CLUSTER: ", total)
print("📈 MEAN SHARPE RATIO CLUSTER:", round(best_cluster_df['sharpe_ratio'].mean(), 4))
print("📉 STANDARD DEVIATION SHARPE RATIO CLUSTER:", round(best_cluster_df['sharpe_ratio'].std(), 4))
print("🏅 BEST SHARPE RATIO CLUSTER:", round(best_cluster_df['sharpe_ratio'].max(), 4))

best_row = best_cluster_df.loc[best_cluster_df['sharpe_ratio'].idxmax()]
print("\n🏆 Best Performer in Best Cluster:\n")
print(best_row)


mean = best_cluster_df['compounded_return'].mean()
print(mean)
std = best_cluster_df['compounded_return'].std()
print(std)
z_score = (best_row['compounded_return'] - mean) / std
print("Z SCORE = ", z_score)

top_5 = best_cluster_df.sort_values(by='sharpe_ratio', ascending=False).head(5)
print(top_5)