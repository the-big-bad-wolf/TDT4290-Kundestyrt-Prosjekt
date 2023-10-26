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
        self.Plotting = Plotting()
        self.GARCHClass = GARCHClass(self.standardized_data)
        self.items_in_forecasting = int(
            util.config("forecasting", "items_in_forecasting")
        )
        self.observations_to_plot = int(
            util.config("forecasting", "observations_to_plot")
        )

    def standardize(self, data):
        return (data - self.mean_initial) / self.std_initial

    def update_and_predict(self, new_value):
        standardized_value = self.standardize(new_value)
        self.standardized_data = np.append(self.standardized_data, standardized_value)
        arma_forecast = self.ARMAClass.update_and_predict(
            self.standardized_data[-self.items_in_forecasting :]
        )
        garch_forecast = self.GARCHClass.update_and_predict(
            self.ARMAClass.get_residuals()
        )
        # option to use results from ARMA and GARCH separately
        # garch_result = self.mean_initial + standard_deviation_forecast
        # arima_result = forecast
        arima_and_garch_combined_forecast = arma_forecast + garch_forecast

        self.Plotting.plot(
            self.standardized_data[-self.observations_to_plot :],
            arima_and_garch_combined_forecast,
            len(self.standardized_data),
        )
        self.Plotting.backtest(standardized_value, arima_and_garch_combined_forecast)

        is_outlier = np.any((np.abs(arima_and_garch_combined_forecast) >= 2)) or np.abs(
            standardized_value >= 2
        )

        return arima_and_garch_combined_forecast, is_outlier
