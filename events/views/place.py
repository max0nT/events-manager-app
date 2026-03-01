from django.db.models import QuerySet
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from ..models import Place
from ..serializers import PlaceSerializer


class PlaceViewSet(ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self) -> QuerySet:
        """Allow to show places for admin only.

        It's needed to avoid OpenApi spec validation error.

        """
        if self.request.user.is_superuser:
            return super().get_queryset()
        return Place.objects.none()
