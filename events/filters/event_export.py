from django_filters import rest_framework as filters

from ..models import Event


class EventExportFilter(filters.FilterSet):
    """Filter set class for `Event` model."""

    class Meta:  # noqa: D106
        model = Event
        fields = {
            "publication_datetime": (
                "gte",
                "lte",
            ),
            "start_datetime": (
                "gte",
                "lte",
            ),
            "end_datetime": (
                "gte",
                "lte",
            ),
            "place": ("exact",),
        }
