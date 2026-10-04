import unittest

from lexer import lex
from parser import Parser, ParserError
from ast_nodes import (
    ProgramNode,
    AssignmentNode,
    PrintNode,
    NumberNode,
    VariableNode,
    BinaryOpNode,
)


def parse_program(source):
    parser = Parser(lex(source))
    tree = parser.parse_program()
    parser.expect("EOF")
    return tree


class StatementParserTests(unittest.TestCase):

    def test_assignment(self):
        tree = parse_program("let x = 5;")

        self.assertIsInstance(tree, ProgramNode)
        self.assertEqual(len(tree.statements), 1)

        assignment = tree.statements[0]
        self.assertIsInstance(assignment, AssignmentNode)
        self.assertEqual(assignment.variable.name, "x")
        self.assertIsInstance(assignment.expression, NumberNode)
        self.assertEqual(assignment.expression.value, 5)

    def test_reassignment(self):
        tree = parse_program("x = 7;")

        assignment = tree.statements[0]

        self.assertIsInstance(assignment, AssignmentNode)
        self.assertEqual(assignment.variable.name, "x")
        self.assertEqual(assignment.expression.value, 7)

    def test_display(self):
        tree = parse_program("display(2 + 3 * 4);")

        statement = tree.statements[0]

        self.assertIsInstance(statement, PrintNode)
        self.assertIsInstance(statement.expression, BinaryOpNode)
        self.assertEqual(statement.expression.operator, "+")
        self.assertEqual(statement.expression.right.operator, "*")

    def test_multiple_statements(self):
        tree = parse_program("let x = 5; display(x);")

        self.assertIsInstance(tree, ProgramNode)
        self.assertEqual(len(tree.statements), 2)

        self.assertIsInstance(tree.statements[0], AssignmentNode)
        self.assertIsInstance(tree.statements[1], PrintNode)

    def test_assignment_preserves_precedence(self):
        tree = parse_program(
            "let x = 2 + 3 * 4; display(x);"
        )

        assignment = tree.statements[0]
        expression = assignment.expression

        self.assertEqual(expression.operator, "+")
        self.assertEqual(expression.left.value, 2)
        self.assertEqual(expression.right.operator, "*")
        self.assertEqual(expression.right.left.value, 3)
        self.assertEqual(expression.right.right.value, 4)

    def test_missing_expression(self):
        with self.assertRaises(ParserError):
            parse_program("let x = ;")

    def test_missing_right_parenthesis(self):
        with self.assertRaises(ParserError):
            parse_program("display(5;")

    def test_missing_semicolon(self):
        with self.assertRaises(ParserError):
            parse_program("let x = 5")


if __name__ == "__main__":
    unittest.main(verbosity=2)
