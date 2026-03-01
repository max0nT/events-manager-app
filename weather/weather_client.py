import httpx
import pydantic

WEATHER_DIRECTIONS = (
    "С",
    "СВ",
    "В",
    "ЮВ",
    "Ю",
    "ЮЗ",
    "З",
    "СЗ",
)


class WeatherData(pydantic.BaseModel):
    temperature: float
    humidity: int
    pressure_hpa: float
    wind_speed: float
    wind_direction_deg: int

    @property
    def wind_direction_text(self) -> str:
        """Define wind directions."""
        index = int((self.wind_direction_deg + 22.5) // 45) % 8
        return WEATHER_DIRECTIONS[index]

    @property
    def pressure_mmhg(self) -> float:
        """Translate to mmhq format."""
        return round(self.pressure_hpa * 0.75006, 1)


class WeatherAppClient:
    """Api client to get weather forecast."""

    def get_weather_forecast(
        self,
        latitude: float,
        longitude: float,
        start_date: str,
    ) -> WeatherData:
        """Get weather data."""
        with httpx.Client(base_url="https://api.open-meteo.com") as client:
            params = {
                "latitude": latitude,
                "longitude": longitude,
                "start_date": start_date,
                "end_date": start_date,
                "hourly": [
                    "temperature_2m",
                    "relative_humidity_2m",
                    "surface_pressure",
                    "wind_speed_10m",
                    "wind_direction_10m",
                ],
                "timezone": "auto",
            }

            response = client.get("/v1/forecast", params=params)

            response.raise_for_status()

            data = response.json()
        return WeatherData(
            temperature=data["hourly"]["temperature_2m"][0],
            humidity=data["hourly"]["relative_humidity_2m"][0],
            pressure_hpa=data["hourly"]["surface_pressure"][0],
            wind_speed=data["hourly"]["wind_speed_10m"][0],
            wind_direction_deg=data["hourly"]["wind_direction_10m"][0],
        )
