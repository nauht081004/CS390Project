# AI Use Statement

**AI Tool(s) Used:**
Claude (Anthropic) and ChatGPT/Codex (OpenAI) were used by different members on different parts of this milestone.

**How did your group use AI for this project milestone?**
We used AI tools to help design the structure of the parser, including how to lay out operator precedence as a chain of functions, how to add statement and program parsing on top of that, and how to write and run a thorough test suite. One AI tool was also used to review the finished parser and generate test cases and AST demonstrations against it. The actual ANVI language design and grammar came from our own work in earlier parts — AI helped us implement, test, and document it correctly, not design it.

**Which project components received AI assistance?**
- Structuring the expression-parsing methods (comparison, addition, multiplication, unary, primary) in `parser.py`
- Structuring the statement and program parsing methods (`parse_statement`, `parse_assignment`, `parse_print`, `parse_program`)
- The two test files (expression-level and statement-level tests) and the AST demonstration script
- README 

**Describe at least one AI-generated suggestion, explanation, or code segment that your group modified, corrected, rejected, or improved.**
One AI tool initially wrote test cases that only checked whether parsing a bare expression succeeded, without confirming the entire input was consumed. Reviewing the parser showed that `parse_expression` on its own doesn't enforce reaching the end of input, so an incomplete or malformed expression could technically "pass" a loose test. The test helper was corrected to also call `expect('EOF')` after parsing, and a specific test (parsing `"2 3"`, two numbers with nothing joining them) was added to confirm leftover tokens are now correctly rejected as a syntax error. Separately, when combining everyone's work, we found that an early set of test notes claimed statement and program parsing were still missing from the parser — this was accurate at the time it was written, but became outdated once that part was finished. We caught this during integration and corrected the documentation before submitting, rather than leaving outdated status notes in the final version.

**How did your group test or independently verify AI-assisted work?**
No AI-suggested code was accepted without being run. We ran the parser ourselves on real inputs, including the exact example from the assignment (`2 + 3 * 4`), and checked by hand that the resulting tree placed multiplication inside addition, confirming correct precedence. We then ran the full combined test suite — 20 tests total covering expressions, statements, multiple statements, and error cases like a missing expression, a missing parenthesis, and a missing semicolon — and confirmed all 20 passed together against the same final parser file, not just individually against separate drafts.

**What did your group learn from using AI during this milestone?**
We learned how to structure a recursive-descent parser so that operator precedence falls naturally out of how functions call each other, and how statement-level parsing builds on top of expression-level parsing rather than replacing it. We also learned a practical integration lesson: when different people work on different pieces at different times, documentation (like test notes or a README) can get out of sync with the actual code. Catching and fixing that mismatch before submitting was as important as writing the code itself.