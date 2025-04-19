import numpy as np
from scipy.interpolate import interp1d

class MinettiModel:
    def __init__(self):
        """
        Initialize the MinettiModel instance by building an interpolator based
        on the reference data of energy cost as a function of slope.

        Attributes:
            _interpolator (scipy.interpolate.interp1d): Cubic interpolator used
            to estimate energy cost from slope percentage.
        """
        self._interpolator = self._build_model()

    def _build_model(self):
        """
        Build a cubic interpolation model for the cost of running on slopes
        using Minetti's reference data.

        Returns:
            interp1d: Interpolation function that estimates energy cost (CR)
                      based on slope percentage.
        """
        reference_slopes = np.array([-45, -40, -35, -30, -20, -10, 0, 10, 20, 30, 35, 40, 45])
        cr_values = np.array([3.92, 3.49, 2.81, 2.43, 1.73, 1.93, 3.40, 5.77, 8.92, 12.52, 14.43, 16.83, 18.93])
        return interp1d(reference_slopes, cr_values, kind='cubic', fill_value='extrapolate')

    def get_energy_cost(self, slope):
        """
        Get the estimated energy cost of running for a given slope using the Minetti model.

        Parameters:
            slope (float): Slope percentage (e.g., 10 for 10% incline, -10 for 10% decline).

        Returns:
            float: Estimated energy cost (CR) for the given slope.
        """
        return float(self._interpolator(slope))
