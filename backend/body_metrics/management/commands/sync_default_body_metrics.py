from django.core.management.base import BaseCommand

from body_metrics.services import sync_default_body_metrics


class Command(BaseCommand):
    def handle(self, *args, **options):
        sync_default_body_metrics()
