# Cross-Border Finance Operations

A finance operations analysis project modeled on a fictional medical-device manufacturer, MediRobo Diagnostics. The notebook combines supply-chain order data with a synthetic finance layer to explore accounts receivable, customer payment risk, bank reconciliation, internal controls, and employee reimbursements.

## Project contents

- `Morphle_FinOps_Project.ipynb` — analysis, modeling, reconciliation, and CSV export workflow.
- `DataCoSupplyChainDataset.csv` — source supply-chain dataset required by the notebook.
- Finance CSV files in the project root — sample reports and data for accounts receivable, vendor invoices, reimbursements, reconciliation, and internal controls.
- `exports/` — generated CSV reports created when the notebook finishes.

## Requirements

- Python 3.10 or newer
- Jupyter Notebook or JupyterLab
- `pandas`, `numpy`, `Faker`, `scipy`, `scikit-learn`, and `rapidfuzz`

Install the Python packages with:

```bash
python -m pip install pandas numpy Faker scipy scikit-learn rapidfuzz jupyter
```

## Run the project

1. Place `DataCoSupplyChainDataset.csv` in the same folder as the notebook.
2. Start Jupyter from the project folder:

   ```bash
   jupyter notebook
   ```

3. Open `Morphle_FinOps_Project.ipynb` and run all cells from top to bottom.

The notebook reads the source CSV from the project folder and creates an `exports/` directory containing the AR aging report, vendor invoices, reimbursement claims, reconciliation results, and internal controls.

## Data and interpretation

The order and shipping data comes from the DataCo supply-chain dataset. Payment behavior, vendor invoices, bank activity, employee reimbursement claims, and control rules are synthetic additions used to demonstrate finance operations workflows. The notebook also maps some source market names to illustrative business regions; these labels are for analysis and storytelling, not a claim about the source dataset's actual geography.
