import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('seaborn-darkgrid')
pd.set_option("display.max_rows", None)
import talib as ta
import datetime as dt

# Cargar el DataFrame
in_sample_backtests = pd.read_csv('parameter_sweep (STOP LOSS-HOLD PERIOD-LOOKBACKS)-(2020-2024)-TRAIN.csv')
print(in_sample_backtests)

# Estadísticas generales
positive_performance = (in_sample_backtests['compounded_return'] > 0).sum()
negative_performance = (in_sample_backtests['compounded_return'] < 0).sum()
mean_return = in_sample_backtests['compounded_return'].mean()
std_return = in_sample_backtests['compounded_return'].std()
total = len(in_sample_backtests)

print(f"Positive: {positive_performance} ({100 * positive_performance / total:.2f}%)")
print(f"Negative: {negative_performance} ({100 * negative_performance / total:.2f}%)")
print(f"Total:    {total}")
print(f"Mean Return: {mean_return}")
print(f"Standard Deviation Return: {std_return}")

import numpy as np

# Extract Sharpe ratios
sharpe_ratios = in_sample_backtests['sharpe_ratio']

# Histogram of Sharpe ratios (same bins as in your plot)
counts, bins = np.histogram(sharpe_ratios, bins=50)

# Find the bin with the most strategies
max_count_index = np.argmax(counts)
bin_start = bins[max_count_index]
bin_end = bins[max_count_index + 1]

print(f"Most populated Sharpe bin: {bin_start:.4f} to {bin_end:.4f} with {counts[max_count_index]} strategies")

# Filter strategies within this bin
dense_sharpe_cluster = in_sample_backtests[
    (sharpe_ratios >= bin_start) & (sharpe_ratios < bin_end)
]

# Preview
print("\nSample of strategies from the most populated Sharpe bin:")
print(dense_sharpe_cluster.head())

# Sort by compounded return (optional)
top_by_return = dense_sharpe_cluster.sort_values(by='compounded_return', ascending=False).head(10)
print("\nTop 5 strategies (by return) within the stable Sharpe cluster:")
print(top_by_return[['lookback', 'hold', 'stop_loss', 'compounded_return', 'sharpe_ratio']])



fig, axs = plt.subplots(2, 1, figsize=(10, 10), sharex=False)

# --- Subplot 1: Compounded Return ---
axs[0].hist(in_sample_backtests['compounded_return'], bins=50, color='skyblue', edgecolor='black')

mean_cr = in_sample_backtests['compounded_return'].mean()
std_cr = in_sample_backtests['compounded_return'].std()

axs[0].scatter(mean_cr, 0, color='black', s=100, label='Mean')
axs[0].scatter([mean_cr - std_cr, mean_cr + std_cr], [0, 0], color='orange', s=100, label='±1 Std Dev')

axs[0].axvline(mean_cr, color='black', linestyle='--', linewidth=1.5, label=f'Mean = {mean_cr:.2f}')
axs[0].axvline(mean_cr - std_cr, color='orange', linestyle='--', linewidth=1.2, label=f'-1 Std = {mean_cr - std_cr:.2f}')
axs[0].axvline(mean_cr + std_cr, color='orange', linestyle='--', linewidth=1.2, label=f'+1 Std = {mean_cr + std_cr:.2f}')

axs[0].set_title('Distribution of Compounded Returns\nwith Mean ± Std Dev', fontsize=13)
axs[0].set_xlabel('Compounded Return')
axs[0].set_ylabel('Data Points')
axs[0].legend()
axs[0].grid(True)

# --- Subplot 2: Sharpe Ratio ---
axs[1].hist(in_sample_backtests['sharpe_ratio'], bins=50, color='lightgreen', edgecolor='black')

mean_sr = in_sample_backtests['sharpe_ratio'].mean()
std_sr = in_sample_backtests['sharpe_ratio'].std()

axs[1].scatter(mean_sr, 0, color='black', s=100, label='Mean')
axs[1].scatter([mean_sr - std_sr, mean_sr + std_sr], [0, 0], color='orange', s=100, label='±1 Std Dev')

axs[1].axvline(mean_sr, color='black', linestyle='--', linewidth=1.5, label=f'Mean = {mean_sr:.2f}')
axs[1].axvline(mean_sr - std_sr, color='orange', linestyle='--', linewidth=1.2, label=f'-1 Std = {mean_sr - std_sr:.2f}')
axs[1].axvline(mean_sr + std_sr, color='orange', linestyle='--', linewidth=1.2, label=f'+1 Std = {mean_sr + std_sr:.2f}')

axs[1].set_title('Distribution of Sharpe Ratios\nwith Mean ± Std Dev', fontsize=13)
axs[1].set_xlabel('Sharpe Ratio')
axs[1].set_ylabel('Data Points')
axs[1].legend()
axs[1].grid(True)

plt.tight_layout(pad=2.0)
plt.show()


