import psycopg2 as pg
import pandas_datareader as web
import json
import time
from get_credentials import get_credentials,Connect_Financial_db

def insert_asset(stock,id,found_stock):
    print('Inserting asset: ',stock,'id: ',id)
    try:
            if found_stock:
                query = 'insert into Equities values({},'.format(id) + "'" + stock + "'"
                query += ",'"+ 'stock'+"'," 'True)'
                cur.execute(query)
            else:
                query = 'insert into Equities values({},'.format(id) + "'" + stock + "'"
                query += ",'"+ 'stock'+"'," 'False)'
                cur.execute(query)
    except Exception as e:
        print('Couldnt update Asset table: ',e)

def insert_hasdaily(stock,id):
        print('Inserting has daily: ',stock,' id: ',id)
        try:
            time_now = time.time() #save time in epoch
            cur.execute("""insert into hasdaily values({},'{}','{}')""".format(id,time_now,time_now))
        except Exception as e:
            print('Couldnt update Relation hasDaily table: ',e)

def insert_dailydata(df,stock,id):
    print('inserting dailydata: {}'.format(stock))
    for index,row in df.iterrows():
        date = str(index)[:10]
        try:
            cur.execute("""insert into dailydata_equities values ('{}',{},{},{},{},{},{},{})""".format(
                date,
                id,
                row['High'],
                row['Low'],
                row['Open'],
                row['Close'],
                row['Volume'],
                row['Adj Close']
                )
            )
        except Exception as e:
            print('Inserting daily data failed!: ',e)
            continue

def insert_dailydata_riskFree(df,stock,id):
    print('inserting dailydata_riskfree: {}'.format(stock))
    for index,row in df.iterrows():
        date = str(index)[:10]
        try:
            cur.execute("""insert into dailydata_riskfree values ('{}',{},{},{},{},{},{},{})""".format(
                date,
                id,
                row['High'],
                row['Low'],
                row['Open'],
                row['Close'],
                row['Volume'],
                row['Adj Close']
                )
            )
        except Exception as e:
            print('Inserting daily data failed!: ',e)
            continue

def insert_dailydata_market(df,stock,id):
    print('inserting dailydata_riskfree: {}'.format(stock))
    for index,row in df.iterrows():
        date = str(index)[:10]
        try:
            cur.execute("""insert into dailydata_market values ('{}',{},{},{},{},{},{},{})""".format(
                date,
                id,
                row['High'],
                row['Low'],
                row['Open'],
                row['Close'],
                row['Volume'],
                row['Adj Close']
                )
            )
        except Exception as e:
            print('Inserting daily data failed!: ',e)
            continue

def insert_RiskFree(id,ticker,description,country):
    try:
        cur.execute("""insert into RiskFree values({},'{}','{}','{}')""".format(id,ticker,description,country))
    except Exception as e:
        print('Failed to insert risk free data: ',e)

def insert_market(id,ticker,name,country):
    try:
        cur.execute("""insert into Market values({},'{}','{}','{}')""".format(id,ticker,name,country))
    except Exception as e:
        print('Failed to insert market data: ',e)


def get_stock_data(ticker):
    print('getting data ...',ticker)
    try:
        df = web.DataReader(ticker,'yahoo')
        print('Found!')
    except Exception as e:
        print('stock not found in data reader: ',e,ticker)
        df = None
    return df


if __name__ == "__main__":
    #========== DB postgresql ==================
    conn = Connect_Financial_db()
    cur = conn.cursor()

    file = open('ticker_text.json','r')
    tickers = json.load(file)
    #print(tickers)
    file.close()
    stock_id = 1
    for key in tickers.keys():
        #check_emergency_commit()
        for stock in tickers[key]:
            df = get_stock_data(stock)
            if df is None:
                insert_asset(stock,stock_id,False)
                stock_id += 1
                continue
            else:
                insert_asset(stock,stock_id,True)
                insert_hasdaily(stock,stock_id)
                insert_dailydata(df,stock,stock_id)
                stock_id += 1
            print('next faster! ..')

    #Stocks done get 1 risk free asset for now and 1 market NASDAQ
    rf = get_stock_data('^IRX')
    nasdaq = get_stock_data('^IXIC')
    insert_market(1,'^IXIC','NASDAQ','USA')
    insert_RiskFree(1,'^IRX','13 Week Treasury Tbill','AUSTRALIA')
    insert_dailydata_riskFree(rf,'^IRX',1)
    insert_dailydata_market(nasdaq,'^IXIC',1)


    cur.close()
    conn.commit()
    conn.close()