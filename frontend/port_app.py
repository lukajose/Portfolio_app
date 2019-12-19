# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from flask import Flask
import pandas_datareader as web
import datetime
import pandas as pd

def get_stock_data(ticker):
    data = web.DataReader(ticker, 'yahoo')
    return data

def get_returns(stock):
    stock['Returns'] = (stock['Close'] / stock['Close'].shift(1))-1
    return stock

def transform_data(df):
    #print('Transforming....\n ',df.head(10))
    df.index = pd.to_datetime(df['Date'])
    df = df.rename(columns={'Price':'Close'})
    df = get_returns(df)
    return df



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
server = Flask(__name__)
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
asset = get_stock_data('TSLA')
df = pd.read_csv('../backend/Aussie_bond.csv') #data from investing.com
auss_bond = transform_data(df) 
colors = {
    'background': '#ffffff',
    'text': '#111111'
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
        id='Portfolio app',
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
    ),
    html.Div(children='Risk Free Asset returns', style={
        'textAlign': 'center',
        'color': colors['text']
    }),
    dcc.Graph(
        id = 'individual_stock',
        figure={
            'data': [
                {'x':list(auss_bond.index),'y':list(auss_bond['Returns'])}
            ],
            'layout': {
                'font': {
                    'color':colors['text']
                }
            }
        }
    )
])




if __name__ == '__main__':
    app.run_server(debug=True)
