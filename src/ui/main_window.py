"""
Project : WhatsApp Campaign Manager
Project ID : 026

Main Application Window
"""

import tkinter as tk
from tkinter import ttk

from src.config import (
    APP_NAME,
    APP_VERSION,
    MIN_WINDOW_HEIGHT,
    MIN_WINDOW_WIDTH,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
)
from src.models.contact_model import Contact
from src.models.message_model import Message
from src.ui.csv_import_panel import CSVImportPanel
from src.ui.message_panel import MessagePanel
from src.ui.messaging_session_panel import MessagingSessionPanel


class MainWindow:
    """Main application window for WhatsApp Campaign Manager."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root

        self.contacts: list[Contact] = []
        self.message: Message | None = None

        self._configure_window()
        self._build_layout()
        self.show_import_panel()

    def _configure_window(self) -> None:
        """Configure the main application window."""
        self.root.title(
            f"{APP_NAME} - v{APP_VERSION}"
        )

        self.root.geometry(
            f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}"
        )

        self.root.minsize(
            MIN_WINDOW_WIDTH,
            MIN_WINDOW_HEIGHT,
        )

    def _build_layout(self) -> None:
        """Build the main application layout."""
        self.root.columnconfigure(
            0,
            weight=1,
        )

        self.root.rowconfigure(
            1,
            weight=1,
        )

        header = ttk.Frame(
            self.root,
            padding=(16, 12),
        )

        header.grid(
            row=0,
            column=0,
            sticky="ew",
        )

        header.columnconfigure(
            0,
            weight=1,
        )

        title_label = ttk.Label(
            header,
            text=APP_NAME,
            font=("Segoe UI", 16, "bold"),
        )

        title_label.grid(
            row=0,
            column=0,
            sticky="w",
        )

        version_label = ttk.Label(
            header,
            text=f"Version {APP_VERSION}",
        )

        version_label.grid(
            row=1,
            column=0,
            sticky="w",
            pady=(2, 0),
        )

        navigation_frame = ttk.Frame(
            header
        )

        navigation_frame.grid(
            row=0,
            column=1,
            rowspan=2,
            sticky="e",
        )

        self.import_button = ttk.Button(
            navigation_frame,
            text="Contacts",
            command=self.show_import_panel,
        )

        self.import_button.grid(
            row=0,
            column=0,
            padx=(0, 6),
        )

        self.message_button = ttk.Button(
            navigation_frame,
            text="Message",
            command=self.show_message_panel,
        )

        self.message_button.grid(
            row=0,
            column=1,
            padx=(0, 6),
        )

        self.session_button = ttk.Button(
            navigation_frame,
            text="Messaging Session",
            command=self.show_messaging_session,
        )

        self.session_button.grid(
            row=0,
            column=2,
        )

        separator = ttk.Separator(
            self.root,
            orient="horizontal",
        )

        separator.grid(
            row=0,
            column=0,
            sticky="se",
        )

        self.content_frame = ttk.Frame(
            self.root,
            padding=16,
        )

        self.content_frame.grid(
            row=1,
            column=0,
            sticky="nsew",
        )

        self.content_frame.columnconfigure(
            0,
            weight=1,
        )

        self.content_frame.rowconfigure(
            0,
            weight=1,
        )

        self.status_var = tk.StringVar(
            value="Ready"
        )

        status_bar = ttk.Label(
            self.root,
            textvariable=self.status_var,
            relief="sunken",
            anchor="w",
            padding=(8, 4),
        )

        status_bar.grid(
            row=2,
            column=0,
            sticky="ew",
        )

        self._update_navigation_buttons()

    def show_import_panel(self) -> None:
        """Display the contact import panel."""
        self._clear_content()

        panel = CSVImportPanel(
            self.content_frame,
            status_callback=self.set_status,
            contacts_callback=self.set_contacts,
        )

        panel.pack(
            fill="both",
            expand=True,
        )

        self.set_status(
            "Select a Google Contacts CSV file."
        )

    def show_message_panel(self) -> None:
        """Display the message preparation panel."""
        if not self.contacts:
            self.set_status(
                "Import contacts before preparing messages."
            )
            return

        self._clear_content()

        panel = MessagePanel(
            self.content_frame,
            contacts=self.contacts,
            status_callback=self.set_status,
            message_callback=self.set_message,
        )

        panel.pack(
            fill="both",
            expand=True,
        )

        self.set_status(
            f"{len(self.contacts)} contacts available."
        )

    def show_messaging_session(self) -> None:
        """Display the sequential messaging session."""
        if not self.contacts:
            self.set_status(
                "Import contacts before starting a session."
            )
            return

        if self.message is None:
            self.set_status(
                "Prepare a message before starting a session."
            )
            return

        self._clear_content()

        panel = MessagingSessionPanel(
            self.content_frame,
            contacts=self.contacts,
            message=self.message,
            status_callback=self.set_status,
        )

        panel.pack(
            fill="both",
            expand=True,
        )

        self.set_status(
            "Messaging session ready."
        )

    def set_contacts(
        self,
        contacts: list[Contact],
    ) -> None:
        """Store contacts imported from the CSV."""
        self.contacts = contacts

        if contacts:
            self.set_status(
                f"Imported {len(contacts)} contacts."
            )
        else:
            self.set_status(
                "No contacts were imported."
            )

        self._update_navigation_buttons()

    def set_message(
        self,
        message: Message,
    ) -> None:
        """Store the message prepared by the user."""
        self.message = message

        self._update_navigation_buttons()

        self.set_status(
            "Message saved. Messaging session is ready."
        )

    def set_content(
        self,
        widget: tk.Widget,
    ) -> None:
        """Display a widget in the main content area."""
        self._clear_content()

        widget.pack(
            fill="both",
            expand=True,
        )

    def set_status(
        self,
        message: str,
    ) -> None:
        """Update the application status message."""
        self.status_var.set(message)

    def _update_navigation_buttons(self) -> None:
        """Update navigation button availability."""
        if self.contacts:
            self.message_button.state(
                ["!disabled"]
            )
        else:
            self.message_button.state(
                ["disabled"]
            )

        if self.contacts and self.message:
            self.session_button.state(
                ["!disabled"]
            )
        else:
            self.session_button.state(
                ["disabled"]
            )

    def _clear_content(self) -> None:
        """Remove the current content widget."""
        for child in self.content_frame.winfo_children():
            child.destroy()


__all__ = [
    "MainWindow",
]