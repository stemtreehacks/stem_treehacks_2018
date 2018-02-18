# based on neural decompsition from https://github.com/rokastamosiunas/neural_decomposition

import matplotlib.pyplot as plt
import seaborn
import numpy as np
import pandas as pd
from keras.models import Input, Model, Sequential
from keras.layers.core import Dense
from keras.layers.merge import Concatenate
from keras.layers import LSTM, Activation
from keras import regularizers
from scipy.interpolate import interp1d
from keras import backend as K

plt.rcParams['figure.figsize'] = [12.0, 8.0]
def parser(x):
        return pd.datetime.strptime(x, '%Y-%m-%d %H:%M:%S')
series = pd.read_csv('new_data.csv', header=0, parse_dates=[0], index_col=0, squeeze=True, date_parser=parser)
X = series.values

def create_model(n, units=10, noise=0.001):
    """
    Constructs neural decomposition model and returns it
    """
    data = Input(shape=(1,), name='time')
    # sin will not work on TensorFlow backend, use Theano instead
    sinusoid = Dense(n, activation=K.sin, name='sin')(data)
    linear = Dense(units, activation='linear', name='linear')(data)
    softplus = Dense(units, activation='softplus', name='softplus')(data)
    sigmoid = Dense(units, activation='sigmoid', name='sigmoid')(data)
    combined = Concatenate(name='combined')([sinusoid, linear, softplus, sigmoid])
    out = Dense(1, kernel_regularizer=regularizers.l1(0.01), name='output')(combined)

    model = Model(inputs=[data], outputs=[out])    
    model.compile(loss="mse", optimizer="adam")

    K.set_value(model.weights[0],(2*np.pi*np.floor(np.arange(n)/2))[np.newaxis,:].astype('float32'))
    K.set_value(model.weights[1],(np.pi/2+np.arange(n)%2*np.pi/2).astype('float32'))
    K.set_value(model.weights[2],(np.ones(shape=(1,units)) + np.random.normal(size=(1,units))*noise).astype('float32'))
    K.set_value(model.weights[3],(np.random.normal(size=(units))*noise).astype('float32'))
    K.set_value(model.weights[4],(np.random.normal(size=(1,units))*noise).astype('float32'))
    K.set_value(model.weights[5],(np.random.normal(size=(units))*noise).astype('float32'))
    K.set_value(model.weights[6],(np.random.normal(size=(1,units))*noise).astype('float32'))
    K.set_value(model.weights[7],(np.random.normal(size=(units))*noise).astype('float32'))
    K.set_value(model.weights[8],(np.random.normal(size=(n+3*units,1))*noise).astype('float32'))
    K.set_value(model.weights[9],(np.random.normal(size=(1))*noise).astype('float32'))

    return model

model = create_model(len(X))
t = np.linspace(0, 1, len(X))
hist = model.fit(t, X, epochs=100)
#plt.plot(hist.history['loss']) 

prediction = model.predict(np.linspace(0, 2, 31 * 24 * 4 * 13)).flatten()
#print(prediction)
for j in np.nditer(prediction, op_flags=['readwrite']):
    if j < 0:
        j[...] = 0
model.save('nd_model.h5')
opfile = open("predictions.txt", "w")
opfile.write(str([x for x in prediction]))
opfile.close()
#plt.plot(prediction, color='blue')
#plt.plot(X, color='red')
#plt.show()

