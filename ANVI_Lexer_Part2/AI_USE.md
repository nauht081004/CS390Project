# AI Use Statement

**AI Tool(s) Used:**
Claude 

**How did your group use AI for this project milestone?**
One of us wrote the main structure of the lexer — the Token class, the keyword list, and the tokenize() function that actually reads through the code. We used Claude mainly as a helper on top of that: to understand how the code worked, to catch a bug we wouldn't have noticed just by reading it, and to help write the test cases and documentation. The core design and the actual ANVI language itself all came from our own work in Part 1 and our draft for Part 2, Claude didn't design any of that, it just helped us finish and check it.

**Which project components received AI assistance?**
- Filling in the parentheses/braces/commas/semicolons section
- Catching and fixing a bug in the peek() function that made the whole file crash
- Writing the five test cases
- Writing the output file and the README

**Describe at least one AI-generated suggestion, explanation, or code segment that your group modified, corrected, rejected, or improved.**
The peek() function had a small bug, it used a variable called offset that didn't actually exist anywhere, and was also missing a closing bracket. Because of this, the file wouldn't even run at all. Claude pointed this out and explained why it was broken, and suggested fixing it by having peek() just look one character ahead using self.pos + 1. We made that fix ourselves in the actual file, then tested it by running the lexer on a simple example and checking by eye that the output looked right before trusting it enough to build tests on top of it.

**How did your group test or independently verify AI-assisted work?**
We didn't just trust the code because it was suggested — we ran it ourselves every time. After fixing peek(), we tested the lexer by hand in the terminal first. Once that looked right, we wrote five test cases covering a variable, some math, a print statement, an if/else, and bad input, and ran them all with Python's built-in test tool. All five passed, including the one checking that a bad character like @ gives a proper error instead of crashing the program.

**What did your group learn from using AI during this milestone?**
We learned how a lexer actually reads code character by character and turns it into tokens, and we got more comfortable writing and running tests. The biggest lesson was to always run code ourselves and check it, instead of assuming it works just because it looks fine — the peek() bug is a good example of something that looked okay at a glance but would've stopped the whole thing from running if we hadn't caught it.