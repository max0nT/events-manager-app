from rest_framework import serializers

from ..models import EventImage


class EventImageSerializer(serializers.ModelSerializer):
    """Serializer class for `EventImage` model."""

    class Meta:  # noqa: D106
        model = EventImage
        fields = ["id", "image"]
