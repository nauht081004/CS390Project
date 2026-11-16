"""Standalone reference lexer, generated with ChatGPT assistance.
Not a copy of Van, Sisir, or Anna's implementation. See INTEGRATION.md.
"""
import argparse
import re
import sys
from pathlib import Path
from errors import LexicalError
from token_defs import KEYWORDS, OPERATORS, Token

NUMBER = re.compile(r"[0-9]+(?:\.[0-9]+)?")
IDENTIFIER = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")


def tokenize(source):
    # Treat CRLF and CR as single line endings, including direct API input.
    source = source.replace("\r\n", "\n").replace("\r", "\n")
    lines = source.split("\n")
    tokens = []
    pos, line, column = 0, 1, 1
    while pos < len(source):
        ch = source[pos]
        if ch == "\n":
            pos += 1
            line += 1
            column = 1
            continue
        if ch in " \t\f\v":
            pos += 1
            column += 1
            continue
        number = NUMBER.match(source, pos)
        identifier = IDENTIFIER.match(source, pos)
        if number:
            lexeme = number.group()
            kind = "NUMBER"
        elif identifier:
            lexeme = identifier.group()
            kind = KEYWORDS.get(lexeme, "ID")
        elif source[pos:pos + 2] in OPERATORS:
            # Longest operator first: >= must be one token, not > then =.
            lexeme = source[pos:pos + 2]
            kind = OPERATORS[lexeme]
        elif ch in OPERATORS:
            lexeme = ch
            kind = OPERATORS[ch]
        else:
            # No skipped gaps: every non-whitespace character is checked.
            raise LexicalError(ch, line, column, lines[line - 1])
        tokens.append(Token(kind, lexeme, line, column))
        pos += len(lexeme)
        column += len(lexeme)
    return tokens


def main():
    parser = argparse.ArgumentParser(description="ANVI reference lexer")
    parser.add_argument("source", type=Path)
    args = parser.parse_args()
    try:
        source = args.source.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        print(f"Cannot read source file: {error}", file=sys.stderr)
        return 2
    try:
        tokens = tokenize(source)
    except LexicalError as error:
        print(error, file=sys.stderr)
        return 1
    for token in tokens:
        print(token)
    return 0


if __name__ == "__main__":
    sys.exit(main())
