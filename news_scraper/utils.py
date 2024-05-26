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


def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
            It must be "yes" (the default), "no" or None (meaning
            an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == "":
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' " "(or 'y' or 'n').\n")
