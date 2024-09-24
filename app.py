import dash
from dash import html, dcc, ClientsideFunction
import dash.dependencies as dd
import json
import os
from utils import vis_start, vis_end, ppred_start, start_date, end_date
from utils import download_stock_data, tickers
from pathlib import Path

import dash_bootstrap_components as dbc

stock_data = download_stock_data(tickers, start_date, end_date)
stock_data_json = json.dumps(stock_data)

mdl_data = ""
with open("model_list.json") as file:
    mdl_data = json.load(file)

md_text = ""
with open("desc.md") as file:
    md_text = file.read()

metric_style = {
    'width': '95vw',
    'marginLeft': 'auto',
    'marginRight': 'auto',
}

graph_input = []
pred_data = []


assert os.path.exists('forecasts')

# Get all predictions from forecasts/ directory
for mdl in mdl_data:
    print(f"Adding data from {mdl['name']}!")

    with open(os.path.join('forecasts', mdl['file'])) as file:
        pred_data.append(
            html.Div(
                id=f'pred-{Path(mdl["file"]).stem}',
                style={'display': 'none'},
                children=json.dumps(json.load(file))
            )
        )

        graph_input.append(
            dd.Input(f'pred-{Path(mdl["file"]).stem}', 'children')
        )
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.themes.DARKLY])

md_text = ""
with open('desc.md', 'r') as file:
    md_text = file.read()


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


sidebar = html.Div(
    [
        html.H2("Alcompare", className='display-4', style={'text-align': 'center'}),
        html.Hr(style={'color': 'white', 'width': '20vw', 'margin': 'auto'}),
        html.P(
            "Effective and easy comparisions of time series models",
            className='lead'
        ),

        dcc.Dropdown(
            id='stock-dropdown',
            options=[{'label': ticker, 'value': ticker} for ticker in tickers],
            value=tickers[0],
            style={'width': '20vw', 'margin': 'auto'}
        ),

        dcc.Checklist(
            id='model-checklist',
            options=[{'label': x['name'], 'value': x['value']} for x in mdl_data],
            value=['line_reg', 'xgb', 'prophet'],
            style={'margin-top': '5vh', 'margin-down': '5vh', 'margin-left': '1vw', 'margin-right': '5vw'}
        ),

        html.Div(
            [
                dbc.RadioItems(
                    id="metric-tabs",
                    className="btn-group",
                    inputClassName="btn-check",
                    labelClassName="btn btn-outline-primary",
                    labelCheckedClassName="active",
                    options=[
                        {"label": "MSE", "value": 'mse'},
                        {"label": "MAPE", "value": 'mape'},
                        {"label": "R2", "value": 'r2'},
                        {'label': 'MedAE', 'value': 'medae'}
                    ],
                    value='mse',
                    style={'width': '15vw', 'margin-left': '5vw', 'margin-right': '5vw', 'margin-top': '3vh'}
                )
            ],
            className='radio-group'
        )
    ],

    style={
        'height': '100vh',
        'width': '25vw',
        'background-color': 'black',
        "top": 0,
        "left": 0,
        "bottom": 0,
        'position': 'fixed'
    }
)

main_contents = html.Div(
    [
        dcc.Graph(
            id='stock-graph',
            style={'width': '70vw', 'margin': 'auto', 'margin-top': '3vh'},
            className='data-graph'
        ),

        dcc.Graph(
            id='metric-graph',
            className='data-graph',
            style={
                'width': '70vw',
                'margin': 'auto',
                'margin-top': '3vh'
            }
        )
    ],

    style={
        'height': '100vh',
        'width': '75vw',
        'margin-left': '25vw'
    }
)

data_divs = html.Div(
    [
        html.Div(
            id='hidden-stock-data',
            style={'display': 'none'},
            children=stock_data_json
        ),

        html.Div(
            id='hidden-start-date',
            style={'display': 'none'},
            children=vis_start
        ),

        html.Div(
            id='hidden-end-date',
            style={'display': 'none'},
            children=vis_end
        ),

        html.Div(
            id='hidden-pstart-date',
            style={'display': 'none'},
            children=ppred_start
        ),

        html.Div(
            id='hidden-model-data',
            style={'display': 'none'},
            children=json.dumps(mdl_data)
        ),
    ]
)

app.layout = dbc.Container(
    [
        sidebar,
        main_contents,
        data_divs,
        *pred_data
    ],

    fluid=True,
    style={'display': 'flex'},
)

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
