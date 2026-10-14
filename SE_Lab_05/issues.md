# Issues Found and Fixed

Script: `scholarship_disbursement.py`

Before: Pylint **5.00/10**, Bandit **4 issues** (1 Medium, 3 Low), Flake8 **6 issues**.
After: Pylint **10.00/10**, Bandit **0 issues**, Flake8 **0 issues**.

Reports are in `reports/before/` and `reports/after/`.

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| SQL injection (Bandit B608, Medium) | Security | 10 | `INSERT` built with `%` string formatting, so a student name like `x'); DROP TABLE awards;--` becomes part of the SQL | Use `?` placeholders and pass `(student, scheme, amount)` as parameters |
| Shell command (Bandit B605 Low, B607 Low) | Security | 26 | `os.system("echo ...")` starts a shell and uses a partial executable path; no need for a subprocess at all | Replace with `print("archiving awards")` and remove the unused `os` import |
| Silent failure (Bandit B110 Low, Pylint W0718) | Security / Bug | 25-28 | `try: ... except Exception: pass` swallows every error, so a failed archive would go unnoticed | Remove the try/except; nothing in the body needs it |
| Mutable default arg (Pylint W0102) | Bug | 9 | `audit=[]` is created once and shared across all calls, so the audit list grows across unrelated calls | Default to `None` and create a new list inside `grant()` |
| Global state (Pylint W0603, C0103) | Design | 6, 16 | `global disbursed_total` is mutable module state and not UPPER_CASE; it can drift from the database | Remove it; add `get_disbursed_total()` which sums disbursed awards in SQL |
| Inconsistent returns (Pylint R1710) | Bug | 15-21 | `disburse()` returns a value on one path and falls off the end (implicit `None`) on the other | Return `None` explicitly when the award is missing |
| Double disbursement (found in review) | Bug | 17-20 | The same award id could be disbursed twice, adding its amount to the total each time | Select only rows with `disbursed = 0`, so a second call returns `None` |
| Naming (Pylint C0103) | Style | 31 | `bySchemeCount` is camelCase | Rename to `count_by_scheme` |
| None comparison (Flake8 E711, Pylint C0121) | Style | 32 | `scheme == None` | Use `scheme is None` |
| Missing docstrings (Pylint C0114, C0116) | Style | 1, 9, 15, 24, 31, 37 | Module and five functions have no docstrings | Add short docstrings |
| Long lines (Flake8 E501, Pylint C0301) | Style | 5, 10, 17, 19, 34 | Lines up to 130 characters, limit is 79 for Flake8 / 100 for Pylint | Wrap SQL strings and call arguments across lines |
| f-string suggestion (Pylint C0209) | Style | 10 | `%` formatting on a string | Resolved by the parameterized SQL fix |
| Import-time side effects | Design | 45 | `main()` ran on import, so importing the module for testing executed the demo | Wrap in `if __name__ == "__main__":` |

## Commits

1. Fix Bandit findings (B608, B605, B607, B110)
2. Fix Pylint findings (docstrings, mutable default, global, returns, naming)
3. Fix Flake8 findings (E501, E711)

## Behavior check

The program's output is identical before and after:

```
50000 None
1 50000
archiving awards
```
