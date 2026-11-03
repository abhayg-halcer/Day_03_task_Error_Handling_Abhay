from datetime import datetime
from pathlib import Path

from data_toolkit.models.support_ticket import SupportTicket
from data_toolkit.processing.ticket_validator import validate_ticket_row


def clean_tickets(rows: list[dict]) -> tuple[list[SupportTicket], list[dict]]:
    """
    Clean raw ticket rows.

    Returns:
        valid_tickets: Valid SupportTicket objects.
        quality_report: List of rejected or flagged data-quality issues.
    """
    valid_tickets = []
    quality_report = []
    seen_ticket_ids = set()

    for row_number, row in enumerate(rows, start=2):
        ticket_id = row.get("ticket_id", "").strip()

        # Reject duplicate ticket IDs
        if ticket_id and ticket_id in seen_ticket_ids:
            quality_report.append({
                "row_number": row_number,
                "ticket_id": ticket_id,
                "field": "ticket_id",
                "issue": "duplicate_ticket_id",
                "action": "rejected",
            })
            continue

        if ticket_id:
            seen_ticket_ids.add(ticket_id)

        issues = validate_ticket_row(row)

        # Invalid ratings are optional: flag and normalize to None
        blocking_issues = []

        for issue in issues:
            report_item = {
                "row_number": row_number,
                "ticket_id": ticket_id,
                "field": issue["field"],
                "issue": issue["issue"],
                "action": "normalized_to_none"
                if issue["issue"] == "invalid_rating"
                else "rejected",
            }
            quality_report.append(report_item)

            if issue["issue"] != "invalid_rating":
                blocking_issues.append(issue)

        if blocking_issues:
            continue

        try:
            duration = row["resolution_time_hours"].strip()
            rating = row["customer_rating"].strip()

            if rating:
                try:
                    rating_value = int(rating)
                    if not 1 <= rating_value <= 5:
                        rating = ""
                except ValueError:
                    rating = ""

            ticket = SupportTicket(
                ticket_id=ticket_id,
                customer_id=row["customer_id"].strip(),
                category=row["category"].strip(),
                priority=row["priority"].strip(),
                status=row["status"].strip(),
                created_at=datetime.fromisoformat(row["created_at"].strip()),
                resolution_time_hours=float(duration) if duration else None,
                customer_rating=int(rating) if rating else None,
                description=row["description"].strip(),
            )

            valid_tickets.append(ticket)

        except (ValueError, TypeError) as error:
            quality_report.append({
                "row_number": row_number,
                "ticket_id": ticket_id,
                "field": "record",
                "issue": str(error),
                "action": "rejected",
            })

    return valid_tickets, quality_report