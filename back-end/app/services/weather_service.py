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
    return map_weather_for_ml(data, lat=lat, lon=lon)


def get_weatherapi_location_name(location: dict) -> str:
    """WeatherAPI usually returns name + province, so this is only a fallback."""
    location_parts = [
        location.get("name"),
        location.get("region"),
    ]
    return ", ".join(part for part in location_parts if part)


def reverse_geocode_location_name(lat: float, lon: float) -> str | None:
    """Resolve GPS coordinates to a concise area + city label."""
    url = "https://nominatim.openstreetmap.org/reverse"
    params = {
        "format": "jsonv2",
        "lat": lat,
        "lon": lon,
        "zoom": 14,
        "addressdetails": 1,
    }
    headers = {
        "User-Agent": "SkinSenseAI-Capstone/1.0",
    }

    try:
        response = requests.get(url, params=params, headers=headers, timeout=5)
        response.raise_for_status()
        address = response.json().get("address", {})
    except Exception:
        return None

    area = (
        address.get("village")
        or address.get("suburb")
        or address.get("neighbourhood")
        or address.get("quarter")
        or address.get("hamlet")
        or address.get("city_district")
    )
    city = (
        address.get("city")
        or address.get("town")
        or address.get("municipality")
        or address.get("county")
    )

    if area and city and area.lower() != city.lower():
        return f"{area}, {city}"
    if city:
        return city
    if area:
        return area
    return None


def map_weather_for_ml(weatherapi_response: dict, lat: float | None = None, lon: float | None = None) -> dict:
    """Map WeatherAPI field names to ML service field names."""
    current = weatherapi_response["current"]
    location = weatherapi_response.get("location", {})
    try:
        pm25 = current["air_quality"]["pm2_5"]
    except (KeyError, TypeError):
        pm25 = 0.0

    location_name = None
    if lat is not None and lon is not None:
        location_name = reverse_geocode_location_name(lat, lon)
    location_name = location_name or get_weatherapi_location_name(location)

    return {
        "location_name": location_name or "Current location",
        "temperature": current["temp_c"],
        "humidity": current["humidity"],
        "uv_index": current["uv"],
        "pm25": pm25,
    }
