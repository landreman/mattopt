import unittest
from mattopt.target import Identity
from mattopt.least_squares_term import LeastSquaresTerm
from mattopt.least_squares_problem import LeastSquaresProblem
from mattopt.rosenbrock import Rosenbrock

class LeastSquaresProblemTests(unittest.TestCase):

    def test_basic(self):
        """
        Test basic usage
        """
        # Objective function f(x) = ((x - 3) / 2) ** 2
        iden1 = Identity()
        term1 = LeastSquaresTerm(iden1.target, 3, 2)
        prob = LeastSquaresProblem([term1])
        self.assertAlmostEqual(prob.objective, 2.25)
        iden1.x.val = 10
        self.assertAlmostEqual(prob.objective, 12.25)
        self.assertEqual(prob.parameters, [iden1.x])

        # Objective function
        # f(x,y) = ((x - 3) / 2) ** 2 + ((y + 4) / 5) ** 2
        iden2 = Identity()
        term2 = LeastSquaresTerm(iden2.target, -4, 5)
        prob = LeastSquaresProblem([term1, term2])
        self.assertAlmostEqual(prob.objective, 12.89)
        iden1.x.val = 5
        iden2.x.val = -7
        self.assertAlmostEqual(prob.objective, 1.36)
        #print("prob.parameters:",prob.parameters)
        #print("[iden1.x, iden2.x]:",[iden1.x, iden2.x])
        self.assertEqual(set(prob.parameters), {iden1.x, iden2.x})

    def test_exceptions(self):
        """
        Verify that exceptions are raised when invalid inputs are
        provided.
        """
        # Argument must be a list of LeastSquaresTerms
        with self.assertRaises(ValueError):
            prob = LeastSquaresProblem(7)
        with self.assertRaises(ValueError):
            prob = LeastSquaresProblem([])
        with self.assertRaises(ValueError):
            prob = LeastSquaresProblem([7, 1])

    def test_solve_quadratic(self):
        """
        Minimize f(x,y,z) = ((x-1)/1)^2 + ((y-2)/2)^2 + ((z-3)/3)^2.
        The optimum is at (x,y,z)=(1,2,3), and f=0 at this point.
        """
        iden1 = Identity()
        iden2 = Identity()
        iden3 = Identity()
        term1 = LeastSquaresTerm(iden1.target, 1, 1)
        term2 = LeastSquaresTerm(iden2.target, 2, 2)
        term3 = LeastSquaresTerm(iden3.target, 3, 3)
        prob = LeastSquaresProblem([term1, term2, term3])
        prob.solve()
        self.assertAlmostEqual(prob.objective, 0)
        self.assertAlmostEqual(iden1.x.val, 1)
        self.assertAlmostEqual(iden2.x.val, 2)
        self.assertAlmostEqual(iden3.x.val, 3)

    def test_solve_rosenbrock(self):
        """
        Minimize the Rosenbrock function.
        """
        r = Rosenbrock()
        term1 = LeastSquaresTerm(r.target1, 0, 1)
        term2 = LeastSquaresTerm(r.target2, 0, 1)
        prob = LeastSquaresProblem([term1, term2])
        prob.solve()
        self.assertAlmostEqual(prob.objective, 0)
        self.assertAlmostEqual(r.x1.val, 1)
        self.assertAlmostEqual(r.x2.val, 1)

if __name__ == "__main__":
    unittest.main()
