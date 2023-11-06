import numpy as np
from arch import arch_model


class GARCHClass:
    """
    GARCH Model for standard deviation forecasting.

    Attributes:
    -----------
    p : int
        Lag order for the autoregressive component.
    q : int
        Lag order for the moving average component.
    """

    def __init__(self, history, p=None, q=None, forecast_length=10):
        """
        Initialize the GARCH model.

        Parameters:
        -----------
        residuals : np.ndarray
            residuals from the ARMA model.
        """
        self.forecast_length = forecast_length

        # If p or q is None, estimate the order of the model
        if p is None or q is None:
            self.p, self.q = self.estimate_order(history)
        else:
            self.p = p
            self.q = q

        # Counter used to re-estimate p and q every 41st iteration
        self.counter = 0

    def estimate_order(self, history):
        """
        Estimate the order (p, q) for the GARCH model based on AIC, Akaike information criterion
        https://en.wikipedia.org/wiki/Akaike_information_criterion

        Returns:
        --------
        - tuple: Best order (p, q) based on AIC.
        """
        best_aic = np.inf
        best_order = None

        for p in range(2, 6):
            for q in range(2, 6):
                model = arch_model(history, vol="Garch", p=p, q=q, rescale=False)
                model_fit = model.fit(disp="off")
                if model_fit.aic < best_aic:
                    best_aic = model_fit.aic
                    best_order = (p, q)
        print(f"Best order GARCH: {best_order}")
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
        model = arch_model(history, vol="Garch", p=self.p, q=self.q, rescale=False)
        model_fit = model.fit(disp="off")

        forecasts = model_fit.forecast(horizon=self.forecast_length)
        return forecasts.mean["h.01"].iloc[-1]
