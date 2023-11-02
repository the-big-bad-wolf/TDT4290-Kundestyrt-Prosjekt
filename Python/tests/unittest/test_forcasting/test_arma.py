import unittest
import numpy as np
from crunch.forecasting.arma import ARMAClass

class TestARMAClass(unittest.TestCase):
    """
    Unit test class for ARMAClass
    """

    def test_estimate_order(self):
        """
        Test that the estimate_order method returns integers p and q 
        in the correct range [2, 5].
        """
        data = np.random.rand(100)
        armaclass = ARMAClass(data)
        p, q = armaclass.estimate_order(data)
        self.assertTrue(2 <= p <= 5)
        self.assertTrue(2 <= q <= 5)

    def test_update_and_predict(self):
        """
        Test that the update_and_predict method returns a list of 
        forecasts of the correct length.
        """
        data = np.random.rand(100)
        armaclass = ARMAClass(data)
        history = np.random.rand(80)
        forecast = armaclass.update_and_predict(history)
        self.assertEqual(len(forecast), 10)

    def test_get_residuals(self):
        """
        Test that the get_residuals method returns a list of residuals 
        of the correct length.
        """
        data = np.random.rand(100)
        armaclass = ARMAClass(data)
        residuals = armaclass.get_residuals()
        self.assertEqual(len(residuals), len(data))

if __name__ == '__main__':
    unittest.main()
