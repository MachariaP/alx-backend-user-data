#!/usr/bin/env python3

"""Regex-ing
"""

import re


def filter_datum(fields, redaction, message, separator):
    """
    obfuscate specified fields in a log message.

    Args:
        fields (list): List of strings representing fields of obfuscate.
        redaction (str): String to replace the field value with.
        message (str): The log message to be obfuscated.
        separator (str): Character separating the fields in the log message.

    Returns:
        str: The obfuscated log message.
    """
    pattern = f"({'|'.join(fields)})=[^{separator}]*"
    return re.sub(pattern, lambda m: f"{m.group(1)}={redaction}", message)
