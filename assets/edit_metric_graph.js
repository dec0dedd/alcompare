window.dash_clientside = Object.assign({}, window.dash_clientside, {
    metric_ed: {
        edit_metric: function(selected_stock, model_json, selected_metric) {
            var model_data = JSON.parse(model_json)

            var mdl_name = [];
            var mdl_value = [];

            const arg_idx = 3;
            console.log(`Number of models detected: ${arguments.length-arg_idx}`);

            for (var i=0; i<model_data.length; ++i) {
                var obj = model_data[i];

                for (key in obj) {
                    if (key == "name") {
                        mdl_name.push(obj[key]);
                    } else if (key == "value") {
                        mdl_value.push(obj[key]);
                    }
                }
            }

            var mdl_use = [];
            var mdl_chk = arguments[arg_idx]

            for (var i=0; i<mdl_value.length; ++i) {
                if (mdl_chk.includes(mdl_value[i])) {
                    mdl_use.push(1);
                } else {
                    mdl_use.push(0);
                }
            }

            console.log(mdl_chk)

            var metric_conv = {
                'mse': 'MSE',
                'mape': 'MAPE',
                'r2': 'R2',
                'medae': 'MedAE'
            }

            var data = [];
            for (var i=0; i<mdl_use.length; ++i) {
                if (mdl_use[i] === 0) {
                    continue;
                }

                var met_data = JSON.parse(arguments[i+arg_idx+1])['metrics'][selected_stock][metric_conv[selected_metric]]
                console.log(met_data)

                var dbar = {
                    x: [met_data],
                    y: [mdl_name[i]],
                    name: mdl_name[i],
                    type: 'bar',
                    orientation: 'h',
                    marker: {'color': model_data[i]['color']}
                };

                data.push(dbar)
            }

            var layout = {
                title: 'Model metrics on ' + selected_stock + ' stock prices',
                xaxis: {title: metric_conv[selected_metric], gridcolor: '#444'},
                yaxis: {gridcolor: '#444'},
                paper_bgcolor: '#1e1e1e',
                plot_bgcolor: '#1e1e1e',
                font: {'color': 'white'}

            }

            console.log(data)
            return {
                data: data,
                layout: layout,
            };
        }
    }
});
