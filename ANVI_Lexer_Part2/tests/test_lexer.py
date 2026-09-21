from lexer import lex, LexerError
import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


class TestANVILexer(unittest.TestCase):
    def test_1_variable_declaration(self):
        tokens = lex("let x = 10;")
        types = [t.type for t in tokens]
        expected = ["LET", "ID", "ASSIGN", "NUMBER", "SEMICOLON", "EOF"]
        self.assertEqual(types, expected)

    def test_2_arithmetic_expression(self):
        tokens = lex("let result = x + y * 2 - 1;")
        types = [t.type for t in tokens]
        expected = ["LET", "ID", "ASSIGN", "ID", "PLUS", "ID", "MULTIPLY",
                    "NUMBER", "MINUS", "NUMBER", "SEMICOLON", "EOF"]
        self.assertEqual(types, expected)

    def test_3_print_statement(self):
        tokens = lex("display(x + 1);")
        types = [t.type for t in tokens]
        expected = ["DISPLAY", "LPAREN", "ID", "PLUS", "NUMBER",
                    "RPAREN", "SEMICOLON", "EOF"]
        self.assertEqual(types, expected)

    def test_4_control_structure(self):
        tokens = lex("if (x > 10) { display(x); } else { display(0); }")
        types = [t.type for t in tokens]
        expected = [
            "IF", "LPAREN", "ID", "GREATER", "NUMBER", "RPAREN", "LBRACE",
            "DISPLAY", "LPAREN", "ID", "RPAREN", "SEMICOLON", "RBRACE",
            "ELSE", "LBRACE", "DISPLAY", "LPAREN", "NUMBER", "RPAREN",
            "SEMICOLON", "RBRACE", "EOF"
        ]
        self.assertEqual(types, expected)

    def test_5_invalid_input(self):
        with self.assertRaises(LexerError):
            lex("let x = 10 @ 5;")
