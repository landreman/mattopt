#!/usr/bin/env python3

"""
This module contains classes related to parameters in simsopt.  A
Parameter is a value that has the potential to be varied in an
optimization.  Sometimes however the value may also be held fixed. If
the value is varied, there may be box constraints, also known as bound
constraints, i.e. upper and lower bounds.

This module contains the Parameter class, which stores a single value,
and the ParameterArray class, which stores arbitrary-dimension arrays
of Parameters.
"""

import numpy as np

class Parameter:
    """
    This class represents a value that has the potential to be varied
    in an optimization, though sometime it may also be held
    fixed. This class has 4 private variables: _val, _fixed, _min, and
    _max. For each of these variables there is a public "property":
    val, fixed, min, and max. By using the @property decorator it is
    possible to do some validation any time a user attempts to change
    the attributes.

    The instance variables val, min, and max can be any type, not just
    float. This is important because we may want parameters that have
    type int, bool, or something more exotic.
    """
    def __init__(self, val=0.0, listener=None, fixed=True, min=np.NINF, \
                     max=np.Inf):
        """
        Constructor
        """
        self._val = val
        self._fixed = fixed
        self._min = min
        self._max = max
        self.verify_bounds()
        # Initialize _listeners to be a set of all listeners
        if listener is None:
            self._listeners = set()
        elif callable(listener):
            self._listeners = {listener}
        elif type(listener) is set:
            for s in listener:
                if not callable(s):
                    raise ValueError("listener must be None, a callable, or " \
                                         + "a set of callable objects.")
            self._listeners = listener
        else:
            raise ValueError("listener must be None, a callable, or a set " \
                                 + "of callable objects.")

    # When "val", "min", or "max" is altered by a user, we should
    # check that val is indeed in between min and max.

    @property
    def val(self):
        return self._val

    @val.setter
    def val(self, newval):
        self.verify_bounds(val=newval)
        self._val = newval
        # Update all objects that observe this Parameter:
        for listener in self._listeners:
            listener()

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
            raise ValueError(
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
            raise ValueError("Parameter has min > max. " +
                               "min = " + str(min) +
                               ", max = " + str(max))
        if val < min:
            raise ValueError("Parameter has val < min. " +
                               "val = " + str(val) +
                               ", min = " + str(min))
        if val > max:
            raise ValueError("Parameter has val > max. " +
                               "val = " + str(val) +
                               ", max = " + str(max))


class ParameterArray:
    """
    This class stores arrays of parameters. However instead of storing
    a list or numpy.ndarray in which the elements are from the class
    Parameter, here instead we have a Parameter-like class in which
    the elements have type numpy.ndarray. The reason is that we want
    to allow ndarray slicing syntax, e.g.
    p = ParameterArray(numpy.zeros(10, 20))
    p.fixed[2:3, 5:10] = True

    As with a Parameter, a ParameterArray instance has 4 private
    variables: _val, _fixed, _min, and _max. For each of these
    variables there is a public "property": val, fixed, min, and
    max. By using the @property decorator it is possible to do some
    validation any time a user attempts to change the attributes.

    Presently there is no checking that min <= val <= max or that
    fixed has type bool. For the first of these, I don't know how to
    automatically validate when a user changes specific ndarray
    elements.

    Presently it is not possible to resize or reshape a
    ParameterArray. This is awkward because it would require changing
    the shape/size of all 4 member arrays (val, fixed, min, max). If
    you tried changing one of those 4 arrays at a time, it would not
    possible to distinguish correct usage from incorrectly changing
    the size of one array without changing the other 3.
    """
    def __init__(self, val, fixed=None, min=None, max=None):
        if not isinstance(val, np.ndarray):
            raise ValueError("val must have type numpy.ndarray")
        self._val = val

        # Handle the attribute "fixed"
        if fixed is None:
            # Create an array of the same shape as "val" populated
            # with "true" entries
            self._fixed = np.full(self._val.shape, True)
        elif isinstance(fixed, bool):
            # A single bool was provided. Copy it to all entries.
            self._fixed = np.full(self._val.shape, fixed)
        elif not isinstance(fixed, np.ndarray):
            raise ValueError( \
                "fixed must either be None or have type bool or numpy.ndarray")
        elif fixed.shape == self._val.shape:
            self._fixed = fixed
        else:
            raise ValueError("fixed has a different shape than val")
        # I should also verify that the type is bool.

        # Handle the attribute "min"
        if min is None:
            # Create an array of the same shape as "val" populated
            # with np.NINF entries
            self._min = np.full(self._val.shape, np.NINF)
        elif isinstance(min, int) or isinstance(min, float):
            # A single number was provided. Copy it to all entries.
            self._min = np.full(self._val.shape, min)
        elif not isinstance(min, np.ndarray):
            raise ValueError( \
                "min must either be None or have type int, " \
                + "float, or numpy.ndarray")
        elif min.shape == self._val.shape:
            self._min = min
        else:
            raise ValueError("min has a different shape than val")
        # I should also verify that the type is float.

        # Handle the attribute "max"
        if max is None:
            # Create an array of the same shape as "val" populated
            # with np.Inf entries
            self._max = np.full(self._val.shape, np.Inf)
        elif isinstance(max, int) or isinstance(max, float):
            # A single number was provided. Copy it to all entries.
            self._max = np.full(self._val.shape, max)
        elif not isinstance(max, np.ndarray):
            raise ValueError( \
                "max must either be None or have type int, " \
                + "float, or numpy.ndarray")
        elif max.shape == self._val.shape:
            self._max = max
        else:
            raise ValueError("max has a different shape than val")
        # I should also verify that the type is float.

    def __repr__(self): 
        """
        Print the object in an informative way.
        """
        s = "--- ParameterArray" + str(self._val.shape) + " ---"
        s += "\nval:\n" + self._val.__repr__()
        s += "\nfixed:\n" + self._fixed.__repr__()
        s += "\nmin:\n" + self._min.__repr__()
        s += "\nmax:\n" + self._max.__repr__()
        return s

    @property
    def val(self):
        return self._val

    @val.setter
    def val(self, newval):
        if isinstance(newval, int) or isinstance(newval, float):
            newval = np.full(self._val.shape, newval)
        elif not isinstance(newval, np.ndarray):
            raise ValueError("val must have type numpy.ndarray.")
        elif newval.shape != self._val.shape:
            raise ValueError("Shape and size of the val array cannot be " \
              "changed. old shape=" + str(self._val.shape) + " new=" \
              + str(newval.shape))
        #self.verify_bounds(val=newval)
        self._val = newval

    @property
    def fixed(self):
        return self._fixed

    @fixed.setter
    def fixed(self, newfixed):
        if isinstance(newfixed, bool):
            newfixed = np.full(self._val.shape, newfixed)
        elif not isinstance(newfixed, np.ndarray):
            raise ValueError("fixed must have type numpy.ndarray.")
        elif newfixed.shape != self._fixed.shape:
            raise ValueError("Shape and size of the fixed array cannot be " \
              "changed. old shape=" + str(self._fixed.shape) + " new=" \
              + str(newfixed.shape))
        #self.verify_bounds(fixed=newfixed)
        self._fixed = newfixed

    @property
    def min(self):
        return self._min

    @min.setter
    def min(self, newmin):
        if isinstance(newmin, int) or isinstance(newmin, float):
            newmin = np.full(self._val.shape, newmin)
        elif not isinstance(newmin, np.ndarray):
            raise ValueError("min must have type numpy.ndarray.")
        elif newmin.shape != self._min.shape:
            raise ValueError("Shape and size of the min array cannot be " \
              "changed. old shape=" + str(self._min.shape) + " new=" \
              + str(newmin.shape))
        #self.verify_bounds(min=newmin)
        self._min = newmin

    @property
    def max(self):
        return self._max

    @max.setter
    def max(self, newmax):
        if isinstance(newmax, int) or isinstance(newmax, float):
            newmax = np.full(self._val.shape, newmax)
        elif not isinstance(newmax, np.ndarray):
            raise ValueError("max must have type numpy.ndarray.")
        elif newmax.shape != self._max.shape:
            raise ValueError("Shape and size of the max array cannot be " \
              "changed. old shape=" + str(self._max.shape) + " new=" \
              + str(newmax.shape))
        #self.verify_bounds(max=newmax)
        self._max = newmax

