"""Tests for CSV validation."""

import pytest

from data_toolkit.exceptions import (
    DataValidationError,
    SchemaValidationError,
)
from data_toolkit.processing.validator import validate_columns, validate_row


def test_valid_columns() -> None:
    validate_columns(["product", "quantity", "price"])


def test_missing_columns() -> None:
    with pytest.raises(SchemaValidationError):
        validate_columns(["product", "price"])


@pytest.mark.parametrize(
    "row",
    [
        {"product": "", "quantity": "2", "price": "10"},
        {"product": "Laptop", "quantity": "abc", "price": "10"},
        {"product": "Laptop", "quantity": "2", "price": "-10"},
        {"product": "Laptop", "quantity": "0", "price": "10"},
        {"product": "Laptop", "quantity": "2", "price": "nan"},
    ],
)
def test_invalid_rows(row: dict[str, str]) -> None:
    with pytest.raises(DataValidationError):
        validate_row(row, 2)
