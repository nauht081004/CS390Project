# ANVI Part 2 — Kiran's error handling and testing package

Prepared for Kiran's assigned portion, with ChatGPT assistance. This is a contribution package plus a standalone reference lexer, not the group's merged final submission.

## Run it

Install Python 3.9 or newer. No additional packages are needed. Extract the ZIP, open a terminal inside `Kiran_Part2_Lexer`, and run:

```text
python lexer.py tests/01_variable_declaration.anvi
python lexer.py tests/05_invalid.anvi
python run_tests.py
python generate_outputs.py
```

On Windows, use `py` instead of `python` if needed. On macOS/Linux, `python3` may be needed.

The lexer displays token types, original lexemes, and one-based line/column positions. It does not execute ANVI programs. Invalid input stops at the first error and exits with status 1. A source-file reading error exits with status 2. Successful tokenization exits with status 0. Tokens are collected before display, so invalid source does not print a partial token list.

Example error:

```text
Lexical error at line 1, column 12: invalid character '@'.
let x = 10 @ 5;
           ^
```

## Files

- `errors.py`: reusable lexical error class for Kiran's portion.
- `run_tests.py`: automated assertions for 12 source cases, line positions, caret alignment, and command-line error behavior.
- `tests/`: 12 source files and independently specified expected token sequences/error positions in `cases.json`.
- `test_outputs.txt`: actual CLI output for every source case.
- `verification.txt`: actual automated test-run results. Four unittest methods run; one method checks all 12 source cases as subtests.
- `lexer.py` and `token_defs.py`: AI-assisted standalone reference implementation used to run the tests. These are not attributed to the other group members.
- `generate_outputs.py`: regenerates the output report.
- `INTEGRATION.md`: instructions for combining this contribution with the team's code.
- `LEXICAL_RULES.md`: token rules, Part 1 source, and assumptions needing team confirmation.
- `AI_USE_STATEMENT.md`: assistance disclosure and a specific suggestion for the group to verify.

## Test coverage

| Case | Coverage | Expected result |
| --- | --- | --- |
| 01 | Variable declaration | LET, ID, ASSIGN, NUMBER, SEMICOLON |
| 02 | Arithmetic expression | All five arithmetic operators and parentheses |
| 03 | Print statement | ANVI `display` keyword |
| 04 | Conditional | `if`, `else`, braces, comparison |
| 05 | Invalid input | `@` at line 1, column 12 |
| 06 | Decimal and loop | Decimal NUMBER and `wloop` |
| 07 | Function | `func`, parameters, comma, `return` |
| 08 | Operator boundaries | All six comparisons and assignment |
| 09 | Keyword boundaries | Whole-word matching, booleans, brackets, `floop` |
| 10 | Whitespace | Empty token sequence |
| 11 | Multi-line invalid input | `#` at line 2, column 14 |
| 12 | Invalid exclamation | `!` at line 1, column 9; `!=` remains valid |

Cases 08 and 09 are token-recognition fragments, not necessarily complete grammatical programs. A lexer checks tokens; a later parser checks syntax.

## Before the group submits

Merge against the current team implementation, run the tests again on that implementation, regenerate output, and complete the group's verification entry in the AI-use statement. Preserve the team's full Part 1 grammar and update it only for agreed changes. The available Part 1 document contains headings but no content for its grammar section, so a complete original grammar could not be checked here. This package has not been committed to GitHub.
