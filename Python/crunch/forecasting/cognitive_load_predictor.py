import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import acf, pacf
import warnings
import matplotlib.pyplot as plt
from crunch.forecasting.arma import ARMAClass
from crunch.forecasting.plotting import Plotting

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
		self.ARMAClass= ARMAClass(self.standardized_data)
		self.Plotting = Plotting()


	def standardize(self, data):
		return (data-self.mean_initial)/self.std_initial

	def update_and_predict(self, new_value):
		standardized_value=self.standardize(new_value)
		forecast, is_outlier = self.ARMAClass.update_and_predict(standardized_value)
		self.standardized_data=np.append(self.standardized_data,standardized_value)
		self.Plotting.plot(self.standardized_data,forecast)

		self.Plotting.backtest(new_value, forecast[0])

		return forecast, is_outlier

