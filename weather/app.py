import typing
from concurrent import futures

import grpc

import grpc_config.weather_pb2 as weather_pb2
import grpc_config.weather_pb2_grpc as weather_pb2_grpc
from weather.weather_client import WeatherAppClient


class MyWeatherService(weather_pb2_grpc.WeatherServiceServicer):
    def GetWeatherData(self, request, context) -> typing.Any:  # noqa: ANN001
        print(
            f"Getting weather for {request.latitude} {request.longitude}"
            f" at {request.start_date}"
        )

        result = WeatherAppClient().get_weather_forecast(
            latitude=request.latitude,
            longitude=request.longitude,
            start_date=request.start_date,
        )

        print(
            f"Weather for {request.latitude} {request.longitude}"
            f" at {request.start_date} is fetched successfully."
        )

        return weather_pb2.WeatherResponse(
            temperature=result.temperature,
            pressure=result.pressure_mmhg,
            windSpeed=result.wind_speed,
            windDirection=result.wind_direction_text,
            humidity=result.humidity,
        )


def serve() -> None:
    """Run grpc server."""
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    weather_pb2_grpc.add_WeatherServiceServicer_to_server(
        MyWeatherService(), server
    )
    server.add_insecure_port("weather:50051")

    print("Server is running now")
    server.start()
    server.wait_for_termination()
    print("Grpc is stopped now, termination....")


if __name__ == "__main__":
    serve()
