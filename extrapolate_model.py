from keras.models import load_model

def extrapolate(l, model):
    """
    Extrapolates sequence by appending half original length predictions
    """
    n = l.shape[0]

    # if sequence contains a single element, then continue with it
    if len(set(l)) == 1:
        return np.concatenate([l, l[0] * np.ones(int(n / 2))])

    minimum = l.min()
    maximum = l.max()
    # as suggested in paper we apply scaling to [0, 10] range
    l_scaled = (l - minimum) / (maximum - minimum) * 10
    # we have found that interpolation can make significant difference!
    extension = 200 // n + 1     # perform interpolation if necessary
    x = np.linspace(0, 1, n)     # result will be in original scale
    x_extended = np.linspace(0, 1, n * extension)
    f = interp1d(x, l_scaled)
    hist = model.fit(x_extended, f(x_extended), epochs=5, verbose=0)
    # prediction is made for next n/2 steps
    p = model.predict(np.concatenate([x, 1 + np.arange(1, int(n / 2) + 1) * x[1]])).flatten()
    p_scaled = p * (maximum - minimum) / 10 + minimum
    return p_scaled

def parser(x):
    return pd.datetime.strptime(x, '%Y-%m-%d %H:%M:%S')
series = pd.read_csv('new_data.csv', header=0, parse_dates=[0], index_col=0, squeeze=True, date_parser=parser)
X = series.values

model = load_model('nd_model.h5')
