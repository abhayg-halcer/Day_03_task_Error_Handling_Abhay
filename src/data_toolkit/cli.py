"""Command-line interface for the data toolkit."""

import argparse
import logging
from pathlib import Path

from data_toolkit.analytics.summary import generate_summary
from data_toolkit.config.settings import DEFAULT_LOG_FILE
from data_toolkit.exceptions import DataToolkitError
from data_toolkit.logging_config import configure_logging
from data_toolkit.processing.loader import load_csv


def main() -> int:
    """Run the CSV analysis application."""
    parser = argparse.ArgumentParser(
        description="Validate and analyze a CSV sales file."
    )
    parser.add_argument(
        "file",
        type=Path,
        help="Path to the input CSV file.",
    )
    args = parser.parse_args()

    configure_logging(DEFAULT_LOG_FILE)
    logger = logging.getLogger(__name__)

    try:
        records = load_csv(args.file)
        summary = generate_summary(records)

    except DataToolkitError as error:
        logger.error("Processing failed: %s", error)
        print(f"Error: {error}")
        return 1

    print("\nSALES SUMMARY")
    print("-" * 30)

    for key, value in summary.items():
        print(f"{key.replace('_', ' ').title()}: {value}")

    logger.info("Sales summary generated successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
