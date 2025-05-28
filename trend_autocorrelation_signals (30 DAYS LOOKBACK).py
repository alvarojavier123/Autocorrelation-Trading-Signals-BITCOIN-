import pandas as pd
pd.set_option('display.float_format', lambda x: '%.5f' % x)
import numpy as np
import matplotlib.pyplot as plt
from colorama import init, Fore, Style
init()

pd.set_option("display.max_rows", None)

import talib as ta
plt.style.use('seaborn-darkgrid')
import datetime as dt


data = pd.read_csv('BTC_USDT_1d_(2020-2025).csv')
data.index = pd.to_datetime(data['timestamp'])
data = data.drop('timestamp', axis=1)


signals = pd.DataFrame(columns=['BTC', 'Price'], index=data.index)
lookback = 30

for i in data.index:

    if i == dt.datetime(2025,5,1): # MAKE SURE STOP ITERATING SPECIFIC DATE.
        break

    if i > data.index[0] + dt.timedelta(days=lookback):
        time = i
        print("TIME = ", time.strftime('%Y-%m-%d'))

        df = data.loc[i-dt.timedelta(days=30):i] # TAKES LAST 30 DAYS

        price_direction = df["close"].iloc[-1] - df["close"].iloc[0] # CALCULATES PRICE DIFFERENT WITH THE PRICE 30 DAYS AGO.
        print(Fore.YELLOW  +  "Price Direction = ", str(price_direction) + Style.RESET_ALL) 
        df["daily price differences"] = df["close"].diff() # CALCULATES THE DAILY PRICE DIFFERENCE OVER THE PAST 30 DAYS AND STORES IN A NEW COLUMN.
        print(df)

        avg_close = df["close"].mean()
        print("Average Price (close):", avg_close) # CALULATE SIMPLE MEAN, NOTHING IS DONE WITH IT...

        std_dev = df["daily price differences"].std() # CALCULATE STANDARD DEVIATION TO MEASURE VOLATILITY OF THE PRICE DIFFERENCES OVER THE PAST 30 DAYS.
        print(Fore.LIGHTYELLOW_EX  +  "Standard Deviation (price differences):", str(std_dev) + Style.RESET_ALL)
        
        second_std_dev = 2 * std_dev # JUST MULTIPLY THE STANDARD DEVIATION TIMES 2.
        print("2 Standard Deviation (price differences):", second_std_dev)

        best_line = np.polyfit(df["close"][0:-1],df["close"][1:], 1) # PERFORMS LINEAR REGRESSION TO THE DATA : X (YESTERDAY PRICES) , Y (TODAY'S PRICES)
        slope = best_line[0] # THE SLOPE OF THE LINE.
        print(Fore.CYAN  +  "Slope:", str(slope) + Style.RESET_ALL)

        if slope > 0.5 and price_direction > second_std_dev:
            signals.loc[time, 'BTC'] = 1
            signals.loc[time, 'Price'] = df["close"].iloc[-1]
            print(signals.loc[time])
            print(Fore.LIGHTGREEN_EX  +  "LONG SIGNAL" +  Style.RESET_ALL)
        
        """
        res = input("Continue ?")
        if res == "":
                continue
        """
        
        
        

signals.to_csv(f'long-signals (30 DAYS LOOKBACK).csv')