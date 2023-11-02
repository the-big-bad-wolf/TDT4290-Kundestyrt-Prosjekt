import numpy as np
from arch import arch_model


class GARCHClass:
    """
    GARCH Model for standard deviation forecasting.

    Attributes:
    -----------
    data : np.ndarray
        Time series data.
    p : int
        Lag order for the autoregressive component.
    q : int
        Lag order for the moving average component.
    model : arch_model
        GARCH model instance.
    model_fit : ARCHModelResult
        Fitted GARCH model.
    """

    def __init__(self, residuals, p=3,q=5):
        """
        Initialize the GARCH model.

        Parameters:
        -----------
        data : np.ndarray
            Standardized time series data.
        """
        self.residuals = residuals
        self.p, self.q = self.estimate_order()
        self.model = arch_model(
            self.residuals, vol="Garch", p=self.p, q=self.q, rescale=False
        )
        self.model_fit = self.model.fit(disp="off")
        self.counter = 0

    def estimate_order(self):
        """
        Estimate the order (p, q) for the GARCH model based on AIC.

        Returns:
        --------
        tuple
            Best order (p, q) based on AIC.
        """
        best_aic = np.inf
        best_order = None

        for p in range(2, 6):
            for q in range(2, 6):
                model = arch_model(self.residuals, vol="Garch", p=p, q=q, rescale=False)
                results = model.fit(disp="off")
                if results.aic < best_aic:
                    best_aic = results.aic
                    best_order = (p, q)

        return best_order

    def update_and_predict(self, residuals):
        """
        Update the model with a new observation and forecast the next value's volatility.

        Parameters:
        -----------
        new_data : float
            New observation.

        Returns:
        --------
        - Float: Forecasted standard diviation for the next period.
        """
        if self.counter == 41:
            self.counter = 0
            self.estimate_order()
        self.counter += 1
        self.residuals = residuals
        self.model = arch_model(
            self.residuals, vol="Garch", p=self.p, q=self.q, rescale=False
        )
        self.model_fit = self.model.fit(disp="off")

        forecasts = self.model_fit.forecast(horizon=10)

        return forecasts.mean["h.01"].iloc[-1]
