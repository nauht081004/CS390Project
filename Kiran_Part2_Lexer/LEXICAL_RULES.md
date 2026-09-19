# ANVI lexical rules and grammar status

Source checked: `FinalProject_Part1_Group3_ver2.docx`, the available Part 1 document. It defines ANVI keywords, operators, delimiters, function syntax, and example programs. Its section 8 (initial BNF/EBNF grammar) is blank. The live GitHub code and any later group grammar were not available for this work.

## Rules followed from Part 1

- Keywords, case-sensitive: `let if else wloop floop func return display T F`.
- `display`, `wloop`, and `func` are the language's equivalents of `print`, `while`, and `function`. The English alternatives are identifiers in this reference lexer, not additional reserved words.
- Arithmetic: `+ - * / %`.
- Comparison: `== != < > <= >=`.
- Assignment: `=`.
- Delimiters: `( ) { } [ ] , ;`.
- Each keyword is recognized only after reading an entire identifier: `letter` is ID, not LET followed by another token.

## Explicit implementation assumptions to confirm with the team

The available Part 1 material does not specify detailed identifier/number lexical patterns. This reference uses:

```text
identifier = (ASCII letter | "_") { ASCII letter | digit | "_" }
number     = digit { digit } [ "." digit { digit } ]
digit      = "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
```

Numbers retain their source spelling as strings; numeric conversion belongs in a later stage. Negative values have a MINUS token followed by NUMBER. Exponents, leading-dot decimals, and trailing-dot decimals are not supported. Number/identifier adjacency such as `10abc` is emitted as NUMBER then ID; any syntax restriction on this is left to the parser.

Spaces, tabs, newlines, form feed, and vertical tabs are ignored. CRLF and CR are normalized to LF. Column positions count source characters, with a tab counting as one character; the displayed caret expands tabs to four-space tab stops.

No string literals or comments are specified in the checked Part 1 file, so quote characters and `#` produce lexical errors. Confirm whether the group's later grammar adds them. There is no explicit EOF token. The first invalid character stops scanning.

No changes to the checked Part 1 keyword/operator/delimiter list are proposed. The rules above document implementation assumptions, not a verified replacement for the group's full grammar. Include the actual group grammar if it changes during integration.
