import warnings
import numpy as np
from statsmodels.tsa.arima.model import ARIMA


warnings.filterwarnings("ignore")


class ARMAClass:
    def __init__(self, data , p=None, q=None, baseline_length=28):
        self.p = p
        self.q = q

        # If p or q is None, estimate the order of the model
        if self.p is None or self.q is None:
            self.p, self.q = self.estimate_order(data, baseline_length)

        self.model = ARIMA(data, order=(self.p, 0, self.q))
        self.model_fit = self.model.fit()
        self.counter = 0

    def estimate_order(self, history):
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
                    model = ARIMA(history, order=(p, 0, q))
                    model_fit = model.fit()
                    aic = model_fit.aic
                    if aic < best_aic:
                        best_aic = aic
                        best_order = (p, q)
                except:
                    continue
        print(f"Best order: {best_order}")
        return best_order

    def update_and_predict(self, history):
        """
        Updates the model with a new cognitive load value and predicts the next value.

        Parameters:
        - history (np.list): The historical values used to make forecast.

        Returns:
        - forecast: The array of forecasted cognitive load values.
        """

        if self.counter == 41:
            self.counter = 0
            self.estimate_order(history)
        self.counter += 1
        self.model = ARIMA(history, order=(self.p, 0, self.q))
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

