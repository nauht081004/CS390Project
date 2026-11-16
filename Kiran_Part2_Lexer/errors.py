"""Kiran's assigned area: lexical errors. Prepared with ChatGPT assistance."""

class LexicalError(Exception):
    """An invalid source character, with a one-based source position."""

    def __init__(self, character, line, column, source_line):
        self.character = character
        self.line = line
        self.column = column
        self.source_line = source_line
        super().__init__(
            f"Lexical error at line {line}, column {column}: "
            f"invalid character {character!r}."
        )

    def __str__(self):
        # Expand tabs in both the source and prefix so the caret stays aligned.
        shown_line = self.source_line.expandtabs(4)
        prefix = self.source_line[:self.column - 1].expandtabs(4)
        return f"{super().__str__()}\n{shown_line}\n{' ' * len(prefix)}^"
