import unittest

from ast_nodes import (
    ProgramNode,
    NumberNode,
    VariableNode,
    BooleanNode,
    StringNode,
    UnaryOpNode,
    BinaryOpNode,
    AssignmentNode,
    PrintNode,
    ExpressionStatementNode,
    BlockNode,
    IfNode,
    WhileNode,
    FunctionDefNode,
    FunctionCallNode,
    ReturnNode,
)


class ASTNodePart6Tests(unittest.TestCase):
    def test_number_node(self):
        node = NumberNode(42)
        self.assertEqual(node.value, 42)
        self.assertEqual(node.to_string(), "NumberNode: 42")

    def test_variable_node(self):
        node = VariableNode("total")
        self.assertEqual(node.name, "total")
        self.assertEqual(node.to_string(), "VariableNode: total")

    def test_boolean_true_node(self):
        node = BooleanNode(True)
        self.assertIs(node.value, True)
        self.assertEqual(node.to_string(), "BooleanNode: True")

    def test_boolean_false_node(self):
        node = BooleanNode(False)
        self.assertIs(node.value, False)
        self.assertEqual(node.to_string(), "BooleanNode: False")

    def test_string_node(self):
        node = StringNode("hello")
        self.assertEqual(node.value, "hello")
        self.assertEqual(node.to_string(), "StringNode: 'hello'")

    def test_unary_operation_node(self):
        node = UnaryOpNode("-", NumberNode(5))
        self.assertEqual(node.operator, "-")
        self.assertIsInstance(node.operand, NumberNode)
        self.assertIn("UnaryOpNode: -", node.to_string())
        self.assertIn("NumberNode: 5", node.to_string())

    def test_binary_operation_node(self):
        node = BinaryOpNode("+", NumberNode(2), NumberNode(3))
        self.assertEqual(node.operator, "+")
        self.assertIsInstance(node.left, NumberNode)
        self.assertIsInstance(node.right, NumberNode)
        self.assertIn("BinaryOpNode: +", node.to_string())

    def test_nested_expression_tree(self):
        # Represents 2 + (3 * 4), with multiplication nested on the right.
        node = BinaryOpNode(
            "+",
            NumberNode(2),
            BinaryOpNode("*", NumberNode(3), NumberNode(4)),
        )
        rendered = node.to_string()
        self.assertLess(rendered.index("BinaryOpNode: +"),
                        rendered.index("BinaryOpNode: *"))

    def test_assignment_declaration(self):
        node = AssignmentNode(VariableNode("x"), NumberNode(10))
        self.assertTrue(node.is_declaration)
        self.assertIn("AssignmentNode", node.to_string())
        self.assertIn("VariableNode: x", node.to_string())

    def test_reassignment(self):
        node = AssignmentNode(
            VariableNode("x"), NumberNode(20), is_declaration=False
        )
        self.assertFalse(node.is_declaration)
        self.assertIn("ReassignmentNode", node.to_string())

    def test_print_node(self):
        node = PrintNode(StringNode("ANVI"))
        self.assertIsInstance(node.expression, StringNode)
        self.assertIn("PrintNode", node.to_string())

    def test_expression_statement_node(self):
        node = ExpressionStatementNode(
            FunctionCallNode("calculate", [NumberNode(2)])
        )
        self.assertIsInstance(node.expression, FunctionCallNode)
        self.assertIn("ExpressionStatementNode", node.to_string())

    def test_block_node(self):
        node = BlockNode([PrintNode(NumberNode(1)), PrintNode(NumberNode(2))])
        self.assertEqual(len(node.statements), 2)
        self.assertIn("BlockNode", node.to_string())

    def test_if_node_without_else(self):
        node = IfNode(BooleanNode(True), BlockNode([]))
        self.assertIsNone(node.else_branch)
        self.assertIn("IfNode", node.to_string())

    def test_if_node_with_else(self):
        node = IfNode(
            BooleanNode(False),
            BlockNode([PrintNode(NumberNode(1))]),
            BlockNode([PrintNode(NumberNode(2))]),
        )
        self.assertIsNotNone(node.else_branch)
        self.assertIn("IfNode", node.to_string())
        self.assertEqual(node.to_string().count("BlockNode"), 2)

    def test_while_node(self):
        node = WhileNode(BooleanNode(True), BlockNode([]))
        self.assertIsInstance(node.condition, BooleanNode)
        self.assertIsInstance(node.body, BlockNode)
        self.assertIn("WhileNode", node.to_string())

    def test_function_definition_node(self):
        body = BlockNode([ReturnNode(VariableNode("value"))])
        node = FunctionDefNode("identity", ["value"], body)
        self.assertEqual(node.name, "identity")
        self.assertEqual(node.parameters, ["value"])
        self.assertIs(node.body, body)
        self.assertIn("FunctionDefNode: identity(value)", node.to_string())

    def test_function_call_node(self):
        node = FunctionCallNode("add", [NumberNode(2), NumberNode(3)])
        self.assertEqual(node.name, "add")
        self.assertEqual(len(node.arguments), 2)
        self.assertIn("FunctionCallNode: add", node.to_string())

    def test_return_node_with_expression(self):
        node = ReturnNode(NumberNode(7))
        self.assertIsInstance(node.expression, NumberNode)
        self.assertIn("ReturnNode", node.to_string())
        self.assertIn("NumberNode: 7", node.to_string())

    def test_return_node_without_expression(self):
        node = ReturnNode()
        self.assertIsNone(node.expression)
        self.assertEqual(node.to_string(), "ReturnNode")

    def test_program_node(self):
        node = ProgramNode([
            AssignmentNode(VariableNode("x"), NumberNode(1)),
            PrintNode(VariableNode("x")),
        ])
        self.assertEqual(len(node.statements), 2)
        self.assertIn("ProgramNode", node.to_string())
        self.assertIn("AssignmentNode", node.to_string())
        self.assertIn("PrintNode", node.to_string())


if __name__ == "__main__":
    unittest.main()
