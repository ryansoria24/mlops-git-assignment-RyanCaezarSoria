"""
run_gx_validation.py
--------------------
Sets up Great Expectations, creates the `customer_data_expectations` suite,
validates the messy CSV, and builds the HTML data docs.

What this script does, step by step:
  1. Initialise a file-based GX project in ./gx  (Part 1)
  2. Register a pandas datasource pointing at ./data               (Part 1)
  3. Create the expectation suite + 8 expectations                (Part 2)
  4. Run the suite against customer_data.csv via a checkpoint      (Part 3)
  5. Build the Data Docs HTML and print a pass/fail summary        (Part 3)

Run from the project root:
    python run_gx_validation.py
"""

import great_expectations as gx

CSV_NAME = "customer_data.csv"
SUITE_NAME = "customer_data_expectations"

VALID_EMAIL_REGEX = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
ALLOWED_COUNTRIES = ["USA", "Canada", "UK", "Australia"]


def main():
    # ---- 1. Initialise / load the file-based GX context (Part 1) ----------
    # project_root_dir="." creates a ./gx folder the first time
    # it runs (this is the programmatic equivalent of `great_expectations init`).
    context = gx.get_context(project_root_dir=".")

    # ---- 2. Datasource pointing at the ./data folder (Part 1) -------------
    datasource_name = "customer_data_source"
    if datasource_name in context.datasources:
        datasource = context.datasources[datasource_name]
    else:
        datasource = context.sources.add_pandas_filesystem(
            name=datasource_name, base_directory="./data"
        )

    asset_name = "customer_data_asset"
    try:
        asset = datasource.get_asset(asset_name)
    except LookupError:
        asset = datasource.add_csv_asset(
            name=asset_name, batching_regex=r"customer_data\.csv"
        )

    batch_request = asset.build_batch_request()

    # ---- 3. Expectation suite + the 8 required expectations (Part 2) ------
    context.add_or_update_expectation_suite(SUITE_NAME)
    validator = context.get_validator(
        batch_request=batch_request, expectation_suite_name=SUITE_NAME
    )

    # customer_id: unique and not null
    validator.expect_column_values_to_be_unique("customer_id")
    validator.expect_column_values_to_not_be_null("customer_id")
    # age: between 0 and 120
    validator.expect_column_values_to_be_between("age", min_value=0, max_value=120)
    # email: valid format via regex
    validator.expect_column_values_to_match_regex("email", VALID_EMAIL_REGEX)
    # salary: present in at least 95% of rows (mostly parameter)
    validator.expect_column_values_to_not_be_null("salary", mostly=0.95)
    # country: one of the allowed values
    validator.expect_column_values_to_be_in_set("country", ALLOWED_COUNTRIES)
    # signup_date: parseable as a YYYY-MM-DD date (datetime-type check for a CSV)
    validator.expect_column_values_to_match_strftime_format(
        "signup_date", "%Y-%m-%d"
    )
    # table row count: between 500 and 1000
    validator.expect_table_row_count_to_be_between(min_value=500, max_value=1000)

    validator.save_expectation_suite(discard_failed_expectations=False)

    # ---- 4. Validate via a checkpoint (Part 3) ---------------------------
    checkpoint = context.add_or_update_checkpoint(
        name="customer_data_checkpoint",
        validations=[
            {
                "batch_request": batch_request,
                "expectation_suite_name": SUITE_NAME,
            }
        ],
    )
    result = checkpoint.run()

    # ---- 5. Build Data Docs HTML + print a summary (Part 3) --------------
    context.build_data_docs()

    print("\n" + "=" * 70)
    print("VALIDATION SUMMARY")
    print("=" * 70)
    for vr in result.list_validation_results():
        overall = "PASS" if vr["success"] else "FAIL"
        print(f"Overall suite result: {overall}")
        for r in vr["results"]:
            exp = r["expectation_config"]["expectation_type"]
            col = r["expectation_config"]["kwargs"].get("column", "(table)")
            status = "PASS" if r["success"] else "FAIL"
            unexpected = r["result"].get("unexpected_count")
            extra = f"  (unexpected={unexpected})" if unexpected is not None else ""
            print(f"  [{status}] {col:<12} {exp}{extra}")
    print("=" * 70)
    print("Data Docs written to: gx/uncommitted/data_docs/"
          "local_site/index.html")


if __name__ == "__main__":
    main()
