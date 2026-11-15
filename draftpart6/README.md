# ANVI Part 5 — Functions, Scope, and Recursion

This project extends the Part 4 ANVI interpreter with user-defined functions, parameters, return values, local variable environments, and recursion as its extension feature.

## Features

- `let name = expression;` declarations and reassignment with `name = expression;`
- Arithmetic and comparison operators with precedence and parentheses
- Output with `display(expression);` or the earlier supported `display expression;` form
- `if (...) { ... } else { ... }` and `wloop (...) { ... }`
- `func name(parameter, ...) { ... }` definitions and `name(argument, ...);` calls
- `return expression;` (or bare `return;` to return `null`)
- Local function scope; local declarations may shadow globals
- Recursive calls (extension feature), demonstrated by factorial
- Runtime checks for unknown functions, argument-count mismatches, invalid returns, and excessive recursion
- Loop iteration limit to protect against accidental infinite loops

ANVI keeps the project's established keywords `func`, `display`, and `wloop`. The assignment handout's `function`, `print`, and `while` spellings are not used; `print` and `while` are intentionally rejected as keywords to preserve the existing project language.

## Run a program

From this directory:

```bash
python3 main.py tests/part5/05_recursion.anvi
```

Expected output:

```text
120
```

Other examples are in `tests/part5/`:

1. `01_basic_function.anvi` — a function without parameters
2. `02_parameters.anvi` — parameters and return value
3. `03_return_value.anvi` — using a returned value in a variable assignment
4. `04_scope.anvi` — local variable shadowing and global preservation
5. `05_recursion.anvi` — recursive factorial

## Run all tests

```bash
python3 -m unittest discover -s tests -v
```

The suite includes Part 4 regression tests and Part 5 tests for calls, scope, recursion, incorrect argument counts, return outside functions, and undefined functions.

## Scope and runtime behavior

Each function call creates a local environment containing its parameters and local declarations. The local environment can read global variables through its parent environment. A local `let` declaration shadows a same-named global. Reassignment updates the nearest existing binding. Function definitions are registered before top-level statements execute, so a function can be called before its definition appears in the file and recursive calls are supported.

Functions without an explicit return produce `null`. Values printed by `display` are collected by the interpreter and formatted for the command-line runner. Integral floating-point values display without `.0`; booleans display as `T` and `F`.
