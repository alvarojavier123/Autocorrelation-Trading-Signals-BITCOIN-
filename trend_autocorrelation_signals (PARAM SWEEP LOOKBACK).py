import pandas as pd
pd.set_option('display.float_format', lambda x: '%.5f' % x)
import numpy as np
import matplotlib.pyplot as plt
from colorama import init, Fore, Style
init()

import os
import time
import talib as ta
import datetime as dt

pd.set_option("display.max_rows", None)
plt.style.use('seaborn-darkgrid')

# Load data
data = pd.read_csv('BTC_USDT_1d_(2020-2025).csv')
data.index = pd.to_datetime(data['timestamp'])
data = data.drop('timestamp', axis=1)

# Create output folder
output_folder = "long_signal_sweeps"
os.makedirs(output_folder, exist_ok=True)

# Sweep lookback from 5 to 40
lookbacks = list(range(5, 41))
total = len(lookbacks)
start_time = time.time()

for idx, lookback in enumerate(lookbacks, start=1):
    print(Fore.MAGENTA + f"\n===== Processing LOOKBACK = {lookback} days =====" + Style.RESET_ALL)
    loop_start = time.time()

    signals = pd.DataFrame(columns=['BTC', 'Price'], index=data.index)

    for i in data.index:
        if i == dt.datetime(2025, 5, 1):
            break

        if i > data.index[0] + dt.timedelta(days=lookback):
            time_point = i
            print("TIME = ", time_point.strftime('%Y-%m-%d'))

            df = data.loc[i - dt.timedelta(days=lookback):i]

            price_direction = df["close"].iloc[-1] - df["close"].iloc[0]
            print(Fore.YELLOW + "Price Direction = ", str(price_direction) + Style.RESET_ALL)

            df["daily price differences"] = df["close"].diff()
            print(df)

            avg_close = df["close"].mean()
            print("Average Price (close):", avg_close)

            std_dev = df["daily price differences"].std()
            print(Fore.LIGHTYELLOW_EX + "Standard Deviation (price differences):", str(std_dev) + Style.RESET_ALL)

            second_std_dev = 2 * std_dev
            print("2 Standard Deviation (price differences):", second_std_dev)

            best_line = np.polyfit(df["close"][0:-1], df["close"][1:], 1)
            slope = best_line[0]
            print(Fore.CYAN + "Slope:", str(slope) + Style.RESET_ALL)

            if slope > 0.5 and price_direction > second_std_dev:
                signals.loc[time_point, 'BTC'] = 1
                signals.loc[time_point, 'Price'] = df["close"].iloc[-1]
                print(signals.loc[time_point])
                print(Fore.LIGHTGREEN_EX + "LONG SIGNAL" + Style.RESET_ALL)

    # Save to file
    filename = f"long-signals ({lookback} DAYS LOOKBACK).csv"
    filepath = os.path.join(output_folder, filename)
    signals.dropna().to_csv(filepath)

    # Timer and ETA
    loop_end = time.time()
    elapsed_total = loop_end - start_time
    avg_time = elapsed_total / idx
    time_left = avg_time * (total - idx)

    print(Fore.CYAN + f"Finished LOOKBACK = {lookback} in {loop_end - loop_start:.2f} seconds.")
    print(f"Estimated time left: {time_left:.2f} seconds." + Style.RESET_ALL)

print(Fore.GREEN + "\nAll signal files saved successfully in the folder 'long_signal_sweeps'." + Style.RESET_ALL)
