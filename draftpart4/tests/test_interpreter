
import unittest

from parser import parse_source
from interpreter import Interpreter, RuntimeErrorANVI


class InterpreterTests(unittest.TestCase):

    def run_program(self, source):
        interpreter = Interpreter()
        return interpreter.interpret(parse_source(source))

    def test_variable_assignment_and_reassignment(self):
        output = self.run_program("""
            let x = 10;
            x = x + 5;
            display(x);
        """)
        self.assertEqual(output, ["15"])

    def test_if_true_branch(self):
        output = self.run_program("""
            let x = 10;
            if (x >= 10) {
                display(x);
            } else {
                display(0);
            }
        """)
        self.assertEqual(output, ["10"])

    def test_else_branch(self):
        output = self.run_program("""
            let x = 5;
            if (x >= 10) {
                display(x);
            } else {
                display(0);
            }
        """)
        self.assertEqual(output, ["0"])

    def test_while_loop(self):
        output = self.run_program("""
            let x = 1;
            wloop (x <= 5) {
                display(x);
                x = x + 1;
            }
        """)
        self.assertEqual(output, ["1", "2", "3", "4", "5"])

    def test_undefined_assignment(self):
        with self.assertRaises(RuntimeErrorANVI):
            self.run_program("x = 10;")

    def test_infinite_loop_limit(self):
        interpreter = Interpreter(max_loop_iterations=3)
        program = parse_source("""
            wloop (T) {
                display(1);
            }
        """)
        with self.assertRaisesRegex(
            RuntimeErrorANVI, "loop iteration limit exceeded"
        ):
            interpreter.interpret(program)


if __name__ == "__main__":
    unittest.main()
