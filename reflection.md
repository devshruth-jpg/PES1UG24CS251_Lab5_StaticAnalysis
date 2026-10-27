# Reflection

## 1. What did each tool catch, and which was most useful?
Pylint found the most (21 messages) and took the score from 5.53 to 10.00. It mostly caught code quality problems like the mutable default, the bare except and missing docstrings. Flake8 only cared about formatting, mainly blank lines and long lines. Bandit gave just four findings, but the one High finding, `shell=True` in the ping function, was the most serious problem in the whole file. Pylint was the most useful overall, but Bandit mattered most per finding.

## 2. Which issues were hardest or most surprising to fix?
`shell=True` took the most thought. Deleting it breaks the command, so the call became an argument list, the hostname needed validating, and the ping flag differs between Windows (`-n`) and Linux (`-c`). The hardcoded password was similar: it moved to an environment variable, so the program now needs it set to close a ticket. I was also surprised that a global counter could be replaced neatly with `itertools.count`.

## 3. Did the tools give false positives, or miss anything?
A few Bandit Low findings were noise. B404 only says `subprocess` is imported, which is fine once it is used safely, so I marked it `# nosec` with a reason instead of removing a needed import. More importantly, the tools missed real bugs: a priority of -7 was accepted, a wrong password was silently ignored, and `ping -c` fails on Windows. I only found those by running the program and reading the output.

## 4. How would you use static analysis in a real project?
I would run all three tools before every commit with a pre-commit hook, and again in CI on every pull request, failing the build on any High Bandit finding or a Pylint score below a set threshold. Fix in order of severity: security first, then bugs, then style. And only suppress a warning with a written reason, never just to make the report clean.

## 5. What did you learn about code quality and maintainability?
The original code ran fine yet scored 5.53, so working code is not the same as good code. After the fixes it is easier to read (names, docstrings), safer, and fails loudly instead of silently. Static analysis works well as a first reviewer, but it does not replace testing or reading the program's output.
