import warnings
import numpy as np
from statsmodels.tsa.arima.model import ARIMA


warnings.filterwarnings("ignore")


class ARMAClass:
    def __init__(self, history, p=None, q=None, forecast_length=10):
        self.forecast_length = forecast_length

        # If p or q is None, estimate the order of the model
        if p is None or q is None:
            self.p, self.q = self.estimate_order(history)
        else:
            self.p = p
            self.q = q

        self.model = ARIMA(history, order=(self.p, 0, self.q))
        self.model_fit = self.model.fit()
        # Counter used to re-estimate p and q every 41st iteration
        self.counter = 0

    def estimate_order(self, history):
        """
        Estimates the AR and MA order (p and q) for the ARIMA model based on AIC, Akaike information criterion
        https://en.wikipedia.org/wiki/Akaike_information_criterion
        Returns:
        - tuple: Best order (p, q) based on AIC.
        """
        best_aic = np.inf
        best_order = None

        for p in range(2, 6):
            for q in range(2, 6):
                try:
                    model = ARIMA(history, order=(p, 0, q))
                    model_fit = model.fit()
                    aic = model_fit.aic
                    if aic < best_aic:
                        best_aic = aic
                        best_order = (p, q)
                except:
                    continue
        print(f"Best order ARMA: {best_order}")
        return best_order

    def update_and_predict(self, history):
        """
        Make forecast of next [forecast_length] observations based on history.

        Parameters:
        - history (np.list): The historical values used to make forecast.

        Returns:
        - forecast: The array of forecasted cognitive load values.
        """

        if self.counter == 41:
            self.counter = 0
            self.estimate_order(history)
        self.counter += 1
        model = ARIMA(history, order=(self.p, 0, self.q))
        self.model_fit = model.fit()

        forecast = self.model_fit.forecast(steps=self.forecast_length)
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
