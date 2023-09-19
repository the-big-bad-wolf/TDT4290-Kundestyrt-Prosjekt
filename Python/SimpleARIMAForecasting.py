import numpy as np
from statsmodels.tsa.arima.model import ARIMA


def establish_reference(data_array):
    """
    Calculate the average for a given 1D-array.

    Parameters:
    - data_array: A 1D numpy array

    Returns:
    - average: Average of the array
    """
    return np.mean(data_array)


def predict_next_direction(data_array, reference_avg):
    """
    Predicts the next value and determines its direction (up or down) compared to the reference average.

    Parameters:
    - data_array: A recent 1D numpy array (90 data points each second from the Tobii glasses)
    - reference_avg: A previously calculated average (from the first 10,800 data points)

    Returns:
    - direction: "up" or "down" based on the comparison of forecasted value to reference_avg
    """
    model = ARIMA(data_array, order=(5, 1, 0))
    model_fit = model.fit()
    forecast = model_fit.forecast(steps=1)[0]

    return "up" if forecast > reference_avg else "down"
