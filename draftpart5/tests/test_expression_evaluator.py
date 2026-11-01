import unittest
from lexer import lex
from parser import Parser
from environment import Environment
from expression_evaluator import evaluate, InterpreterError


def run(source, env=None):
    if env is None:
        env = Environment()
    tree = Parser(lex(source)).parse_expression()
    return evaluate(tree, env)


class ExpressionEvaluatorTests(unittest.TestCase):

    def test_precedence(self):
        self.assertEqual(run("2 + 3 * 4"), 14)

    def test_parentheses(self):
        self.assertEqual(run("(2 + 3) * 4"), 20)

    def test_subtraction_is_left_to_right(self):
        self.assertEqual(run("10 - 3 - 2"), 5)

    def test_exact_division_stays_integer(self):
        result = run("10 / 2")
        self.assertEqual(result, 5)
        self.assertIsInstance(result, int)

    def test_division_with_remainder(self):
        self.assertEqual(run("10 / 4"), 2.5)

    def test_modulo(self):
        self.assertEqual(run("17 % 5"), 2)

    def test_unary_minus(self):
        self.assertEqual(run("-3 + 5"), 2)

    def test_comparisons(self):
        self.assertIs(run("5 >= 5"), True)
        self.assertIs(run("2 < 1"), False)
        self.assertIs(run("3 != 3"), False)
        self.assertIs(run("4 == 4"), True)
        self.assertIs(run("7 > 2"), True)
        self.assertIs(run("7 <= 2"), False)

    def test_variable_lookup(self):
        env = Environment()
        env.define("x", 10)
        self.assertEqual(run("x + 5", env), 15)

    def test_string_join(self):
        self.assertEqual(run('"ab" + "cd"'), "abcd")

    def test_boolean_is_not_equal_to_number(self):
        self.assertIs(run("1 == T"), False)

    def test_undefined_variable(self):
        with self.assertRaisesRegex(InterpreterError, "undefined variable 'y'"):
            run("y + 1")

    def test_division_by_zero(self):
        with self.assertRaisesRegex(InterpreterError, "Division by zero"):
            run("5 / 0")

    def test_modulo_by_zero(self):
        with self.assertRaisesRegex(InterpreterError, "Modulo by zero"):
            run("5 % 0")

    def test_invalid_operation_string_minus_number(self):
        with self.assertRaisesRegex(InterpreterError, "Invalid operation"):
            run('"a" - 1')

    def test_invalid_operation_boolean_arithmetic(self):
        with self.assertRaisesRegex(InterpreterError, "Invalid operation"):
            run("T + 1")


if __name__ == "__main__":
    unittest.main(verbosity=2)
