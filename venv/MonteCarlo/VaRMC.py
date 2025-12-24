import numpy as np
import yfinance as yf
import datetime
import pandas as pd

def download_data(stock, start, end):
    data = {}
    ticker = yf.download(stock, start=start, end=end)
    data['Close'] = ticker['Close']
    return pd.concat(data, axis=1)

class VaRMC:
    def __init__(self, S, mu, sigma, c, n, iterations):
        # this is the value of our initial investment at t = 0
        self.S = S
        self.mu = mu
        self.sigma = sigma
        self.c = c
        self.n = n
        self.iterations = iterations

    def simulate(self):
        rand = np.random.normal(0, 1, [1, self.iterations])

        # equation for the S(t) stock price
        # the random walk of our initial investment
        stock_price = self.S * np.exp(self.n * (self.mu - 0.5 * self.sigma ** 2) +
                                      self.sigma * np.sqrt(self.n) * rand)

        # we have to sort the stock prices to determine the percentile
        stock_price = np.sort(stock_price)

        # depends on the confidence level: 95% -> 5 and 99% -> 1
        percentile = np.percentile(stock_price, (1 - self.c) * 100)

        return self.S - percentile

if __name__ == '__main__':
    S = 1e6 # initial investment (stocks, etc)
    c = 0.95 # confidence interval
    n = 1 # num of days
    iterations = 100000 # number of paths in the MC simulation

    # historical data to approximate mean and std. dev.
    start = datetime.datetime(2020, 1, 1)
    end = datetime.datetime(2025, 1, 1)

    # download stock-related data from Yahoo Finance
    citi = download_data('C', start, end)

    # use pct_change() to calculate daily returns
    citi['returns'] = citi['Close'].pct_change()

    # we can assume daily returns are normally distributed
    # mean and variance (Std. dev.) can describe the process
    mu = np.mean(citi['returns'])
    sigma = np.std(citi['returns'])

    model = VaRMC(S, mu, sigma, c, n, iterations)
    print('Value at risk with MC Simulation: $%.2f' % model.simulate())
