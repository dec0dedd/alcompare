import yfinance as yf
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import warnings

warnings.filterwarnings('ignore')

RND_INT = 1237  # random state in forecasting models
PRED_LEN = 120  # number of days of prediction for forecasting models

tickers = ['MSFT', 'GOOGL', 'NVDA', 'GS']
end_date = datetime.today() - timedelta(1)
start_date = end_date - relativedelta(years=1)

pstart_date = end_date - timedelta(PRED_LEN-1)
pend_date = end_date

ptrain_start = start_date
ptrain_end = pstart_date - timedelta(1)

end_date = end_date.strftime('%Y-%m-%d')
start_date = start_date.strftime('%Y-%m-%d')

pstart_date = pstart_date.strftime('%Y-%m-%d')
pend_date = pend_date.strftime('%Y-%m-%d')

ptrain_start = ptrain_start.strftime('%Y-%m-%d')
ptrain_end = ptrain_end.strftime('%Y-%m-%d')


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
