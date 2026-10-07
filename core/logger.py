"""
📝 Premium Logger
Colored console + file logging
"""

import logging
import sys
import time
from pathlib import Path
from core.colors import C


class PremiumFormatter(logging.Formatter):
    """Pretty formatter with colors and icons."""

    ICONS = {
        "DEBUG": "🔍",
        "INFO": "ℹ️ ",
        "WARNING": "⚠️ ",
        "ERROR": "❌",
        "CRITICAL": "🚨",
    }

    COLORS = {
        "DEBUG": C.DIM + C.WHITE,
        "INFO": C.BRIGHT_CYAN,
        "WARNING": C.BRIGHT_YELLOW,
        "ERROR": C.BRIGHT_RED,
        "CRITICAL": C.BG_RED + C.BRIGHT_WHITE,
    }

    def format(self, record):
        icon = self.ICONS.get(record.levelname, "•")
        color = self.COLORS.get(record.levelname, "")
        time_str = time.strftime("%H:%M:%S", time.localtime(record.created))

        return (
            f"{C.DIM}[{time_str}]{C.RESET} "
            f"{color}{icon} {record.getMessage()}{C.RESET}"
        )


def setup_logger(name="rotator", log_file="logs/rotator.log"):
    """Setup premium logger."""

    Path("logs").mkdir(exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.handlers.clear()

    # Console handler (colored)
    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(PremiumFormatter())
    logger.addHandler(console)

    # File handler (plain)
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    )
    logger.addHandler(file_handler)

    return logger


log = setup_logger()
