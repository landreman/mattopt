"""
This module provides several classes for representing toroidal
surfaces.  There is a base class Surface, and several child classes
corresponding to different discrete representations.
"""

import numpy as np
from .parameter import Parameter, ParameterArray

class Surface:
    """
    Surface is a base class for various representations of toroidal
    surfaces in simsopt.
    """

    def __init__(self, nfp=1, stelsym=True):
        # Perform some validation.
        if not isinstance(nfp, int):
            raise RuntimeError("nfp must have type int")
        if nfp < 1:
            raise RuntimeError("nfp must be at least 1")
        if not isinstance(stelsym, bool):
            raise RuntimeError("stelsym must have type bool")
        self.nfp = Parameter(nfp, min=1)
        self.stelsym = Parameter(stelsym)

    def __repr__(self):
        return "simsopt base Surface (nfp=" + str(self.nfp.val) + \
            ", stelsym=" + str(self.stelsym.val) + ")"

    def to_RZ(self):
        """
        Return a SurfaceRZ instance corresponding to the shape of this
        surface.  All subclasses should implement this abstract
        method.
        """
        raise NotImplementedError

class SurfaceRZ(Surface):
    """
    SurfaceRZ is a surface that is represented in cylindrical
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
        self.mpol = Parameter(mpol, min=1)
        self.ntor = Parameter(ntor, min=0)
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
        return "simsopt SurfaceRZ (nfp=" + str(self.nfp.val) + ", stelsym=" \
            + str(self.stelsym.val) + ", mpol=" + str(self.mpol.val) + \
            ", ntor=" + str(self.ntor.val) + ")"

#    def get_Rc(self, m, n):
#        return self.Rc[
