from dash.react import Dash
from dash_components import h1, PlotlyGraph,TextInput

front_app = Dash('portfolio')
front_app.layout = div([
    h1('Hello portfolio!'),
    TextInput(
        label = 'Stock Tickers'),
    PlotlyGraph(figure = {'data':[
        {'x':[1,2],'y':[3,4,5]}
            ]
        })
    ])
front_app.server.run(debug = True)
