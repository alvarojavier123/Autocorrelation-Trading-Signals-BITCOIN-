import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('seaborn-darkgrid')
pd.set_option("display.max_rows", None)
import talib as ta
import datetime as dt

signals = pd.read_csv('long-signals.csv')


def getReturns(position, time, hold, stop_loss):
    print('TIME = ', time)
    asset_hourly_data = pd.read_csv(f'BTC_USDT_1h_since_2020.csv')
    asset_hourly_data['timestamp'] = pd.to_datetime(asset_hourly_data['timestamp'])
    asset_hourly_data.set_index('timestamp', inplace=True)
    asset_hourly_data = asset_hourly_data.drop('volume', axis=1)
    #print(asset_hourly_data)
    
    time = dt.datetime.strptime(time, "%Y-%m-%d")
    print('TIME = ', time)
    time = time + dt.timedelta(hours=23)
    print('TIME = ', time)
    entry_time = asset_hourly_data.loc[time + dt.timedelta(hours=1)].name
    print("Entry Time = ", entry_time)
    entry_price = asset_hourly_data['open'].loc[entry_time]
    print("Entry Price = ", entry_price)

    exit_time = asset_hourly_data.loc[time + dt.timedelta(hours=hold)].name
    print("Exit Time = ", exit_time)
    exit_price = asset_hourly_data['close'].loc[exit_time]
    print("Exit Price = ", exit_price)

    row = asset_hourly_data.loc[time]
    #print(row)

    print('POSITION TO OPEN = ', position)

    trade = asset_hourly_data.loc[entry_time:exit_time]
    print(trade)

    
    if position == -1:

                stop_loss = entry_price*(1+stop_loss)
                for i in trade.index:
                    if trade.loc[i].open >=stop_loss or trade.loc[i].high >=stop_loss or trade.loc[i].low >=stop_loss or trade.loc[i].close >=stop_loss:
            
                        returns = pd.Series([stop_loss, entry_price])
                        returns = round(returns.pct_change()[1], 4)  
                        returns = returns - (returns * 0.0005)
                        return returns, entry_time, entry_price, i, stop_loss, signal
                    
                
                returns = pd.Series([exit_price, entry_price])
                returns = round(returns.pct_change()[1], 4)
                returns = returns - (returns * 0.0005)
                     
                return returns, entry_time, entry_price, exit_time, exit_price, signal
            
    elif position == 1:

                stop_loss = entry_price*(1-stop_loss)
                for i in trade.index:
                    if trade.loc[i].open <=stop_loss or trade.loc[i].high <=stop_loss or trade.loc[i].low <=stop_loss or trade.loc[i].close <=stop_loss:
                        returns = pd.Series([entry_price, stop_loss])
                        returns = round(returns.pct_change()[1], 4)
                        returns = returns - (returns * 0.0005)
                        return returns, entry_time, entry_price, i, stop_loss, signal
                    
                returns = pd.Series([entry_price, exit_price])
                returns = round(returns.pct_change()[1], 4)
                returns = returns - (returns * 0.0005)
            
                return returns, entry_time, entry_price, exit_time, exit_price, signal


    



strategy_returns  = pd.DataFrame(columns=['entry time', 'exit time', 'entry price', 'exit price', 'position', 'returns'])
exit_time = signals['timestamp'].loc[0]

hold = 240
stop_loss = 0.01
print("exit time initial = ", exit_time)

for day in signals.index:
    time = signals['timestamp'].loc[day]
    print("Time = ", time)
    signal = signals['BTC'].loc[day]
    print("Signal = ", signal)
    price = signals['Price'].loc[day]
    print("Price at the time = ", price)

    if pd.to_datetime(time) == dt.datetime(2025, 5 ,1):
          break

    if pd.to_datetime(time) > dt.datetime(2020, 1 ,29) and pd.to_datetime(time) >= pd.to_datetime(exit_time):

        if signal == 1:
            returns, entry_time, entry_price, exit_time, exit_price, signal = getReturns(signal, time, hold, stop_loss)
        
            print("EXIT TIME = ", exit_time)
            print("RETURNS = ", returns)
            strategy_returns.loc[len(strategy_returns)] = {
                "entry time": entry_time,
                "exit time": exit_time,
                "entry price": entry_price,
                "exit price" : exit_price,
                "position": signal,
                "returns": returns
            }
        
        if signal == -1:
            returns, entry_time, entry_price, exit_time, exit_price, signal = getReturns(signal, time, hold, stop_loss)
        
            print("EXIT TIME = ", exit_time)
            print("RETURNS = ", returns)
            strategy_returns.loc[len(strategy_returns)] = {
                "entry time": entry_time,
                "exit time": exit_time,
                "entry price": entry_price,
                "exit price" : exit_price,
                "position": signal,
                "returns": returns
            }

        """
        print(strategy_returns)
        res = input("Continue ?")
        if res == "":
                print(res)
        """
    print("-------------------------------------------------------------------")


strategy_returns = strategy_returns.dropna()
strategy_returns['cumsum returns'] = strategy_returns['returns'].cumsum()
strategy_returns['cumulative returns'] = (1 + strategy_returns['returns']).cumprod()
print(strategy_returns)

compound_returns = (strategy_returns['returns']+1).cumprod()
#print('compound returns = ', compound_returns)
total_returns = (compound_returns.iloc[-1]-1)*100
print('The total returns from strategy {:,.2f}% '.format(total_returns))
print('Max returns =', compound_returns.max())

running_max = np.maximum.accumulate(compound_returns).dropna()
running_max[running_max < 1] = 1
drawdown = (compound_returns)/running_max - 1
max_dd = drawdown.min()*100
print('The maximum drawdown is %.2f' % max_dd)

# Plot the cumulative strategy returns
#daily_returns['returns'].cumsum().plot(figsize=(10, 7))
(strategy_returns['returns']+1).cumprod().plot(figsize=(10, 7))
plt.xlabel('Date')
plt.ylabel('Strategy Returns (%)')
plt.show()

strategy_returns['returns'].cumsum().plot(figsize=(10, 7))
plt.xlabel('Date')
plt.ylabel('Strategy Returns (%)')
plt.show()
  

