# A description match concealed a cash discrepancy

**Source:** Original simulated FinOps export, bank entry B4071 and ledger entry L3071. The original export recorded 48,196.7455 and 47,719.55 respectively. Its description similarity was 100. The entries fell inside the configured 2% candidate tolerance, and the report treated the pair as matched.

**Impact:** An analyst counting uncleared cash could overlook a ₹477.20 difference after rounding to paise.

**Acceptance criterion:** A reference may link a bank record to a ledger record. Cash clears only when the monetary difference is zero and the link is unique. A nonzero difference stays open with a signed variance.

**Retest:** The test named test_historical_variance uses the original amounts rounded to paise and assigns synthetic account and reference identifiers for the investor scenario. Expected result: B4071 links to L3071 with status amount_mismatch and variance +47,720 paise. Run the test command in the README to reproduce it. The account and reference are fixture values.
