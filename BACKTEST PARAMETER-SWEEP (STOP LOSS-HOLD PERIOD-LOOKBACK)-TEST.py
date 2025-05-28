import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt
import time
import os
import re
import concurrent.futures

plt.style.use('seaborn-darkgrid')
pd.set_option("display.max_rows", None)

# Load hourly data
asset_hourly_data = pd.read_csv('BTC_USDT_1h_(2024-2025)-TEST.csv')
asset_hourly_data['timestamp'] = pd.to_datetime(asset_hourly_data['timestamp'])
asset_hourly_data.set_index('timestamp', inplace=True)
asset_hourly_data = asset_hourly_data.drop('volume', axis=1)

def getReturns(position, time, hold, stop_loss):
    try:
        time = dt.datetime.strptime(time, "%Y-%m-%d") + dt.timedelta(hours=23)

        entry_time = time + dt.timedelta(hours=1)
        exit_time = time + dt.timedelta(hours=hold)

        if entry_time not in asset_hourly_data.index or exit_time not in asset_hourly_data.index:
            return np.nan, None, None, None, None, None

        entry_price = asset_hourly_data['open'].loc[entry_time]
        exit_price = asset_hourly_data['close'].loc[exit_time]
        trade = asset_hourly_data.loc[entry_time:exit_time]

        spread = 0.0003
        fee = 0.0005

        if position == -1:
            slippage_cost = entry_price * 0.0005    
            entry_price -= slippage_cost
            entry_price *= (1 - spread)

            stop_loss_price = entry_price * (1 + stop_loss)
            for i in trade.index:
                if trade.loc[i].high >= stop_loss_price:
                    returns = pd.Series([stop_loss_price, entry_price])
                    returns = round(returns.pct_change()[1], 4)  
                    returns -= returns * fee
                    return returns, entry_time, entry_price, i, stop_loss_price, position

            exit_price *= (1 + spread)
            returns = pd.Series([exit_price, entry_price])
            returns = round(returns.pct_change()[1], 4)
            returns -= returns * fee
            return returns, entry_time, entry_price, exit_time, exit_price, position

        elif position == 1:
            slippage_cost = entry_price * 0.0005
            entry_price += slippage_cost
            entry_price *= (1 + spread)

            stop_loss_price = entry_price * (1 - stop_loss)
            for i in trade.index:
                if trade.loc[i].low <= stop_loss_price:
                    returns = pd.Series([entry_price, stop_loss_price])
                    returns = round(returns.pct_change()[1], 4)
                    returns -= returns * fee
                    return returns, entry_time, entry_price, i, stop_loss_price, position

            exit_price *= (1 - spread)
            returns = pd.Series([entry_price, exit_price])
            returns = round(returns.pct_change()[1], 4)
            returns -= returns * fee
            return returns, entry_time, entry_price, exit_time, exit_price, position

    except Exception as e:
        print(f"Error in getReturns: {e} for time: {time}")
        return np.nan, None, None, None, None, None


def run_backtest(signals, hold, stop_loss):
    strategy_returns  = pd.DataFrame(columns=['entry time', 'exit time', 'entry price', 'exit price', 'position', 'returns'])
    exit_time = signals['timestamp'].iloc[0]

    for day in signals.index:
        time_signal = signals['timestamp'].loc[day]
        signal = signals['BTC'].loc[day]

        if pd.to_datetime(time_signal) == dt.datetime(2025, 5, 1):
            break

        if exit_time is None:
            continue

        if pd.to_datetime(time_signal) > dt.datetime(2024, 2 ,1) and pd.to_datetime(time_signal) >= pd.to_datetime(exit_time):
            if signal in [1, -1]:
                returns, entry_time, entry_price, exit_time, exit_price, position = getReturns(signal, time_signal, hold, stop_loss)

                if np.isnan(returns):
                    continue

                strategy_returns.loc[len(strategy_returns)] = {
                    "entry time": entry_time,
                    "exit time": exit_time,
                    "entry price": entry_price,
                    "exit price" : exit_price,
                    "position": position,
                    "returns": returns
                }

    strategy_returns['entry time'] = pd.to_datetime(strategy_returns['entry time'])
    strategy_returns['exit time'] = pd.to_datetime(strategy_returns['exit time'])
    strategy_returns = strategy_returns.sort_values('entry time').reset_index(drop=True)

    compounded_returns = (1 + strategy_returns['returns']).prod() - 1
    simple_returns = strategy_returns['returns'].sum()
    cumulative_compounded = (1 + strategy_returns['returns']).cumprod()

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

    return {
        'strategy_returns': strategy_returns,
        'metrics': {
            'compounded_returns': compounded_returns,
            'simple_returns': simple_returns,
            'max_drawdown': max_drawdown,
            'sharpe_ratio': sharpe_ratio,
            'win_rate': win_rate,
            'profit_factor': profit_factor
        }
    }

# Sweep setup
hold_values = [24, 48, 72, 96, 120, 240, 360, 480, 720]
stop_loss_values = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1]
signal_folder = 'long_signal_sweeps'
signal_files = [f for f in os.listdir(signal_folder) if f.endswith('.csv')]

def extract_lookback(filename):
    match = re.search(r'\((\d+)\sDAYS LOOKBACK\)', filename)
    return int(match.group(1)) if match else None


def run_single_backtest(params):
    file, lookback, hold, stop_loss = params
    signals = pd.read_csv(os.path.join(signal_folder, file))
    backtest_result = run_backtest(signals, hold, stop_loss)
    metrics = backtest_result['metrics']

    return {
        'lookback': lookback,
        'hold': hold,
        'stop_loss': stop_loss,
        'compounded_return': metrics['compounded_returns'],
        'simple_return': metrics['simple_returns'],
        'max_drawdown': metrics['max_drawdown'],
        'sharpe_ratio': metrics['sharpe_ratio'],
        'win_rate': metrics['win_rate'],
        'profit_factor': metrics['profit_factor']
    }


if __name__ == "__main__":
    all_params = []
    for file in signal_files:
        lookback = extract_lookback(file)
        for hold in hold_values:
            for stop_loss in stop_loss_values:
                all_params.append((file, lookback, hold, stop_loss))

    all_results = []
    total_runs = len(all_params)
    start_time = time.time()

    with concurrent.futures.ProcessPoolExecutor() as executor:
        for i, result in enumerate(executor.map(run_single_backtest, all_params), 1):
            all_results.append(result)
            elapsed = time.time() - start_time
            avg_time = elapsed / i
            remaining = avg_time * (total_runs - i)
            print(f"Run {i}/{total_runs} | Lookback: {result['lookback']} | Hold: {result['hold']} | SL: {result['stop_loss']:.2%} | CR: {result['compounded_return']:.2%}")
            print(f"Elapsed: {elapsed:.1f}s | Remaining approx: {remaining:.1f}s\n")

    results_df = pd.DataFrame(all_results)
    results_df = results_df.sort_values(['lookback', 'compounded_return'], ascending=[True, False])
    results_df.to_csv('parameter_sweep (STOP LOSS-HOLD PERIOD-LOOKBACKS)-(2024-2025)-TEST.csv', index=False)


    """
    summary = results_df.groupby('lookback')['compounded_return'].max().reset_index()
    plt.figure(figsize=(10, 5))
    plt.plot(summary['lookback'], summary['compounded_return'], marker='o')
    plt.title("Max Compounded Return per Lookback")
    plt.xlabel("Lookback (days)")
    plt.ylabel("Max Compounded Return")
    plt.grid(True)
    plt.show()
    """

