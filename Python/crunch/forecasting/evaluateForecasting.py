import csv
import numpy as np
from arma import ARMAClass
from garch import GARCHClass
from plotting import Plotting

class EvaluateForecasting:

    def __init__(self):
        self.plotting = Plotting()
        self.forecast_matrix = np.zeros((10, 10))  # Assuming a 10-step forecast
        self.counter = 0  # To track the number of forecasts

    def standardize(self, data, mean, std):
        return (data - mean) / std
    
    def update_forecast_matrix(self, forecast):
        # Shift the matrix down and add the new forecast at the top
        self.forecast_matrix[1:] = self.forecast_matrix[:-1]
        self.forecast_matrix[0] = forecast

        # Calculate the average forecast for the current step
        current_forecast = np.mean(self.forecast_matrix, axis=0)[0]  # Average of the first column
        return current_forecast

    def calculate_mae(self, actual, predicted):
        return np.mean(np.abs(predicted - actual))

    def read_csv_and_predict(self, file_path):
        # Store results
        results = []

        # Loop through different baseline lengths
        for baseline_length in range(30, 35):  # Adjust range as needed
            with open(file_path, 'r') as file:
                reader = csv.reader(file)
                header = next(reader)  # Skip the header row

                # Prepare the baseline data
                baseline_data = [float(next(reader)[1]) for _ in range(baseline_length)]
                baseline_array = np.array(baseline_data)

                # Standardize the baseline data (if you're using this approach)
                mean_initial = np.mean(baseline_array)
                std_initial = np.std(baseline_array)
                standardized_data = self.standardize(baseline_array, mean_initial, std_initial)

                # Loop through different p and q values for the models
                for p in range(2, 6):
                    for q in range(2, 6):
                        try:
                            print(f"Testing with baseline length: {baseline_length}, p: {p}, q: {q}")

                            # Initialize ARMA model with current p and q
                            arma_model = ARMAClass(standardized_data.tolist(), p, q)  # Convert np.array to list

                            actual_values = []
                            # You don't need to store ARMA predictions here, as the model will handle this

                            # Continue reading the file and updating the model
                            for line in reader:
                                time, value = line  
                                actual_value = float(value)
                                standardized_value = self.standardize(actual_value, mean_initial, std_initial)

                                actual_values.append(actual_value)

                                # Update ARMA model with the new data point and generate a forecast
                                forecast = arma_model.update_and_predict(standardized_value)
                                combined_forecast  = self.update_forecast_matrix(forecast)
                            
                            # After all data points are processed, we perform backtesting
                            # backtest_results = arma_model.backtest(actual_values)

                            # Store the result along with the parameters used
                            results.append({
                                'baseline_length': baseline_length,
                                'p': p,
                                'q': q,
                                'ARMA MAE': combined_forecast['MAE'],  # Extract MAE from backtest results
                                # ... (similar for other metrics or models if you're using them)
                            })
                            print(f"Results for p={p}, q={q}: {results[-1]}")  # Print the last result
                        except Exception as e:
                            print(f"Error occurred: {e}")
                            continue
            # After all iterations, find the set of parameters with the lowest MAE
            best_result = min(results, key=lambda x: x['ARMA MAE'])
            print(f"Best result: {best_result}")

# The main execution
if __name__ == "__main__":
    evaluator = EvaluateForecasting()
    file_path = r'C:\Users\MikkelGuttormsen\OneDrive\Documents\NTNU\7. Høst 2023\TDT4290 Kundestyrt prosjekt\TDT4290-Kundestyrt-Prosjekt\Python\crunch\forecasting\cognitive_load.csv'
    evaluator.read_csv_and_predict(file_path)
