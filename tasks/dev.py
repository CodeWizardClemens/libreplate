"""
Invoke tasks for project development workflows.

This module provides command-line tasks for maintaining the LibrePlate codebase,
including:

- Running code quality checks
- Automatically formatting source code
- Running the Django test suite
- Starting the development or production web server
"""

import shlex

from invoke import Context, task

from .utils import (
    BASE_DIR,
    VENV_DIR,
    django_run,
    info,
    npm_run,
    npx_run,
    print_success,
    uv_run,
)


def isort_cmd(check_only: bool = False) -> str:
    args = [
        "isort",
        str(BASE_DIR),
        "--skip",
        str(VENV_DIR),
        "--settings-path",
        "backend/pyproject.toml",
    ]

    if check_only:
        args.insert(2, "--check-only")

    return " ".join(args)


def black_cmd() -> str:
    return f"black {BASE_DIR} --check --exclude '(/\\.venv/)'"


def ruff_check_cmd(fix: bool = False, exit_zero: bool = False) -> str:
    args = [
        "ruff",
        "check",
        str(BASE_DIR),
        "--exclude",
        str(VENV_DIR),
    ]

    if fix:
        args.append("--fix")

    if exit_zero:
        args.append("--exit-zero")

    return " ".join(args)


@task(help={"verbose": "Show stdout output from commands."})
def verify(c: Context, verbose: bool = False) -> None:
    """
    Run all code quality checks and tests.
    """

    check(c, verbose)
    test(c, verbose)


@task()
def user_add_dummy(c: Context):
    """
    Create a dummy LibrePlate user account.
    """
    username = "dummy"
    first_name = "Dummy"
    last_name = "User"
    email = "dummy@example.com"
    password = "dummy"

    info(f"Adding dummy user `{username}`")

    django_run(
        c,
        "add_user "
        f"{shlex.quote(username)} "
        f"{shlex.quote(first_name)} "
        f"{shlex.quote(last_name)} "
        f"{shlex.quote(email)} "
        f"{shlex.quote(password)} "
        "--skip-password-validation",
    )


@task(help={"verbose": "Show stdout output from commands."})
def check(c: Context, verbose: bool = False) -> None:
    """
    Run code quality checks.
    """

    if verbose:
        info("Checking code quality. This may take a while.")

    uv_run(c, isort_cmd(check_only=True), quiet_stdout=not verbose)
    uv_run(c, black_cmd(), quiet_stdout=not verbose)
    uv_run(c, ruff_check_cmd(fix=True), quiet_stdout=not verbose)
    npx_run(c, "oxlint .", quiet_stdout=not verbose)
    npx_run(
        c,
        f"prettier --check . --ignore-path {BASE_DIR / 'frontend/.prettierignore'}",
        quiet_stdout=not verbose,
    )

    print_success(message="Succesfully ran all code checks")


@task(help={"verbose": "Show stdout output from commands."})
def format(c: Context, verbose: bool = False) -> None:
    """
    Automatically format the codebase.
    """

    if verbose:
        info("Formatting codebase.")

    npx_run(
        c,
        f"prettier --write . --ignore-path {BASE_DIR / 'frontend/.prettierignore'}",
        quiet_stdout=not verbose,
    )
    uv_run(c, isort_cmd(), quiet_stdout=not verbose)
    uv_run(c, black_cmd().replace("--check", ""), quiet_stdout=not verbose)
    uv_run(c, f"ruff format {BASE_DIR} --exclude {VENV_DIR}", quiet_stdout=not verbose)
    uv_run(c, ruff_check_cmd(fix=True, exit_zero=True), quiet_stdout=not verbose)

    print_success(message="Succesfully ran all formatters")


@task(help={"verbose": "Show stdout output from commands."})
def test(c: Context, verbose: bool = False) -> None:
    """
    Run the LibrePlate automated test suite.
    """

    if verbose:
        info("Running tests")
    django_run(c, "test", quiet_stdout=not verbose)

    print_success(message="Succesfully ran all tests")


@task
def serve_backend(c: Context) -> None:
    """
    Start the backend development server.
    """
    info("Running backend server")

    django_run(c, "runserver")


@task
def serve_frontend(c: Context) -> None:
    """
    Start the frontend development server.
    """
    info("Running frontend server")

    npm_run(c, "run dev")


@task
def generate_api(c: Context) -> None:
    """
    Generate the frontend API client from the Django OpenAPI schema.
    """
    schema_path = BASE_DIR / "frontend" / "openapi.yaml"

    with c.cd(BASE_DIR / "backend"):
        uv_run(
            c,
            f"python manage.py spectacular --file {schema_path}",
        )

    npm_run(c, "run api:generate")

    print_success("Frontend API generated")
