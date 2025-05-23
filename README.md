# Autocorrelation Trading Signals (Long Only) - Momentum Trading Strategy (BITCOIN)

<h2>Description</h2>
<br />
The following logic is under the file trend_autocorrelation.py :
<br />
This project iterates over the daily OHLCV of BITCOIN from 2020-01-01 until 2025-05-16 and on each day (or iteration) it takes the last 30 days which would be the lookback period (30 days is arbitary) of closing prices and calculates the slope with numpy function polyfit() and I pass as a parameter the closing prices time series with 1 lag (lagged 1 day) as X and Y to the function. I also calculate the standard deviation of the daily differences of the closing prices and the second standard deviation. In addition to this I also calculate the price difference which would be the difference between todays's price (the closing price on the iteration) and the closing price 30 days ago. If the slope is greater than 0.5 and the price difference is greater than the second standard deviation, I assume the price is trending upwards. I generate a simple trading signal if this criteria happens, I go long If the price difference is positive. 
On the BACKTEST.py I backtested the strategy, I hardcoded a stop loss at 1% losses per trade and also a holding period of 10 days (240 hours). at the end the metrics are printed.
If you run BACKTEST.py you will see the results at the end in an interactive graph that will show you the details. The long-signals.csv contain the signals with the fixed parameters.
<br />

<h2>STRATEGY LOGIC :</h2>

<p align="center">
<br/>
<img src="https://i.imgur.com/noh7GP7.png"/>
<br />

<h2>RESULTS WITH FIXED PARAMETERS (1%:STOP LOSS - HOLDING PERIOD:10 DAYS - LOOKBACK:30 DAYS) </h2>
<p align="center">
<br/>
<img src="https://i.imgur.com/mmP2xx8.png"/>
<br />
