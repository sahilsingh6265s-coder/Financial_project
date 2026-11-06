# Cross-Border Finance Operations

A step-by-step finance operations analysis for a fictional, cross-border medical-device manufacturer, MediRobo Diagnostics. The project combines public supply-chain order and shipping data with a synthetic finance layer to demonstrate accounts receivable (AR), accounts payable (AP), payment-risk analysis, bank reconciliation, internal controls, and employee reimbursements.

> **Important:** This is an educational portfolio project, not a production finance system. Finance transactions and payment behavior are simulated and do not represent Morphle Labs or any real company. Market relabeling is illustrative only.

## Project at a glance

The notebook, [FinOps_Project.ipynb`](./Morphle_FinOps_Project.ipynb), runs three connected workflows:

1. **Supply chain and AR:** clean and summarize order and delivery data, simulate customer payment terms, and produce regional AR aging and delivery analyses.
2. **Customer payment risk:** test whether overdue payments vary across customer segments and regions, then evaluate a logistic-regression classifier.
3. **Finance operations controls:** generate example vendor, bank, ledger, and reimbursement records; analyze AP and currency exposure; reconcile transactions; and flag control exceptions.

The final notebook section exports the key reports as CSV files.

## Repository contents

| Path | Description |
| --- | --- |
| `Morphle_FinOps_Project.ipynb` | Main notebook containing the analysis and workflow. |
| `DataCoSupplyChainDataset.csv` | Required public supply-chain source data (approximately 180,000 rows). |
| `ar_aging_report.csv`, `vendor_invoices.csv`, etc. | Example finance reports supplied with the project. The notebook generates its own reports under `exports/`. |
| `exports/` | Output directory created by the final notebook cell. |

## Requirements

- Python 3.10 or newer
- Jupyter Notebook or JupyterLab
- The notebook packages listed below
- The source file `DataCoSupplyChainDataset.csv` in the project root, next to the notebook

Install the dependencies in your Python environment:

```bash
python -m pip install pandas numpy Faker scipy scikit-learn rapidfuzz jupyter
```

## Run the notebook

1. **Get the project files.** Clone or download this repository, and ensure `DataCoSupplyChainDataset.csv` is in the same folder as the notebook.
2. **Open a terminal in the project folder.** This matters because the notebook loads the dataset using a relative path.
3. **Install dependencies** using the command above.
4. **Start Jupyter:**

   ```bash
   jupyter notebook
   ```

   Alternatively, use `jupyter lab` if you prefer JupyterLab.
5. **Open `Morphle_FinOps_Project.ipynb`.** Select the Python environment where you installed the dependencies.
6. **Run every cell from top to bottom.** The analyses build on dataframes and tables created earlier in the notebook; running sections out of order may fail.
7. **Review results** in each section and find the generated CSV reports in the new `exports/` directory.

The notebook uses fixed NumPy, Python `random`, and Faker seeds to make its synthetic examples more reproducible. Model results can still depend on library versions and execution environment.

## Workflows, step by step

### 1. Supply chain and accounts receivable

1. Load the DataCo supply-chain CSV and parse order and shipping dates.
2. Map source markets into illustrative business regions: `USCA` to `USA`, `Pacific Asia` to `India & APAC`, and `Africa` to `Middle East & Africa`. These names are a storytelling convention, not a correction to the source data.
3. Create distinct order, customer, and product tables, then load the analysis tables into an in-memory SQLite database.
4. Add a **simulated AR layer** to the real orders: regional payment terms, due dates, and seeded sample payment behavior. The source dataset does not contain invoice payment history.
5. Use SQL to summarize AR aging by region and to compare late deliveries by region and shipping mode, alongside regional profitability/landed-cost analyses.

### 2. Customer payment risk

1. Build a customer/order analysis dataset from the prepared orders and the simulated AR outcomes.
2. Use statistical tests to examine the relationship between overdue status and customer region, customer segment, and order value.
3. Fit a logistic-regression classifier using a train/test split.
4. Review the ROC-AUC and classification report to understand the model's test-set performance.

The risk labels are generated for demonstration; model metrics are not evidence of real customer default risk.

### 3. AP, reconciliation, controls, and reimbursements

1. Generate sample vendors and multi-currency vendor invoices, then summarize payables by status and currency.
2. Apply illustrative exchange rates to estimate open payable exposure in INR.
3. Generate sample bank statement and internal-ledger transactions. Match candidates by amount and date window, then rank candidates by description similarity using RapidFuzz.
4. Separate matched entries from unmatched bank and ledger entries.
5. Apply the sample internal-control rules to flag transactions requiring review and stale unreconciled entries.
6. Generate employee reimbursement claims and evaluate them against the configured checks, such as missing receipts and review timing.

These records and control outcomes are synthetic examples created in the notebook; they are not loaded from the similarly named sample CSVs in the project root.

## Generated reports

When the final export cell completes, `exports/` contains:

| File | Contents |
| --- | --- |
| `ar_aging_report.csv` | Open AR summarized by region and aging bucket. |
| `vendor_invoices.csv` | Simulated vendor invoices with amounts, currencies, due dates, and payment status. |
| `reimbursement_claims.csv` | Simulated employee claims and processing/control status. |
| `reconciliation_matches.csv` | Bank transactions and their proposed ledger matches, including match quality. |
| `reconciliation_unmatched_bank.csv` | Bank transactions without a ledger match. |
| `internal_controls.csv` | The sample control rules and their thresholds. |

The notebook also displays additional analysis tables and metrics interactively; not every displayed intermediate result is exported.

## Data sources and interpretation

The supply-chain portion uses the DataCo dataset for order, product, customer, and shipping information. The notebook layers generated finance assumptions on top of those orders because the public dataset does not provide AR payment histories, vendor invoices, bank statements, or employee reimbursements. Regional payment terms, simulated payment behavior, foreign-exchange rates, vendor records, bank/ledger transactions, and reimbursement claims should all be treated as illustrative assumptions.

The market mapping does not make the DataCo dataset representative of Morphle Labs' real customers or geographic footprint. No company financial records are used or implied.
