import pandas as pd
import psycopg2 as pg
import pandas_datareader as web
import numpy as np
from sklearn.linear_model import LinearRegression
from get_credentials import Connect_Financial_db
import matplotlib.pyplot as plt


#Get stock data from yahoo finance
def get_stock_data(ticker):
    print('getting data ...',ticker)
    try:
        df = web.DataReader(ticker,'yahoo')
        print('Found!')
    except Exception as e:
        print('stock not found in data reader: ',e,ticker)
        df = None
    return df

#get returns from stock to dataframe
def get_returns(stock):
    stock['Returns'] = (stock['Close'] / stock['Close'].shift(1))-1
    print(stock['Returns'])
    return stock

#Perform a linear Regression aka CAPM
def get_LinearRegression(x,y):
    """Performs CAPM model x is the excess return of the NASDAQ index and risk free Tbill 13 weeks 
    and y is the returns of a stock"""
    model = LinearRegression()
    model.fit(x,y)
    r_sq = model.score(x,y)
    alpha = model.intercept_
    Beta = model.coef_
    return (alpha,Beta,r_sq)




if __name__ == "__main__":
    conn = Connect_Financial_db()
    cur = conn.cursor()
    
    df = pd.DataFrame()

    nasdaq = get_returns(nasdaq)
    rf = get_returns(rf)
    df['Excess_Returns'] = nasdaq['Returns'] - rf['Returns']
    df['Risk_free'] = rf['Returns']
    fig,ax = plt.subplots(figsize=(7,7))
    sctr = ax.scatter(x=df.index,y=df['Risk_free'], c=df['Risk_free'], cmap='RdYlGn')
    ax.set_title('Excess returns over time')
    cur.execute('Select close from dailydata where id = 1')
    ListTupl= cur.fetchall()
    X = np.array(ListTupl)

    plt.show()

    cur.close()
    conn.close()


    