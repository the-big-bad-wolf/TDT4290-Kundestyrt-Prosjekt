import numpy as np
import matplotlib.pyplot as plt

from crunch import util


class Plotting:
    def __init__(self):
        self.fig, (self.ax, self.mse_ax) = plt.subplots(2, 1, figsize=(10, 12))
        plt.subplots_adjust(hspace=0.5)
        plt.ion()

        self.nr_observations_to_plot = int(
            util.config("forecasting", "observations_to_plot")
        )
        self.baseline_items = int(util.config("websocket", "baseline_items"))

    def plot(self, data, average_forecasts, forecast, observation_length):
        """
        Args:
                new_value (float): newest actual measured value
                forecast (np.ndarray): Array of the next 10 forecasted values
        """
        # Reset the plot
        self.ax.clear()

        # Plot the data
        self.ax.plot(data, label="Observed Value", color="blue")

        forecast_history_x_values = np.arange(len(average_forecasts))
        # Plot the historical average forecast
        self.ax.plot(
            forecast_history_x_values,
            average_forecasts,
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
        self.ax.set_ylim(-2, 2)

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

    def plot_error(self, errors, observation_length):
        self.mse_ax.clear()

        # Only consider the last 30 error values
        x_values = np.arange(len(errors)) + 1

        self.mse_ax.plot(x_values, errors, label="Error", color="red")

        self.mse_ax.set_title("Absolute Error Over Time")
        self.mse_ax.set_xlabel("Observation Nr.")
        self.mse_ax.set_ylabel("Absolute Error")
        self.mse_ax.legend()
        self.mse_ax.grid(True)

        plt.draw()
        plt.pause(0.5)
