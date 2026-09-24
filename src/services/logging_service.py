"""
Project : WhatsApp Campaign Manager
Project ID : 026

Application Logging Service
"""

from datetime import datetime
from pathlib import Path

from src.config import (
    APPLICATION_LOG_PATH,
    EXECUTION_REPORT_PATH,
    APP_VERSION,
    initialize_directories,
)


class LoggingService:
    """Provides application logging and execution reporting."""

    def __init__(
        self,
        application_log_path: Path = APPLICATION_LOG_PATH,
        execution_report_path: Path = EXECUTION_REPORT_PATH,
    ) -> None:
        initialize_directories()

        self.application_log_path = application_log_path
        self.execution_report_path = execution_report_path

        self._start_time = datetime.now()

    def log(self, message: str) -> None:
        """Write a timestamped message to the application log."""
        timestamp = self._timestamp()

        with self.application_log_path.open(
            mode="a",
            encoding="utf-8",
        ) as log_file:
            log_file.write(
                f"{timestamp} | {message}\n"
            )

    def checkpoint(
        self,
        checkpoint_name: str,
        status: str = "PASS",
        details: str = "",
    ) -> None:
        """Record an execution checkpoint."""
        message = (
            f"CHECKPOINT | {checkpoint_name} | "
            f"{status}"
        )

        if details:
            message += f" | {details}"

        self.log(message)

    def error(
        self,
        message: str,
    ) -> None:
        """Record an application error."""
        self.log(f"ERROR | {message}")

    def write_execution_report(
        self,
        status: str,
        last_successful_checkpoint: str,
        error_message: str = "",
    ) -> None:
        """Write the current application execution report."""
        end_time = datetime.now()
        duration = end_time - self._start_time

        report_lines = [
            "WhatsApp Campaign Manager",
            f"Project ID: 026",
            f"Application Version: {APP_VERSION}",
            "",
            f"Start Time: {self._start_time.isoformat(timespec='seconds')}",
            f"End Time: {end_time.isoformat(timespec='seconds')}",
            f"Duration: {duration}",
            "",
            f"Status: {status}",
            (
                "Last Successful Checkpoint: "
                f"{last_successful_checkpoint}"
            ),
        ]

        if error_message:
            report_lines.extend(
                [
                    "",
                    f"Error: {error_message}",
                ]
            )

        with self.execution_report_path.open(
            mode="w",
            encoding="utf-8",
        ) as report_file:
            report_file.write(
                "\n".join(report_lines)
                + "\n"
            )

    @staticmethod
    def _timestamp() -> str:
        """Return the current timestamp for log entries."""
        return datetime.now().isoformat(
            timespec="seconds"
        )


__all__ = [
    "LoggingService",
]