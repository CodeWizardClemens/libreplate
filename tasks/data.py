from invoke import Context, task

from .utils import django_run, info


@task
def create_cache_table(c: Context) -> None:
    """
    Create the Django database cache table.
    """
    django_run(c, "createcachetable django_cache")


@task(aliases=["m"])
def migrate(c: Context):
    """
    Create and apply Django migrations.
    """
    info("Creating and applying migrations")

    django_run(c, "makemigrations")
    django_run(c, "migrate")


@task(aliases=["sd"])
def sync_default_data(c: Context, overwrite=False):
    """
    Synchronize default application data.
    """
    info("Syncing default data")

    for command in [
        "sync_default_nutrients",
        "sync_default_units",
        "sync_default_body_metrics",
    ]:
        full_command = command
        if overwrite:
            full_command += " --overwrite"

        django_run(c, full_command)
