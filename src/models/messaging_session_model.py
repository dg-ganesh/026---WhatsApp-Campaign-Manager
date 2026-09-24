"""
Project : WhatsApp Campaign Manager
Project ID : 026

Messaging Session Model
"""

from dataclasses import dataclass, field


@dataclass(slots=True)
class MessagingSession:
    """Stores the state of a sequential messaging session."""

    total_contacts: int
    current_index: int = 0
    completed_indexes: set[int] = field(
        default_factory=set
    )
    skipped_indexes: set[int] = field(
        default_factory=set
    )

    @property
    def completed_count(self) -> int:
        """Return the number of completed contacts."""
        return len(self.completed_indexes)

    @property
    def skipped_count(self) -> int:
        """Return the number of skipped contacts."""
        return len(self.skipped_indexes)

    @property
    def remaining_count(self) -> int:
        """Return the number of contacts not yet completed or skipped."""
        return max(
            self.total_contacts
            - self.completed_count
            - self.skipped_count,
            0,
        )

    @property
    def progress_position(self) -> int:
        """Return the one-based current contact position."""
        if self.total_contacts <= 0:
            return 0

        return self.current_index + 1

    @property
    def is_complete(self) -> bool:
        """Return whether all contacts have been processed."""
        return (
            self.completed_count
            + self.skipped_count
            >= self.total_contacts
        )


__all__ = [
    "MessagingSession",
]