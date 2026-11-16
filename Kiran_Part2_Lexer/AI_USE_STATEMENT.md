# AI Use Statement

ChatGPT was used to read the available ANVI Part 1 document and prepare a draft Python lexical-error class, a standalone reference lexer, token definitions, test source files, expected token/error data, documentation, and integration instructions. ChatGPT also ran the generated reference implementation and tests in its execution environment and saved the results. This package is AI-assisted and should not be described as entirely student-written.

## Specific suggestion to verify

AI suggested matching two-character comparison operators before their one-character prefixes. For example, `>=` should produce one GE token rather than GT followed by ASSIGN. It also recommended raising an error at an unmatched character instead of searching ahead and skipping it.

The automated reference checks run by ChatGPT verified that case 08 recognizes `==`, `!=`, `<=`, and `>=` as single tokens, and case 05 rejects `@` at line 1, column 12. A CLI test checked exit status 1 and confirmed no traceback was printed for that input. These results document AI-run checks, not a completed review by a group member.

## Group verification — complete after reviewing the merged code

The assignment requires at least one AI suggestion that the group verified, modified, corrected, or rejected. A member must actually perform and record this review before submission.

- Reviewer and date: [complete after review]
- AI suggestion reviewed: [for example, longest-operator matching]
- Action taken: [verified / modified / corrected / rejected]
- Evidence from the final group lexer: [command, observed output, and any change made]

For the suggested check, run the final lexer on `tests/08_operator_boundaries.anvi` and confirm that each two-character comparison is a single token. Then run `tests/05_invalid.anvi` and confirm the invalid character is reported. Record what actually happened; do not claim a check was performed before doing it.
