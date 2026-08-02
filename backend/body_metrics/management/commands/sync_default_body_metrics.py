from body_metrics.services import sync_default_body_metrics
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        sync_default_body_metrics()
