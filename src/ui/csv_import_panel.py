"""
Project : WhatsApp Campaign Manager
Project ID : 026

CSV Import Panel
"""

import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from src.models.contact_model import Contact
from src.services.csv_service import (
    CSVService,
    ContactImportResult,
)


class CSVImportPanel(ttk.Frame):
    """UI panel for importing and previewing contacts."""

    def __init__(
        self,
        parent: tk.Widget,
        csv_service: CSVService | None = None,
        status_callback: callable | None = None,
        contacts_callback: callable | None = None,
    ) -> None:
        super().__init__(parent)

        self.csv_service = (
            csv_service or CSVService()
        )

        self.status_callback = status_callback
        self.contacts_callback = contacts_callback

        self.selected_file_var = tk.StringVar(
            value="No CSV file selected"
        )

        self.summary_var = tk.StringVar(
            value="No contacts imported"
        )

        self._build_layout()

    def _build_layout(self) -> None:
        """Build the CSV import panel."""
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        header = ttk.Label(
            self,
            text="Contact Import",
            font=("Segoe UI", 14, "bold"),
        )
        header.grid(
            row=0,
            column=0,
            sticky="w",
            pady=(0, 12),
        )

        file_frame = ttk.Frame(self)
        file_frame.grid(
            row=1,
            column=0,
            sticky="ew",
            pady=(0, 12),
        )

        file_frame.columnconfigure(0, weight=1)

        selected_file_label = ttk.Label(
            file_frame,
            textvariable=self.selected_file_var,
        )
        selected_file_label.grid(
            row=0,
            column=0,
            sticky="w",
            padx=(0, 8),
        )

        browse_button = ttk.Button(
            file_frame,
            text="Select CSV",
            command=self._select_csv,
        )
        browse_button.grid(
            row=0,
            column=1,
            sticky="e",
        )

        table_frame = ttk.Frame(self)
        table_frame.grid(
            row=2,
            column=0,
            sticky="nsew",
        )

        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)

        self.contact_table = ttk.Treeview(
            table_frame,
            columns=("name", "phone"),
            show="headings",
        )

        self.contact_table.heading(
            "name",
            text="Name",
        )

        self.contact_table.heading(
            "phone",
            text="Phone Number",
        )

        self.contact_table.column(
            "name",
            width=300,
            anchor="w",
        )

        self.contact_table.column(
            "phone",
            width=220,
            anchor="w",
        )

        table_scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.contact_table.yview,
        )

        self.contact_table.configure(
            yscrollcommand=table_scrollbar.set
        )

        self.contact_table.grid(
            row=0,
            column=0,
            sticky="nsew",
        )

        table_scrollbar.grid(
            row=0,
            column=1,
            sticky="ns",
        )

        footer = ttk.Frame(self)
        footer.grid(
            row=3,
            column=0,
            sticky="ew",
            pady=(12, 0),
        )

        footer.columnconfigure(0, weight=1)

        summary_label = ttk.Label(
            footer,
            textvariable=self.summary_var,
        )

        summary_label.grid(
            row=0,
            column=0,
            sticky="w",
        )

        continue_button = ttk.Button(
            footer,
            text="Prepare Message",
            command=self._prepare_message,
        )

        continue_button.grid(
            row=0,
            column=1,
        )

        self.prepare_message_button = (
            continue_button
        )

        self._update_continue_button(
            contacts=[]
        )

    def _select_csv(self) -> None:
        """Open the CSV file selection dialog."""
        file_path = filedialog.askopenfilename(
            title="Select Google Contacts CSV",
            filetypes=[
                ("CSV files", "*.csv"),
                ("All files", "*.*"),
            ],
        )

        if not file_path:
            return

        self._import_csv(
            Path(file_path)
        )

    def _import_csv(
        self,
        file_path: Path,
    ) -> None:
        """Import contacts from the selected CSV file."""
        self._set_status(
            f"Importing {file_path.name}..."
        )

        try:
            result = self.csv_service.import_contacts(
                file_path
            )

            self._display_result(
                file_path,
                result,
            )

            if self.contacts_callback:
                self.contacts_callback(
                    result.contacts
                )

            self._set_status(
                f"Imported {result.imported_count} contacts"
            )

            if result.skipped_count:
                self._show_skipped_rows(
                    result
                )

        except (
            FileNotFoundError,
            ValueError,
        ) as error:
            self._set_status(
                "Import failed"
            )

            messagebox.showerror(
                "CSV Import Error",
                str(error),
            )

        except OSError as error:
            self._set_status(
                "Import failed"
            )

            messagebox.showerror(
                "File Error",
                str(error),
            )

    def _display_result(
        self,
        file_path: Path,
        result: ContactImportResult,
    ) -> None:
        """Display imported contacts and summary."""
        self.selected_file_var.set(
            str(file_path)
        )

        self._clear_contact_table()

        for contact in result.contacts:
            self.contact_table.insert(
                "",
                "end",
                values=(
                    contact.name,
                    contact.phone_number,
                ),
            )

        self.summary_var.set(
            f"Imported: {result.imported_count} | "
            f"Skipped: {result.skipped_count}"
        )

        self._update_continue_button(
            result.contacts
        )

    def _clear_contact_table(self) -> None:
        """Remove all rows from the contact table."""
        for item in self.contact_table.get_children():
            self.contact_table.delete(item)

    def _show_skipped_rows(
        self,
        result: ContactImportResult,
    ) -> None:
        """Display skipped-row information."""
        details = "\n".join(
            result.skipped_rows
        )

        messagebox.showwarning(
            "Import Completed with Skipped Rows",
            (
                f"{result.skipped_count} row(s) "
                "were skipped.\n\n"
                f"{details}"
            ),
        )

    def _prepare_message(self) -> None:
        """Notify the parent that contacts are ready."""
        if not self.contacts_callback:
            return

        contacts = [
            self._get_contact_from_table(
                item
            )
            for item in self.contact_table.get_children()
        ]

        contacts = [
            contact
            for contact in contacts
            if contact is not None
        ]

        if not contacts:
            messagebox.showwarning(
                "No Contacts",
                "Import at least one contact first.",
            )
            return

        self.contacts_callback(
            contacts
        )

        self._set_status(
            "Contacts ready for message preparation."
        )

    def _get_contact_from_table(
        self,
        item_id: str,
    ) -> Contact | None:
        """Create a Contact from a table row."""
        values = self.contact_table.item(
            item_id,
            "values",
        )

        if len(values) < 2:
            return None

        return Contact(
            name=str(values[0]),
            phone_number=str(values[1]),
        )

    def _update_continue_button(
        self,
        contacts: list[Contact],
    ) -> None:
        """Enable or disable the message preparation button."""
        if contacts:
            self.prepare_message_button.state(
                ["!disabled"]
            )
        else:
            self.prepare_message_button.state(
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
    "CSVImportPanel",
]