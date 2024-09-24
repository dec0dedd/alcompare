window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        edit_stock: function(stock_data_json, selected_stock, start_date, end_date, pstart_date, model_json) {
            var stock_data = JSON.parse(stock_data_json);
            var model_data = JSON.parse(model_json)
            var stock = stock_data[selected_stock];

            const arg_idx = 6;
            console.log(`Number of forecasts detected: ${arguments.length-arg_idx-1}`);

            const mdl_value = [];
            const mdl_name = [];
            const mdl_color = [];

            for (var i=0; i < model_data.length; ++i) {
                var obj = model_data[i];

                for (var key in obj) {
                    if (key === "name") {
                        mdl_name.push(obj[key])
                    } else if (key === "value") {
                        mdl_value.push(obj[key])
                    } else if (key == "color") {
                        mdl_color.push(obj[key])
                    }
                }
            }

            var model_use = [];

            var model_chk = arguments[arg_idx]
            for (var i=0; i<mdl_value.length; ++i) {
                if (model_chk.includes(mdl_value[i])) {
                    model_use.push(1);
                } else {
                    model_use.push(0);
                }
            }
    
            var filtered_dates = [];
            var filtered_prices = [];
    
            var start = new Date(start_date);
            var end = new Date(end_date);

            for (var i = 0; i < stock.dates.length; i++) {
                var date = new Date(stock.dates[i]);
                if (date >= start && date <= end) {
                    filtered_dates.push(stock.dates[i]);
                    filtered_prices.push(stock.prices[i]);
                }
            }

            var trace = {
                x: filtered_dates,
                y: filtered_prices,
                mode: 'lines',
                name: selected_stock + ' Prices',
                marker: {color: 'red'},
            };

            var layout = {
                title: selected_stock + ' Stock Prices',
                xaxis: {title: 'Date', gridcolor: '#444'},
                yaxis: {title: 'Price (USD)', gridcolor: '#444'},
                paper_bgcolor: '#1e1e1e',
                plot_bgcolor: '#1e1e1e',
                font: {'color': 'white'},
                shapes: [],
            };

            var data = [trace];

            for (var i=0; i<model_use.length; ++i) {
                if (model_use[i] === 0) {
                    continue;
                }

                var pred_json = JSON.parse(arguments[i+arg_idx+1])['data'][selected_stock]

                var pdates = [];
                var pprices = [];
                for (var key in pred_json) {
                    pdates.push(key)
                    pprices.push(pred_json[key])
                }

                var dtrace = {
                    x: pdates,
                    y: pprices,
                    mode: 'lines',
                    name: mdl_name[i],
                    marker: {color: mdl_color[i]}
                }

                data.push(dtrace);
            }

            const pred_rect = {
                type: 'rect',
                x0: pstart_date, 
                x1: end_date,
                y0: 0,
                y1: 1,
                xref: 'x',
                yref: 'paper',
                line: {
                    color: 'rgba(27, 69, 99, 0.5)',
                    width: 2
                },
                fillcolor: 'rgba(27, 69, 99, 0.2)'
            };

            layout.shapes.push(pred_rect);
            return {
                data: data,
                layout: layout,
            };
        }
    }
});
