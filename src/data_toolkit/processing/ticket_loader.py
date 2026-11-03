"""Reliable CSV loading for the customer support ticket pipeline."""

import csv
import logging
from pathlib import Path
from typing import Any

from data_toolkit.exceptions import (
    FileAccessError,
    FileFormatError,
    SchemaValidationError,
)

logger = logging.getLogger(__name__)

TICKET_COLUMNS = (
    "ticket_id",
    "customer_id",
    "category",
    "priority",
    "status",
    "created_at",
    "resolution_time_hours",
    "customer_rating",
    "description",
)


def load_tickets(file_path: str | Path) -> list[dict[str, Any]]:
    """Load ticket rows after validating and normalizing CSV headers."""
    path = Path(file_path)

    try:
        with path.open("r", newline="", encoding="utf-8-sig") as csv_file:
            reader = csv.DictReader(csv_file)

            if not reader.fieldnames:
                raise SchemaValidationError(
                    "CSV file is empty or has no header."
                )

            normalized = [
                header.strip().casefold()
                for header in reader.fieldnames
                if header is not None
            ]

            if len(normalized) != len(reader.fieldnames):
                raise SchemaValidationError("CSV contains an invalid header.")

            if len(normalized) != len(set(normalized)):
                seen: set[str] = set()
                duplicates: set[str] = set()
                for header in normalized:
                    if header in seen:
                        duplicates.add(header)
                    seen.add(header)
                names = ", ".join(sorted(duplicates))
                raise SchemaValidationError(
                    f"CSV contains duplicate column(s) after normalization: {names}."
                )

            missing = set(TICKET_COLUMNS) - set(normalized)
            if missing:
                names = ", ".join(sorted(missing))
                raise SchemaValidationError(
                    f"CSV is missing required column(s): {names}."
                )

            reader.fieldnames = normalized
            records: list[dict[str, Any]] = []

            for row_number, row in enumerate(reader, start=2):
                if None in row:
                    raise FileFormatError(
                        f"Row {row_number} contains more values than the header."
                    )
                records.append({
                    key: value if value is not None else ""
                    for key, value in row.items()
                })

            logger.info("Loaded %d ticket rows from %s", len(records), path)
            return records

    except (FileAccessError, FileFormatError, SchemaValidationError):
        raise
    except FileNotFoundError as error:
        raise FileAccessError(f"CSV file not found: {path}") from error
    except PermissionError as error:
        raise FileAccessError(f"Permission denied reading: {path}") from error
    except UnicodeDecodeError as error:
        raise FileFormatError(f"CSV file is not valid UTF-8: {path}") from error
    except csv.Error as error:
        raise FileFormatError(f"Malformed CSV file: {path}: {error}") from error
    except OSError as error:
        raise FileAccessError(f"Unable to read CSV file: {path}: {error}") from error
