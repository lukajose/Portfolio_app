import psycopg2 as pg

def get_credentials():
    File = open('credentials.txt','r')
    passw = File.readline()
    return passw

def Connect_Financial_db():
    passw = get_credentials()
    conn = pg.connect(
            host="localhost",
            user="postgres",
            password=passw,
            database = "financial_db"
        )
    return conn
