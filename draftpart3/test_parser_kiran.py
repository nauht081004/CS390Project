"""Expression tests for the uploaded Part 3 snapshot; AI assistance disclosed separately."""
import unittest
from lexer import lex
from parser import Parser, ParserError
from ast_nodes import NumberNode, VariableNode, BinaryOpNode, UnaryOpNode


def parse_complete_expression(source):
    parser = Parser(lex(source))
    tree = parser.parse_expression()
    # parse_expression intentionally stops at delimiters. This test helper
    # requires a complete standalone expression, so leftover tokens are errors.
    parser.expect('EOF')
    return tree


class ParserExpressionTests(unittest.TestCase):
    def test_integer(self):
        node = parse_complete_expression('42')
        self.assertIsInstance(node, NumberNode)
        self.assertEqual(node.value, 42)

    def test_decimal(self):
        self.assertEqual(parse_complete_expression('3.25').value, 3.25)

    def test_variable(self):
        node = parse_complete_expression('total')
        self.assertIsInstance(node, VariableNode)
        self.assertEqual(node.name, 'total')

    def test_multiplication_precedence(self):
        node = parse_complete_expression('2 + 3 * 4')
        self.assertIsInstance(node, BinaryOpNode)
        self.assertEqual(node.operator, '+')
        self.assertEqual(node.left.value, 2)
        self.assertEqual(node.right.operator, '*')
        self.assertEqual((node.right.left.value, node.right.right.value), (3, 4))

    def test_parentheses(self):
        node = parse_complete_expression('(2 + 3) * 4')
        self.assertEqual(node.operator, '*')
        self.assertEqual(node.left.operator, '+')
        self.assertEqual((node.left.left.value, node.left.right.value, node.right.value), (2, 3, 4))

    def test_left_associative_subtraction(self):
        node = parse_complete_expression('10 - 3 - 2')
        self.assertEqual(node.operator, '-')
        self.assertEqual(node.left.operator, '-')
        self.assertEqual((node.left.left.value, node.left.right.value, node.right.value), (10, 3, 2))

    def test_division_and_modulo(self):
        node = parse_complete_expression('20 / 5 % 3')
        self.assertEqual(node.operator, '%')
        self.assertEqual(node.left.operator, '/')
        self.assertEqual((node.left.left.value, node.left.right.value, node.right.value), (20, 5, 3))

    def test_unary_minus(self):
        node = parse_complete_expression('-x * 2')
        self.assertEqual(node.operator, '*')
        self.assertIsInstance(node.left, UnaryOpNode)
        self.assertEqual(node.left.operator, '-')
        self.assertEqual(node.left.operand.name, 'x')
        self.assertEqual(node.right.value, 2)

    def test_comparison_precedence(self):
        node = parse_complete_expression('2 + 3 > 4')
        self.assertEqual(node.operator, '>')
        self.assertEqual(node.left.operator, '+')
        self.assertEqual((node.left.left.value, node.left.right.value, node.right.value), (2, 3, 4))

    def test_missing_operand(self):
        with self.assertRaisesRegex(ParserError, r'line 1, column 4: unexpected token EOF'):
            parse_complete_expression('2 +')

    def test_missing_parenthesis(self):
        with self.assertRaisesRegex(ParserError, r'expected RPAREN but got EOF'):
            parse_complete_expression('(2 + 3')

    def test_extra_token(self):
        with self.assertRaisesRegex(ParserError, r'expected EOF but got NUMBER'):
            parse_complete_expression('2 3')


if __name__ == '__main__':
    unittest.main(verbosity=2)
