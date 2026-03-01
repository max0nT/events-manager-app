from django.contrib.gis.db import models


class Place(models.Model):
    """Model class to describe place which is used for event's location."""

    name = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    rating = models.IntegerField()

    def __str__(self):
        return self.name
