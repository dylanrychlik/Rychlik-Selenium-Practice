"""Central logging configuration for test framework."""

from __future__ import annotations

import logging
from pathlib import Path


def configure_logger(log_level: int = logging.INFO) -> None:
    """Configure root logger for console + file output."""
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)

    logging.basicConfig(
        level=log_level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(logs_dir / "test_run.log", encoding="utf-8"),
        ],
        force=True,
    )
