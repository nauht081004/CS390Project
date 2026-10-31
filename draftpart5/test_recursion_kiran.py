import unittest

from environment import Environment
from scope_runtime_kiran import CallStack


class RecursionScopeTests(unittest.TestCase):
    def setUp(self):
        self.global_scope = Environment()
        self.global_scope.define("n", 999)
        self.stack = CallStack(max_depth=10)

    def factorial(self, number):
        with self.stack.enter_call(
            "factorial", ["n"], [number], self.global_scope
        ) as local:
            if local.get("n") <= 1:
                return 1

            smaller_result = self.factorial(local.get("n") - 1)

            # Deeper calls must not change this call's n.
            self.assertEqual(local.get("n"), number)
            return local.get("n") * smaller_result

    def test_factorial_and_separate_variables(self):
        self.assertEqual(self.factorial(5), 120)
        self.assertEqual(self.global_scope.get("n"), 999)
        self.assertEqual(self.stack.frames, [])

    def test_base_case(self):
        self.assertEqual(self.factorial(0), 1)
        self.assertEqual(self.stack.frames, [])

    def test_cleanup_after_error(self):
        with self.assertRaisesRegex(ValueError, "test error"):
            with self.stack.enter_call(
                "broken", [], [], self.global_scope
            ):
                raise ValueError("test error")

        self.assertEqual(self.stack.frames, [])

    def test_depth_limit_and_recovery(self):
        with self.assertRaisesRegex(
            RuntimeError, "Maximum function call depth"
        ):
            self.factorial(20)

        self.assertEqual(self.stack.frames, [])
        self.assertEqual(self.factorial(3), 6)

    def test_wrong_argument_count(self):
        with self.assertRaisesRegex(RuntimeError, "expects 1"):
            with self.stack.enter_call(
                "factorial", ["n"], [], self.global_scope
            ):
                self.fail("Invalid call should not execute")

        self.assertEqual(self.stack.frames, [])


if __name__ == "__main__":
    unittest.main(verbosity=2)