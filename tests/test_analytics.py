"""Tests for sales analytics."""

from data_toolkit.analytics.summary import generate_summary
from data_toolkit.models.record import Record


def test_generate_summary(sample_records: list[Record]) -> None:
    summary = generate_summary(sample_records)

    assert summary["total_records"] == 3
    assert summary["total_quantity"] == 10
    assert summary["total_sales"] == 1235.0
    assert summary["average_sale"] == 411.67
    assert summary["best_selling_product"] == "Mouse"


def test_empty_summary() -> None:
    summary = generate_summary([])

    assert summary["total_records"] == 0
    assert summary["total_sales"] == 0.0
    assert summary["best_selling_product"] == "N/A"
