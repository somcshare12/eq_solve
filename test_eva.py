import math
import unittest

from Eq_Evaluator import Eq_Evaluator


class EqEvaluatorTest(unittest.TestCase):
    def setUp(self):
        self.evaluator = Eq_Evaluator()

    def evaluate(self, expression, variables=None):
        return self.evaluator.evaluate((expression, variables or {}))

    def assertEvaluatesAlmostEqual(self, expression, expected, variables=None):
        self.assertAlmostEqual(self.evaluate(expression, variables), expected)

    def test_arithmetic_precedence_and_functions(self):
        self.assertEvaluatesAlmostEqual(
            "sin(x)+cos(y)*tan(z)",
            math.sin(1) + math.cos(2) * math.tan(3),
            {"x": 1, "y": 2, "z": 3},
        )
        self.assertEvaluatesAlmostEqual(
            "2^sin(x+1)",
            2 ** math.sin(2),
            {"x": 1},
        )
        self.assertEvaluatesAlmostEqual(
            "sin(cos(x))",
            math.sin(math.cos(1)),
            {"x": 1},
        )

    def test_exponentiation_is_right_associative(self):
        self.assertEqual(self.evaluate("2^3^2"), 512)

    def test_unary_minus_and_scientific_notation(self):
        self.assertEqual(self.evaluate("2*-3"), -6)
        self.assertEqual(self.evaluate("-(x+2)", {"x": 4}), -6)
        self.assertAlmostEqual(self.evaluate("1e-3 + 2"), 2.001)

    def test_assignment_updates_variables(self):
        variables = {"x": 2}

        result = self.evaluator.evalute(("answer = x^2 + 1", variables))

        self.assertEqual(result, 5)
        self.assertEqual(variables["answer"], 5)

    def test_invalid_input_raises_clear_errors(self):
        with self.assertRaises(ValueError):
            self.evaluate("1 + @")

        with self.assertRaises(NameError):
            self.evaluate("missing + 1")


if __name__ == "__main__":
    unittest.main()