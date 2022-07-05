from ast import Str, Try
import json
from sqlite3 import Date
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, null
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from model import Coins
from requests import Request, Session
from datetime import datetime
import pandas as pd

def check_if_valid_data(df: pd.DataFrame) -> bool:
    
    # Check if dataframe is empty
    if df.empty:
        print("\nDataframe empty. Finishing execution")
        return False 

    # Check for nulls
    if df.symbol.empty:
        raise Exception("\nSymbol is Null or the value is empty")
 
     # Check for nulls
    if df.price.empty:
        raise Exception("\nPrice is Null or the value is empty")

    # Check for nulls
    if df.data_added.empty:
        raise Exception("\nData is Null or the value is empty")

    return True
    
def load_data(table_name, coins_df, session_db, engine_db):
    
    # validate
    if check_if_valid_data(coins_df):
        print("\nData valid, proceed to Load stage")
    
    # load data on database
    try:
        coins_df.to_sql(table_name, engine_db, index=False, if_exists='append')
        print ('\nData Loaded on Database')

    except:
        print("\nFail to load data on database")

    session_db.commit()
    session_db.close()
    print("\nClose database successfully")
    return session_db

def get_data(session_db, engine_db, start, limit, convert, key, url):
    
    # set limit of data from api
    parameters = {
        'start': start,
        'limit': limit,
        'convert': convert
    }

    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': key,
    }

    session = Session()
    session.headers.update(headers)

    name = []
    symbol = []
    data_added = []
    last_updated = []
    price = []
    volume_24h = []

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)

        print ('\n')
        for coin in data['data']:
            name.append(coin['name'])
            symbol.append(coin['symbol'])
            data_added.append(coin['date_added'])
            last_updated.append(coin['last_updated'])
            price.append(coin['quote']['USD']['price'])
            volume_24h.append(coin['quote']['USD']['volume_24h'])

        # Prepare a dictionary in order to turn it into a pandas dataframe below       
        coin_dict = {
            "name" : name,
            "symbol": symbol,
            "data_added" : data_added,
            "last_updated" : last_updated,
            "price": price,
            "volume_24h": volume_24h
        }
    except:
        print ('Error to get data from APi')
        exit(1)
    
    # create dataframe to structure data
    coins_df = pd.DataFrame(coin_dict, columns = ["name", "symbol", "data_added", "last_updated","price","volume_24h"])
    print ("Data on Pandas Dataframe:\n")
    print(coins_df.head())
    
    # call the function to load data on database
    load_data('Coins',coins_df, session_db, engine_db)

# Declaration base
Base = declarative_base()

# Make the coin table
get_session_db, get_engine = Coins.start()

# call the get_data function and load data on database
get_data(get_session_db,
         get_engine,
         '1',
         '500',
         'USD',
         '7bdc01a6-f004-4c0b-b21c-1c1d3970352f',
         'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest')