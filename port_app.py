# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from flask import Flask
import pandas_datareader as web
import datetime

def get_stock_data(ticker):
    start = datetime.datetime(2014, 11, 14)
    end = datetime.datetime(2019, 11, 13)
    data = web.DataReader("ACRGF", 'yahoo', start, end)
    return data


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
server = Flask(__name__)
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
asset = get_stock_data('TSLA')
colors = {
    'background': '#ffffff',
    'text': '#ff1aff'
}

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Algorithmic Trading portfolio',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Div(children='Portfolio performance', style={
        'textAlign': 'center',
        'color': colors['text']
    }),

    dcc.Graph(
        id='example-graph-2',
        figure={
            'data': [
                {'x':list(asset.index),'y':list(asset['Close'])}
            ],
            'layout': {
                'font': {
                    'color': colors['text']
                }
            }
        }
    )
])





if __name__ == '__main__':
    app.run_server(debug=True)
