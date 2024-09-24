import dash
from dash import html, dcc, ClientsideFunction
import dash.dependencies as dd
import json
import os
from utils import vis_start, vis_end, ppred_start, start_date, end_date
from utils import download_stock_data, tickers, PRED_LEN
from pathlib import Path

import dash_bootstrap_components as dbc

stock_data = download_stock_data(tickers, start_date, end_date)
stock_data_json = json.dumps(stock_data)

mdl_data = ""
with open("model_list.json") as file:
    mdl_data = json.load(file)

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
            style={
                'width': '70vw',
                'margin': 'auto',
                'margin-top': '2vh',
                'margin-left': '26vw'
            },
            className='data-graph'
        ),

        dcc.Graph(
            id='metric-graph',
            className='data-graph',
            style={
                'width': '70vw',
                'margin': 'auto',
                'margin-top': '2vh',
                'margin-left': '26vw'
            }
        ),

        html.Div(
            [
                html.H1("How does it work?"),
                html.P(
                    f"""
                    Alcompare analyzes and visualizes the performance of multiple time series forecasting models 
                    using financial data sourced from the yfinance Python library. 
                    The models are trained on approximately 15 years of historical stock closing prices for a selected ticker. 
                    Leveraging this extensive dataset, they aim to predict the stock's closing price for the next {PRED_LEN} days, 
                    providing a robust comparison of forecasting accuracy and model effectiveness
                    """
                )
            ],

            style={
                'text-align': 'center',
                'height': '20vh',
                'width': '70vw',
                'margin-top': '4vh',
                'margin-left': '26vw'
            }
        ),

        html.Div(
            [
                html.H1("How should I compare models?"),
                html.P(
                    [
                        """
                        Alcompare delivers intuitive visualizations of model predictions, making interpretation simpler than raw data alone. 
                        In addition, it calculates key performance metrics like """,
                        html.A("MSE", href="https://en.wikipedia.org/wiki/Mean_squared_error"),
                        ", ",
                        html.A("MAPE", href="https://en.wikipedia.org/wiki/Mean_absolute_percentage_error"),
                        ", ",
                        html.A("R2", href="https://en.wikipedia.org/wiki/Coefficient_of_determination"),
                        ", ",
                        html.A("MedAE", href="https://scikit-learn.org/stable/modules/generated/sklearn.metrics.median_absolute_error.html"),
                        " enabling more precise and quantitative comparisons."
                    ]
                )
            ],

            style={
                'text-align': 'center',
                'height': '20vh',
                'width': '70vw',
                'margin-left': '26vw',
                'margin-top': '2vh'
            }
        ),

        html.Div(
            [
                html.H1("Why?"),
                html.P(
                    [
                        "A key motivation behind this project was to deepen my understanding of data visualization using Dash and Plotly. ",
                        "Additionally, I saw it as an intriguing challenge to explore hosting a dynamic Dash application on GitHub Pages — "
                        "an area where I noticed a lack of available resources. I decided it would be a valuable contribution to not only accomplish "
                        "this but also create a comprehensive tutorial to guide others. If you're interested in learning how to host a Dash app with interactive, "
                        "real-time graphs (like the one showcased here) on GitHub Pages, you can check out the tutorial I've written ",
                        html.A("here", href="#"),
                        "."
                    ]
                )
            ],

            style={
                'text-align': 'center',
                'height': '20vh',
                'width': '70vw',
                'margin-left': '26vw',
                'margin-top': '2vh'
            }
        ),

        html.Div(
            [
                html.H1("Can I contribute?"),
                html.P(
                    [
                        "If you have an idea, suggestion or a comment feel free to open a merge request, issue or contact me via my ",
                        html.A("email", href="mailto:michal.burzynski0805@gmail.com"),
                        ". Feel free to visit my ",
                        html.A("GitHub Profile", href="https://github.com/dec0dedd"),
                        " and check out other projects."
                    ]
                )
            ],

            style={
                'text-align': 'center',
                'height': '20vh',
                'width': '70vw',
                'margin-left': '26vw',
                'margin-top': '2vh'
            }
        )
    ],

    style={
        'height': '100vh',
        'width': '75vw',
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
