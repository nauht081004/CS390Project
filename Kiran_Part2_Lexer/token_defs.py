"""Reference token definitions; reconcile names with the group's lexer."""
from dataclasses import dataclass

KEYWORDS = {
    'let': 'LET', 'if': 'IF', 'else': 'ELSE', 'wloop': 'WLOOP',
    'floop': 'FLOOP', 'func': 'FUNC', 'return': 'RETURN',
    'display': 'DISPLAY', 'T': 'TRUE', 'F': 'FALSE',
}
OPERATORS = {
    '==': 'EQ', '!=': 'NE', '<=': 'LE', '>=': 'GE',
    '+': 'PLUS', '-': 'MINUS', '*': 'STAR', '/': 'SLASH',
    '%': 'MOD', '<': 'LT', '>': 'GT', '=': 'ASSIGN',
    '(': 'LPAREN', ')': 'RPAREN', '{': 'LBRACE', '}': 'RBRACE',
    '[': 'LBRACKET', ']': 'RBRACKET', ',': 'COMMA', ';': 'SEMICOLON',
}

@dataclass(frozen=True)
class Token:
    type: str
    lexeme: str
    line: int
    column: int

    def __str__(self):
        return f"{self.type}({self.lexeme}) @ {self.line}:{self.column}"
