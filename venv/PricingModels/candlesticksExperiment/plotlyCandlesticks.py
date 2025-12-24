import plotly.graph_objects as go
import pandas as pd
import yfinance as yf
from datetime import datetime
import time

stock = 'AAPL'
start_date = '2020-01-01'
end_date = datetime.today().strftime('%Y-%m-%d')

# Grabs stock data from Yahoo Finance, returning OHLC values
def download_data():
    # Grabs stock data
    OHLC_cols = ['open', 'high', 'low', 'close']
    data = yf.download(stock, start=start_date, end=end_date)
    # formatting purposes to avoid capitalization inconsistencies
    data.columns = data.columns.get_level_values(0)
    data.columns = data.columns.str.lower().str.strip()
    data.index.name = 'date'

    # Removes any NaN values in data
    data.dropna(subset=OHLC_cols, inplace=True)

    # Prepares data for plotting on candlestick plot
    data = data.reset_index()
    data['date'] = pd.to_datetime(data['date'])

    # force data in columns to be floats to ensure numeric values for plotting
    for col in OHLC_cols:
        data[col] = data[col].astype(float)

    # returns formatted data
    return data

# exports retrieved data from yfinance and stores in .csv file
def export_data(dataset):
    dataset.to_csv('stockData.csv', index=False)

# Displays dataset as a candlestick chart from Plotly
def display_chart(dataset):
    plot = go.Figure(data=[go.Candlestick(x=dataset['date'], open=dataset['open'], high=dataset['high'], low=dataset['low'], close=dataset['close'])])
    plot.update_layout(title=f'{stock}Candlestick Price', xaxis_rangeslider_visible=False)

    # filename = f'{stock}_candlesticks.html'
    # plot.write_html(filename)

    plot.show()

if __name__ == '__main__':
    while True:
        data = download_data()
        print(data.head())
        export_data(data)
        display_chart(data)
        time.sleep(10)
