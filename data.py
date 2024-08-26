from datetime import datetime
from dateutil.relativedelta import relativedelta

RND_INT = 1237  # random state in forecasting models
PRED_LEN = 60  # length of prediction for forecasting models

tickers = ['MSFT', 'GOOGL', 'NVDA', 'GS']
end_date = datetime.today()
start_date = end_date - relativedelta(years=1)
end_date = end_date.strftime('%Y-%m-%d')
start_date = start_date.strftime('%Y-%m-%d')
