"""Runtime environment (symbol table) for ANVI variables."""

class EnvironmentError(Exception):
    pass


class Environment:
    def __init__(self):
        self.values = {}

    def define(self, name, value):
        """Create/update a variable from a let declaration."""
        self.values[name] = value

    def get(self, name):
        if name not in self.values:
            raise EnvironmentError(f"undefined variable '{name}'")
        return self.values[name]

    def assign(self, name, value):
        """Update an existing variable; assignment cannot create a new one."""
        if name not in self.values:
            raise EnvironmentError(f"cannot assign to undefined variable '{name}'")
        self.values[name] = value

    def snapshot(self):
        return dict(self.values)
