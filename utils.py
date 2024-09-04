import yfinance as yf
from datetime import datetime
from dateutil.relativedelta import relativedelta

RND_INT = 1237  # random state in forecasting models
PRED_LEN = 10  # number of days of prediction for forecasting models

tickers = ['MSFT', 'GOOGL', 'NVDA', 'GS']
end_date = datetime.today()
start_date = end_date - relativedelta(years=1)
end_date = end_date.strftime('%Y-%m-%d')
start_date = start_date.strftime('%Y-%m-%d')


def download_stock_data(tickers, start_date, end_date):
    stock_data = {}
    for ticker in tickers:
        df = yf.download(ticker, start=start_date, end=end_date)
        df.reset_index(inplace=True)
        stock_data[ticker] = {
            "dates": df['Date'].dt.strftime('%Y-%m-%d').tolist(),
            "prices": df['Close'].tolist(),
            "volumes": df['Volume'].tolist()
        }
    return stock_data
