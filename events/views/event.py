import typing

from django.db.models import QuerySet
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from ..filters import EventFilter
from ..models import Event
from ..serializers import EventSerializer


class EventViewSet(ModelViewSet):
    queryset = Event.objects.select_related("place", "author")
    serializer_class = EventSerializer
    filterset_class = EventFilter
    permission_classes = (IsAuthenticated,)
    search_fields = ["name", "place__name"]
    ordering_fields = ["name", "start_datetime", "end_datetime"]

    def get_queryset(self) -> QuerySet:
        """Allow view only published events for unauthenticated users."""
        queryset = super().get_queryset()
        if self.request.user.is_superuser:
            return queryset

        return queryset.filter(status="published")

    def get_permissions(self) -> tuple[typing.Any, ...]:
        """Allow make not safe method for admin only."""
        if self.action in ("create", "update", "destroy"):
            return (IsAdminUser(),)
        return super().get_permissions()
