import os
import requests
import pandas as pd
from datetime import datetime
from pytz import timezone
from apscheduler.schedulers.blocking import BlockingScheduler
from google.cloud import storage
import logging

# Set up logging
logging.basicConfig(
    filename="../log/daily_data_collection.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Set Google Cloud credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/gim-yeji/Downloads/service_account.json"

# Configure Google Cloud Storage
BUCKET_NAME = "my-iot-project-data-bucket"
storage_client = storage.Client()

# OpenWeather API configuration
OPENWEATHER_API_KEY = "e8dcaeb7b872e2cdd1df5696c4bd87ca"
OPENWEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# TransportAPI configuration
TRANSPORT_BASE_URL = "https://transportapi.com/v3/uk/"
TRANSPORT_APP_ID = "ec65c482"
TRANSPORT_APP_KEY = "87d5e066137cb00e38a1cd3d1c5651f1"

# Function to fetch current weather data
def fetch_current_weather(lat, lon):
    """
    Fetch current weather data for a specific latitude and longitude.
    """
    params = {
        "lat": lat,
        "lon": lon,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric"  # Return temperature in Celsius
    }

    try:
        print(f"Fetching weather data for lat={lat}, lon={lon}...")
        response = requests.get(OPENWEATHER_BASE_URL, params=params)
        if response.status_code == 200:
            data = response.json()
            print("Weather data successfully fetched!")
            logging.info("Weather data successfully fetched.")
            return {
                "datetime": datetime.now(),
                "temperature": data["main"]["temp"],
                "humidity": data["main"]["humidity"],
                "pressure": data["main"]["pressure"],
                "wind_speed": data["wind"]["speed"],
                "weather_description": data["weather"][0]["description"],
                "latitude": lat,
                "longitude": lon
            }
        else:
            print(f"Failed to fetch weather data: {response.status_code}, {response.text}")
            logging.error(f"Failed to fetch weather data: {response.status_code}, {response.text}")
            return {}
    except Exception as e:
        print(f"Error fetching weather data: {e}")
        logging.error(f"Error fetching weather data: {e}")
        return {}

# Function to fetch TransportAPI data for a specific ATCO code
def fetch_live_departures(atco_code):
    """
    Fetch live bus departures for a specific ATCO code using TransportAPI.
    """
    url = f"{TRANSPORT_BASE_URL}bus/stop/{atco_code}/live.json"
    params = {
        "app_id": TRANSPORT_APP_ID,
        "app_key": TRANSPORT_APP_KEY,
        "group": "route",
        "nextbuses": "yes"
    }
    try:
        print(f"Fetching transport data for ATCO code {atco_code}...")
        response = requests.get(url, params=params)
        if response.status_code == 200:
            departures = []
            for service in response.json().get("departures", {}).values():
                for departure in service:
                    departures.append({
                        "atco_code": atco_code,
                        "line": departure.get("line"),
                        "direction": departure.get("direction"),
                        "operator": departure.get("operator"),
                        "destination": departure.get("destination_name"),
                        "best_departure_estimate": departure.get("best_departure_estimate"),
                        "source": departure.get("source")
                    })
            print(f"Transport data successfully fetched for ATCO code {atco_code}.")
            logging.info(f"Transport data successfully fetched for ATCO code {atco_code}.")
            return pd.DataFrame(departures)
        else:
            print(f"Failed to fetch transport data for {atco_code}: {response.status_code}, {response.text}")
            logging.error(f"Failed to fetch transport data for {atco_code}: {response.status_code}, {response.text}")
            return pd.DataFrame()
    except Exception as e:
        print(f"Error fetching transport data for {atco_code}: {e}")
        logging.error(f"Error fetching transport data for {atco_code}: {e}")
        return pd.DataFrame()

# Function to save data to a CSV file and upload to GCS
def save_and_upload(data, file_name):
    """
    Save data to CSV and upload to Google Cloud Storage.
    """
    try:
        # Save locally
        data.to_csv(file_name, index=False)
        print(f"{file_name} saved locally.")
        logging.info(f"{file_name} saved locally.")

        # Upload to GCS
        bucket = storage_client.bucket(BUCKET_NAME)
        blob = bucket.blob(file_name)
        blob.upload_from_filename(file_name)
        print(f"{file_name} uploaded to GCS.")
        logging.info(f"{file_name} uploaded to GCS.")
    except Exception as e:
        print(f"Failed to save or upload {file_name}: {e}")
        logging.error(f"Failed to save or upload {file_name}: {e}")

# Scheduler setup
def start_scheduler():
    """
    Start APScheduler to run the data collection daily at specific times.
    """
    scheduler = BlockingScheduler()

    # Weather data collection at specific time
    scheduler.add_job(
        func=lambda: save_and_upload(
            pd.DataFrame([fetch_current_weather(51.5074, -0.1278)]),  # London
            f"weather_data_{datetime.now().strftime('%Y-%m-%d')}.csv"
        ),
        trigger="cron",
        hour=15,
        minute=37,
        timezone=timezone('Europe/London'),
    )

    # Transport data collection at specific time
    scheduler.add_job(
        func=lambda: save_and_upload(
            pd.concat([fetch_live_departures(atco) for atco in ["0100BRP90310", "0100BRP90312"]]),
            f"transport_data_{datetime.now().strftime('%Y-%m-%d')}.csv"
        ),
        trigger="cron",
        hour=15,
        minute=38,
        timezone=timezone('Europe/London'),

    )

    logging.info("Scheduler started. Weather and Transport data collection jobs added.")
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logging.info("Scheduler stopped.")

# Main execution
if __name__ == "__main__":
    start_scheduler()