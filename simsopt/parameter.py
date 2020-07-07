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
    The instance variable val can be any type, not just float. This is
    important because we may want parameters that have type int or
    something more exotic.
    """
    def __init__(self, val, fixed=True, min=np.NINF, max=np.Inf):
        """
        Constructor
        """
        self.val = val
        self.fixed = fixed
        self.min = min
        self.max = max
        self.verify_bounds()

    def __repr__(self):
        """
        Print the object in an informative way.
        """
        return str(self.val) + ' (fixed=' + str(self.fixed) + ', min=' + \
            str(self.min) + ', max=' + str(self.max) + ')'

    def verify_bounds(self):
        """
        Check that the value, lower bound, and upper bound are
        consistent.
        """
        # Q: Is there a way to get this method to run when the user
        # manually edits the data?
        if self.min > self.max:
            raise RuntimeError("Parameter has min > max. " +
                               "min = " + str(self.min) +
                               ", max = " + str(self.max))
        if self.val < self.min:
            raise RuntimeError("Parameter has val < min. " +
                               "val = " + str(self.val) +
                               ", min = " + str(self.min))
        if self.val > self.max:
            raise RuntimeError("Parameter has val > max. " +
                               "val = " + str(self.val) +
                               ", max = " + str(self.max))


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
