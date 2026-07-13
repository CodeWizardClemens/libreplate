# body_metrics/services.py

from .defaults import DEFAULT_BODY_METRICS
from .models import BodyMetric


def sync_body_metrics():
    for body_metric in DEFAULT_BODY_METRICS:
        print(body_metric)
        BodyMetric.objects.get_or_create(
            name=body_metric.name,
            defaults=body_metric.model_dump(exclude={"name"}),
        )