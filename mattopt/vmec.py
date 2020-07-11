"""
This module provides a class that handles the VMEC equilibrium code.
"""

import numpy as np
from mattopt import *
from FortranNamelist import NamelistFile

class Vmec(Equilibrium):
    """
    This class represents the VMEC equilibrium code.
    """
    def __init__(self):
        """
        Constructor
        """
        # nfp and stelsym are initialized by the Equilibrium constructor:
        Equilibrium.__init__(self)
        self.mpol = Parameter(1, min=1)
        self.ntor = Parameter(0, min=0)
        self.delt = Parameter(0.7, min=0, max=1)
        self.tcon0 = Parameter(2.0)
        self.phiedge = Parameter(1.0)
        self.curtor = Parameter(0.0)
        self.gamma = Parameter(0.0)
        self.boundary = SurfaceRZ(nfp=self.nfp.val, stelsym=self.stelsym.val, \
                                      mpol=self.mpol.val, ntor=self.ntor.val)
        # Handle a few variables that are not Parameters:
        self.ncurr = 1
        self.free_boundary = False
        self.status = "setup"

    def __repr__(self):
        """
        Print the object in an informative way.
        """
        return "Vmec instance (nfp=" + str(self.nfp.val) + " mpol=" + \
            str(self.mpol.val) + " ntor=" + str(self.ntor.val) + " status=" + \
            self.status + ")"

    def parse_namelist_var(self, dict, var, default, min=np.NINF, max=np.Inf, \
                               new_name=None, parameter=True):
        """
        This method is used to streamline from_input_file(), and would
        not usually be called by users.
        """
        if var in dict:
            val_to_use = dict[var]
        else:
            val_to_use = default

        if new_name is None:
            name = var
        else:
            name = new_name

        if parameter:
            setattr(self, name, Parameter(val_to_use, min=min, max=max))
        else:
            setattr(self, name, val_to_use)

    @classmethod
    def from_input_file(cls, filename):
        """
        Create an instance of the Vmec class based on settings that
        are read in from a VMEC input namelist.
        """
        vmec = cls()

        nml = NamelistFile(filename)
        dict = nml["indata"]

        vmec.parse_namelist_var(dict, "nfp", 1, min=1)
        vmec.parse_namelist_var(dict, "mpol", 1, min=1)
        vmec.parse_namelist_var(dict, "ntor", 0, min=0)
        vmec.parse_namelist_var(dict, "delt", 0.7)
        vmec.parse_namelist_var(dict, "tcon0", 2.0)
        vmec.parse_namelist_var(dict, "phiedge", 1.0)
        vmec.parse_namelist_var(dict, "curtor", 0.0)
        vmec.parse_namelist_var(dict, "gamma", 0.0)
        vmec.parse_namelist_var(dict, "lfreeb", False, \
                                    new_name="free_boundary", parameter=False)
        vmec.parse_namelist_var(dict, "ncurr", 1, parameter=False)

        # Handle a few variables separately:
        if "lasym" in dict:
            lasym = dict["lasym"]
        else:
            lasym = False
        vmec.stelsym = Parameter(not lasym)

        vmec.boundary = SurfaceRZ(nfp=vmec.nfp.val, stelsym=vmec.stelsym.val, \
                                      mpol=vmec.mpol.val, ntor=vmec.ntor.val)

        return vmec
