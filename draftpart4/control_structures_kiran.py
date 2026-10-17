"""Kiran's statement executor. No dependency on the demo evaluator/environment."""
from ast_nodes import (ProgramNode, BlockNode, AssignmentNode, PrintNode,
                       IfNode, WhileNode, ExpressionStatementNode)


class StatementExecutor:
    def __init__(self, environment, evaluate, output=print):
        """evaluate(expression, environment) returns a value.

        environment implements define(name, value) and assign(name, value).
        output(value) receives each printed value (print by default).
        Runtime errors propagate to the caller; they are not silently ignored.
        """
        self.environment = environment
        self.evaluate = evaluate
        self.output = output

    def condition_is_true(self, expression):
        value = self.evaluate(expression, self.environment)
        # Explicit policy: booleans or numbers only; zero is false.
        if type(value) not in (bool, int, float):
            raise RuntimeError("Condition must be a boolean or number")
        return bool(value)

    def execute(self, node):
        if isinstance(node, (ProgramNode, BlockNode)):
            # Blocks share the environment so loop updates remain visible.
            for statement in node.statements:
                self.execute(statement)
        elif isinstance(node, AssignmentNode):
            value = self.evaluate(node.expression, self.environment)
            name = node.variable.name
            if node.is_declaration:
                self.environment.define(name, value)
            else:
                self.environment.assign(name, value)
        elif isinstance(node, PrintNode):
            self.output(self.evaluate(node.expression, self.environment))
        elif isinstance(node, IfNode):
            if self.condition_is_true(node.condition):
                self.execute(node.then_branch)
            elif node.else_branch is not None:
                self.execute(node.else_branch)
        elif isinstance(node, WhileNode):
            # Evaluate again after every execution of the body.
            while self.condition_is_true(node.condition):
                self.execute(node.body)
        elif isinstance(node, ExpressionStatementNode):
            self.evaluate(node.expression, self.environment)
        else:
            raise RuntimeError(f"Unsupported statement: {type(node).__name__}")
