import numpy as np
import yfinance as yf
from scipy.stats import norm
import pandas as pd
import datetime

def download_data(stock, start, end):
    data = {}
    ticker = yf.download(stock, start, end)
    data[stock] = ticker['Close']
    # return pd.DataFrame(data)
    return pd.concat(data, axis=1)

# how to calculate the VaR for tomorrow (n = 1)
def calculate_var(position, c, mu, sigma):
    # v = norm.ppf(1 - c)
    var = position * (mu - sigma * norm.ppf(1 - c))
    return var

# how to calculate the VaR for any day(s) in the future
def calculate_var_n(position, c, mu, sigma, n):
    # v = norm.ppf(1 - c)
    var = position * (mu * n - sigma * np.sqrt(n) * norm.ppf(1 - c))
    return var

if __name__ == '__main__':
    start = datetime.datetime(2014, 1, 1)
    end = datetime.datetime(2018, 12, 31)
    stock_data = download_data('AAPL', start, end)

    stock_data['returns'] = np.log(stock_data['AAPL'] / stock_data['AAPL'].shift(1))
    stock_data = stock_data[1:]
    print(stock_data)

    # this is the investment (stocks, etc.)
    S = 1e6
    # this is the confidence level
    c = 0.99

    # we assume that daily returns are normally distributed
    mu = np.mean(stock_data['returns'])
    sigma = np.std(stock_data['returns'])
    print('Value at risk is: $%0.2f' % calculate_var_n(S, c, mu, sigma, 10))

    print(stock_data)
