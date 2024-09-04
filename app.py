import dash
from dash import html, dcc, ClientsideFunction
import dash.dependencies as dd
import json
import os
from utils import start_date, end_date, tickers, pstart_date
from utils import download_stock_data
from pathlib import Path

stock_data = download_stock_data(tickers, start_date, end_date)
stock_data_json = json.dumps(stock_data)

model_options = [
    {'label': 'Linear regression', 'value': 'line_reg'},
    {'label': 'Polynomial regression', 'value': 'poly_reg'}
]

layout_data = [
    html.H1("Stockviz", style={"text-align": "center"}),
    dcc.Dropdown(
        id='stock-dropdown',
        options=[{'label': ticker, 'value': ticker} for ticker in tickers],
        value='NVDA'
    ),

    dcc.Checklist(
        id='sma-checkbox',
        options=[{'label': 'Show 3-day SMA', 'value': 'SMA'}],
        value=[]
    ),

    dcc.Graph(id='stock-graph'),

    dcc.Checklist(
        id='model-checklist',
        options=model_options,
        value=['line_reg']
    ),

    html.Div(
        id='hidden-stock-data',
        style={'display': 'none'},
        children=stock_data_json
    ),

    html.Div(
        id='hidden-start-date',
        style={'display': 'none'},
        children=start_date
    ),

    html.Div(
        id='hidden-end-date',
        style={'display': 'none'},
        children=end_date
    ),

    html.Div(
        id='hidden-pstart-date',
        style={'display': 'none'},
        children=pstart_date
    )
]

graph_input = [
    dd.Input('hidden-stock-data', 'children'),
    dd.Input('stock-dropdown', 'value'),
    dd.Input('hidden-start-date', 'children'),
    dd.Input('hidden-end-date', 'children'),
    dd.Input('hidden-pstart-date', 'children'),
    dd.Input('sma-checkbox', 'value'),
    dd.Input('model-checklist', 'value')
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
