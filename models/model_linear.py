import pandas as pd
import sys
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from datetime import datetime

sys.path.append(".")
from utils import start_date, end_date, ptrain_end, pstart_date, tickers, PRED_LEN, download_stock_data

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

print(f"Starting prediction for Linear regression model from {pstart_date} to {end_date}.")

sm_data = gen_tintv(pstart_date, PRED_LEN)

for ticker in tickers:
    df = pd.DataFrame(data[ticker], columns=['dates', 'prices', 'volumes'])
    df.drop(columns=['volumes'], inplace=True)
    df['dates'] = df['dates'].apply(date2ts)

    df_train = df.loc[df['dates'] <= date2ts(ptrain_end)]
    df_pred = df.loc[df['dates'] >= date2ts(pstart_date)]

    X_train = df_train.pop('dates').to_frame()
    y_train = df_train.pop('prices').to_frame()

    X_pred = df_pred.pop('dates').to_frame()
    y_pred = df_pred.pop('prices').to_frame()

    mdl = LinearRegression(
        n_jobs=-1
    ).fit(X_train, y_train)

    mse = mean_squared_error(y_train, mdl.predict(X_train))
    print(f"MSE of {type(mdl).__name__} = {mse} for {ticker}")

    to_pred = gen_tintv(pstart_date, PRED_LEN).to_frame()
    prd = mdl.predict(to_pred).reshape(PRED_LEN)

    sm_data = pd.concat([sm_data, pd.Series(prd, name=ticker)], axis=1)


sm_data['dates'] = sm_data['dates'].apply(ts2date)
sm_data.set_index('dates', inplace=True)

assert sm_data.shape[0] == PRED_LEN
print(sm_data)

sm_data.to_json('./forecasts/LinearRegression.json')
