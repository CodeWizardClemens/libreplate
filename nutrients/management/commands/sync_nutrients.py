# nutrients/management/commands/sync_nutrients.py

from django.core.management.base import BaseCommand
from nutrients.services import sync_default_nutrients


class Command(BaseCommand):
    def handle(self, *args, **options):
        sync_default_nutrients()