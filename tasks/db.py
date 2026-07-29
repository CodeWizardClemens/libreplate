from invoke import Context, task

from .utils import django_run, info


@task
def migrate(c: Context):
    """
    Create and apply Django migrations.
    """
    info("Creating and applying migrations")

    django_run(c, "makemigrations")
    django_run(c, "migrate")


@task(aliases=["sd"])
def sync_default_data(c: Context):
    """
    Synchronize default application data.
    """
    info("Syncing default data")

    for command in [
        "sync_nutrients",
        "sync_units",
        "sync_default_body_metrics",
    ]:
        django_run(c, command)
