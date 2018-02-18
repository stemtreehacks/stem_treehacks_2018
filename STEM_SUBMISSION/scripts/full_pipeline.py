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
import sys
import pandas as pd

series = read_csv('data_2.csv', header=0, parse_dates=[0], index_col=0, squeeze=True, date_parser=parse)

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


predictions = np.load("data_2_prediction.npz")

print 'Computing optimization'
X = np.array(predictions).T
n = X.size

max_kw = 150
max_kwh = 250
lam = 0.0001

jan = np.matrix(np.array(X[0:n])).T


t = cvx.Variable(1, 1)
z = cvx.Variable(n, 1)
energy_above_cutoff = cvx.Variable(n, 1)

obj = cvx.Minimize(t - lam*sum(z))

constrs = []
ones = np.matrix(np.ones([n,1]))

for j in range(1, n):
  constrs += [energy_above_cutoff[j] == jan[j-1] - t]
  constrs += [z[j] <= max_kwh]
  constrs += [z[j] >= max_kwh / 2.]
  constrs += [z[j] <= z[j-1] - energy_above_cutoff[j-1]]
  constrs += [cvx.abs(z[j] - z[j-1]) < max_kw]


constrs += [z[0] == max_kwh]
print 'Computed constraints'
prob = cvx.Problem(obj, constrs)
print 'Solving...'
result = prob.solve()

print result
line = [result] * n
plt.figure(1)
plt.subplot(211)
plt.plot(X.T)
plt.plot(line, color='red')
plt.subplot(212)
plt.plot(z.value, color='green')
plt.ylim(0, 300)
plt.show()
z_list = np.array(z.value).flatten().tolist()
X = X.T
with open('battery.csv', 'wb') as csvfile:
  for i in range(len(z_list)):
    csvfile.write(str(dates[i]) + "," + str(X[i].flatten()[0])+","+str(z_list[i])+'\n')