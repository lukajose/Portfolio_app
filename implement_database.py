import psycopg2 as pg
import pandas_datareader as web
import json
import time


def insert_asset(stock,id):
    print('Inserting asset: ',stock,'id: ',id)
    try:
        query = 'insert into Asset values({},'.format(id) + "'" + stock + "'"
        query += ",'"+ 'stock'+"'," 'True)'
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
            cur.execute("""insert into dailydata values ('{}',{},{},{},{},{},{},{})""".format(
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
        
def get_stock_data(ticker):
    print('getting data ...',ticker)
    try:
        df = web.DataReader(stock_test,'yahoo')
        print('Found!')
    except Exception as e:
        print('stock not found in data reader: ',e,stock_test)
        df = None
    return df


if __name__ == "__main__":
    #========== DB postgresql ==================
    conn = pg.connect(
            host="localhost",
            user="postgres",
            password= "Mayo199515??",
            database = "financial_db"
        )
    cur = conn.cursor()
    # execute a statement
    print('PostgreSQL database version:')
    try:
        cur.execute('SELECT version()')
    except Exception as e:
        print('Couldnt connect to db: ',e)
    # display the PostgreSQL database server version
    db_version = cur.fetchone()
    print(db_version)

    file = open('ticker_text.json','r')
    tickers = json.load(file)
    #print(tickers)
    file.close()
    for key in tickers.keys():
        for stock in tickers[key]:
            df = web.DataReader(stock)
            cur.execute('insert into Asset()')"""
    stock_id = 1

    df = get_stock_data(stock_test)
    insert_asset(stock_test,stock_id)
    insert_hasdaily(stock_test,stock_id)
    if df is not None:
        insert_dailydata(df,stock_test,stock_id)   
    else:
        print('Skipping stock') 


    cur.close()
    conn.commit()
    conn.close()