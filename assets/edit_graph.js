window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        edt: function(stock_data_json, selected_stock, start_date, end_date, sma_checkbox) {
            var stock_data = JSON.parse(stock_data_json);
            var stock = stock_data[selected_stock];

            const arg_idx = 5;
            console.log(`Number of forecasts detected: ${arguments.length-arg_idx-1}`);

            const val_ar = ['line_reg', 'poly_reg'];
            var model_use = [];

            var model_chk = arguments[arg_idx]
            for (var i=0; i<val_ar.length; ++i) {
                if (model_chk.includes(val_ar[i])) {
                    model_use.push(1);
                } else {
                    model_use.push(0);
                }
            }
    
            var filtered_dates = [];
            var filtered_prices = [];
            var filtered_volumes = [];
    
            var start = new Date(start_date);
            var end = new Date(end_date);

            for (var i = 0; i < stock.dates.length; i++) {
                var date = new Date(stock.dates[i]);
                if (date >= start && date <= end) {
                    filtered_dates.push(stock.dates[i]);
                    filtered_prices.push(stock.prices[i]);
                    filtered_volumes.push(stock.volumes[i]);
                }
            }

            var sma_prices = [];
            if (sma_checkbox.includes('SMA')) {
                for (var i = 2; i < filtered_prices.length; i++) {
                    var sma = (filtered_prices[i] + filtered_prices[i-1] + filtered_prices[i-2]) / 3;
                    sma_prices.push(sma);
                }
            }

            var trace = {
                x: filtered_dates,
                y: filtered_prices,
                mode: 'lines',
                name: selected_stock + ' Prices',
                marker: {color: 'green'}
            };

            var sma_trace = {
                x: filtered_dates.slice(2),  // SMA starts from the 3rd date
                y: sma_prices,
                mode: 'lines',
                name: selected_stock + ' 3-day SMA',
                line: {dash: 'dash', color: 'blue'}
            };

            var volume_trace = {
                x: filtered_dates,
                y: filtered_volumes,
                type: 'bar',
                name: selected_stock + ' Volume',
                yaxis: 'y2',
                opacity: 0.3,
                marker: {color: 'orange'}
            };

            var layout = {
                title: selected_stock + ' Stock Prices',
                xaxis: {title: 'Date'},
                yaxis: {title: 'Price (USD)'},
                yaxis2: {
                    title: 'Volume',
                    overlaying: 'y',
                    side: 'right'
                },
                margin: {l: 40, r: 40, t: 40, b: 40}
            };

            var data = [trace, volume_trace];
            if (sma_checkbox.includes('SMA')) {
                data.push(sma_trace);
            }

            for (var i=0; i<model_use.length; ++i) {
                if (model_use[i] === 0) {
                    continue;
                }

                pred_json = JSON.parse(arguments[i+arg_idx+1])[selected_stock];

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
                    name: "Model " + i,
                    marker: {color: 'red'}
                }

                data.push(dtrace)
            }
    
            return {
                data: data,
                layout: layout
            };
        }
    }
});
