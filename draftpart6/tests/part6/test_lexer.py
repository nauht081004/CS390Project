"""Part 6 lexer tests for the ANVI interpreter.

Run from the project root with:
    python3 -m pytest tests/part6/test_lexer.py -v
"""

import os
import sys
import unittest

# Make the project root importable when pytest is launched from another folder.
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from lexer import LexerError, lex


class LexerPart6Tests(unittest.TestCase):
    def token_pairs(self, source):
        return [(token.type, token.value) for token in lex(source)]

    def test_keywords(self):
        pairs = self.token_pairs("let if else wloop func return display T F")
        self.assertEqual(
            pairs,
            [
                ("LET", "let"), ("IF", "if"), ("ELSE", "else"),
                ("WLOOP", "wloop"), ("FUNC", "func"),
                ("RETURN", "return"), ("DISPLAY", "display"),
                ("TRUE", "T"), ("FALSE", "F"), ("EOF", ""),
            ],
        )

    def test_identifier_and_underscore(self):
        self.assertEqual(
            self.token_pairs("total _value value2"),
            [("ID", "total"), ("ID", "_value"), ("ID", "value2"), ("EOF", "")],
        )

    def test_integer_and_decimal_numbers(self):
        self.assertEqual(
            self.token_pairs("0 42 3.14"),
            [("NUMBER", "0"), ("NUMBER", "42"), ("NUMBER", "3.14"), ("EOF", "")],
        )

    def test_rejects_decimal_point_without_following_digits(self):
        for source in ("12.", "12.a"):
            with self.subTest(source=source):
                with self.assertRaisesRegex(LexerError, "decimal point must be followed by digits"):
                    lex(source)

    def test_rejects_multiple_decimal_points(self):
        with self.assertRaisesRegex(LexerError, "malformed number"):
            lex("12.3.4")

    def test_string_literal(self):
        self.assertEqual(self.token_pairs('"hello world"'), [("STRING", "hello world"), ("EOF", "")])

    def test_string_escape_sequences(self):
        tokens = lex(r'"line1\nline2\t\"quoted\"\\end"')
        self.assertEqual(tokens[0].type, "STRING")
        self.assertEqual(tokens[0].value, 'line1\nline2\t"quoted"\\end')

    def test_unterminated_string_at_end(self):
        with self.assertRaisesRegex(LexerError, "unterminated string"):
            lex('"unfinished')

    def test_unterminated_string_at_newline(self):
        with self.assertRaisesRegex(LexerError, "unterminated string"):
            lex('"first line\nsecond line"')

    def test_arithmetic_operators(self):
        self.assertEqual(
            self.token_pairs("+ - * / %"),
            [("PLUS", "+"), ("MINUS", "-"), ("MULTIPLY", "*"),
             ("DIVIDE", "/"), ("MODULO", "%"), ("EOF", "")],
        )

    def test_assignment_and_comparison_operators(self):
        self.assertEqual(
            self.token_pairs("= == != < > <= >="),
            [("ASSIGN", "="), ("EQUAL", "=="), ("NOT_EQUAL", "!="),
             ("LESS", "<"), ("GREATER", ">"), ("LESS_EQUAL", "<="),
             ("GREATER_EQUAL", ">="), ("EOF", "")],
        )

    def test_delimiters(self):
        self.assertEqual(
            self.token_pairs("( ) { } , ;"),
            [("LPAREN", "("), ("RPAREN", ")"), ("LBRACE", "{"),
             ("RBRACE", "}"), ("COMMA", ","), ("SEMICOLON", ";"), ("EOF", "")],
        )

    def test_tracks_line_and_column(self):
        tokens = lex("let x = 1;\ndisplay(x);")
        display_token = next(token for token in tokens if token.value == "display")
        self.assertEqual((display_token.line, display_token.column), (2, 1))

    def test_appends_eof_token(self):
        token = lex("let x = 1;")[-1]
        self.assertEqual((token.type, token.value), ("EOF", ""))

    def test_invalid_character_reports_location(self):
        with self.assertRaisesRegex(LexerError, r"line 1, column 6.*invalid character '@'"):
            lex("let x@")

    def test_complete_function_program(self):
        source = "func add(a, b) { return a + b; } display(add(2, 3));"
        pairs = self.token_pairs(source)
        self.assertEqual(pairs[0], ("FUNC", "func"))
        self.assertIn(("RETURN", "return"), pairs)
        self.assertIn(("DISPLAY", "display"), pairs)
        self.assertEqual(pairs[-1], ("EOF", ""))


if __name__ == "__main__":
    unittest.main()
