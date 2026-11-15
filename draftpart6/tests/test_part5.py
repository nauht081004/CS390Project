import unittest
from parser import parse_source
from interpreter import Interpreter, RuntimeErrorANVI

class Part5Tests(unittest.TestCase):
    def run_source(self, source):
        return Interpreter().interpret(parse_source(source))
    def test_function_and_parameters(self):
        self.assertEqual(self.run_source('func add(a, b) { return a + b; } display(add(10, 20));'), ['30'])
    def test_local_scope_does_not_overwrite_global(self):
        self.assertEqual(self.run_source('let x = 10; func test() { let x = 20; display(x); } test(); display(x);'), ['20', '10'])
    def test_recursion_factorial(self):
        self.assertEqual(self.run_source('func fact(n) { if (n <= 1) { return 1; } return n * fact(n - 1); } display(fact(5));'), ['120'])
    def test_argument_count_error(self):
        with self.assertRaisesRegex(RuntimeErrorANVI, 'expects 2 argument'):
            self.run_source('func add(a, b) { return a + b; } display(add(1));')
    def test_return_outside_function(self):
        with self.assertRaisesRegex(RuntimeErrorANVI, 'outside a function'):
            self.run_source('return 5;')
    def test_unknown_function(self):
        with self.assertRaisesRegex(RuntimeErrorANVI, "undefined function 'missing'"):
            self.run_source('display(missing());')

if __name__ == '__main__': unittest.main()
