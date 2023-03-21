import pandas as pd
from sklearn.linear_model import LinearRegression as LR
from sklearn.model_selection import train_test_split as TTS
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
import requests
import csv
import os



def get_user_input():
    stockName = input("Enter the name of stock(s) that you want to predict: ")
    parseStocks = [s.strip() for s in stockName.split(',')]
    gather_stock_info(parseStocks)



def gather_stock_info(parseStocks: list):
    #api_key (REPLACE WITH * WHEN UPLOADING TO GITHUB)
    my_api_key = "*******"

    for i in parseStocks:
        #Define API Endpoint URL
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={i}&apikey={my_api_key}"
        
        #send api request and get response
        response = requests.get(url)
        #load response
        data = response.json()
        
        if os.path.isfile(f'{i}.csv'):
            with open(f'{i}.csv', 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Date', 'Open', 'High', 'Low', 'Close', 'Adjusted Close', 'Volume', 'Dividend Amount', 'Split Coefficient'])
                for date, values in data['Time Series (Daily)'].items():
                    row = [date, values['1. open'], values['2. high'], values['3. low'], values['4. close'], values['5. adjusted close'], values['6. volume'], values['7. dividend amount'], values['8. split coefficient']]
                    writer.writerow(row)
        else:
            with open(f'{i}.csv', 'x', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Date', 'Open', 'High', 'Low', 'Close', 'Adjusted Close', 'Volume', 'Dividend Amount', 'Split Coefficient'])
                for date, values in data['Time Series (Daily)'].items():
                    row = [date, values['1. open'], values['2. high'], values['3. low'], values['4. close'], values['5. adjusted close'], values['6. volume'], values['7. dividend amount'], values['8. split coefficient']]
                    writer.writerow(row)
                    
        #load data    
        data = pd.read_csv(f'{i}.csv')
        predictData(data)



def predictData(data):    
    #TTS the model
    train_data, test_data = TTS(data, test_size=0.2)

    #define features
    X_train = train_data[['Open', 'High', 'Low', 'Close', 'Volume']]
    y_train = train_data[['Adjusted Close']]
    X_test = test_data[['Open', 'High', 'Low', 'Close', 'Volume']]

    #fit and train lr model
    lr = LR()
    z = StandardScaler()
    #zscore variables 
    z.fit_transform(X_train)
    z.transform(X_test)

    lr.fit(X_train, y_train)

    y_pred = lr.predict(X_test)
    y_pred = [round(i[0],2) for i in y_pred]
    
    #Print all the values predicted
    ans = []
    for y in y_pred:
        ans.append(f"${y}")
        # print("$",y, sep="")    
        #Calculate R-squared score
    r2 = r2_score(test_data['Adjusted Close'], y_pred)
    
    #Calculate MSE
    mse = mean_squared_error(test_data['Adjusted Close'], y_pred)
    print(f"R2 score: {r2}")
    print(f"MSE: {mse}")
    print(ans) 

    
    
def main():
    get_user_input()

if __name__ == '__main__':
    main()
