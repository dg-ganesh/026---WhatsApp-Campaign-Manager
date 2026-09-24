"""
Project : WhatsApp Campaign Manager
Project ID : 026

Contact Model
"""

from dataclasses import dataclass


@dataclass(slots=True)
class Contact:
    """Represents a contact imported from the source CSV file."""

    name: str
    phone_number: str
    source_row: int | None = None


__all__ = [
    "Contact",
]