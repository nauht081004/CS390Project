<img width="1190" height="691" alt="image" src="https://github.com/user-attachments/assets/9e43da79-c40c-4f28-9c76-37f1a2d952c8" />

<img width="1052" height="105" alt="image" src="https://github.com/user-attachments/assets/ef3a106a-d7ae-4ef2-8f3d-e0ddc6efd2ab" />

<img width="1062" height="85" alt="image" src="https://github.com/user-attachments/assets/241ff9ba-8e0a-422e-8a5c-0c85a82cbc64" />

<img width="1030" height="92" alt="image" src="https://github.com/user-attachments/assets/735eec43-2c30-4175-a0d5-943bf4f8a178" />

<img width="993" height="132" alt="image" src="https://github.com/user-attachments/assets/860ccfc1-3d1b-4717-a37f-e6b7ad9d21a0" />

<img width="1081" height="101" alt="image" src="https://github.com/user-attachments/assets/11677028-84ac-46f3-9f22-6fd425257964" />


ANVI Part 4 — Test Results
1. Overview

The ANVI Part 4 interpreter extends the Part 3 lexer and recursive-descent parser with expression evaluation, variable storage, runtime error handling, and control structures.

Testing was performed using Python's built-in unittest framework and five complete ANVI example programs.

Automated test result: 22 tests passed, 0 failures, 0 errors.

2. Automated Unit Tests

Command used:

python -m unittest discover -s tests -v


Result:

Ran 22 tests
OK

Expression Evaluator Tests — 16 Passed
Test	Result
Boolean is not equal to number	PASS
Comparisons	PASS
Division by zero	PASS
Division with remainder	PASS
Exact division stays integer	PASS
Invalid boolean arithmetic	PASS
Invalid string-minus-number operation	PASS
Modulo	PASS
Modulo by zero	PASS
Parentheses	PASS
Operator precedence	PASS
String concatenation	PASS
Subtraction is left-to-right	PASS
Unary minus	PASS
Undefined variable	PASS
Variable lookup	PASS
Interpreter Tests — 6 Passed
Test	Result
Else branch executes when condition is false	PASS
If true branch executes	PASS
Infinite loop iteration limit	PASS
Assignment to undefined variable is rejected	PASS
Variable assignment and reassignment	PASS
While loop executes correctly	PASS
3. Example Program Tests

Five complete ANVI programs were executed using main.py.

Command format:

python main.py tests/program1_arithmetic.anvi

Program	Feature demonstrated	Result
program1_arithmetic.anvi	Arithmetic and operator precedence	PASS
program2_variables.anvi	Variables and arithmetic	PASS
program3_if_else.anvi	Conditional execution	PASS
program4_while.anvi	While loop and variable reassignment	PASS
program5_comparisons.anvi	Comparison operators and boolean output	PASS
Observed Output

The programs produced the following output when run in sequence:

14
20
10
15
12
12
200
1
2
3
4
5
T
T
T
T
T
T


The output above is the combined console output from the five commands. Each program should be checked individually against its expected output.

4. Runtime Error Handling

The expression evaluator's automated tests verified the following error cases:

Division by zero
Modulo by zero
Undefined variable access
Invalid arithmetic using incompatible types

The interpreter tests also verified that assigning to an undefined variable is rejected and that an infinite loop is stopped by the iteration limit.

5. Environment and Symbol Table

The environment stores variable names and their runtime values in a Python dictionary.

define(name, value) creates a variable.
get(name) retrieves a variable's value and reports an error if it does not exist.
assign(name, value) updates an existing variable and rejects undefined names.

These behaviors are exercised by the variable lookup, assignment, reassignment, and undefined-variable tests.

6. Conclusion

All 22 automated unit tests passed with no failures or errors. All five example programs also executed successfully and produced console output.

The test suite provides evidence that ANVI Part 4 supports expression evaluation, variable management, conditional execution, loops, comparisons, and selected runtime error cases.
