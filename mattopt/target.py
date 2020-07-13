"""
This module provides the Target class for quantities that can be
targeted in optimization.
"""

from .parameter import Parameter

class Target:
    """
    Target is an abstract base class for any scalar quantity that can
    be part of an objective function for optimization.
    """

    @staticmethod
    def empty_reset_function():
        pass

    def __init__(self, parameters, function, reset_function=None):
        """
        When constructing a Target, you should supply a python set in
        which the elements are the Parameter objects upon which this
        Target depends.

        reset_function can be None or something callable.
        """
        if type(parameters) is not set:
            raise ValueError("Argument to Target.__init__ must have type 'set'")
        for param in parameters:
            if type(param) is not Parameter:
                raise ValueError("In parameters argument to Target.__init__, " \
                                     "each element must have type Parameter.")
        if not callable(function):
            raise ValueError("function must be callable.")
        self._function = function

        if reset_function is None:
            self._reset_function = Target.empty_reset_function
        elif not callable(reset_function):
            raise ValueError("reset_function must be None or callable")
        else:
            self._reset_function = reset_function
            
        self._parameters = parameters

    def __repr__(self):
        return "Target(parameters=" + self._parameters.__repr__() + \
            "; evaluate=" + self._function.__repr__() + "; reset=" + \
            self._reset_function.__repr__() + ")"

    @property
    def parameters(self):
        """
        Return a python set containing all the Parameter objects from
        which the value of this Target can be calculated. There should
        be no arguments.
        """
        return self._parameters

    def evaluate(self):
        """
        Return a float, the scalar value that can be part of an
        objective function. Doing this generally requires running a
        physics code. There should be no arguments.
        """
        return self._function()

    def reset(self):
        """
        This method is called by the optimization algorithm when
        Parameter values are changed, and so the physics code
        associated with this Target should prepare for a new
        computation.
        """
        self._reset_function()
