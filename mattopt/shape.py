"""
This module provides a base class for shapes that can be
optimized. Surfaces and Coils will be subclasses of this class.
"""

import numpy as np
from .parameter import Parameter

class Shape:
    """
    Shape is a base class for shapes that can be optimized, such as
    toroidal surfaces and coils.

    This class has two properites, nfp and stelsym. They ar`e
    implemented using the @property decorator and protected variables
    to ensure users do not set them to any type other than Parameter.
    """

    def __init__(self, nfp=1, stelsym=True):
        # Perform some validation.
        if not isinstance(nfp, int):
            raise RuntimeError("nfp must have type int")
        if nfp < 1:
            raise RuntimeError("nfp must be at least 1")
        if not isinstance(stelsym, bool):
            raise RuntimeError("stelsym must have type bool")
        self._nfp = Parameter(nfp, min=1, name="nfp")
        self._stelsym = Parameter(stelsym, name="stelsym")

    def __repr__(self):
        return "simsopt base Shape (nfp=" + str(self._nfp.val) + \
            ", stelsym=" + str(self._stelsym.val) + ")"

    @property
    def nfp(self):
        return self._nfp

    @nfp.setter
    def nfp(self, newval):
        if not isinstance(newval, Parameter):
            raise ValueError("nfp must have type Parameter")
        self._nfp = newval

    @property
    def stelsym(self):
        return self._stelsym

    @stelsym.setter
    def stelsym(self, newval):
        if not isinstance(newval, Parameter):
            raise ValueError("stelsym must have type Parameter")
        self._stelsym = newval

