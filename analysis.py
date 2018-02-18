import pandas as pd
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras import regularizers
import copy
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
import numpy as np
import math

dir = 'D:\\StanfordYearTwo\\Classes\\CS230_Learning\\TimeSeries\\'
dir = '/Users/Yu-Lin/Box Sync/GitHub/treehacks-energy/'
data = pd.read_csv(dir+'time_series2.csv');

data.fillna(12, inplace = True);

usage = data['usage'];
short_rolling = usage.rolling(window=2).mean()

data = usage.values
data = data.astype('float32')
data = data.reshape(len(data),1)


plt.plot(usage);
plt.plot(short_rolling.values)
plt.show()

scaler = MinMaxScaler(feature_range=(0, 1))
unscaled_data = data;
data = scaler.fit_transform(data)

train_size = int(len(data) * 0.9)
test_size = len(data) - train_size
train, test = data[0:train_size, :], data[train_size:len(data), :]
print(len(train), len(test))

# convert an array of values into a dataset matrix
def create_dataset(dataset, look_back=1):
	dataX, dataY = [], []
	for i in range(len(dataset)-look_back-1):
		a = dataset[i:(i+look_back), 0]
		dataX.append(a)
		dataY.append(dataset[i + look_back, 0])
	return np.array(dataX), np.array(dataY)

look_back = 50; #determine look-back using FFT
trainX, trainY = create_dataset(train, look_back)
testX, testY = create_dataset(test, look_back)

# reshape input to be [samples, time steps, features]
trainX = np.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))
testX = np.reshape(testX, (testX.shape[0], 1, testX.shape[1]))

model = Sequential()
model.add(LSTM(4, return_sequences = True, input_shape=(1, look_back)))
model.add(LSTM(10))
#model.add(Dense(4, kernel_regularizer=regularizers.l2(0.01)))
model.add(Dense(1))
model.compile(loss='mean_squared_error', optimizer='adam')
history = model.fit(trainX, trainY, epochs=5, batch_size=200, verbose=True)

# summarize history for loss
print(history.history.keys())
plt.plot(history.history['loss'])
#plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

# make predictions
trainPredict = model.predict(trainX)
testPredict = model.predict(testX)
# invert predictions
trainPredict = scaler.inverse_transform(trainPredict)
trainY = scaler.inverse_transform([trainY])
testPredict = scaler.inverse_transform(testPredict)
testY = scaler.inverse_transform([testY])
# calculate root mean squared error
trainScore = math.sqrt(mean_squared_error(trainY[0], trainPredict[:,0]))
print('Train Score: %.2f RMSE' % (trainScore))
testScore = math.sqrt(mean_squared_error(testY[0], testPredict[:,0]))
print('Test Score: %.2f RMSE' % (testScore))

# shift train predictions for plotting
trainPredictPlot = np.empty_like(data)
trainPredictPlot[:, :] = np.nan
trainPredictPlot[look_back:len(trainPredict)+look_back, :] = trainPredict
# shift test predictions for plotting
testPredictPlot = np.empty_like(data)
testPredictPlot[:, :] = np.nan
testPredictPlot[len(trainPredict)+(look_back*2)+1:len(data)-1, :] = testPredict
# plot baseline and predictions
plt.plot(scaler.inverse_transform(data))
plt.plot(trainPredictPlot)
plt.plot(testPredictPlot)


## error correction
differences = list();
for i in range(len(trainPredict)):
    y_hat = trainPredict[i][0];
    y = unscaled_data[i][0];
    if(y > np.percentile(unscaled_data, 90)): #prox for being in a peak region;
        differences.append(abs(y-y_hat));

#correction = mean of difference;
correction = np.mean(differences);

corrected_predict = copy.copy(trainPredict)
for i in range(len(trainPredict)):
    y_hat = trainPredict[i][0];
    y = unscaled_data[i][0];
    if (y > np.percentile(unscaled_data, 90)):#prox for being in a peak region;
        corrected_predict[i] = y_hat + correction;


trainScore = math.sqrt(mean_squared_error(trainY[0], corrected_predict[:,0]))
print('corrected Train Score: %.2f RMSE' % (trainScore))

# shift train predictions for plotting
trainPredictPlot = np.empty_like(data)
trainPredictPlot[:, :] = np.nan
trainPredictPlot[look_back:len(trainPredict)+look_back, :] = corrected_predict

plt.plot(trainPredictPlot);
plt.show()

#distribution of errors...
plt.hist(differences);
plt.show()

#generate mean corrected predictions of the test

#use the model to generate predictions for the month of January
