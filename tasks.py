"""
Invoke tasks for managing the LibrePlate application.

Provides automation commands code quality checks, database migrations etc.

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
from invoke import task

load_dotenv()

BASE_DIR = Path(__file__).parent.resolve()
VENV_DIR = BASE_DIR / ".venv"
DJANGO_CMD = "uv run python manage.py"


def log(message: str):
    print(f"\n==> {message}")


IS_RELEASE = (lambda v: {"True": True, "False": False}[v])(
    os.getenv("RELEASE", "False")
)


@task
def check_code_quality(c):
    """
    Run code quality checks like import sorting, formatting, and linting.
    """
    # TODO linters for css/js/html files.
    c.run(f"isort {BASE_DIR} --check-only --skip {VENV_DIR}")
    c.run(f"black {BASE_DIR} --check --exclude '{VENV_DIR}'")
    c.run(f"ruff check {BASE_DIR} --exclude {VENV_DIR}")
    # TODO needs more configuration
    # c.run(f"bandit -r {BASE_DIR} -x {VENV_DIR}")


@task
def format_code(c):
    """
    Automatically format the codebase.
    """
    # TODO formatters for css/js/html files.
    c.run(f"isort {BASE_DIR} --skip {VENV_DIR}")
    c.run(f"black {BASE_DIR} --exclude '{VENV_DIR}'")
    c.run(f"ruff format {BASE_DIR} --exclude {VENV_DIR}")


@task
def migrate(c):
    """
    Create new Django migrations and apply pending database migrations.
    """
    log("Creating and applying migrations")
    c.run(f"{DJANGO_CMD} makemigrations")
    c.run(f"{DJANGO_CMD} migrate")


@task
def collectstatic(c):
    """
    Collect Django static files for deployment.
    """
    log("Collecting static files")
    c.run(f"{DJANGO_CMD} collectstatic --noinput")


@task
def update(c):
    """
    Update LibrePlate dependencies, source code, and database state.
    """
    log("Updating LibrePlate")
    c.run("uv sync")
    c.run("git pull origin master")
    migrate(c)
    collectstatic(c)


@task
def sync_default_data(c):
    """
    Synchronize default application data.
    """
    log("Syncing default data")

    for sync_command in ["sync_nutrients", "sync_units", "sync_body_metrics"]:
        c.run(f"{DJANGO_CMD} {sync_command}")


@task
def add_user(c, username, first_name, last_name, email, password):
    """
    Create a new LibrePlate user account.
    """
    log(f"Adding new user `{username}`")
    c.run(
        f"{DJANGO_CMD} add_user "
        f"{shlex.quote(username)} "
        f"{shlex.quote(first_name)} "
        f"{shlex.quote(last_name)} "
        f"{shlex.quote(email)} "
        f"{shlex.quote(password)}"
    )


@task
def remove_user(c, username):
    """
    Remove an existing LibrePlate user account.
    """
    log(f"Removing user `{username}`")
    c.run(f'{DJANGO_CMD} remove_user "{username}"')


@task
def add_usda_api_key(c, key):
    """
    Configure the USDA API key used for food data integration.

    Stores the provided API key so LibrePlate can access USDA food information.
    """
    log("Add a USDA API key")
    c.run(f"{DJANGO_CMD} add_usda_api_key {key}")


@task
def serve(c):
    """
    Start the LibrePlate web server.
    """
    log("Running server")
    if IS_RELEASE():
        c.run("uv run gunicorn libreplate.wsgi:application")
    else:
        c.run(f"{DJANGO_CMD} runserver")


@task
def test(c):
    """
    Run the LibrePlate automated test suite.
    """
    log("Running tests")
    c.run(f"{DJANGO_CMD} test")


@task
def init(c):
    """
    Install and initialize LibrePlate.
    """

    log("Installing libreplate")

    migrate(c)

    if IS_RELEASE():
        collectstatic(c)

    sync_default_data(c)
