"""Tests for SupportTicket model validation and representation."""

from dataclasses import FrozenInstanceError, replace
from datetime import datetime

import pytest

from data_toolkit.models.support_ticket import SupportTicket


@pytest.fixture
def valid_ticket() -> SupportTicket:
    return SupportTicket(
        ticket_id="TKT001",
        customer_id="CUST001",
        category="Technical",
        priority="High",
        status="Resolved",
        created_at=datetime(2024, 1, 15, 10, 30),
        resolution_time_hours=2.5,
        customer_rating=5,
        description="Unable to access account.",
    )


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("ticket_id", " ", "Ticket ID cannot be empty"),
        ("customer_id", "", "Customer ID cannot be empty"),
        ("category", "Unknown", "Invalid category"),
        ("priority", "Urgent", "Invalid priority"),
        ("status", "Pending", "Invalid status"),
        ("created_at", "2024-01-15", "created_at must be a datetime object"),
        ("resolution_time_hours", -1.0, "Resolution time cannot be negative"),
        ("customer_rating", 0, "Customer rating must be between 1 and 5"),
        ("customer_rating", 6, "Customer rating must be between 1 and 5"),
        ("customer_rating", True, "Customer rating must be between 1 and 5"),
        ("description", "  ", "Description cannot be empty"),
    ],
)
def test_rejects_invalid_ticket_fields(
    valid_ticket: SupportTicket,
    field: str,
    value: object,
    message: str,
) -> None:
    with pytest.raises(ValueError, match=message):
        replace(valid_ticket, **{field: value})


@pytest.mark.parametrize("status", ["Resolved", "Closed"])
def test_resolved_tickets_require_resolution_time(
    valid_ticket: SupportTicket,
    status: str,
) -> None:
    with pytest.raises(
        ValueError,
        match="Resolved or Closed tickets need a resolution time",
    ):
        replace(valid_ticket, status=status, resolution_time_hours=None)


@pytest.mark.parametrize("status", ["Open", "In Progress"])
def test_unresolved_tickets_cannot_have_resolution_time(
    valid_ticket: SupportTicket,
    status: str,
) -> None:
    with pytest.raises(
        ValueError,
        match="Unresolved tickets cannot have a resolution time",
    ):
        replace(valid_ticket, status=status)


@pytest.mark.parametrize("status", ["Open", "In Progress"])
def test_valid_unresolved_ticket(
    valid_ticket: SupportTicket,
    status: str,
) -> None:
    ticket = replace(
        valid_ticket,
        status=status,
        resolution_time_hours=None,
        customer_rating=None,
    )

    assert ticket.status == status
    assert ticket.resolution_time_hours is None
    assert ticket.customer_rating is None


def test_ticket_string_representation(valid_ticket: SupportTicket) -> None:
    assert str(valid_ticket) == (
        "Ticket TKT001: High priority, status=Resolved"
    )
    assert repr(valid_ticket) == (
        "SupportTicket(ticket_id='TKT001', "
        "priority='High', status='Resolved')"
    )


def test_ticket_is_immutable(valid_ticket: SupportTicket) -> None:
    with pytest.raises(FrozenInstanceError):
        valid_ticket.status = "Open"
