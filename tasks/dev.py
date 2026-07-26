from invoke import Context, task

from .utils import BASE_DIR, IS_DEBUG, VENV_DIR, django_run, log


@task(name="check-code-quality")
def check_code_quality(c: Context):
    """
    Run code quality checks.
    """
    log("Checking code quality. This may take a while.")

    c.run(
        f"isort {BASE_DIR} --check-only --skip {VENV_DIR}"
    )
    c.run(
        f"black {BASE_DIR} --check --exclude '{VENV_DIR}'"
    )
    c.run(
        f"ruff check {BASE_DIR} --exclude {VENV_DIR}"
    )


@task(name="format-code")
def format_code(c: Context):
    """
    Automatically format the codebase.
    """
    c.run(
        f"isort {BASE_DIR} --skip {VENV_DIR}"
    )
    c.run(
        f"black {BASE_DIR} --exclude '{VENV_DIR}'"
    )
    c.run(
        f"ruff format {BASE_DIR} --exclude {VENV_DIR}"
    )


@task
def test(c: Context):
    """
    Run the LibrePlate automated test suite.
    """
    log("Running tests")
    django_run(c, "test")


@task
def serve(c: Context):
    """
    Start the LibrePlate web server.
    """
    log("Running server")

    if IS_DEBUG:
        django_run(c, "runserver")
    else:
        c.run("uv run gunicorn libreplate.wsgi:application")