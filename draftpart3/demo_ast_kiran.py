"""Print three real ASTs using the team's expression parser."""
from test_parser_kiran import parse_complete_expression

EXAMPLES = [
    ('2 + 3 * 4', 'Multiplication is the right child of addition.'),
    ('(2 + 3) * 4', 'Parentheses place addition beneath multiplication.'),
    ('10 - 3 - 2', 'The left subtraction subtree represents (10 - 3) - 2.'),
]

if __name__ == '__main__':
    for index, (source, explanation) in enumerate(EXAMPLES, 1):
        print(f'Example {index}\nInput: {source}\nAST:')
        print(parse_complete_expression(source).to_string())
        print(f'Explanation: {explanation}\n')
