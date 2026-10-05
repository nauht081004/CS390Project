# ANVI Parser — Part 3

## What this is
A parser for ANVI that converts the token list from the lexer (Part 2) into
an Abstract Syntax Tree (AST), with correct operator precedence, statement
parsing, and syntax error handling.

## Status
The parser includes both expression parsing (numbers, variables, booleans,
strings, arithmetic, comparison, parentheses, unary minus) and statement/
program parsing (assignment, display/print, multiple statements). All 20
tests pass: 12 expression-level tests and 8 statement/program-level tests,
run together against the same parser.py with no conflicts.

## Files
- `lexer.py` — tokenizer (Part 2).
- `ast_nodes.py` — AST node class definitions.
- `parser.py` — the parser: expression parsing, statement parsing, and
  program parsing.
- `grammar.txt` — updated BNF/EBNF grammar.
- `tests/test_parser_kiran.py` — 12 expression-level tests.
- `tests/test_parser_anna.py` — 8 statement/program-level tests.
- `demo_ast_kiran.py` — generates AST output for 3 example expressions.
- `ast_demonstrations.txt` — recorded AST output for those 3 examples.
- `AI_USE.md` — AI Use Statement.
- `README.md` — this file.

## How to run it

**Run all tests:**
```
python -m unittest tests.test_parser_kiran tests.test_parser_anna -v
```

**Generate the AST demonstrations:**
```
python demo_ast_kiran.py
```

**Parse a program directly:**
```
python -c "from parser import parse_program; print(parse_program('let x = 2 + 3 * 4; display(x);').to_string())"
```

## What the parser supports
- Numbers (integer and decimal)
- Variables
- Booleans (`T` / `F`) and string literals
- Arithmetic expressions (`+ - * / %`)
- Comparison expressions (`== != < > <= >=`)
- Parenthesized expressions
- Unary minus (e.g. `-x`)
- Variable assignment (`let x = ...;` and `x = ...;`)
- Print statements (`display(...);`)
- Multiple statements in sequence

## Operator precedence (loosest to tightest)
Comparison → Addition/Subtraction → Multiplication/Division/Modulo → Unary
minus → Primary (numbers, variables, booleans, strings, parenthesized
expressions)

## Error handling
Invalid syntax raises a `ParserError` with the line and column, instead of
an unhandled Python exception. For example:
- `let x = ;` — missing expression after `=`
- `display(5;` — missing closing parenthesis
- `let x = 5` — missing semicolon

## AST examples
See `ast_demonstrations.txt` for three worked examples (`2 + 3 * 4`,
`(2 + 3) * 4`, `10 - 3 - 2`), generated directly from the parser's own
`to_string()` output.

## AI Use
See `AI_USE.md` for the full AI Use Statement.