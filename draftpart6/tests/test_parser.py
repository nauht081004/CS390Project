import unittest

from lexer import LexerError, lex
from parser import ParserError, parse_source
from ast_nodes import (
    ProgramNode,
    NumberNode,
    VariableNode,
    BinaryOpNode,
    AssignmentNode,
    PrintNode,
    ExpressionStatementNode,
    UnaryOpNode,
)


class ParserTests(unittest.TestCase):

    def test_1_operator_precedence(self):
        ast = parse_source("2 + 3 * 4")

        self.assertIsInstance(ast, ProgramNode)
        self.assertEqual(len(ast.statements), 1)

        statement = ast.statements[0]
        self.assertIsInstance(statement, ExpressionStatementNode)

        plus = statement.expression
        self.assertIsInstance(plus, BinaryOpNode)
        self.assertEqual(plus.operator, "+")

        self.assertIsInstance(plus.left, NumberNode)
        self.assertEqual(plus.left.value, 2)

        multiply = plus.right
        self.assertIsInstance(multiply, BinaryOpNode)
        self.assertEqual(multiply.operator, "*")
        self.assertEqual(multiply.left.value, 3)
        self.assertEqual(multiply.right.value, 4)

    def test_2_parentheses(self):
        ast = parse_source("(2 + 3) * 4")

        multiply = ast.statements[0].expression

        self.assertEqual(multiply.operator, "*")
        self.assertEqual(multiply.left.operator, "+")
        self.assertEqual(multiply.left.left.value, 2)
        self.assertEqual(multiply.left.right.value, 3)
        self.assertEqual(multiply.right.value, 4)

    def test_3_assignment(self):
        ast = parse_source("let x = 10;")

        assignment = ast.statements[0]

        self.assertIsInstance(assignment, AssignmentNode)
        self.assertEqual(assignment.variable.name, "x")
        self.assertIsInstance(assignment.expression, NumberNode)
        self.assertEqual(assignment.expression.value, 10)

    def test_4_multiple_statements(self):
        ast = parse_source(
            "let x = 2 + 3 * 4; display(x);"
        )

        self.assertEqual(len(ast.statements), 2)
        self.assertIsInstance(ast.statements[0], AssignmentNode)
        self.assertIsInstance(ast.statements[1], PrintNode)

        expression = ast.statements[0].expression
        self.assertEqual(expression.operator, "+")
        self.assertEqual(expression.right.operator, "*")

        self.assertEqual(
            ast.statements[1].expression.name,
            "x"
        )

    def test_5_invalid_assignment(self):
        with self.assertRaises(ParserError) as context:
            parse_source("let x = ;")

        self.assertIn(
            "expected expression after '='",
            str(context.exception)
        )

    def test_6_missing_right_parenthesis(self):
        with self.assertRaises(ParserError):
            parse_source("display (2 + 3;")

    def test_7_unary_minus(self):
        ast = parse_source("let x = -5 + 2;")

        expression = ast.statements[0].expression

        self.assertEqual(expression.operator, "+")
        self.assertIsInstance(expression.left, UnaryOpNode)
        self.assertEqual(expression.left.operator, "-")
        self.assertEqual(expression.left.operand.value, 5)
        self.assertEqual(expression.right.value, 2)

    def test_8_float(self):
        ast = parse_source("let x = 3.14 * 2;")

        expression = ast.statements[0].expression

        self.assertEqual(expression.operator, "*")
        self.assertEqual(expression.left.value, 3.14)
        self.assertEqual(expression.right.value, 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
