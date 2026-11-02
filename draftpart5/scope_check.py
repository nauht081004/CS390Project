from interpreter import interpret_source

source = """
let x = 10;

func test() {
    let x = 20;
    display(x);
}

test();
display(x);
"""

print(interpret_source(source))
