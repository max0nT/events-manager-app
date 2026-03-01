import django_filters

from events.models import Event


class EventFilter(django_filters.FilterSet):
    """Filter class for event API."""

    start_datetime = django_filters.DateTimeFromToRangeFilter()
    end_datetime = django_filters.DateTimeFromToRangeFilter()

    rating = django_filters.RangeFilter()
    place = django_filters.ModelMultipleChoiceFilter(
        field_name="place",
    )

    class Meta:  # noqa: D106
        model = Event
        fields = [
            "start_datetime",
            "end_datetime",
            "rating",
            "place",
        ]
