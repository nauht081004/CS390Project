"""Manage separate local scopes for ANVI function calls."""

from contextlib import contextmanager
from environment import Environment


class CallStack:
    def __init__(self, max_depth=50):
        self.frames = []
        self.max_depth = max_depth

    @contextmanager
    def enter_call(
        self, function_name, parameters, arguments,
        definition_environment
    ):
        # Arguments must already be evaluated by the caller.
        if len(parameters) != len(arguments):
            raise RuntimeError(
                f"{function_name} expects {len(parameters)} "
                f"arguments, but received {len(arguments)}"
            )

        if len(self.frames) >= self.max_depth:
            raise RuntimeError(
                "Maximum function call depth exceeded"
            )

        # Use the scope where the function was defined.
        # Each call receives a fresh local environment.
        local_environment = Environment(
            parent=definition_environment
        )

        for name, value in zip(parameters, arguments):
            local_environment.define(name, value)

        self.frames.append(local_environment)

        try:
            yield local_environment
        finally:
            # Clean up even when a function returns or fails.
            self.frames.pop()