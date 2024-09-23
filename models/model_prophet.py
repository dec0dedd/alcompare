import pandas as pd
import sys
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error
from sklearn.metrics import r2_score, median_absolute_error

from prophet import Prophet

from datetime import datetime
import json

sys.path.append(".")
from utils import start_date, end_date, ppred_start, ppred_end, tickers
from utils import PRED_LEN, download_stock_data

data = download_stock_data(tickers, start_date, end_date)


def date2ts(dt):
    dt = datetime.strptime(dt, '%Y-%m-%d')
    return int(dt.timestamp())


def ts2date(ts):
    ts = datetime.fromtimestamp(ts)
    return str(ts.date())


def gen_tintv(start, len):
    dt_pred = pd.DataFrame(
        pd.date_range(start=start, freq='D', periods=len)
        )

    dt_pred = dt_pred[0].astype('int64') // 10**9
    dt_pred.name = 'dates'
    return dt_pred


print(f"Starting prediction for Prophet model from {ppred_start} to {ppred_end}.")

sm_data = gen_tintv(ppred_start, PRED_LEN)

dc = {
    'metrics': {
        ticker: {} for ticker in tickers
    },
}

for ticker in tickers:
    df = pd.DataFrame(data[ticker], columns=['dates', 'prices', 'volumes'])
    df.drop(columns=['volumes'], inplace=True)
    df['ds'] = pd.to_datetime(df['dates'])
    df['y'] = df.pop('prices')

    df_train = df.loc[df['ds'] < datetime.strptime(ppred_start, '%Y-%m-%d')]
    df_pred = df.loc[df['ds'] >= datetime.strptime(ppred_start, '%Y-%m-%d')]

    mdl = Prophet().fit(df_train)
    ftr = mdl.make_future_dataframe(periods=PRED_LEN).tail(PRED_LEN)

    X_pred = df_pred.pop('ds').to_frame()
    y_pred = df_pred.pop('y').to_frame()

    pred = mdl.predict(X_pred)['yhat']
    mse = mean_squared_error(y_pred, pred)
    mape = mean_absolute_percentage_error(y_pred, pred)
    r2 = r2_score(y_pred, pred)
    medae = median_absolute_error(y_pred, pred)
    print(f"Metrics for Linear forecast on {ticker}:")
    print(f"MSE: {mse}")
    print(f"MAPE: {mape}")
    print(f"R^2: {r2}")
    print(f"MedAE: {medae}")

    dc['metrics'][ticker]['MSE'] = mse
    dc['metrics'][ticker]['MAPE'] = mape
    dc['metrics'][ticker]['R2'] = r2
    dc['metrics'][ticker]['MedAE'] = medae

    ftr = mdl.make_future_dataframe(periods=PRED_LEN).tail(PRED_LEN)
    prd = mdl.predict(ftr)['yhat'].rename(ticker)

    sm_data = pd.concat([sm_data, prd], axis=1)


sm_data['dates'] = sm_data['dates'].apply(ts2date)
sm_data.set_index('dates', inplace=True)

assert sm_data.shape[0] == PRED_LEN

dc['data'] = sm_data.to_dict()

with open('./forecasts/prophet.json', 'w') as fl:
    json.dump(dc, fl)
