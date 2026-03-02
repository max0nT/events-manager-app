from django.db.models import QuerySet
from import_export_extensions import fields, resources

from events.filters import EventExportFilter

from .models import Event, Place


class EventResource(resources.CeleryModelResource):
    """Resource class for events import/export."""

    filterset_class = EventExportFilter

    # Fields for import events
    place_name = fields.Field(
        column_name="Название места проведения",
        attribute="place__name",
    )
    latitude = fields.Field(
        column_name="Гео-координаты: широта",
        attribute="place__latitude",
    )
    longitude = fields.Field(
        column_name="Гео-координаты: долгота",
        attribute="place__longitude",
    )

    # General fields
    name = fields.Field(
        column_name="Название",
        attribute="name",
    )
    description = fields.Field(
        column_name="Описание",
        attribute="description",
    )
    publication_datetime = fields.Field(
        column_name="Дата и время публикации",
        attribute="publication_datetime",
    )
    start_datetime = fields.Field(
        column_name="Дата и время начала проведения",
        attribute="start_datetime",
    )
    end_datetime = fields.Field(
        column_name="Дата и время завершения проведения",
        attribute="end_datetime",
    )
    rating = fields.Field(
        column_name="Рейтинг",
        attribute="rating",
    )

    class Meta:  # noqa: D106
        model = Event
        fields = (
            "id",
            "place_name",
            "name",
            "latitude",
            "longitude",
            "description",
            "publication_datetime",
            "start_datetime",
            "end_datetime",
            "rating",
        )

        export_order = fields
        import_id_fields = ("id",)

    def before_import_row(self, row: dict, **kwargs) -> None:
        """Create `Place` instance before event place.."""
        place_name = row.get("Название места проведения")
        lat = row.get("Гео-координаты: широта", 0)
        lon = row.get("Гео-координаты: долгота", 0)

        if place_name:
            place, _ = Place.objects.get_or_create(
                name=place_name,
                defaults={"latitude": lat, "longitude": lon, "rating": 0},
            )
            row["place"] = place.id

        user = kwargs.get("user")
        if user := kwargs.get("user"):
            row["author"] = user.id

    def get_export_queryset(self, **kwargs) -> QuerySet:
        """Add select related for place and author."""
        return (
            super()
            .get_export_queryset(**kwargs)
            .select_related("place", "author")
        )
