"""
This module provides a class that handles the VMEC equilibrium code.
"""

import numpy as np
from mattopt import *
from FortranNamelist import NamelistFile

class Vmec:
    """
    This class represents the VMEC equilibrium code.
    """
    def __init__(self):
        """
        Constructor
        """
        self.nfp = Parameter(1, min=1)
        self.stelsym = Parameter(True)
        self.mpol = Parameter(1, min=1)
        self.ntor = Parameter(0, min=0)
        self.status = "setup"

    def __repr__(self):
        """
        Print the object in an informative way.
        """
        return "Vmec instance (nfp=" + str(self.nfp.val) + " mpol=" + \
            str(self.mpol.val) + " ntor=" + str(self.ntor.val) + " status=" + \
            self.status + ")"

    def parse_namelist_var(self, dict, var, default, min=np.NINF, max=np.Inf):
        """
        This method is used to streamline from_input_file(), and would
        not usually be called by users.
        """
        if var in dict:
            val_to_use = dict[var]
        else:
            val_to_use = default
        setattr(self, var, Parameter(val_to_use, min=min, max=max))

    @classmethod
    def from_input_file(cls, filename):
        """
        Read in a VMEC input namelist.
        """
        vmec = cls()

        nml = NamelistFile(filename)
        dict = nml["indata"]

        vmec.parse_namelist_var(dict, "nfp", 1, min=1)
        vmec.parse_namelist_var(dict, "mpol", 1, min=1)
        vmec.parse_namelist_var(dict, "ntor", 0, min=0)

        # Handle lasym separately since we actually store its opposite.
        if "lasym" in dict:
            lasym = dict["lasym"]
        else:
            lasym = False
        vmec.stelsym = Parameter(not lasym)

        return vmec
