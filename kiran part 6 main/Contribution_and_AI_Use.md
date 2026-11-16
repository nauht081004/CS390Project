# Contribution and AI use

Prepared for Kiran Reddy Kommula's testing and quality assurance assignment.
This package contains 26 ANVI programs, a subprocess regression runner, expected
outputs, actual results, terminal screenshots, a report section, a video script,
and a proposed unary-plus fix. The uploaded interpreter was preserved unchanged.

ChatGPT assisted with source inspection, test design, runner implementation, executing
tests, documentation, screenshot capture, and proposing and checking a fix.
Baseline execution returned 25/26 passing programs; a patched copy returned 26/26.
All 11 existing test scripts exited successfully against their matching versions.

Example requiring correction: an initial expectation that the existing interpreter
would evaluate display(+5) as 5 was contradicted by execution. The parser accepted
the source but the evaluator raised an unknown-unary-operator error. The defect
was recorded, a numeric unary-plus branch was proposed, and the suite was rerun.
This is a correction of an assumption during AI-assisted testing, not evidence
that the original defect was AI-authored. The group must supply its own verified
example if the instructor specifically requires a correction to earlier AI code.

Kiran must review and run the package, understand the checks, and record his own
presentation before claiming personal completion. No teammate's unobserved work,
GitHub upload, or human recording is claimed here.
