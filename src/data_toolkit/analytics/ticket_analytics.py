from collections import Counter

from data_toolkit.models.support_ticket import SupportTicket


def generate_summary(tickets: list[SupportTicket]) -> dict:
    """
    Generate overall ticket summary metrics.
    """
    status_counts = Counter(ticket.status for ticket in tickets)
    priority_counts = Counter(ticket.priority for ticket in tickets)

    return {
        "total_tickets": len(tickets),
        "status_counts": dict(status_counts),
        "priority_counts": dict(priority_counts),
        "average_resolution_hours": (
            round(
                sum(
                    ticket.resolution_time_hours
                    for ticket in tickets
                    if ticket.resolution_time_hours is not None
                )
                / sum(
                    ticket.resolution_time_hours is not None
                    for ticket in tickets
                ),
                2,
            )
            if any(
                ticket.resolution_time_hours is not None
                for ticket in tickets
            )
            else 0
        ),
    }

SLA_LIMITS = {
    "Critical": 4,
    "High": 8,
    "Medium": 24,
    "Low": 72,
}


def analyze_sla_breaches(
    tickets: list[SupportTicket],
) -> list[dict]:
    """
    Calculate SLA breaches grouped by priority.
    """
    results = []

    for priority, sla_limit in SLA_LIMITS.items():
        priority_tickets = [
            ticket for ticket in tickets
            if ticket.priority == priority
        ]

        resolved = [
            ticket for ticket in priority_tickets
            if ticket.resolution_time_hours is not None
        ]

        unresolved = [
            ticket for ticket in priority_tickets
            if ticket.resolution_time_hours is None
        ]

        breached = sum(
            ticket.resolution_time_hours > sla_limit
            for ticket in resolved
        )

        within_sla = len(resolved) - breached

        breach_percentage = (
            round(breached / len(resolved) * 100, 2)
            if resolved else 0
        )

        results.append({
            "priority": priority,
            "total_tickets": len(priority_tickets),
            "resolved_tickets": len(resolved),
            "unresolved_tickets": len(unresolved),
            "breached_tickets": breached,
            "within_sla_tickets": within_sla,
            "breach_percentage": breach_percentage,
        })

    return results