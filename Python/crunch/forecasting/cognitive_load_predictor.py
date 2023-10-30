import numpy as np
from crunch.forecasting.arma import ARMAClass
from crunch.forecasting.garch import GARCHClass
from crunch.forecasting.plotting import Plotting
import crunch.util as util


class CognitiveLoadPredictor:
    """
    A class to predict cognitive load using the ARIMA model ARIMA(p,d,q).
    Due to stationarity in the data we use ARMA model, which is a special case of ARIMA, where d=0.

    Attributes:
    - data (numpy.array): The array of cognitive load data.
    - p (int): The AR order for the ARIMA model.
    - q (int): The MA order for the ARIMA model.
    - model (ARIMA): The ARIMA model instance.
    - model_fit (ARIMA): The fitted ARIMA model.
    """

    def __init__(self, initial_data):
        """
        Initializes the CognitiveLoadPredictor with initial data.

        Parameters:
        - initial_data (numpy.array): The initial array of cognitive load data.
        """
        self.mean_initial = np.mean(initial_data)
        self.std_initial = np.std(initial_data)
        self.standardized_data = self.standardize(initial_data)

        self.ARMAClass = ARMAClass(self.standardized_data)
        self.GARCHClass = GARCHClass(self.standardized_data)
        self.forecast_matrix = np.zeros(
            (10, 10)
        )  # 10 forecasts, 10 values each. Used for calculating the average forecasted value for each observation.
        self.forecast_counter = 0
        self.average_forecasts = self.standardized_data
        self.errors = []
        self.Plotting = Plotting()

        self.history_used_in_forecasting = int(
            util.config("forecasting", "history_used_in_forecasting")
        )
        self.observations_to_plot = int(
            util.config("forecasting", "observations_to_plot")
        )
        self.forecast_length = int(util.config("forecasting", "forecast_length"))

        self.first_forecast()

    def standardize(self, data):
        """Converts the data to Z-scores"""
        return (data - self.mean_initial) / self.std_initial

    def update_and_predict(self, new_observation):
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
        """Add the forecast to the forecast matrix and compute the mean absolute error.
        Calculate the sum of the first column in the forecast matrix and divide by the number of observations
        After plotting the mean absolute error shift the matrix down and drop the oldest forecast's last value
        Because it's being compared to the actual value

        Args:
            new_value (float: the next actual value
            forecast (np.list): list consisting of the next 10 forecasted values
        """
        # Compute the average forecast for the next time step
        diagonal_sum = np.trace(self.forecast_matrix)
        average_forecast = diagonal_sum / min(
            self.forecast_counter, self.forecast_length
        )  # Use min to handle cases where counter < 10

        # Use the average forecast to compute the error
        error = abs(new_observation - average_forecast)
        self.errors.append(error)

        # Append the average forecast to the averages list
        self.average_forecasts = np.append(self.average_forecasts, average_forecast)

    def first_forecast(self):
        arma_forecast = self.ARMAClass.update_and_predict(
            self.standardized_data[-self.history_used_in_forecasting :]
        )
        garch_forecast = self.GARCHClass.update_and_predict(
            self.ARMAClass.get_residuals()
        )
        self.current_forecast = arma_forecast + garch_forecast
        self.is_outlier = np.any((np.abs(self.current_forecast) >= 2)) or np.abs(
            self.standardized_data[-1] >= 2
        )
        self.forecast_counter += 1
        self.forecast_matrix[0] = self.current_forecast

        self.Plotting.plot(
            self.standardized_data[-self.observations_to_plot :],
            self.average_forecasts[-self.observations_to_plot :],
            self.current_forecast,
            len(self.standardized_data),
        )
