"""
Project : WhatsApp Campaign Manager
Project ID : 026

Messaging Session Service
"""

from src.models.contact_model import Contact
from src.models.messaging_session_model import MessagingSession


class MessagingSessionService:
    """Controls the sequential messaging session."""

    def __init__(
        self,
        contacts: list[Contact],
    ) -> None:
        self.contacts = contacts

        self.session = MessagingSession(
            total_contacts=len(contacts)
        )

    @property
    def current_contact(self) -> Contact | None:
        """Return the currently selected contact."""
        if not self.contacts:
            return None

        if (
            self.session.current_index < 0
            or self.session.current_index
            >= len(self.contacts)
        ):
            return None

        return self.contacts[
            self.session.current_index
        ]

    def mark_sent(self) -> bool:
        """
        Mark the current contact as manually sent.

        This method records the user's confirmation only.
        It does not send anything through WhatsApp.
        """
        if self.current_contact is None:
            return False

        index = self.session.current_index

        self.session.completed_indexes.add(
            index
        )

        self.session.skipped_indexes.discard(
            index
        )

        self._move_to_next_unprocessed()

        return True

    def skip_current(self) -> bool:
        """Skip the current contact and move forward."""
        if self.current_contact is None:
            return False

        index = self.session.current_index

        self.session.skipped_indexes.add(
            index
        )

        self.session.completed_indexes.discard(
            index
        )

        self._move_to_next_unprocessed()

        return True

    def next_contact(self) -> bool:
        """
        Move to the next contact without marking
        the current contact as sent or skipped.
        """
        if not self.contacts:
            return False

        next_index = (
            self.session.current_index + 1
        )

        if next_index >= len(self.contacts):
            return False

        self.session.current_index = next_index

        return True

    def previous_contact(self) -> bool:
        """Move to the previous contact."""
        if not self.contacts:
            return False

        previous_index = (
            self.session.current_index - 1
        )

        if previous_index < 0:
            return False

        self.session.current_index = previous_index

        return True

    def reset_to_first_unprocessed(self) -> None:
        """Move to the first contact not yet processed."""
        self.session.current_index = 0

        self._move_to_next_unprocessed(
            include_current=True
        )

    def _move_to_next_unprocessed(
        self,
        include_current: bool = False,
    ) -> None:
        """Move to the next contact not yet processed."""
        if not self.contacts:
            return

        start_index = self.session.current_index

        if not include_current:
            start_index += 1

        for index in range(
            start_index,
            len(self.contacts),
        ):
            if (
                index
                not in self.session.completed_indexes
                and index
                not in self.session.skipped_indexes
            ):
                self.session.current_index = index
                return

        # No unprocessed contact remains.
        self.session.current_index = min(
            max(len(self.contacts) - 1, 0),
            start_index,
        )


__all__ = [
    "MessagingSessionService",
]