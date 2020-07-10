#!/usr/bin/env python3

import unittest
from mattopt.parameter import *
import numpy as np

class ParameterTests(unittest.TestCase):
    def test_init1(self):
        v = 7.2
        p = Parameter(v)
        self.assertEqual(p.val, v)
        self.assertEqual(p.fixed, True)
        self.assertEqual(p.min, np.NINF)
        self.assertEqual(p.max, np.Inf)

    def test_init2(self):
        v = 7.2
        p = Parameter(v, fixed=False, min=-5, max=10)
        self.assertEqual(p.val, v)
        self.assertEqual(p.fixed, False)
        self.assertEqual(p.min, -5)
        self.assertEqual(p.max, 10)


if __name__ == "__main__":
    unittest.main()
