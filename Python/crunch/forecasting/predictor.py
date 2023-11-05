import numpy as np
from crunch.forecasting.arma import ARMAClass
from crunch.forecasting.garch import GARCHClass
from crunch.forecasting.plotting import Plotting
import crunch.util as util


class Predictor:
    """
    A class to predict future values using the ARIMA model ARIMA(p,d,q).
    Due to stationarity in the data we use ARMA model, which is a special case of ARIMA, where d=0.

    Attributes:
    - standardized_data (numpy.array): Standardized array of data.
    - self.mean_initial the mean of the initial data
    - self.std_initial the standard deviation of the initial data
    - self.forecast_matrix (numpy.array): A matrix of the last 10 forecasts used to calculate an average forecast for each observation.
    - self.forecast_counter (int): A counter used to keep track of the number of forecasts made so we can divide by the correct number of forecasts to calculate the average forecast for the [forecast_length] first observations.
    - self.average_forecasts (numpy.array): An array of the average forecasts for each observation.
    - self.errors (numpy.array): An array of the errors for each observation.
    - self.Plotting (Plotting): An instance of the Plotting class.
    - self.history_used_in_forecasting (int): The number of historical observations used to calculate the forecast.
    - self.observations_to_plot (int): The number of observations to plot.
    - self.forecast_length (int): How far into the future to forecast.
    - ARMAClass: The ARIMA model instance.
    - GARCHClass: The Garch model instance.

    """

    def __init__(self, baseline_data):
        """
        Initializes the Predictor with initial data.

        Parameters:
        - baseline_data (numpy.array): The initial array of data used to calculate a baseline.
        """
        self.history_used_in_forecasting = int(
            util.config("forecasting", "history_used_in_forecasting")
        )
        self.observations_to_plot = int(
            util.config("forecasting", "observations_to_plot")
        )
        self.forecast_length = int(util.config("forecasting", "forecast_length"))

        self.mean_initial = np.mean(baseline_data)
        self.std_initial = np.std(baseline_data)
        self.standardized_data = self.standardize(baseline_data)

        self.ARMAClass = ARMAClass(
            self.standardized_data, forecast_length=self.forecast_length
        )
        self.GARCHClass = GARCHClass(
            self.ARMAClass.get_residuals(), forecast_length=self.forecast_length
        )

        self.forecast_matrix = np.zeros(
            (self.forecast_length, self.forecast_length)
        )  # Used for calculating the average forecasted value for each observation so we can calculate an error between forecasted value and observed value.

        self.forecast_counter = 0
        self.average_forecasts = self.standardized_data
        self.errors = []

        self.Plotting = Plotting()

        self.first_forecast()

    def standardize(self, data):
        """Converts the data to Z-scores"""
        return (data - self.mean_initial) / self.std_initial

    def update_and_predict(self, new_observation):
        """Updates the forecast with a new observation and plots the results."""
        standardized_value = self.standardize(new_observation)
        self.standardized_data = np.append(self.standardized_data, standardized_value)

        arma_forecast = self.ARMAClass.update_and_predict(
            self.standardized_data[-self.history_used_in_forecasting :]
        )
        garch_forecast = self.GARCHClass.update_and_predict(
            self.ARMAClass.get_residuals()
        )
        self.current_forecast = arma_forecast + garch_forecast
        self.is_outlier = np.any((np.abs(self.current_forecast) >= 2)) or np.abs(
            standardized_value >= 2
        )
        self.forecast_counter += 1

        # Calculate the error
        self.backtest(standardized_value)

        # Shift all rows down
        self.forecast_matrix[1:] = self.forecast_matrix[:-1]
        # Add the new forecast to the top row
        self.forecast_matrix[0] = self.current_forecast

        self.Plotting.plot(
            self.standardized_data[-self.observations_to_plot :],
            self.average_forecasts[-self.observations_to_plot :],
            self.current_forecast,
            len(self.standardized_data),
        )
        self.Plotting.plot_error(
            self.errors[-self.observations_to_plot :], len(self.standardized_data)
        )

    def backtest(self, new_observation):
        """Compute the average absolute error.
        Calculate the sum of the diagonal in the forecast matrix and divide by the number of forecasts made. The last value in the last row corresponds to the same observation as the first value in the first row.
        Args:
            new_observation (float: the newly observed value
        """
        # Compute the average forecast for the newly observed value
        diagonal_sum = np.trace(self.forecast_matrix)
        average_forecast = diagonal_sum / min(
            self.forecast_counter, self.forecast_length
        )  # Use min to handle cases where counter < forecast_length

        # Use the average forecast to compute the error and append to error list.
        error = abs(new_observation - average_forecast)
        self.errors.append(error)

        # Append the average forecast to the averages list
        self.average_forecasts = np.append(self.average_forecasts, average_forecast)

    def first_forecast(self):
        """Function to make the first forecast. This is done separately because we don't have any historical forecasts to calculate or plot error."""
        arma_forecast = self.ARMAClass.update_and_predict(
            self.standardized_data[-self.history_used_in_forecasting :]
        )
        garch_forecast = self.GARCHClass.update_and_predict(
            self.ARMAClass.get_residuals()
        )
        # Final forecast is the ARMA forecast plus the GARCH forecast on the residuals from the ARMA model.
        self.current_forecast = arma_forecast + garch_forecast

        # Set is_outlier to True if the measured value or any forecasted value is more than 2 standard deviations away from the mean.
        self.is_outlier = np.any((np.abs(self.current_forecast) >= 2)) or np.abs(
            self.standardized_data[-1] >= 2
        )
        self.forecast_counter += 1
        # Add the new forecast to the top row
        self.forecast_matrix[0] = self.current_forecast

        self.Plotting.plot(
            self.standardized_data[-self.observations_to_plot :],
            self.average_forecasts[-self.observations_to_plot :],
            self.current_forecast,
            len(self.standardized_data),
        )
