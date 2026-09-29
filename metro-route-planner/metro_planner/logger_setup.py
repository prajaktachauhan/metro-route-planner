"""Logging configuration.

Logs go to logs/metro_planner.log so the console stays clean for the user.
If the log file cannot be created the program still runs (reliability).
"""

import logging

from .config import LOG_DIR, LOG_FILE, LOG_LEVEL


def setup_logging():
    """Configure the root logger once; safe to call repeatedly."""
    root = logging.getLogger()
    if any(getattr(h, "_metro_handler", False) for h in root.handlers):
        return
    root.setLevel(LOG_LEVEL)
    try:
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    except OSError:
        handler = logging.NullHandler()
    handler._metro_handler = True
    handler.setFormatter(logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"))
    root.addHandler(handler)
