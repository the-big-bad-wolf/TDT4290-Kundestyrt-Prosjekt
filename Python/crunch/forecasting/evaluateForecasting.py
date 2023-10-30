import csv
import numpy as np
from arma import ARMAClass
from garch import GARCHClass

class EvaluateForecasting:

    def __init__(self):
        self.arma_forecast_matrix = np.zeros((10, 10))  # Assuming a 10-step forecast
        self.garch_forecast_matrix = np.zeros((10, 10))  # Assuming a 10-step forecast
        self.armagarch_forecast_matrix = np.zeros((10, 10))  # Assuming a 10-step forecast
        self.counter = 0  # To track the number of forecasts

    def standardize(self, data, mean, std):
        return (data - mean) / std
    
    def update_garch_forecast_matrix(self, garch_forecast):
        self.garch_forecast_matrix[1:] = self.garch_forecast_matrix[:-1]
        self.garch_forecast_matrix[0] = garch_forecast
        current_garch_forecast = np.mean(self.garch_forecast_matrix, axis=0)[0]  # Average of the first column
        return current_garch_forecast
    
    def update_armagarch_forecast_matrix(self, armagarch_forecast):
        self.armagarch_forecast_matrix[1:] = self.armagarch_forecast_matrix[:-1]
        self.armagarch_forecast_matrix[0] = armagarch_forecast
        diagonal_sum = np.trace(self.armagarch_forecast_matrix)
        current_armagarch_forecast = diagonal_sum/min(self.counter, 10) # Average of the diagonal
        return current_armagarch_forecast
    
    def update_arma_forecast_matrix(self, arma_forecast):
        # Shift the matrix down and add the new forecast at the top
        self.arma_forecast_matrix[1:] = self.arma_forecast_matrix[:-1]
        self.arma_forecast_matrix[0] = arma_forecast
        diagonal_sum = np.trace(self.arma_forecast_matrix)
        current_arma_forecast = diagonal_sum/min(self.counter, 10)  # Average of the diagonal
        return current_arma_forecast

    def reset_matrices(self):
        self.arma_forecast_matrix = np.zeros((10, 10))
        self.garch_forecast_matrix = np.zeros((10, 10))
        self.armagarch_forecast_matrix = np.zeros((10, 10))
        self.counter = 0

    def read_csv_and_predict(self, file_path):
        # Store results
        results = []

        # Read the entire CSV into a list
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row
            data_list = list(reader)
            

        # Loop through different baseline lengths
        for forecast_length in range(28, 29):  # Adjust range as needed
            # Prepare the baseline data
            baseline_data = [float(row[1]) for row in data_list[:10]]
            baseline_array = np.array(baseline_data)

            # Standardize the baseline data
            mean_initial = np.mean(baseline_array)
            std_initial = np.std(baseline_array)
            standardized_data = self.standardize(baseline_array, mean_initial, std_initial)
            standardized_data.tolist()

           # Loop through different p and q values for the ARMA model
            for p_arma in range(2, 6):
                for q_arma in range(2, 6):
                    
                    # Loop through different p and q values for the GARCH model
                    for p_garch in range(2, 6):
                        for q_garch in range(2, 6):
                            try:
                                print(f"Testing with baseline length: {forecast_length}, p_arma: {p_arma}, q_arma: {q_arma}, p_garch: {p_garch}, q_garch: {q_garch}")
                                arma_model = ARMAClass(standardized_data, p_arma, q_arma)
                                garch_standalone = GARCHClass(standardized_data, p_garch, q_garch)
                                garch_combined = GARCHClass(arma_model.get_residuals(), p_garch, q_garch)

                                # Initialize the MAE lists
                                garch_standalone_maes = []
                                armagarch_combined_maes = []
                                arma_standalone_maes = []

                                # Continue iterating over the data_list and updating the model
                                for row in data_list[forecast_length:]:
                                    self.counter += 1   
                                    time, value = row  
                                    actual_value = float(value)
                                    standardized_value = self.standardize(actual_value, mean_initial, std_initial)

                                    # Update ARMA model with the new data point and generate a forecast
                                    arma_forecast = arma_model.update_and_predict(standardized_value)
                                    avg_arma_standalone_forecast = self.update_arma_forecast_matrix(arma_forecast)
                                    arma_standalone_maes.append(standardized_value - avg_arma_standalone_forecast )
                                    
                                    # Update standalone GARCH model with the new data point and generate a forecast
                                    # garch_forecast = garch_standalone.update_and_predict(standardized_value) # Husk å fjern evaluate fra garch
                                    # garch_standalone_combined_forecast = self.update_garch_forecast_matrix(garch_forecast)
                                    
                                    # Update combined GARCH model with the new data point and generate a forecast
                                    armagarch_combined_forecast = garch_combined.update_and_predict(arma_model.get_residuals())
                                    avg_armagarch_combined_forecast = self.update_armagarch_forecast_matrix(armagarch_combined_forecast)
                                    armagarch_combined_maes.append(standardized_value - avg_armagarch_combined_forecast - avg_arma_standalone_forecast)
                                    
                                self.reset_matrices()  # Reset the matrices for the next iteration
                                
                                # Store the result along with the parameters used
                                print('Appending result')
                                results.append({
                                    'baseline_length': forecast_length,
                                    'p_arma': p_arma,
                                    'q_arma': q_arma,
                                    'p_garch': p_garch,
                                    'q_garch': q_garch,
                                    'ARMA MAE': abs(np.mean(arma_standalone_maes)),
                                    # 'Garch Standalone MAE': abs(garch_standalone_combined_forecast - actual_value),
                                    'ARMA + Garch MAE': abs(np.mean(armagarch_combined_maes)),
                                })
                                print(f"Results for p_arma={p_arma}, q_arma={q_arma}, p_garch={p_garch}, q_garch={q_garch}: {results[-1]}")  # Print the last result
                            except Exception as e:
                                print(f"Error occurred: {e}")
                                continue

            # After all iterations, find the set of parameters with the lowest MAE
            best_arma_result = min(results, key=lambda x: x['ARMA MAE'])
            # best_garch_standalone_result = min(results, key=lambda x: x['Garch Standalone MAE'])
            best_garch_combined_result = min(results, key=lambda x: x['ARMA + Garch MAE'])
            print(f"Best result: {best_arma_result}, {best_garch_combined_result}")
            


# The main execution
if __name__ == "__main__":
    evaluator = EvaluateForecasting()
    file_path = r'C:\Users\MikkelGuttormsen\OneDrive\Documents\NTNU\7. Høst 2023\TDT4290 Kundestyrt prosjekt\TDT4290-Kundestyrt-Prosjekt\Python\cognitive_load.csv'
    evaluator.read_csv_and_predict(file_path)
