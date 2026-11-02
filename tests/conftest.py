"""Shared pytest fixtures."""

import pytest

from data_toolkit.models.record import Record


@pytest.fixture
def sample_records() -> list[Record]:
    """Provide sample sales records."""
    return [
        Record("Laptop", 2, 500.0),
        Record("Mouse", 5, 20.0),
        Record("Keyboard", 3, 45.0),
    ]
