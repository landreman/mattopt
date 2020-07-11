import unittest
from mattopt.parameter import *
import numpy as np

class ParameterTests(unittest.TestCase):
    def test_init1(self):
        v = 7.2 # Any value will do here.
        p = Parameter(v)
        self.assertEqual(p.val, v)
        self.assertEqual(p.fixed, True)
        self.assertEqual(p.min, np.NINF)
        self.assertEqual(p.max, np.Inf)

    def test_init2(self):
        v = -1 # Any value will do here.
        p = Parameter(v, fixed=False, min=-5, max=10)
        self.assertEqual(p.val, v)
        self.assertEqual(p.fixed, False)
        self.assertEqual(p.min, -5)
        self.assertEqual(p.max, 10)


class ParameterArrayTests(unittest.TestCase):
    def test_init1(self):
        d1 = 2
        d2 = 3
        v = np.ones((d1,d2))
        p = ParameterArray(v)
        self.assertEqual(p.fixed.shape, v.shape)

if __name__ == "__main__":
    unittest.main()
