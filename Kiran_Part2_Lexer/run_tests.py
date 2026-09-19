"""Explicit expected tokens and source locations; no third-party packages."""
import json
import subprocess
import sys
import unittest
from pathlib import Path
from errors import LexicalError
from lexer import tokenize

ROOT = Path(__file__).resolve().parent
CASES = json.loads((ROOT / "tests/cases.json").read_text())

class LexerTests(unittest.TestCase):
    def test_cases(self):
        for case in CASES:
            with self.subTest(case=case["name"]):
                source = (ROOT / "tests" / case["file"]).read_bytes().decode()
                if "error" in case:
                    with self.assertRaises(LexicalError) as caught:
                        tokenize(source)
                    e = caught.exception
                    self.assertEqual([e.character, e.line, e.column], case["error"])
                    self.assertIn("Lexical error", str(e))
                else:
                    actual = [(t.type, t.lexeme) for t in tokenize(source)]
                    expected = [tuple(pair) for pair in case["tokens"]]
                    self.assertEqual(actual, expected)

    def test_positions_and_line_endings(self):
        tokens = tokenize("let x=1;\r\n\tdisplay(x);\rlet y=2;")
        self.assertEqual((tokens[5].line, tokens[5].column), (2, 2))
        self.assertEqual((tokens[10].line, tokens[10].column), (3, 1))

    def test_tab_error_caret(self):
        with self.assertRaises(LexicalError) as caught:
            tokenize("\t@")
        self.assertEqual(str(caught.exception).splitlines()[-1], "    ^")

    def test_cli_invalid_input(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "lexer.py"), str(ROOT / "tests/05_invalid.anvi")],
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("invalid character '@'", result.stderr)
        self.assertNotIn("Traceback", result.stderr)
        self.assertEqual(result.stdout, "")

if __name__ == "__main__":
    unittest.main(verbosity=2)
