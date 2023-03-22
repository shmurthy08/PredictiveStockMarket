import pandas as pd
from sklearn.linear_model import LinearRegression as LR
from sklearn.model_selection import train_test_split as TTS
from sklearn.preprocessing import StandardScaler
import requests


def get_user_input():
    stockName = input("Enter the name of stock(s) that you want to predict: ")
    parseStocks = [s.strip() for s in stockName.split(' ')]
    gather_stock_info(parseStocks)



def gather_stock_info(parseStocks: list):
    
    #api_key (REPLACE WITH * WHEN UPLOADING TO GITHUB)
    my_api_key = "******"

    for i in parseStocks:
        
        #Define API Endpoint URL
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={i}&apikey={my_api_key}"
        
        #send api request and get response
        response = requests.get(url)
        
        #load response
        data = response.json()
        df = pd.DataFrame.from_dict(data['Time Series (Daily)'], orient='index')
        df.reset_index(inplace=True)
        df.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Adjusted Close', 'Volume', 'Dividend Amount', 'Split Coefficient']
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.sort_values('Date')
        df.set_index('Date', inplace=True)
        
        #load data    
        print(df)
        