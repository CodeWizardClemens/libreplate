from django.core.management.base import BaseCommand

from units.services import sync_default_units


class Command(BaseCommand):
    def handle(self, *args, **options):
        sync_default_units()
