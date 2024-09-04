import yfinance as yf
import os


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


def get_path(path):
    return os.path.join(os.getcwd(), path)
