"""End-to-end ANVI tests: lexer -> parser -> AST -> interpreter."""

import unittest

from parser import parse_source
from interpreter import Interpreter, RuntimeErrorANVI
from environment import EnvironmentError


class ANVIIntegrationPart6Tests(unittest.TestCase):
    def run_anvi(self, source):
        program = parse_source(source)
        interpreter = Interpreter()
        return interpreter.interpret(program)

    def test_arithmetic_and_operator_precedence(self):
        source = """
        display(2 + 3 * 4);
        display((2 + 3) * 4);
        """
        self.assertEqual(self.run_anvi(source), ["14", "20"])

    def test_variables_and_reassignment(self):
        source = """
        let score = 10;
        score = score + 5;
        display(score);
        """
        self.assertEqual(self.run_anvi(source), ["15"])

    def test_comparison_and_if_branch(self):
        source = """
        let age = 21;
        if (age >= 18) {
            display("adult");
        } else {
            display("minor");
        }
        """
        self.assertEqual(self.run_anvi(source), ["adult"])

    def test_else_branch(self):
        source = """
        let ready = F;
        if (ready) {
            display("go");
        } else {
            display("wait");
        }
        """
        self.assertEqual(self.run_anvi(source), ["wait"])

    def test_wloop(self):
        source = """
        let count = 0;
        wloop (count < 3) {
            display(count);
            count = count + 1;
        }
        """
        self.assertEqual(self.run_anvi(source), ["0", "1", "2"])

    def test_function_without_parameters(self):
        source = """
        func greeting() {
            display("hello");
        }
        greeting();
        """
        self.assertEqual(self.run_anvi(source), ["hello"])

    def test_function_parameters_and_return_value(self):
        source = """
        func add(a, b) {
            return a + b;
        }
        let result = add(4, 6);
        display(result);
        """
        self.assertEqual(self.run_anvi(source), ["10"])

    def test_local_scope_does_not_leak(self):
        source = """
        func makeValue() {
            let localValue = 99;
            return localValue;
        }
        display(makeValue());
        """
        self.assertEqual(self.run_anvi(source), ["99"])
        # The function-local declaration should not become a global variable.
        program = parse_source(source)
        interpreter = Interpreter()
        interpreter.interpret(program)
        with self.assertRaises(EnvironmentError):
            interpreter.environment.get("localValue")

    def test_recursive_function(self):
        source = """
        func factorial(n) {
            if (n <= 1) {
                return 1;
            }
            return n * factorial(n - 1);
        }
        display(factorial(5));
        """
        self.assertEqual(self.run_anvi(source), ["120"])

    def test_runtime_error_undefined_variable(self):
        source = "display(missingValue);"
        program = parse_source(source)
        with self.assertRaises(RuntimeErrorANVI):
            Interpreter().interpret(program)

    def test_runtime_error_wrong_argument_count(self):
        source = """
        func add(a, b) {
            return a + b;
        }
        display(add(1));
        """
        program = parse_source(source)
        with self.assertRaises(RuntimeErrorANVI):
            Interpreter().interpret(program)


if __name__ == "__main__":
    unittest.main()
