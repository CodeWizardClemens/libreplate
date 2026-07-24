"""
Invoke tasks for managing the LibrePlate application.

Provides automation commands for updates, installs code quality checks,
database migrations etc.

Commands are executed through Invoke, for example:

    inv install
    inv test
    inv format-code
    inv serve

For a complete list of available commands and options, run:

    invoke --list
"""

from __future__ import annotations

import os
import shlex
from pathlib import Path

from dotenv import load_dotenv
from invoke import Context, task

# Invoke does not print the commands that are being executed. This
# makes debugging difficult. For this reason the default run function is
# overwritten.
_original_run = Context.run


def run_and_print(self, command, *args, **kwargs):
    print(f"$ {command}")
    return _original_run(self, command, *args, **kwargs)


Context.run = run_and_print

BASE_DIR = Path(__file__).parent.resolve()
VENV_DIR = BASE_DIR / ".venv"

# .env file is located in the root LibrePlate directory.
load_dotenv(BASE_DIR.parent / ".env")


def django_run(c: Context, command: str) -> None:
    """
    Run a Django management command.
    """
    c.run(f"uv run python manage.py {command}")


def log(message: str) -> None:
    """
    Pretify printing a message to the user.
    """
    print(f"\n==> {message}")


def get_bool_env(name: str, default: bool = False) -> bool:
    """
    Helper function to get a boolean value from the environment variables.
    """
    value = os.getenv(name, str(default)).lower()

    if value not in {"true", "false"}:
        raise ValueError(f"{name} must be 'true' or 'false', got {value!r}")

    return value == "true"


IS_RELEASE = get_bool_env("RELEASE")


@task
def check_code_quality(c: Context):
    """
    Run code quality checks like import sorting, formatting, and linting.
    """
    log("Checking code quality. This may take a while.")
    # TODO linters for css/js/html files.
    c.run(f"isort {BASE_DIR} --check-only --skip {VENV_DIR}")
    c.run(f"black {BASE_DIR} --check --exclude '{VENV_DIR}'")
    c.run(f"ruff check {BASE_DIR} --exclude {VENV_DIR}")
    # TODO needs more configuration
    # c.run(f"bandit -r {BASE_DIR} -x {VENV_DIR}")


@task
def format_code(c: Context):
    """
    Automatically format the codebase.
    """
    # TODO formatters for css/js/html files.
    c.run(f"isort {BASE_DIR} --skip {VENV_DIR}")
    c.run(f"black {BASE_DIR} --exclude '{VENV_DIR}'")
    c.run(f"ruff format {BASE_DIR} --exclude {VENV_DIR}")


@task
def migrate(c: Context):
    """
    Create new Django migrations and apply pending database migrations.
    """
    log("Creating and applying migrations")
    django_run(c, "makemigrations")
    django_run(c, "migrate")


@task
def collectstatic(c: Context):
    """
    Collect Django static files for deployment.
    """
    log("Collecting static files")
    django_run(c, "collectstatic --noinput")


@task
def update(c: Context):
    """
    Update LibrePlate dependencies, source code, and database state.
    """
    log("Updating LibrePlate")
    c.run("git pull origin master")
    c.run("uv sync")
    migrate(c)
    collectstatic(c)


@task
def sync_default_data(c: Context):
    """
    Synchronize default application data.
    """
    log("Syncing default data")

    for sync_command in ["sync_nutrients", "sync_units", "sync_body_metrics"]:
        django_run(c, sync_command)


@task
def add_user(
    c: Context,
    username: str,
    first_name: str,
    last_name: str,
    email: str,
    password: str,
):
    """
    Create a new LibrePlate user account.

    Arguments are forwarded to the Django management command for validation.
    So use simple strings in this command.
    """
    log(f"Adding new user `{username}`")

    django_run(
        c,
        "add_user "
        f"{shlex.quote(username)} "
        f"{shlex.quote(first_name)} "
        f"{shlex.quote(last_name)} "
        f"{shlex.quote(email)} "
        f"{shlex.quote(password)}",
    )


@task
def remove_user(c: Context, username):
    """
    Remove an existing LibrePlate user account.
    """
    log(f"Removing user `{username}`")
    django_run(c, f'remove_user "{username}"')


@task
def add_usda_api_key(c: Context, key):
    """
    Configure the USDA API key used for food data integration.

    Stores the provided API key so LibrePlate can access USDA food information.
    """
    log("Add a USDA API key")
    django_run(c, f"add_usda_api_key {key}")


@task
def serve(c: Context):
    """
    Start the LibrePlate web server.

    In development mode, this starts Django's built-in development server.

    In release mode, this starts the production WSGI server using Gunicorn.
    Gunicorn is intended to run behind a reverse proxy (e.g. nginx or
    another frontend proxy) which handles external HTTP traffic.
    """
    log("Running server")

    if IS_RELEASE:
        # TODO allow for gunicorn config to be passed as argument.
        c.run("uv run gunicorn libreplate.wsgi:application")
    else:
        django_run(c, "runserver")


@task
def test(c: Context):
    """
    Run the LibrePlate automated test suite.
    """
    log("Running tests")
    django_run(c, "test")


@task
def init(c: Context):
    """
    Initialize LibrePlate.
    """
    log("Installing libreplate")

    migrate(c)

    if IS_RELEASE:
        collectstatic(c)

    sync_default_data(c)
