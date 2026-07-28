from __future__ import annotations

import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from invoke import Context
from invoke.exceptions import Failure

BASE_DIR = Path(__file__).parent.parent.resolve()
VENV_DIR = BASE_DIR / "backend" / ".venv"

load_dotenv(BASE_DIR / ".env")


GREEN = "\033[92m"
BOLD = "\033[1m"
RESET = "\033[0m"


def info(message: str) -> None:
    """
    Pretty print a message.
    """
    print(f"{BOLD}INFO:{RESET} {message}")


def print_success(message: str) -> None:
    """
    Pretty print a success message.
    """
    print(f"{GREEN}{BOLD}SUCCESS:{RESET} {GREEN}{message}{RESET}")


def run_command(c: Context, command: str, quiet_stdout: bool = False) -> None:
    """
    Run a command, optionally suppressing normal output.
    """
    if quiet_stdout:
        result = c.run(command, hide=True, warn=True)

        # Only show stderr when the command failed
        if result.exited != 0:
            sys.stderr.write(result.stderr or "")
            raise Failure(result)

    else:
        c.run(command)


def uv_run(c: Context, command: str, quiet_stdout: bool = False) -> None:
    """
    Run a UV command.
    """
    run_command(c, f"uv run {command}", quiet_stdout)


def django_run(c: Context, command: str, quiet_stdout: bool = False) -> None:
    """
    Run a Django command.
    """
    with c.cd(BASE_DIR / "backend"):
        uv_run(c, f"python manage.py {command}", quiet_stdout)


def npx_run(c: Context, command: str, quiet_stdout: bool = False) -> None:
    """
    Run a Node command.
    """
    with c.cd(BASE_DIR / "frontend"):
        run_command(c, f"npx {command}", quiet_stdout)


def get_bool_env(name: str, default: bool = False) -> bool:
    """
    Get a boolean environment variable.
    """
    value = os.getenv(name, str(default)).lower()

    if value not in {"true", "false"}:
        raise ValueError(f"{name} must be 'true' or 'false', got {value!r}")

    return value == "true"


IS_DEBUG = get_bool_env("DEBUG")
