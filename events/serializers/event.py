from rest_framework import serializers

from ..models import Event
from .event_image import EventImageSerializer
from .place import PlaceSerializer


class EventSerializer(serializers.ModelSerializer):
    """Serializer class for `Event` model."""

    images = EventImageSerializer(many=True, read_only=True)
    place = PlaceSerializer(read_only=True)

    class Meta:  # noqa: D106
        model = Event
        fields = "__all__"
