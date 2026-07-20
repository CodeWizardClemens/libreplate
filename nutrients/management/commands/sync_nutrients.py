from django.core.management.base import BaseCommand
from nutrients.services import sync_default_nutrients


class Command(BaseCommand):
    help = "Sync default nutrients"

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Update existing nutrients with default values",
        )

    def handle(self, *args, **options):
        force = options["force"]

        sync_default_nutrients(force=force)

        if force:
            self.stdout.write(
                self.style.SUCCESS("Nutrients synced with updates applied.")
            )
        else:
            self.stdout.write(
                self.style.SUCCESS("Nutrients synced without overwriting existing data.")
            )