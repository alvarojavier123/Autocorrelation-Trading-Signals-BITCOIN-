import pandas as pd
pd.set_option('display.float_format', lambda x: '%.5f' % x)
import numpy as np
import matplotlib.pyplot as plt


pd.set_option("display.max_rows", None)

import talib as ta
plt.style.use('seaborn-darkgrid')
import datetime as dt


data = pd.read_csv('BTC_USDT_1d_since_2020.csv')
data.index = pd.to_datetime(data['timestamp'])
#data.index = data.index.tz_localize('UTC').tz_convert('America/Bogota')

data = data.drop('timestamp', axis=1)


signals = pd.DataFrame(columns=['BTC', 'Price'], index=data.index)

for i in data.index:

    if i == dt.datetime(2025,5,10):
        break

    if i > data.index[0] + dt.timedelta(days=30):
        time = i
        print("TIME = ", time.strftime('%Y-%m-%d'))

        print(type(i))


        df = data.loc[i-dt.timedelta(days=30):i]
        print(df)
      
        price_direction = df["close"][-1] - df["close"][0]
        print("Price Direction = ", price_direction)

        avg_close = df["close"].mean()
        print("Average Price (close):", avg_close)

        std_dev = df["close"].std()
        print("Standard Deviation (close ):", std_dev)

        second_std_dev = 2 * std_dev
        print("2 Standard Deviation (close ):", second_std_dev)
        print("- 2 Standard Deviation (close ):", -second_std_dev)

        # Set figure size
        #plt.figure(figsize=(15, 7))

        # Plotting the lagged correlation
        #plt.plot(df["close"][0:-1],df["close"][1:],'o')

        m = np.polyfit(df["close"][0:-1],df["close"][1:], 1)
        print(m)
  

        if m[0] > 0.5 and price_direction > second_std_dev:
            print(m[0])
            signals.loc[time, 'BTC'] = 1
            signals.loc[time, 'Price'] = df["close"].iloc[-1]
            print(signals.loc[time])

            """
            res = input("Continue ?")
            if res == "":
                continue
            """
        
        """
        if m[0] > 0.5 and price_direction < -second_std_dev:
            print(m[0])
            signals.loc[time, 'BTC'] = -1
            signals.loc[time, 'Price'] = df["close"].iloc[-1]
            print(signals.loc[time])

            
            res = input("Continue ?")
            if res == "":
                continue
            
        """
            
            
         

        """
        # Linearly fitting the lagged correlation data
        m = np.polyfit(ts[0:-1],ts[1:],1)

        # Creating x-values for the fit
        xx = ts[0:-1]

        # Calculating the y-values from the x-values
        # and the fitting parameters m
        yy = np.polyval(m,xx)

        # Plotting the regression line
        plt.plot(xx,yy)

        # Set the title and labels and their sizes
        plt.title('SPY Current Vs Past Returns', fontsize=16)
        plt.xlabel('Previous Day Returns', fontsize=14)
        plt.ylabel('Current Day Returns', fontsize=14)
        plt.show()
        """

signals.to_csv(f'long-signals.csv')
        
        