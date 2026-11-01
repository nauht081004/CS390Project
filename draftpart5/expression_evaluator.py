"""Expression evaluator for ANVI: turns expression AST nodes into real values."""
from ast_nodes import (
    NumberNode, VariableNode, BooleanNode, StringNode,
    UnaryOpNode, BinaryOpNode, FunctionCallNode,
)
from environment import EnvironmentError


class InterpreterError(RuntimeError):
    """Raised for any runtime error while evaluating an expression."""


def is_number(value):
    # In Python, True/False count as ints, so check the exact type.
    return type(value) in (int, float)


def describe(value):
    if type(value) is bool:
        return "a boolean"
    if is_number(value):
        return "a number"
    if type(value) is str:
        return "a string"
    return type(value).__name__


def values_equal(left, right):
    # A boolean is never equal to a number (so 1 == T is false).
    if type(left) is bool or type(right) is bool:
        return type(left) is type(right) and left == right
    return left == right


def invalid_operation(op, left, right):
    return InterpreterError(
        f"Invalid operation: cannot use '{op}' on {describe(left)} and {describe(right)}"
    )


def evaluate(node, environment, call_function=None):
    """Compute the value of an expression node.

    call_function (Part 5) is supplied by the interpreter. It takes a
    FunctionCallNode, runs the user's function, and returns its result.
    """
    if isinstance(node, (NumberNode, BooleanNode, StringNode)):
        return node.value

    if isinstance(node, VariableNode):
        try:
            return environment.get(node.name)
        except EnvironmentError as error:
            raise InterpreterError(str(error))

    if isinstance(node, FunctionCallNode):                      # Part 5
        if call_function is None:
            raise InterpreterError("Function calls are not available here")
        return call_function(node)

    if isinstance(node, UnaryOpNode):
        return evaluate_unary(node, environment, call_function)

    if isinstance(node, BinaryOpNode):
        return evaluate_binary(node, environment, call_function)

    raise InterpreterError(f"Cannot evaluate node type: {type(node).__name__}")


def evaluate_unary(node, environment, call_function=None):
    value = evaluate(node.operand, environment, call_function)
    if node.operator == "-":
        if not is_number(value):
            raise InterpreterError(
                f"Invalid operation: cannot negate {describe(value)}")
        return -value
    raise InterpreterError(f"Unknown unary operator '{node.operator}'")


def evaluate_binary(node, environment, call_function=None):
    op = node.operator
    left = evaluate(node.left, environment, call_function)
    right = evaluate(node.right, environment, call_function)

    # Equality works on any two values.
    if op == "==":
        return values_equal(left, right)
    if op == "!=":
        return not values_equal(left, right)

    # + adds numbers or joins two strings.
    if op == "+":
        if is_number(left) and is_number(right):
            return left + right
        if type(left) is str and type(right) is str:
            return left + right
        raise invalid_operation(op, left, right)

    # Everything else needs two numbers.
    if not (is_number(left) and is_number(right)):
        raise invalid_operation(op, left, right)

    if op == "<":
        return left < right
    if op == ">":
        return left > right
    if op == "<=":
        return left <= right
    if op == ">=":
        return left >= right
    if op == "-":
        return left - right
    if op == "*":
        return left * right

    if op in ("/", "%"):
        if right == 0:
            name = "Division" if op == "/" else "Modulo"
            raise InterpreterError(f"{name} by zero")
        if op == "%":
            return left % right
        # Whole-number results stay integers (10 / 2 is 5, not 5.0).
        if type(left) is int and type(right) is int and left % right == 0:
            return left // right
        return left / right

    raise InterpreterError(f"Unknown operator '{op}'")
