import unittest
from mattopt.target import Identity
from mattopt.least_squares_term import LeastSquaresTerm

class LeastSquaresTermTests(unittest.TestCase):

    def another_function(self):
        return self.p1.val + 100

    def test_basic(self):
        """
        Test basic usage
        """
        iden = Identity()
        lst = LeastSquaresTerm(iden.target, 3, 0.1)
        self.assertIs(lst.target, iden.target)
        self.assertEqual(lst.goal, 3)
        self.assertAlmostEqual(lst.sigma, 0.1, places=13)

        iden.x.val = 17
        self.assertEqual(lst.valin, 17)
        shouldbe = ((17 - 3) / 0.1) ** 2
        self.assertAlmostEqual(lst.valout, shouldbe, places=13)

    def test_exceptions(self):
        """
        Test that exceptions are thrown when invalid inputs are
        provided.
        """
        # First argument must have type Target
        with self.assertRaises(ValueError):
            lst = LeastSquaresTerm(2, 3, 0.1)

        # Second and third arguments must be real numbers
        iden = Identity()
        with self.assertRaises(ValueError):
            lst = LeastSquaresTerm(iden.target, "hello", 0.1)
        with self.assertRaises(ValueError):
            lst = LeastSquaresTerm(iden.target, 3, iden)

if __name__ == "__main__":
    unittest.main()
