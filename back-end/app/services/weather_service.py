import requests
from flask import current_app


def fetch_weather(lat: float, lon: float) -> dict:
    """Fetch current weather from WeatherAPI and map to ML-compatible format."""
    api_key = current_app.config["WEATHERAPI_KEY"]
    if not api_key:
        raise ValueError("WEATHERAPI_KEY is not configured")

    url = "https://api.weatherapi.com/v1/current.json"
    params = {"key": api_key, "q": f"{lat},{lon}", "aqi": "yes"}
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()
    return map_weather_for_ml(data)


def map_weather_for_ml(weatherapi_response: dict) -> dict:
    """Map WeatherAPI field names to ML service field names."""
    current = weatherapi_response["current"]
    try:
        pm25 = current["air_quality"]["pm2_5"]
    except (KeyError, TypeError):
        pm25 = 0.0

    return {
        "temperature": current["temp_c"],
        "humidity": current["humidity"],
        "uv_index": current["uv"],
        "pm25": pm25,
    }
