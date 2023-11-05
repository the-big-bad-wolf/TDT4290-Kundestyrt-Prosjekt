import unittest
import numpy as np
from crunch.forecasting.garch import GARCHClass


class TestGARCHClass(unittest.TestCase):
    """
    Unit test class for GARCHClass.

    """

    def test_estimate_order(self):
        """
        Test the estimate_order method.

        estimate_order is supposed to return integers p and q, which represent the order
        of the GARCH model. p and q should be in the range [2, 5] as per the model specification.
        """
        residuals = np.random.randn(100)
        garch = GARCHClass(residuals)
        p, q = garch.estimate_order(residuals)
        self.assertIsInstance(p, int)
        self.assertIsInstance(q, int)
        self.assertTrue(2 <= p <= 5)
        self.assertTrue(2 <= q <= 5)

    def test_update_and_predict(self):
        """
        Test the update_and_predict method.

        update_and_predict is supposed to update the model with new data (new_residuals)
        and return a float prediction for the next time step.
        """
        residuals = np.random.randn(100)
        garch = GARCHClass(residuals)
        new_residuals = np.random.randn(101)
        prediction = garch.update_and_predict(new_residuals)
        self.assertIsInstance(prediction, float)


if __name__ == "__main__":
    unittest.main()
