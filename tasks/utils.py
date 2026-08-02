"""
Invoke utility functions and configuration helpers for project automation tasks.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from invoke import Context
from invoke.exceptions import Failure
from rich.console import Console

BASE_DIR = Path(__file__).parent.parent.resolve()
VENV_DIR = BASE_DIR / ".venv"

load_dotenv(BASE_DIR / ".env")


# Rich console handles terminal output, colors, and formatting.
# It automatically detects terminal capabilities and falls back gracefully.
console = Console()


def info(message: str) -> None:
    """
    Pretty print an informational message.
    """
    console.print(f"[bold]INFO[/bold] {message}")


def print_success(message: str) -> None:
    """
    Pretty print a success message.
    """
    console.print(f"[bold green]SUCCESS[/bold green] {message}")


def print_error(message: str) -> None:
    """
    Pretty print an error message.
    """
    console.print(f"[bold red]ERROR[/bold red] {message}")


def run_command(c: Context, command: str, quiet_stdout: bool = False) -> None:
    """
    Run a command, optionally suppressing normal output.
    """
    if quiet_stdout:
        result = c.run(command, hide=True, warn=True)

        # Only show stderr when the command failed.
        if result.exited != 0:
            sys.stderr.write(result.stderr or "")
            raise Failure(result)

    else:
        c.run(command)


def venv_run(c: Context, command: str, quiet_stdout: bool = False) -> None:
    """
    Run a command from the project virtual environment.
    """
    executable, *args = command.split(" ")

    executable_path = VENV_DIR / "bin" / executable

    if executable_path.exists():
        command = f'"{executable_path}" {" ".join(args)}'

    run_command(c, command, quiet_stdout)


def django_run(c: Context, command: str, quiet_stdout: bool = False) -> None:
    """
    Run a Django command.
    """
    with c.cd(BASE_DIR / "backend"):
        venv_run(c, f"python manage.py {command}", quiet_stdout)


def npx_run(c: Context, command: str, quiet_stdout: bool = False) -> None:
    """
    Run a Node command with npx.
    """
    with c.cd(BASE_DIR / "frontend"):
        run_command(c, f"npx {command}", quiet_stdout)


def npm_run(c: Context, command: str, quiet_stdout: bool = False) -> None:
    """
    Run a Node command with npm.
    """
    with c.cd(BASE_DIR / "frontend"):
        run_command(c, f"npm {command}", quiet_stdout)


def get_bool_env(name: str, default: bool = False) -> bool:
    """
    Get a boolean environment variable.
    """
    value = os.getenv(name, str(default)).lower()

    if value not in {"true", "false"}:
        raise ValueError(f"{name} must be 'true' or 'false', got {value!r}")

    return value == "true"


IS_DEBUG = get_bool_env("DEBUG")
