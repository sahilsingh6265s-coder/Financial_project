SELECT b.id FROM bank b LEFT JOIN outcomes o ON o.bank_id=b.id
GROUP BY b.id HAVING COUNT(o.bank_id) <> 1 OR
    SUM(CASE WHEN o.status IN ('cleared','amount_mismatch','ambiguous','unmatched') THEN 1 ELSE 0 END) <> 1
UNION ALL
SELECT o.bank_id FROM outcomes o LEFT JOIN bank b ON b.id=o.bank_id WHERE b.id IS NULL;
