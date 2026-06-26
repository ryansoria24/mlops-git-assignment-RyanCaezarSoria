"""
data_utils.py
-------------
Small, well-defined data utility functions used by the customer-data pipeline.

These three functions are the units under test in tests/test_data_utils.py:
    - load_csv(filepath)      -> load a CSV into a pandas DataFrame (with error handling)
    - clean_phone(phone)      -> normalise messy phone strings to one consistent format
    - validate_email(email)   -> return True/False for whether an email is well-formed

Keeping these as tiny, pure functions is what makes them easy to unit test:
each one has predictable inputs and outputs and no hidden side effects.
"""

import os
import re

import pandas as pd


# A single compiled regex reused by validate_email().
# Breakdown:
#   ^[A-Za-z0-9._%+-]+   one or more "local part" chars before the @
#   @                    exactly one @ sign
#   [A-Za-z0-9.-]+       the domain (letters/digits/dots/hyphens)
#   \.[A-Za-z]{2,}$      a dot followed by a 2+ letter top-level domain, at the end
_EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")


def load_csv(filepath):
    """Load a CSV file into a pandas DataFrame.

    Parameters
    ----------
    filepath : str
        Path to the CSV file.

    Returns
    -------
    pandas.DataFrame
        The loaded data.

    Raises
    ------
    FileNotFoundError
        If the file does not exist.
    ValueError
        If the file exists but contains no data (empty file).
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")

    try:
        df = pd.read_csv(filepath)
    except pd.errors.EmptyDataError as exc:
        # pandas raises EmptyDataError on a 0-byte / header-less file.
        # We re-raise as a ValueError so callers get one predictable error type.
        raise ValueError(f"No data found in file: {filepath}") from exc

    if df.empty:
        raise ValueError(f"No data found in file: {filepath}")

    return df


def clean_phone(phone):
    """Normalise a phone number to the consistent format '(XXX) XXX-XXXX'.

    The raw data contains many formats, e.g. '3637929158', '423.366.4508',
    '719-808-4765', '(318) 414-9221', '733 274 6639'. This function strips
    everything except digits and then reformats valid 10-digit US numbers.

    Parameters
    ----------
    phone : str | int | float | None
        The raw phone value (may be messy or missing).

    Returns
    -------
    str | None
        A string like '(363) 792-9158' for a valid number, or None if the
        input is missing or cannot be interpreted as a 10-digit number.
    """
    # Treat None / NaN / empty as "no usable number".
    if phone is None or (isinstance(phone, float) and pd.isna(phone)):
        return None

    digits = re.sub(r"\D", "", str(phone))  # keep digits only

    # A US number with a leading country code '1' -> drop it.
    if len(digits) == 11 and digits.startswith("1"):
        digits = digits[1:]

    # Only a clean 10-digit number can be normalised.
    if len(digits) != 10:
        return None

    return f"({digits[0:3]}) {digits[3:6]}-{digits[6:10]}"


def validate_email(email):
    """Return True if `email` is a well-formed email address, else False.

    Parameters
    ----------
    email : str | None
        The email value to check.

    Returns
    -------
    bool
        True for a valid format (e.g. 'user@example.com'),
        False for missing or malformed values (e.g. '@domain.com',
        'user@@domain.com', 'no-dot@com').
    """
    if email is None or not isinstance(email, str):
        return False

    return bool(_EMAIL_RE.match(email.strip()))
