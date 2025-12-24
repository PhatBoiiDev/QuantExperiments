import numpy as np

class OptionPricing:

    def __init__(self, initialValue, strikePrice, maturityTime, riskFreeRate, sigma, numIterations):
        self.initialValue = initialValue
        self.strikePrice = strikePrice
        self.maturityTime = maturityTime
        self.riskFreeRate = riskFreeRate
        self.sigma = sigma
        self.numIterations = numIterations

    def call_option_simulation(self):
        # we have 2 columns: col 1 will hold 0s, col 2 will store the payoff
        # we need the first column of 0s: payoff function is max(0, S - E) for call option
        optionData = np.zeros([self.numIterations, 2])

        # dimensions: 1-dimensional array with as many items as the iterations
        rand = np.random.normal(0, 1, [1, self.numIterations])

        # equation for the stock price S(t) at T
        stockPrice = self.initialValue * np.exp(self.maturityTime * (self.riskFreeRate - 0.5 * self.sigma ** 2)
                                                + self.sigma * np.sqrt(self.maturityTime) * rand)

        # we need S - E because we have to calculate the max(S - E, 0)
        optionData[:, 1] = stockPrice - self.strikePrice

        # average for the Monte-Carlo simulation
        # max() returns the max(S - E, 0) according to the formula
        average = np.sum(np.amax(optionData, axis=1)) / float(self.numIterations)

        # have to use the exp(-rT) dicsount factor
        return np.exp(-1.0 * self.riskFreeRate * self.maturityTime) * average
        #print(optionData)

    def put_option_simulation(self):
        # we have 2 columns: col 1 will hold 0s, col 2 will store the payoff
        # we need the first column of 0s: payoff function is max(0, S - E) for call option
        optionData = np.zeros([self.numIterations, 2])

        # dimensions: 1-dimensional array with as many items as the iterations
        rand = np.random.normal(0, 1, [1, self.numIterations])

        # equation for the stock price S(t) at T
        stockPrice = self.initialValue * np.exp(self.maturityTime * (self.riskFreeRate - 0.5 * self.sigma ** 2)
                                                + self.sigma * np.sqrt(self.maturityTime) * rand)

        # we need E - S because we have to calculate the max(E - S, 0)
        optionData[:, 1] = self.strikePrice - stockPrice

        # average for the Monte-Carlo simulation
        # max() returns the max(E - S, 0) according to the formula
        average = np.sum(np.amax(optionData, axis=1)) / float(self.numIterations)

        # have to use the exp(-rT) dicsount factor
        return np.exp(-1.0 * self.riskFreeRate * self.maturityTime) * average
        #print(optionData)

if __name__ == '__main__':
    model = OptionPricing(100, 100, 1, 0.05, 0.2, 1000)
    model.call_option_simulation()
    print('Value of the call option is: $%.2f' % model.call_option_simulation())
    print('Value of the put option is: $%.2f' % model.put_option_simulation())

