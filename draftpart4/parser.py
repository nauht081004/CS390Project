"""Recursive-descent parser for ANVI Part 4."""
from lexer import lex, LexerError
from ast_nodes import (ProgramNode, NumberNode, VariableNode, BooleanNode,
    StringNode, UnaryOpNode, BinaryOpNode, AssignmentNode, PrintNode,
    ExpressionStatementNode, BlockNode, IfNode, WhileNode)

class ParserError(Exception):
    def __init__(self, message, token=None):
        if token is not None:
            message = (f"Parser error at line {token.line}, column {token.column}: {message} "
                       f"(found {token.type}" + (f", value={token.value!r}" if token.value else "") + ")")
        super().__init__(message)
        self.token = token

class Parser:
    def __init__(self, tokens): self.tokens, self.current = tokens, 0
    def peek(self): return self.tokens[self.current]
    def is_at_end(self): return self.peek().type == "EOF"
    def advance(self):
        token = self.peek()
        if not self.is_at_end(): self.current += 1
        return token
    def check(self, *types): return self.peek().type in types
    def match(self, *types):
        if self.check(*types): return self.advance()
        return None
    def consume(self, token_type, message):
        if self.check(token_type): return self.advance()
        raise ParserError(message, self.peek())

    def parse(self):
        statements = []
        while not self.is_at_end(): statements.append(self.parse_statement())
        return ProgramNode(statements)

    def parse_statement(self):
        if self.check("LET"): return self.parse_assignment(True)
        if self.check("ID") and self.current + 1 < len(self.tokens) and self.tokens[self.current + 1].type == "ASSIGN":
            return self.parse_assignment(False)
        if self.check("DISPLAY"): return self.parse_print()
        if self.check("IF"): return self.parse_if()
        if self.check("WLOOP"): return self.parse_while()
        if self.check("LBRACE"): return self.parse_block()
        if self.check("SEMICOLON"): raise ParserError("empty statements are not allowed", self.peek())
        expression = self.parse_expression()
        # Permit a single bare expression at EOF for the Part 3 AST demo;
        # expressions inside full programs still require semicolons.
        if not self.is_at_end():
            self.consume("SEMICOLON", "expected ';' after expression")
        return ExpressionStatementNode(expression)

    def parse_assignment(self, declaration):
        if declaration: self.consume("LET", "expected 'let'")
        name = self.consume("ID", "expected variable name")
        self.consume("ASSIGN", "expected '=' after variable name")
        if self.check("SEMICOLON"): raise ParserError("expected expression after '='", self.peek())
        expression = self.parse_expression()
        self.consume("SEMICOLON", "expected ';' after assignment")
        return AssignmentNode(VariableNode(name.value), expression, declaration)

    def parse_print(self):
        self.advance()  # DISPLAY
        if self.check("SEMICOLON"): raise ParserError("expected expression after display", self.peek())
        expression = self.parse_expression()
        self.consume("SEMICOLON", "expected ';' after display")
        return PrintNode(expression)

    def parse_if(self):
        self.consume("IF", "expected 'if'")
        self.consume("LPAREN", "expected '(' after 'if'")
        condition = self.parse_expression()
        self.consume("RPAREN", "expected ')' after if condition")
        then_branch = self.parse_block()
        else_branch = None
        if self.match("ELSE"): else_branch = self.parse_block()
        return IfNode(condition, then_branch, else_branch)

    def parse_while(self):
        self.advance()  # WLOOP
        self.consume("LPAREN", "expected '(' after 'wloop'")
        condition = self.parse_expression()
        self.consume("RPAREN", "expected ')' after wloop condition")
        body = self.parse_block()
        return WhileNode(condition, body)

    def parse_block(self):
        self.consume("LBRACE", "expected '{' to begin block")
        statements = []
        while not self.check("RBRACE") and not self.is_at_end():
            statements.append(self.parse_statement())
        self.consume("RBRACE", "expected '}' after block")
        return BlockNode(statements)

    def parse_expression(self): return self.parse_comparison()
    def parse_comparison(self):
        expr = self.parse_addition()
        while self.check("EQUAL", "NOT_EQUAL", "LESS", "GREATER", "LESS_EQUAL", "GREATER_EQUAL"):
            op = self.advance(); expr = BinaryOpNode(op.value, expr, self.parse_addition())
        return expr
    def parse_addition(self):
        expr = self.parse_multiplication()
        while self.check("PLUS", "MINUS"):
            op = self.advance(); expr = BinaryOpNode(op.value, expr, self.parse_multiplication())
        return expr
    def parse_multiplication(self):
        expr = self.parse_unary()
        while self.check("MULTIPLY", "DIVIDE", "MODULO"):
            op = self.advance(); expr = BinaryOpNode(op.value, expr, self.parse_unary())
        return expr
    def parse_unary(self):
        if self.match("PLUS"): return UnaryOpNode("+", self.parse_unary())
        if self.match("MINUS"): return UnaryOpNode("-", self.parse_unary())
        return self.parse_primary()
    def parse_primary(self):
        token = self.peek()
        if self.match("NUMBER"):
            return NumberNode(float(token.value) if "." in token.value else int(token.value))
        if self.match("ID"): return VariableNode(token.value)
        if self.match("TRUE"): return BooleanNode(True)
        if self.match("FALSE"): return BooleanNode(False)
        if self.match("STRING"): return StringNode(token.value)
        if self.match("LPAREN"):
            expr = self.parse_expression(); self.consume("RPAREN", "expected ')' after expression"); return expr
        raise ParserError("expected expression", token)

def parse_source(source): return Parser(lex(source)).parse()
def parse_tokens(tokens): return Parser(tokens).parse()
