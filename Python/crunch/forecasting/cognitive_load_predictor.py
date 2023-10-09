import numpy as np
import warnings
from arma import ARMAClass
from garch import GARCHClass
from plotting import Plotting

# Ignore warnings
# Fryktelig mange warnings fra AIC-estimeringen
warnings.filterwarnings("ignore")


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
        self.raw_data = initial_data
        self.mean_initial = np.mean(initial_data)
        self.std_initial = np.std(initial_data)
        self.standardized_data = self.standardize(initial_data)
        self.ARMAClass = ARMAClass(self.standardized_data)
        self.Plotting = Plotting()
        self.GARCHClass = GARCHClass(self.standardized_data)

    def standardize(self, data):
        return (data - self.mean_initial) / self.std_initial

    def update_and_predict(self, new_value):
        standardized_value = self.standardize(new_value)
        forecast, is_outlier = self.ARMAClass.update_and_predict(standardized_value)
        standard_deviation_forecast = self.GARCHClass.update_and_predict(
            standardized_value
        )
        # option to use results from ARMA and GARCH separately
        # garch_result = self.mean_initial + standard_deviation_forecast
        # arima_result = forecast
        arima_and_garch_combined_forecast = forecast + standard_deviation_forecast
        self.standardized_data = np.append(self.standardized_data, standardized_value)
        self.Plotting.plot(self.standardized_data, arima_and_garch_combined_forecast)

        self.Plotting.backtest(new_value, arima_and_garch_combined_forecast[0])

        return forecast, is_outlier
