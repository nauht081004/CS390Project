# ANVI Lexer — Part 2

## What this is
A lexer for the ANVI programming language (designed in Part 1). It reads ANVI source code as plain text and converts it into a sequence of tokens (keywords, identifiers, numbers, operators, and delimiters), or raises a clear error if it finds a character it doesn't recognize.

## Files
- `lexer.py` — the lexer itself
- `tests/test_lexer.py` — the five required test cases 
- `generate_output.py` — runs all five test cases and writes `lexer_output.txt`
- `lexer_output.txt` — recorded token output for every test case
- `AI_USE.md` — AI Use Statement
- `README.md` — this file

## How to run it

**Tokenize a source file:**
```
python lexer.py path/to/source.anvi
```

**Run the test suite:**
```
python -m unittest tests.test_lexer -v
```

**Regenerate the recorded output file:**
```
python generate_output.py
```

## Token types recognized
Keywords (`let`, `if`, `else`, `wloop`, `floop`, `func`, `return`, `display`, `T`, `F`, `try`, `catch`), identifiers, integer and decimal numbers, string literals, arithmetic operators (`+ - * / %`), comparison operators (`== != < > <= >=`), the assignment operator (`=`), parentheses, braces, commas, semicolons, and whitespace (skipped, not tokenized).

## Error handling
Any character that doesn't match a known token pattern (e.g. `@`) raises a `LexerError` describing the line and column, instead of an unhandled Python exception.