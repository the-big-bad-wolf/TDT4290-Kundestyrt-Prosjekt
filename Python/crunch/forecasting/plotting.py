import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import acf, pacf
import warnings
import matplotlib.pyplot as plt
from crunch.forecasting.arma import ARMAClass

class Plotting:
	def __init__(self):
		self.old_forecast=None
		self.squared_errors=[]
		self.MSEs=[]
		self.fig, (self.ax, self.mse_ax) = plt.subplots(2, 1, figsize=(10, 12))
		plt.ion()
		
	def plot(self, standardized_data, forecast):
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
		self.ax.plot(standardized_data, label="Data", color="blue")

		# Plot the new value
		self.ax.scatter(
			len(standardized_data) - 1, standardized_data[-1], color="red", label="New Value"
		)

		# Plot the forecast
		forecast_x_values = np.arange(len(standardized_data), len(standardized_data) + len(forecast))     
		self.ax.plot(forecast_x_values, forecast, color="green", label="Forecast", linestyle='--')
		self.ax.set_ylim(-5,5)

		self.ax.set_title("Cognitive Load Data and Forecast")
		self.ax.set_xlabel("Time")
		self.ax.set_ylabel("Standardized Value")
		self.ax.legend()
		self.ax.grid(True)

		plt.draw()  # Oppdater figuren
		plt.pause(1)  # Legg til en liten forsinkelse'

	def backtest(self,new_value,forecast):
		if self.old_forecast==None:
			self.old_forecast=new_value
			return
		squared_error=(new_value-self.old_forecast)**2
		self.old_forecast=forecast
		self.squared_errors.append(squared_error)
		MSE=np.mean(self.squared_errors)/len(self.squared_errors)
		self.MSEs.append(MSE)
		self._plot_mse()

	def _plot_mse(self):         
		self.mse_ax.clear()
		self.mse_ax.plot(self.MSEs, label="MSE", color="red")

		self.mse_ax.set_title("Mean Squared Error Over Time")
		self.mse_ax.set_xlabel("Number of Predictions")
		self.mse_ax.set_ylabel("MSE")
		self.mse_ax.legend()
		self.mse_ax.grid(True)
		plt.draw()
		plt.pause(1)