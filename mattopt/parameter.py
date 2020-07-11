#!/usr/bin/env python3

"""
This module contains classes related to parameters in simsopt.  A
Parameter is a value that has the potential to be varied in an
optimization.  Sometimes however the value may also be held fixed. If
the value is varied, there may be box constraints, also known as bound
constraints, i.e. upper and lower bounds.
"""

import numpy as np

class Parameter:
    """
    This class represents a value that has the potential to be varied
    in an optimization, though sometime it may also be held
    fixed. This class has 4 private variables: _val, _fixed, _min, and
    _max. For each of these variables there is a public "property":
    val, fixed, min, and max. By using the "property" decorator it is
    possible to do some validation any time a user attempts to change
    the attributes.

    The instance variable val can be any type, not just float. This is
    important because we may want parameters that have type int or
    something more exotic.
    """
    def __init__(self, val=0.0, fixed=True, min=np.NINF, max=np.Inf):
        """
        Constructor
        """
        self._val = val
        self._fixed = fixed
        self._min = min
        self._max = max
        self.verify_bounds()

    # When "val", "min", or "max" is altered by a user, we should
    # check that val is indeed in between min and max.

    @property
    def val(self):
        return self._val

    @val.setter
    def val(self, newval):
        self.verify_bounds(val=newval)
        self._val = newval

    @property
    def min(self):
        return self._min

    @min.setter
    def min(self, newmin):
        self.verify_bounds(min=newmin)
        self._min = newmin

    @property
    def max(self):
        return self._max

    @max.setter
    def max(self, newmax):
        self.verify_bounds(max=newmax)
        self._max = newmax

    # When "fixed" is changed, we do not need to verify the bounds,
    # but we do want to ensure that "fixed" has type bool.
    @property
    def fixed(self):
        return self._fixed

    @fixed.setter
    def fixed(self, value):
        if not isinstance(value, bool):
            raise RuntimeError(
                "fixed attribute of a Parameter must have type bool.")
        self._fixed = value

    def __repr__(self):
        """
        Print the object in an informative way.
        """
        return str(self._val) + ' (fixed=' + str(self._fixed) + ', min=' + \
            str(self._min) + ', max=' + str(self._max) + ')'

    def verify_bounds(self, val=None, min=None, max=None):
        """
        Check that the value, lower bound, and upper bound are
        consistent. If no arguments are supplied, the method checks
        the private variables of this instance. The method can also
        check potential new values for val, min, or max, via optional
        arguments.
        """
        if val is None:
            val = self._val
        if min is None:
            min = self._min
        if max is None:
            max = self._max

        if min > max:
            raise RuntimeError("Parameter has min > max. " +
                               "min = " + str(min) +
                               ", max = " + str(max))
        if val < min:
            raise RuntimeError("Parameter has val < min. " +
                               "val = " + str(val) +
                               ", min = " + str(min))
        if val > max:
            raise RuntimeError("Parameter has val > max. " +
                               "val = " + str(val) +
                               ", max = " + str(max))


class ParameterArray1D:
    """
    This class represents a 1D array of Parameters. This class is
    useful for extracting arrays of values (or the upper or lower
    bounds) from arrays of Parameters.
    """
    # Q: Is there a way to keep the instance variable n synched to
    # len(arr)?
    def __init__(self, n=1, val=0, fixed=True, min=np.NINF, max=np.Inf):
        if not isinstance(n, int):
            raise RuntimeError("n must have type int")
        if n < 0:
            raise RuntimeError("n must be at least 0")
        self.n = n
        self.arr = [Parameter(val, fixed=fixed, min=min, max=max) \
                        for j in range(n)]

    def __repr__(self): 
        """
        Print the object in an informative way.
        """
        return "ParameterArray1D[" + str(self.n) + "]:\n" + \
            "\n".join([" " + p.__repr__() for p in self.arr])

    def verify_bounds(self):
        for j in range(len(self.arr)):
            self.arr[j].verify_bounds()

    def get_vals(self):
        return np.array([item.val for item in self.arr])

    def get_fixeds(self):
        return [item.fixed for item in self.arr]

    def get_mins(self):
        return np.array([item.min for item in self.arr])

    def get_maxs(self):
        return np.array([item.max for item in self.arr])

    def set_vals(self, val):
        for j in range(len(self.arr)):
            self.arr[j].val = val
            self.arr[j].verify_bounds()

    def set_fixeds(self, fixed):
        if not isinstance(fixed, bool):
            raise RuntimeError("fixed must have type bool")
        for j in range(len(self.arr)):
            self.arr[j].fixed = fixed

    def set_maxs(self, max):
        for j in range(len(self.arr)):
            self.arr[j].max = max
            self.arr[j].verify_bounds()

    def set_mins(self, min):
        for j in range(len(self.arr)):
            self.arr[j].min = min
            self.arr[j].verify_bounds()

    def count_fixed(self):
        return sum(self.get_fixeds())

    def count_variable(self):
        return len(self.arr) - self.count_fixed()


