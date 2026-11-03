"""Command-line interface for the support ticket data pipeline."""

import argparse
import logging
from pathlib import Path

from data_toolkit.analytics.ticket_analytics import (
    analyze_sla_breaches,
    generate_summary,
)
from data_toolkit.config.settings import DEFAULT_LOG_FILE
from data_toolkit.exceptions import DataToolkitError
from data_toolkit.logging_config import configure_logging
from data_toolkit.processing.ticket_cleaner import clean_tickets
from data_toolkit.processing.ticket_loader import load_tickets
from data_toolkit.reporting.report_exporter import export_report, export_summary


def main() -> int:
    """Load, validate, analyze, and export support ticket data."""
    parser = argparse.ArgumentParser(
        description="Validate and analyze customer support tickets."
    )
    parser.add_argument(
        "file",
        nargs="?",
        type=Path,
        default=Path("data/tickets.csv"),
        help="Path to the input ticket CSV file.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("outputs"),
        help="Directory for generated CSV reports.",
    )
    args = parser.parse_args()

    configure_logging(DEFAULT_LOG_FILE)
    logger = logging.getLogger(__name__)

    try:
        raw_tickets = load_tickets(args.file)
        valid_tickets, quality_report = clean_tickets(raw_tickets)

        summary = generate_summary(valid_tickets)
        sla_results = analyze_sla_breaches(valid_tickets)

        args.output_dir.mkdir(parents=True, exist_ok=True)
        export_report(
            quality_report,
            args.output_dir / "data_quality_report.csv",
        )
        export_summary(
            summary,
            args.output_dir / "summary_metrics.csv",
        )
        export_report(
            sla_results,
            args.output_dir / "sla_breach_by_priority.csv",
        )

    except DataToolkitError as error:
        logger.exception("Ticket processing failed")
        print(f"Error: {error}")
        return 1

    print("SUPPORT TICKET PIPELINE")
    print("-" * 32)
    print(f"Raw records loaded: {len(raw_tickets)}")
    print(f"Valid tickets: {len(valid_tickets)}")
    print(f"Quality issues found: {len(quality_report)}")
    print(f"Average resolution time: {summary['average_resolution_hours']} hours")

    print("\nSLA BREACH ANALYSIS")
    for result in sla_results:
        print(
            f"{result['priority']}: "
            f"{result['breached_tickets']} breached / "
            f"{result['resolved_tickets']} resolved "
            f"({result['breach_percentage']}%)"
        )

    print(f"\nReports exported to: {args.output_dir}")
    logger.info("Ticket pipeline completed successfully")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
