"""Run an ANVI source file: python main.py path/to/program.anvi"""
import sys
from lexer import LexerError
from parser import ParserError, parse_source
from interpreter import Interpreter, RuntimeErrorANVI

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <source-file>")
        return 2
    try:
        with open(sys.argv[1], "r", encoding="utf-8") as file:
            source = file.read()
        ast = parse_source(source)
        interpreter = Interpreter()
        for line in interpreter.interpret(ast):
            print(line)
        return 0
    except (OSError, LexerError, ParserError, RuntimeErrorANVI) as error:
        print(error, file=sys.stderr)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
