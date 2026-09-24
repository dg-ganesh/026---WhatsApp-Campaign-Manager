"""
Project : WhatsApp Campaign Manager
Project ID : 026

Message Model
"""

from dataclasses import dataclass


@dataclass(slots=True)
class Message:
    """Represents a message prepared for a WhatsApp contact."""

    template: str

    def prepare_for_contact(self, contact_name: str) -> str:
        """
        Prepare the message for a specific contact.

        The optional {name} placeholder is replaced with
        the supplied contact name.
        """
        return self.template.replace(
            "{name}",
            contact_name,
        )


__all__ = [
    "Message",
]
