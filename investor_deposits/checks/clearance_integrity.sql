SELECT o.bank_id, o.ledger_id
FROM outcomes o LEFT JOIN bank b ON o.bank_id=b.id LEFT JOIN ledger l ON o.ledger_id=l.id
WHERE o.status='cleared' AND (
    b.id IS NULL OR l.id IS NULL OR b.account <> l.account OR b.reference <> l.reference
    OR b.currency <> l.currency OR b.amount <> l.amount OR o.variance IS NOT 0
    OR ABS(julianday(b.posted)-julianday(l.posted)) > 5
);
