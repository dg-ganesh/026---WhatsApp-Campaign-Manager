"""
Project : WhatsApp Campaign Manager
Project ID : 026

Application Entry Point
"""

import tkinter as tk

from src.config import (
    APP_NAME,
    initialize_directories,
)
from src.services.logging_service import LoggingService
from src.ui.main_window import MainWindow


def main() -> None:
    """Initialize and start the application."""
    initialize_directories()

    logging_service = LoggingService()

    logging_service.log(
        f"{APP_NAME} application starting."
    )

    logging_service.checkpoint(
        "APPLICATION_INITIALIZATION",
        "PASS",
    )

    root = tk.Tk()

    main_window = MainWindow(root)

    logging_service.checkpoint(
        "MAIN_WINDOW_INITIALIZATION",
        "PASS",
    )

    logging_service.log(
        f"{APP_NAME} application ready."
    )

    try:
        root.mainloop()

        logging_service.checkpoint(
            "APPLICATION_SESSION_COMPLETE",
            "PASS",
        )

        logging_service.write_execution_report(
            status="PASS",
            last_successful_checkpoint=(
                "APPLICATION_SESSION_COMPLETE"
            ),
        )

    except Exception as error:
        logging_service.error(
            str(error)
        )

        logging_service.write_execution_report(
            status="FAIL",
            last_successful_checkpoint=(
                "MAIN_WINDOW_INITIALIZATION"
            ),
            error_message=str(error),
        )

        raise


if __name__ == "__main__":
    main()