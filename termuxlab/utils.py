import os
import sys
from datetime import datetime


def clear_screen():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def format_timestamp(ts=None):
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S") if ts is None else ts


def input_safe(prompt):
    try:
        return input(prompt)
    except (KeyboardInterrupt, EOFError):
        print("\nInterrupted. Returning to menu.")
        return ""


def yes_no(prompt):
    answer = input_safe(f"{prompt} [y/N]: ").strip().lower()
    return answer in ("y", "yes")


def ensure_directory(path):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
