# body_metrics/management/commands/sync_body_metrics.py

from body_metrics.services import sync_body_metrics
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        sync_body_metrics()
