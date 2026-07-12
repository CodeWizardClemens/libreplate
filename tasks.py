from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

from invoke import task

APP_NAME = "libreplate"

BASE_DIR = Path(__file__).parent.resolve()
VENV_DIR = BASE_DIR / ".venv"
ENV_FILE = BASE_DIR / ".env"

PYTHON = sys.executable
PYTHON_REQUIRED = (3, 10)
POSTGRES_REQUIRED = 13


def log(message: str):
    print(f"\n==> {message}")


def fail(message: str):
    raise SystemExit(f"\nERROR: {message}")

# TODO replace run command with default c.run, but add fail message to all
# invoke runs.
def run(command, env=None):
    try:
        subprocess.run(command, check=True, env=env)
    except subprocess.CalledProcessError as e:
        cmd = " ".join(map(str, e.cmd))
        fail(f"Command failed (exit code {e.returncode}):\n\n    {cmd}")

def venv_python():
    if os.name == "nt":
        return VENV_DIR / "Scripts" / "python.exe"
    return VENV_DIR / "bin" / "python"


def load_env():
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text().splitlines():
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                os.environ.setdefault(k, v)


@task
def check_python(c):
    log("Checking Python")

    version = sys.version_info[:2]

    print(f"Python version: {version[0]}.{version[1]}")

    if version < PYTHON_REQUIRED:
        fail(
            f"Python {PYTHON_REQUIRED[0]}.{PYTHON_REQUIRED[1]}+ required"
        )

    print("Python version OK")


@task
def check_postgresql(c):
    log("Checking PostgreSQL")

    try:
        result = subprocess.run(
            ["psql", "--version"],
            capture_output=True,
            text=True,
            check=True,
        )
    except FileNotFoundError:
        fail("psql not installed")

    version = result.stdout.split()[2]
    major = int(version.split(".")[0])

    print(f"PostgreSQL version: {version}")

    if major < POSTGRES_REQUIRED:
        fail(f"PostgreSQL {POSTGRES_REQUIRED}+ required")

    print("PostgreSQL version OK")


@task
def create_directories(c):
    log("Creating directories")

    for directory in ("uploads", "static", "logs"):
        (BASE_DIR / directory).mkdir(parents=True, exist_ok=True)

    print("Directories OK")


@task
def create_virtualenv(c):
    log("Creating virtual environment")

    if not VENV_DIR.exists():
        run([PYTHON, "-m", "venv", str(VENV_DIR)])
        print("Virtual environment created")
    else:
        print("Virtual environment already exists")


@task(pre=[create_virtualenv])
def install_dependencies(c):
    log("Installing dependencies")

    requirements = BASE_DIR / "requirements.txt"

    if not requirements.exists():
        fail("requirements.txt not found")

    lines = [
        l for l in requirements.read_text().splitlines()
        if l.strip() and not l.startswith("#")
    ]

    if not all("==" in line for line in lines):
        fail("requirements.txt must contain pinned versions")

    python = str(venv_python())

    run([python, "-m", "pip", "install", "--upgrade", "pip", "setuptools", "wheel"])
    run([python, "-m", "pip", "install", "-r", str(requirements)])


@task
def migrate(c):
    if not (BASE_DIR / "manage.py").exists():
        print("No Django project detected")
        return

    load_env()
    log("Running migrations")
    python = str(venv_python())
    run([python, "manage.py", "makemigrations"])
    run([python, "manage.py", "migrate", "--noinput"])
    log("Collecting static")
    run([python, "manage.py", "collectstatic", "--noinput"])


@task
def create_admin(c, password):
    if not password:
        fail("--password is required")

    if not (BASE_DIR / "manage.py").exists():
        print("No Django project detected")
        return

    load_env()

    log("Creating admin user")

    env = os.environ.copy()
    env["DJANGO_SUPERUSER_USERNAME"] = "admin"
    env["DJANGO_SUPERUSER_EMAIL"] = ""
    env["DJANGO_SUPERUSER_PASSWORD"] = password

    try:
        run(
            [
                str(venv_python()),
                "manage.py",
                "createsuperuser",
                "--noinput",
            ],
            env=env,
        )
    except subprocess.CalledProcessError:
        print("Admin user already exists")


@task
def sync_default_data(c):
    load_env()
    c.run("python manage.py sync_nutrients")
    c.run("python manage.py sync_units")


@task
def add_user(
    c,
    username,
    first_name,
    last_name,
    email,
    password,
):
    """
    Create a normal Django user.
    """

    load_env()

    script = f"""
from django.contrib.auth import get_user_model

User = get_user_model()

if User.objects.filter(username="{username}").exists():
    print("User already exists")
else:
    user = User.objects.create_user(
        username="{username}",
        email="{email}",
        password="{password}",
        first_name="{first_name}",
        last_name="{last_name}",
    )
    print(f"Created {{user.username}}")
"""

    run(
        [
            str(venv_python()),
            "manage.py",
            "shell",
            "-c",
            script,
        ]
    )


@task
def serve_dev(c, host="127.0.0.1", port=8000):
    """
    Run the application server for development.
    """
    load_env()
    python = VENV_DIR / "bin" / "python"
    run(
        [
            str(python),
            "manage.py",
            "runserver",
        ]
    )

@task
def test(c, app=None):
    """
    Run all tests, or tests for a specific app.

    Examples:
        inv test
        inv test --app units
    """

    load_env()
    log("Running tests")

    if not (BASE_DIR / "manage.py").exists():
        fail("No Django project detected")

    command = [
        str(venv_python()),
        "manage.py",
        "test",
    ]

    if app:
        command.append(app)

    run(command)

    print("Tests passed")


@task
def install(c):
    """
    Full installation.
    """

    check_python(c)
    check_postgresql(c)
    create_directories(c)
    create_virtualenv(c)
    install_dependencies(c)
    migrate(c)
    sync_default_data(c)

    print(
        f"""

Installation complete.

Activate:

    source {VENV_DIR}/bin/activate

Start:

    gunicorn libreplate.wsgi:application
"""
    )