import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import acf, pacf
import warnings
import matplotlib.pyplot as plt

# Ignore warnings
# Fryktelig mange warnings fra AIC-estimeringen
warnings.filterwarnings("ignore")


class CognitiveLoadPredictor:
    """
    A class to predict cognitive load using the ARIMA model ARIMA(p,d,q).
    Due to stationarity in the data we use ARMA model, which is a special case of ARIMA, where d=0.

    Attributes:
    - data (numpy.array): The array of cognitive load data.
    - reference_median (float): The median value from the initial data.
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
        self.data = self._standardize_data(initial_data)
        self.reference_median = np.median(self.data)
        self.p, self.q = self._estimate_order()
        self.model = ARIMA(self.data, order=(self.p, 0, self.q))
        self.model_fit = self.model.fit()

    def _standardize_data(self, data):
        """Standardizes the data."""
        return (data - self.mean_initial) / self.std_initial

    def _estimate_order(self):
        """
        Estimates the AR and MA order (p and q) for the ARIMA model based on AIC, Akaike information criterion
        https://en.wikipedia.org/wiki/Akaike_information_criterion
        Returns:
        - tuple: A tuple containing the estimated p and q values.
        """
        best_aic = float("inf")
        best_order = None

        max_p = 5
        max_q = 5

        for p in range(max_p + 1):
            for q in range(max_q + 1):
                try:
                    model = ARIMA(self.data, order=(p, 0, q))
                    model_fit = model.fit()
                    aic = model_fit.aic
                    if aic < best_aic:
                        best_aic = aic
                        best_order = (p, q)
                except:
                    continue
        print(f"Best order: {best_order}")
        return best_order

    def update_and_predict(self, new_value):
        """
        Updates the model with a new cognitive load value and predicts the next value.

        Parameters:
        - new_value (float): The new cognitive load value.

        Returns:
        - tuple: The forecasted cognitive load value and a boolean indicating if the forecasted value is more than 2 standard deviations from the reference median.
        """
        self.raw_data = np.append(self.raw_data[1:], new_value)
        self.data = self._standardize_data(self.raw_data)
        self.model = ARIMA(self.data, order=(self.p, 0, self.q))
        self.model_fit = self.model.fit()

        forecast = self.model_fit.forecast(steps=1)[0]
        print(f"Forecast: {forecast}")
        print(f"Reference median: {self.reference_median}")
        is_outlier = np.abs(forecast - self.reference_median) > 2
        self._plot_data_and_forecast(new_value, forecast)
        return forecast, is_outlier

    def _plot_data_and_forecast(self, new_value, forecast):
        """
        TODO sjekk om denne oppdateres

        Args:
            new_value (_type_): _description_
            forecast (_type_): _description_
        """
        if not hasattr(self, "fig"):
            self.fig, self.ax = plt.subplots(figsize=(10, 6))
            plt.ion()  # Aktiver interaktiv modus

        self.ax.clear()  # Fjern tidligere plott

        # Plot the data
        self.ax.plot(self.data, label="Data", color="blue")

        # Plot the new value
        self.ax.scatter(
            len(self.data) - 1, self.data[-1], color="red", label="New Value"
        )

        # Plot the forecast
        self.ax.scatter(len(self.data), forecast, color="green", label="Forecast")

        self.ax.set_title("Cognitive Load Data and Forecast")
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Standardized Value")
        self.ax.legend()
        self.ax.grid(True)

        plt.draw()  # Oppdater figuren
        plt.pause(0.1)  # Legg til en liten forsinkelse


# # For testing
# initial_data = 2 + 2 * np.random.rand(
#     120
# )  # Dette vil gi deg 120 tilfeldige verdier mellom 2 og 4
# predictor = CognitiveLoadPredictor(initial_data)

# # When a new value becomes available:
# new_value = 11
# print(f"New value: {new_value}")
# forecast, is_outlier = predictor.update_and_predict(new_value)
# new_value = 8
# forecast, is_outlier = predictor.update_and_predict(new_value)
# new_value = 15
# forecast, is_outlier = predictor.update_and_predict(new_value)
# print(f"Forecasted value: {forecast}")
# print(f"Is outlier: {is_outlier}")
# print(f"Reference median: {predictor.reference_median}")
# print(f"Reference mean: {predictor.mean_initial}")


# plt.show(block=True)  # ikke nødvendig når den kjører live:)
