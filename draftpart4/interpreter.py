"""Integrated tree-walking interpreter for ANVI Part 4.

Expression evaluation is implemented in expression_evaluator.py
Statement execution is implemented in control_structures_kiran.py
"""
from ast_nodes import ProgramNode
from environment import Environment, EnvironmentError
from expression_evaluator import evaluate as evaluate_expression, InterpreterError
from control_structures_kiran import StatementExecutor


class RuntimeErrorANVI(RuntimeError):
    """A runtime error raised while executing an ANVI program."""


class Interpreter:
    def __init__(self, environment=None, max_loop_iterations=100000):
        self.environment = environment if environment is not None else Environment()
        self.max_loop_iterations = max_loop_iterations
        self.output = []
        self.executor = StatementExecutor(
            self.environment,
            self._evaluate,
            output=self._capture_output,
        )
        self._loop_iterations = 0

    def _evaluate(self, expression, environment):
        try:
            return evaluate_expression(expression, environment)
        except (InterpreterError, RuntimeError) as error:
            if isinstance(error, RuntimeErrorANVI):
                raise
            raise RuntimeErrorANVI(str(error)) from error

    def _capture_output(self, value):
        self.output.append(self.format_value(value))

    def interpret(self, program):
        if not isinstance(program, ProgramNode):
            raise RuntimeErrorANVI("interpreter expected a ProgramNode")
        self.output = []
        self._loop_iterations = 0
        try:
            self._execute_with_loop_guard(program)
       except RuntimeErrorANVI:
            raise
       except (RuntimeError, EnvironmentError) as error:
            raise RuntimeErrorANVI(str(error)) from error
        return self.output

    def _execute_with_loop_guard(self, node):
        # StatementExecutor owns the statement semantics. This wrapper adds a
        # safety limit so accidental infinite loops cannot hang the interpreter.
        from ast_nodes import WhileNode, ProgramNode, BlockNode, IfNode
        if isinstance(node, WhileNode):
            # Run a loop here to enforce the limit while reusing executor logic
            # for its condition and body.
            while self.executor.condition_is_true(node.condition):
                self._loop_iterations += 1
                if self._loop_iterations > self.max_loop_iterations:
                    raise RuntimeErrorANVI("loop iteration limit exceeded")
                self._execute_with_loop_guard(node.body)
        elif isinstance(node, ProgramNode):
            for statement in node.statements:
                self._execute_with_loop_guard(statement)
        elif isinstance(node, BlockNode):
            for statement in node.statements:
                self._execute_with_loop_guard(statement)
        elif isinstance(node, IfNode):
            if self.executor.condition_is_true(node.condition):
                self._execute_with_loop_guard(node.then_branch)
            elif node.else_branch is not None:
                self._execute_with_loop_guard(node.else_branch)
        else:
            self.executor.execute(node)

    @staticmethod
    def format_value(value):
        if type(value) is float and value.is_integer():
            return str(int(value))
        if value is True:
            return "T"
        if value is False:
            return "F"
        return str(value)


def interpret_source(source):
    from parser import parse_source
    return Interpreter().interpret(parse_source(source))
