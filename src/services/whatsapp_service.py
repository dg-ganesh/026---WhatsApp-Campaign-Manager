"""
Project : WhatsApp Campaign Manager
Project ID : 026

WhatsApp Web Service
"""

import webbrowser
from urllib.parse import quote

from src.models.message_model import Message


class WhatsAppService:
    """Provides URL-based navigation to WhatsApp Web."""

    BASE_URL = "https://web.whatsapp.com/send"

    def build_message(
        self,
        message: Message,
        contact_name: str,
    ) -> str:
        """Prepare a message for the specified contact."""
        return message.prepare_for_contact(
            contact_name
        )

    def build_url(
        self,
        phone_number: str,
        message_text: str,
    ) -> str:
        """
        Build a WhatsApp Web URL for a phone number and message.

        The message is URL-encoded so spaces, punctuation,
        and line breaks can be safely passed to WhatsApp Web.
        """
        encoded_message = quote(
            message_text,
            safe="",
        )

        return (
            f"{self.BASE_URL}"
            f"?phone={phone_number}"
            f"&text={encoded_message}"
        )

    def open_conversation(
        self,
        phone_number: str,
        message_text: str,
    ) -> str:
        """
        Open the WhatsApp Web conversation in the default browser.

        Returns the URL used to open the conversation.
        """
        url = self.build_url(
            phone_number,
            message_text,
        )

        webbrowser.open(url)

        return url


__all__ = [
    "WhatsAppService",
]