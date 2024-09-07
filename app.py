import dash
from dash import html, dcc, ClientsideFunction
import dash.dependencies as dd
import json
import os
from utils import start_date, end_date, pstart_date, tickers
from utils import download_stock_data
from pathlib import Path

stock_data = download_stock_data(tickers, start_date, end_date)
stock_data_json = json.dumps(stock_data)

mdl_data = ""
with open("model_list.json") as file:
    mdl_data = json.load(file)

layout_data = [
    html.H1("Alcompare", style={"text-align": "center"}),
    dcc.Dropdown(
        id='stock-dropdown',
        options=[{'label': ticker, 'value': ticker} for ticker in tickers],
        value='NVDA'
    ),

    dcc.Graph(
        id='stock-graph'
    ),

    dcc.Checklist(
        id='model-checklist',
        options=[{'label': x['name'], 'value': x['value']} for x in mdl_data],
        value=['line_reg']
    ),

    dcc.Tabs(
        id='metric-tabs',
        children=[
            dcc.Tab(label='MSE', value='mse'),
            dcc.Tab(label='MAPE', value='mape')
        ],
        value='mse'
    ),

    dcc.Graph(
        id='metric-graph'
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
    ),

    html.Div(
        id='hidden-model-data',
        style={'display': 'none'},
        children=json.dumps(mdl_data)
    )
]

graph_input = [

]


assert os.path.exists('forecasts')

# Get all predictions from forecasts/ directory
for mdl in mdl_data:
    print(f"Adding data from {mdl['name']}!")

    with open(os.path.join('forecasts', mdl['file'])) as file:
        layout_data.append(
            html.Div(
                id=f'pred-{Path(mdl["file"]).stem}',
                style={'display': 'none'},
                children=json.dumps(json.load(file))
            )
        )

        graph_input.append(
            dd.Input(f'pred-{Path(mdl["file"]).stem}', 'children')
        )

app = dash.Dash(__name__)

md_text = ""
with open('desc.md', 'r') as file:
    md_text = file.read()


app.layout = html.Div(layout_data)

app.clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='edit_stock'
    ),

    dd.Output('stock-graph', 'figure'),
    [
        dd.Input('hidden-stock-data', 'children'),
        dd.Input('stock-dropdown', 'value'),
        dd.Input('hidden-start-date', 'children'),
        dd.Input('hidden-end-date', 'children'),
        dd.Input('hidden-pstart-date', 'children'),
        dd.Input('hidden-model-data', 'children'),
        dd.Input('model-checklist', 'value')
    ] + graph_input
)

app.clientside_callback(
    ClientsideFunction(
        namespace='metric_ed',
        function_name='edit_metric'
    ),

    dd.Output('metric-graph', 'figure'),
    [
        dd.Input('stock-dropdown', 'value'),
        dd.Input('hidden-model-data', 'children'),
        dd.Input('metric-tabs', 'value'),
        dd.Input('model-checklist', 'value')
    ] + graph_input
)

app.title = "Alcompare"

if __name__ == '__main__':
    app.run_server(debug=False)
