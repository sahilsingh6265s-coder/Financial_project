"""Simulated investor cash reconciliation. Amounts are integer minor units."""
import sqlite3
from datetime import date
from pathlib import Path

FOLDER = Path(__file__).resolve().parent
FIELDS = "id, account, reference, currency, amount, posted"
SOURCES = ("bank", "ledger")


def initialize(db):
    for table in SOURCES:
        db.execute(f"""CREATE TABLE IF NOT EXISTS {table} (
            id TEXT PRIMARY KEY NOT NULL, account TEXT NOT NULL, reference TEXT NOT NULL,
            currency TEXT NOT NULL, amount INTEGER NOT NULL, posted TEXT NOT NULL)""")
    db.execute("""CREATE TABLE IF NOT EXISTS outcomes (
        bank_id TEXT PRIMARY KEY NOT NULL, ledger_id TEXT, status TEXT NOT NULL,
        variance INTEGER)""")


def import_rows(db, table, rows):
    if table not in SOURCES:
        raise ValueError("Unknown source")
    added = 0
    with db:
        for record in rows:
            row = tuple(record)
            if len(row) != 6 or not all(isinstance(v, str) and v.strip() for v in row[:4]):
                raise ValueError("Each deposit requires identifiers and currency")
            if type(row[4]) is not int or row[4] <= 0:
                raise ValueError("Supply a positive amount in integer minor units")
            date.fromisoformat(row[5])
            prior = db.execute(f"SELECT {FIELDS} FROM {table} WHERE id=?", (row[0],)).fetchone()
            if prior is None:
                db.execute(f"INSERT INTO {table} VALUES (?,?,?,?,?,?)", row)
                added += 1
            elif tuple(prior) != row:
                raise ValueError(f"Conflicting {table} transaction ID: {row[0]}")
    return added


def reconcile(db):
    with db:
        db.execute("DELETE FROM outcomes")
        db.execute((FOLDER / "match.sql").read_text())


def audit(db):
    return {path.stem: db.execute(path.read_text()).fetchall()
            for path in sorted((FOLDER / "checks").glob("*.sql"))}


DAY = "2026-11-24"
LEDGER = [
    ("L-A", "A", "DEP-A", "INR", 500000, DAY),
    ("L-B", "B", "DEP-B", "INR", 500000, DAY),
    ("L-V", "A", "DEP-V", "INR", 495000, DAY),
]
BANK = [
    ("B-B", "B", "DEP-B", "INR", 500000, DAY),
    ("B-V", "A", "DEP-V", "INR", 500000, DAY),
]


def demo():
    with sqlite3.connect(":memory:") as db:
        initialize(db)
        import_rows(db, "ledger", LEDGER)
        import_rows(db, "bank", BANK)
        reconcile(db)
        print("Bank ID | Ledger ID | Status | Variance (minor units)")
        for row in db.execute("SELECT * FROM outcomes ORDER BY bank_id"):
            print(*row, sep=" | ")
        print("Uncleared ledger IDs:", [r[0] for r in db.execute(
            """SELECT id FROM ledger EXCEPT SELECT ledger_id FROM outcomes WHERE status='cleared'""")])
        print("Rows added by repeat import:", import_rows(db, "bank", BANK))
        reconcile(db)
        findings = audit(db)
        print("SQL control violations:", {name: len(rows) for name, rows in findings.items()})
        if any(findings.values()):
            raise AssertionError(findings)


if __name__ == "__main__":
    demo()
