"""
Central logging module.
"""

from __future__ import annotations

import logging
from pathlib import Path


LOGGER_NAME = "PAF"


def get_logger(
    log_file: str = "logs/paf.log",
) -> logging.Logger:
    """
    Returns configured logger.
    """

    logger = logging.getLogger(LOGGER_NAME)

    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    BASE_DIR = Path(__file__).resolve().parent.parent

    log_file = BASE_DIR / log_file

    log_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    file_handler = logging.FileHandler(
        log_file,
        encoding="utf-8",
    )

    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()

    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
