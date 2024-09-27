# Alcompare

Alcompare is a simple Python and JavaScript project for comparing different models at forecasting time series data. The data used comes from Yahoo Finance using [yfinance](https://pypi.org/project/yfinance/) library. The project uses Github Pages to generate and show visualization and Github Actions to run forecasts. Time series is updated every day with new data.

Visualizations are made using [Dash](https://dash.plotly.com/) and [Plotly.js](https://plotly.com/javascript/) for clientside callbacks.

## Run locally
In order to run the app locally you need to download the repository and install all dependencies. Then generate forecasts of all models with:
```
make forecast
```
You can find the predictions (in JSON format) in directory `forecasts/`. Then you just need to run:
```
python app.py
```
and go to `http://127.0.0.1:8050`.

## Adding new models

In order to add a model you need to do the following:

1. Add model data to `model_list.json`. Simply add another dict with model information e.g.

```
{
    "name": "Linear regression",
    "value": "line_reg",
    "file": "LinearRegression.json",
    "color": "green"
}
```

where:
- `name` is the name of the model (used e.g. in checklist), 
- `value` is a unique id of the model (it has to be different from values of all other models), 
- `file` is a name of the file in `forecasts/` where prediction results will be stored,
- `color` is the color of a line used to denote model's forecasts.

2. Create a python file in `models/` to generate predictions. The model should generate predictions and save them to JSON file. The file should have the following structure:

```
{
    "metrics": {
        "MSFT": {
            "MSE": ...,
            "MAPE": ...,
        },
        
        "GOOGL": {
            "MSE": ...,
            "MAPE": ...,
        },
        
        ...
    },
    
    "data": {
        "MSFT": {
            "2023-09-15": ...,
            "2023-09-16": ...,
            ...
        },
        
        "GOOGL": {
            "2023-09-15": ...,
            "2023-09-16": ...,
            ...
        },
        
        ...
    }
}
```

3. Run the model to generate predictions. Feel free to submit a merge request if you'd like to share your model, and I'll check it out :)