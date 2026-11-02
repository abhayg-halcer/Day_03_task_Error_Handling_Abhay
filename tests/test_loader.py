"""Tests for CSV loading."""

from pathlib import Path

import pytest

from data_toolkit.exceptions import (
    DataValidationError,
    FileAccessError,
    SchemaValidationError,
)
from data_toolkit.processing.loader import load_csv


FIXTURE = Path(__file__).parent / "fixtures" / "sample_sales.csv"


def test_load_valid_csv() -> None:
    records = load_csv(FIXTURE)

    assert len(records) == 3
    assert records[0].product == "Laptop"
    assert records[0].total == 1000.0


def test_missing_file() -> None:
    with pytest.raises(FileAccessError, match="not found"):
        load_csv("missing_file.csv")


@pytest.mark.parametrize(
    ("content", "error"),
    [
        (
            """name,amount
Laptop,500
""",
            SchemaValidationError,
        ),
        (
            """product,quantity,price
Laptop,abc,500
""",
            DataValidationError,
        ),
        (
            """product,quantity,price
Laptop,2,-5
""",
            DataValidationError,
        ),
        (
            """product,quantity,price
Laptop,0,500
""",
            DataValidationError,
        ),
        (
            """product,quantity,price
,2,500
""",
            DataValidationError,
        ),
    ],
)
def test_invalid_csv(
    tmp_path: Path,
    content: str,
    error: type[Exception],
) -> None:
    csv_file = tmp_path / "invalid.csv"
    csv_file.write_text(content, encoding="utf-8")

    with pytest.raises(error):
        load_csv(csv_file)


def test_directory_path_is_rejected(tmp_path: Path) -> None:
    with pytest.raises(FileAccessError, match="not a file"):
        load_csv(tmp_path)


def test_csv_with_extra_value_is_rejected(tmp_path: Path) -> None:
    csv_file = tmp_path / "extra.csv"
    csv_file.write_text(
        "product,quantity,price\nLaptop,2,500,unexpected\n",
        encoding="utf-8",
    )

    from data_toolkit.exceptions import FileFormatError

    with pytest.raises(FileFormatError, match="too many values"):
        load_csv(csv_file)


def test_csv_with_missing_value_is_rejected(tmp_path: Path) -> None:
    csv_file = tmp_path / "missing_value.csv"
    csv_file.write_text(
        "product,quantity,price\nLaptop,2\n",
        encoding="utf-8",
    )

    from data_toolkit.exceptions import FileFormatError

    with pytest.raises(FileFormatError, match="missing CSV field"):
        load_csv(csv_file)


def test_invalid_utf8_file_is_rejected(tmp_path: Path) -> None:
    from data_toolkit.exceptions import FileFormatError

    csv_file = tmp_path / "invalid_encoding.csv"
    csv_file.write_bytes(b"product,quantity,price\nLaptop,\xff,500\n")

    with pytest.raises(FileFormatError, match="UTF-8"):
        load_csv(csv_file)


def test_csv_parser_error_is_handled(tmp_path: Path, monkeypatch) -> None:
    import csv

    from data_toolkit.exceptions import FileFormatError
    from data_toolkit.processing import loader

    csv_file = tmp_path / "parser_error.csv"
    csv_file.write_text(
        "product,quantity,price\nLaptop,2,500\n",
        encoding="utf-8",
    )

    def raise_csv_error(*args, **kwargs):
        raise csv.Error("simulated parser error")

    monkeypatch.setattr(loader.csv, "DictReader", raise_csv_error)

    with pytest.raises(FileFormatError, match="malformed data"):
        load_csv(csv_file)


def test_permission_error_is_handled(tmp_path: Path, monkeypatch) -> None:
    from data_toolkit.processing import loader

    csv_file = tmp_path / "permission.csv"
    csv_file.write_text("product,quantity,price\n", encoding="utf-8")

    def raise_permission_error(self, *args, **kwargs):
        raise PermissionError("simulated permission error")

    monkeypatch.setattr(Path, "open", raise_permission_error)

    with pytest.raises(FileAccessError, match="Permission denied"):
        loader.load_csv(csv_file)


def test_filesystem_error_is_handled(tmp_path: Path, monkeypatch) -> None:
    from data_toolkit.processing import loader

    csv_file = tmp_path / "filesystem.csv"
    csv_file.write_text("product,quantity,price\n", encoding="utf-8")

    def raise_os_error(self, *args, **kwargs):
        raise OSError("simulated filesystem error")

    monkeypatch.setattr(Path, "open", raise_os_error)

    with pytest.raises(FileAccessError, match="filesystem error"):
        loader.load_csv(csv_file)
