# Pending statement/program tests - NOT RUN

The uploaded parser has no statement or program entry point. These cases are planned against grammar.txt; they are not completed or passing tests.

| Input | Expected structural check |
| --- | --- |
| let x = 5; | AssignmentNode assigning NumberNode(5) to VariableNode(x) |
| x = 7; | AssignmentNode for reassignment |
| display(2 + 3 * 4); | PrintNode containing addition with multiplication on the right |
| let x = 5; display(x); | ProgramNode with assignment then print, in source order |
| let x = 2 + 3 * 4; display(x); | ProgramNode preserving precedence inside the assignment |
| let x = ; | Meaningful missing-expression syntax error after recognizing the assignment |
| display(5; | Meaningful missing-RPAREN syntax error |
| let x = 5 | Missing-semicolon syntax error, as required by the current grammar |

Use the team's final public parser entry point once provided. Confirm full source consumption, not just successful parsing of the first statement. Re-run all tests against the integrated files; update actual results honestly.
