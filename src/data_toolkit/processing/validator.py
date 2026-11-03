"""Validation functions for CSV sales data."""

from collections.abc import Mapping

from data_toolkit.config.settings import REQUIRED_COLUMNS
from data_toolkit.exceptions import DataValidationError, SchemaValidationError


def validate_columns(columns: list[str] | None) -> None:
    """Validate required columns and reject duplicate normalized headers."""
    if not columns:
        raise SchemaValidationError("CSV file is empty or has no header.")

    normalized_columns = [column.strip().lower() for column in columns]

    if len(normalized_columns) != len(set(normalized_columns)):
        seen: set[str] = set()
        duplicates: set[str] = set()

        for column in normalized_columns:
            if column in seen:
                duplicates.add(column)
            seen.add(column)

        duplicate_names = ", ".join(sorted(duplicates))
        raise SchemaValidationError(
            f"CSV contains duplicate column(s) after normalization: "
            f"{duplicate_names}."
        )

    normalized = set(normalized_columns)
    missing = set(REQUIRED_COLUMNS) - normalized

    if missing:
        missing_names = ", ".join(sorted(missing))
        raise SchemaValidationError(
            f"CSV is missing required column(s): {missing_names}."
        )


def validate_row(row: Mapping[str, str | None], row_number: int) -> None:
    """Validate one CSV row."""
    product = (row.get("product") or "").strip()
    quantity = (row.get("quantity") or "").strip()
    price = (row.get("price") or "").strip()

    if not product:
        raise DataValidationError(
            f"Row {row_number}: product name cannot be empty."
        )

    try:
        quantity_value = int(quantity)
    except ValueError:
        raise DataValidationError(
            f"Row {row_number}: quantity must be a whole number."
        ) from None

    if quantity_value <= 0:
        raise DataValidationError(
            f"Row {row_number}: quantity must be greater than zero."
        )

    try:
        price_value = float(price)
    except ValueError:
        raise DataValidationError(
            f"Row {row_number}: price must be a number."
        ) from None

    if price_value < 0:
        raise DataValidationError(
            f"Row {row_number}: price cannot be negative."
        )

    if price_value != price_value or price_value in (float("inf"), float("-inf")):
        raise DataValidationError(
            f"Row {row_number}: price must be a finite number."
        )
