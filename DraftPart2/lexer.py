# 1. Import libraries
from dataclasses import dataclass

# 2. Define Token
@dataclass
class Token:
    type: str
    value: str
    line: int
    column: int


# 3. Define ANVI keywords
KEYWORDS = {
    "let": "LET",
    "if": "IF",
    "else": "ELSE",
    "wloop": "WLOOP",
    "floop": "FLOOP",
    "func": "FUNC",
    "return": "RETURN",
    "display": "DISPLAY",
    "T": "TRUE",
    "F": "FALSE",
    "try": "TRY",
    "catch": "CATCH",
}


# 4. Define operators and symbols
SINGLE_CHAR_TOKENS = {
    "+": "PLUS",
    "-": "MINUS",
    "*": "MULTIPLY",
    "/": "DIVIDE",
    "%": "MODULO",
    "=": "ASSIGN",
    "(": "LPAREN",
    ")": "RPAREN",
    "{": "LBRACE",
    "}": "RBRACE",
    ",": "COMMA",
    ";": "SEMICOLON",
}

COMPARISON_TOKENS = {
    "==": "EQUAL",
    "!=": "NOT_EQUAL",
    "<": "LESS",
    ">": "GREATER",
    "<=": "LESS_EQUAL",
    ">=": "GREATER_EQUAL",
}


# 5. Define Lexer Error
class LexerError(Exception):
    pass


# 6. Define Lexer class
class Lexer:

    # Initialize lexer
    def __init__(self, source):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1

    # Get current character
    def current(self):
        if self.pos >= len(self.source):
            return None
        return self.source[self.pos]

    # Look at next character
    def peek(self):
        index = self.pos + offset
        if index >= len(self.source):
            return None
        return self.source[index

    # Move to next character
    def advance(self):
        ch = self.current()
        if ch is None:
            return None

        self.pos += 1
        if ch == "\n":
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return ch

    # Main function: convert source code into tokens
    def tokenize(self):
        tokens = []

        while self.current() is not None:
            ch = self.current()

            if ch.isspace():
                self.advance()
                continue

            start_line = self.line
            start_column = self.column

            # Identifier or keyword
            if ch.isalpha() or ch == "_":
                value = self.read_identifier()
                token_type = KEYWORDS.get(value, "ID")
                tokens.append(
                    Token(token_type, value, start_line, start_column))
                continue

            # Number
            if ch.isdigit():
                value = self.read_number()
                tokens.append(Token("NUMBER", value, start_line, start_column))
                continue

            # String literal (used by the Part 1 try/catch example)
            if ch == '"':
                value = self.read_string()
                tokens.append(Token("STRING", value, start_line, start_column))
                continue

            # Two-character comparison operators
            two_chars = (ch or "") + (self.peek() or "")
            if two_chars in COMPARISON_TOKENS:
                self.advance()
                self.advance()
                tokens.append(
                    Token(COMPARISON_TOKENS[two_chars], two_chars,
                          start_line, start_column)
                )
                continue

            # One-character operators and delimiters
            if ch in SINGLE_CHAR_TOKENS:
                self.advance()
                tokens.append(
                    Token(SINGLE_CHAR_TOKENS[ch], ch,
                          start_line, start_column)
                )
                continue

            # One-character comparison operators
            if ch in "<>":
                self.advance()
                tokens.append(
                    Token(COMPARISON_TOKENS[ch], ch,
                          start_line, start_column)
                )
                continue

            raise LexerError(
                f"Lexical error at line {start_line}, column {start_column}: "
                f"invalid character {ch!r}"
            )

        tokens.append(Token("EOF", "", self.line, self.column))
        return tokens

    # Read identifier or keyword
    def read_identifier(self):
        result = []

        while self.current() is not None:
            ch = self.current()
            if ch.isalnum() or ch == "_":
                result.append(self.advance())
            else:
                break

        return "".join(result)

    # Read integer or decimal number
    def read_number(self):
        result = []

        while self.current() is not None and self.current().isdigit():
            result.append(self.advance())

        # ANVI numbers follow the Part 1 grammar:
        # integer [ "." integer ]
        if self.current() == ".":
            if self.peek() is None or not self.peek().isdigit():
                line, column = self.line, self.column
                raise LexerError(
                    f"Lexical error at line {line}, column {column}: "
                    "decimal point must be followed by digits"
                )

            result.append(self.advance())

            while self.current() is not None and self.current().isdigit():
                result.append(self.advance())

        # Reject things such as 12.3.4 as one malformed number.
        if self.current() == ".":
            line, column = self.line, self.column
            raise LexerError(
                f"Lexical error at line {line}, column {column}: "
                "malformed number"
            )

        return "".join(result)

    # Read string
    def read_string(self):
        # Store the contents without the surrounding quotes.
        self.advance()  # opening quote
        result = []

        while self.current() is not None:
            ch = self.current()

            if ch == '"':
                self.advance()
                return "".join(result)

            if ch == "\n":
                line, column = self.line, self.column
                raise LexerError(
                    f"Lexical error at line {line}, column {column}: "
                    "unterminated string"
                )

            if ch == "\\":
                # Basic escaped-character support.
                self.advance()
                escaped = self.current()
                if escaped is None:
                    raise LexerError(
                        f"Lexical error at line {self.line}, column {self.column}: "
                        "unterminated string"
                    )
                escapes = {"n": "\n", "t": "\t", '"': '"', "\\": "\\"}
                result.append(escapes.get(escaped, escaped))
                self.advance()
            else:
                result.append(self.advance())

        raise LexerError(
            f"Lexical error at line {self.line}, column {self.column}: "
            "unterminated string"
        )

def lex(source: str):
    return Lexer(source).tokenize()

# 7. Main program
if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python lexer.py <source-file>")
        sys.exit(1)

    path = sys.argv[1]

    try:
        source = open(path, "r", encoding="utf-8").read()
        for token in lex(source):
            print(token)
    except LexerError as error:
        print(error)
        sys.exit(1)
    except OSError as error:
        print(f"Could not read source file: {error}")
        sys.exit(1)
