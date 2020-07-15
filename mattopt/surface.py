"""
This module provides several classes for representing toroidal
surfaces.  There is a base class Surface, and several child classes
corresponding to different discrete representations.
"""

import numpy as np
from .parameter import Parameter, ParameterArray
from .shape import Shape

class Surface(Shape):
    """
    Surface is a base class for various representations of toroidal
    surfaces in simsopt.

    This class has two properites, nfp and stelsym. They are
    implemented using the @property decorator and protected variables
    to ensure users do not set them to any type other than Parameter.
    """

    def __init__(self, nfp=1, stelsym=True):
        Shape.__init__(self, nfp, stelsym)

    def __repr__(self):
        return "simsopt base Surface (nfp=" + str(self._nfp.val) + \
            ", stelsym=" + str(self._stelsym.val) + ")"

    def to_RZFourier(self):
        """
        Return a SurfaceRZFourier instance corresponding to the shape of this
        surface.  All subclasses should implement this abstract
        method.
        """
        raise NotImplementedError

class SurfaceRZFourier(Surface):
    """
    SurfaceRZFourier is a surface that is represented in cylindrical
    coordinates using the following Fourier series: 

    R(theta, phi) = \sum_{m=0}^{mpol} \sum_{n=-ntor}^{ntor} [
                     R_{c,m,n} \cos(m \theta - n nfp \phi)
                     + R_{s,m,n} \sin(m \theta - n nfp \phi) ]

    and the same for Z(theta, phi).

    Here, (R, phi, Z) are standard cylindrical coordinates, and theta
    is any poloidal angle.
    """
    def __init__(self, nfp=1, stelsym=True, mpol=1, ntor=0):
        # Perform some validation.
        if not isinstance(mpol, int):
            raise RuntimeError("mpol must have type int")
        if not isinstance(ntor, int):
            raise RuntimeError("ntor must have type int")
        if mpol < 1:
            raise RuntimeError("mpol must be at least 1")
        if ntor < 0:
            raise RuntimeError("ntor must be at least 0")
        self.mpol = Parameter(mpol, min=1, name="mpol for SurfaceRZFourier " \
                                  + str(hex(id(self))))
        self.ntor = Parameter(ntor, min=0, name="ntor for SurfaceRZFourier " \
                                  + str(hex(id(self))))
        Surface.__init__(self, nfp=nfp, stelsym=stelsym)
        self.allocate()

    def allocate(self):
        print("Allocating")
        self.mdim = self.mpol.val + 1
        self.ndim = 2 * self.ntor.val + 1
        self.Rc = ParameterArray(np.zeros((self.mdim, self.ndim)))
        self.Zs = ParameterArray(np.zeros((self.mdim, self.ndim)))
        if not self.stelsym.val:
            self.Rs = ParameterArray(np.zeros((self.mdim, self.ndim)))
            self.Zc = ParameterArray(np.zeros((self.mdim, self.ndim)))

    def __repr__(self):
        return "simsopt SurfaceRZFourier (nfp=" + str(self.nfp.val) + \
            ", stelsym=" + str(self.stelsym.val) + ", mpol=" + \
            str(self.mpol.val) + ", ntor=" + str(self.ntor.val) + ")"

#    def get_Rc(self, m, n):
#        return self.Rc[
