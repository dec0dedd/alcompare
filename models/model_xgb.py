import pandas as pd
import sys
from skforecast.ForecasterAutoreg import ForecasterAutoreg
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error
from sklearn.metrics import r2_score, median_absolute_error
from datetime import datetime
import json

sys.path.append(".")
from utils import start_date, end_date, ppred_start, ppred_end, tickers
from utils import PRED_LEN, download_stock_data, RND_INT

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


sm_data = gen_tintv(ppred_start, PRED_LEN)


dc = {
    'metrics': {
        ticker: {} for ticker in tickers
    },
}


def transform_df(df):
    return df


for ticker in tickers:
    df = pd.DataFrame(data[ticker], columns=['dates', 'prices', 'volumes'])
    df.drop(columns=['volumes'], inplace=True)
    df['dates'] = df['dates'].apply(date2ts)
    df = transform_df(df)

    df_train = df.loc[df['dates'] < date2ts(ppred_start)]
    df_pred = df.loc[df['dates'] >= date2ts(ppred_start)]

    X_train = df_train.pop('dates').to_frame()
    y_train = df_train.pop('prices')

    X_pred = df_pred.pop('dates').to_frame()
    y_pred = df_pred.pop('prices')

    mdl = ForecasterAutoreg(
        regressor=XGBRegressor(
            n_estimators=3000,
            learning_rate=0.01,
            n_jobs=-1,
            random_state=RND_INT,
            verbose=-1
        ),
        lags=120
    )

    mdl.fit(y=y_train)

    mse = mean_squared_error(y_pred, mdl.predict(steps=y_pred.shape[0]))
    mape = mean_absolute_percentage_error(y_pred, mdl.predict(y_pred.shape[0]))
    r2 = r2_score(y_pred, mdl.predict(y_pred.shape[0]))
    medae = median_absolute_error(y_pred, mdl.predict(y_pred.shape[0]))
    print(f"Metrics for XGB forecast on {ticker}:")
    print(f"MSE: {mse}")
    print(f"MAPE: {mape}")
    print(f"R2: {r2}")
    print(f"MedAE: {medae}")

    dc['metrics'][ticker]['MSE'] = mse
    dc['metrics'][ticker]['MAPE'] = mape
    dc['metrics'][ticker]['R2'] = r2
    dc['metrics'][ticker]['MedAE'] = medae

    prd = mdl.predict(steps=PRED_LEN).reset_index(drop=True)
    prd.name = ticker

    sm_data = pd.concat(
        [sm_data, prd],
        axis=1
    )


sm_data['dates'] = sm_data['dates'].apply(ts2date)
sm_data.set_index('dates', inplace=True)

assert sm_data.shape[0] == PRED_LEN

dc['data'] = sm_data.to_dict()

with open('./forecasts/XGB.json', 'w') as fl:
    json.dump(dc, fl)
