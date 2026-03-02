import grpc

from events.models import Event, WeatherData
from grpc_config import weather_pb2, weather_pb2_grpc


def sync_event_with_weather(
    event: Event,
    stub: weather_pb2_grpc.WeatherServiceStub,
) -> None:
    """Sync weather data with event."""
    try:
        request_body = weather_pb2.WeatherRequest(
            latitude=event.place.latitude,
            longitude=event.place.longitude,
            start_date=event.start_datetime.date().strftime("%Y-%m-%d"),
        )
        response = stub.GetWeatherData(request_body)
    except grpc.RpcError as e:
        print(
            f"Error during sync with weather api gRPC: {e.code()} - {e.details()}"
        )
        return
    event.weather_data = WeatherData(
        temperature=response.temperature,
        pressure_hpa=response.pressure,
        humidity=response.humidity,
        wind_speed=response.windSpeed,
        wind_direction=response.windDirection,
    )
    event.save()
