import unittest
import numpy as np
from crunch.forecasting.cognitive_load_predictor import CognitiveLoadPredictor  # Replace 'your_module' with the name of the module where the CognitiveLoadPredictor class is defined

class TestCognitiveLoadPredictor(unittest.TestCase):
    """
    Test if the update_and_predict method correctly updates the standardized_data attribute and the current_forecast attribute.
    """
    def test_update_and_predict(self):
        # Sample initial data
        initial_data = np.array([2.72, 2.6, 2.76, 4.44, 4.56, 4.4, 4.16, 4.44, 4.08, 4.48, 4.48, 4.76, 4.56, 4.4, 4.12, 4.0, 4.0, 4.24, 4.04])
        
        # Initialize the CognitiveLoadPredictor with the initial data
        predictor = CognitiveLoadPredictor(initial_data)
        
        # New observation
        new_observation = 3.5
        
        # Update and predict with the new observation
        predictor.update_and_predict(new_observation)
        
        # Check if the standardized_data attribute was updated correctly
        standardized_new_observation = (new_observation - np.mean(initial_data)) / np.std(initial_data)
        np.testing.assert_array_equal(predictor.standardized_data[-1], standardized_new_observation)
        
        # Check if the current_forecast attribute was updated correctly
        self.assertTrue(hasattr(predictor, 'current_forecast'))
        self.assertIsInstance(predictor.current_forecast, np.ndarray)

if __name__ == '__main__':
    unittest.main()
