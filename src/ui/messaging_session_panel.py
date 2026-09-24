"""
Project : WhatsApp Campaign Manager
Project ID : 026

Messaging Session Panel
"""

import tkinter as tk
from tkinter import messagebox, ttk

from src.models.contact_model import Contact
from src.models.message_model import Message
from src.services.messaging_session_service import MessagingSessionService
from src.services.whatsapp_service import WhatsAppService


class MessagingSessionPanel(ttk.Frame):
    """Provides the sequential contact messaging workflow."""

    def __init__(
        self,
        parent: tk.Widget,
        contacts: list[Contact],
        message: Message,
        whatsapp_service: WhatsAppService | None = None,
        status_callback: callable | None = None,
    ) -> None:
        super().__init__(parent)

        self.contacts = contacts
        self.message = message
        self.whatsapp_service = whatsapp_service or WhatsAppService()
        self.status_callback = status_callback

        self.session_service = MessagingSessionService(self.contacts)

        self.contact_name_var = tk.StringVar(value="")
        self.phone_number_var = tk.StringVar(value="")
        self.progress_var = tk.StringVar(value="")
        self.message_preview_var = tk.StringVar(value="")
        self.session_status_var = tk.StringVar(value="")

        self._build_layout()
        self._refresh_display()

    def _build_layout(self) -> None:
        """Build the messaging session user interface."""

        header_frame = ttk.Frame(self)
        header_frame.pack(fill="x", padx=15, pady=(15, 10))

        ttk.Label(
            header_frame,
            text="Messaging Session",
            font=("TkDefaultFont", 16, "bold"),
        ).pack(anchor="w")

        ttk.Label(
            header_frame,
            text=(
                "Work through the imported contacts one at a time. "
                "The application prepares WhatsApp Web; you click Send manually."
            ),
            wraplength=850,
        ).pack(anchor="w", pady=(5, 0))

        contact_frame = ttk.LabelFrame(
            self,
            text="Current Contact",
            padding=12,
        )
        contact_frame.pack(fill="x", padx=15, pady=10)

        ttk.Label(
            contact_frame,
            text="Name:",
        ).grid(row=0, column=0, sticky="w", padx=(0, 10), pady=5)

        ttk.Label(
            contact_frame,
            textvariable=self.contact_name_var,
            font=("TkDefaultFont", 11, "bold"),
        ).grid(row=0, column=1, sticky="w", pady=5)

        ttk.Label(
            contact_frame,
            text="Phone:",
        ).grid(row=1, column=0, sticky="w", padx=(0, 10), pady=5)

        ttk.Label(
            contact_frame,
            textvariable=self.phone_number_var,
        ).grid(row=1, column=1, sticky="w", pady=5)

        ttk.Label(
            contact_frame,
            textvariable=self.progress_var,
        ).grid(row=0, column=2, rowspan=2, sticky="e", padx=(30, 0))

        contact_frame.columnconfigure(1, weight=1)

        message_frame = ttk.LabelFrame(
            self,
            text="Prepared Message",
            padding=12,
        )
        message_frame.pack(fill="both", expand=True, padx=15, pady=10)

        message_text = tk.Text(
            message_frame,
            height=10,
            wrap="word",
            state="disabled",
        )
        message_text.pack(fill="both", expand=True)

        self.message_text = message_text

        controls_frame = ttk.Frame(self)
        controls_frame.pack(fill="x", padx=15, pady=(5, 10))

        self.previous_button = ttk.Button(
            controls_frame,
            text="Previous",
            command=self._previous_contact,
        )
        self.previous_button.pack(side="left", padx=(0, 5))

        self.next_button = ttk.Button(
            controls_frame,
            text="Next",
            command=self._next_contact,
        )
        self.next_button.pack(side="left", padx=5)

        self.open_whatsapp_button = ttk.Button(
            controls_frame,
            text="Open WhatsApp Web",
            command=self._open_whatsapp,
        )
        self.open_whatsapp_button.pack(side="left", padx=5)

        self.sent_button = ttk.Button(
            controls_frame,
            text="Mark Sent & Next",
            command=self._mark_sent,
        )
        self.sent_button.pack(side="left", padx=5)

        self.skip_button = ttk.Button(
            controls_frame,
            text="Skip & Next",
            command=self._skip_current,
        )
        self.skip_button.pack(side="left", padx=5)

        status_frame = ttk.Frame(self)
        status_frame.pack(fill="x", padx=15, pady=(0, 15))

        ttk.Label(
            status_frame,
            textvariable=self.session_status_var,
        ).pack(side="left")

    def _refresh_display(self) -> None:
        """Refresh the displayed contact, message and session controls."""

        contact = self.session_service.current_contact

        if contact is None:
            self.contact_name_var.set("")
            self.phone_number_var.set("")
            self.progress_var.set("No contacts available")
            self._set_message_text("")
            self.session_status_var.set("No contacts available.")

            self.previous_button.configure(state="disabled")
            self.next_button.configure(state="disabled")
            self.open_whatsapp_button.configure(state="disabled")
            self.sent_button.configure(state="disabled")
            self.skip_button.configure(state="disabled")
            return

        prepared_message = self.whatsapp_service.build_message(
            self.message,
            contact.name,
        )

        self.contact_name_var.set(contact.name)
        self.phone_number_var.set(contact.phone_number)
        self.progress_var.set(
            f"Contact {self.session_service.session.progress_position} "
            f"of {self.session_service.session.total_contacts}"
        )

        self._set_message_text(prepared_message)

        session = self.session_service.session

        self.session_status_var.set(
            f"Completed: {session.completed_count} | "
            f"Skipped: {session.skipped_count} | "
            f"Remaining: {session.remaining_count}"
        )

        self.previous_button.configure(
            state=(
                "normal"
                if session.current_index > 0
                else "disabled"
            )
        )

        self.next_button.configure(
            state=(
                "normal"
                if session.current_index < len(self.contacts) - 1
                else "disabled"
            )
        )

        self.open_whatsapp_button.configure(state="normal")

        self.sent_button.configure(
            state="disabled" if session.is_complete else "normal"
        )

        self.skip_button.configure(
            state="disabled" if session.is_complete else "normal"
        )

    def _set_message_text(self, message_text: str) -> None:
        """Replace the read-only message preview content."""

        self.message_text.configure(state="normal")
        self.message_text.delete("1.0", tk.END)
        self.message_text.insert("1.0", message_text)
        self.message_text.configure(state="disabled")

    def _open_whatsapp(self) -> None:
        """Open the current contact's prepared message in WhatsApp Web."""

        contact = self.session_service.current_contact

        if contact is None:
            return

        prepared_message = self.whatsapp_service.build_message(
            self.message,
            contact.name,
        )

        try:
            self.whatsapp_service.open_conversation(
                contact.phone_number,
                prepared_message,
            )
        except Exception as error:
            messagebox.showerror(
                "WhatsApp Web Error",
                f"Unable to open WhatsApp Web.\n\n{error}",
            )
            self._set_status(f"Unable to open WhatsApp Web: {error}")
            return

        self._set_status(
            f"WhatsApp Web opened for {contact.name}. "
            "Review the message and click Send manually."
        )

    def _mark_sent(self) -> None:
        """Mark the current contact as sent and advance the session."""

        contact = self.session_service.current_contact

        if contact is None:
            return

        if self.session_service.mark_sent():
            self._set_status(
                f"Marked {contact.name} as sent."
            )

        self._refresh_display()

        if self.session_service.session.is_complete:
            messagebox.showinfo(
                "Messaging Session Complete",
                "All contacts have been processed.",
            )

    def _skip_current(self) -> None:
        """Mark the current contact as skipped and advance the session."""

        contact = self.session_service.current_contact

        if contact is None:
            return

        if self.session_service.skip_current():
            self._set_status(
                f"Skipped {contact.name}."
            )

        self._refresh_display()

        if self.session_service.session.is_complete:
            messagebox.showinfo(
                "Messaging Session Complete",
                "All contacts have been processed.",
            )

    def _next_contact(self) -> None:
        """Move to the next contact without changing session status."""

        if self.session_service.next_contact():
            self._set_status("Moved to the next contact.")
        else:
            self._set_status("Already at the last contact.")

        self._refresh_display()

    def _previous_contact(self) -> None:
        """Move to the previous contact without changing session status."""

        if self.session_service.previous_contact():
            self._set_status("Moved to the previous contact.")
        else:
            self._set_status("Already at the first contact.")

        self._refresh_display()

    def _set_status(self, message: str) -> None:
        """Send a status message to the parent window."""

        if self.status_callback:
            self.status_callback(message)


__all__ = ["MessagingSessionPanel"]