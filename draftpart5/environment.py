"""Store ANVI variables in local and enclosing scopes."""


class EnvironmentError(Exception):
    pass


class Environment:
    def __init__(self, parent=None):
        self.values = {}
        self.parent = parent

    def define(self, name, value):
        """Declare a variable in this scope only."""
        self.values[name] = value

    def get(self, name):
        """Look in this scope, then search enclosing scopes."""
        if name in self.values:
            return self.values[name]

        if self.parent is not None:
            return self.parent.get(name)

        raise EnvironmentError(f"undefined variable '{name}'")

    def assign(self, name, value):
        """Update the nearest existing variable."""
        if name in self.values:
            self.values[name] = value
            return

        if self.parent is not None:
            self.parent.assign(name, value)
            return

        raise EnvironmentError(
            f"cannot assign to undefined variable '{name}'"
        )

    def snapshot(self):
        """Return a copy of variables in this scope only."""
        return dict(self.values)