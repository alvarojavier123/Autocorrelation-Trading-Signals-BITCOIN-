# Autocorrelation Trading Signals (Long Only) - Momentum Trading Strategy (BITCOIN)

<h2>Description</h2>
<br />
The following logic is under the file trend_autocorrelation_signals (30 DAYS LOOKBACK) :
<br />
This project iterates over the daily OHLCV of BITCOIN from 2020-01-01 until 2025-05-16 and on each day (or iteration) it takes the last 30 days which would be the lookback period (30 days is arbitary) of closing prices and calculates the slope with numpy function polyfit() and I pass as a parameter the closing prices time series with 1 lag (lagged 1 day) as X and Y to the function. I also calculate the standard deviation of the daily differences of the closing prices and the second standard deviation. In addition to this I also calculate the price difference which would be the difference between todays's price (the closing price on the iteration) and the closing price 30 days ago. If the slope is greater than 0.5 and the price difference is greater than the second standard deviation, I assume the price is trending upwards. I generate a simple trading signal if this criteria happens, I go long If the price difference is positive. After this, I save the signals in the file long-signals (30 DAYS LOOKBACK).csv as a standard file with the signals for the main parameter set which is (30 days lookback). 
I also run a parameter sweep on the file trend_autocorrelation_signals (PARAM SWEEP LOOKBACK).py to try different lookback periods: from 5 days lookback until 40 days lookback and then I save them under the file long_signal_sweeps.
The files BACKTEST (STOP LOSS-HOLD PERIOD)-TEST.py and BACKTEST (STOP LOSS-HOLD PERIOD)-TRAIN.py are to manually backtest the parameters, the train dataset is from 2020-2024 and the test dataset is from 2024-2025. the files BACKTEST PARAMETER-SWEEP (STOP LOSS-HOLD PERIOD-LOOKBACK)-TEST.py and BACKTEST PARAMETER-SWEEP (STOP LOSS-HOLD PERIOD-LOOKBACK)-TRAIN.py perform backtest with many parameter configurations (lookbacks-holding periods-stop losses) and then they save the results with metrics (compounded returns, simple returns, drawdowns, sharpe ratio, profit factor, win ratio) in the files parameter_sweep (STOP LOSS-HOLD PERIOD-LOOKBACKS)-(2020-2024)-TRAIN.csv and parameter_sweep (STOP LOSS-HOLD PERIOD-LOOKBACKS)-(2020-2024)-TEST.csv respectively. In the BEST_PARAMETER.py file I imported the in-sample results from 2020-2024 and used the K-Means clustering to find the cluster with the highest average sharpe ratio, then i just grabbed the sample or strategy with the highest sharpe ratio, which would have performed pretty well in the in-sample period and also in the out-of-sample period 2024-2025, but it could be an outliar.

Also, different lookback periods could be used on trend_autocorrelation_signals.py where the trading signals are calculated.
<br />

<h2>STRATEGY LOGIC :</h2>

<p align="center">
<br/>
<img src="https://i.imgur.com/noh7GP7.png"/>
<br />

<h2>RESULTS WITH BEST POSSIBLE PARAMETERS (LOOKBACK: 29 DAYS, HOLD: 4 DAYS, STOP LOSS: 10%) IN SAMPLE PERIOD 2020-2024 </h2>
<p align="center">
<br/>
<img src="https://i.imgur.com/85h4dv0.png"/>
<br />

<h2>RESULTS WITH BEST POSSIBLE PARAMETERS (LOOKBACK: 29 DAYS, HOLD: 4 DAYS, STOP LOSS: 10%) OUT OF SAMPLE PERIOD 2024-2025</h2>
<p align="center">
<br/>
<img src="https://i.imgur.com/2aJJM1z.png"/>
<br />
