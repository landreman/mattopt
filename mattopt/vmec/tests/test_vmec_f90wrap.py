import unittest
import numpy as np
from mpi4py import MPI
import os
from mattopt.vmec import vmec_f90wrap
from mattopt.vmec.core import run_modes

class F90wrapVmecTests(unittest.TestCase):
    def test_read_input(self):
        """
        Try reading a VMEC input file.
        """
        fcomm = MPI.COMM_WORLD.py2f()
        rank = MPI.COMM_WORLD.Get_rank()
        verbose = (rank == 0)
        # The input file will be in the same directory as this file:
        filename = os.path.join(os.path.dirname(__file__), 'input.li383_low_res')

        ictrl = np.zeros(5, dtype=np.int32)

        ier = 0
        numsteps = 1
        ns_index = -1
        iseq = rank
        ictrl[0] = run_modes['input']
        ictrl[1] = ier
        ictrl[2] = numsteps
        ictrl[3] = ns_index
        ictrl[4] = iseq

        reset_file = ''

        vmec_f90wrap.runvmec(ictrl, filename, verbose, fcomm, reset_file)

        success_codes = [0, 11]
        self.assertTrue(ictrl[1] in success_codes)

        self.assertEqual(vmec_f90wrap.vmec_input.nfp, 3)
        self.assertEqual(vmec_f90wrap.vmec_input.mpol, 4)
        self.assertEqual(vmec_f90wrap.vmec_input.ntor, 3)
        print('rbc.shape:', vmec_f90wrap.vmec_input.rbc.shape)
        print('rbc:',vmec_f90wrap.vmec_input.rbc[101:103, 0:4])

        # n = 0, m = 0:
        self.assertAlmostEqual(vmec_f90wrap.vmec_input.rbc[101,0], 1.3782)

        # n = 0, m = 1:
        self.assertAlmostEqual(vmec_f90wrap.vmec_input.zbs[101,1], 4.6465E-01)

        # n = 1, m = 1:
        self.assertAlmostEqual(vmec_f90wrap.vmec_input.zbs[102,1], 1.6516E-01)

if __name__ == "__main__":
    unittest.main()
