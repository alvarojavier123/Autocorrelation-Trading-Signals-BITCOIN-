# Autocorrelation Trading Signals , Momentum Trading Strategy (BITCOIN)

<h2>Description</h2>
The following logic is under the file trend_autocorrelation.py:
This project iterates over the daily OHLCV of BITCOIN from 2020-01-01 until 2025-05-16 and on each day (or iteration) it takes the last 30 days which would be the lookback period (30 days is arbitary) of closing prices and calculates the correlation coefficient (slope) with numpy function polyfit() and I pass as a parameter the closing prices time series with 1 lag (lagged 1 day) as X and Y to the function. I also calculate the standard deviation of this time series and the second standard deviation. In addition to this I also calculate the price difference which would be the difference between todays's price (the closing price on the iteration) and the closing price 30 days ago. If the correlation coefficient is greater than 0.5 and the price difference is greater than the second standard deviation, I assume the price is trending upwards. I generate a simple trading signal if this criteria happens, I go long If the price difference is positive. This strategy would have performed very well with a compounded return of 480.51% and a maximum drawdown of -25.27 , no slippage cost included.
The corresponding backtest is done in the file BACKTEST.py
<br />

<h2>STRATEGY LOGIC :</h2>

<p align="center">
<br/>
<img src="https://i.imgur.com/UUu8qMz.png"/>
<br />
