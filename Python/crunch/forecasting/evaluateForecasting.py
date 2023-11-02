import csv
import numpy as np
from arma import ARMAClass
from garch import GARCHClass

class EvaluateForecasting:

    def __init__(self):
        """
        Initializes the ForecastModel with matrices to store ARMA, GARCH, and combined ARMA-GARCH forecasts,
        as well as a counter to track the number of forecasts made.
        Each forecast matrix is initialized to a 10x10 zero matrix, which assumes a 10-step forecast horizon.
        """
        self.arma_forecast_matrix = np.zeros((10, 10))  # Assuming a 10-step forecast
        self.garch_forecast_matrix = np.zeros((10, 10))  # Assuming a 10-step forecast
        self.armagarch_forecast_matrix = np.zeros((10, 10))  # Assuming a 10-step forecast
        self.counter = 0  # To track the number of forecasts

    def standardize(self, data, mean, std):
        """
        Standardizes the given data using the provided mean and standard deviation.

        Parameters:
        - data: The data to be standardized.
        - mean: The mean to be used for standardization.
        - std: The standard deviation to be used for standardization.

        Returns:
        - The standardized data.
        """
        return (data - mean) / std
    
    def update_armagarch_forecast_matrix(self, armagarch_forecast):
        """
        Updates the ARMA-GARCH forecast matrix with a new forecast, shifting the existing forecasts down one position,
        and computes the current ARMA-GARCH forecast as the average of the diagonal values of the matrix.

        This method assumes that the forecast matrix is updated at each time step with a new forecast,
        and that the diagonal represents the sum of the most recent forecast for each step.

        Parameters:
        - armagarch_forecast: A 1D array or list representing the new ARMA-GARCH forecast to be added to the matrix.

        Returns:
        - float: The current ARMA-GARCH forecast, which is computed as the average of the diagonal of the forecast matrix.
        """
        self.armagarch_forecast_matrix[1:] = self.armagarch_forecast_matrix[:-1] # Shift the matrix down and add the new forecast at the top
        self.armagarch_forecast_matrix[0] = armagarch_forecast # Add the new forecast at the top
        diagonal_sum = np.trace(self.armagarch_forecast_matrix) # Sum of the diagonal
        current_armagarch_forecast = diagonal_sum/min(self.counter, 10) # Average of the diagonal
        return current_armagarch_forecast
    
    def update_arma_forecast_matrix(self, arma_forecast):
        """
        Updates the ARMA forecast matrix with a new forecast, shifting the existing forecasts down one position,
        and computes the current ARMA forecast as the average of the diagonal values of the matrix.

        This method assumes that the forecast matrix is updated at each time step with a new forecast,
        and that the diagonal represents the sum of the most recent forecast for each step.

        Parameters:
        - arma_forecast: A 1D array or list representing the new ARMA forecast to be added to the matrix.

        Returns:
        - float: The current ARMA forecast, which is computed as the average of the diagonal of the forecast matrix.
        """
        self.arma_forecast_matrix[1:] = self.arma_forecast_matrix[:-1] # Shift the matrix down 
        self.arma_forecast_matrix[0] = arma_forecast # Add the new forecast at the top
        diagonal_sum = np.trace(self.arma_forecast_matrix) # Sum of the diagonal
        current_arma_forecast = diagonal_sum/min(self.counter, 10)  # Average of the diagonal
        return current_arma_forecast

    def reset_matrices(self):
        """
        Resets the ARMA, GARCH, and ARMA-GARCH forecast matrices and the counter to their initial state,
        effectively clearing all stored forecasts and count.

        This method is useful when starting a new set of forecasts or when the existing forecasts are no longer relevant.
        """
        self.arma_forecast_matrix = np.zeros((10, 10))
        self.garch_forecast_matrix = np.zeros((10, 10))
        self.armagarch_forecast_matrix = np.zeros((10, 10))
        self.counter = 0

    def read_csv_and_predict(self, file_path):
        """
        Reads a CSV file containing cognitivte load time series data from a user. and performs forecasting using ARMA and GARCH models.
        It loops over different baseline lengths and ARMA model parameters, computes the mean absolute error (MAE)
        for the forecasts, and finds the best parameters based on the lowest MAE.

        Parameters:
        - file_path: A string representing the path to the CSV file containing the data.
                     The CSV is expected to have a header, with the first column being timestamps and the second column being the values to forecast.

        Side Effects:
        - Prints the progress and results of the forecasting to the console.
        - Resets the forecast matrices after each full pass of parameter testing using the `reset_matrices` method.

        Returns:
        - A tuple containing two dictionaries:
            1. The best ARMA model parameters and their corresponding MAE.
            2. The best combined ARMA+GARCH model parameters and their corresponding MAE.
        """
        # Store results
        results = []

        # Read the entire CSV into a list
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row
            data_list = list(reader)
            

        # Loop through different baseline lengths
        for forecast_length in range(10, 35): 
            # Prepare the baseline data
            baseline_data = [float(row[1]) for row in data_list[:10]]
            baseline_array = np.array(baseline_data)

            # Standardize the baseline data
            mean_initial = np.mean(baseline_array)
            std_initial = np.std(baseline_array)
            standardized_data = self.standardize(baseline_array, mean_initial, std_initial)
            standardized_data.tolist()

           # Loop through different p and q values for the ARMA model
            for p in range(2, 6):
                for q in range(2, 6):
                            try:
                                print(f"Testing with baseline length: {forecast_length}, p: {p}, q: {q}")
                                arma_model = ARMAClass(standardized_data, p, q)
                                arma_garch_model = GARCHClass(arma_model.get_residuals(), p, q)

                                # Initialize the MAE lists
                                armagarch_combined_maes = []
                                arma_standalone_maes = []

                                # Continue iterating over the data_list and updating the model
                                for row in data_list[forecast_length:100]:
                                    self.counter += 1   
                                    time, value = row  
                                    actual_value = float(value)
                                    standardized_value = self.standardize(actual_value, mean_initial, std_initial)

                                    # Update ARMA model with the new data point and generate a forecast
                                    arma_forecast = arma_model.update_and_predict(standardized_value)
                                    avg_arma_standalone_forecast = self.update_arma_forecast_matrix(arma_forecast)
                                    arma_standalone_maes.append(standardized_value - avg_arma_standalone_forecast )
                                    
                                    # Update combined GARCH model with the new data point and generate a forecast
                                    armagarch_combined_forecast = arma_garch_model.update_and_predict(arma_model.get_residuals())
                                    avg_armagarch_combined_forecast = self.update_armagarch_forecast_matrix(armagarch_combined_forecast)
                                    armagarch_combined_maes.append(standardized_value - avg_armagarch_combined_forecast - avg_arma_standalone_forecast)
                                    
                                self.reset_matrices()  # Reset the matrices for the next iteration
                                
                                # Store the result along with the parameters used
                                results.append({
                                    'baseline_length': forecast_length,
                                    'p_arma': p,
                                    'q_arma': q,
                                    'ARMA MAE': abs(np.mean(arma_standalone_maes)),
                                    'ARMA + Garch MAE': abs(np.mean(armagarch_combined_maes)),
                                })
                                print(f"Results for p_arma={p}, q_arma={q}, {results[-1]}")  # Print the latest result
                            except Exception as e:
                                print(f"Error occurred: {e}")
                                continue

            # After all iterations, find the set of parameters with the lowest MAE
            best_arma_result = min(results, key=lambda x: x['ARMA MAE'])
            best_garch_combined_result = min(results, key=lambda x: x['ARMA + Garch MAE'])
            print(f"Best result: {best_arma_result}, {best_garch_combined_result}")
            return best_arma_result, best_garch_combined_result

            


# The main execution
if __name__ == "__main__":
    evaluator = EvaluateForecasting()
    file_path = 'cognitive_load.csv'
    best_arma_result, best_garch_combined_result = evaluator.read_csv_and_predict(file_path)
