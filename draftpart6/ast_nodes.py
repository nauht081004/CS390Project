"""AST node definitions for ANVI."""
class ASTNode:
    def to_string(self, indent=0): raise NotImplementedError

class ProgramNode(ASTNode):
    def __init__(self, statements): self.statements = statements
    def to_string(self, indent=0): return "\n".join([" "*indent+"ProgramNode"]+[s.to_string(indent+2) for s in self.statements])
class NumberNode(ASTNode):
    def __init__(self, value): self.value=value
    def to_string(self, indent=0): return " "*indent+f"NumberNode: {self.value}"
class VariableNode(ASTNode):
    def __init__(self, name): self.name=name
    def to_string(self, indent=0): return " "*indent+f"VariableNode: {self.name}"
class BooleanNode(ASTNode):
    def __init__(self, value): self.value=value
    def to_string(self, indent=0): return " "*indent+f"BooleanNode: {self.value}"
class StringNode(ASTNode):
    def __init__(self, value): self.value=value
    def to_string(self, indent=0): return " "*indent+f"StringNode: {self.value!r}"
class UnaryOpNode(ASTNode):
    def __init__(self, operator, operand): self.operator,self.operand=operator,operand
    def to_string(self, indent=0): return "\n".join([" "*indent+f"UnaryOpNode: {self.operator}",self.operand.to_string(indent+2)])
class BinaryOpNode(ASTNode):
    def __init__(self, operator, left, right): self.operator,self.left,self.right=operator,left,right
    def to_string(self, indent=0): return "\n".join([" "*indent+f"BinaryOpNode: {self.operator}",self.left.to_string(indent+2),self.right.to_string(indent+2)])
class AssignmentNode(ASTNode):
    def __init__(self, variable, expression, is_declaration=True): self.variable,self.expression,self.is_declaration=variable,expression,is_declaration
    def to_string(self, indent=0): return "\n".join([" "*indent+("AssignmentNode" if self.is_declaration else "ReassignmentNode"),self.variable.to_string(indent+2),self.expression.to_string(indent+2)])
class PrintNode(ASTNode):
    def __init__(self, expression): self.expression=expression
    def to_string(self, indent=0): return "\n".join([" "*indent+"PrintNode",self.expression.to_string(indent+2)])
class ExpressionStatementNode(ASTNode):
    def __init__(self, expression): self.expression=expression
    def to_string(self, indent=0): return "\n".join([" "*indent+"ExpressionStatementNode",self.expression.to_string(indent+2)])
class BlockNode(ASTNode):
    def __init__(self, statements): self.statements=statements
    def to_string(self, indent=0): return "\n".join([" "*indent+"BlockNode"]+[s.to_string(indent+2) for s in self.statements])
class IfNode(ASTNode):
    def __init__(self, condition, then_branch, else_branch=None): self.condition,self.then_branch,self.else_branch=condition,then_branch,else_branch
    def to_string(self, indent=0): return "\n".join([" "*indent+"IfNode",self.condition.to_string(indent+2),self.then_branch.to_string(indent+2)]+([self.else_branch.to_string(indent+2)] if self.else_branch else []))
class WhileNode(ASTNode):
    def __init__(self, condition, body): self.condition,self.body=condition,body
    def to_string(self, indent=0): return "\n".join([" "*indent+"WhileNode",self.condition.to_string(indent+2),self.body.to_string(indent+2)])
class FunctionDefNode(ASTNode):
    def __init__(self, name, parameters, body): self.name,self.parameters,self.body=name,parameters,body
    def to_string(self, indent=0): return " "*indent+f"FunctionDefNode: {self.name}({', '.join(self.parameters)})\n"+self.body.to_string(indent+2)
class FunctionCallNode(ASTNode):
    def __init__(self, name, arguments): self.name,self.arguments=name,arguments
    def to_string(self, indent=0): return "\n".join([" "*indent+f"FunctionCallNode: {self.name}"]+[a.to_string(indent+2) for a in self.arguments])
class ReturnNode(ASTNode):
    def __init__(self, expression=None): self.expression=expression
    def to_string(self, indent=0): return " "*indent+"ReturnNode"+("\n"+self.expression.to_string(indent+2) if self.expression else "")
