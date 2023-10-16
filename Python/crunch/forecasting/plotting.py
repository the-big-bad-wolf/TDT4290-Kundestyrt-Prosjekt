import numpy as np
import matplotlib.pyplot as plt


class Plotting:
    def __init__(self):
        self.old_forecast = None
        self.errors = []
        self.counter = 0
        self.averages = []
        self.forecast_matrix = np.zeros((10, 10))  # 10 forecasts, 10 values each
        self.fig, (self.ax, self.mse_ax) = plt.subplots(2, 1, figsize=(10, 12))
        plt.subplots_adjust(hspace=0.5)
        plt.ion()

    def plot(self, standardized_data, forecast):
        """
        Args:
                new_value (float): newest actual measured value
                forecast (np.ndarray): Array of the next 10 forecasted values
        """
        if not hasattr(self, "fig"):
            self.fig, self.ax = plt.subplots(figsize=(10, 6))
            plt.ion()  # Aktivate interactive mode

        self.ax.clear()  # Reset the plot
        if self.averages == []:
            self.averages = standardized_data.tolist()
        # Only consider the last 30 items
        data_to_plot = standardized_data[-30:]
        averages_to_plot = self.averages[-30:]

        # Plot the data
        self.ax.plot(data_to_plot, label="Observed Value", color="blue")

        # Plot the historical average forecast
        self.ax.plot(
            averages_to_plot,
            label="Average Forecast",
            color="purple",
            linestyle=":",
        )
        # Plot the new value
        self.ax.scatter(
            len(data_to_plot) - 1,
            data_to_plot[-1],
            color="red",
            label="New Value",
        )

        # Adjust the forecast_x_values to start from the current data point
        forecast_x_values = np.arange(
            len(data_to_plot) - 1, len(data_to_plot) + len(forecast)
        )
        forecast_plot = np.append(data_to_plot[-1], forecast)
        self.ax.plot(
            forecast_x_values,
            forecast_plot,
            color="green",
            label="Forecast",
            linestyle="--",
        )
        self.ax.set_ylim(-5, 5)

        self.ax.set_title("Cognitive Load Data and Forecast")
        self.ax.set_xlabel("Number of Observations")
        self.ax.set_ylabel("Z-Score")
        self.ax.legend()
        self.ax.grid(True)

        # Update the x-axis to reflect the actual data points
        actual_x_ticks = np.arange(
            len(standardized_data) - len(data_to_plot), len(standardized_data)
        )
        tick_interval = max(
            1, len(data_to_plot) // 6
        )  # Adjust dynamically based on data length
        self.ax.set_xticks(np.arange(0, len(data_to_plot), tick_interval))
        self.ax.set_xticklabels(actual_x_ticks[::tick_interval])

        plt.draw()  # Update figure
        plt.pause(1)  # Add minor delay to plotting

    def backtest(self, new_value, forecast):
        """Add the forecast to the forecast matrix and compute the MSE.
        Calculate the sum of the first column in the forecast matrix and divide by the number of observations
        After plotting the MSE shift the matrix down and drop the oldest forecast's last value
        Because it's being compared to the actual value

        Args:
            new_value (float: the next actual value
            forecast (np.list): list consisting of the next 10 forecasted values
        """
        # Shift all rows down
        self.forecast_matrix[1:] = self.forecast_matrix[:-1]
        # Add the new forecast to the top row
        self.forecast_matrix[0] = forecast

        # Compute the average forecast for the next time step
        left_column_sum = np.sum(self.forecast_matrix[:, 0])
        average_forecast = left_column_sum / min(self.counter + 1, 10)
        # Use min to handle cases where counter < 10

        # Append the average forecast to the averages list
        self.averages.append(average_forecast)

        # Use the average forecast to compute the squared error
        error = abs(new_value - self.averages[-1])
        self.errors.append(error)
        self._plot_rmse()

        # Increment the counter until the number of predicted steps is reached
        if self.counter < 10:
            self.counter += 1

    def _plot_rmse(self):
        self.mse_ax.clear()

        # Only consider the last 30 RMSE values
        rmse_to_plot = self.errors[-30:]
        x_values = np.arange(len(rmse_to_plot))

        self.mse_ax.plot(x_values, rmse_to_plot, label="Error", color="red")

        self.mse_ax.set_title("Error Over Time")
        self.mse_ax.set_xlabel("Number of Predictions")
        self.mse_ax.set_ylabel("Error")
        self.mse_ax.legend()
        self.mse_ax.grid(True)

        # Update the x-axis to reflect the actual prediction numbers
        actual_x_ticks = np.arange(
            len(self.errors) - len(rmse_to_plot), len(self.errors)
        )
        tick_interval = max(
            1, len(rmse_to_plot) // 6
        )  # Adjust dynamically based on data length
        self.mse_ax.set_xticks(x_values[::tick_interval])
        self.mse_ax.set_xticklabels(actual_x_ticks[::tick_interval])

        plt.draw()
        plt.pause(1)
