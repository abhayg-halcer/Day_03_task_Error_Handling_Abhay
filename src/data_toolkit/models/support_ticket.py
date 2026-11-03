from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class SupportTicket:
    ticket_id: str
    customer_id: str
    category: str
    priority: str
    status: str
    created_at: datetime
    resolution_time_hours: Optional[float]
    customer_rating: Optional[int]
    description: str

    def __post_init__(self):
        allowed_categories = {
            "Billing", "Technical", "Account", "Delivery", "Product"
        }
        allowed_priorities = {"Low", "Medium", "High", "Critical"}
        allowed_statuses = {"Open", "In Progress", "Resolved", "Closed"}

        if not self.ticket_id.strip():
            raise ValueError("Ticket ID cannot be empty")

        if not self.customer_id.strip():
            raise ValueError("Customer ID cannot be empty")

        if self.category not in allowed_categories:
            raise ValueError(f"Invalid category: {self.category}")

        if self.priority not in allowed_priorities:
            raise ValueError(f"Invalid priority: {self.priority}")

        if self.status not in allowed_statuses:
            raise ValueError(f"Invalid status: {self.status}")

        if not isinstance(self.created_at, datetime):
            raise ValueError("created_at must be a datetime object")

        if self.resolution_time_hours is not None:
            if self.resolution_time_hours < 0:
                raise ValueError("Resolution time cannot be negative")

        if self.customer_rating is not None:
            if isinstance(self.customer_rating, bool) or not 1 <= self.customer_rating <= 5:
                raise ValueError("Customer rating must be between 1 and 5")

        if self.status in {"Resolved", "Closed"}:
            if self.resolution_time_hours is None:
                raise ValueError("Resolved or Closed tickets need a resolution time")

        if self.status in {"Open", "In Progress"}:
            if self.resolution_time_hours is not None:
                raise ValueError("Unresolved tickets cannot have a resolution time")

        if not self.description.strip():
            raise ValueError("Description cannot be empty")

    def __str__(self):
        return (
            f"Ticket {self.ticket_id}: "
            f"{self.priority} priority, "
            f"status={self.status}"
        )

    def __repr__(self):
        return (
            f"SupportTicket(ticket_id={self.ticket_id!r}, "
            f"priority={self.priority!r}, "
            f"status={self.status!r})"
        )
