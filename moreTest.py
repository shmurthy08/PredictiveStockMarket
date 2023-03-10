import pandas as pd
from sklearn.linear_model import LinearRegression as LR
from sklearn.model_selection import train_test_split as TTS
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, r2_score

#load data
data = pd.read_csv('APPLE.csv')

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
for y in y_pred:
    print("$",y)
    