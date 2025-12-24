import numpy as np
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import scipy.optimize as optimization

# On average, there are 252 trading days in a year
NUM_TRADING_DAYS = 252
# We will generate random weights (w) for different portfolios
NUM_PORTFOLIOS = 10000

# stocks we are going to handle
# removed: GE, ^DJI, TSLA
stocks = ['AAPL', 'INTC', 'QUBT', 'AMZN', 'PFE', 'HOOD', 'RGTI']

# historical data - define START and END dates
start_date = '2022-01-01'
end_date = '2025-01-01'

def download_data():
    # name of the stock (key) - stock values (2010 - 2017) as the values
    stock_data = {}

    for stock in stocks:
        # closing prices
        ticker = yf.Ticker(stock)
        stock_data[stock] = ticker.history(start=start_date, end=end_date)['Close']

    return pd.DataFrame(stock_data)


def show_data(data):
    data.plot(figsize=(10, 5))
    plt.show()


def calculate_return(data):
    # NORMALIZATION: to measure all variables in comparable metric
    log_return = np.log(data / data.shift(1))
    return log_return[1:]


def show_statistics(returns):
    # instead of daily metrics, we look for annual metrics
    # mean of annual return
    print(returns.mean() * NUM_TRADING_DAYS)
    print(returns.cov() * NUM_TRADING_DAYS)


def show_mean_variance(returns, weights):
    portfolio_return = np.sum(returns.mean() * weights) * NUM_TRADING_DAYS;
    portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(returns.cov() * NUM_TRADING_DAYS, weights)))

    print("Expected portfolio mean (return): ", portfolio_return)
    print("Expected portfolio volatility (standard deviation): ", portfolio_volatility)


def show_portfolios(returns, volatilities):
    plt.figure(figsize=(10, 6))
    plt.scatter(volatilities, returns, c=returns/volatilities, marker='o')
    plt.grid(True)
    plt.xlabel('Expected Volatility')
    plt.ylabel('Expected Return')
    plt.colorbar(label = 'Sharpe Ratio')
    plt.show()


def generate_portfolios(returns):
    portfolio_means = []
    portfolio_risks = []
    portfolio_weights = []

    for _ in range(NUM_PORTFOLIOS):
        w = np.random.random(len(stocks))
        w /= np.sum(w)
        portfolio_weights.append(w)
        portfolio_means.append(np.sum(returns.mean() * w) * NUM_TRADING_DAYS)
        portfolio_risks.append(np.sqrt(np.dot(w.T, np.dot(returns.cov() * NUM_TRADING_DAYS, w))))

    return np.array(portfolio_weights), np.array(portfolio_means), np.array(portfolio_risks)


def statistics(weights, returns):
    portfolio_return = np.sum(returns.mean() * weights) * NUM_TRADING_DAYS
    portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(returns.cov() * NUM_TRADING_DAYS, weights)))

    return np.array([portfolio_return, portfolio_volatility, portfolio_return / portfolio_volatility])


# scipy optimize module can find the minimum of a given function
# The maximum of a f(x) is the minimum of -f(x)
def min_function_sharpe(weights, returns):
    return -statistics(weights, returns)[2]


# What are the constraints? The sum of weights = 1
# f(x) = 0, this is the function to minimize
def optimize_portfolio(weights, returns):
    # The sum of weights is 1
    constraints = {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}
    # The weights can be 1 at most, when 100% of money is invested into a single stock
    bounds = tuple((0, 1) for _ in range(len(stocks)))
    return optimization.minimize(fun = min_function_sharpe, x0 = weights[0], args = returns, method = 'SLSQP', bounds = bounds, constraints = constraints)


def print_optimal_portfolio(optimum, returns):
    print("Optimal Portfolio: ", optimum['x'].round(3))
    print("Expected return, volatility, and Sharpe Ratio: ", statistics(optimum['x'].round(3), returns))


def show_optimal_portfolio(optimum, returns, portfolio_returns, portfolio_volatilities):
    plt.figure(figsize=(10, 6))
    plt.scatter(portfolio_volatilities, portfolio_returns, c = portfolio_returns / portfolio_volatilities, marker='o')
    plt.grid(True)
    plt.xlabel('Expected Volatility')
    plt.ylabel('Expected Return')
    plt.colorbar(label = 'Sharpe Ratio')
    plt.plot(statistics(optimum['x'], returns)[1], statistics(optimum['x'], returns)[0], 'g*', markersize = 20)
    plt.show()


if __name__ == "__main__":
    dataset = download_data()
    print(dataset)
    show_data(dataset)
    log_daily_returns = calculate_return(dataset)
    show_statistics(log_daily_returns)

    weights, means, risks = generate_portfolios(log_daily_returns)
    show_portfolios(means, risks)
    optimum = optimize_portfolio(weights, log_daily_returns)
    print_optimal_portfolio(optimum, log_daily_returns)
    show_optimal_portfolio(optimum, log_daily_returns, means, risks)







