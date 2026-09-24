"""
Project : WhatsApp Campaign Manager
Project ID : 026

Message Preparation Panel
"""

import tkinter as tk
from tkinter import messagebox, ttk

from src.models.contact_model import Contact
from src.models.message_model import Message
from src.services.whatsapp_service import WhatsAppService


class MessagePanel(ttk.Frame):
    """UI panel for preparing messages and opening WhatsApp Web."""

    def __init__(
        self,
        parent: tk.Widget,
        contacts: list[Contact],
        whatsapp_service: WhatsAppService | None = None,
        status_callback: callable | None = None,
        message_callback: callable | None = None,
    ) -> None:
        super().__init__(parent)

        self.contacts = contacts
        self.whatsapp_service = (
            whatsapp_service or WhatsAppService()
        )
        self.status_callback = status_callback
        self.message_callback = message_callback

        self.selected_contact_index = 0

        self.contact_name_var = tk.StringVar(
            value=""
        )
        self.contact_phone_var = tk.StringVar(
            value=""
        )
        self.preview_var = tk.StringVar(
            value=""
        )

        self._build_layout()

        if self.contacts:
            self._display_contact(0)

    def _build_layout(self) -> None:
        """Build the message preparation interface."""
        self.columnconfigure(0, weight=1)
        self.rowconfigure(4, weight=1)

        header = ttk.Label(
            self,
            text="Message Preparation",
            font=("Segoe UI", 14, "bold"),
        )
        header.grid(
            row=0,
            column=0,
            sticky="w",
            pady=(0, 12),
        )

        contact_frame = ttk.LabelFrame(
            self,
            text="Selected Contact",
            padding=12,
        )
        contact_frame.grid(
            row=1,
            column=0,
            sticky="ew",
            pady=(0, 12),
        )

        contact_frame.columnconfigure(
            1,
            weight=1,
        )

        ttk.Label(
            contact_frame,
            text="Name:",
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=(0, 12),
        )

        ttk.Label(
            contact_frame,
            textvariable=self.contact_name_var,
        ).grid(
            row=0,
            column=1,
            sticky="w",
        )

        ttk.Label(
            contact_frame,
            text="Phone:",
        ).grid(
            row=1,
            column=0,
            sticky="w",
            padx=(0, 12),
            pady=(6, 0),
        )

        ttk.Label(
            contact_frame,
            textvariable=self.contact_phone_var,
        ).grid(
            row=1,
            column=1,
            sticky="w",
            pady=(6, 0),
        )

        message_frame = ttk.LabelFrame(
            self,
            text="Message",
            padding=12,
        )
        message_frame.grid(
            row=2,
            column=0,
            sticky="ew",
            pady=(0, 12),
        )

        message_frame.columnconfigure(
            0,
            weight=1,
        )

        instruction = ttk.Label(
            message_frame,
            text=(
                "Enter your message. Use {name} "
                "to personalize it."
            ),
        )
        instruction.grid(
            row=0,
            column=0,
            sticky="w",
            pady=(0, 6),
        )

        self.message_text = tk.Text(
            message_frame,
            height=6,
            wrap="word",
        )
        self.message_text.grid(
            row=1,
            column=0,
            sticky="ew",
        )

        self.message_text.bind(
            "<KeyRelease>",
            self._on_message_changed,
        )

        preview_frame = ttk.LabelFrame(
            self,
            text="Prepared Message",
            padding=12,
        )
        preview_frame.grid(
            row=3,
            column=0,
            sticky="ew",
            pady=(0, 12),
        )

        preview_frame.columnconfigure(
            0,
            weight=1,
        )

        preview_label = ttk.Label(
            preview_frame,
            textvariable=self.preview_var,
            wraplength=850,
            justify="left",
        )
        preview_label.grid(
            row=0,
            column=0,
            sticky="w",
        )

        action_frame = ttk.Frame(self)
        action_frame.grid(
            row=4,
            column=0,
            sticky="ew",
        )

        action_frame.columnconfigure(
            0,
            weight=1,
        )

        self.previous_button = ttk.Button(
            action_frame,
            text="Previous",
            command=self._previous_contact,
        )
        self.previous_button.grid(
            row=0,
            column=0,
            sticky="w",
        )

        self.next_button = ttk.Button(
            action_frame,
            text="Next",
            command=self._next_contact,
        )
        self.next_button.grid(
            row=0,
            column=1,
            padx=(8, 0),
        )

        open_button = ttk.Button(
            action_frame,
            text="Open WhatsApp Web",
            command=self._open_whatsapp,
        )
        open_button.grid(
            row=0,
            column=2,
            padx=(8, 0),
        )

        self.prepare_button = ttk.Button(
            action_frame,
            text="Use Message for Session",
            command=self._use_message_for_session,
        )
        self.prepare_button.grid(
            row=0,
            column=3,
            padx=(8, 0),
        )

        self._update_navigation_buttons()
        self._update_message_button()

    def _display_contact(
        self,
        index: int,
    ) -> None:
        """Display the selected contact."""
        if not self.contacts:
            self.contact_name_var.set("")
            self.contact_phone_var.set("")
            self.preview_var.set("")
            return

        self.selected_contact_index = index

        contact = self.contacts[index]

        self.contact_name_var.set(
            contact.name
        )
        self.contact_phone_var.set(
            contact.phone_number
        )

        self._update_preview()
        self._update_navigation_buttons()

        self._set_status(
            f"Contact {index + 1} of "
            f"{len(self.contacts)}"
        )

    def _on_message_changed(
        self,
        _event: tk.Event,
    ) -> None:
        """Handle message text changes."""
        self._update_preview()
        self._update_message_button()

    def _update_preview(self) -> None:
        """Update the personalized message preview."""
        message_text = self.message_text.get(
            "1.0",
            "end-1c",
        )

        if not message_text.strip():
            self.preview_var.set(
                "Enter a message to see the preview."
            )
            return

        contact = self.contacts[
            self.selected_contact_index
        ]

        message = Message(
            template=message_text,
        )

        prepared_message = (
            message.prepare_for_contact(
                contact.name
            )
        )

        self.preview_var.set(
            prepared_message
        )

    def _use_message_for_session(self) -> None:
        """Send the entered message to the main window."""
        message_text = self.message_text.get(
            "1.0",
            "end-1c",
        ).strip()

        if not message_text:
            messagebox.showwarning(
                "Message Required",
                "Please enter a message first.",
            )
            return

        message = Message(
            template=message_text,
        )

        if self.message_callback:
            self.message_callback(
                message
            )

        self._set_status(
            "Message saved for the messaging session."
        )

    def _open_whatsapp(self) -> None:
        """Prepare the message and open WhatsApp Web."""
        if not self.contacts:
            messagebox.showwarning(
                "No Contacts",
                "No contacts are currently available.",
            )
            return

        message_text = self.message_text.get(
            "1.0",
            "end-1c",
        ).strip()

        if not message_text:
            messagebox.showwarning(
                "Message Required",
                "Please enter a message first.",
            )
            return

        contact = self.contacts[
            self.selected_contact_index
        ]

        message = Message(
            template=message_text,
        )

        prepared_message = (
            message.prepare_for_contact(
                contact.name
            )
        )

        self.whatsapp_service.open_conversation(
            phone_number=contact.phone_number,
            message_text=prepared_message,
        )

        self._set_status(
            "WhatsApp Web opened. "
            "Review the message and send it manually."
        )

    def _previous_contact(self) -> None:
        """Display the previous contact."""
        if not self.contacts:
            return

        if self.selected_contact_index <= 0:
            return

        self._display_contact(
            self.selected_contact_index - 1
        )

    def _next_contact(self) -> None:
        """Display the next contact."""
        if not self.contacts:
            return

        if (
            self.selected_contact_index
            >= len(self.contacts) - 1
        ):
            return

        self._display_contact(
            self.selected_contact_index + 1
        )

    def _update_navigation_buttons(self) -> None:
        """Enable or disable contact navigation buttons."""
        if not self.contacts:
            self.previous_button.state(
                ["disabled"]
            )
            self.next_button.state(
                ["disabled"]
            )
            return

        if self.selected_contact_index == 0:
            self.previous_button.state(
                ["disabled"]
            )
        else:
            self.previous_button.state(
                ["!disabled"]
            )

        if (
            self.selected_contact_index
            >= len(self.contacts) - 1
        ):
            self.next_button.state(
                ["disabled"]
            )
        else:
            self.next_button.state(
                ["!disabled"]
            )

    def _update_message_button(self) -> None:
        """Enable the session message button when text exists."""
        message_text = self.message_text.get(
            "1.0",
            "end-1c",
        ).strip()

        if message_text:
            self.prepare_button.state(
                ["!disabled"]
            )
        else:
            self.prepare_button.state(
                ["disabled"]
            )

    def _set_status(
        self,
        message: str,
    ) -> None:
        """Update the parent application's status."""
        if self.status_callback:
            self.status_callback(
                message
            )


__all__ = [
    "MessagePanel",
]