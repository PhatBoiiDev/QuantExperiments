import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

# market interest rate
RISK_FREE_RATE = 0.05
# considering monthly returns, and we want to caluclate the annual return
MONTHS_IN_YEAR = 12

class CAPM:
    def __init__(self, stocks, start_date, end_date):
        self.stocks = stocks
        self.start_date = start_date
        self.end_date = end_date
        self.data = None

    def download_data(self):
        data = {}
        for stock in self.stocks:
            ticker = yf.download(stock, self.start_date, self.end_date)

            #if ticker.empty:
            #    continue
            #if 'Close' not in ticker.columns:
            #    continue

            data[stock] = ticker['Close']

        # return pd.DataFrame(data)
        return pd.concat(data, axis=1)

    def initialize(self):
        stock_data = self.download_data()
        print(stock_data)
        # We use monthly returns instead of daily returns
        stocks_data = stock_data.resample('ME').last()
        # self.data = pd.DataFrame({'s_adjclose': stock_data[self.stocks[0]],
        #                          'm_adjclose': stock_data[self.stocks[1]]})
        self.data = pd.concat({'s_adjclose': stock_data[self.stocks[0]],
                                  'm_adjclose': stock_data[self.stocks[1]]}, axis=1)

        #print(self.data)
        # Logarithmic monthly returns
        self.data[['s_returns', 'm_returns']] = np.log(self.data[['s_adjclose', 'm_adjclose']] /
                                                       self.data[['s_adjclose', 'm_adjclose']].shift(1))

        # remove the NaN values
        self.data = self.data[1:]
        print(self.data)

    def calculate_beta(self):
        # covariance matrix: the diagonal items are the variances
        # off diagonals are the covariances
        # the matrix is symmetric: cov[0, 1] = cov[1, 0]
        covariance_matrix = np.cov(self.data['s_returns'], self.data['m_returns'])
        # calculating beta according to the matrix
        beta = covariance_matrix[0, 1] / covariance_matrix[1, 1]
        print("Beta from formula: ", beta)

    def regression(self):
        # using linear regression to fit a line to the data
        # [stock_returns, market_returns] - slope is the beta
        beta, alpha = np.polyfit(self.data['m_returns'], self.data['s_returns'], deg=1)
        print("Beta from regression: ", beta)
        # calculate the expected return according to the CAPM formula
        # we are after the annual return (why we multiply by 12)
        expected_return = RISK_FREE_RATE + beta * (self.data['m_returns'].mean() * MONTHS_IN_YEAR - RISK_FREE_RATE)
        print("Expected Return: ", expected_return)
        self.plot_regression(alpha, beta)

    def plot_regression(self, alpha, beta):
        fig, axis = plt.subplots(1, figsize=(16, 8))
        axis.scatter(self.data['m_returns'], self.data['s_returns'], label = "Data Points")
        axis.plot(self.data['m_returns'], beta * self.data['m_returns'] + alpha, color = 'red', label = "CAPM Line")
        plt.title('Capital Asset Pricing Model, finding alpha and beta')
        plt.xlabel('Market Return $R_m$', fontsize=18)
        plt.ylabel('Stock Return $R_a$')
        plt.text(0.08, 0.05, r'$R_a = \beta * R_m + \alpha$', fontsize=18)
        plt.legend()
        plt.grid(True)
        plt.show()



if __name__ == '__main__':
    capm = CAPM(['IBM', '^GSPC'], '2015-01-01', '2020-01-01')
    capm.initialize()
    capm.calculate_beta()
    capm.regression()