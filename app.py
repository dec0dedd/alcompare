import dash
from dash import html, dcc, ClientsideFunction
import dash.dependencies as dd
import yfinance as yf
import json
from data import start_date, end_date, tickers


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


stock_data = download_stock_data(tickers, start_date, end_date)
stock_data_json = json.dumps(stock_data)


app = dash.Dash(__name__)

md_text = ""
with open('desc.md', 'r') as file:
    md_text = file.read()


app.layout = html.Div([
    dcc.Dropdown(
        id='stock-dropdown',
        options=[{'label': ticker, 'value': ticker} for ticker in tickers],
        value='NVDA'
    ),

    dcc.DatePickerRange(
        id='date-picker-range',
        start_date=start_date,
        end_date=end_date,
        display_format='YYYY-MM-DD'
    ),

    dcc.Checklist(
        id='sma-checkbox',
        options=[{'label': 'Show 3-day SMA', 'value': 'SMA'}],
        value=[]
    ),

    dcc.Graph(id='stock-graph'),

    html.Div(
        id='hidden-stock-data',
        style={'display': 'none'},
        children=stock_data_json
    ),

    dcc.Markdown(md_text)
])

app.clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='edt'
    ),

    dd.Output('stock-graph', 'figure'),

    [dd.Input('hidden-stock-data', 'children'),
     dd.Input('stock-dropdown', 'value'),
     dd.Input('date-picker-range', 'start_date'),
     dd.Input('date-picker-range', 'end_date'),
     dd.Input('sma-checkbox', 'value')]
)

if __name__ == '__main__':
    app.run_server(debug=False)
