"""
test_data_utils.py
------------------
pytest unit tests for the three utility functions in src/data_utils.py.

Run from the project root with:
    pytest -v

Test coverage (as required by Assignment 2, Part 4):
    load_csv        -> file not found, empty file, successful loading
    clean_phone     -> several valid formats + invalid / missing inputs
    validate_email  -> valid emails, invalid emails, and edge cases
"""

import os
import sys

import pandas as pd
import pytest

# Make src/ importable no matter where pytest is launched from.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from data_utils import load_csv, clean_phone, validate_email  # noqa: E402


# ---------------------------------------------------------------------------
# load_csv
# ---------------------------------------------------------------------------
class TestLoadCsv:
    def test_file_not_found(self):
        """A non-existent path should raise FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            load_csv("this/path/does/not/exist.csv")

    def test_empty_file(self, tmp_path):
        """A completely empty file should raise ValueError."""
        empty = tmp_path / "empty.csv"
        empty.write_text("")  # 0 bytes
        with pytest.raises(ValueError):
            load_csv(str(empty))

    def test_successful_load(self, tmp_path):
        """A well-formed CSV should load into a DataFrame with the right shape."""
        good = tmp_path / "good.csv"
        good.write_text("id,name\n1,Alice\n2,Bob\n")
        df = load_csv(str(good))
        assert isinstance(df, pd.DataFrame)
        assert df.shape == (2, 2)
        assert list(df.columns) == ["id", "name"]


# ---------------------------------------------------------------------------
# clean_phone
# ---------------------------------------------------------------------------
class TestCleanPhone:
    @pytest.mark.parametrize(
        "raw,expected",
        [
            ("3637929158", "(363) 792-9158"),       # plain digits
            ("423.366.4508", "(423) 366-4508"),     # dotted
            ("719-808-4765", "(719) 808-4765"),      # dashed
            ("(318) 414-9221", "(318) 414-9221"),    # already formatted
            ("733 274 6639", "(733) 274-6639"),      # space separated
            ("1-202-555-0123", "(202) 555-0123"),    # leading country code 1
        ],
    )
    def test_valid_formats_normalised(self, raw, expected):
        """All valid 10-digit inputs map to the single '(XXX) XXX-XXXX' format."""
        assert clean_phone(raw) == expected

    @pytest.mark.parametrize(
        "bad",
        [
            "-8437",        # too few digits
            "abc",          # no digits at all
            "123",          # too short
            "123456789012", # too long (not 11-with-leading-1)
            "",             # empty string
            None,           # missing
        ],
    )
    def test_invalid_inputs_return_none(self, bad):
        """Anything that is not a clean 10-digit number returns None."""
        assert clean_phone(bad) is None

    def test_consistent_output_across_formats(self):
        """The same number in different formats yields identical output."""
        results = {
            clean_phone("3637929158"),
            clean_phone("363-792-9158"),
            clean_phone("363.792.9158"),
            clean_phone("(363) 792-9158"),
        }
        assert results == {"(363) 792-9158"}


# ---------------------------------------------------------------------------
# validate_email
# ---------------------------------------------------------------------------
class TestValidateEmail:
    @pytest.mark.parametrize(
        "email",
        [
            "user@example.com",
            "first.last@example.com",
            "user+tag@example.co.uk",
            "a.b-c@sub.domain.io",
        ],
    )
    def test_valid_emails(self, email):
        assert validate_email(email) is True

    @pytest.mark.parametrize(
        "email",
        [
            "@domain.com",            # no local part
            "user@@domain.com",       # double @
            "no-dot@com",             # no dot in domain
            "user@",                  # nothing after @
            "missingatsign.com",      # no @ at all
            "user@.com",              # domain starts with a dot
            "user name@domain.com",   # space in local part
            "user@domain.",           # trailing dot, no TLD
        ],
    )
    def test_invalid_emails(self, email):
        assert validate_email(email) is False

    @pytest.mark.parametrize("edge", [None, "", "   ", 12345, ["user@example.com"]])
    def test_edge_cases(self, edge):
        """None, empty/whitespace strings, and non-string types are all invalid."""
        assert validate_email(edge) is False
