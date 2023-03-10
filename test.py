import requests
import csv


#api_key (REPLACE WITH * WHEN UPLOADING TO GITHUB)
api_key = "**********"

#Define API Endpoint URL
url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=AAPL&apikey={api_key}"


#send api request and get response
response = requests.get(url)

#print response
data = response.json()

#convert json to csv
with open('APPLE.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Date', 'Open', 'High', 'Low', 'Close', 'Adjusted Close', 'Volume', 'Dividend Amount', 'Split Coefficient'])
    for date, values in data['Time Series (Daily)'].items():
        row = [date, values['1. open'], values['2. high'], values['3. low'], values['4. close'], values['5. adjusted close'], values['6. volume'], values['7. dividend amount'], values['8. split coefficient']]
        writer.writerow(row)

