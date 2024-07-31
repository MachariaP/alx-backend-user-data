#!/usr/bin/env python3

"""Create logger
"""

import logging
import re
from typing import List, Tuple


def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """
    Obfuscate specified fields in a log message.

    Args:
        fields (list): List of strings representing fields to obfuscate.
        redaction (str): String to replace the field values with.
        message (str): The log message to be obfuscated.
        separator (str): Character separating the fields in the log message.

    Returns:
        str: The obfuscated log message.
    """
    pattern = f"({'|'.join(fields)})=[^{separator}]*"
    return re.sub(pattern, lambda m: f"{m.group(1)}={redaction}", message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        original_message = super().format(record)
        return filter_datum(self.fields, self.REDACTION, original_message, self.SEPARATOR)


# Define PII_FIELDS
PII_FIELDS: Tuple[str, ...] = ("name", "email", "phone", "ssn", "password")


def get_logger() -> logging.Logger:
    """
    Creates and returns a logger named "user_data" with specific configurations.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(fields=PII_FIELDS)
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)

    return logger