class ParameterArray2D:
    """
    This class represents a 1D array of Parameters. This class is
    useful for extracting arrays of values (or the upper or lower
    bounds) from arrays of Parameters
    """
    # Q: Is there a way to keep the instance variables m and n synched
    # to the dimensions of arr?
    def __init__(self, m=1, n=1, val=0, fixed=True, min=np.NINF, max=np.Inf):
        if not isinstance(m, int):
            raise RuntimeError("m must have type int")
        if m < 0:
            raise RuntimeError("m must be at least 0")
        if not isinstance(n, int):
            raise RuntimeError("n must have type int")
        if n < 0:
            raise RuntimeError("n must be at least 0")
        self.m = m
        self.n = n
        self.arr = [[Parameter(val, fixed=fixed, min=min, max=max) \
                         for j in range(n)] for k in range(m)]

    def __repr__(self):
        """
        Print the object in an informative way.
        """
        s = "ParameterArray2D[" + str(self.m) + "," + str(self.n) + "]:"
        for mm in range(len(self.arr)):
            for nn in range(len(self.arr[mm])):
                s += "\n [" + str(mm) + "," + str(nn) + "] " \
                    + self.arr[mm][nn].__repr__()
        return s

    def verify_bounds(self):
        for mm in range(len(self.arr)):
            for nn in range(len(self.arr[mm])):
                self.arr[mm][nn].verify_bounds()

    def get_vals(self):
        return np.array([[item.val for item in row] for row in self.arr])

    def get_fixeds(self):
        return np.array([[item.fixed for item in row] for row in self.arr])

    def get_mins(self):
        return np.array([[item.min for item in row] for row in self.arr])

    def get_maxs(self):
        return np.array([[item.max for item in row] for row in self.arr])

    def set_vals(self, val):
        for j in range(len(self.arr)):
            self.arr[j].val = val
            self.arr[j].verify_bounds()

    def set_fixeds(self, fixed):
        if not isinstance(fixed, bool):
            raise RuntimeError("fixed must have type bool")
        for j in range(len(self.arr)):
            self.arr[j].fixed = fixed

    def set_maxs(self, max):
        for j in range(len(self.arr)):
            self.arr[j].max = max
            self.arr[j].verify_bounds()

    def set_mins(self, min):
        for j in range(len(self.arr)):
            self.arr[j].min = min
            self.arr[j].verify_bounds()

    def count_fixed(self):
        return sum(sum(self.get_fixeds()))

    def count_variable(self):
        return self.m * self.n - self.count_fixed()



class ParameterArray:
    """
    This class stores arrays of parameters. However instead of storing
    a list or numpy.ndarray in which the elements are from the class
    Parameter, here instead we have a Parameter-like class in which
    the elements have type numpy.ndarray.
    """
    def __init__(self, val, fixed=None, min=None, max=None):
        if not isinstance(val, np.ndarray):
            raise RuntimeError("val must have type numpy.ndarray")
        self.val = val

        # Handle the attribute "fixed"
        if fixed is None:
            # Create an array of the same shape as "val" populated
            # with "true" entries
            self.fixed = np.full(self.val.shape, True)
        elif not isinstance(fixed, np.ndarray):
            raise RuntimeError( \
                "fixed must either be None or have type numpy.ndarray")
        elif fixed.shape == self.val.shape:
            self.fixed = fixed
        else:
            raise RuntimeError("fixed has a different shape than val")
        # I should also verify that the type is bool.

        # Handle the attribute "min"
        if min is None:
            # Create an array of the same shape as "val" populated
            # with np.NINF entries
            self.min = np.full(self.val.shape, np.NINF)
        elif not isinstance(min, np.ndarray):
            raise RuntimeError( \
                "min must either be None or have type numpy.ndarray")
        elif min.shape == self.val.shape:
            self.min = min
        else:
            raise RuntimeError("min has a different shape than val")
        # I should also verify that the type is float.

        # Handle the attribute "max"
        if max is None:
            # Create an array of the same shape as "val" populated
            # with np.Inf entries
            self.max = np.full(self.val.shape, np.Inf)
        elif not isinstance(max, np.ndarray):
            raise RuntimeError( \
                "max must either be None or have type numpy.ndarray")
        elif max.shape == self.val.shape:
            self.max = max
        else:
            raise RuntimeError("max has a different shape than val")
        # I should also verify that the type is float.

    def __repr__(self): 
        """
        Print the object in an informative way.
        """
        s = "ParameterArray" + str(self.val.shape) + ":"
        s += "\n val:\n" + self.val.__repr__()
        s += "\n fixed:\n" + self.fixed.__repr__()
        s += "\n min:\n" + self.min.__repr__()
        s += "\n max:\n" + self.max.__repr__()
        return s
