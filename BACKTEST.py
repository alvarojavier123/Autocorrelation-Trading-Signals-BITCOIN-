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
                slippage_cost = entry_price * 0.0005    
                entry_price = entry_price - slippage_cost

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
                slippage_cost = entry_price * 0.0005
                entry_price = entry_price + slippage_cost

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

hold = 480 # HOLDING PERIOD IN HOURS
stop_loss = 0.08 # STOP LOSS
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

import plotly.graph_objects as go


strategy_returns['cumsum returns'] = strategy_returns['returns'].cumsum()
strategy_returns['cumulative returns'] = (1 + strategy_returns['returns']).cumprod()
print(strategy_returns)

strategy_returns['entry time'] = pd.to_datetime(strategy_returns['entry time'])
strategy_returns['exit time'] = pd.to_datetime(strategy_returns['exit time'])
strategy_returns = strategy_returns.sort_values('entry time').reset_index(drop=True)

compounded_returns = (1 + strategy_returns['returns']).prod() - 1
simple_returns = strategy_returns['returns'].sum()
cumulative_compounded = (1 + strategy_returns['returns']).cumprod()
cumulative_simple = strategy_returns['returns'].cumsum()

running_max = cumulative_compounded.cummax()
drawdown = (cumulative_compounded - running_max) / running_max
max_drawdown = drawdown.min()

avg_trade_days = (strategy_returns['exit time'] - strategy_returns['entry time']).dt.days.mean()
avg_trade_days = avg_trade_days if avg_trade_days > 0 else 1
daily_returns = strategy_returns['returns'] / avg_trade_days
annualized_return = (1 + compounded_returns) ** (252 / (avg_trade_days * len(strategy_returns))) - 1
annualized_volatility = daily_returns.std() * np.sqrt(252)
sharpe_ratio = annualized_return / annualized_volatility if annualized_volatility != 0 else np.nan

win_rate = (strategy_returns['returns'] > 0).mean()
gross_profit = strategy_returns.loc[strategy_returns['returns'] > 0, 'returns'].sum()
gross_loss = abs(strategy_returns.loc[strategy_returns['returns'] <= 0, 'returns'].sum())
profit_factor = gross_profit / gross_loss if gross_loss != 0 else np.nan

# --- Crear figura interactiva ---

fig = go.Figure()

# Línea de Retornos Compuestos
fig.add_trace(go.Scatter(
    x=strategy_returns['exit time'],
    y=cumulative_compounded,
    mode='lines',
    name='Compounded Returns ($)',
    line=dict(color='blue')
))

# Línea de Retornos Simples acumulados
fig.add_trace(go.Scatter(
    x=strategy_returns['exit time'],
    y=cumulative_simple,
    mode='lines',
    name='Simple Returns (Cumsum)',
    line=dict(color='green', dash='dash')
))

# Área de Drawdown
fig.add_trace(go.Scatter(
    x=strategy_returns['exit time'],
    y=drawdown,
    mode='lines',
    fill='tozeroy',
    name='Drawdown',
    line=dict(color='red'),
    fillcolor='rgba(255, 0, 0, 0.3)',
    yaxis='y2'
))

# Layout con doble eje Y
fig.update_layout(
    title=f"Strategy Performance from {strategy_returns['entry time'].min().date()} to {strategy_returns['exit time'].max().date()}",
    xaxis_title='Date',
    yaxis=dict(
        title='Returns',
        side='left'
    ),
    yaxis2=dict(
        title='Drawdown',
        overlaying='y',
        side='right',
        showgrid=False,
        tickformat=".0%",
        range=[min(drawdown)*1.1, 0]
    ),
    legend=dict(x=0.01, y=0.99),
    hovermode='x unified',
    margin=dict(l=60, r=60, t=60, b=60),
    height=600
)

# Añadir cuadro con métricas como anotación en la gráfica
metrics_text = (
    f"Compounded Returns: {compounded_returns:.2%}\n"
    f"Simple Returns: {simple_returns:.2%}\n"
    f"Max Drawdown: {max_drawdown:.2%}\n"
    f"Sharpe Ratio: {sharpe_ratio:.2f}\n"
    f"Win Rate: {win_rate:.2%}\n"
    f"Profit Factor: {profit_factor:.2f}"
)

fig.add_annotation(
    xref='paper', yref='paper',
    x=0.5, y=0.98,  # Top center
    xanchor='center',
    showarrow=False,
    align='left',
    bgcolor='white',
    bordercolor='black',
    borderwidth=1,
    borderpad=4,
    text=metrics_text.replace('\n', '<br>'),  # Use <br> for line breaks in HTML
    font=dict(size=12, color='black', family='Arial Black')  # Strong black font
)



import plotly.io as pio
pio.renderers.default = "browser"



fig.show()

print("====== Strategy Performance Metrics ======")
print(metrics_text)
print("==========================================")
