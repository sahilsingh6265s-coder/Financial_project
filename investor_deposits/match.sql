INSERT INTO outcomes (bank_id, ledger_id, status, variance)
WITH candidates AS (
    SELECT b.id AS bank_id, l.id AS ledger_id, b.amount - l.amount AS variance,
           COUNT(*) OVER (PARTITION BY b.id) AS bank_candidates,
           COUNT(*) OVER (PARTITION BY l.id) AS ledger_candidates
    FROM bank b JOIN ledger l
      ON b.account = l.account AND b.reference = l.reference AND b.currency = l.currency
     AND ABS(julianday(b.posted) - julianday(l.posted)) <= 5
), unique_links AS (
    SELECT * FROM candidates WHERE bank_candidates = 1 AND ledger_candidates = 1
)
SELECT b.id, u.ledger_id,
       CASE WHEN u.variance = 0 THEN 'cleared'
            WHEN u.ledger_id IS NOT NULL THEN 'amount_mismatch'
            WHEN EXISTS (SELECT 1 FROM candidates c WHERE c.bank_id = b.id) THEN 'ambiguous'
            ELSE 'unmatched' END,
       u.variance
FROM bank b LEFT JOIN unique_links u ON b.id = u.bank_id;
