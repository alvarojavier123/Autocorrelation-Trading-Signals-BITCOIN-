# For data manipulation
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('seaborn-darkgrid')


np.random.seed(1)
returns = np.random.randn(200000)*0.01
print(returns)
print(len(returns))
price_series = np.cumprod(1+returns)*100
print(price_series)
print(len(price_series))

# Set figure size
plt.figure(figsize=(15, 7))
plt.plot(price_series[-750:])

# Set the title and labels
plt.title('Price Series', fontsize=16)
plt.xlabel('Day', fontsize=15)
plt.ylabel('Price', fontsize=15)
plt.tick_params(axis='both', labelsize=15)
plt.show()

recent_returns = returns[-750:]
plt.figure(figsize=(15, 7))

# Plot the correlation between today's and yesterday's returns
plt.plot(returns[0:-1], returns[1:], 'o')

# Set the title and labels and their sizes
plt.title('Current Returns vs Lagged Returns', fontsize=16)
plt.axis('equal')
plt.xlabel('Current Returns', fontsize=15)
plt.ylabel('Lag 1 Returns', fontsize=15)
plt.show()

def MA(ps, p):


    return [np.mean(ps[i-p:i]) for i in range(p, len(ps))]


recent_prices = price_series[-750:]

plt.figure(figsize=(15, 7))

# Plotting the prices and moving averages
plt.plot(recent_prices[50:])
plt.plot(MA(recent_prices, 20), label='20 SMA (fast)')
plt.plot(MA(recent_prices, 50), label='50 SMA (slow)')

# Set the title and labels
plt.title('50 and 20 Moving Averages', fontsize=16)
plt.xlabel('Day', fontsize=15)
plt.ylabel('Price', fontsize=15)
plt.legend()
plt.show()