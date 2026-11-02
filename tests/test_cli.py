"""Tests for the command-line interface."""

from pathlib import Path

from data_toolkit import cli
from data_toolkit.exceptions import FileAccessError


def test_cli_success(monkeypatch, tmp_path: Path, capsys) -> None:
    sample_file = Path(__file__).parent / "fixtures" / "sample_sales.csv"
    monkeypatch.setattr("sys.argv", ["data-toolkit", str(sample_file)])
    monkeypatch.setattr(cli, "DEFAULT_LOG_FILE", tmp_path / "app.log")

    result = cli.main()

    output = capsys.readouterr().out
    assert result == 0
    assert "SALES SUMMARY" in output
    assert "Total Records: 3" in output
    assert "Total Sales: 1235.0" in output


def test_cli_handles_processing_error(
    monkeypatch, tmp_path: Path, capsys
) -> None:
    monkeypatch.setattr("sys.argv", ["data-toolkit", "missing.csv"])
    monkeypatch.setattr(cli, "DEFAULT_LOG_FILE", tmp_path / "app.log")

    def raise_file_error(file_path):
        raise FileAccessError("CSV file not found: missing.csv")

    monkeypatch.setattr(cli, "load_csv", raise_file_error)

    result = cli.main()

    output = capsys.readouterr().out
    assert result == 1
    assert "Error: CSV file not found" in output
