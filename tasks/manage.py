from invoke import Context, task

from .data import migrate
from .utils import info


@task(aliases=["u"])
def update(c: Context):
    """
    Update LibrePlate dependencies, source code, and database state.
    """
    info("Updating LibrePlate")

    c.run("git pull origin master")
    c.run("uv sync")

    migrate(c)
