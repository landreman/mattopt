import unittest
import numpy as np
from mattopt.parameter import *

class ParameterTests(unittest.TestCase):
    def test_init1(self):
        """
        This is the most common use case.
        """
        v = 7.2 # Any value will do here.
        p = Parameter(v)
        self.assertEqual(p.val, v)
        self.assertEqual(p.fixed, True)
        self.assertEqual(p.min, np.NINF)
        self.assertEqual(p.max, np.Inf)
        self.assertEqual(p.__repr__(), "7.2 (fixed=True, min=-inf, max=inf)")

    def test_init2(self):
        """
        Try an int type and including finite bounds.
        """
        v = -1 # Any value will do here.
        p = Parameter(v, fixed=False, min=-5, max=10)
        self.assertEqual(p.val, v)
        self.assertEqual(p.fixed, False)
        self.assertEqual(p.min, -5)
        self.assertEqual(p.max, 10)

    def test_init3(self):
        """
        Try initializing with no initial val.
        """
        p = Parameter()
        self.assertEqual(p.val, 0.0)
        self.assertEqual(p.fixed, True)
        self.assertEqual(p.min, np.NINF)
        self.assertEqual(p.max, np.Inf)

    def test_init_validation(self):
        """
        If min <= val <= max is not satisfied, the constructor should
        raise an exception.
        """
        with self.assertRaises(RuntimeError):
            p = Parameter(1, min=2, max=3)

        with self.assertRaises(RuntimeError):
            p = Parameter(1, min=-10, max=-5)

    def test_fixed_validation(self):
        """
        We should not be able to change the "fixed" attribute to
        anything other than a bool.
        """

        p = Parameter(1)
        p.fixed = True
        self.assertTrue(p.fixed)
        p.fixed = False
        self.assertFalse(p.fixed)

        with self.assertRaises(RuntimeError):
            p.fixed = 1

        with self.assertRaises(RuntimeError):
            p.fixed = 1.0

    def test_validation(self):
        """
        Check validation when we change val, min, or max after the
        Parameter is created.
        """
        p = Parameter(1, min=-10, max=10)
        p.val = 3
        self.assertEqual(p.val, 3)
        p.min = -5
        self.assertEqual(p.min, -5)
        p.max = 5
        self.assertEqual(p.max, 5)
        
        with self.assertRaises(RuntimeError):
            p.val = -20
        with self.assertRaises(RuntimeError):
            p.val = 20
        self.assertEqual(p.val, 3)
            
        with self.assertRaises(RuntimeError):
            p.min = 10
        self.assertEqual(p.min, -5)

        with self.assertRaises(RuntimeError):
            p.max = -10
        self.assertEqual(p.max, 5)
            

class ParameterArrayTests(unittest.TestCase):
    def test_init1(self):
        d1 = 2
        d2 = 3
        v = np.ones((d1,d2))
        p = ParameterArray(v)
        self.assertEqual(p.fixed.shape, v.shape)

if __name__ == "__main__":
    unittest.main()
