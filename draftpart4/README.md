# ANVI Part 4 — Interpreter & Control Structures

This project extends the Part 3 ANVI lexer and recursive-descent parser with a tree-walking interpreter.

## Features

- `let name = expression;` variable declarations
- `name = expression;` reassignment of an existing variable
- Arithmetic: `+`, `-`, `*`, `/`, `%` with precedence and parentheses
- Comparisons: `==`, `!=`, `<`, `>`, `<=`, `>=`
- Output via `display(expression);`
- `if (condition) { ... } else { ... }`
- `wloop (condition) { ... }`; 
- `T` / `F` booleans, numeric literals, strings
- Runtime errors for undefined variables, division/modulo by zero, invalid operand types, and non-boolean conditions
- A loop-iteration limit prevents accidental infinite loops

## Files

- `lexer.py`: token definitions and lexer (updated with `print` and `while` keywords)
- `ast_nodes.py`: AST classes, including `IfNode`, `WhileNode`, and `BlockNode`
- `parser.py`: parser for statements and expressions with precedence
- `environment.py`: symbol table for storing and retrieving variables
- `expression_evaluator.py` evaluates literal, variable, unary, and binary expression AST nodes.
- `control_structures_kiran.py` executes program/block nodes, declarations and assignments, print statements, if/else, while loops, and expression statements.
- `interpreter.py`: evaluates AST nodes and collects printed output
- `main.py`: command-line entry point
- `grammar.ebnf`: grammar for the implemented Part 4 subset
- `tests/part4/`: five complete example programs and expected outputs
- `tests/test_interpreter.py`: automated parser/interpreter/runtime tests
- `AI_USE_STATEMENT.md`: AI assistance disclosure

## Run a program

From this directory:

```bash
python3 main.py tests/part4/program4_while.anvi
```

Expected output:

```text
1
2
3
4
5
```

## Run all tests

```bash
python3 -m unittest discover -s tests -v
```

The suite includes the original Part 3 parser tests plus Part 4 interpreter tests. Expected result: all 19 tests pass.

## Symbol table / environment

`Environment` stores variables in a Python dictionary (`values`), mapping each variable name to its runtime value. `let` calls `define(name, value)`. Reading a variable calls `get(name)`, which raises a runtime error if the name does not exist. Reassignment calls `assign(name, value)` and also rejects an undefined name. The interpreter uses one environment shared by all statements and blocks in this version.

## Runtime behavior

- Division by zero raises `RuntimeErrorANVI: division by zero`.
- Modulo by zero raises `RuntimeErrorANVI: modulo by zero`.
- Reading an undefined variable raises a clear runtime error.
- Arithmetic operators require numeric operands; booleans are not treated as numbers.
- `if` and `wloop` conditions must evaluate to `T` or `F` (boolean values).
- Division returns a floating-point value; integral floating-point output is formatted without `.0`.

