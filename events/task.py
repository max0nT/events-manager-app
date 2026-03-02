import grpc
from celery import shared_task

from grpc_config import weather_pb2_grpc

from .models import Event
from .services.sync_event_with_weather import sync_event_with_weather


@shared_task
def sync_events_with_weather() -> None:
    """Sync events with weather data by weather api calling."""
    queryset = Event.objects.filter(weather_data__isnull=True)
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = weather_pb2_grpc.WeatherServiceStub(channel)
        for event in queryset:
            sync_event_with_weather(event, stub)
