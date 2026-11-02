"""Tree-walking interpreter for ANVI Part 5: functions, scope and recursion."""
from ast_nodes import (ProgramNode, BlockNode, AssignmentNode, PrintNode, IfNode,
    WhileNode, ExpressionStatementNode, FunctionDefNode, FunctionCallNode, ReturnNode)
from environment import Environment, EnvironmentError
from expression_evaluator import evaluate as evaluate_expression, InterpreterError

class RuntimeErrorANVI(RuntimeError): pass
class ReturnSignal(Exception):
    def __init__(self,value): self.value=value

class UserFunction:
    def __init__(self, node, closure):
        self.node = node
        self.closure = closure

class Interpreter:
    def __init__(self, environment=None, max_loop_iterations=100000, max_call_depth=500):
        self.environment=environment if environment is not None else Environment()
        self.max_loop_iterations=max_loop_iterations; self.max_call_depth=max_call_depth
        self.output=[]; self.functions={}; self._loop_iterations=0; self._call_depth=0
    def _capture_output(self,value): self.output.append(self.format_value(value))
    def _evaluate(self,node,env=None):
        env=env or self.environment
        try: return evaluate_expression(node,env,lambda call:self._call_function(call,env))
        except (InterpreterError,EnvironmentError) as error: raise RuntimeErrorANVI(str(error)) from error
    def _call_function(self,call,caller_env):
        if call.name not in self.functions: raise RuntimeErrorANVI(f"undefined function '{call.name}'")
        fn=self.functions[call.name]
        if len(call.arguments)!=len(fn.node.parameters):
            raise RuntimeErrorANVI(f"function '{call.name}' expects {len(fn.node.parameters)} argument(s), got {len(call.arguments)}")
        args=[self._evaluate(arg,caller_env) for arg in call.arguments]
        self._call_depth+=1
        if self._call_depth>self.max_call_depth:
            self._call_depth-=1; raise RuntimeErrorANVI("function call depth limit exceeded")
        local = Environment(parent=fn.closure)
        for name,value in zip(fn.node.parameters,args): local.define(name,value)
        try:
            self._execute_block(fn.node.body,local)
            return None
        except ReturnSignal as signal: return signal.value
        finally: self._call_depth-=1
    def _condition(self,expr,env):
        value=self._evaluate(expr,env)
        if type(value) not in (bool,int,float): raise RuntimeErrorANVI("Condition must be a boolean or number")
        return bool(value)
    def _execute_block(self,block,env):
        for statement in block.statements: self._execute(statement,env)
    def _execute(self,node,env=None):
        env=env or self.environment
        if isinstance(node,ProgramNode):
            for statement in node.statements: self._execute(statement,env)
        elif isinstance(node,FunctionDefNode):
            if node.name in self.functions: raise RuntimeErrorANVI(f"function '{node.name}' is already defined")
            self.functions[node.name]=UserFunction(node)
        elif isinstance(node,BlockNode): self._execute_block(node,env)
        elif isinstance(node,AssignmentNode):
            value=self._evaluate(node.expression,env); name=node.variable.name
            try:
                if node.is_declaration: env.define(name,value)
                else: env.assign(name,value)
            except EnvironmentError as error: raise RuntimeErrorANVI(str(error)) from error
        elif isinstance(node,PrintNode): self._capture_output(self._evaluate(node.expression,env))
        elif isinstance(node,IfNode):
            if self._condition(node.condition,env): self._execute(node.then_branch,env)
            elif node.else_branch is not None: self._execute(node.else_branch,env)
        elif isinstance(node,WhileNode):
            while self._condition(node.condition,env):
                self._loop_iterations+=1
                if self._loop_iterations>self.max_loop_iterations: raise RuntimeErrorANVI("loop iteration limit exceeded")
                self._execute(node.body,env)
        elif isinstance(node,ExpressionStatementNode): self._evaluate(node.expression,env)
        elif isinstance(node,ReturnNode):
            if self._call_depth==0: raise RuntimeErrorANVI("return used outside a function")
            raise ReturnSignal(self._evaluate(node.expression,env) if node.expression is not None else None)
        else: raise RuntimeErrorANVI(f"Unsupported statement: {type(node).__name__}")
    def interpret(self,program):
        if not isinstance(program,ProgramNode): raise RuntimeErrorANVI("interpreter expected a ProgramNode")
        self.output=[]; self.functions={}; self._loop_iterations=0; self._call_depth=0
        # Register definitions before running top-level statements, enabling calls before definitions.
        for statement in program.statements:
            if isinstance(statement,FunctionDefNode):
                if statement.name in self.functions: raise RuntimeErrorANVI(f"function '{statement.name}' is already defined")
                self.functions[statement.name]=UserFunction(statement)
        try:
            for statement in program.statements:
                if not isinstance(statement,FunctionDefNode): self._execute(statement,self.environment)
        except ReturnSignal as signal: raise RuntimeErrorANVI("return used outside a function") from signal
        except RuntimeErrorANVI: raise
        except RuntimeError as error: raise RuntimeErrorANVI(str(error)) from error
        return self.output
    @staticmethod
    def format_value(value):
        if type(value) is float and value.is_integer(): return str(int(value))
        if value is True: return "T"
        if value is False: return "F"
        if value is None: return "null"
        return str(value)
def interpret_source(source):
    from parser import parse_source
    return Interpreter().interpret(parse_source(source))
