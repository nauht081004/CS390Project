from environment import Environment, EnvironmentError

# Create the global scope.
global_scope = Environment()
global_scope.define("x", 10)

# Create a local scope connected to the global scope.
local_scope = Environment(parent=global_scope)
local_scope.define("x", 20)

assert local_scope.get("x") == 20
assert global_scope.get("x") == 10
print("PASS: Local x does not overwrite global x.")

# Local scope can read global variables.
global_scope.define("total", 100)
assert local_scope.get("total") == 100
print("PASS: Local scope can read global variables.")

# Assignment updates the nearest existing variable.
local_scope.assign("x", 30)
assert local_scope.get("x") == 30
assert global_scope.get("x") == 10
print("PASS: Assignment updates the local variable.")

local_scope.assign("total", 200)
assert global_scope.get("total") == 200
print("PASS: Assignment can update an existing global variable.")

# Local variables must not appear in the global scope.
local_scope.define("secret", 99)
try:
    global_scope.get("secret")
except EnvironmentError:
    print("PASS: Local variables stay private.")
else:
    raise AssertionError("Local variable leaked into global scope!")

# Separate calls need separate local variables.
another_scope = Environment(parent=global_scope)
another_scope.define("x", 50)
assert local_scope.get("x") == 30
assert another_scope.get("x") == 50
print("PASS: Separate local scopes keep separate values.")

print("All scope tests passed!")