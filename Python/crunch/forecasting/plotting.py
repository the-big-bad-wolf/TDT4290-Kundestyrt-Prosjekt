import numpy as np
import matplotlib.pyplot as plt


class Plotting:
    def __init__(self):
        self.old_forecast = None
        self.squared_errors = []
        self.RMSEs = []
        self.counter = 0
        self.averages = []
        self.forecast_matrix = np.zeros((10, 10))  # 10 forecasts, 10 values each
        self.fig, (self.ax, self.mse_ax) = plt.subplots(2, 1, figsize=(10, 12))
        plt.ion()

    def plot(self, standardized_data, forecast):
        """
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

        # Plot the historical average forecast
        self.ax.plot(
            self.averages, label="Average Forecast", color="purple", linestyle=":"
        )
        # Plot the new value
        self.ax.scatter(
            len(standardized_data) - 1,
            standardized_data[-1],
            color="red",
            label="New Value",
        )

        # Plot the forecast
        forecast_x_values = np.arange(
            len(standardized_data) - 1, len(standardized_data) + len(forecast) - 1
        )
        self.ax.plot(
            forecast_x_values, forecast, color="green", label="Forecast", linestyle="--"
        )
        self.ax.set_ylim(-5, 5)

        self.ax.set_title("Cognitive Load Data and Forecast")
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Standardized Value")
        self.ax.legend()
        self.ax.grid(True)

        plt.draw()  # Oppdater figuren
        plt.pause(1)  # Legg til en liten forsinkelse'

    def backtest(self, new_value, forecast):
        """Add the forecast to the forecast matrix and compute the MSE.
        Calculate the sum of the first column in the forecast matrix and divide by the number of observations
        After plotting the MSE shift the matrix left and drop the oldest forecast's first value
        Because it's beeing compared to the actual value

        Args:
            new_value (float: the next actual value
            forecast (np.list): list consisting of the next 10 forecasted values
        """
        if self.old_forecast == None:
            self.forecast_matrix[
                -1
            ] = forecast  # Add the first forecast to the last row
            self.old_forecast = new_value
            self.counter += 1
            return

        # Compute the average forecast for the next time step
        left_column_sum = np.sum(self.forecast_matrix[:, 0])
        average_forecast = (
            left_column_sum / self.counter
        )  # divide on the number of observations

        # Append the average forecast to the averages list
        self.averages.append(average_forecast)

        # Use the average forecast to compute the squared error
        squared_error = (new_value - average_forecast) ** 2
        self.squared_errors.append(squared_error)
        RMSE = np.sqrt(np.mean(self.squared_errors))
        self.RMSEs.append(RMSE)
        self._plot_rmse()

        # Shift the forecasts left and drop the oldest forecast's first value
        self.forecast_matrix[:, :-1] = self.forecast_matrix[:, 1:]
        # Add the new forecast to the last row
        self.forecast_matrix[-1] = forecast

        # Increment the counter until the number of predicted steps is reached
        if self.counter < 10:
            self.counter += 1

    def _plot_rmse(self):
        self.mse_ax.clear()
        self.mse_ax.plot(self.RMSEs, label="MSE", color="red")

        self.mse_ax.set_title("Root Mean Squared Error Over Time")
        self.mse_ax.set_xlabel("Number of Predictions")
        self.mse_ax.set_ylabel("RMSE")
        self.mse_ax.legend()
        self.mse_ax.grid(True)
        plt.draw()
        plt.pause(1)


def generate_mock_data(start_value, num_points, noise_scale):
    """Generate mock data with some noise."""
    return np.cumsum(np.random.randn(num_points) * noise_scale + start_value)


def generate_mock_forecast(current_value, num_points, noise_scale):
    """Generate mock forecast data based on the current value."""
    return current_value + np.cumsum(np.random.randn(num_points) * noise_scale)


if __name__ == "__main__":
    num_data_points = 100
    noise_scale = 0.5
    start_value = 0

    # Generate initial mock data
    data = generate_mock_data(start_value, num_data_points, noise_scale)

    plotter = Plotting()

    # Simulate the input of new forecast values
    for i in range(num_data_points - 10):
        new_value = data[i]
        forecast = generate_mock_forecast(new_value, 10, noise_scale)
        plotter.backtest(new_value, forecast)
        plotter.plot(data[: i + 1], forecast)

    plt.show()
