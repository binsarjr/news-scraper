import os
import dateparser
from datetime import datetime

import sys

import re


def base_path(path: str):
    """
    Memngambil dan menggabungkan file dari base root path
    """
    return os.path.join(os.path.dirname(__file__), path)


def clear_console():
    os.system("cls" if os.name == "nt" else "clear")


def is_valid_datetime(input_str, format_str="%Y-%m-%d %H:%M:%S"):
    try:
        datetime.strptime(input_str, format_str)
        return True
    except ValueError:
        return False


def indo_to_datetime(date: str, format="%A, %d %B %Y %H:%M %Z"):
    return dateparser.parse(
        date,
        date_formats=[format],
        languages=["id"],
        settings={"TIMEZONE": "Asia/Jakarta"},
    ).strftime("%Y-%m-%d %H:%M:%S")


def string_to_datetime(text: str):
    return dateparser.parse(
        text,
        languages=["en"],
        settings={"TIMEZONE": "Asia/Jakarta"},
    )
