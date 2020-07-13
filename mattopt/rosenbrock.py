"""
This module provides a minimal object that possesses Parameters and
Targets.
"""

import numpy as np
from .parameter import Parameter
from .target import Target

class Rosenbrock():
    """
    This class defines a minimal object that possesses Parameters and
    Targets.
    """

    def reset(self):
        print("Resetting")
        self.is_reset = True

    def long_computation(self):
        if self.is_reset:
            print("Running long computation...")
        self.is_reset = False

    def evaluate_target1(self):
        """
        First term in the 2D Rosenbrock function.
        """
        self.long_computation()
        return self.a - self.x1.val

    def evaluate_target2(self):
        """
        Second term in the 2D Rosenbrock function.
        """
        self.long_computation()
        return (self.x2.val - self.x1.val * self.x1.val) * self.sqrtb

    def __init__(self, a=1, b=100):
        self.a = a
        self.sqrtb = np.sqrt(b)
        self.x1 = Parameter(0.0)
        self.x2 = Parameter(0.0)
        params = {self.x1, self.x2}
        self.is_reset = False
        self.target1 = Target(params, self.evaluate_target1, self.reset)
        self.target2 = Target(params, self.evaluate_target2)

