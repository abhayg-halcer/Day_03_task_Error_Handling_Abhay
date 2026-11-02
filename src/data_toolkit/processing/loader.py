"""CSV loading functionality."""

import csv
import logging
from pathlib import Path

from data_toolkit.exceptions import (
    DataToolkitError,
    FileAccessError,
    FileFormatError,
)
from data_toolkit.models.record import Record
from data_toolkit.processing.validator import validate_columns, validate_row

logger = logging.getLogger(__name__)


def load_csv(file_path: str | Path) -> list[Record]:
    """Load and validate sales records from a CSV file."""
    path = Path(file_path)

    if not path.exists():
        logger.error("CSV input file does not exist.")
        raise FileAccessError(f"CSV file not found: {path.name}")

    if not path.is_file():
        logger.error("CSV input path is not a regular file.")
        raise FileAccessError("The supplied CSV path is not a file.")

    records: list[Record] = []

    try:
        with path.open("r", encoding="utf-8-sig", newline="") as csv_file:
            reader = csv.DictReader(csv_file)

            validate_columns(reader.fieldnames)

            for row_number, row in enumerate(reader, start=2):
                if None in row:
                    raise FileFormatError(
                        f"Row {row_number}: too many values for the CSV columns."
                    )

                if any(value is None for value in row.values()):
                    raise FileFormatError(
                        f"Row {row_number}: missing CSV field value."
                    )

                normalized_row = {
                    key.strip().lower(): value
                    for key, value in row.items()
                    if key is not None
                }

                validate_row(normalized_row, row_number)

                records.append(
                    Record(
                        product=normalized_row["product"].strip(),
                        quantity=int(normalized_row["quantity"]),
                        price=float(normalized_row["price"]),
                    )
                )

    except DataToolkitError:
        raise
    except UnicodeDecodeError:
        logger.error("CSV input could not be decoded as UTF-8.")
        raise FileFormatError(
            "CSV file must use UTF-8 text encoding."
        ) from None
    except csv.Error:
        logger.error("CSV parsing failed.")
        raise FileFormatError(
            "CSV file contains malformed data."
        ) from None
    except PermissionError:
        logger.error("Permission denied while reading CSV input.")
        raise FileAccessError(
            "Permission denied while reading the CSV file."
        ) from None
    except OSError:
        logger.error("Operating system error while reading CSV input.")
        raise FileAccessError(
            "Could not read the CSV file due to a filesystem error."
        ) from None

    logger.info("Successfully loaded %d sales records.", len(records))
    return records
