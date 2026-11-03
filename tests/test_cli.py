"""Tests for the support ticket command-line interface."""

from pathlib import Path

from data_toolkit import cli
from data_toolkit.exceptions import FileAccessError


def test_cli_success(monkeypatch, tmp_path: Path, capsys) -> None:
    sample_file = Path("data/tickets.csv")
    output_dir = tmp_path / "reports"

    monkeypatch.setattr(
        "sys.argv",
        [
            "data-toolkit",
            str(sample_file),
            "--output-dir",
            str(output_dir),
        ],
    )
    monkeypatch.setattr(cli, "DEFAULT_LOG_FILE", tmp_path / "app.log")

    result = cli.main()
    output = capsys.readouterr().out

    assert result == 0
    assert "SUPPORT TICKET PIPELINE" in output
    assert "Raw records loaded: 40" in output
    assert "Valid tickets: 32" in output
    assert "Quality issues found: 9" in output
    assert "Average resolution time: 7.75 hours" in output

    assert (output_dir / "data_quality_report.csv").exists()
    assert (output_dir / "summary_metrics.csv").exists()
    assert (output_dir / "sla_breach_by_priority.csv").exists()


def test_cli_handles_processing_error(
    monkeypatch, tmp_path: Path, capsys
) -> None:
    monkeypatch.setattr(
        "sys.argv",
        ["data-toolkit", "missing.csv"],
    )
    monkeypatch.setattr(cli, "DEFAULT_LOG_FILE", tmp_path / "app.log")

    def raise_file_error(file_path):
        raise FileAccessError("CSV file not found: missing.csv")

    monkeypatch.setattr(cli, "load_tickets", raise_file_error)

    result = cli.main()
    output = capsys.readouterr().out

    assert result == 1
    assert "Error: CSV file not found: missing.csv" in output
