import unittest
from parser import parse_source, ParserError
from ast_nodes import (
    ProgramNode, AssignmentNode, PrintNode, ExpressionStatementNode,
    BlockNode, FunctionDefNode, FunctionCallNode, ReturnNode,
    NumberNode, VariableNode, BinaryOpNode,
)


class FunctionParserTests(unittest.TestCase):

    def test_function_definition_with_parameters(self):
        tree = parse_source("func add(a, b) { return a + b; }")
        function = tree.statements[0]
        self.assertIsInstance(function, FunctionDefNode)
        self.assertEqual(function.name, "add")
        self.assertEqual(function.parameters, ["a", "b"])
        self.assertIsInstance(function.body, BlockNode)
        statement = function.body.statements[0]
        self.assertIsInstance(statement, ReturnNode)
        self.assertEqual(statement.expression.operator, "+")

    def test_function_without_parameters(self):
        tree = parse_source("func hello() { display(1); }")
        function = tree.statements[0]
        self.assertEqual(function.parameters, [])
        self.assertIsInstance(function.body.statements[0], PrintNode)

    def test_call_inside_assignment(self):
        tree = parse_source("let result = add(10, 20);")
        assignment = tree.statements[0]
        self.assertIsInstance(assignment, AssignmentNode)
        call = assignment.expression
        self.assertIsInstance(call, FunctionCallNode)
        self.assertEqual(call.name, "add")
        self.assertEqual([a.value for a in call.arguments], [10, 20])

    def test_call_as_statement(self):
        tree = parse_source("test();")
        statement = tree.statements[0]
        self.assertIsInstance(statement, ExpressionStatementNode)
        self.assertIsInstance(statement.expression, FunctionCallNode)
        self.assertEqual(statement.expression.arguments, [])

    def test_call_inside_display(self):
        tree = parse_source("display(add(1, 2));")
        statement = tree.statements[0]
        self.assertIsInstance(statement, PrintNode)
        self.assertIsInstance(statement.expression, FunctionCallNode)

    def test_arguments_can_be_expressions_and_calls(self):
        tree = parse_source("add(1 + 2, add(3, 4));")
        call = tree.statements[0].expression
        self.assertIsInstance(call.arguments[0], BinaryOpNode)
        self.assertIsInstance(call.arguments[1], FunctionCallNode)

    def test_call_respects_operator_precedence(self):
        tree = parse_source("let y = 2 * add(1, 2) + 3;")
        expression = tree.statements[0].expression
        self.assertEqual(expression.operator, "+")
        self.assertEqual(expression.left.operator, "*")
        self.assertIsInstance(expression.left.right, FunctionCallNode)

    def test_scope_example_from_assignment(self):
        source = """
        let x = 10;
        func test() {
            let x = 20;
            display(x);
        }
        test();
        display(x);
        """
        tree = parse_source(source)
        kinds = [type(s) for s in tree.statements]
        self.assertEqual(kinds, [AssignmentNode, FunctionDefNode,
                                 ExpressionStatementNode, PrintNode])

    def test_recursive_function_shape(self):
        source = "func fact(n) { if (n <= 1) { return 1; } return n * fact(n - 1); }"
        function = parse_source(source).statements[0]
        self.assertEqual(len(function.body.statements), 2)
        last = function.body.statements[1]
        self.assertIsInstance(last, ReturnNode)
        self.assertEqual(last.expression.operator, "*")
        self.assertIsInstance(last.expression.right, FunctionCallNode)
        self.assertEqual(last.expression.right.name, "fact")

    def test_error_missing_closing_parenthesis_in_call(self):
        with self.assertRaisesRegex(ParserError, "expected '\\)' after arguments"):
            parse_source("add(1, 2;")

    def test_error_trailing_comma_in_call(self):
        with self.assertRaisesRegex(ParserError, "expected expression"):
            parse_source("add(1, );")

    def test_error_missing_function_name(self):
        with self.assertRaisesRegex(ParserError, "expected function name"):
            parse_source("func (a) { return a; }")

    def test_error_missing_function_body(self):
        with self.assertRaisesRegex(ParserError, "expected '\\{' to begin block"):
            parse_source("func f(a) return a;")

    def test_error_duplicate_parameter(self):
        with self.assertRaisesRegex(ParserError, "duplicate parameter 'a'"):
            parse_source("func f(a, a) { return a; }")

    def test_error_return_outside_function(self):
        with self.assertRaisesRegex(ParserError, "only allowed inside a function"):
            parse_source("return 5;")

    def test_error_return_without_value(self):
        with self.assertRaisesRegex(ParserError, "expected expression after 'return'"):
            parse_source("func f() { return; }")

    def test_error_return_missing_semicolon(self):
        with self.assertRaisesRegex(ParserError, "expected ';' after return"):
            parse_source("func f() { return 1 }")


if __name__ == "__main__":
    unittest.main(verbosity=2)