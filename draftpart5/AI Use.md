# AI Use Statement

**AI Tool(s) Used:**
Claude (Anthropic) and ChatGPT/Codex (OpenAI) were used by different members on different parts of this milestone.

**How did your group use AI for this project milestone?**
We used AI tools to help implement and debug function definitions, function calls, return statements, and variable scope in the ANVI interpreter. AI also assisted with updating the parser and AST, implementing function execution, designing recursive function examples, writing tests, and updating documentation. The ANVI language design and the foundation of the interpreter came from our own work in earlier parts — AI helped us extend, test, and integrate the existing code.

**Which project components received AI assistance?**
Function definitions, parameters, and function calls in the parser and AST

Function execution and return-value handling in the interpreter

Local variable environments and variable scope

Recursion as an extension feature

README and example programs

**Describe at least one AI-generated suggestion, explanation, or code segment that your group modified, corrected, rejected, or improved.**
DuAI suggested using a separate local environment for each function call to handle parameters and local variables. We reviewed this approach and integrated it with our existing environment implementation. We also tested variable shadowing to make sure that changing a local variable inside a function would not accidentally modify a global variable with the same name. This helped us verify that function scope behaved as intended.

**How did your group test or independently verify AI-assisted work?**
We tested the new functionality using separate programs for function definitions, parameters, function calls, return values, local and global variables, and recursion. We also tested error cases, such as calling an undefined function, passing an incorrect number of arguments, and using return outside a function. In addition, we ran the existing Part 4 tests to check that the new features did not break previously implemented functionality.

**What did your group learn from using AI during this milestone?**
WWe learned how function definitions and function calls are processed through the parser, AST, and interpreter. We also gained a better understanding of how local environments help implement variable scope and how return statements transfer values from functions back to their callers. Implementing recursion helped us understand how functions can call themselves while maintaining separate local environments for each call. We also learned that AI-generated code needs to be reviewed and tested carefully, especially when integrating new features into an existing interpreter.