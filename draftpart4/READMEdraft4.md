ANVI Part 4 — Tree-Walking Interpreter
Project Overview

This project extends the ANVI lexer and recursive-descent parser developed in Part 3 by implementing a tree-walking interpreter. The interpreter traverses the Abstract Syntax Tree (AST) and executes ANVI programs.

The project demonstrates expression evaluation, variable management, conditional execution, loops, and runtime error handling.

Features
Variable declarations using let.
Variable reassignment.
Arithmetic operations: +, -, *, /, and %.
Operator precedence and parentheses.
Comparisons: ==, !=, <, >, <=, and >=.
Output using display(expression);.
Conditional execution using if and else.
Repeated execution using wloop.
Boolean values using T and F.
String literals and string concatenation, if supported by the implementation.
Runtime error handling for undefined variables, division by zero, modulo by zero, and invalid operations.
A loop iteration limit to prevent accidental infinite loops.
Project Structure
File or directory	Description
lexer.py	Converts source code into tokens.
ast_nodes.py	Defines AST node classes.
parser.py	Parses tokens into an AST.
environment.py	Stores and retrieves variable values.
expression_evaluator.py	Evaluates literals, variables, unary expressions, and binary expressions.
control_structures_kiran.py	Executes statements, assignments, conditionals, and loops.
interpreter.py	Integrates expression evaluation and statement execution.
main.py	Command-line entry point.
grammar.ebnf	Documents the implemented language grammar.
tests/	Contains automated tests and example ANVI programs.
test results.md	Documents test results and expected versus actual output.
AI_USE_STATEMENT.md	Documents AI assistance used during development.
Requirements
Python 3
No additional third-party dependencies are required, if the project uses only the Python standard library.
Running an ANVI Program

Open a terminal in the project directory and run:

python main.py tests/program1_arithmetic.anvi


Other example programs can be executed with:

python main.py tests/program2_variables.anvi
python main.py tests/program3_if_else.anvi
python main.py tests/program4_while.anvi
python main.py tests/program5_comparisons.anvi

Example Program
let x = 1;
wloop (x <= 5) {
    display(x);
    x = x + 1;
}


Expected output:

1
2
3
4
5

Environment and Symbol Table

The interpreter uses an environment to store variable names and their runtime values in a dictionary.

define(name, value) creates a variable.
get(name) retrieves a variable's value.
assign(name, value) updates an existing variable.

Reading an undefined variable or assigning to an undefined variable raises a runtime error. Statements and blocks share the same environment in this implementation.

Runtime Error Handling

The interpreter reports runtime errors for invalid operations, undefined variables, division by zero, and modulo by zero.

Arithmetic operators require numeric operands, and boolean values are not treated as numbers. Conditions must evaluate to the supported boolean values. A loop iteration limit helps prevent programs from running indefinitely.

Running Automated Tests

From the project root, run:

python -m unittest discover -s tests -v


The current test suite contains 22 tests covering expression evaluation, comparisons, arithmetic, variable lookup, runtime errors, conditional branches, loops, and loop iteration limits.

The expected result is that all tests pass. See test results.md for the recorded test results and example program outputs.

Test Programs

The project includes five example ANVI programs demonstrating arithmetic, variables, conditional execution, loops, and comparisons.

Expected and actual outputs are documented in test results.md.

Grammar

The implemented language grammar is documented in grammar.ebnf. It describes the syntax supported by the lexer and parser.

AI Use Disclosure

AI assistance used during development is documented in AI_USE_STATEMENT.md, including an example of a suggestion that was verified or corrected during implementation.

Project Status

Part 4 implements a tree-walking interpreter for the supported ANVI language features. Automated tests and example programs are used to verify its behavior.
