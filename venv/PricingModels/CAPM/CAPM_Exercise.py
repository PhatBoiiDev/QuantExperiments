import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from scipy.stats import norm

def download_data(stock, start_date, end_date):
    data = {}
    ticker = yf.download(stock, start_date, end_date)
    data['Price'] = ticker['Close']
    return pd.concat(data, axis=1)

def calculate_returns(stock_data):
    stock_data['Price'] = np.log(stock_data['Close'] / stock_data['Close'].shift(1))
    return stock_data[1:]

def show_data(stock_data):
    plt.hist(stock_data, bins=700)
    stock_variance = stock_data.var()
    stock_mean = stock_data.mean()
    sigma = np.sqrt(stock_variance)
    x = np.linspace(stock_mean - 3 * sigma, stock_mean + 3 * sigma, 100)
    plt.plot(x, norm.pdf(x, stock_mean, sigma))
    plt.show()

if __name__ == '__main__':
        stock_data = download_data('IBM', '2010-01-01', '2025-01-01')
        show_data(stock_data)

