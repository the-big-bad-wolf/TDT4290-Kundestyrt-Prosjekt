import unittest
import numpy as np
from crunch.forecasting.garch import GARCHClass

class TestGARCHClass(unittest.TestCase):
    """
    Unit test class for GARCHClass
    """

    def test_estimate_order(self):
        """
        Test that the estimate_order method returns integers p and q 
        in the correct range [2, 5].
        """
        residuals = np.random.randn(100)
        garch = GARCHClass(residuals)
        p, q = garch.estimate_order()
        self.assertIsInstance(p, int)
        self.assertIsInstance(q, int)
        self.assertTrue(2 <= p <= 5)
        self.assertTrue(2 <= q <= 5)

    def test_update_and_predict(self):
        """
        Test that the update_and_predict method returns a float prediction.
        """
        residuals = np.random.randn(100)
        garch = GARCHClass(residuals)
        new_residuals = np.random.randn(101)
        prediction = garch.update_and_predict(new_residuals)
        self.assertIsInstance(prediction, float)

if __name__ == "__main__":
    unittest.main()
