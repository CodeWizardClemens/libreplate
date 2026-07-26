from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from invoke import Context

# Invoke does not print commands by default.
# Override run so commands are visible during execution.
_original_run = Context.run


def run_and_print(self, command, *args, **kwargs):
    print(f"$ {command}")
    return _original_run(self, command, *args, **kwargs)


Context.run = run_and_print


BASE_DIR = Path(__file__).parent.parent.resolve()
VENV_DIR = BASE_DIR / "backend" / ".venv"

load_dotenv(BASE_DIR / ".env")


def django_run(c: Context, command: str) -> None:
    """
    Run a Django management command.
    """
    c.run(f"uv run python manage.py {command}")


def log(message: str) -> None:
    """
    Pretty print a message.
    """
    print(f"\n==> {message}")


def get_bool_env(name: str, default: bool = False) -> bool:
    """
    Get a boolean environment variable.
    """
    value = os.getenv(name, str(default)).lower()

    if value not in {"true", "false"}:
        raise ValueError(
            f"{name} must be 'true' or 'false', got {value!r}"
        )

    return value == "true"


IS_DEBUG = get_bool_env("DEBUG")