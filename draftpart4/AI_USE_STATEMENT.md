AI Use Statement — ANVI Part 4
Purpose of AI Assistance

Our group used ChatGPT as an AI-assisted resource during the development and documentation of the ANVI Part 4 interpreter. AI assistance helped us understand interpreter implementation, review code, identify possible improvements, and organize project documentation.

Areas Where AI Was Used

AI assistance was used for the following tasks:

Reviewing the interpreter's structure, including the lexer, AST nodes, parser, environment, expression evaluator, and statement executor.
Understanding how a tree-walking interpreter evaluates expressions and executes statements.
Reviewing the environment and symbol table implementation.
Identifying possible improvements to runtime error handling.
Reviewing the EBNF grammar to ensure it matched the language features implemented by the parser.
Developing test cases for arithmetic, variables, comparisons, conditional statements, loops, and runtime errors.
Organizing the README and project documentation.
AI-Generated Suggestion Reviewed and Modified

One AI-generated suggestion was to modify the condition-handling method in control_structures_kiran.py so that if and wloop conditions accept only boolean values (T and F), rather than accepting numbers as conditions.

We reviewed the existing code and compared its behavior with the documented language rules. The original implementation allowed numeric conditions and converted them to booleans. We changed the condition-handling method to reject non-boolean values and return the boolean result directly.

The change was intended to make the implementation consistent with the language specification. The group should verify this behavior using appropriate runtime tests before considering the change complete.

AI assistance also helped identify duplicated wording in the division-by-zero error message in expression_evaluator.py. The error message was simplified to make runtime errors clearer.

Human Review and Responsibility

AI-generated suggestions were treated as recommendations rather than automatically accepted solutions. Group members reviewed suggested changes and remained responsible for integrating, testing, and understanding the code.

The group is responsible for ensuring that the final implementation, test results, grammar, and documentation accurately represent the submitted project.

Conclusion

AI was used as a supporting tool for programming assistance, code review, testing ideas, and documentation. The goal was to improve the clarity, consistency, and reliability of the ANVI interpreter while maintaining human review and responsibility for the final submission.
