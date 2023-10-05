import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import acf, pacf
import warnings
import matplotlib.pyplot as plt

# Ignore warnings
# Fryktelig mange warnings fra AIC-estimeringen
warnings.filterwarnings("ignore")


class ARMAClass:



    def __init__(self,data):
        self.data=data
        self.p,self.q=self._estimate_order()
        self.model = ARIMA(self.data, order=(self.p, 0, self.q))
        self.model_fit = self.model.fit()
        self.old_forecast=None
        
        

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

        for p in range(2,max_p + 1):
            for q in range(2,max_q + 1):
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

        self.data = np.append(self.data[1:], new_value)
        self.model = ARIMA(self.data, order=(self.p, 0, self.q))
        self.model_fit = self.model.fit()

        forecast = self.model_fit.forecast(steps=10)
        is_outlier = np.any((np.abs(forecast) >= 2))

        return forecast, is_outlier