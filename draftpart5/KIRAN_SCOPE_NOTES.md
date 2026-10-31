# Kiran — Variable Scope and Recursion Support

## Files
- environment.py: local variables and parent-scope lookup.
- scope_runtime_kiran.py: separate environments for function calls.
- test_scope_kiran.py: scope checks.
- test_recursion_kiran.py: recursive-call helper tests.

## How scope works
Each Environment stores variables in a dictionary.
A local environment has a parent pointing to the scope where
the function was defined.

define() creates a variable in the current scope.
get() searches the current scope, then its parents.
assign() updates the nearest existing variable.

Each function call gets a fresh local environment so recursive
calls do not overwrite each other's parameters or local variables.

## Integration with function execution
1. Create one CallStack per interpreter and reuse it for all calls.
2. Store the defining environment with each function definition.
3. Make the function available by name before executing its body.
4. Evaluate arguments in the caller's environment.
5. Use CallStack.enter_call() with the function name, parameter
   names, evaluated arguments, and defining environment.
6. Execute the function body using the local environment yielded
   by enter_call().
7. Handle the function's return value using the interpreter's
   return mechanism.
8. If execution temporarily switches the interpreter or statement
   executor's environment, restore the previous environment in
   a finally block.

The helper removes its call frame on normal completion or errors.
It does not switch the interpreter's environment automatically.

## Verified results
- Six scope checks passed.
- Five recursive-call helper tests passed.
- All 23 existing interpreter tests passed.

## Remaining integration
The helper tests use Python recursion. They do not yet prove
that ANVI source programs support recursive function calls.
After integration with the parser and function execution code,
run ANVI tests for local/global shadowing and recursive factorial.
factorial(5) should return 120.

## AI assistance
ChatGPT provided scope code, a call-stack helper, tests, and
step-by-step guidance. I added the code and ran the tests locally.

One AI suggestion I verified was creating a fresh environment
for every call. The recursive factorial helper test confirmed
that deeper calls preserved each caller's parameter and left
the global variable unchanged.
