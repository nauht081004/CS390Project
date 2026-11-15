# ANVI Part 4 — Expected and Actual Output

Outputs below were captured by running the interpreter against each complete test program.

## program1_arithmetic.anvi

Source:
```anvi
let result = 2 + 3 * 4;
display(result);
display((2 + 3) * 4);
```

Actual output (exit code 0):
```text
14
20
```

## program2_variables.anvi

Source:
```anvi
let x = 10;
let y = x + 5;
display(x);
display(y);
x = y - 3;
display(x);
```

Actual output (exit code 0):
```text
10
15
12
```

## program3_if_else.anvi

Source:
```anvi
let x = 12;
if (x >= 10) {
    display(x);
} else {
    display(0);
}
if (x < 10) {
    display(100);
} else {
    display(200);
}
```

Actual output (exit code 0):
```text
12
200
```

## program4_wloop.anvi

Source:
```anvi
let x = 1;
wloop (x <= 5) {
    display(x);
    x = x + 1;
}
```

Actual output (exit code 0):
```text
1
2
3
4
5
```

## program5_comparisons.anvi

Source:
```anvi
display(5 == 5);
display(5 != 4);
display(3 < 4);
display(4 > 3);
display(4 <= 4);
display(5 >= 4);
```

Actual output (exit code 0):
```text
T
T
T
T
T
T
```
