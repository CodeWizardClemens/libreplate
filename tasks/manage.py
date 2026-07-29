from invoke import Context, task

from .db import migrate
from .utils import info


@task
def update(c: Context):
    """
    Update LibrePlate dependencies, source code, and database state.
    """
    info("Updating LibrePlate")

    c.run("git pull origin master")
    c.run("uv sync")

    migrate(c)
