# AI Use Statement — Part 5

AI tools (ChatGPT) were used as a programming assistant while extending the ANVI interpreter. Assistance included reviewing the Part 4 project structure, proposing an implementation approach for function AST nodes and parsing, explaining how nested environments can provide local scope, and helping design test cases for function calls, return values, scope, and recursion.

One AI-generated suggestion was to use a parent-linked environment for function-local variables. This was implemented and verified with a scope test in which a function declares a local `x = 20` while the global `x` remains `10`; the output is `20` followed by `10`. AI-generated implementation changes were tested against the existing Part 4 regression suite and the new Part 5 tests. The final implementation was adjusted where needed to preserve the project's existing ANVI keywords (`func`, `display`, and `wloop`) and existing syntax compatibility.

AI assistance was used to support implementation and testing; the submitted code and behavior should be reviewed by the project team, and this statement should be edited if it does not accurately describe each team member's use of AI.
