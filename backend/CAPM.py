import pandas as pd
import psycopg2 as pg
import pandas_datareader as web
import numpy as np
from sklearn.linear_model import LinearRegression
from get_credentials import Connect_Financial_db


def transform_stock_data(stock):
    stock = list_tuples_toDataFrame(stock,['Date','Close'])
    stock = stock.set_index('Date')
    return stock

#get returns from stock to dataframe
def get_returns(stock):
    stock['Returns'] = (stock['Close'] / stock['Close'].shift(1))-1
    return stock

#Perform a linear Regression aka CAPM
def get_LinearRegression(x,y):
    """Performs CAPM model x is the excess return of the NASDAQ index and risk free Tbill 13 weeks 
    and y is the returns of a stock"""
    model = LinearRegression()
    model.fit(x,y)
    r_sq = model.score(x,y)
    alpha = model.intercept_
    Beta = model.coef_[0] #just one coefficient to return
    return (alpha,Beta,r_sq)

def list_tuples_toDataFrame(list_t,column_header):
    df = pd.DataFrame(list_t,columns = column_header)
    return df

def get_market_excess_returns(market_id,riskfree_id):
    """Returns a dataframe ready to regress on any stock 'i' with the expected returns from the market
    risk free asset and the difference (excess returns) The risk free asset is the 13 week TBill "market index is nasdaq
    Input: market_id to look in database
    riskfree_id to look for in database
    Ouput: pandas dataframe ready for regression"""
    #get the market index
    cur.execute('select day,close::float from dailydata_market where market_id = {}'.format(market_id))
    nasdaq = cur.fetchall()
    nasdaq = list_tuples_toDataFrame(nasdaq,['Date','Close'])
    nasdaq = nasdaq.set_index('Date')
    nasdaq = get_returns(nasdaq)
    #print(nasdaq)
    #Get the risk free asset
    cur.execute('select day,close::float from dailydata_riskfree where riskfree_id = {}'.format(riskfree_id))
    rf = cur.fetchall()
    rf = list_tuples_toDataFrame(rf,['Date','Close'])
    rf = rf.set_index('Date')
    rf = get_returns(rf)
    
    excess = pd.merge(nasdaq,rf,left_index=True,right_index=True)
    excess['Excess_ret'] = excess['Returns_x'] - excess['Returns_y']
    excess.rename({'Returns_x':'Nasdaq_ret','Returns_y':'Riskfree_ret'})
    #print(excess.head(10))
    return excess
    
def preprocessing_for_linearregression(excess,stock):
    """scikit learn only takes numpy arrays prepocess the data and dates from all values to perform linear regression
    vectors need to be same size
    Input: dataframe with nasdaq and 10 year aussie bond
    Output: numpy arrays of same size transormed for Linear regression"""
    print('stock: ',stock.head(10))
    print('excess: ',excess.head(10))
    CAPM_stock = pd.merge(excess,stock,left_index = True,right_index=True) 
    X = CAPM_stock['Excess_ret'].to_numpy().reshape(-1,1) #reshape vectors
    X = np.nan_to_num(x=X,nan=round(CAPM_stock['Excess_ret'].mean(),2)) #get rid of nan values replace with mean of excess return
    Y = CAPM_stock['Returns'].to_numpy()    #transform to numpy array
    Y = np.nan_to_num(x=Y,nan=round(CAPM_stock['Returns'].mean(),2)) #get rid of Nan values replace with mean of stock return
    #print('X: {}'.format(X))
    #print('Y: {}'.format(Y))
    return (X,Y)

def insert_equitiesstats(asset_id,avg_ret,variance):
    cur.execute("""insert into equitiesstats values({},{},{})""".format(asset_id,avg_ret,variance))

def insert_CAPM(asset_id,market_id,alpha,Beta,r_sq):
    cur.execute("""insert into CAPM values({},{},{},{},{})""".format(asset_id,market_id,alpha,Beta,r_sq))



if __name__ == "__main__":
    conn = Connect_Financial_db()
    cur = conn.cursor()
    cur.execute('select count(id) from equities')
    equities, = cur.fetchone()
    market_id = 1
    rf_id = 1
    excess_ret = get_market_excess_returns(market_id,rf_id) #market_id = 1 is NASDAQ, rf_id = 1 is 13 weeks Tbill
    print('Excess returns: \n',excess_ret)
    failed = []
    for asset_id in range (1,equities+1):
        print('Getting stock id: {}'.format(asset_id))
        cur.execute('select day,close::float from dailydata_equities where asset_id = {}'.format(asset_id))
        #returns a list of tuples
        data = cur.fetchall()
        
        #puts all data into dataframe
        print('Transforming stock data ...') 
        stock = transform_stock_data(data)
        
        #gets the return of that stock
        print('Getting stock data returns')
        stock = get_returns(stock)

        #transform data to process data
        print('Preprocessing the data ... ')
        X,Y = preprocessing_for_linearregression(excess_ret,stock)
        
        #get all the estimates from the regression
        print('==== Perform linear regression Results:  ===')
        try:
            alpha,Beta, r_sq = get_LinearRegression(X,Y)
            print('alpha: {}, Beta: {}, r_sq: {},asset_id: {}'.format(alpha,Beta,r_sq,asset_id))
        
            #get the expected return of the stock
            expected_ret = stock['Returns'].mean()
        
            #get the variance of individual stock
            vol = stock['Returns'].var()
            print('e_ret: {}, Var: {}'.format(expected_ret,vol))
            print('==================================')
            insert_equitiesstats(asset_id,expected_ret,vol)
            insert_CAPM(asset_id,market_id,alpha,Beta,r_sq)
        except Exception:
            failed.append(asset_id)
            continue
    print('Failed stockes: ', failed)
    print('All done!..')
    cur.close()
    conn.commit()
    conn.close()


    