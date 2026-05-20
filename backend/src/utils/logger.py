"""JSON logger for test execution."""

import json
import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any


class TestLogger:
    """JSON logger for test steps and errors."""

    def __init__(self) -> None:
        self.current_test = "unknown"
        self.logs: list[dict[str, Any]] = []
        self._setup_files()

    def _setup_files(self) -> None:
        """Create log directories and archive old latest.log."""
        logs_dir = Path("logs")
        archive_dir = logs_dir / "archive"
        archive_dir.mkdir(parents=True, exist_ok=True)

        latest = logs_dir / "latest.json"
        if latest.exists():
            timestamp = datetime.now().astimezone().strftime("%Y-%m-%d_%H-%M-%S")
            archive_path = archive_dir / f"{timestamp}.json"
            shutil.move(str(latest), str(archive_path))
            TestLogger._cleanup_old_archives(archive_dir)

        self.log_file = latest

    @staticmethod
    def _cleanup_old_archives(archive_dir: Path) -> None:
        """Keep only last 10 archive files."""
        archives = sorted(archive_dir.glob("*.json"), key=os.path.getmtime)
        for old in archives[:-10]:
            old.unlink()

    def set_test(self, test_name: str) -> None:
        """Set current test name for subsequent log entries."""
        self.current_test = test_name

    def log(self, level: str, step: str, message: str, data: dict[str, Any] | None = None) -> None:
        """Add log entry."""
        entry: dict[str, Any] = {
            "timestamp": datetime.now().astimezone().isoformat(),
            "level": level,
            "test": self.current_test,  # ← используем current_test
            "step": step,
            "message": message,
        }
        if data:
            entry["data"] = data
        self.logs.append(entry)

    def info(self, step: str, message: str, data: dict[str, Any] | None = None) -> None:
        """Log INFO level."""
        self.log("INFO", step, message, data)

    def error(self, step: str, message: str, data: dict[str, Any] | None = None) -> None:
        """Log ERROR level."""
        self.log("ERROR", step, message, data)

    def save(self) -> str:
        """Save logs to file and return content."""
        content = json.dumps(self.logs, indent=2, ensure_ascii=False)
        self.log_file.write_text(content, encoding="utf-8")
        return content

    def clear(self) -> None:
        """Clear in-memory logs."""
        self.logs = []
