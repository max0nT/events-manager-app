import datetime

import grpc
from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage, get_connection

from grpc_config import weather_pb2_grpc

from .models import Event
from .services.sync_event_with_weather import sync_event_with_weather

User = get_user_model()


@shared_task
def sync_events_with_weather() -> None:
    """Sync events with weather data by weather api calling."""
    queryset = Event.objects.filter(weather_data__isnull=True)
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = weather_pb2_grpc.WeatherServiceStub(channel)
        for event in queryset:
            sync_event_with_weather(event, stub)


@shared_task
def send_email_about_events() -> None:
    """Send email about events to users."""
    today = datetime.date.today()
    users = User.objects.filter(email__isnull=False).values("email", flat=True)

    events_today = Event.objects.filter(
        status=Event.Status.PUBLISHED,
        start_datetime__date=today,
    )

    subject = f"События и погода на сегодня ({today})"
    body = "Вот что ждет нас сегодня:\n\n"
    # Make email about all starting events for a day
    for event in events_today:
        w = event.weather_data
        weather_info = (
            f"🌡 Температура: {w.temperature}°C\n"
            f"💧 Влажность: {w.humidity}%\n"
            f"🌬 Ветер: {w.wind_speed} м/с, направление: {w.wind_direction}\n"
            f"⏲ Давление: {w.pressure_hpa} hPa"
        )

        body += f"🔹 {event.name} (Место: {event.place})\n{weather_info}\n"
        body += f"---"

    with get_connection() as connection:
        email = EmailMessage(
            subject=subject,
            body=body,
            from_email=None,
            to=users,
            connection=connection,
        )
        email.bcc = users
        email.to = ["noreply@yourdomain.com"]
        email.send()
