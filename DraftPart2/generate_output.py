from lexer import lex, LexerError

cases = [
    ("Test 1: Variable declaration", "let x = 10;"),
    ("Test 2: Arithmetic expression", "let result = x + y * 2 - 1;"),
    ("Test 3: Print statement", "display(x + 1);"),
    ("Test 4: Control structure",
     "if (x > 10) { display(x); } else { display(0); }"),
    ("Test 5: Invalid input", "let x = 10 @ 5;"),
]

with open("lexer_output.txt", "w") as out:
    for name, src in cases:
        out.write(f"=== {name} ===\n")
        out.write(f"Source: {src}\n")
        out.write("Tokens:\n")
        try:
            for tok in lex(src):
                out.write(f"  {tok}\n")
        except LexerError as e:
            out.write(f"  {e}\n")
        out.write("\n")

print("Wrote lexer_output.txt")
