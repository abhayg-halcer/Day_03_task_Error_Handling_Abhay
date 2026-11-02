"""Tests for application logging configuration."""

import logging
from pathlib import Path

from data_toolkit.logging_config import configure_logging


def test_configure_logging_writes_to_file(tmp_path: Path) -> None:
    log_file = tmp_path / "logs" / "test.log"

    configure_logging(log_file)
    logging.getLogger("test_logging").info("Test log message")

    for handler in logging.getLogger().handlers:
        handler.flush()

    assert log_file.exists()
    assert "Test log message" in log_file.read_text(encoding="utf-8")
