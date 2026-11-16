"""Run every source case and write actual CLI output to test_outputs.txt."""
import json
import subprocess
import sys
from pathlib import Path
root = Path(__file__).resolve().parent
parts = []
for case in json.loads((root / "tests/cases.json").read_text()):
    path = root / "tests" / case["file"]
    result = subprocess.run([sys.executable, str(root / "lexer.py"), str(path)],
                            capture_output=True, text=True)
    parts.extend([f"=== {case['name']} ===", f"Command: python lexer.py tests/{case['file']}",
                  "Source:", path.read_text().rstrip(), "Output:",
                  (result.stdout + result.stderr).rstrip(), f"Exit code: {result.returncode}", ""])
(root / "test_outputs.txt").write_text("\n".join(parts), encoding="utf-8")
print("Wrote test_outputs.txt")
