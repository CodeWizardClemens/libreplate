from invoke import Context, task

from .utils import django_run, log


@task
def migrate(c: Context):
    """
    Create and apply Django migrations.
    """
    log("Creating and applying migrations")

    django_run(c, "makemigrations")
    django_run(c, "migrate")


@task(name="sync-default-data")
def sync_default_data(c: Context):
    """
    Synchronize default application data.
    """
    log("Syncing default data")

    for command in [
        "sync_nutrients",
        "sync_units",
        "sync_body_metrics",
    ]:
        django_run(c, command)