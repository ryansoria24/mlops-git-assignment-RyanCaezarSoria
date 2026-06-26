# MAI201 Assignment 2 — Data Validation & Testing

Data validation with **Great Expectations** and unit testing with **pytest**, run
against a deliberately messy `customer_data.csv` (5,015 rows). No model training.

## Project structure

```
assignment2/
├── data/
│   └── customer_data.csv            # the messy dataset
├── src/
│   └── data_utils.py                # load_csv, clean_phone, validate_email
├── tests/
│   └── test_data_utils.py           # 33 pytest unit tests
├── run_gx_validation.py             # sets up GX, validates, builds data docs
├── gx/                              # Great Expectations project (config + suite)
│   └── expectations/customer_data_expectations.json
├── data_docs/                       # generated HTML data docs (open index.html)
├── screenshots/
│   ├── gx_validation_results.png
│   └── pytest_results.png
├── requirements.txt
├── assignment2_report.md            # the report to submit
└── README.md
```

## Setup (Windows — Git Bash or PowerShell)

> Tip: every command below assumes you are **inside the `assignment2` folder**.
> If your prompt shows a different path, `cd` into it first, e.g.
> `cd C:\Users\Ryan\assignment2`

1. **(Recommended) Create and activate a conda environment**
   ```bash
   conda create -n mai201-a2 python=3.11 -y
   conda activate mai201-a2
   ```

2. **Install the dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   This installs Great Expectations 0.18.19 (the version this project was built
   and tested with), pandas, and pytest.

## Running everything

**Run the pytest unit tests** (Part 4) — should report `33 passed`:
```bash
pytest -v
```

**Run the Great Expectations validation** (Parts 1–3) — creates the suite,
validates the data, prints a pass/fail summary, and builds the HTML data docs:
```bash
python run_gx_validation.py
```
After it runs, open the data documentation in your browser:
```
data_docs/index.html
```
(also written to `gx/uncommitted/data_docs/local_site/index.html`)

## Taking your own screenshots (for the report)

The `screenshots/` folder already contains valid renders of the real output, but
for an authentic submission you can recapture them on your own machine:

- **pytest:** run `pytest -v` and screenshot the terminal showing `33 passed`.
- **Great Expectations:** open `data_docs/index.html`, click into the validation
  result, and screenshot the results table.

Then replace the two files in `screenshots/`.

## What each expectation checks

| Column | Rule |
|--------|------|
| `customer_id` | unique **and** not null |
| `age` | between 0 and 120 |
| `email` | matches a valid email regex |
| `salary` | present in ≥ 95% of rows (`mostly=0.95`) |
| `country` | one of USA / Canada / UK / Australia |
| `signup_date` | parseable as a `YYYY-MM-DD` date |
| *(table)* | row count between 500 and 1000 |

All eight intentionally **fail** on this messy dataset — that is the point: the
validation stage is doing its job by catching the data quality problems.
