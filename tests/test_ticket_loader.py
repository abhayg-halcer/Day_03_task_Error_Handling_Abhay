"""Tests for robust ticket CSV loading."""

import pytest

from data_toolkit.exceptions import (
    FileAccessError,
    FileFormatError,
    SchemaValidationError,
)
from data_toolkit.processing.ticket_loader import load_tickets

HEADER = (
    "ticket_id,customer_id,category,priority,status,created_at,"
    "resolution_time_hours,customer_rating,description"
)

VALID_ROW = (
    "TKT001,C001,Billing,Low,Open,2026-10-01T10:00:00,,,Test ticket"
)


def test_load_ticket_dataset() -> None:
    rows = load_tickets("data/tickets.csv")
    assert len(rows) == 40
    assert rows[0]["ticket_id"] == "TKT001"


@pytest.mark.parametrize(
    "header",
    [
        HEADER + ",ticket_id",
        HEADER + ",TICKET_ID",
        HEADER + ", TICKET_ID ",
    ],
)
def test_reject_duplicate_normalized_headers(
    tmp_path,
    header: str,
) -> None:
    path = tmp_path / "duplicate.csv"
    path.write_text(header + "\n" + VALID_ROW + ",duplicate\n", encoding="utf-8")

    with pytest.raises(SchemaValidationError, match="duplicate"):
        load_tickets(path)


def test_reject_missing_required_header(tmp_path) -> None:
    path = tmp_path / "missing.csv"
    path.write_text("ticket_id,priority\nTKT001,Low\n", encoding="utf-8")

    with pytest.raises(SchemaValidationError, match="missing"):
        load_tickets(path)


def test_missing_cells_are_normalized_to_empty_strings(tmp_path) -> None:
    path = tmp_path / "short_row.csv"
    path.write_text(HEADER + "\nTKT001,C001\n", encoding="utf-8")

    rows = load_tickets(path)
    assert rows[0]["category"] == ""
    assert rows[0]["description"] == ""


def test_extra_csv_values_are_rejected(tmp_path) -> None:
    path = tmp_path / "extra.csv"
    path.write_text(HEADER + "\n" + VALID_ROW + ",extra\n", encoding="utf-8")

    with pytest.raises(FileFormatError, match="more values"):
        load_tickets(path)


def test_missing_file_raises_file_access_error(tmp_path) -> None:
    with pytest.raises(FileAccessError, match="not found"):
        load_tickets(tmp_path / "does_not_exist.csv")
