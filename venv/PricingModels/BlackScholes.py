from scipy import stats
from numpy import log, exp, sqrt

def call_option_price(stockPrice, strikePrice, expiryDate, riskFreeRate, sigma):
    # first, calculate the d1 and d1 parameters
    d1 = (log(stockPrice / strikePrice) + (riskFreeRate + sigma * sigma / 2.0) * expiryDate) / (sigma * sqrt(expiryDate))
    d2 = d1 - sigma * sqrt(expiryDate)
    print("The d1 and d2 parameters are: %s, %s" % (d1, d2))

    # use the N(x) to calculate the price of the option
    return stockPrice * stats.norm.cdf(d1) - strikePrice * exp(-riskFreeRate * expiryDate) * stats.norm.cdf(d2)

def put_option_price(stockPrice, strikePrice, expiryDate, riskFreeRate, sigma):
    # first, calculate the d1 and d1 parameters
    d1 = (log(stockPrice / strikePrice) + (riskFreeRate + sigma * sigma / 2.0) * expiryDate) / (sigma * sqrt(expiryDate))
    d2 = d1 - sigma * sqrt(expiryDate)
    print("The d1 and d2 parameters are: %s, %s" % (d1, d2))

    # use the N(x) to calculate the price of the option
    return -stockPrice * stats.norm.cdf(-d1) + strikePrice * exp(-riskFreeRate * expiryDate) * stats.norm.cdf(-d2)

if __name__ == "__main__":
    # underlying stock price at t = 0
    s0 = 100
    # strike price
    E = 100
    # expiry date is in 1 year = 365 days
    T = 1
    # risk-free rate
    rf = 0.05
    # volatility of the underlying stock
    sigma = 0.2

    print("Call option price according to Black-Scholes Model: ",
          call_option_price(s0, E, T, rf, sigma))
    print("Put option price according to Black-Scholes Model: ",
          put_option_price(s0, E, T, rf, sigma))


