class ASTNode:
    """Base class for all ANVI AST nodes."""

    def to_string(self, indent=0):
        raise NotImplementedError


class ProgramNode(ASTNode):
    def __init__(self, statements):
        self.statements = statements

    def to_string(self, indent=0):
        lines = [" " * indent + "ProgramNode"]
        for statement in self.statements:
            lines.append(statement.to_string(indent + 2))
        return "\n".join(lines)


class NumberNode(ASTNode):
    def __init__(self, value):
        self.value = value

    def to_string(self, indent=0):
        return " " * indent + f"NumberNode: {self.value}"


class VariableNode(ASTNode):
    def __init__(self, name):
        self.name = name

    def to_string(self, indent=0):
        return " " * indent + f"VariableNode: {self.name}"


class BooleanNode(ASTNode):
    def __init__(self, value):
        self.value = value

    def to_string(self, indent=0):
        return " " * indent + f"BooleanNode: {self.value}"


class StringNode(ASTNode):
    def __init__(self, value):
        self.value = value

    def to_string(self, indent=0):
        return " " * indent + f"StringNode: {self.value!r}"


class UnaryOpNode(ASTNode):
    def __init__(self, operator, operand):
        self.operator = operator
        self.operand = operand

    def to_string(self, indent=0):
        lines = [" " * indent + f"UnaryOpNode: {self.operator}"]
        lines.append(self.operand.to_string(indent + 2))
        return "\n".join(lines)


class BinaryOpNode(ASTNode):
    def __init__(self, operator, left, right):
        self.operator = operator
        self.left = left
        self.right = right

    def to_string(self, indent=0):
        lines = [" " * indent + f"BinaryOpNode: {self.operator}"]
        lines.append(self.left.to_string(indent + 2))
        lines.append(self.right.to_string(indent + 2))
        return "\n".join(lines)


class AssignmentNode(ASTNode):
    def __init__(self, variable, expression):
        self.variable = variable
        self.expression = expression

    def to_string(self, indent=0):
        lines = [" " * indent + "AssignmentNode"]
        lines.append(self.variable.to_string(indent + 2))
        lines.append(self.expression.to_string(indent + 2))
        return "\n".join(lines)


class PrintNode(ASTNode):
    def __init__(self, expression):
        self.expression = expression

    def to_string(self, indent=0):
        lines = [" " * indent + "PrintNode"]
        lines.append(self.expression.to_string(indent + 2))
        return "\n".join(lines)


class ExpressionStatementNode(ASTNode):
    """Allows a standalone expression for parser/AST demonstrations."""
    def __init__(self, expression):
        self.expression = expression

    def to_string(self, indent=0):
        lines = [" " * indent + "ExpressionStatementNode"]
        lines.append(self.expression.to_string(indent + 2))
        return "\n".join(lines)
