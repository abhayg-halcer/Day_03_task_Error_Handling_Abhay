"""Data models used by the application."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Record:
    """Represents one product sales record."""

    product: str
    quantity: int
    price: float

    @property
    def total(self) -> float:
        """Calculate total sales for this record."""
        return round(self.quantity * self.price, 2)
