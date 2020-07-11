import unittest
import numpy as np
import os
from mattopt.vmec import *

class VmecTests(unittest.TestCase):
    def test_init(self):
        """
        Just create a Vmec instance using the standard constructor,
        and make sure we can read all the attributes.
        """
        v = Vmec()
        self.assertEqual(v.nfp.val, 1)
        self.assertTrue(v.stelsym.val)
        self.assertEqual(v.mpol.val, 1)
        self.assertEqual(v.ntor.val, 0)
        self.assertEqual(v.status, "setup")

    def test_repr(self):
        """
        Test that Vmec objects are printed in the expected way.
        """
        v = Vmec()
        self.assertEqual(v.__repr__(), \
                             "Vmec instance (nfp=1 mpol=1 ntor=0 status=setup)")

    def test_from_input_file(self):
        """
        Try reading in a VMEC input namelist.
        """
        # We might run this script from this directory or from the
        # project root directory. Handle both cases.
        base_filename = "input.li383_1.4m"
        filename2 = os.path.join("mattopt", "tests", base_filename)
        if os.path.isfile(base_filename):
            filename = base_filename
        elif os.path.isfile(filename2):
            filename = filename2
        else:
            raise RuntimeError("Unable to find test file " + base_filename)
        v = Vmec.from_input_file(filename)

        self.assertEqual(v.nfp.val, 3)
        self.assertTrue(v.stelsym.val)
        self.assertEqual(v.mpol.val, 9)
        self.assertEqual(v.ntor.val, 5)
        self.assertEqual(v.status, "setup")

if __name__ == "__main__":
    unittest.main()
