# custom_exporter.py

import time
import requests
from prometheus_client import start_http_server, Gauge

# === CONFIGURATION ===
API_KEY = "bb147ec1b4190fffc5e585d1ddb31c82"
UPDATE_INTERVAL = 20  # seconds
PORT = 8000

# List of cities with coordinates
CITIES = [
    {"name": "Ulaanbaatar", "lat": 47.9221, "lon": 106.91159},
    {"name": "Boston", "lat": 42.3555, "lon": -71.0565},
    {"name": "Paris", "lat": 48.8566, "lon": 2.3522},
    {"name": "Sydney", "lat": -33.8727, "lon": 151.2057},
]

# === DEFINE PROMETHEUS METRICS WITH CITY LABEL ===
weather_temp = Gauge("weather_temp_celsius", "Temperature in Celsius", ["city"])
weather_feels_like = Gauge("weather_feels_like_celsius", "Feels like temperature in Celsius", ["city"])
weather_pressure = Gauge("weather_pressure_hpa", "Pressure in hPa", ["city"])
weather_humidity = Gauge("weather_humidity_percent", "Humidity percentage", ["city"])
weather_dew_point = Gauge("weather_dew_point_celsius", "Dew point in Celsius", ["city"])
weather_clouds = Gauge("weather_clouds_percent", "Cloud coverage percentage", ["city"])
weather_wind_speed = Gauge("weather_wind_speed_m_s", "Wind speed in m/s", ["city"])
weather_wind_deg = Gauge("weather_wind_deg", "Wind direction in degrees", ["city"])
weather_sunrise = Gauge("weather_sunrise_timestamp", "Sunrise timestamp", ["city"])
weather_sunset = Gauge("weather_sunset_timestamp", "Sunset timestamp", ["city"])
weather_day_length = Gauge("weather_day_length_seconds", "Length of the day in seconds", ["city"])

# === FUNCTION TO FETCH AND UPDATE METRICS ===
def update_metrics():
    for city in CITIES:
        try:
            url = f"https://api.openweathermap.org/data/3.0/onecall?lat={city['lat']}&lon={city['lon']}&exclude=minutely,hourly,daily,alerts&appid={API_KEY}&units=metric"
            response = requests.get(url)
            data = response.json()
            current = data['current']

            # Update metrics with city label
            weather_temp.labels(city=city["name"]).set(current['temp'])
            weather_feels_like.labels(city=city["name"]).set(current['feels_like'])
            weather_pressure.labels(city=city["name"]).set(current['pressure'])
            weather_humidity.labels(city=city["name"]).set(current['humidity'])
            weather_dew_point.labels(city=city["name"]).set(current['dew_point'])
            weather_clouds.labels(city=city["name"]).set(current['clouds'])
            weather_wind_speed.labels(city=city["name"]).set(current['wind_speed'])
            weather_wind_deg.labels(city=city["name"]).set(current['wind_deg'])
            weather_sunrise.labels(city=city["name"]).set(current['sunrise'])
            weather_sunset.labels(city=city["name"]).set(current['sunset'])
            weather_day_length.labels(city=city["name"]).set(current['sunset'] - current['sunrise'])

            print(f"Metrics updated for {city['name']} at {time.strftime('%Y-%m-%d %H:%M:%S')}")
        except Exception as e:
            print(f"Error updating metrics for {city['name']}: {e}")

# === MAIN LOOP ===
if __name__ == "__main__":
    # Start Prometheus HTTP server
    start_http_server(PORT)
    print(f"Custom Exporter running on http://localhost:{PORT}/metrics")

    # Update metrics continuously
    while True:
        update_metrics()
        time.sleep(UPDATE_INTERVAL)
