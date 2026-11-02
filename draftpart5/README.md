# ANVI Part 5 — Functions, Scope & Extension Feature

This project extends the Part 4 ANVI interpreter with user-defined functions, function parameters, return values, local variable scope, and recursion as an extension feature.

## Features

let name = expression; variable declarations

name = expression; reassignment of an existing variable

Arithmetic: +, -, *, /, % with precedence and parentheses

Comparisons: ==, !=, <, >, <=, >=

Output via display(expression);

if (condition) { ... } else { ... }

wloop (condition) { ... }

T / F booleans, numeric literals, and strings

User-defined function declarations using func

Function parameters and function calls with zero or more arguments

Return statements using return

Functions can return values that can be used in expressions and assignments

Local variables inside functions

Local variables can shadow global variables without changing their values

Recursive function calls

Runtime errors for undefined variables, undefined functions, incorrect argument counts, division/modulo by zero, invalid operand types, and non-boolean conditions

A loop-iteration limit prevents accidental infinite loops

A function call-depth limit prevents excessive recursive calls

## Files

lexer.py: token definitions and lexer, including function-related keywords

ast_nodes.py: AST classes, including FunctionDefNode, FunctionCallNode, and ReturnNode, along with the existing statement and expression nodes

parser.py: recursive-descent parser for function definitions, parameters, function calls, return statements, statements, and expressions with precedence

environment.py: symbol table for storing and retrieving variables, including parent environments for local scope

expression_evaluator.py: evaluates literal, variable, unary, binary, and function-call expression AST nodes

control_structures_kiran.py: executes program/block nodes, declarations and assignments, output statements, conditionals, and loops

interpreter.py: registers functions, executes function calls, handles return values, manages function environments, and collects printed output

main.py: command-line entry point

grammar.ebnf: grammar for the implemented Part 5 language features

tests/: automated parser/interpreter tests and example programs

AI_USE_STATEMENT.md: AI assistance disclosure

## Run a program

From this directory:

```bash
python3 main.py tests/part5/02_parameters.anvi
```

The following example demonstrates function definitions, parameters, and return values:

func add(a, b) {
    return a + b;
}

let result = add(10, 20);
display(result);

Expected output:

30

## Run all tests

```bash
python3 -m unittest discover -s tests -v
```

The suite includes the existing Part 4 tests and the new Part 5 function, scope, and recursion tests.

Expected result: all 45 tests pass.

## Function execution

Function definitions use the func keyword, followed by a function name, parameters in parentheses, and a function body enclosed in braces.

For example:

func multiply(a, b) {
    return a * b;
}

When a function is called, the interpreter evaluates its arguments and assigns their values to the corresponding parameters. The function body then executes in its own local environment.

A function can return a value using the return statement:

func square(x) {
    return x * x;
}

let result = square(5);
display(result);

Expected output:

25

Functions without a return statement return None.

## Variable scope / environment

Environment stores variables in a Python dictionary (values), mapping each variable name to its runtime value.

The interpreter creates a separate local environment for each function call. Function parameters and variables declared inside the function are stored in this local environment.

A local environment can access variables from its parent environment. This allows functions to access global variables while keeping local variables separate.

For example:

let x = 10;

func test() {
    let x = 20;
    display(x);
}

test();
display(x);

Expected output:

20
10

The local variable x shadows the global variable inside the function without changing the global value.

## Extension feature: Recursion

Recursion allows a function to call itself to solve a problem by breaking it into smaller problems.

For example, the factorial function:

func factorial(n) {
    if (n <= 1) {
        return 1;
    }

    return n * factorial(n - 1);
}

display(factorial(5));

Expected output:

120

The interpreter supports recursive function calls by creating a new local environment for each call. A function call-depth limit helps prevent excessive recursion.

## Runtime behavior

Division by zero raises RuntimeErrorANVI: division by zero.

Modulo by zero raises RuntimeErrorANVI: modulo by zero.

Reading an undefined variable raises a clear runtime error.

Calling an undefined function raises a runtime error.

Passing an incorrect number of arguments raises a runtime error.

Using return outside a function raises a runtime error.

Arithmetic operators require numeric operands; booleans are not treated as numbers.

if and wloop conditions must evaluate to T or F (boolean values).

Division returns a floating-point value; integral floating-point output is formatted without .0.

Recursive function calls are restricted by a maximum call-depth limit.

