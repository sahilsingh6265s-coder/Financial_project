import sqlite3
import unittest
from investor_deposits.workflow import BANK, LEDGER, DAY, audit, import_rows, initialize, reconcile


class DepositAcceptance(unittest.TestCase):
    def setUp(self):
        self.db = sqlite3.connect(":memory:")
        self.addCleanup(self.db.close)
        initialize(self.db)
        import_rows(self.db, "ledger", LEDGER)
        import_rows(self.db, "bank", BANK)
        reconcile(self.db)

    def outcomes(self):
        return self.db.execute("SELECT * FROM outcomes ORDER BY bank_id").fetchall()

    def test_equal_payments_and_variance(self):
        expected = [('B-B','L-B','cleared',0), ('B-V','L-V','amount_mismatch',5000)]
        self.assertEqual(self.outcomes(), expected)
        self.assertFalse(any(audit(self.db).values()))
        self.db.execute("DELETE FROM ledger")
        import_rows(self.db, "ledger", reversed(LEDGER))
        self.db.execute("DELETE FROM bank")
        import_rows(self.db, "bank", reversed(BANK))
        reconcile(self.db)
        self.assertEqual(self.outcomes(), expected)

    def test_repeat_import(self):
        before = self.outcomes()
        self.assertEqual(import_rows(self.db, "bank", BANK), 0)
        reconcile(self.db)
        self.assertEqual(self.outcomes(), before)

    def test_conflicting_import_rolls_back_entire_batch(self):
        with self.assertRaises(ValueError):
            import_rows(self.db, "bank", [('new', *BANK[0][1:]), ('B-B','B','DEP-B','INR',1,DAY)])
        self.assertEqual(self.db.execute("SELECT COUNT(*) FROM bank").fetchone()[0], 2)

    def test_contested_ledger(self):
        import_rows(self.db, "bank", [('again', *BANK[0][1:])])
        reconcile(self.db)
        self.assertEqual(self.db.execute("SELECT COUNT(*) FROM outcomes WHERE status='ambiguous'").fetchone()[0], 2)

    def test_historical_variance(self):
        import_rows(self.db, 'bank', [('B4071','A','R4071','INR',4819675,DAY)])
        import_rows(self.db, 'ledger', [('L3071','A','R4071','INR',4771955,DAY)])
        reconcile(self.db)
        self.assertIn(('B4071','L3071','amount_mismatch',47720), self.outcomes())

    def test_wrong_identity_or_date(self):
        for account, ref, currency, day in [('A','DEP-B','INR',DAY),('B','other','INR',DAY),
                                            ('B','DEP-B','USD',DAY),('B','DEP-B','INR','2026-11-30')]:
            with self.subTest(account=account, ref=ref, currency=currency, day=day):
                self.db.execute("DELETE FROM bank")
                import_rows(self.db, 'bank', [('X', account, ref, currency, 500000, day)])
                reconcile(self.db)
                self.assertEqual(self.outcomes(), [('X',None,'unmatched',None)])

    def test_duplicate_clearance_control(self):
        self.db.execute("UPDATE outcomes SET ledger_id='L-B', status='cleared' WHERE bank_id='B-V'")
        self.assertIn(('ledger','L-B',2), audit(self.db)['one_to_one'])

    def test_invalid_clearance_control(self):
        self.db.execute("UPDATE outcomes SET status='cleared', variance=0 WHERE bank_id='B-V'")
        self.assertEqual(audit(self.db)['clearance_integrity'], [('B-V','L-V')])

    def test_missing_outcome_control(self):
        self.db.execute("DELETE FROM outcomes WHERE bank_id='B-B'")
        self.assertEqual(audit(self.db)['coverage'], [('B-B',)])
