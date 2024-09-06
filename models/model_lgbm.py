import pandas as pd
import sys
from skforecast.ForecasterAutoreg import ForecasterAutoreg
from lightgbm import LGBMRegressor
from sklearn.metrics import mean_squared_error
from datetime import datetime

sys.path.append(".")
from utils import start_date, end_date, pstart_date, tickers, PRED_LEN, download_stock_data, RND_INT

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


sm_data = gen_tintv(pstart_date, PRED_LEN)


def transform_df(df):
    return df


for ticker in tickers:
    df = pd.DataFrame(data[ticker], columns=['dates', 'prices', 'volumes'])
    df.drop(columns=['volumes'], inplace=True)
    df['dates'] = df['dates'].apply(date2ts)
    df = transform_df(df)

    df_train = df.loc[df['dates'] < date2ts(pstart_date)]
    df_pred = df.loc[df['dates'] >= date2ts(pstart_date)]

    X_train = df_train.pop('dates').to_frame()
    y_train = df_train.pop('prices')

    X_pred = df_pred.pop('dates').to_frame()
    y_pred = df_pred.pop('prices')

    mdl = ForecasterAutoreg(
        regressor=LGBMRegressor(random_state=RND_INT, verbose=-1),
        lags=24
    )

    mdl.fit(y=y_train)

    mse = mean_squared_error(y_pred, mdl.predict(steps=y_pred.shape[0]))
    print(f"MSE of LGBM forecast = {mse} for {ticker}")

    prd = mdl.predict(steps=PRED_LEN).reset_index(drop=True)
    prd.name = ticker

    sm_data = pd.concat(
        [sm_data, prd],
        axis=1
    )


sm_data['dates'] = sm_data['dates'].apply(ts2date)
sm_data.set_index('dates', inplace=True)

assert sm_data.shape[0] == PRED_LEN
print(sm_data)

sm_data.to_json('./forecasts/LGBM.json')
