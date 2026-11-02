AI Use Statement – ANVI Part 5
Use of AI Assistance

ChatGPT was used as an AI assistance tool during the development of ANVI Part 5. AI assistance helped with understanding programming concepts, troubleshooting errors, writing and reviewing code, creating tests, and documenting the project.

The areas where AI assistance was used included:

Functions: Assistance with implementing function definitions, parameters, function calls, and return values.
Variable Scope: Assistance with creating the Environment class to manage local and global variables using parent environments.
Recursion: Assistance with implementing separate local environments for recursive function calls and adding a function call-depth limit.
Testing: Assistance with creating scope and recursion tests and developing five ANVI example programs.
Debugging: Assistance with identifying and fixing issues involving function syntax, recursive calls, and function call-depth errors.
Documentation: Assistance with preparing the README and EBNF grammar documentation.
AI-Generated Suggestions Verified

One AI-generated suggestion was to create a fresh local environment for every function call rather than reusing the same environment.

This suggestion was verified by running recursion tests. The factorial example demonstrated that recursive calls preserved their separate parameter values and correctly calculated:

factorial(5) = 120

Another suggestion was to implement a maximum function call-depth limit to prevent infinite recursive calls. This was tested using a function that repeatedly called itself. The interpreter correctly stopped execution with a function call-depth limit error instead of continuing indefinitely.

Student Contributions and Verification

I manually added and organized the code in my project files, ran the interpreter and test programs locally, reviewed error messages, and verified the results.

I also tested function parameters, return values, local and global variable scope, nested function calls, and recursive factorial calculations.

The final implementation was tested locally using Python's unittest framework and separate ANVI test programs.

AI assistance was used as a development and learning aid. I reviewed and tested the suggested implementations rather than relying only on generated code.
