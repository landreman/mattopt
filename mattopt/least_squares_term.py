"""
This module provides the LeastSquaresTerm class.
"""

from .parameter import Parameter, isnumber
from .target import Target

class LeastSquaresTerm:
    """
    This class represents one term in a nonlinear-least-squares
    problem. A LeastSquaresTerm instance has 3 basic attributes: a
    function (called target), a goal value (called goal), and a weight
    (sigma).  The overall value of the term is:

    ((target - goal) / sigma) ** 2.
    """

    def __init__(self, target, goal, sigma):
        if not isinstance(target, Target):
            raise ValueError('target must be an instance of Target')
        if not isnumber(goal):
            raise ValueError('goal must be a float or int')
        if not isnumber(sigma):
            raise ValueError('sigma must be a float or int')
        self._target = target
        self._goal = goal
        self._sigma = sigma

    @property
    def target(self):
        """
        For simplicity, target is read-only.
        """
        return self._target

    @property
    def goal(self):
        """
        For simplicity, goal is read-only.
        """
        return self._goal

    @property
    def sigma(self):
        """
        For simplicity, sigma is read-only.
        """
        return self._sigma

    @property
    def valin(self):
        """
        This property is a shorthand for target.evaluate().
        """
        return self._target.evaluate()

    @property
    def valout(self):
        """
        Return the overall value of this least-squares term.
        """
        temp = (self._target.evaluate() - self._goal) / self._sigma
        return temp * temp 
