import dash
from dash import html, dcc, ClientsideFunction
import dash.dependencies as dd
import json
import os
from data import start_date, end_date, tickers
from utils import download_stock_data
from pathlib import Path

stock_data = download_stock_data(tickers, start_date, end_date)
stock_data_json = json.dumps(stock_data)

layout_data = [
    html.H1("Stockviz", style={"text-align": "center"}),
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
    )
]

graph_input = [
    dd.Input('hidden-stock-data', 'children'),
    dd.Input('stock-dropdown', 'value'),
    dd.Input('date-picker-range', 'start_date'),
    dd.Input('date-picker-range', 'end_date'),
    dd.Input('sma-checkbox', 'value')
]


assert os.path.exists('forecasts')

# Get all predictions from forecasts/ directory
for fn in os.listdir('forecasts'):
    print(f"Adding data from {fn}")

    with open(os.path.join('forecasts', fn)) as file:
        layout_data.append(
            html.Div(
                id=f'pred-{Path(fn).stem}',
                style={'display': 'none'},
                children=json.dumps(json.load(file))
            )
        )

        graph_input.append(
            dd.Input(f'pred-{Path(fn).stem}', 'children')
        )

app = dash.Dash(__name__)

md_text = ""
with open('desc.md', 'r') as file:
    md_text = file.read()


app.layout = html.Div(layout_data)

app.clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='edt'
    ),

    dd.Output('stock-graph', 'figure'),
    graph_input
)

if __name__ == '__main__':
    app.run_server(debug=False)
