from io import BytesIO

import django_pydantic_field
import pydantic
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.db import models
from PIL import Image

User = get_user_model()


class WeatherData(pydantic.BaseModel):
    """Pydantic model to describe weather data for event."""

    temperature: float
    humidity: int
    pressure_hpa: float
    wind_speed: float
    wind_direction: str


class Event(models.Model):
    """Model class to describe events."""

    class Status(models.TextChoices):
        """Describe event status."""

        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"
        FINISHED = "finished", "Finished"

    name = models.CharField(max_length=255)
    description = models.TextField()
    publication_datetime = models.DateTimeField()
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    place = models.ForeignKey("events.Place", on_delete=models.CASCADE)

    rating = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=Status.choices)

    preview_image = models.ImageField(upload_to="previews/")

    weather_data = django_pydantic_field.SchemaField(
        schema=WeatherData,
        null=True,
    )

    def save(self, *args, **kwargs) -> None:
        """Save with resize preview image."""
        self.resize_preview_image()
        super().save(*args, **kwargs)

    def resize_preview_image(self) -> None:
        """Reduce preview image if it's too large."""
        if not self.preview_image:
            return

        img = Image.open(self.preview_image)
        min_side = min(img.size)

        if min_side <= 200:
            return

        ratio = 200 / min_side
        new_size = (
            int(img.width * ratio),
            int(img.height * ratio),
        )

        img = img.resize(new_size, Image.Resampling.LANCZOS)

        buffer = BytesIO()
        img.save(buffer, format="JPEG", quality=85)
        buffer.seek(0)

        self.preview_image.save(
            self.preview_image.name, ContentFile(buffer.read()), save=False
        )


class EventImage(models.Model):
    """Model class to describe attached images for events."""

    event = models.ForeignKey(
        "events.Event",
        on_delete=models.CASCADE,
        related_name="images",
    )
    image = models.ImageField(upload_to="events/")
