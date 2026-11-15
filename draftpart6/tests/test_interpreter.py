import unittest
from parser import parse_source, ParserError
from interpreter import Interpreter, RuntimeErrorANVI

class InterpreterTests(unittest.TestCase):
    def run_source(self, source):
        return Interpreter().interpret(parse_source(source))

    def test_precedence(self):
        self.assertEqual(self.run_source("display(2 + 3 * 4);"), ["14"])

    def test_parentheses(self):
        self.assertEqual(self.run_source("display((2 + 3) * 4);"), ["20"])

    def test_variables_and_reassignment(self):
        self.assertEqual(self.run_source("let x = 10; let y = x + 5; x = y - 3; display(x);"), ["12"])

    def test_if_true_and_else(self):
        source = "let x = 12; if (x >= 10) { display(x); } else { display(0); }"
        self.assertEqual(self.run_source(source), ["12"])

    def test_if_else_false_branch(self):
        source = "let x = 2; if (x >= 10) { display(1); } else { display(0); }"
        self.assertEqual(self.run_source(source), ["0"])

    def test_while_loop(self):
        source = "let x = 1; wloop (x <= 3) { display(x); x = x + 1; }"
        self.assertEqual(self.run_source(source), ["1", "2", "3"])

    def test_all_comparisons(self):
        source = "display(5 == 5); display(5 != 4); display(3 < 4); display(4 > 3); display(4 <= 4); display(5 >= 4);"
        self.assertEqual(self.run_source(source), ["T"] * 6)

    def test_undefined_variable(self):
        with self.assertRaisesRegex(RuntimeErrorANVI, "undefined variable 'missing'"):
            self.run_source("display(missing);")

    def test_division_by_zero(self):
        with self.assertRaisesRegex(RuntimeErrorANVI, "division by zero"):
            self.run_source("display(10 / 0);")

    def test_invalid_operation(self):
        with self.assertRaisesRegex(RuntimeErrorANVI, "requires numeric operands"):
            self.run_source('display("hello" - 1);')

    def test_invalid_syntax(self):
        with self.assertRaises(ParserError):
            parse_source("let x = ;")

    def test_print_keyword_is_rejected(self):
        with self.assertRaises(ParserError):
            parse_source("print(1);")

    def test_while_keyword_is_rejected(self):
        with self.assertRaises(ParserError):
            parse_source("while (T) { display(1); }")

    def test_integrated_member2_member3_modules(self):
        # Confirms the expression evaluator and statement executor are wired together.
        source = "let x = 1; wloop (x <= 3) { if (x != 2) { display(x + 10); } else { display(x); } x = x + 1; }"
        self.assertEqual(self.run_source(source), ["11", "2", "13"])

    def test_unary_plus(self):
        self.assertEqual(self.run_source("display(+5);") , ["5"])

if __name__ == "__main__":
    unittest.main()
