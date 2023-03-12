import numpy as np
from sklearn.linear_model import LinearRegression, SGDRegressor
from sklearn.preprocessing import StandardScaler
from utils.WuEnda.lab_utils_multi import load_house_data
import matplotlib.pyplot as plt

np.set_printoptions(precision=2)
dlblue = '#0096ff'; dlorange = '#FF9300'; dldarkred='#C00000'; dlmagenta='#FF40FF'; dlpurple='#7030A0';
plt.style.use('./utils/WuEnda/deeplearning.mplstyle')


def sgdr():
    # Load the data set
    X_train, y_train = load_house_data()
    X_features = ['size(sqft)', 'bedrooms', 'floors', 'age']

    # Scale/normalize the training data
    scaler = StandardScaler()
    X_norm = scaler.fit_transform(X_train)
    print(f"Peak to Peak range by column in Raw        X:{np.ptp(X_train, axis=0)}")
    print(f"Peak to Peak range by column in Normalized X:{np.ptp(X_norm, axis=0)}")

    # Create and fit the regression model
    sgdr = SGDRegressor(max_iter=1000)
    sgdr.fit(X_norm, y_train)
    print(sgdr)
    print(f"number of iterations completed: {sgdr.n_iter_}, number of weight updates: {sgdr.t_}")

    # View parameters
    b_norm = sgdr.intercept_
    w_norm = sgdr.coef_
    print(f"model parameters:                   w: {w_norm}, b:{b_norm}")

    # make a prediction using sgdr.predict()
    y_pred_sgd = sgdr.predict(X_norm)
    # make a prediction using w,b.
    y_pred = np.dot(X_norm, w_norm) + b_norm
    print(f"prediction using np.dot() and sgdr.predict match: {(y_pred == y_pred_sgd).all()}")
    print(f"Prediction on training set:\n{y_pred[:4]}")
    print(f"Target values \n{y_train[:4]}")

    # plot predictions and targets vs original features
    fig, ax = plt.subplots(1, 4, figsize=(12, 3), sharey=True)
    for i in range(len(ax)):
        ax[i].scatter(X_train[:, i], y_train, label='target')
        ax[i].set_xlabel(X_features[i])
        ax[i].scatter(X_train[:, i], y_pred, color=dlorange, label='predict')
    ax[0].set_ylabel("Price")
    ax[0].legend()
    fig.suptitle("target versus prediction using z-score normalized model")
    plt.show()


def linear_regression():
    """Linear Regression, closed-form solution"""

    # load the dataset
    X_train, y_train = load_house_data()
    X_features = ['size(sqft)', 'bedrooms', 'floors', 'age']

    linear_model = LinearRegression()
    linear_model.fit(X_train, y_train)

    b = linear_model.intercept_
    w = linear_model.coef_
    print(f"w = {w:}, b = {b:0.2f}")

    print(f"Prediction on training set:\n {linear_model.predict(X_train)[:4]}")
    print(f"prediction using w,b:\n {(X_train @ w + b)[:4]}")
    print(f"Target values \n {y_train[:4]}")

    x_house = np.array([1200, 3, 1, 40]).reshape(-1, 4)
    x_house_predict = linear_model.predict(x_house)[0]
    print(f" predicted price of a house with 1200 sqft,"
          f"3 bedrooms, 1 floor, 40 years old = ${x_house_predict * 1000:0.2f}")
