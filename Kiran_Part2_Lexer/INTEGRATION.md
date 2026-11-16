# Integrating Kiran's contribution

1. Keep the current team lexer as the main implementation. Compare `token_defs.py` with its token names and values. The reference lexer is provided to demonstrate and test the contribution; it does not establish what the other members have implemented.
2. Add `errors.py`, then import `LexicalError` in the team's lexer. At the scanning position where no valid token or whitespace matches, raise:

   ```python
   raise LexicalError(character, line, column, source_line)
   ```

   `line` and `column` start at 1. `source_line` is the full current line without its newline. Track positions through skipped whitespace too. Normalize CRLF/CR before scanning or handle them explicitly.
3. Catch `LexicalError` only at the CLI boundary, print it to standard error, and return exit code 1. Do not catch every exception and disguise coding bugs as lexical errors.
4. Match from the current position and reject unmatched characters. A regex search that jumps ahead to the next known token can silently skip `@`. Check two-character operators before their one-character prefixes.
5. Import the team's tokenization function in `run_tests.py`. If its API differs, adapt its return values to `(type, lexeme)` pairs and retain the independent expected cases. Align agreed token names in `cases.json`; do not derive expected output by calling the lexer under test.
6. Run `python run_tests.py`. After integration, point the CLI checks and output generator at the final lexer, then run `python generate_outputs.py`. Review the error location and all token outputs.
7. Review the decimal/identifier rules in `LEXICAL_RULES.md` with the team. Retain the existing grammar unless an agreed change is needed.
8. Upload your contribution to the existing group repository on a separate branch or agreed folder. Include the reusable error code, tests, docs, and output. Put the reference lexer in a clearly named reference folder if the team already has `lexer.py`; do not overwrite their work. A suitable commit message is `Add lexical error handling and ANVI lexer test cases`.

When the team combines the final submission into one source file, move the error class and token definitions above the scanning function and remove their local imports. Point the tests and output generator at the merged module. Keep test files and documentation in the final ZIP.

Suggested explanation of your portion: The error class reports the invalid character and its source position. The scanner raises this error instead of skipping the character. The command-line handler prints a readable message. The tests compare complete token sequences or the exact expected error location.
