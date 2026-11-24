SELECT 'bank', bank_id, COUNT(*) FROM outcomes WHERE status='cleared'
GROUP BY bank_id HAVING COUNT(*) > 1
UNION ALL
SELECT 'ledger', ledger_id, COUNT(*) FROM outcomes WHERE status='cleared'
GROUP BY ledger_id HAVING COUNT(*) > 1;
