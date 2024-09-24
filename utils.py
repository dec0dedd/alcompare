import yfinance as yf
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import warnings

warnings.filterwarnings('ignore')

RND_INT = 1237  # random state in forecasting models
PRED_LEN = 120  # number of days of prediction for forecasting models
VIS_LEN = 240  # number of days used in visualization

"""
start_date/end_date - start/end date of all data
ptrain_start/ptrain_end - start/end date of data used for training
ppred_start/ppred_end - start/end date used for prediction
vis_start/vis_end - start/end date of points used in visualization
"""

tickers = ['MSFT', 'GOOGL', 'NVDA', 'GS', 'AMZN', 'TSM']
end_date = datetime.today() - timedelta(1)
start_date = end_date - relativedelta(years=15)

vis_end = end_date
vis_start = vis_end - timedelta(VIS_LEN-1)

ppred_start = end_date - timedelta(PRED_LEN-1)
ppred_end = end_date

ptrain_start = start_date
ptrain_end = ppred_start - timedelta(1)

end_date = end_date.strftime('%Y-%m-%d')
start_date = start_date.strftime('%Y-%m-%d')

ppred_start = ppred_start.strftime('%Y-%m-%d')
ppred_end = ppred_end.strftime('%Y-%m-%d')

ptrain_start = ptrain_start.strftime('%Y-%m-%d')
ptrain_end = ptrain_end.strftime('%Y-%m-%d')

vis_end = vis_end.strftime('%Y-%m-%d')
vis_start = vis_start.strftime('%Y-%m-%d')


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
