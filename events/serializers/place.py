from rest_framework import serializers

from ..models import Place


class PlaceSerializer(serializers.ModelSerializer):
    """Serializer class for `Place` model."""

    class Meta:  # noqa: D106
        model = Place
        fields = "__all__"
