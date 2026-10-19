import unittest
from parser import parse_source
from interpreter import Interpreter, RuntimeErrorANVI


class RuntimeErrorTests(unittest.TestCase):
    def test_division_by_zero(self):
        program = parse_source("""
            let x = 10 / 0;
            display(x);
        """)
        with self.assertRaisesRegex(RuntimeErrorANVI, "Division by zero"):
            Interpreter().interpret(program)


if __name__ == "__main__":
    unittest.main()
