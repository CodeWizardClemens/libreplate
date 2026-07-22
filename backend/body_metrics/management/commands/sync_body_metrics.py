# body_metrics/management/commands/sync_body_metrics.py

from django.core.management.base import BaseCommand

from body_metrics.services import sync_body_metrics


class Command(BaseCommand):
    def handle(self, *args, **options):
        sync_body_metrics()
