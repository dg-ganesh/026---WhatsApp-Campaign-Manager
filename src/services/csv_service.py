"""
Project : WhatsApp Campaign Manager
Project ID : 026

CSV Contact Import Service
"""

import csv
from dataclasses import dataclass
from pathlib import Path

from src.config import (
    CSV_DELIMITER,
    DEFAULT_ENCODING,
    GOOGLE_FIRST_NAME_COLUMN,
    GOOGLE_LAST_NAME_COLUMN,
    GOOGLE_MIDDLE_NAME_COLUMN,
    GOOGLE_PHONE_VALUE_COLUMN,
)
from src.models.contact_model import Contact


@dataclass(slots=True)
class ContactImportResult:
    """Contains the result of importing contacts from a CSV file."""

    contacts: list[Contact]
    skipped_rows: list[str]

    @property
    def imported_count(self) -> int:
        """Return the number of successfully imported contacts."""
        return len(self.contacts)

    @property
    def skipped_count(self) -> int:
        """Return the number of skipped rows."""
        return len(self.skipped_rows)


class CSVService:
    """Reads contacts from a Google Contacts CSV export."""

    def import_contacts(
        self,
        file_path: str | Path,
    ) -> ContactImportResult:
        """
        Import contacts from a Google Contacts CSV file.

        A contact requires:
        - A name from the Google Contacts name fields.
        - A value in 'Phone 1 - Value'.

        Rows missing either required value are skipped.
        Phone values are preserved exactly as supplied by the CSV.
        """
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(
                f"CSV file was not found: {path}"
            )

        if not path.is_file():
            raise ValueError(
                f"CSV path is not a file: {path}"
            )

        with path.open(
            mode="r",
            encoding=DEFAULT_ENCODING,
            newline="",
        ) as csv_file:
            reader = csv.DictReader(
                csv_file,
                delimiter=CSV_DELIMITER,
            )

            if not reader.fieldnames:
                raise ValueError(
                    "The CSV file does not contain a header row."
                )

            self._validate_google_contacts_columns(
                reader.fieldnames
            )

            contacts: list[Contact] = []
            skipped_rows: list[str] = []

            for row_number, row in enumerate(
                reader,
                start=2,
            ):
                name = self._build_contact_name(row)

                phone_number = self._get_value(
                    row,
                    GOOGLE_PHONE_VALUE_COLUMN,
                )

                if not name:
                    skipped_rows.append(
                        f"Row {row_number}: Missing contact name"
                    )
                    continue

                if not phone_number:
                    skipped_rows.append(
                        f"Row {row_number}: Missing phone number"
                    )
                    continue

                contacts.append(
                    Contact(
                        name=name,
                        phone_number=phone_number,
                        source_row=row_number,
                    )
                )

        return ContactImportResult(
            contacts=contacts,
            skipped_rows=skipped_rows,
        )

    @staticmethod
    def _validate_google_contacts_columns(
        fieldnames: list[str],
    ) -> None:
        """Verify the required Google Contacts columns exist."""
        required_columns = (
            GOOGLE_FIRST_NAME_COLUMN,
            GOOGLE_MIDDLE_NAME_COLUMN,
            GOOGLE_LAST_NAME_COLUMN,
            GOOGLE_PHONE_VALUE_COLUMN,
        )

        missing_columns = [
            column
            for column in required_columns
            if column not in fieldnames
        ]

        if missing_columns:
            missing = ", ".join(missing_columns)

            raise ValueError(
                "The selected CSV does not appear to be a "
                "Google Contacts export. Missing column(s): "
                f"{missing}"
            )

    @staticmethod
    def _build_contact_name(
        row: dict[str, str | None],
    ) -> str:
        """Build the contact name from Google Contacts name fields."""
        name_parts = (
            CSVService._get_value(
                row,
                GOOGLE_FIRST_NAME_COLUMN,
            ),
            CSVService._get_value(
                row,
                GOOGLE_MIDDLE_NAME_COLUMN,
            ),
            CSVService._get_value(
                row,
                GOOGLE_LAST_NAME_COLUMN,
            ),
        )

        return " ".join(
            part
            for part in name_parts
            if part
        )

    @staticmethod
    def _get_value(
        row: dict[str, str | None],
        column: str,
    ) -> str:
        """
        Return the CSV value without changing its content.

        Leading/trailing whitespace is removed, but the actual
        phone representation is otherwise preserved.
        """
        value = row.get(column)

        if value is None:
            return ""

        return value.strip()


__all__ = [
    "CSVService",
    "ContactImportResult",
]