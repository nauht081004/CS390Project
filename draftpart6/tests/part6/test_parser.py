"""Parser regression tests for the ANVI Part 6 syntax."""
import unittest
from parser import ParserError, parse_source
from ast_nodes import (
    ProgramNode, NumberNode, BooleanNode, StringNode, UnaryOpNode,
    BinaryOpNode, AssignmentNode, PrintNode, BlockNode, IfNode,
    WhileNode, FunctionDefNode, FunctionCallNode, ReturnNode,
)


class ParserPart6Tests(unittest.TestCase):
    def test_arithmetic_precedence(self):
        ast = parse_source("2 + 3 * 4")
        expr = ast.statements[0].expression
        self.assertIsInstance(ast, ProgramNode)
        self.assertEqual(expr.operator, "+")
        self.assertEqual(expr.right.operator, "*")

    def test_parentheses_override_precedence(self):
        ast = parse_source("(2 + 3) * 4")
        expr = ast.statements[0].expression
        self.assertEqual(expr.operator, "*")
        self.assertEqual(expr.left.operator, "+")

    def test_unary_minus(self):
        ast = parse_source("let x = -5 + 2;")
        expr = ast.statements[0].expression
        self.assertIsInstance(expr.left, UnaryOpNode)
        self.assertEqual(expr.right.value, 2)

    def test_comparison_expression(self):
        ast = parse_source("let result = 5 >= 3;")
        self.assertEqual(ast.statements[0].expression.operator, ">=")

    def test_boolean_and_string_literals(self):
        ast = parse_source('let yes = T; let no = F; let message = "hello";')
        self.assertIsInstance(ast.statements[0].expression, BooleanNode)
        self.assertIsInstance(ast.statements[1].expression, BooleanNode)
        self.assertIsInstance(ast.statements[2].expression, StringNode)

    def test_declaration_and_reassignment(self):
        ast = parse_source("let count = 1; count = count + 1;")
        self.assertTrue(ast.statements[0].is_declaration)
        self.assertFalse(ast.statements[1].is_declaration)

    def test_display_parentheses_required(self):
        ast = parse_source("display(7); display(8);")
        self.assertEqual(len(ast.statements), 2)
        self.assertIsInstance(ast.statements[0], PrintNode)
        self.assertEqual(ast.statements[0].expression.value, 7)

    def test_display_without_parentheses_rejected(self):
        with self.assertRaises(ParserError):
            parse_source("display 7;")

    def test_display_parentheses_must_enclose_entire_expression(self):
        with self.assertRaises(ParserError):
            parse_source("display (2 + 3) * 4;")

    def test_display_parenthesized_expression_valid(self):
        ast = parse_source("display((2 + 3) * 4);")
        self.assertIsInstance(ast.statements[0], PrintNode)
        self.assertEqual(ast.statements[0].expression.operator, "*")

    def test_if_else(self):
        ast = parse_source("if (x > 0) { display(x); } else { display(0); }")
        node = ast.statements[0]
        self.assertIsInstance(node, IfNode)
        self.assertIsInstance(node.then_branch, BlockNode)
        self.assertIsInstance(node.else_branch, BlockNode)

    def test_if_without_else(self):
        ast = parse_source("if (T) { display(1); }")
        self.assertIsNone(ast.statements[0].else_branch)

    def test_wloop(self):
        ast = parse_source("wloop (x < 3) { x = x + 1; }")
        self.assertIsInstance(ast.statements[0], WhileNode)

    def test_function_definition(self):
        ast = parse_source("func add(a, b) { return a + b; }")
        node = ast.statements[0]
        self.assertIsInstance(node, FunctionDefNode)
        self.assertEqual(node.parameters, ["a", "b"])

    def test_function_call_with_arguments(self):
        ast = parse_source("let total = add(2, 3 * 4);")
        call = ast.statements[0].expression
        self.assertIsInstance(call, FunctionCallNode)
        self.assertEqual(len(call.arguments), 2)

    def test_function_call_without_arguments(self):
        ast = parse_source("display(getValue());")
        call = ast.statements[0].expression
        self.assertIsInstance(call, FunctionCallNode)
        self.assertEqual(call.arguments, [])

    def test_return_without_expression(self):
        ast = parse_source("func stop() { return; }")
        self.assertIsInstance(ast.statements[0].body.statements[0], ReturnNode)
        self.assertIsNone(ast.statements[0].body.statements[0].expression)

    def test_duplicate_function_parameters_rejected(self):
        with self.assertRaises(ParserError):
            parse_source("func bad(x, x) { return x; }")

    def test_missing_expression_after_assignment_rejected(self):
        with self.assertRaises(ParserError):
            parse_source("let x = ;")

    def test_missing_closing_display_parenthesis_rejected(self):
        with self.assertRaises(ParserError):
            parse_source("display(2 + 3;")

    def test_empty_statement_rejected(self):
        with self.assertRaises(ParserError):
            parse_source(";")


if __name__ == "__main__":
    unittest.main(verbosity=2)
