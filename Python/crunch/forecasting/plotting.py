import numpy as np
import matplotlib.pyplot as plt

from crunch import util


class Plotting:
    def __init__(self):
        self.errors = []
        self.forecast_averages = []
        self.forecast_matrix = np.zeros((10, 10))  # 10 forecasts, 10 values each
        self.counter = 0
        self.fig, (self.ax, self.mse_ax) = plt.subplots(2, 1, figsize=(10, 12))
        self.nr_observations_to_plot = int(
            util.config("forecasting", "observations_to_plot")
        )
        self.baseline_items = int(util.config("websocket", "baseline_items"))

        plt.subplots_adjust(hspace=0.5)
        plt.ion()

    def plot(self, data, forecast, observation_length):
        """
        Args:
                new_value (float): newest actual measured value
                forecast (np.ndarray): Array of the next 10 forecasted values
        """

        self.ax.clear()  # Reset the plot
        if self.forecast_averages == []:
            self.forecast_averages = data.tolist()
        # Only consider the last 30 items
        averages_to_plot = self.forecast_averages[-len(data) :]

        # Plot the data
        self.ax.plot(data, label="Observed Value", color="blue")

        # Plot the historical average forecast
        self.ax.plot(
            averages_to_plot,
            label="Average Forecast",
            color="purple",
            linestyle=":",
        )
        # Plot the new value
        self.ax.scatter(
            len(data) - 1,
            data[-1],
            color="red",
            label="New Value",
        )

        # Adjust the forecast_x_values to start from the current data point
        forecast_x_values = np.arange(len(data) - 1, len(data) + len(forecast))
        forecast = np.append(data[-1], forecast)
        self.ax.plot(
            forecast_x_values,
            forecast,
            color="green",
            label="Forecast",
            linestyle="--",
        )
        self.ax.set_ylim(-5, 5)

        self.ax.set_title("Cognitive Load Data and Forecast")
        self.ax.set_xlabel("Observation Nr.")
        self.ax.set_ylabel("Z-Score")
        self.ax.legend()
        self.ax.grid(True)

        # Update the x-axis to reflect the actual data points
        actual_x_ticks = np.arange(
            observation_length - len(data) + 1, observation_length + 1
        )
        tick_interval = 1  # Adjust dynamically based on data length
        self.ax.set_xticks(np.arange(0, len(data), tick_interval))
        self.ax.set_xticklabels(actual_x_ticks[::tick_interval])

        plt.draw()  # Update figure
        plt.pause(0.5)  # Add minor delay to plotting

    def backtest(self, new_value, forecast):
        """Add the forecast to the forecast matrix and compute the mean absolute error.
        Calculate the sum of the first column in the forecast matrix and divide by the number of observations
        After plotting the mean absolute error shift the matrix down and drop the oldest forecast's last value
        Because it's being compared to the actual value

        Args:
            new_value (float: the next actual value
            forecast (np.list): list consisting of the next 10 forecasted values
        """

        # Compute the average forecast for the next time step
        left_column_sum = np.trace(self.forecast_matrix)
        average_forecast = left_column_sum / min(self.counter + 1, 10)
        # Use min to handle cases where counter < 10

        # Append the average forecast to the averages list
        self.forecast_averages.append(average_forecast)

        # Use the average forecast to compute the squared error
        error = abs(new_value - self.forecast_averages[-1])
        self.errors.append(error)
        self.plot_error()

        # Increment the counter until the number of predicted steps is reached
        if self.counter < 10:
            self.counter += 1
        # Shift all rows down
        self.forecast_matrix[1:] = self.forecast_matrix[:-1]
        # Add the new forecast to the top row
        self.forecast_matrix[0] = forecast

    def plot_error(self):
        self.mse_ax.clear()

        # Only consider the last 30 error values
        errors_to_plot = self.errors[-self.nr_observations_to_plot :]
        x_values = np.arange(len(errors_to_plot))

        self.mse_ax.plot(x_values, errors_to_plot, label="Error", color="red")

        self.mse_ax.set_title("Absolute Error Over Time")
        self.mse_ax.set_xlabel("Observation Nr.")
        self.mse_ax.set_ylabel("Absolute Error")
        self.mse_ax.legend()
        self.mse_ax.grid(True)

        # Update the x-axis to reflect the actual prediction numbers
        actual_x_ticks = np.arange(
            len(self.errors) - len(errors_to_plot) + self.baseline_items + 1,
            len(self.errors) + self.baseline_items + 1,
        )
        tick_interval = 1
        self.mse_ax.set_xticks(x_values[::tick_interval])
        self.mse_ax.set_xticklabels(actual_x_ticks[::tick_interval])

        plt.draw()
        plt.pause(1)
