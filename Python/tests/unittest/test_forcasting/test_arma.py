import unittest
import numpy as np
from crunch.forecasting.arma import ARMAClass


class TestARMAClass(unittest.TestCase):
    """
    Unit test class for ARMAClass.

    """

    def test_estimate_order(self):
        """
        Test the estimate_order method.

        estimate_order should determine the optimal order (p, q) for the ARMA model.
        This test checks whether the returned p and q are integers within the range [2, 5].
        """
        data = np.random.rand(100)
        armaclass = ARMAClass(data)
        p, q = armaclass.estimate_order(data)
        self.assertTrue(2 <= p <= 5)
        self.assertTrue(2 <= q <= 5)

    def test_update_and_predict(self):
        """
        Test the update_and_predict method.

        Given a history of data, update_and_predict should return a list of forecasts
        for future time steps. This test ensures that the forecast list has the correct length.
        """
        data = np.random.rand(100)
        armaclass = ARMAClass(data)
        history = np.random.rand(80)
        forecast = armaclass.update_and_predict(history)
        self.assertEqual(len(forecast), 10)

    def test_get_residuals(self):
        """
        Test the get_residuals method.

        get_residuals should return the list of differences between observed and predicted values
        (residuals) for the ARMA model. This test ensures the returned list has the same length as the input data.
        """
        data = np.random.rand(100)
        armaclass = ARMAClass(data)
        residuals = armaclass.get_residuals()
        self.assertEqual(len(residuals), len(data))


if __name__ == "__main__":
    unittest.main()
