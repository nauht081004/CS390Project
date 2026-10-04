from lexer import lex, LexerError
from ast_nodes import (
    NumberNode, VariableNode, BooleanNode, StringNode,
    UnaryOpNode, BinaryOpNode,
)


class ParserError(Exception):
    pass


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    # --- helpers every parsing method relies on ---

    def current(self):
        return self.tokens[self.pos]

    def peek_type(self):
        return self.current().type

    def advance(self):
        tok = self.current()
        if tok.type != "EOF":
            self.pos += 1
        return tok

    def expect(self, type_):
        tok = self.current()
        if tok.type != type_:
            raise ParserError(
                f"Syntax error at line {tok.line}, column {tok.column}: "
                f"expected {type_} but got {tok.type} ({tok.value!r})"
            )
        return self.advance()

    # --- expression parsing, lowest precedence to highest ---

    def parse_expression(self):
        return self.parse_comparison()

    def parse_comparison(self):
        node = self.parse_additive()
        comparison_types = {"EQUAL", "NOT_EQUAL", "LESS", "GREATER",
                            "LESS_EQUAL", "GREATER_EQUAL"}
        while self.peek_type() in comparison_types:
            op_token = self.advance()
            right = self.parse_additive()
            node = BinaryOpNode(op_token.value, node, right)
        return node

    def parse_additive(self):
        node = self.parse_term()
        while self.peek_type() in ("PLUS", "MINUS"):
            op_token = self.advance()
            right = self.parse_term()
            node = BinaryOpNode(op_token.value, node, right)
        return node

    def parse_term(self):
        node = self.parse_unary()
        while self.peek_type() in ("MULTIPLY", "DIVIDE", "MODULO"):
            op_token = self.advance()
            right = self.parse_unary()
            node = BinaryOpNode(op_token.value, node, right)
        return node

    def parse_unary(self):
        if self.peek_type() == "MINUS":
            op_token = self.advance()
            operand = self.parse_unary()
            return UnaryOpNode(op_token.value, operand)
        return self.parse_primary()

    def parse_primary(self):
        tok = self.current()

        if tok.type == "NUMBER":
            self.advance()
            value = float(tok.value) if "." in tok.value else int(tok.value)
            return NumberNode(value)

        if tok.type == "ID":
            self.advance()
            return VariableNode(tok.value)

        if tok.type == "TRUE":
            self.advance()
            return BooleanNode(True)

        if tok.type == "FALSE":
            self.advance()
            return BooleanNode(False)

        if tok.type == "STRING":
            self.advance()
            return StringNode(tok.value)

        if tok.type == "LPAREN":
            self.advance()
            node = self.parse_expression()
            self.expect("RPAREN")
            return node

        raise ParserError(
            f"Syntax error at line {tok.line}, column {tok.column}: "
            f"unexpected token {tok.type} ({tok.value!r})"
        )
