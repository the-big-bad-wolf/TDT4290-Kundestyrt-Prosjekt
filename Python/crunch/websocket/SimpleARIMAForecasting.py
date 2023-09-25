import numpy as np
from statsmodels.tsa.arima.model import ARIMA


def standardize_data(data_array):
    """
    Standardizes a given 1D-array.

    Parameters:
    - data_array: A 1D numpy array

    Returns:
    - standardized_data: A 1D numpy array with a mean of 0 and a standard deviation of 1
    """
    return (np.mean(data_array)) / np.std(data_array)


def establish_reference(data_array):
    """
    Calculate the average for a given 1D-array.

    Parameters:
    - data_array: A 1D numpy array

    Returns:
    - average: Average of the standardized array
    """
    return np.mean(data_array), np.std(data_array)


def predict_next_direction(data_array, mean, std):
    """
    Predicts the next value and determines its direction (up or down) compared to the reference average.

    Parameters:
    - data_array: A recent 1D numpy array (120 data points each second from the Tobii glasses)
    - reference_avg: A previously calculated average (from the first 15000 data points, est. 2 minutes)

    Returns:
    - direction: "up" or "down" based on the comparison of forecasted value to reference_avg
    """

    z_score_array = (data_array - mean) / std

    model = ARIMA(z_score_array, order=(5, 1, 0))
    model_fit = model.fit()
    forecast = model_fit.forecast(steps=1)[0]
    return (
        True if np.abs(forecast) > 2 else False
    )  # assuming 0 is mean and 2 is 2 std above
