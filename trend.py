import numpy as np

# For data visualisation
import matplotlib.pyplot as plt
plt.style.use('seaborn-darkgrid')

np.random.seed(1)


ts = [0]
g = 0.4  

for i in range(1,750):
    ts.append(np.random.randn()*0.01 + g*ts[i-1])

print(ts)

# Set figure size
plt.figure(figsize=(15, 7))

# Plotting the time series as a cumulative product
plt.plot((np.cumprod(1+np.array(ts))-1))

# Set the title and labels and their sizes
plt.title('Cumulative Returns', fontsize=16)
plt.xlabel('Day', fontsize=14)
plt.ylabel('Returns', fontsize=14)
plt.show()

plt.figure(figsize=(15, 7))
plt.plot(ts[0:-1],ts[1:],'o')

# Set the title and labels and their sizes
plt.title('SPY Current Vs Past Returns', fontsize=16)
plt.xlabel('Previous Day Returns', fontsize=14)
plt.ylabel('Current Day Returns', fontsize=14)
plt.show()

# Set figure size
plt.figure(figsize=(15, 7))

# Plotting the lagged correlation
plt.plot(ts[0:-1],ts[1:],'o')

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

strategy_returns = np.sign(ts[0:-1])*np.array(ts[1:])

# Set figure size
plt.figure(figsize=(15, 7))

# Plotting the PnL cumulative sum of the returns
plt.plot(np.cumsum(strategy_returns))

# Set the title and labels and their sizes
plt.title('Strategy Returns', fontsize=16)
plt.xlabel('Day', fontsize=14)
plt.ylabel('Returns', fontsize=14)
plt.show()