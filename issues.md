# Issues identified (helpdesk_system.py)

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| Shell injection (B602, High) | Security | 38 | `subprocess.call` with `shell=True` and a joined string lets input run any command | Pass a list of arguments, drop `shell=True`, validate hostname |
| Hardcoded password (B105) | Security | 8 | Admin password stored in source code | Read it from the `HELPDESK_ADMIN_PASSWORD` environment variable |
| Try / except / pass (B110, W0702, E722) | Bug | 23-24 | Bare `except` hides every error, so `add_note(999)` fails silently | Catch `KeyError` only and print a clear message |
| subprocess import (B404, Low) | Security | 2 | Import of `subprocess` flagged | Acceptable once `shell=True` is gone; marked `# nosec B404` |
| Mutable default argument (W0102) | Bug | 10 | `audit_trail=[]` is shared across all calls | Default to `None`, create a new list inside the function |
| Resource not closed (R1732, W1514) | Bug | 41-43 | `open()` without `with` and without encoding | `with open(file, "w", encoding="utf-8")` |
| Global statement, constant name (W0603, C0103) | Style | 7, 11 | Global counter, lowercase constant name | Use `itertools.count` (`TICKET_IDS`), no global needed |
| Comparison to None (C0121, E711) | Style | 33 | `tech == None` | Use `is None` |
| Function name (C0103) | Style | 30 | `unresolvedHighPriority` is camelCase | Rename to `unresolved_high_priority` |
| Missing docstrings (C0114, C0116) | Style | 1, 10, 17, 20, 26, 30, 37, 40, 45 | No module or function docstrings | Add short docstrings |
| Dict iteration (C0206) | Style | 32 | Loops over keys then indexes the dict | Use `.items()` |
| String formatting (C0209) | Style | 14 | Old `%` formatting | Use an f-string |
| Unused variable (W0612, F841) | Style | 47 | `t2` assigned but never used | Call the function without storing the result |
| Formatting (E302, E305, E501, C0301) | Style | 13, 14, 52 and many | Missing blank lines, lines over 79 characters | Add blank lines, wrap long lines, final newline |

## Bugs found by running the program (not reported by the tools)

| Problem | Why no tool flagged it | Fix |
|---------|------------------------|-----|
| Priority -7 accepted for a ticket | Valid integer, not a syntax or style problem | `raise_ticket` rejects urgency outside 1-5 |
| `close_ticket` silently does nothing on a wrong password | Logic problem | Prints a message when the password is wrong or not set |
| `ping -c 1` only works on Linux/Mac | Platform behaviour | Use `-n` on Windows, `-c` otherwise |
| `int(urgency)` crashes on non-numeric input | Runtime error | `ValueError` is caught in `main` and reported |
| `main()` runs when the file is imported | Design problem | Added `if __name__ == "__main__"` guard |

## Results

| Tool | Before | After |
|------|--------|-------|
| Pylint | 5.53/10 (21 messages) | 10.00/10 |
| Bandit | 4 issues (1 High, 3 Low) | No issues identified |
| Flake8 | 15 issues | 0 issues |
