import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

NUM_SIMULATIONS = 1000

# N = 252 trading days in a year
def stock_montecarlo(stockPrice, mu, sigma, N = 252):
    result = []

    # number of simulations - possible S(t) realizations of the process
    for _ in range(NUM_SIMULATIONS):
        prices = [stockPrice]
        for _ in range(N):
            # simulate the day-by-day change (t = 1, no need to multiply t)
            stock_price = prices[-1] * np.exp((mu - 0.5 * sigma ** 2) +
                                              sigma * np.random.normal())
            prices.append(stock_price)
        result.append(prices)

    simulation_data = pd.DataFrame(result)
    # the given columns will contain the time series for a given simulation
    simulation_data = simulation_data.T

    simulation_data['mean'] = simulation_data.mean(axis=1)
    plt.plot(simulation_data['mean'])
    plt.show()

    print('Prediction for future stock price: $%.2f' % simulation_data['mean'].tail(1))

if __name__ == '__main__':
    stock_montecarlo(50, 0.0002, 0.01)
