"""Scholarship disbursement ledger.

Grant awards, disburse funds and count awards by scheme.
"""
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute(
    "CREATE TABLE awards ("
    "id INTEGER PRIMARY KEY, student TEXT, scheme TEXT, "
    "amount INTEGER, disbursed INTEGER)"
)


def grant(student, scheme, amount, audit=None):
    """Record a new award and append the student to the audit list."""
    if audit is None:
        audit = []
    conn.execute(
        "INSERT INTO awards (student, scheme, amount, disbursed) "
        "VALUES (?, ?, ?, 0)",
        (student, scheme, amount),
    )
    audit.append(student)
    return audit


def disburse(award_id):
    """Disburse an award and return its amount, or None if it cannot be paid.

    An award that does not exist, or was already disbursed, returns None.
    """
    row = conn.execute(
        "SELECT amount FROM awards WHERE id = ? AND disbursed = 0",
        (award_id,),
    ).fetchone()
    if row is None:
        return None
    conn.execute("UPDATE awards SET disbursed = 1 WHERE id = ?", (award_id,))
    return row[0]


def get_disbursed_total():
    """Return the total amount disbursed so far."""
    return conn.execute(
        "SELECT COALESCE(SUM(amount), 0) FROM awards WHERE disbursed = 1"
    ).fetchone()[0]


def archive():
    """Archive the awards records."""
    print("archiving awards")


def count_by_scheme(scheme):
    """Return how many awards exist under the given scheme."""
    if scheme is None:
        return 0
    return conn.execute(
        "SELECT COUNT(*) FROM awards WHERE scheme = ?", (scheme,)
    ).fetchone()[0]


def main():
    """Run a short demonstration of the ledger."""
    grant("Ishaan", "Merit", 50000)
    grant("Divya", "Need-based", 75000)
    print(disburse(1), disburse(9))
    print(count_by_scheme("Merit"), get_disbursed_total())
    archive()


if __name__ == "__main__":
    main()
