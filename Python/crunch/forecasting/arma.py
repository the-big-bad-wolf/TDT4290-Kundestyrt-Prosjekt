import warnings
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from crunch import util


warnings.filterwarnings("ignore")


class ARMAClass:
    def __init__(self, data):
        self.data = data
        self.p, self.q = self.estimate_order()
        self.model = ARIMA(self.data, order=(self.p, 0, self.q))
        self.model_fit = self.model.fit()
        self.counter = 0
        self.items_in_forecasting = int(
            util.config("forecasting", "items_in_forecasting")
        )

    def estimate_order(self):
        """
        Estimates the AR and MA order (p and q) for the ARIMA model based on AIC, Akaike information criterion
        https://en.wikipedia.org/wiki/Akaike_information_criterion
        Returns:
        - tuple: A tuple containing the estimated p and q values.
        """
        best_aic = np.inf
        best_order = None

        for p in range(2, 6):
            for q in range(2, 6):
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

        if self.counter == 41:
            self.counter = 0
            self.estimate_order()
        self.counter += 1
        self.data = np.append(self.data[-self.items_in_forecasting + 1 :], new_value)
        self.model = ARIMA(self.data, order=(self.p, 0, self.q))
        self.model_fit = self.model.fit()

        forecast = self.model_fit.forecast(steps=10)

        return forecast

    def get_residuals(self):
        """
        Retrieve the residuals from the fitted ARIMA model.

        Returns:
        --------
        np.ndarray
            The residuals from the fitted model.
        """
        return self.model_fit.resid
