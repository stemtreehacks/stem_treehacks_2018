from pandas import read_csv
from pandas import datetime
from matplotlib import pyplot
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error
from dateutil.parser import parse
import numpy as np
import csv
import cvxpy as cvx
import matplotlib.pyplot as plt
import pandas as pd

series = read_csv('data.csv', header=0, parse_dates=[0], index_col=0, squeeze=True, date_parser=parse)

before = -1.0
after = -1.0
df = pd.DataFrame(series)
iterator = df.iterrows()
i = 0

while i < df.shape[0]:
  if(np.isnan(df.iloc[i].values).any() and np.isnan(df.iloc[i+1].values).any()):
    df = df.drop(df.index[i])
    i += 1
  elif(np.isnan(df.iloc[i].values).any()):
    df.set_value(i, 0, (df.iloc[i-1].values[0] + df.iloc[i+1].values[0])/2.0, takeable=True)
    i += 1
  else:
    i += 1

df = df.dropna(axis=0, how='any')
X = df.values
print X.size
dates = df.axes[0].tolist()
jan_date = 0
for i in xrange(len(dates)):
  if (dates[i].strftime('%m-%d-%Y').startswith('02')):
    jan_date = i
    break

print jan_date

train = X
history = [x for x in train]
predictions = list()
test = X[0:jan_date]

np.save(open('history_2.npz', 'wb'), history)

for t in range(len(test)):
  model = ARIMA(history, order=(5,1,0))
  model_fit = model.fit(disp=0)
  output = model_fit.forecast()
  yhat = output[0]
  predictions.append(yhat)
  obs = test[t]
  history.append(obs)
  print('predicted=%f, expected=%f' % (yhat, obs))
  if (t % 50 == 0):
    print float(t)/len(test)

error = mean_squared_error(test, predictions)
print('Test MSE: %.3f' % error)
# plot
np.save(open('data_1_prediction.npz', 'wb'), predictions)
pyplot.plot(test)
pyplot.plot(predictions, color='red')
pyplot.show()